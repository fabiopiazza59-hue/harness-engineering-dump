"""V - verification gate applied to every submission.

A submission passes only if:
  1. every claim slot has a finite numeric value,
  2. the analysis script exists, runs in the task directory, and prints a JSON object whose
     values match the submitted claims (reproducibility of the submitted numbers),
  3. type-based sanity checks pass (p in [0,1], counts are non-negative integers, ...).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from .primitives import read_text, run_command, write_text

RANGE_CHECKS = {
    "pvalue": lambda v: 0.0 <= v <= 1.0,
    "prop": lambda v: 0.0 <= v <= 1.0,
    "corr": lambda v: -1.0 <= v <= 1.0,
    "r2": lambda v: 0.0 <= v <= 1.0,
    "sd": lambda v: v >= 0,
    "se": lambda v: v >= 0,
    "ratio": lambda v: v > 0,
    "count": lambda v: v >= 0 and float(v).is_integer(),
}


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if (math.isnan(f) or math.isinf(f)) else f


def _last_json(stdout: str) -> dict | None:
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                d = json.loads(line)
                if isinstance(d, dict):
                    return d
            except json.JSONDecodeError:
                continue
    return None


def verify_submission(task: dict, workdir: Path, output_dir: Path, claims: dict, analysis_code: str | None,
                      analysis_file: str | None, cfg: dict) -> tuple[bool, list[str], dict]:
    problems: list[str] = []
    slots = [c["id"] for c in task.get("claims") or []]
    types = {c["id"]: c.get("type", "number") for c in task.get("claims") or []}
    if not isinstance(claims, dict):
        return False, ["claims must be an object mapping claim id to number"], {}
    clean: dict = {}
    for cid in slots:
        v = _num(claims.get(cid))
        if v is None:
            problems.append(f"claim '{cid}' missing or not a finite number (got {claims.get(cid)!r})")
            continue
        chk = RANGE_CHECKS.get(types.get(cid))
        if chk and not chk(v):
            problems.append(f"claim '{cid}' fails the {types[cid]} range check (value {v})")
        clean[cid] = int(v) if types.get(cid) == "count" else v
    extra = [k for k in claims if k not in slots]
    if extra:
        problems.append(f"unknown claim ids ignored: {extra[:10]}")

    # analysis script
    code = analysis_code
    if not code and analysis_file:
        p = workdir / analysis_file
        if p.exists():
            code = read_text(p)
        else:
            problems.append(f"analysis_file '{analysis_file}' does not exist in the task directory")
    if not code or not str(code).strip():
        problems.append("no analysis script provided (pass analysis_file or analysis_code)")
        return False, problems, clean
    script = output_dir / "analysis.py"
    write_text(script, code)
    write_text(workdir / "analysis.py", code)
    res = run_command([sys.executable, "analysis.py"], cwd=workdir, timeout=int(cfg.get("python_timeout_s", 180)))
    if res["returncode"] != 0:
        problems.append(f"analysis.py failed (exit {res['returncode']}): {res['stderr'].strip()[-600:]}")
        return False, problems, clean
    printed = _last_json(res["stdout"])
    if printed is None:
        problems.append("analysis.py did not print a JSON object as its last stdout line")
        return False, problems, clean
    rel = float(cfg.get("verify_rel_tol", 1e-3))
    for cid in slots:
        if cid not in clean:
            continue
        pv = _num(printed.get(cid, printed.get("claims", {}).get(cid) if isinstance(printed.get("claims"), dict) else None))
        if pv is None:
            problems.append(f"analysis.py output lacks claim '{cid}'")
        elif abs(pv - clean[cid]) > max(1e-6, rel * abs(clean[cid])):
            problems.append(f"claim '{cid}': submitted {clean[cid]} but analysis.py prints {pv}")
    return (not [p for p in problems if not p.startswith("unknown claim ids")]), problems, clean
