#!/usr/bin/env python3
"""SciHarness UI: drop papers, build tasks, run the harness, validate accuracy, judge, promote versions.

    python ui/server.py            # http://localhost:8765

All state lives in the repo (tasks/uploads, evalkit/truth/uploads, runs/, evolve/ledger.jsonl).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "evalkit"))
from evalkit.score import score_run, truth_path_for  # noqa: E402
from evalkit.judge import judge_run  # noqa: E402
from harness.config import load_model_config  # noqa: E402
from harness.llm import LLM  # noqa: E402
from tasks.generator.make_tasks import TOL  # noqa: E402

app = FastAPI(title="SciHarness")
UPLOADS = ROOT / "tasks" / "uploads"
UPLOAD_TRUTH = ROOT / "evalkit" / "truth" / "uploads"
JOBS: dict[str, dict] = {}

BUILDER_SYSTEM = """You turn a scientific paper into a reproducibility task. You receive the paper text and, if provided,
the column names and a sample of the accompanying dataset.

Produce a single JSON object:
{
 "title": "...",
 "claims": [ {"id": "<snake_case_id>", "description": "<what the number is, precisely, incl. group/scale>",
              "type": "count|mean|sd|diff|stat|pvalue|effect|coef|se|ratio|ci|r2|corr|prop", "value": <number as reported>} ],
 "methods_view": "<markdown: abstract + full methods + results section with EVERY number replaced by [claim_id] placeholders. Keep all methodological detail. No numeric results may remain.>",
 "data_dictionary": "<markdown list of columns and meanings inferred from the paper and the sample; if no data was provided, list the variables the paper describes>",
 "data_available": true|false,
 "notes": "<anything ambiguous a reproducer must know>"
}
Rules: only include claims that can be recomputed from the described data (no citations, no external numbers).
Use 'p<0.001' style values as 0.0005 with type pvalue. Prefer 5-15 claims covering the main analyses.
"""


def pdf_text(path: Path) -> str:
    import pymupdf
    return "\n".join(page.get_text() for page in pymupdf.open(str(path)))


def list_split(split: str) -> list[dict]:
    base = ROOT / "tasks" / split
    out = []
    if not base.exists():
        return out
    for p in sorted(base.iterdir()):
        if p.is_dir() and (p / "task.json").exists():
            t = json.loads((p / "task.json").read_text())
            out.append({"task_id": t["task_id"], "split": split, "title": t.get("title", ""), "n_claims": len(t.get("claims", [])),
                        "has_truth": truth_path_for(p).exists(), "status": t.get("status", "ready")})
        elif p.is_dir() and (p / "upload.json").exists():
            out.append({**json.loads((p / "upload.json").read_text()), "split": split, "has_truth": False})
    return out


def current_harness_commit() -> str:
    try:
        return subprocess.run(["git", "log", "-1", "--format=%h %s", "--", "harness"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


# ------------------------------------------------------------------------------- static
app.mount("/static", StaticFiles(directory=str(ROOT / "ui" / "static")), name="static")


@app.get("/")
def index():
    return FileResponse(str(ROOT / "ui" / "static" / "index.html"))


# ------------------------------------------------------------------------------- tasks
@app.get("/api/tasks")
def api_tasks():
    return {"splits": {s: list_split(s) for s in ("uploads", "dev", "feedback", "heldout")}}


@app.post("/api/upload")
async def api_upload(paper: UploadFile = File(...), data: UploadFile | None = File(None), truth: UploadFile | None = File(None),
                     name: str = Form("")):
    slug = re.sub(r"[^a-z0-9]+", "_", (name or Path(paper.filename).stem).lower()).strip("_")[:40] or "paper"
    tid = f"up_{slug}_{uuid.uuid4().hex[:6]}"
    d = UPLOADS / tid
    d.mkdir(parents=True)
    raw = d / "raw"
    raw.mkdir()
    suffix = Path(paper.filename).suffix.lower() or ".pdf"
    (raw / f"paper{suffix}").write_bytes(await paper.read())
    meta = {"task_id": tid, "title": name or Path(paper.filename).stem, "status": "uploaded", "paper_file": f"raw/paper{suffix}",
            "data_file": None, "truth_file": None, "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    if data and data.filename:
        (raw / "data.csv").write_bytes(await data.read())
        meta["data_file"] = "raw/data.csv"
    if truth and truth.filename:
        (raw / "truth.json").write_bytes(await truth.read())
        meta["truth_file"] = "raw/truth.json"
    (d / "upload.json").write_text(json.dumps(meta, indent=2))
    return meta


@app.post("/api/build_task/{tid}")
def api_build_task(tid: str):
    d = UPLOADS / tid
    if not (d / "upload.json").exists():
        raise HTTPException(404, "unknown upload")
    meta = json.loads((d / "upload.json").read_text())
    paper_path = d / meta["paper_file"]
    text = pdf_text(paper_path) if paper_path.suffix.lower() == ".pdf" else paper_path.read_text(errors="replace")
    sample = ""
    if meta.get("data_file"):
        import pandas as pd
        df = pd.read_csv(d / meta["data_file"])
        sample = f"columns: {list(df.columns)}\nshape: {df.shape}\nhead:\n{df.head(8).to_string()}\ndtypes:\n{df.dtypes.to_string()}"
    llm = LLM(load_model_config(str(ROOT / "configs" / "judge.json")))
    user = "=== PAPER TEXT ===\n" + text[:60000] + "\n\n=== DATA SAMPLE ===\n" + (sample or "(no dataset provided)")
    raw = llm.chat(BUILDER_SYSTEM, [{"role": "user", "content": user}], max_tokens=12000)
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        spec = json.loads(m.group(0) if m else raw)
    except json.JSONDecodeError:
        raise HTTPException(500, f"task builder returned non-JSON: {raw[:500]}")
    # user-provided truth overrides extracted values
    truth_vals = {}
    if meta.get("truth_file"):
        tv = json.loads((d / meta["truth_file"]).read_text())
        items = tv.get("claims", tv)
        truth_vals = {c["id"]: c["value"] for c in items} if isinstance(items, list) else dict(items)
    claims = []
    for c in spec.get("claims", []):
        ctype = c.get("type") if c.get("type") in TOL else "stat"
        val = truth_vals.get(c["id"], c.get("value"))
        claims.append({"id": c["id"], "description": c.get("description", ""), "type": ctype, "value": val})
    task = {"task_id": tid, "family": "reproduce_analysis", "title": spec.get("title", meta["title"]),
            "instructions": ("Reproduce the analysis described in paper_methods.md using data.csv. Follow the Methods exactly. "
                             "Produce a numeric value for every claim slot. Write claims.json and analysis.py (prints the claims as one JSON object)."),
            "paper_view": "paper_methods.md", "data_files": ["data.csv"] if meta.get("data_file") else [],
            "data_dictionary": "data_dictionary.md", "notes": spec.get("notes", ""),
            "claims": [{k: c[k] for k in ("id", "description", "type")} for c in claims],
            "output": {"claims_file": "claims.json", "analysis_script": "analysis.py"}, "status": "ready"}
    (d / "task.json").write_text(json.dumps(task, indent=2) + "\n")
    (d / "paper_methods.md").write_text(spec.get("methods_view", ""))
    (d / "data_dictionary.md").write_text(spec.get("data_dictionary", ""))
    if meta.get("data_file"):
        shutil.copy(d / meta["data_file"], d / "data.csv")
    td = UPLOAD_TRUTH / tid
    td.mkdir(parents=True, exist_ok=True)
    (td / "truth.json").write_text(json.dumps({"task_id": tid, "analysis": "uploaded", "source": "paper-reported values" + (" + user truth" if truth_vals else ""),
                                               "claims": [{"id": c["id"], "value": c["value"], "type": c["type"], "tolerance": TOL[c["type"]]} for c in claims if c["value"] is not None]}, indent=2) + "\n")
    (td / "paper_full.md").write_text(text)
    if paper_path.suffix.lower() == ".pdf":
        shutil.copy(paper_path, td / "paper.pdf")
    meta["status"] = "ready"
    (d / "upload.json").write_text(json.dumps(meta, indent=2))
    return {"task": task, "truth_claims": len([c for c in claims if c["value"] is not None]), "builder_usage": llm.usage(), "notes": spec.get("notes", "")}


@app.get("/api/task/{split}/{tid}")
def api_task(split: str, tid: str):
    d = ROOT / "tasks" / split / tid
    if not (d / "task.json").exists():
        raise HTTPException(404)
    task = json.loads((d / "task.json").read_text())
    tp = truth_path_for(d)
    truth = json.loads(tp.read_text()) if tp.exists() else None
    full = tp.parent / "paper_full.md"
    return {"task": task, "truth": truth, "paper_methods": (d / "paper_methods.md").read_text() if (d / "paper_methods.md").exists() else "",
            "paper_full": full.read_text()[:20000] if full.exists() else "", "has_pdf": (tp.parent / "paper.pdf").exists()}


@app.get("/api/pdf/{split}/{tid}")
def api_pdf(split: str, tid: str):
    p = truth_path_for(ROOT / "tasks" / split / tid).parent / "paper.pdf"
    if not p.exists():
        raise HTTPException(404)
    return FileResponse(str(p), media_type="application/pdf")


# ------------------------------------------------------------------------------- runs
def _run_job(job_id: str, split: str, tid: str, harness_ref: str):
    job = JOBS[job_id]
    try:
        harness_dir = ROOT / "harness"
        if harness_ref and harness_ref != "current":
            hd = ROOT / "runs" / "_harness_snapshots" / harness_ref
            if not hd.exists():
                hd.mkdir(parents=True)
                subprocess.run(f"git archive {harness_ref} harness | tar -x -C {hd}", shell=True, cwd=ROOT, check=True)
            harness_dir = hd / "harness"
        task_dir = ROOT / "tasks" / split / tid
        run_dir = ROOT / "runs" / job_id / tid / "r0"
        work, out = run_dir / "work", run_dir / "out"
        shutil.copytree(task_dir, work, ignore=shutil.ignore_patterns("raw"))
        out.mkdir(parents=True)
        env = dict(os.environ)
        env["PYTHONPATH"] = str(harness_dir.parent)
        env.pop("CLAUDECODE", None)
        cfg = json.loads((ROOT / "configs" / "executor.json").read_text())
        proc = subprocess.run([sys.executable, "-m", "harness", "run", "--task-json", str(work / "task.json"), "--workdir", str(work),
                               "--model-config", str(ROOT / "configs" / "executor.json"), "--output-dir", str(out)],
                              cwd=str(harness_dir.parent), capture_output=True, text=True, env=env, timeout=int(cfg.get("run_timeout_s", 1500)) + 120)
        (out / "stdout.log").write_text(proc.stdout)
        (out / "stderr.log").write_text(proc.stderr)
        tp = truth_path_for(task_dir)
        score = score_run(task_dir, out) if tp.exists() else {"score": None, "raw_accuracy": None, "provenance_ok": None, "per_claim": [], "note": "no numeric truth; use the judge"}
        job.update({"status": "done", "score": score, "out": str(out.relative_to(ROOT)), "finished_at": time.time()})
        (run_dir / "score.json").write_text(json.dumps(score, indent=2))
    except Exception as e:  # noqa: BLE001
        job.update({"status": "error", "error": str(e)})


@app.post("/api/run/{split}/{tid}")
def api_run(split: str, tid: str, harness_ref: str = "current"):
    if not (ROOT / "tasks" / split / tid / "task.json").exists():
        raise HTTPException(404, "task not built")
    job_id = f"ui_{time.strftime('%Y%m%d_%H%M%S')}_{tid[:20]}"
    JOBS[job_id] = {"job_id": job_id, "split": split, "task_id": tid, "harness_ref": harness_ref, "status": "running", "started_at": time.time()}
    threading.Thread(target=_run_job, args=(job_id, split, tid, harness_ref), daemon=True).start()
    return JOBS[job_id]


@app.get("/api/job/{job_id}")
def api_job(job_id: str):
    j = JOBS.get(job_id)
    if not j:
        raise HTTPException(404)
    if j["status"] == "running":
        tp = ROOT / "runs" / job_id / j["task_id"] / "r0" / "out" / "trajectory.jsonl"
        j["steps"] = sum(1 for l in tp.read_text().splitlines() if '"kind": "model_reply"' in l) if tp.exists() else 0
    return j


@app.get("/api/runs")
def api_runs():
    out = []
    for d in sorted((ROOT / "runs").iterdir(), reverse=True):
        if d.name.startswith("_") or not d.is_dir():
            continue
        s = d / "summary.json"
        if s.exists():
            summ = json.loads(s.read_text())
            out.append({"run_id": d.name, "kind": "eval", "split": summ["split"], "label": summ.get("label", ""), "mean_score": summ["mean_score"],
                        "n": summ["n_tasks"] * summ["repeats"], "cost": summ["total_cost_usd"], "commit": summ.get("harness_commit", "")})
        else:
            for t in sorted(p for p in d.iterdir() if p.is_dir()):
                sc = t / "r0" / "score.json"
                if sc.exists():
                    s2 = json.loads(sc.read_text())
                    out.append({"run_id": d.name, "kind": "ui", "task_id": t.name, "score": s2.get("score"), "raw": s2.get("raw_accuracy"),
                                "provenance": s2.get("provenance_ok"), "has_judge": (t / "r0" / "out" / "judge.json").exists()})
    return out


@app.get("/api/result/{job_id}/{tid}")
def api_result(job_id: str, tid: str):
    base = ROOT / "runs" / job_id / tid / "r0"
    out = base / "out"
    if not out.exists():
        raise HTTPException(404)
    res = {"score": json.loads((base / "score.json").read_text()) if (base / "score.json").exists() else None,
           "result": json.loads((out / "result.json").read_text()) if (out / "result.json").exists() else None,
           "claims": json.loads((out / "claims.json").read_text()) if (out / "claims.json").exists() else None,
           "analysis": (out / "analysis.py").read_text() if (out / "analysis.py").exists() else "",
           "response": (out / "response.md").read_text() if (out / "response.md").exists() else "",
           "judge": json.loads((out / "judge.json").read_text()) if (out / "judge.json").exists() else None,
           "human": json.loads((out / "human_verdict.json").read_text()) if (out / "human_verdict.json").exists() else None,
           "trajectory": [json.loads(l) for l in (out / "trajectory.jsonl").read_text().splitlines() if l.strip()] if (out / "trajectory.jsonl").exists() else []}
    return res


@app.post("/api/judge/{job_id}/{split}/{tid}")
def api_judge(job_id: str, split: str, tid: str):
    out = ROOT / "runs" / job_id / tid / "r0" / "out"
    if not out.exists():
        raise HTTPException(404)
    return judge_run(ROOT / "tasks" / split / tid, out, None, str(ROOT / "configs" / "judge.json"))


@app.post("/api/verdict/{job_id}/{tid}")
def api_verdict(job_id: str, tid: str, body: dict):
    out = ROOT / "runs" / job_id / tid / "r0" / "out"
    if not out.exists():
        raise HTTPException(404)
    body["saved_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    (out / "human_verdict.json").write_text(json.dumps(body, indent=2))
    return body


# ------------------------------------------------------------------------------- versions
@app.get("/api/versions")
def api_versions():
    ledger = ROOT / "evolve" / "ledger.jsonl"
    rows = [json.loads(l) for l in ledger.read_text().splitlines() if l.strip()] if ledger.exists() else []
    promos = ROOT / "evolve" / "promotions.jsonl"
    promotions = [json.loads(l) for l in promos.read_text().splitlines() if l.strip()] if promos.exists() else []
    return {"current": current_harness_commit(), "versions": rows, "promotions": promotions}


@app.post("/api/promote")
def api_promote(body: dict):
    commit = body.get("commit")
    if not commit:
        raise HTTPException(400, "commit required")
    subprocess.run(["git", "checkout", commit, "--", "harness"], cwd=ROOT, check=True)
    msg = f"Promote harness version {body.get('version', '')} ({commit[:8]}) after human review\n\nReason: {body.get('reason', '')}"
    subprocess.run(["git", "-c", "user.email=ui@local", "-c", "user.name=SciHarness UI", "commit", "-q", "-m", msg, "--", "harness"], cwd=ROOT, check=False)
    rec = {"commit": commit, "version": body.get("version"), "reason": body.get("reason", ""), "at": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(ROOT / "evolve" / "promotions.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return {"ok": True, "current": current_harness_commit(), **rec}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", "8765")))
