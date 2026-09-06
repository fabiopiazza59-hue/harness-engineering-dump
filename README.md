# SciHarness: an LLM-built, feedback-evolved harness for reproducing published analyses

This repo is a working implementation of the idea in *HarnessDev* (arXiv 2609.01437, see
`docs/harnessdev-paper-goal-analysis.md`): treat the agent harness as the thing being developed,
let an LLM build it from a weak seed, let an LLM keep improving it from execution feedback, and
measure whether the improvements are real. It applies the seven guardrails that the paper's
evidence supports (`docs/PROTOCOL.md`) to one narrow scientific task family.

**Task family.** Reproduce the numbers a paper reports, from its Methods section and the
accompanying CSV. The harness sees a methods-only view with every result withheld, plus a list of
claim slots (group sizes, means, test statistics, p-values, coefficients, odds and hazard ratios,
adjusted p-values, ...). It must return numbers and a script that recomputes them.

**Scoring.** Deterministic. Fraction of claim slots within a per-type tolerance, multiplied by a
provenance gate: the submitted `analysis.py` is re-run in a clean copy of the task directory and
must reproduce the submitted claims. No model is involved in the score. An LLM judge exists for
uploaded papers without numeric truth and is reported separately.

## Layout

| Path | What |
|---|---|
| `docs/PROTOCOL.md` | The contract: task family, scoring, roles, splits, guardrails |
| `docs/LEDGER.md` | Full evolution ledger (feedback and held-out), written by the controller |
| `seed/harness/` | The weak seed: runnable, policy-free, scores 0 (git tag `seed`) |
| `harness/` | The current promoted harness (git tag `H0` = Creation result). Evolved candidates live on branch `evolution` |
| `tasks/generator/` | Synthetic paper generators: easy tier (6 analysis types) and hard tier (6 more, messy data) |
| `tasks/{dev,feedback,heldout}/` | Harness-visible task files. Truth lives in `evalkit/truth/<split>/` |
| `evalkit/` | `score.py`, `run_eval.py`, `noise.py`, `judge.py`, `audit_harness.py`, `heldout_results/` |
| `evolve/evolve.py` | Evolution controller (forced diagnosis, isolated worktree, hidden held-out, no auto-promotion) |
| `ui/` | FastAPI + single page: drop papers, build tasks, run, validate, judge, promote versions |
| `configs/` | `executor.json` (runtime model), `creator.json` (evolver), `judge.json` |

## Quickstart

```bash
make deps                      # python deps (needs Python 3.11+)
make tasks                     # regenerate dev/feedback/heldout (deterministic seeds)
make seed-check                # weak seed on dev: scores 0
make dev                       # current harness on dev
make feedback                  # feedback set x3 (the evolver's signal)
make heldout                   # held-out x3 (stored under evalkit/heldout_results)
make noise                     # noise band of a repeated run
make evolve                    # one evolution round (see docs/PROTOCOL.md section 5)
make ui                        # http://localhost:8765
```

The runtime model is whatever `configs/executor.json` says. Backends: `claude-cli` (headless
`claude -p`, the default, uses your Claude Code login), `anthropic` (raw Messages API with
`ANTHROPIC_API_KEY`), `openai` (any chat-completions endpoint). The harness never hard-codes a
model, a step cap, or a timeout; `evalkit/audit_harness.py` checks that.

## The UI

`python ui/server.py`, then open http://localhost:8765.

1. **Papers.** Drop a PDF (plus its CSV, plus optionally a truth JSON). *Build task* runs the
   LLM task builder: it extracts the reported numbers as ground-truth claim slots and writes a
   methods-only view with every number replaced by a placeholder, so the harness cannot copy
   results from the paper.
2. **Validate.** Pick a task and a harness version, run it, and see every claim next to the
   truth with the scorer's verdict and tolerance. *Run LLM judge* adds a second opinion against
   the full paper and a methods-fidelity rubric. Tick or cross each claim yourself; verdicts are
   saved with the run.
3. **Versions.** The evolution ledger with feedback and held-out columns side by side and the
   noise band. *Promote* is the only way a version becomes the current harness.
4. **Runs.** Everything that has been run, with cost.

## Results

See the bottom of this file and `docs/LEDGER.md` for the numbers from this session.

### What happened in this session (2026-09-06)

Executor: Claude Sonnet 5 via headless `claude -p`, effort medium. Creator: Claude in Claude Code
(Creation), Claude Opus 5 via `claude -p` (Evolution). Scorer: deterministic. Every number below is
the mean task score (claim accuracy times provenance gate) over all runs of a split.

| version | what changed | dev (3) | feedback (16 tasks) | held-out (16 tasks, hidden) | crash rate | verdict by the noise rule |
|---|---|---|---|---|---|---|
| seed | policy-free compatibility layer | 0.00 | – | – | – | – |
| H0 | Creation from the seed on 3 dev tasks | 1.00 | 0.917 (x3, 48 runs) | 0.875 (x3, 48 runs) | fb 8.3% / ho 12.5% | baseline |
| H1 | round 1: JSON repair layer in the action parser, informative parse errors | 1.00 | 1.000 (x2, 32 runs) | 0.993 (x2, 32 runs) | 0% / 0% | within noise band |
| H2 | round 2: verification gate re-runs `analysis.py` in a clean copy of the task files; every exit path ships only claims its script reproduces | 1.00 | 1.000 (x2, 32 runs) | 1.000 (x2, 32 runs) | 0% / 0% | within noise band |

Reading the table honestly:

- **Creation worked.** H0 went from a zero-scoring seed to 0.92 / 0.88 in one Creation pass, and
  when it did not crash it reproduced even the hard tier (Cox from dates with administrative
  censoring, Mantel-Haenszel, HC3 interaction models, BH correction, messy exports).
- **Every H0 failure was one harness bug.** All 10 zero-score runs out of 96 were the same
  all-or-nothing crash: the executor emits one closing brace too few on long nested JSON, the
  parser rejected it three times, and the run ended with nothing submitted.
- **Evolution round 1 found exactly that bug from the trajectories**, replayed all 20 logged
  replies through a repaired parser (16 previously fatal replies now parse), and added a bounded
  repair layer. Crash rate went from 8 to 12 percent to 0 on 64 fresh runs. That is a real,
  transferable fix, and the held-out set confirms it.
- **Evolution round 2 had no failures to look at** and still produced a defensible change: it
  compared the harness's verification gate against the scorer's contract, found the gate was
  weaker (it re-ran scripts in the live workdir, not a clean copy) and that non-passing exits
  shipped claims the gate had just rejected, and closed both gaps. Held-out went to 1.000. It is
  a latent-defect fix; the feedback set could not have revealed it.
- **The noise-band rule says "within noise band" for both rounds.** With 3 repeats and
  all-or-nothing crashes, the H0 band is 0.19, wider than the 0.083 of headroom that existed.
  The paper's warning applies: score deltas of this size are not evidence on their own. The
  crash-rate column (0 of 64 vs 10 of 96) is the signal that survives that caveat.
- **The one held-out miss of H1** (Mantel-Haenszel confidence interval, 2 claims) was a genuine
  methods ambiguity: the paper says "95% CI" without naming the variance estimator. That is the
  kind of error a harness cannot fix and a judge has to adjudicate.
- **Nothing was promoted.** `harness/` is still H0. The Versions tab shows H1 and H2 with both
  columns; promoting is a human decision.

Cost of the whole session: about 27 USD of evaluation runs, 5.6 USD for the two creator rounds,
under 1 USD for UI runs, builder and judge calls. A single task run costs 5 to 12 cents.

Full ledger with per-task tables, diagnoses and changelogs: `docs/LEDGER.md`. Screenshots of the
UI flow: `runs/ui_shots/`.

## Honest limitations

- The task corpus is synthetic. It is realistic in the ways that matter for the harness
  (exclusion rules, transformations, test variants, messy exports, derived variables), but real
  papers are vaguer and their data are rarely attached. The UI path for uploaded papers relies on
  the LLM task builder for both the claim slots and the withheld-methods view; check its output.
- Held-out isolation is by construction (the evolver's worktree contains no truth and no held-out
  task) plus a transcript audit, not by a sandbox. Treat generated harness code as untrusted.
- One trajectory per round, small task sets, and a noise band of roughly 0.1: the same caveat the
  paper makes applies here. Do not read a single round's gain as evidence.
