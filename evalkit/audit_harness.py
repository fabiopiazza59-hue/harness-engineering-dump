#!/usr/bin/env python3
"""Static audit of a harness directory for prohibited patterns (docs/PROTOCOL.md section 6).

    python evalkit/audit_harness.py [harness_dir]

Exit 1 on violations. Checks:
  - hard-coded executor model names outside the provider dispatch in llm.py
  - hard-coded numeric step/time caps outside config defaults
  - references to evalkit/truth, truth.json, reference_analysis, or task ids
  - TODO / NotImplementedError / bare `pass` placeholders on the executable path
  - provider SDK imports (anthropic, openai) replacing the gateway
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("model name hard-coded", re.compile(r"[\"'](claude-[a-z0-9-]+|gpt-[0-9a-z.-]+|gemini[-a-z0-9.]*|sonnet|opus|haiku)[\"']", re.I), {"llm.py", "config.py"}),
    ("truth/reference access", re.compile(r"evalkit/truth|truth\.json|reference_analysis|heldout_results"), set()),
    ("task id hard-coded", re.compile(r"\b(dev|fb|ho)_0\d\d_"), set()),
    ("placeholder", re.compile(r"\bTODO\b|NotImplementedError|^\s*pass\s*$", re.M), set()),
    ("provider SDK import", re.compile(r"^\s*(import|from)\s+(anthropic|openai)\b", re.M), set()),
    ("numeric step cap literal", re.compile(r"(max_steps|step_limit|MAX_STEPS)\s*=\s*\d+"), {"config.py"}),
]


def main():
    hdir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "harness"
    violations = []
    for py in sorted(hdir.rglob("*.py")):
        text = py.read_text()
        for label, rx, exempt in CHECKS:
            if py.name in exempt:
                continue
            for m in rx.finditer(text):
                line = text[: m.start()].count("\n") + 1
                snippet = text.splitlines()[line - 1].strip()
                if snippet.startswith("#") or snippet.startswith('"""') or snippet.startswith("'''"):
                    continue
                if label == "placeholder" and snippet == "pass" and line >= 2:
                    prev = text.splitlines()[line - 2].strip()
                    if prev.startswith("class ") and "Exception" in prev or prev.startswith("class ") and "Error" in prev:
                        continue  # empty exception class body is not a placeholder
                violations.append(f"{py.relative_to(hdir)}:{line}: {label}: {snippet[:100]}")
    if violations:
        print("AUDIT VIOLATIONS:")
        print("\n".join(violations))
        sys.exit(1)
    print(f"audit clean: {hdir}")


if __name__ == "__main__":
    main()
