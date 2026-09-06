# SciHarness protocol: LLM-built, feedback-evolved harness for reproducing published analyses

This document is the contract for the whole project. Everything in the repo follows it.
It applies the seven guardrails derived from the HarnessDev paper
(`docs/harnessdev-paper-goal-analysis.md`, section 10) to one narrow task family.

## 1. Task family: reproduce a published analysis

A task is a "paper" plus its dataset. The agent must reproduce the numbers the paper
reports, from the methods description alone.

Harness-visible inputs (in the task directory):

| File | Content |
|---|---|
| `task.json` | Task id, instructions, list of claim slots to fill, file names |
| `paper_methods.md` | Abstract, methods, and a results section with every number withheld |
| `data.csv` | The dataset |
| `data_dictionary.md` | Column descriptions |

Withheld from the harness (kept under `evalkit/truth/<split>/<task_id>/`):

| File | Content |
|---|---|
| `truth.json` | Claim values, per-claim tolerances, analysis type |
| `paper_full.md`, `paper.pdf` | The full paper with numbers, for humans and the UI |
| `reference_analysis.py` | The generator's reference code |

Required outputs (in the run's output directory):

| File | Content |
|---|---|
| `claims.json` | `{"claims": [{"id": ..., "value": <number>}], "notes": "..."}` |
| `analysis.py` | A script that, run from the task workdir, prints the same claims as JSON to stdout |
| `result.json`, `trajectory.jsonl`, `response.md` | Audit envelope shared by seed and harness |

Claim slots are the paper's reported quantities (group sizes, means, test statistics,
p-values, coefficients, odds ratios, R squared, ...). The harness sees the slot id and a
description, never the value.

## 2. Scoring (the verifiable metric)

`evalkit/score.py` scores a run without any model involvement:

1. **Per-claim accuracy.** A claim is correct when `|pred - truth| <= max(abs_tol, rel_tol * |truth|)`.
   Tolerances are set per claim type (counts exact, p-values abs 0.002 or rel 5%, effect sizes rel 2%, ...).
   `raw_accuracy` = fraction of claim slots correct. Missing or non-numeric values are incorrect.
2. **Provenance gate.** The scorer re-executes the submitted `analysis.py` in a clean copy of the task
   workdir with a timeout. If the script fails or its printed claims do not match the submitted
   `claims.json` within tolerance, the run's `score` is 0 regardless of `raw_accuracy`. This blocks
   copied or hallucinated numbers.
3. **Task score** = `raw_accuracy` if the provenance gate passes, else 0. Set score = mean of task scores.

Self-reported status in `result.json` is never a scoring input.

An LLM judge (`evalkit/judge.py`) exists only for uploaded papers with no numeric ground truth,
and for qualitative rubric items. Judge scores are reported separately and never feed the
evolution loop.

## 3. Roles

| Role | Who | Notes |
|---|---|---|
| Creator (builds and evolves the harness) | Claude inside Claude Code (Creation), `claude -p` with Opus (Evolution) | Never the same model config as the executor |
| Executor (runs inside the frozen harness) | Configured in `configs/executor.json`; default `claude-cli` + `sonnet` | Changing this file changes the executor, nothing else |
| Scorer | `evalkit/score.py`, deterministic | No model |
| Judge (optional) | `evalkit/judge.py` | Separate model config |
| Final version selection | A human, via the UI Versions tab | Nothing auto-promotes |

## 4. Splits

| Split | Size | Visible to | Purpose |
|---|---|---|---|
| `dev` | 3 | Creator during Creation | The 1 to 3 development cases of the paper |
| `feedback` | 10 | Evolution loop | Scores and trajectories are returned to the creator |
| `heldout` | 10 | Nobody during development | Scored after each version is frozen; never shown to the creator |

The evolution controller gives the creator a git worktree that contains only `harness/` and the
feedback-set artifacts. The held-out truth and results are physically outside it.

## 5. The seven guardrails, as implemented

1. **Narrow task family with a verifiable metric.** Section 1 and 2.
2. **Held-out split from day one.** `tasks/heldout` is generated with a separate seed; its truth
   lives in `evalkit/truth/heldout`; results go to `evalkit/heldout_results/`. The ledger shows
   feedback and held-out columns side by side.
3. **Noise band measured before believing any gain.** `evalkit/noise.py` runs one version
   several times on the feedback set and reports the spread. A candidate counts as improved only
   if its feedback gain exceeds the band.
4. **Creator and executor separated; no executor-specific constants.** Step limits, timeouts,
   context budgets, and the model name all come from `configs/executor.json` or the task, never
   from the harness source. The audit script `evalkit/audit_harness.py` greps for hard-coded
   model names and numeric step caps.
5. **Verification gate before done.** The harness cannot finish until every slot has a numeric
   value, `analysis.py` exists and reproduces `claims.json` when re-run, and sanity checks pass.
6. **Forced trace reading with an external ledger.** In every evolution round the creator must
   write `diagnosis.md` naming failure modes with task ids and trajectory evidence before any
   edit is accepted. Every round appends to `docs/LEDGER.md` (version, hypothesis, diff size,
   feedback score, noise band, held-out score filled in by the controller).
7. **Human approves the final version.** The UI lists versions with both scores; a person clicks
   Promote. The controller never changes `harness/` on its own.

## 6. Prohibited harness behaviour (audited)

No hard-coded task ids or values, no reading of anything under `evalkit/truth`, no replacing
the provider-neutral LLM gateway with a provider SDK, no `TODO`/`pass` placeholders on the
executable path, no degrading the agent to a single LLM call. The scorer's provenance gate and
`evalkit/audit_harness.py` check this after every evaluation.
