#!/usr/bin/env python3
"""Evolution controller: feedback-driven harness improvement with the protocol's guardrails.

    python evolve/evolve.py --rounds 2 --start H0 --baseline-run fb_H0_x3

Each round:
  1. make an isolated worktree from the lineage head containing ONLY harness/, the dev tasks
     (with their truth), and a feedback packet (scores, per-claim errors, trajectories of failed
     runs on the feedback set, and the visible ledger without held-out columns);
  2. run the creator model (claude -p, configs/creator.json) under the evolution contract:
     it must write diagnosis.md (named failure modes citing feedback task ids and trajectory
     evidence) BEFORE editing, then edit harness/, then write changelog.md;
  3. reject the round if diagnosis.md is missing or cites no feedback task; otherwise commit
     harness/ on branch `evolution`, audit it, smoke-test on dev, evaluate on the feedback set;
  4. evaluate on the held-out set and store the result where the creator never sees it;
  5. append to evolve/ledger.jsonl (full) and docs/LEDGER.md (full). The creator only ever sees
     the feedback columns.
Nothing here promotes a version into harness/. A human does that in the UI.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKTREES = ROOT / "evolve" / "worktrees"
LEDGER = ROOT / "evolve" / "ledger.jsonl"
LEDGER_MD = ROOT / "docs" / "LEDGER.md"
FEEDBACK_SPLIT = "feedback"
HELDOUT_SPLIT = "heldout"


def sh(cmd, cwd=ROOT, check=True, timeout=None, env=None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=check, timeout=timeout, env=env)


def git(*args, cwd=ROOT, check=True) -> str:
    return sh(["git", *args], cwd=cwd, check=check).stdout.strip()


# ----------------------------------------------------------------------------- feedback packet
def load_results(run_id: str) -> list[dict]:
    p = ROOT / "runs" / run_id / "results.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def summary_of(run_id: str) -> dict:
    return json.loads((ROOT / "runs" / run_id / "summary.json").read_text())


def fail_rate(run_id: str) -> float:
    """Fraction of runs that ended with no claims submitted (crash-type failures)."""
    rows = load_results(run_id)
    return round(sum(1 for r in rows if not r.get("submitted_any")) / max(1, len(rows)), 4)


def noise_band(run_id: str) -> dict:
    sys.path.insert(0, str(ROOT / "evalkit"))
    from noise import band, repeat_means
    return band(repeat_means(run_id))


def ledger_rows() -> list[dict]:
    if not LEDGER.exists():
        return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]


def visible_ledger_md(rows: list[dict]) -> str:
    lines = ["# Evolution ledger (creator view: feedback set only)", "",
             "| version | commit | feedback mean | noise band (H0) | run fail-rate | feedback per-task | hypothesis | outcome |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        pt = " ".join(f"{k.split('_')[0]}{k.split('_')[1]}={v['score']:.2f}" for k, v in sorted(r.get("feedback_per_task", {}).items()))
        lines.append(f"| {r['version']} | {r['commit'][:8]} | {r.get('feedback_mean', 'n/a')} | {r.get('noise_band', 'n/a')} | {r.get('feedback_fail_rate', 'n/a')} | {pt} | "
                     f"{r.get('hypothesis', '')[:120].replace('|', '/')} | {r.get('outcome', '')} |")
    return "\n".join(lines) + "\n"


def build_feedback_packet(dst: Path, run_id: str, rows: list[dict]):
    """Write feedback/ into the worktree: summary, per-claim errors with truth, failed trajectories."""
    fb = dst / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    results = load_results(run_id)
    summ = summary_of(run_id)
    lines = [f"# Feedback packet: run {run_id}", "",
             f"Feedback set mean score: {summ['mean_score']}  raw accuracy: {summ['mean_raw_accuracy']}  provenance rate: {summ['provenance_rate']}  "
             f"timeouts: {summ['timeouts']}  mean cost/run: {round(summ['total_cost_usd'] / max(1, len(results)), 3)} USD", "",
             "Score = fraction of claim slots within tolerance, or 0 when analysis.py does not reproduce the submitted claims.", "",
             "| task | repeat | score | raw | provenance | steps/duration | wrong or missing claims (pred vs truth) |", "|---|---|---|---|---|---|---|"]
    failed_dirs = []
    for r in sorted(results, key=lambda x: (x["task_id"], x.get("repeat", 0))):
        wrong = [f"{c['id']}: {c['pred']} vs {round(c['truth'], 4) if isinstance(c['truth'], float) else c['truth']}"
                 for c in r.get("per_claim", []) if not c["correct"]]
        prov = "ok" if r.get("provenance_ok") else f"FAIL ({r.get('provenance_log', '')[:60]})"
        lines.append(f"| {r['task_id']} | {r.get('repeat', 0)} | {r['score']} | {r['raw_accuracy']} | {prov} | {r.get('duration_s', '?')}s | {'; '.join(wrong)[:400]} |")
        if r["score"] < 1.0:
            failed_dirs.append((r["task_id"], r.get("repeat", 0), ROOT / r["run_dir"] / "out"))
    lines += ["", "## Per-task means", ""]
    for tid, row in sorted(summ["per_task"].items()):
        lines.append(f"- {tid}: score {row['score']}, raw {row['raw_accuracy']}, provenance {row['provenance_rate']}")
    lines += ["", "## Failed run artifacts", "", "Each failed (task, repeat) has a folder under feedback/runs/<task>_r<k>/ with trajectory.jsonl, "
              "response.md, claims.json, analysis.py, state.json, stderr.log. Read the trajectories before diagnosing.", ""]
    for tid, rep, out in failed_dirs:
        d = fb / "runs" / f"{tid}_r{rep}"
        d.mkdir(parents=True, exist_ok=True)
        for f in ("trajectory.jsonl", "response.md", "claims.json", "analysis.py", "state.json", "stderr.log", "stdout.log"):
            if (out / f).exists():
                shutil.copy(out / f, d / f)
        if (out / "scripts").exists():
            shutil.copytree(out / "scripts", d / "scripts", dirs_exist_ok=True)
        lines.append(f"- feedback/runs/{tid}_r{rep}/")
    (fb / "summary.md").write_text("\n".join(lines) + "\n")
    (fb / "ledger_visible.md").write_text(visible_ledger_md(rows))
    # feedback-set truth is allowed: it is the development signal
    for tid in summ["per_task"]:
        tdir = ROOT / "evalkit" / "truth" / FEEDBACK_SPLIT / tid
        if tdir.exists():
            d = fb / "truth" / tid
            d.mkdir(parents=True, exist_ok=True)
            for f in ("truth.json", "paper_full.md"):
                if (tdir / f).exists():
                    shutil.copy(tdir / f, d / f)
    return len(failed_dirs)


# ----------------------------------------------------------------------------- worktree
def make_worktree(name: str, commit: str) -> Path:
    WORKTREES.mkdir(parents=True, exist_ok=True)
    wt = WORKTREES / name
    if wt.exists():
        sh(["git", "worktree", "remove", "--force", str(wt)], check=False)
        shutil.rmtree(wt, ignore_errors=True)
    git("worktree", "prune")
    git("worktree", "add", "--detach", str(wt), commit)
    # keep only what the creator may see
    for child in list(wt.iterdir()):
        if child.name in ("harness", ".git"):
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    # dev tasks with truth (allowed development cases) and the tooling to run them
    for split in ("dev",):
        shutil.copytree(ROOT / "tasks" / split, wt / "devtasks" / split)
        shutil.copytree(ROOT / "evalkit" / "truth" / split, wt / "devtasks" / "truth" / split)
    (wt / "configs").mkdir()
    shutil.copy(ROOT / "configs" / "executor.json", wt / "configs" / "executor.json")
    shutil.copy(ROOT / "evalkit" / "score.py", wt / "score.py")
    (wt / "run_dev.py").write_text(RUN_DEV)
    return wt


RUN_DEV = '''#!/usr/bin/env python3
"""Local check: run the harness on the dev tasks and score them. Unlimited and free of budget."""
import json, os, shutil, subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from score import score_run
only = sys.argv[1:]
tasks = sorted(p for p in (here / "devtasks" / "dev").iterdir() if p.is_dir())
for t in tasks:
    if only and t.name not in only:
        continue
    run = here / "devruns" / t.name
    if run.exists(): shutil.rmtree(run)
    work, out = run / "work", run / "out"
    shutil.copytree(t, work); out.mkdir(parents=True)
    env = dict(os.environ); env["PYTHONPATH"] = str(here); env.pop("CLAUDECODE", None)
    subprocess.run([sys.executable, "-m", "harness", "run", "--task-json", str(work / "task.json"), "--workdir", str(work),
                    "--model-config", str(here / "configs" / "executor.json"), "--output-dir", str(out)], cwd=here, env=env)
    truth = json.loads((here / "devtasks" / "truth" / "dev" / t.name / "truth.json").read_text())
    s = score_run(t, out, truth)
    print(t.name, "score", s["score"], "raw", s["raw_accuracy"], "provenance", s["provenance_ok"], s["provenance_log"])
'''

CONTRACT = """
# Harness Evolution Contract (SciHarness)

You are the harness engineer for an agent that reproduces published statistical analyses from a paper's
Methods section and a CSV. The harness (harness/, run as `python -m harness run ...`) is executed later by a
DIFFERENT runtime model configured in configs/executor.json. You are improving the harness code, not solving tasks.

## What you have
- harness/: the current harness (E execution loop, T tools, C context, S state, L lifecycle, V verification).
- feedback/summary.md: scores of the current version on the feedback set, per-claim errors with the true values,
  and paths to the full artifacts of every failed run (feedback/runs/*/trajectory.jsonl etc.).
- feedback/truth/<task>/: truth.json and the full paper for each feedback task (development signal, allowed).
- feedback/ledger_visible.md: previous versions and their feedback scores.
- devtasks/ and run_dev.py: three development tasks you may run locally as often as you like
  (`python3 run_dev.py` or `python3 run_dev.py dev_002_ttest`). Each run costs real model calls; keep it purposeful.

## Required working order (enforced by the controller)
1. DIAGNOSE FIRST. Read feedback/summary.md and the trajectories of the failed runs. Write diagnosis.md with
   exactly these headings:
   ## Failure modes   - one bullet per named failure mode, each citing feedback task ids and quoting the
                        trajectory or script evidence (file path + what you saw). Executor-capability limits are not
                        a failure mode: name the harness structure that would have caught or prevented the error.
   ## Hypothesis      - the single change most likely to raise held-out performance, and why.
   ## Planned change  - which module(s) and what exactly.
   ## Verification    - how you will check it (which dev tasks, what you expect).
   The controller rejects the round if diagnosis.md is missing, lacks these headings, or cites no feedback task id.
2. EDIT harness/ to implement the planned change. Keep edits targeted. Do not add code that is never called.
3. VERIFY locally with run_dev.py; fix regressions.
4. Write changelog.md: what changed, the hypothesis, and what the dev check showed.

## Hard rules (audited; a violation zeroes the version)
- No hard-coded task ids, claim values, or benchmark-specific shortcuts. No reading of anything outside this
  directory. No executor-specific constants (model names, step caps, timeouts) in harness code: read them
  from the model config. Do not replace the provider-neutral gateway in harness/llm.py with a provider SDK.
- Keep the CLI contract and the output files (result.json with honest status, trajectory.jsonl, response.md,
  claims.json, analysis.py). Do not make the harness assert success it has not verified.
- Do not touch feedback/, devtasks/, score.py, run_dev.py, configs/.

## What good harness work looks like here
Prefer structural fixes over prompt tweaks: a verification step that catches a class of error, a context
element that makes the Methods rules explicit, a tool that removes a source of mistakes, a recovery path for a
failure you saw. One well-verified change beats three speculative ones. Deletion is a valid change.
"""


def run_creator(wt: Path, round_no: int, cfg: dict) -> dict:
    prompt = (f"Evolution round {round_no}. Work in the current directory. Follow the contract: read feedback/summary.md and the "
              f"failed trajectories, write diagnosis.md, then edit harness/, verify with run_dev.py, and write changelog.md. "
              f"Finish with a short summary of what you changed and what you expect.")
    allowed = ["Read", "Edit", "Write", "Glob", "Grep", "Bash(python3:*)", "Bash(python:*)", "Bash(ls:*)", "Bash(cat:*)",
               "Bash(head:*)", "Bash(tail:*)", "Bash(grep:*)", "Bash(wc:*)", "Bash(diff:*)", "Bash(git diff:*)", "Bash(git status:*)",
               "Bash(sed -n:*)", "Bash(find:*)"]
    # the prompt goes on stdin: --allowedTools is variadic and would swallow a trailing positional argument
    cmd = ["claude", "-p", "--no-session-persistence", "--output-format", "json", "--model", cfg.get("model", "opus"),
           "--max-turns", str(cfg.get("max_turns", 90)), "--append-system-prompt", CONTRACT, "--allowedTools", *allowed]
    if cfg.get("effort"):
        cmd += ["--effort", str(cfg["effort"])]
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=str(wt), input=prompt, capture_output=True, text=True, timeout=int(cfg.get("timeout_s", 3000)), env=env)
        raw = proc.stdout
    except subprocess.TimeoutExpired as e:
        raw = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    (wt / "creator_session.json").write_text(raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"is_error": True, "result": raw[-2000:]}
    return {"duration_s": round(time.time() - t0, 1), "cost_usd": data.get("total_cost_usd"), "turns": data.get("num_turns"),
            "is_error": data.get("is_error"), "summary": (data.get("result") or "")[:3000]}


def check_diagnosis(wt: Path) -> tuple[bool, str]:
    p = wt / "diagnosis.md"
    if not p.exists():
        return False, "diagnosis.md missing"
    text = p.read_text()
    for h in ("## Failure modes", "## Hypothesis", "## Planned change", "## Verification"):
        if h.lower() not in text.lower():
            return False, f"diagnosis.md lacks heading '{h}'"
    ids = set(re.findall(r"\bfb_\d{3}_[a-z]+", text))
    if not ids:
        return False, "diagnosis.md cites no feedback task id"
    return True, f"cites {sorted(ids)}"


def transcript_audit(wt: Path) -> list[str]:
    """Flag any creator access to held-out material by scanning its session output."""
    raw = (wt / "creator_session.json").read_text() if (wt / "creator_session.json").exists() else ""
    hits = []
    for pat in ("evalkit/truth", "heldout", "ho_0"):
        if pat in raw:
            hits.append(pat)
    return hits


def eval_split(split: str, harness_dir: Path, run_id: str, repeats: int, label: str) -> dict:
    cmd = [sys.executable, str(ROOT / "evalkit" / "run_eval.py"), "--split", split, "--harness-dir", str(harness_dir.relative_to(ROOT)),
           "--repeats", str(repeats), "--workers", "3", "--run-id", run_id, "--label", label]
    proc = sh(cmd, check=False, timeout=7200)
    (ROOT / "runs" / f"{run_id}.log").write_text(proc.stdout + "\n" + proc.stderr)
    return summary_of(run_id)


def append_ledger(row: dict):
    with open(LEDGER, "a") as fh:
        fh.write(json.dumps(row) + "\n")
    rows = ledger_rows()
    lines = ["# Evolution ledger (full, controller view)", "",
             "Held-out columns are never shown to the creator. A candidate 'improves' only when its feedback gain exceeds the H0 noise band.", "",
             "| version | commit | round | feedback mean | Δ vs H0 | noise band | fb fail-rate | held-out mean | Δ vs H0 | ho fail-rate | diff (+/-) | verdict | hypothesis |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    h0 = next((r for r in rows if r["version"] == "H0"), None)
    for r in rows:
        dfb = round(r["feedback_mean"] - h0["feedback_mean"], 4) if h0 and r.get("feedback_mean") is not None else ""
        dho = round(r["heldout_mean"] - h0["heldout_mean"], 4) if h0 and r.get("heldout_mean") is not None and h0.get("heldout_mean") is not None else ""
        lines.append(f"| {r['version']} | {r['commit'][:8]} | {r.get('round', '')} | {r.get('feedback_mean', '')} | {dfb} | {r.get('noise_band', '')} | {r.get('feedback_fail_rate', '')} | "
                     f"{r.get('heldout_mean', '')} | {dho} | {r.get('heldout_fail_rate', '')} | {r.get('diff', '')} | {r.get('outcome', '')} | {r.get('hypothesis', '')[:160].replace('|', '/')} |")
    lines += ["", "## Round notes", ""]
    for r in rows:
        if r.get("round"):
            lines += [f"### {r['version']} (round {r['round']}, commit {r['commit'][:8]})", "",
                      f"- creator: {r.get('creator', {})}", f"- diagnosis check: {r.get('diagnosis_check', '')}",
                      f"- audit: {r.get('audit', '')}", f"- smoke (dev): {r.get('smoke', '')}",
                      f"- feedback per task: {json.dumps({k: v['score'] for k, v in r.get('feedback_per_task', {}).items()})}",
                      f"- held-out per task: {json.dumps({k: v['score'] for k, v in r.get('heldout_per_task', {}).items()})}",
                      "", "Changelog:", "", (r.get("changelog") or "(none)")[:2500], ""]
    LEDGER_MD.write_text("\n".join(lines) + "\n")


def record_h0(commit: str, fb_run: str, ho_run: str | None):
    rows = ledger_rows()
    if any(r["version"] == "H0" for r in rows):
        return
    fb = summary_of(fb_run)
    nb = noise_band(fb_run)
    row = {"version": "H0", "commit": commit, "round": 0, "feedback_run": fb_run, "feedback_mean": fb["mean_score"],
           "feedback_per_task": fb["per_task"], "feedback_fail_rate": fail_rate(fb_run), "noise_band": nb["band"], "noise": nb, "hypothesis": "baseline from Creation",
           "outcome": "baseline", "diff": "", "created_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    if ho_run:
        ho = summary_of(ho_run)
        row.update({"heldout_run": ho_run, "heldout_mean": ho["mean_score"], "heldout_per_task": ho["per_task"], "heldout_fail_rate": fail_rate(ho_run)})
    append_ledger(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--start", default=None, help="commit/tag to start the lineage from (default: last ledger commit or H0)")
    ap.add_argument("--baseline-run", default="fb_H0_x3")
    ap.add_argument("--baseline-heldout-run", default="ho_H0_x3")
    ap.add_argument("--creator", default="configs/creator.json")
    a = ap.parse_args()
    cfg = json.loads((ROOT / a.creator).read_text())
    h0_commit = git("rev-parse", "H0^{commit}")
    record_h0(h0_commit, a.baseline_run, a.baseline_heldout_run if (ROOT / "runs" / a.baseline_heldout_run / "summary.json").exists() else None)
    rows = ledger_rows()
    head = a.start and git("rev-parse", a.start + "^{commit}") or rows[-1]["commit"]
    last_fb_run = rows[-1].get("feedback_run", a.baseline_run)
    band_val = next(r for r in rows if r["version"] == "H0")["noise_band"]
    h0_fb = next(r for r in rows if r["version"] == "H0")["feedback_mean"]

    for _ in range(a.rounds):
        round_no = max([r.get("round", 0) for r in rows]) + 1
        version = f"H{round_no}"
        print(f"=== round {round_no}: lineage head {head[:8]}, feedback signal from {last_fb_run} ===", flush=True)
        wt = make_worktree(f"cand_{round_no}", head)
        n_failed = build_feedback_packet(wt, last_fb_run, rows)
        print(f"feedback packet built ({n_failed} failed runs) at {wt}", flush=True)
        creator = run_creator(wt, round_no, cfg)
        print(f"creator finished: {creator['turns']} turns, {creator['duration_s']}s, ${creator['cost_usd']}", flush=True)
        ok, why = check_diagnosis(wt)
        hits = transcript_audit(wt)
        row = {"version": version, "round": round_no, "parent": head, "creator": creator, "diagnosis_check": why,
               "transcript_audit_hits": hits, "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
               "diagnosis": (wt / "diagnosis.md").read_text()[:6000] if (wt / "diagnosis.md").exists() else "",
               "changelog": (wt / "changelog.md").read_text()[:6000] if (wt / "changelog.md").exists() else ""}
        m = re.search(r"## Hypothesis\s*(.+?)(?:\n## |\Z)", row["diagnosis"], re.S | re.I)
        row["hypothesis"] = (m.group(1).strip() if m else "").replace("\n", " ")[:400]
        if not ok:
            row.update({"commit": head, "outcome": f"REJECTED: {why}", "feedback_mean": None})
            append_ledger(row)
            rows = ledger_rows()
            print(f"round {round_no} rejected: {why}", flush=True)
            continue
        # commit harness changes in the worktree
        git("add", "-A", "harness", cwd=wt)
        diff = git("diff", "--cached", "--shortstat", cwd=wt)
        if not diff.strip():
            row.update({"commit": head, "outcome": "REJECTED: no code change", "feedback_mean": None, "diff": ""})
            append_ledger(row)
            rows = ledger_rows()
            continue
        sh(["git", "-c", "user.email=harness-evolver@local", "-c", "user.name=harness-evolver", "commit", "-q", "-m",
            f"{version}: {row['hypothesis'][:72] or 'evolution round ' + str(round_no)}\n\n{row['changelog'][:1500]}"], cwd=wt)
        commit = git("rev-parse", "HEAD", cwd=wt)
        git("branch", "-f", "evolution", commit)
        row.update({"commit": commit, "diff": diff.strip()})
        audit = sh([sys.executable, str(ROOT / "evalkit" / "audit_harness.py"), str(wt / "harness")], check=False)
        row["audit"] = "clean" if audit.returncode == 0 else audit.stdout.strip()[-800:]
        if audit.returncode != 0:
            row.update({"outcome": "REJECTED: audit violations", "feedback_mean": None})
            append_ledger(row)
            rows = ledger_rows()
            continue
        smoke = eval_split(cfg.get("smoke_split", "dev"), wt / "harness", f"dev_{version}", 1, f"{version} smoke")
        row["smoke"] = {"mean_score": smoke["mean_score"], "timeouts": smoke["timeouts"]}
        fb = eval_split(FEEDBACK_SPLIT, wt / "harness", f"fb_{version}_x{cfg.get('feedback_repeats', 2)}", int(cfg.get("feedback_repeats", 2)), f"{version} feedback")
        row.update({"feedback_run": fb["run_id"], "feedback_mean": fb["mean_score"], "feedback_per_task": fb["per_task"],
                    "feedback_fail_rate": fail_rate(fb["run_id"]), "feedback_cost_usd": fb["total_cost_usd"], "noise_band": band_val})
        gain = fb["mean_score"] - h0_fb
        row["outcome"] = ("improved beyond noise band" if gain > band_val else "regressed beyond noise band" if gain < -band_val else "within noise band")
        ho = eval_split(HELDOUT_SPLIT, wt / "harness", f"ho_{version}_x{cfg.get('heldout_repeats', 2)}", int(cfg.get("heldout_repeats", 2)), f"{version} heldout")
        row.update({"heldout_run": ho["run_id"], "heldout_mean": ho["mean_score"], "heldout_per_task": ho["per_task"], "heldout_fail_rate": fail_rate(ho["run_id"])})
        append_ledger(row)
        rows = ledger_rows()
        head, last_fb_run = commit, fb["run_id"]
        print(f"{version}: feedback {fb['mean_score']} (H0 {h0_fb}, band {band_val}) -> {row['outcome']}; held-out recorded (hidden from creator)", flush=True)


if __name__ == "__main__":
    main()
