"""Stable command-line contract shared by the seed and every harness built from it.

Supported invocation forms:
    python -m harness run --task-json <task.json> --model-config <model.json> --output-dir <out>
    python -m harness --task-json <task.json> --workdir <dir> --model-config <model.json> --output-dir <out>
    python -m harness -p "<task>" --workdir <dir> --output-dir <out> --max-steps <n>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .config import load_model_config
from .runner import run


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harness")
    p.add_argument("command", nargs="?", default="run")
    p.add_argument("--task-json")
    p.add_argument("-p", "--prompt")
    p.add_argument("--workdir", "--work-dir", "--workspace", dest="workdir")
    p.add_argument("--model-config")
    p.add_argument("--output-dir", "--output", dest="output_dir")
    p.add_argument("--max-steps", "--max-turns", dest="max_steps", type=int)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "run" and not args.command.startswith("-"):
        print(f"unknown command: {args.command}", file=sys.stderr)
        return 2
    workdir = Path(args.workdir or os.getcwd()).resolve()
    if args.task_json:
        task_path = Path(args.task_json).resolve()
        task = json.loads(task_path.read_text())
        if not args.workdir:
            workdir = task_path.parent
    elif args.prompt:
        task = {"task_id": "adhoc", "instructions": args.prompt, "claims": []}
    else:
        print("either --task-json or -p/--prompt is required", file=sys.stderr)
        return 2
    output_dir = Path(args.output_dir or (workdir / "harness_output")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cfg = load_model_config(args.model_config)
    if args.max_steps:
        cfg["max_steps"] = args.max_steps
    result = run(task=task, workdir=workdir, output_dir=output_dir, cfg=cfg)
    return 0 if result.get("status") in ("success", "partial") else 1
