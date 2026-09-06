"""E - the execution loop.

One turn = render context -> call LLM -> parse action -> dispatch tool or gate -> record.
Stops on a passing submission, budget exhaustion, or a forced finalisation.
"""
from __future__ import annotations

from pathlib import Path

from .audit import Trajectory
from .context import Transcript, system_prompt, task_message
from .lifecycle import Budget, ParseError, finalize, parse_action
from .llm import LLM, LLMError
from .state import State
from .tools import ToolError, Tools
from .verify import verify_submission


def run_loop(task: dict, workdir: Path, output_dir: Path, cfg: dict) -> dict:
    traj = Trajectory(output_dir)
    state = State.load(output_dir) if cfg.get("resume") else None
    state = state or State(task_id=str(task.get("task_id", "task")))
    tools = Tools(workdir, output_dir, state, cfg)
    llm = LLM(cfg)
    budget = Budget(cfg, state)
    transcript = Transcript(cfg, state)
    system = system_prompt(tools.spec())
    transcript.add_task(task_message(task, workdir, cfg))
    traj.log("start", task_id=state.task_id, provider=cfg.get("provider"), model=cfg.get("model"), max_steps=budget.max_steps)

    reason = "unknown"
    while True:
        stop = budget.exhausted()
        if stop:
            reason = stop
            break
        state.step += 1
        compacted = transcript.maybe_compact()
        if compacted:
            traj.log("compaction", step=state.step, size=transcript.size())
        try:
            raw = llm.chat(system, transcript.render())
        except LLMError as e:
            state.failures.append(f"llm: {e}")
            traj.log("llm_error", step=state.step, error=str(e))
            reason = f"LLM failure: {e}"
            break
        traj.log("model_reply", step=state.step, chars=len(raw), reply=raw[:4000])
        try:
            act = parse_action(raw)
        except ParseError as e:
            state.parse_failures += 1
            transcript.add_action(raw)
            transcript.add_observation(
                f"ERROR: {e}\nYour previous reply was NOT executed. Send the SAME action again, but as one "
                "syntactically complete JSON object and nothing else - count the closing braces, and escape every "
                'newline, quote and backslash inside string values. Shape: {"thought": "...", "action": {"tool": '
                '"...", "args": {...}}} (three closing braces at the end).')
            traj.log("parse_error", step=state.step, error=str(e))
            state.save(output_dir)
            continue
        state.parse_failures = 0
        transcript.add_action(raw)
        tool, args = act["action"]["tool"], act["action"]["args"]
        repaired = act.get("_repaired")
        if repaired:
            state.repairs += 1
            traj.log("parse_repair", step=state.step, tool=tool, repair=repaired)
            prefix = (f"NOTE: your reply was not valid JSON ({repaired}). The harness repaired it and ran "
                      f"{tool} as shown. Emit complete JSON next time; a repair can silently truncate your "
                      "arguments, so check the result below is what you intended.\n\n")
        else:
            prefix = ""

        if tool == "submit":
            claims = args.get("claims") or {}
            ok, problems, clean = verify_submission(task, workdir, output_dir, claims, args.get("analysis_code"),
                                                    args.get("analysis_file", "analysis.py"), cfg)
            state.submissions.append({"ok": ok, "problems": problems, "claims": clean})
            if clean:
                state.best_claims = clean
            if (output_dir / "analysis.py").exists():
                state.best_analysis = (output_dir / "analysis.py").read_text()
            traj.log("gate", step=state.step, ok=ok, problems=problems, n_claims=len(clean))
            if ok:
                reason = "verification gate passed"
                state.save(output_dir)
                break
            if budget.gate_exhausted():
                reason = "verification gate failed repeatedly; best-effort claims kept"
                state.save(output_dir)
                break
            transcript.add_observation(prefix + "SUBMISSION REJECTED by the verification gate:\n- "
                                       + "\n- ".join(problems) + "\nFix the issues and submit again.")
            state.save(output_dir)
            continue

        try:
            obs = tools.call(tool, args)
            traj.log("tool", step=state.step, tool=tool, args={k: (v[:300] if isinstance(v, str) else v) for k, v in args.items()},
                     observation=obs[:2000])
        except ToolError as e:
            obs = f"TOOL ERROR: {e}"
            state.failures.append(f"{tool}: {e}")
            traj.log("tool_error", step=state.step, tool=tool, error=str(e))
        transcript.add_observation(prefix + obs)
        state.save(output_dir)

    result = finalize(task, output_dir, workdir, state, llm.usage(), reason)
    traj.log("end", status=result["status"], reason=reason, usage=llm.usage())
    traj.close()
    return result
