#!/usr/bin/env python3
"""LLM-as-judge for a run. Used for uploaded papers without numeric truth, and as a
second opinion on any run. Judge scores never feed the evolution loop.

    python evalkit/judge.py --task tasks/uploads/<id> --output runs/<run>/<id>/r0/out \
        [--paper evalkit/truth/uploads/<id>/paper_full.md] [--config configs/judge.json]

Writes judge.json into the output directory and prints it.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness.config import load_model_config  # noqa: E402
from harness.llm import LLM  # noqa: E402

SYSTEM = """You are a meticulous statistical reviewer. You compare an automated reproduction of a paper's analysis
against the paper itself. You are given: the paper (with its reported numbers), the claim slots, the values the
reproduction produced, and the reproduction's analysis script.

Judge two things:
1. For every claim slot: does the reproduced value match the value reported in the paper? Use the paper's own
   rounding: a match means equal after rounding to the paper's precision, or within 2% for effect sizes and
   statistics, or within 0.005 for p-values (p reported as "< 0.001" matches any value below 0.001).
   Verdicts: "match", "mismatch", "not_reported" (the paper does not report this quantity), "unclear".
2. Methods fidelity of the script, each 0-2 (0 = wrong/absent, 1 = partly, 2 = as described):
   exclusions, transformations, test_or_model_choice, variable_coding, reporting_definitions.

Reply with a single JSON object only:
{"claims": [{"id": "...", "paper_value": "...", "reproduced_value": ..., "verdict": "...", "note": "..."}],
 "fidelity": {"exclusions": 0-2, "transformations": 0-2, "test_or_model_choice": 0-2, "variable_coding": 0-2, "reporting_definitions": 0-2},
 "overall_assessment": "<two sentences>", "confidence": 0.0-1.0}
"""


def paper_text_for(task_dir: Path, explicit: str | None) -> str:
    if explicit:
        p = Path(explicit)
    else:
        split, tid = task_dir.resolve().parent.name, task_dir.name
        p = ROOT / "evalkit" / "truth" / split / tid / "paper_full.md"
    if p.suffix.lower() == ".pdf":
        import pymupdf
        return "\n".join(page.get_text() for page in pymupdf.open(str(p)))
    return p.read_text()


def judge_run(task_dir: Path, output_dir: Path, paper: str | None, cfg_path: str) -> dict:
    task = json.loads((task_dir / "task.json").read_text())
    paper_text = paper_text_for(task_dir, paper)
    claims_path = output_dir / "claims.json"
    claims = json.loads(claims_path.read_text()) if claims_path.exists() else {"claims": []}
    script = (output_dir / "analysis.py").read_text() if (output_dir / "analysis.py").exists() else "(no analysis.py)"
    user = "\n\n".join([
        "=== PAPER (full, with reported numbers) ===", paper_text[:30000],
        "=== CLAIM SLOTS ===", json.dumps(task.get("claims", []), indent=1),
        "=== REPRODUCED CLAIMS ===", json.dumps(claims, indent=1),
        "=== ANALYSIS SCRIPT ===", script[:12000],
    ])
    llm = LLM(load_model_config(cfg_path))
    raw = llm.chat(SYSTEM, [{"role": "user", "content": user}], max_tokens=6000)
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        verdict = json.loads(m.group(0) if m else raw)
    except json.JSONDecodeError:
        verdict = {"error": "judge returned non-JSON", "raw": raw[:2000]}
    cl = verdict.get("claims", []) if isinstance(verdict, dict) else []
    n_rep = [c for c in cl if c.get("verdict") in ("match", "mismatch")]
    verdict["judge_accuracy"] = round(sum(c.get("verdict") == "match" for c in n_rep) / len(n_rep), 4) if n_rep else None
    fid = verdict.get("fidelity") or {}
    verdict["fidelity_score"] = round(sum(float(v) for v in fid.values()) / (2 * len(fid)), 4) if fid else None
    verdict["usage"] = llm.usage()
    (output_dir / "judge.json").write_text(json.dumps(verdict, indent=2) + "\n")
    return verdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--paper")
    ap.add_argument("--config", default=str(ROOT / "configs" / "judge.json"))
    a = ap.parse_args()
    print(json.dumps(judge_run(Path(a.task), Path(a.output), a.paper, a.config), indent=2))


if __name__ == "__main__":
    main()
