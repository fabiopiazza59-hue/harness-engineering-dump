"""Tolerant extraction of one JSON object from a model reply.

Model replies delivered through the CLI backend occasionally arrive with a stray token or a
missing closing delimiter. This parser tries strict parsing first, then a small set of bounded
repairs: code-fence stripping, stray-token removal between a string and the next delimiter, and
appending the closers implied by a string-aware scan. It never invents keys or values.
"""
from __future__ import annotations

import json
import re

FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)
STRAY = re.compile(r'("\s*)[A-Za-z_]+(\s*[,}\]:])')


def _scan_closers(text: str) -> str:
    stack, in_str, esc = [], False, False
    for ch in text:
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]" and stack:
            stack.pop()
    tail = '"' if in_str else ""
    return tail + "".join(reversed(stack))


def parse_json_object(raw: str) -> dict:
    """Return the first JSON object in raw, repairing bounded defects. Raises ValueError."""
    text = raw.strip()
    candidates = []
    m = FENCE.search(text)
    if m:
        candidates.append(m.group(1))
    if "{" in text:
        start = text.index("{")
        candidates.append(text[start: text.rindex("}") + 1] if "}" in text else text[start:])
    candidates.append(text)
    for c in candidates:
        for variant in (c, STRAY.sub(r"\1\2", c)):
            for attempt in (variant, variant.rstrip().rstrip(",") + _scan_closers(variant)):
                try:
                    d = json.loads(attempt)
                    if isinstance(d, dict):
                        return d
                except json.JSONDecodeError:
                    continue
    raise ValueError("no JSON object could be recovered from the reply")
