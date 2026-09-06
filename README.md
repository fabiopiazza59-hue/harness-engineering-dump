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
| `harness/` | The current promoted harness (git tag `H0` = Creation result) |
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

RESULTS_PLACEHOLDER

## Honest limitations

- The task corpus is synthetic. It is realistic in the ways that matter for the harness
  (exclusion rules, transformations, test variants, messy exports, derived variables), but real
  papers are vaguer and their data are rarely attached. The UI path for uploaded papers relies on
  the LLM task builder for both the claim slots and the withheld-methods view; check its output.
- Held-out isolation is by construction (the evolver's worktree contains no truth and no held-out
  task) plus a transcript audit, not by a sandbox. Treat generated harness code as untrusted.
- One trajectory per round, small task sets, and a noise band of roughly 0.1: the same caveat the
  paper makes applies here. Do not read a single round's gain as evidence.
