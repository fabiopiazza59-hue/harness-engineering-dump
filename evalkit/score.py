#!/usr/bin/env python3
"""Deterministic scorer for reproduce-analysis runs. No model involved.

score = raw_accuracy if the provenance gate passes else 0
  raw_accuracy   fraction of claim slots whose submitted value is within tolerance of truth
  provenance     the submitted analysis.py, re-run in a clean copy of the task dir, prints
                 claims that match the submitted claims.json within tolerance

Usage:
    python evalkit/score.py --task tasks/dev/dev_002_ttest --output runs/x/dev_002_ttest/out
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def truth_path_for(task_dir: Path) -> Path:
    task_dir = task_dir.resolve()
    split, task_id = task_dir.parent.name, task_dir.name
    return ROOT / "evalkit" / "truth" / split / task_id / "truth.json"


def within(pred, truth, tol) -> bool:
    try:
        pred = float(pred)
    except (TypeError, ValueError):
        return False
    if pred != pred or math.isinf(pred):
        return False
    return abs(pred - float(truth)) <= max(float(tol.get("abs", 0)), float(tol.get("rel", 0)) * abs(float(truth)))


def load_submitted(output_dir: Path) -> dict:
    p = output_dir / "claims.json"
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError:
        return {}
    claims = data.get("claims", data) if isinstance(data, dict) else data
    out = {}
    if isinstance(claims, dict):
        for k, v in claims.items():
            out[k] = v.get("value") if isinstance(v, dict) else v
    elif isinstance(claims, list):
        for c in claims:
            if isinstance(c, dict) and "id" in c:
                out[c["id"]] = c.get("value")
    return out


JSON_LINE = re.compile(r"\{.*\}", re.S)


def rerun_script(task_dir: Path, script: Path, timeout: int = 180) -> tuple[dict | None, str]:
    """Run analysis.py in a scratch copy of the task dir; return (claims, log)."""
    if not script.exists():
        return None, "analysis.py missing"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        shutil.copytree(task_dir, work, ignore=shutil.ignore_patterns("harness_output", "__pycache__"))
        shutil.copy(script, work / "analysis.py")
        try:
            proc = subprocess.run([sys.executable, "analysis.py"], cwd=work, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, "analysis.py timed out"
        if proc.returncode != 0:
            return None, f"analysis.py exit {proc.returncode}: {proc.stderr[-800:]}"
        # last JSON object on stdout
        objs = [line for line in proc.stdout.strip().splitlines() if line.strip().startswith("{")]
        for line in reversed(objs):
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    return {k: (v.get("value") if isinstance(v, dict) else v) for k, v in data.get("claims", data).items()} \
                        if isinstance(data.get("claims", data), dict) else \
                        {c["id"]: c.get("value") for c in data["claims"] if isinstance(c, dict)}, "ok"
            except json.JSONDecodeError:
                continue
        m = JSON_LINE.search(proc.stdout)
        if m:
            try:
                data = json.loads(m.group(0))
                return data if isinstance(data, dict) else None, "ok"
            except json.JSONDecodeError:
                pass
        return None, f"no JSON object on stdout: {proc.stdout[-300:]}"


def score_run(task_dir: Path, output_dir: Path, truth: dict | None = None, rerun: bool = True) -> dict:
    task_dir, output_dir = Path(task_dir), Path(output_dir)
    truth = truth or json.loads(truth_path_for(task_dir).read_text())
    submitted = load_submitted(output_dir)
    per_claim = []
    n_ok = 0
    for c in truth["claims"]:
        pred = submitted.get(c["id"])
        ok = pred is not None and within(pred, c["value"], c["tolerance"])
        n_ok += int(ok)
        per_claim.append({"id": c["id"], "truth": c["value"], "pred": pred, "correct": ok, "tolerance": c["tolerance"]})
    raw = n_ok / max(1, len(truth["claims"]))
    prov_ok, prov_log, prov_mismatch = False, "not checked", []
    if rerun:
        if not submitted:
            prov_ok, prov_log = False, "no claims submitted"
        else:
            reproduced, prov_log = rerun_script(task_dir, output_dir / "analysis.py")
            if reproduced is not None:
                tol_by_id = {c["id"]: c["tolerance"] for c in truth["claims"]}
                for cid, val in submitted.items():
                    if cid not in tol_by_id:
                        continue
                    rv = reproduced.get(cid)
                    if rv is None or not within(rv, float(val) if _is_num(val) else float("nan"), tol_by_id[cid]):
                        prov_mismatch.append({"id": cid, "submitted": val, "rerun": rv})
                prov_ok = not prov_mismatch
                if prov_mismatch:
                    prov_log = f"{len(prov_mismatch)} claims not reproduced by analysis.py"
    else:
        prov_ok = True
    return {
        "task_id": truth["task_id"], "raw_accuracy": round(raw, 4), "provenance_ok": prov_ok,
        "score": round(raw if prov_ok else 0.0, 4), "n_claims": len(truth["claims"]), "n_correct": n_ok,
        "provenance_log": prov_log, "provenance_mismatch": prov_mismatch, "per_claim": per_claim,
        "submitted_any": bool(submitted),
    }


def _is_num(v) -> bool:
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--truth")
    ap.add_argument("--no-rerun", action="store_true")
    a = ap.parse_args()
    truth = json.loads(Path(a.truth).read_text()) if a.truth else None
    print(json.dumps(score_run(Path(a.task), Path(a.output), truth, rerun=not a.no_rerun), indent=2))


if __name__ == "__main__":
    main()
