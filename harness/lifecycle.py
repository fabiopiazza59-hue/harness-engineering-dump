"""L - lifecycle: action parsing with recovery, budgets, timeouts, and finalisation."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .audit import write_response, write_result
from .primitives import write_json
from .state import State

FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)


class ParseError(Exception):
    pass


def parse_action(raw: str) -> dict:
    """Extract {"thought", "action": {"tool", "args"}} from the model reply."""
    text = raw.strip()
    candidates = []
    m = FENCE.search(text)
    if m:
        candidates.append(m.group(1))
    candidates.append(text)
    # first '{' to last '}' as a fallback
    if "{" in text and "}" in text:
        candidates.append(text[text.index("{"): text.rindex("}") + 1])
    for c in candidates:
        try:
            d = json.loads(c)
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and isinstance(d.get("action"), dict) and d["action"].get("tool"):
            d["action"].setdefault("args", {})
            if not isinstance(d["action"]["args"], dict):
                d["action"]["args"] = {}
            return d
        if isinstance(d, dict) and d.get("tool"):
            return {"thought": d.get("thought", ""), "action": {"tool": d["tool"], "args": d.get("args") or {}}}
    raise ParseError("reply was not a JSON object of the form {\"thought\": ..., \"action\": {\"tool\": ..., \"args\": {...}}}")


class Budget:
    def __init__(self, cfg: dict, state: State):
        self.max_steps = int(cfg.get("max_steps", 30))
        self.run_timeout = float(cfg.get("run_timeout_s", 1800))
        self.reserve = float(cfg.get("finalize_reserve_s", 120))
        self.max_parse_failures = int(cfg.get("max_parse_failures", 3))
        self.max_gate_failures = int(cfg.get("max_gate_failures", 4))
        self.state = state

    def exhausted(self) -> str | None:
        if self.state.step >= self.max_steps:
            return f"step budget reached ({self.max_steps})"
        if self.state.elapsed() > self.run_timeout - self.reserve:
            return f"time budget reached ({int(self.run_timeout)}s)"
        if self.state.parse_failures >= self.max_parse_failures:
            return "too many unparseable replies"
        return None

    def gate_exhausted(self) -> bool:
        return sum(1 for s in self.state.submissions if not s["ok"]) >= self.max_gate_failures


def finalize(task: dict, output_dir: Path, workdir: Path, state: State, usage: dict, reason: str) -> dict:
    """Write claims.json, analysis.py, response.md and an honest result.json."""
    claims = state.best_claims or state.draft_claims or {}
    slots = [c["id"] for c in task.get("claims") or []]
    filled = [s for s in slots if s in claims]
    passed = bool(state.submissions) and state.submissions[-1]["ok"]
    if claims:
        write_json(output_dir / "claims.json", {"claims": [{"id": k, "value": v} for k, v in claims.items() if k in slots or not slots],
                                               "notes": reason, "gate_passed": passed})
    if state.best_analysis and not (output_dir / "analysis.py").exists():
        (output_dir / "analysis.py").write_text(state.best_analysis)
    if passed:
        status = "success"
    elif claims and filled:
        status = "partial"
    else:
        status = "failed"
    state.status = status
    state.finished = True
    state.save(output_dir)
    write_response(output_dir, "\n".join([
        f"# Run summary for {task.get('task_id')}", "", f"Status: {status}", f"Reason: {reason}",
        f"Steps: {state.step}; scripts: {len(state.scripts)}; gate attempts: {len(state.submissions)}; compactions: {state.compactions}",
        "", "## Claims", json.dumps(claims, indent=2) if claims else "(none)", "", "## Plan", state.plan or "(none)",
    ]) + "\n")
    return write_result(output_dir, status, task_id=task.get("task_id"), reason=reason, steps=state.step,
                        claims_written=bool(claims), slots_filled=len(filled), slots_total=len(slots),
                        gate_passed=passed, usage=usage,
                        artifacts={"claims": "claims.json", "analysis": "analysis.py", "state": "state.json"})
