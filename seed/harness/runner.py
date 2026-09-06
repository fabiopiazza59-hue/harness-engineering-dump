"""Seed runner: one non-acting pass.

Parses the task and environment, optionally probes the configured LLM with a summary-only
prompt, writes the audit envelope, and terminates with status "partial". It never attempts
the task: no loop, no tools policy, no context management, no state, no recovery, no verifier.
"""
from __future__ import annotations

from pathlib import Path

from .audit import Trajectory, write_response, write_result
from .llm import LLM, LLMError
from .primitives import Paths, list_tree, read_text


def run(task: dict, workdir: Path, output_dir: Path, cfg: dict) -> dict:
    traj = Trajectory(output_dir)
    paths = Paths(workdir)
    traj.log("start", task_id=task.get("task_id"), workdir=str(workdir), provider=cfg.get("provider"), model=cfg.get("model"))
    files = list_tree(workdir)
    traj.log("observe", files=files[:50])

    summary = ""
    llm = LLM(cfg)
    view = task.get("paper_view")
    if view and paths.contains(paths.resolve(view)):
        excerpt = read_text(paths.resolve(view), max_chars=3000)
        try:
            summary = llm.chat(
                system="Summarise the following document in two sentences. Do not attempt any task.",
                messages=[{"role": "user", "content": excerpt}],
            )
            traj.log("llm_probe", ok=True, chars=len(summary))
        except LLMError as e:
            traj.log("llm_probe", ok=False, error=str(e))

    write_response(output_dir, f"# Seed harness\n\nThe seed performed no task work.\n\nProbe summary: {summary}\n")
    result = write_result(
        output_dir, "partial",
        task_id=task.get("task_id"), reason="seed harness has no execution logic",
        artifacts={}, claims_written=False, usage=llm.usage(),
    )
    traj.log("end", status="partial")
    traj.close()
    return result
