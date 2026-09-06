#!/usr/bin/env python3
"""Estimate the run-to-run noise band of one harness version.

    python evalkit/noise.py --run-id fb_H0_x3
    python evalkit/noise.py --run-ids run_a run_b run_c

With repeats in one run, the band is computed from per-repeat set means. With several runs it is
computed from their mean scores. Reports mean, sd, min, max, and the recommended band
(the larger of 2*sd and max-min), which a candidate must exceed to count as improved.
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def repeat_means(run_id: str) -> list[float]:
    rows = [json.loads(l) for l in (ROOT / "runs" / run_id / "results.jsonl").read_text().splitlines() if l.strip()]
    by_rep = {}
    for r in rows:
        by_rep.setdefault(r.get("repeat", 0), []).append(r["score"])
    return [statistics.mean(v) for _, v in sorted(by_rep.items())]


def band(values: list[float]) -> dict:
    sd = statistics.stdev(values) if len(values) > 1 else 0.0
    return {"n": len(values), "mean": round(statistics.mean(values), 4), "sd": round(sd, 4),
            "min": round(min(values), 4), "max": round(max(values), 4),
            "band": round(max(2 * sd, max(values) - min(values)), 4), "values": [round(v, 4) for v in values]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id")
    ap.add_argument("--run-ids", nargs="*")
    a = ap.parse_args()
    if a.run_id:
        vals = repeat_means(a.run_id)
    else:
        vals = [json.loads((ROOT / "runs" / r / "summary.json").read_text())["mean_score"] for r in a.run_ids]
    print(json.dumps(band(vals), indent=2))


if __name__ == "__main__":
    main()
