"""T - tool registry and dispatch.

Tools are the only way the runtime LLM touches the workspace. Each tool validates its
arguments, bounds its output, and records what it did in the state.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from .primitives import Paths, list_tree, read_text, run_command, write_text
from .state import State

JSON_OBJ = re.compile(r"\{.*\}", re.S)


class ToolError(Exception):
    pass


class Tools:
    def __init__(self, workdir: Path, output_dir: Path, state: State, cfg: dict):
        self.paths = Paths(workdir)
        self.workdir = Path(workdir)
        self.output_dir = Path(output_dir)
        self.state = state
        self.cfg = cfg
        self.max_out = int(cfg.get("max_tool_output_chars", 6000))
        self.py_timeout = int(cfg.get("python_timeout_s", 180))
        self.registry = {
            "plan": self.plan, "list_files": self.list_files, "read_file": self.read_file,
            "inspect_data": self.inspect_data, "run_python": self.run_python, "write_file": self.write_file,
        }

    # ------------------------------------------------------------ helpers
    def spec(self) -> str:
        return (
            "TOOLS (call exactly one per turn):\n"
            "- plan(checklist: str): record your analysis plan: every exclusion/transformation rule from the Methods in order, "
            "the exact test/model and its options, how each claim slot maps to a computed quantity. Call this first.\n"
            "- list_files(): list files in the task directory.\n"
            "- read_file(path: str, max_chars: int = 8000): read a text file.\n"
            "- inspect_data(path: str = 'data.csv'): shape, dtypes, head, summary statistics, missing counts, category counts.\n"
            "- run_python(code: str, save_as: str = null): run Python in the task directory (pandas, numpy, scipy, statsmodels available). "
            "If save_as is given the code is also saved to that file. Print results as JSON so they are captured.\n"
            "- write_file(path: str, content: str): write a text file in the task directory.\n"
            "- submit(claims: {id: number}, analysis_file: str = 'analysis.py' OR analysis_code: str): submit final claims. "
            "The harness re-runs the analysis script and checks that it prints the same claims; it also checks every slot is filled "
            "and values are sane. If the check fails you get the problems back and can continue."
        )

    def _trim(self, text: str) -> str:
        if len(text) <= self.max_out:
            return text
        head = self.max_out * 2 // 3
        return text[:head] + f"\n...[{len(text) - self.max_out} chars omitted]...\n" + text[-(self.max_out - head):]

    def call(self, name: str, args: dict) -> str:
        fn = self.registry.get(name)
        if fn is None:
            raise ToolError(f"unknown tool '{name}'. Available: {', '.join(self.registry)}, submit")
        if not isinstance(args, dict):
            raise ToolError("args must be an object")
        try:
            return fn(**args)
        except TypeError as e:
            raise ToolError(f"bad arguments for {name}: {e}")

    # -------------------------------------------------------------- tools
    def plan(self, checklist: str = "", **_) -> str:
        if not str(checklist).strip():
            raise ToolError("plan requires a non-empty checklist")
        self.state.plan = str(checklist)
        return "Plan recorded. It will stay visible in your progress notes. Now inspect the data and implement it step by step."

    def list_files(self, **_) -> str:
        return "\n".join(list_tree(self.workdir)) or "(empty)"

    def read_file(self, path: str, max_chars: int = 8000, **_) -> str:
        p = self.paths.resolve(path)
        if not p.exists():
            raise ToolError(f"no such file: {path}")
        return self._trim(read_text(p, max_chars=int(max_chars)))

    def inspect_data(self, path: str = "data.csv", **_) -> str:
        p = self.paths.resolve(path)
        if not p.exists():
            raise ToolError(f"no such file: {path}")
        code = (
            "import pandas as pd, json\n"
            f"df = pd.read_csv({str(p)!r})\n"
            "print('shape:', df.shape)\nprint('dtypes:'); print(df.dtypes.to_string())\n"
            "print('head:'); print(df.head(5).to_string())\n"
            "print('describe:'); print(df.describe().T.to_string())\n"
            "print('missing per column:'); print(df.isna().sum().to_string())\n"
            "for c in df.columns:\n"
            "    if df[c].dtype == object or df[c].nunique() <= 6:\n"
            "        print(f'value counts {c}:', df[c].value_counts(dropna=False).to_dict())\n"
        )
        res = run_command([sys.executable, "-c", code], cwd=self.workdir, timeout=60)
        return self._trim(res["stdout"] + ("\nSTDERR:\n" + res["stderr"] if res["stderr"].strip() else ""))

    def run_python(self, code: str, save_as: str | None = None, **_) -> str:
        if not str(code).strip():
            raise ToolError("run_python requires code")
        n = len(self.state.scripts) + 1
        name = f"scratch_{n:02d}.py"
        script_path = self.output_dir / "scripts" / name
        write_text(script_path, code)
        if save_as:
            write_text(self.paths.resolve(save_as), code)
        res = run_command([sys.executable, str(script_path)], cwd=self.workdir, timeout=self.py_timeout)
        out = res["stdout"]
        err = res["stderr"]
        summary = (out.strip().splitlines() or [err.strip()[-200:] if err.strip() else "(no output)"])[-1][:200]
        self.state.scripts.append({"name": name + (f" -> {save_as}" if save_as else ""), "returncode": res["returncode"], "summary": summary})
        captured = self._capture_json(out)
        if captured:
            self.state.draft_claims = captured
        if res["returncode"] != 0:
            self.state.failures.append(f"{name}: exit {res['returncode']}: {err.strip()[-200:]}")
        text = f"exit code: {res['returncode']}" + (" (TIMED OUT)" if res["timed_out"] else "") + "\nSTDOUT:\n" + out
        if err.strip():
            text += "\nSTDERR:\n" + err[-3000:]
        return self._trim(text)

    def write_file(self, path: str, content: str, **_) -> str:
        p = self.paths.resolve(path)
        n = write_text(p, str(content))
        return f"wrote {n} chars to {path}"

    @staticmethod
    def _capture_json(stdout: str) -> dict:
        for line in reversed(stdout.strip().splitlines()):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    d = json.loads(line)
                    if isinstance(d, dict) and all(isinstance(v, (int, float)) for v in d.values()):
                        return d
                except json.JSONDecodeError:
                    continue
        return {}
