"""Passive primitives. They act only when the harness calls them; there is no policy here."""
from __future__ import annotations

import fnmatch
import json
import os
import subprocess
from pathlib import Path


class Paths:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()

    def resolve(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if not str(p).startswith(str(self.root)):
            raise PermissionError(f"path escapes workdir: {rel}")
        return p

    def contains(self, p: Path) -> bool:
        return str(Path(p).resolve()).startswith(str(self.root))


def read_text(path: Path, max_chars: int | None = None) -> str:
    text = Path(path).read_text(errors="replace")
    if max_chars and len(text) > max_chars:
        return text[:max_chars] + f"\n...[truncated {len(text) - max_chars} chars]"
    return text


def write_text(path: Path, text: str) -> int:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text)
    return len(text)


def read_json(path: Path):
    return json.loads(Path(path).read_text())


def write_json(path: Path, obj) -> None:
    Path(path).write_text(json.dumps(obj, indent=2, default=str) + "\n")


def list_tree(root: Path, max_entries: int = 200) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        for f in sorted(filenames):
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            out.append(rel)
            if len(out) >= max_entries:
                return out
    return out


def glob(root: Path, pattern: str) -> list[str]:
    return [p for p in list_tree(root, 10000) if fnmatch.fnmatch(p, pattern)]


def grep(root: Path, pattern: str, max_hits: int = 100) -> list[str]:
    import re
    rx = re.compile(pattern)
    hits = []
    for rel in list_tree(root, 10000):
        try:
            for i, line in enumerate(read_text(root / rel).splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{rel}:{i}:{line[:200]}")
                    if len(hits) >= max_hits:
                        return hits
        except Exception:  # noqa: BLE001
            continue
    return hits


def run_command(cmd: list[str] | str, cwd: Path, timeout: int = 120, shell: bool = False) -> dict:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, shell=shell)
        return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr, "timed_out": False}
    except subprocess.TimeoutExpired as e:
        return {"returncode": -1, "stdout": (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""),
                "stderr": "timed out", "timed_out": True}
