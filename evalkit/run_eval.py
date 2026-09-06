#!/usr/bin/env python3
"""Run a frozen harness over a task split, score every run, and write a summary.

    python evalkit/run_eval.py --split dev --harness-dir harness --repeats 1 --workers 3
    python evalkit/run_eval.py --split feedback --harness-dir evolve/worktrees/cand_3 --run-id cand_3_fb

Outputs (runs/<run_id>/):
    results.jsonl   one line per (task, repeat) with the scorer output and usage
    summary.json    mean score, raw accuracy, provenance rate, tokens, cost, duration, per-task table
For --split heldout the summary is also copied to evalkit/heldout_results/<run_id>.json.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evalkit"))
from score import score_run, truth_path_for  # noqa: E402


def list_tasks(split: str, only: list[str] | None) -> list[Path]:
    base = ROOT / "tasks" / split
    tasks = sorted(p for p in base.iterdir() if p.is_dir() and (p / "task.json").exists())
    if only:
        tasks = [t for t in tasks if t.name in only]
    return tasks


def run_one(harness_dir: Path, task_dir: Path, run_dir: Path, executor_cfg: Path, timeout: int) -> dict:
    work = run_dir / "work"
    out = run_dir / "out"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(task_dir, work)
    out.mkdir(parents=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(harness_dir.parent)
    env.pop("CLAUDECODE", None)
    cmd = [sys.executable, "-m", "harness", "run", "--task-json", str(work / "task.json"), "--workdir", str(work),
           "--model-config", str(executor_cfg), "--output-dir", str(out)]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=str(harness_dir.parent), capture_output=True, text=True, timeout=timeout, env=env)
        (out / "stdout.log").write_text(proc.stdout)
        (out / "stderr.log").write_text(proc.stderr)
        rc, timed_out = proc.returncode, False
    except subprocess.TimeoutExpired as e:
        (out / "stdout.log").write_text(str(e.stdout or ""))
        (out / "stderr.log").write_text("RUN TIMED OUT\n" + str(e.stderr or ""))
        rc, timed_out = -1, True
    dur = time.time() - t0
    sc = score_run(task_dir, out)
    usage = {}
    rp = out / "result.json"
    if rp.exists():
        try:
            usage = json.loads(rp.read_text()).get("usage", {})
        except json.JSONDecodeError:
            pass
    return {**sc, "returncode": rc, "timed_out": timed_out, "duration_s": round(dur, 1), "usage": usage,
            "run_dir": str(run_dir.relative_to(ROOT))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True)
    ap.add_argument("--tasks", nargs="*")
    ap.add_argument("--harness-dir", default="harness")
    ap.add_argument("--executor", default="configs/executor.json")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--run-id")
    ap.add_argument("--label", default="")
    a = ap.parse_args()

    harness_dir = (ROOT / a.harness_dir).resolve()
    executor_cfg = (ROOT / a.executor).resolve()
    cfg = json.loads(executor_cfg.read_text())
    timeout = int(cfg.get("run_timeout_s", 1500)) + 120
    run_id = a.run_id or f"{a.split}_{time.strftime('%Y%m%d_%H%M%S')}"
    run_root = ROOT / "runs" / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    tasks = list_tasks(a.split, a.tasks)
    harness_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=harness_dir, capture_output=True, text=True).stdout.strip()

    jobs = [(t, r) for t in tasks for r in range(a.repeats)]
    results = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_one, harness_dir, t, run_root / t.name / f"r{r}", executor_cfg, timeout): (t, r) for t, r in jobs}
        for f in as_completed(futs):
            t, r = futs[f]
            try:
                res = f.result()
            except Exception as e:  # noqa: BLE001
                res = {"task_id": t.name, "score": 0.0, "raw_accuracy": 0.0, "provenance_ok": False, "error": str(e)}
            res["repeat"] = r
            results.append(res)
            print(f"[{len(results)}/{len(jobs)}] {t.name} r{r}: score={res.get('score')} raw={res.get('raw_accuracy')} "
                  f"prov={res.get('provenance_ok')} {res.get('duration_s', '?')}s", flush=True)
            with open(run_root / "results.jsonl", "a") as fh:
                fh.write(json.dumps(res) + "\n")

    per_task = {}
    for r in results:
        per_task.setdefault(r["task_id"], []).append(r)
    table = {tid: {"score": round(statistics.mean(x["score"] for x in rs), 4),
                   "raw_accuracy": round(statistics.mean(x["raw_accuracy"] for x in rs), 4),
                   "provenance_rate": round(sum(x["provenance_ok"] for x in rs) / len(rs), 3),
                   "n": len(rs)} for tid, rs in per_task.items()}
    scores = [r["score"] for r in results]
    summary = {
        "run_id": run_id, "split": a.split, "label": a.label, "harness_dir": str(harness_dir.relative_to(ROOT)),
        "harness_commit": harness_commit, "executor": cfg, "n_tasks": len(tasks), "repeats": a.repeats,
        "mean_score": round(statistics.mean(scores), 4) if scores else 0.0,
        "mean_raw_accuracy": round(statistics.mean(r["raw_accuracy"] for r in results), 4) if results else 0.0,
        "provenance_rate": round(sum(r["provenance_ok"] for r in results) / len(results), 3) if results else 0.0,
        "timeouts": sum(1 for r in results if r.get("timed_out")),
        "total_cost_usd": round(sum(float(r.get("usage", {}).get("cost_usd", 0) or 0) for r in results), 3),
        "total_llm_calls": sum(int(r.get("usage", {}).get("calls", 0) or 0) for r in results),
        "mean_output_tokens": round(statistics.mean(int(r.get("usage", {}).get("output_tokens", 0) or 0) for r in results), 1) if results else 0,
        "wall_s": round(time.time() - t0, 1),
        "per_task": table,
        "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if a.split == "heldout":
        hr = ROOT / "evalkit" / "heldout_results"
        hr.mkdir(exist_ok=True)
        (hr / f"{run_id}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "per_task"}, indent=2))
    for tid, row in sorted(table.items()):
        print(f"  {tid:28s} score={row['score']:.3f} raw={row['raw_accuracy']:.3f} prov={row['provenance_rate']:.2f}")


if __name__ == "__main__":
    main()
