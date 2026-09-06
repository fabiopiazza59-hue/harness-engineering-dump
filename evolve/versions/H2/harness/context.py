"""C - context construction and compaction.

The system prompt is static (role, tools, output protocol, rules). The first user message holds
the task. Each later turn is an assistant JSON action followed by a user observation. When the
transcript exceeds the configured budget, older observations are collapsed to one-line stubs and
the state's progress notes are re-injected so nothing essential is lost.
"""
from __future__ import annotations

import json
from pathlib import Path

from .primitives import read_text
from .state import State

SYSTEM = """You are a careful computational scientist reproducing the analysis of a published paper from its Methods section and the accompanying dataset.

You work by calling tools. Every reply MUST be a single JSON object and nothing else (no prose, no code fences):
{"thought": "<brief reasoning>", "action": {"tool": "<name>", "args": {...}}}

{tools}

RULES
1. Follow the Methods literally: apply exclusions in the stated order, use the stated test variant (e.g. Welch vs Student, Pearson vs Spearman, continuity correction or not, sample SD with n-1), the stated coding of variables, the stated transformations, and the stated definitions of derived quantities. When the text is explicit, do not substitute a "better" method.
2. Compute every claim slot from the data with code. Never guess or copy a number. If a slot cannot be computed, compute your best estimate and say so in the thought.
3. Keep one script that does the whole pipeline (load -> exclusions -> analysis -> print a JSON object mapping every claim id to a number). Save it as analysis.py via run_python(save_as="analysis.py"). The final JSON must be the last line of stdout. analysis.py is re-run in a fresh copy of the task directory containing only the files the task shipped with, so it must recompute everything from those original data files: never have it read a cleaned dataset, a cached result or a helper module you created during this run.
4. Before submitting, re-read the plan and check each rule was applied exactly once and in order. Check counts add up (e.g. group sizes after exclusions) and that p-values, proportions, and correlations are in range.
5. Submit with {"tool": "submit", "args": {"claims": {"<id>": <number>, ...}, "analysis_file": "analysis.py"}}. All values must be plain numbers.
6. Use as few turns as necessary: inspect once, plan once, write the full pipeline, run it, fix errors, submit.
"""


def system_prompt(tools_spec: str) -> str:
    return SYSTEM.replace("{tools}", tools_spec)


def task_message(task: dict, workdir: Path, cfg: dict) -> str:
    parts = [f"TASK {task.get('task_id', '')}: {task.get('title', '')}".strip(), "", task.get("instructions", ""), ""]
    claims = task.get("claims") or []
    if claims:
        parts.append("CLAIM SLOTS TO FILL (id: description [type]):")
        for c in claims:
            parts.append(f"- {c['id']}: {c.get('description', '')} [{c.get('type', 'number')}]")
        parts.append("")
    view = task.get("paper_view")
    if view and (workdir / view).exists():
        parts.append(f"=== {view} ===")
        parts.append(read_text(workdir / view, max_chars=int(cfg.get("paper_max_chars", 20000))))
        parts.append("")
    dd = task.get("data_dictionary")
    if dd and (workdir / dd).exists():
        parts.append(f"=== {dd} ===")
        parts.append(read_text(workdir / dd, max_chars=4000))
        parts.append("")
    parts.append("Data files: " + ", ".join(task.get("data_files") or ["(see list_files)"]))
    parts.append("Start by calling plan, then inspect_data.")
    return "\n".join(parts)


class Transcript:
    def __init__(self, cfg: dict, state: State):
        self.cfg = cfg
        self.state = state
        self.budget = int(cfg.get("context_budget_chars", 60000))
        self.keep_recent = int(cfg.get("compaction_keep_recent", 6))
        self.messages: list[dict] = []   # {"role", "content", "kind": "task"|"action"|"observation"|"notes"}

    def add_task(self, text: str):
        self.messages.append({"role": "user", "content": text, "kind": "task"})

    def add_action(self, raw: str):
        self.messages.append({"role": "assistant", "content": raw, "kind": "action"})

    def add_observation(self, text: str):
        self.messages.append({"role": "user", "content": text, "kind": "observation"})

    def size(self) -> int:
        return sum(len(m["content"]) for m in self.messages)

    def maybe_compact(self) -> bool:
        if self.size() <= self.budget:
            return False
        # collapse old observations (keep the task and the most recent turns intact)
        n = len(self.messages)
        cutoff = max(1, n - self.keep_recent)
        for i in range(1, cutoff):
            m = self.messages[i]
            if m["kind"] == "observation" and len(m["content"]) > 400:
                m["content"] = "[earlier observation compacted] " + m["content"][:300].replace("\n", " ") + " ..."
            elif m["kind"] == "action" and len(m["content"]) > 1500:
                try:
                    d = json.loads(m["content"])
                    tool = d.get("action", {}).get("tool")
                    m["content"] = json.dumps({"thought": "[compacted]", "action": {"tool": tool, "args": "[compacted]"}})
                except json.JSONDecodeError:
                    m["content"] = m["content"][:600] + " ...[compacted]"
        self.state.compactions += 1
        return True

    def render(self) -> list[dict]:
        """Messages for the LLM, with progress notes appended to the latest user turn."""
        msgs = [{"role": m["role"], "content": m["content"]} for m in self.messages]
        notes = self.state.progress_notes()
        if msgs and msgs[-1]["role"] == "user":
            msgs[-1] = {"role": "user", "content": msgs[-1]["content"] + "\n\n[PROGRESS NOTES]\n" + notes}
        return msgs
