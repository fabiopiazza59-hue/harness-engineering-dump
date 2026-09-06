"""Unified audit contract: result.json, trajectory.jsonl, response.md, logs."""
from __future__ import annotations

import json
import time
from pathlib import Path


class Trajectory:
    def __init__(self, output_dir: Path):
        self.path = output_dir / "trajectory.jsonl"
        self.t0 = time.time()
        self.n = 0
        self._fh = open(self.path, "a", encoding="utf-8")

    def log(self, kind: str, **fields):
        self.n += 1
        rec = {"seq": self.n, "t": round(time.time() - self.t0, 3), "kind": kind, **fields}
        self._fh.write(json.dumps(rec, default=str) + "\n")
        self._fh.flush()
        return rec

    def close(self):
        self._fh.close()


def write_result(output_dir: Path, status: str, **fields):
    """status must be honest: success | partial | failed."""
    assert status in ("success", "partial", "failed")
    rec = {"status": status, **fields}
    (output_dir / "result.json").write_text(json.dumps(rec, indent=2, default=str) + "\n")
    return rec


def write_response(output_dir: Path, text: str):
    (output_dir / "response.md").write_text(text)
