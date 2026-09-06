"""Entry point used by the CLI: runs the execution loop for one task."""
from __future__ import annotations

from pathlib import Path

from .execution import run_loop


def run(task: dict, workdir: Path, output_dir: Path, cfg: dict) -> dict:
    return run_loop(task=task, workdir=Path(workdir), output_dir=Path(output_dir), cfg=cfg)
