"""L - lifecycle: action parsing with recovery, budgets, timeouts, and finalisation."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .audit import write_response, write_result
from .primitives import write_json
from .state import State

FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)
CLOSERS = {"{": "}", "[": "]"}
DANGLING_KEY = re.compile(r',?\s*"(?:[^"\\]|\\.)*"\s*:\s*$')


class ParseError(Exception):
    pass


def _scan(text: str, start: int) -> dict:
    """String-aware walk from `start`. Reports the open-delimiter stack, whether the text
    ends inside a string, and where the first top-level value closed (None if it never did)."""
    stack: list[str] = []
    in_string = escaped = False
    end = None
    for i in range(start, len(text)):
        ch = text[i]
        if escaped:
            escaped = False
            continue
        if in_string:
            if ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch in CLOSERS:
            stack.append(CLOSERS[ch])
        elif ch in ("}", "]"):
            if not stack:
                break
            stack.pop()
            if not stack:
                end = i + 1
                break
    return {"stack": stack, "in_string": in_string, "escaped": escaped, "end": end}


def _objects(text: str) -> list[str]:
    """Every complete top-level {...} object in order, plus a trailing incomplete one if present.

    Lets a stray object or prose before/after the action be stepped over instead of swallowed by
    the naive first-'{'-to-last-'}' slice.
    """
    out, i = [], text.find("{")
    while i >= 0:
        s = _scan(text, i)
        if s["end"] is None:
            out.append(text[i:])
            break
        out.append(text[i:s["end"]])
        i = text.find("{", s["end"])
    return out


def repair_json(text: str) -> tuple[str | None, str]:
    """Close a structurally incomplete JSON object. Returns (repaired_text, description).

    Only ever closes an unterminated string, trims an incomplete trailing token, and appends
    the closing delimiters implied by the open stack. Never invents keys or values.
    """
    i = text.find("{")
    if i < 0:
        return None, ""
    s = _scan(text, i)
    if s["end"] is not None or not s["stack"]:
        return None, ""
    body = text[i:]
    notes = []
    if s["escaped"]:
        body = body[:-1]
    if s["in_string"]:
        body += '"'
        notes.append("closed an unterminated string")
    stripped = body.rstrip()
    while True:
        if stripped.endswith(","):
            stripped = stripped[:-1].rstrip()
            continue
        m = DANGLING_KEY.search(stripped)
        if m:
            stripped = stripped[:m.start()].rstrip()
            notes.append("dropped a key with no value")
            continue
        break
    closers = "".join(reversed(s["stack"]))
    notes.append(f"appended {len(closers)} missing closing delimiter(s) '{closers}'")
    return stripped + closers, "; ".join(notes)


def _as_action(d) -> dict | None:
    if not isinstance(d, dict):
        return None
    act = d.get("action")
    if isinstance(act, dict) and act.get("tool"):
        args = act.get("args")
        return {"thought": d.get("thought", ""),
                "action": {"tool": act["tool"], "args": args if isinstance(args, dict) else {}}}
    if d.get("tool"):
        args = d.get("args")
        return {"thought": d.get("thought", ""),
                "action": {"tool": d["tool"], "args": args if isinstance(args, dict) else {}}}
    return None


def _diagnose(text: str) -> str:
    i = text.find("{")
    if i < 0:
        return "the reply contained no JSON object (no '{' found)"
    s = _scan(text, i)
    bits = []
    if s["in_string"]:
        bits.append("it ends inside an unterminated string (a quote or backslash is unescaped, or the reply was cut off)")
    if s["stack"]:
        needed = "".join(reversed(s["stack"]))
        bits.append(f"{len(s['stack'])} delimiter(s) were never closed; it needs a trailing {needed!r}")
    if not bits:
        bits.append("it is not valid JSON and has no recognisable 'action': {'tool': ..., 'args': {...}} object")
    return "; ".join(bits)


def parse_action(raw: str) -> dict:
    """Extract {"thought", "action": {"tool", "args"}} from the model reply.

    Strict parsing first; then a structural repair for replies that are unambiguously an action
    object but are missing closing delimiters. A repaired action carries "_repaired" describing
    what was fixed so the caller can log it honestly.
    """
    text = raw.strip()
    candidates = []
    m = FENCE.search(text)
    if m:
        candidates.append(m.group(1))
    candidates.append(text)
    candidates.extend(_objects(text))
    if "{" in text and "}" in text:
        candidates.append(text[text.index("{"): text.rindex("}") + 1])

    for c in candidates:
        try:
            act = _as_action(json.loads(c))
        except json.JSONDecodeError:
            continue
        if act:
            return act
    for c in candidates:
        fixed, how = repair_json(c)
        if not fixed:
            continue
        try:
            act = _as_action(json.loads(fixed))
        except json.JSONDecodeError:
            continue
        if act:
            act["_repaired"] = how
            return act
    raise ParseError("reply was not a valid JSON object of the form "
                     "{\"thought\": ..., \"action\": {\"tool\": ..., \"args\": {...}}} - " + _diagnose(text)
                     + ". Your reply ended with: ..." + text[-80:])


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
