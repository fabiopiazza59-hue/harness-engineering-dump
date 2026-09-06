"""S - persistent task state with checkpointing.

The state records the goal, the plan, scripts run, failures, draft claims, and gate outcomes.
It is checkpointed to state.json after every step and can be resumed.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class State:
    task_id: str
    step: int = 0
    started_at: float = field(default_factory=time.time)
    plan: str = ""
    scripts: list[dict] = field(default_factory=list)      # {"name", "returncode", "summary"}
    failures: list[str] = field(default_factory=list)
    draft_claims: dict = field(default_factory=dict)       # last numeric JSON printed by a script
    claim_scripts: list[str] = field(default_factory=list)  # scratch scripts that printed such a JSON, in order
    submissions: list[dict] = field(default_factory=list)  # gate attempts {"ok", "problems", "claims"}
    best_claims: dict = field(default_factory=dict)        # last submitted claims (best effort)
    best_analysis: str = ""
    parse_failures: int = 0
    repairs: int = 0                                       # replies the parser had to structurally repair
    compactions: int = 0
    finished: bool = False
    status: str = "running"

    def elapsed(self) -> float:
        return time.time() - self.started_at

    def save(self, output_dir: Path) -> None:
        (output_dir / "state.json").write_text(json.dumps(asdict(self), indent=2, default=str) + "\n")

    @classmethod
    def load(cls, output_dir: Path) -> "State | None":
        p = output_dir / "state.json"
        if not p.exists():
            return None
        data = json.loads(p.read_text())
        return cls(**data)

    def progress_notes(self) -> str:
        """Compact notes injected into context; survives compaction."""
        lines = [f"step {self.step}; scripts run: {len(self.scripts)}; gate attempts: {len(self.submissions)}"]
        if self.plan:
            lines.append("PLAN:\n" + self.plan.strip())
        if self.scripts:
            last = self.scripts[-1]
            lines.append(f"last script: {last['name']} (exit {last['returncode']}): {last['summary'][:300]}")
        if self.draft_claims:
            lines.append("latest numeric JSON printed by a script: " + json.dumps(self.draft_claims)[:800])
        if self.submissions:
            s = self.submissions[-1]
            lines.append("last gate result: " + ("PASS" if s["ok"] else "FAIL: " + "; ".join(s["problems"])[:600]))
        if self.failures:
            lines.append("recent failures: " + " | ".join(self.failures[-3:])[:500])
        return "\n".join(lines)
