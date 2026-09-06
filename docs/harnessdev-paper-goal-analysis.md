# HarnessDev (arXiv 2609.01437v1): what the paper is trying to do

Source: *HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?*
ByteDance Seed, SUTD, Georgia Tech, M-A-P, TokenWave.AI. Dated 2 September 2026.
Project page: https://self-developing-agents.github.io/

## 1. The goal in one sentence

Change the unit of agent evaluation from *the answer a model gives inside a fixed
harness* to *the harness itself*, and measure whether a frontier LLM can build that
harness from almost nothing (Creation) and then keep improving it from execution
feedback (Evolution) without the gains being an illusion.

The paper is a benchmark and measurement paper, not a method paper. Its deliverable
is a protocol that makes "agent-built execution infrastructure" a measurable,
auditable object.

## 2. Why the authors think this goal matters

- **The harness moves the number as much as the weights do.** Their motivating
  fact: the same GPT-5 weights score 35.2% on Terminal-Bench 2.1 inside Terminus 2
  and 49.6% inside Codex CLI. The scaffold is not a detail of the setup.
- **Harnesses are never finished.** Real deployments need continuous development
  as requirements shift. The paper frames this through the forward-deployed
  engineer (FDE) role: the human who turns a capable model into a working system
  and stays with it. FDE work supplies three things benchmarks presuppose: a
  concrete target, a feedback signal, and an execution system. HarnessDev
  isolates the third one and asks whether the model can do that job.
- **Existing benchmarks hide this.** SWE-bench, GAIA, WebArena, tau-bench all fix
  the harness as experimental configuration. Harness-Bench varies the harness but
  still treats it as an input. Nobody was measuring the model's ability to
  *develop* the harness.
- **It is a different skill from ordinary coding.** When a model edits a normal
  program, the target is external and success is locally checkable. When it edits
  its own harness, it changes how it observes, plans, and recovers on every future
  task. It has to read its own traces, diagnose structural bottlenecks in the
  system it runs inside, and make changes that accumulate rather than one-off
  fixes. The authors argue frontier models already have this ability latent; what
  was missing is a benchmark.

## 3. The two research questions

| Stage | Question | Starting point | Signal available | Output |
|---|---|---|---|---|
| Creation (RQ1) | Can a model build an effective harness from a weak but runnable seed? | Shared seed `H_seed`, scores zero everywhere | Task-family spec, tool/permission constraints, short tutorial, 1 to 3 dev cases | Frozen harness `H` |
| Evolution (RQ2) | Can a model improve an existing harness while preserving what already works? | Its own RQ1 code harness `H0` | Results on a 100-task SWE-Pro feedback set and all 89 Terminal-Bench tasks | Frozen paired candidates and a creator-declared final version |

The formal pipeline is: `(L_C, D) -> H`, then `(H, L_E, x) -> y -> J -> score`.
Creator `L_C` builds the harness inside a development environment `D`
(Claude Code 2.1.177, or Codex 0.144.3 for GPT-5.5). The harness is frozen. An
executor `L_E` then runs inside it on downstream task `x` and an evaluator `J`
scores the output. Keeping these four roles separate is itself part of the goal:
it stops the paper from attributing the dev tool's help or the executor's raw
ability to the quality of the harness.

## 4. What the goal *is not*, and the design choices that enforce that

The paper spends most of its methodology on preventing a generated harness from
scoring for the wrong reason. Each design choice maps to a failure mode the
authors are explicitly trying to exclude.

- **Reproducing benchmark boilerplate.** Everyone starts from the same weak seed:
  a runnable compatibility layer that parses task and model config, exposes
  passive primitives (paths, files, search, process, LLM gateway, artifact I/O),
  and writes the audit envelope. It has no loop, no planner, no tool policy, no
  context management, no state, no verifier, no retry, no stopping rule. Unmodified
  it scores zero on all five benchmarks, so any nonzero score is the creator's
  execution logic. An empty repo would have mixed harness design with setup work;
  a mature agent would have given away the structure being tested.
- **Fitting to one model.** Every harness is run under two executors: Self-Eval
  (executor = creator, the regime users actually deploy) and Unified-Eval
  (every harness run by a fixed Gemini 3.1 Pro). A high unified score means the
  harness is a transferable software asset, not a fit to one model.
- **Memorizing development examples.** Hidden tasks, answers, and official scores
  are withheld during Creation. In Evolution, every official version is scored
  afterwards on 630 SWE-Pro instances disjoint from the 100-task feedback set,
  and those scores are never shown to the creator.
- **Claiming success instead of earning it.** The score path is isolated from the
  harness. Self-reported status is never a scoring input. SWE-Pro credit comes
  only from the real repository diff, Terminal-Bench credit only from final
  environment state.
- **Gaming the scorer.** The spec forbids hard-coding instance IDs or answers,
  consulting hidden tests or scorer internals, and replacing the provider-neutral
  LLM client. Every run keeps its trajectory, result, and metrics next to the
  frozen source so this can be audited post hoc. They audited every reported run
  and found no violations.
- **Winning by burning tokens.** Quality is reported on two axes: capability
  (held-out task success) and efficiency (executor tokens per task). Creator
  tokens used to build the harness are excluded.
- **A single lucky build.** Each creator builds three independent harnesses per
  benchmark and the score is avg@3, because independent creations from the same
  model can differ sharply (one Opus code harness collapses under Gemini because it
  hard-codes a 120-step limit tuned to its original executor).

## 5. The working definition of a harness

The paper abstracts a harness as `H = <E, T, C, S, L, V>`:

- **E** execution: loop, planning, stop conditions, scheduling
- **T** tools: interfaces, selection, I/O constraints, error handling
- **C** context: how tasks, code, logs, history, constraints enter the prompt
- **S** state: goals, hypotheses, progress, attempts, failures, artifact state
- **L** lifecycle: hooks, failure and timeout handling, recovery, finalization
- **V** verification: tests, checks, judges, artifact validation, trajectory

The creator is told it does not need six files with these names; it needs the
final system to actually *perform* these responsibilities rather than describe
them. The runtime LLM drives semantic decisions (what to edit, when to finish).
The harness's job is to make those decisions executable, observable, recoverable,
verifiable, and scorable. This division of labour is the clearest statement of
what the authors think a harness is for.

## 6. Scope of the instantiation

Creation covers four domains and five benchmarks, 2,207 unique downstream
instances in total: SWE-bench Pro public split (731), Terminal-Bench 2.1 (89),
MLE-bench (75), EQ-Bench3 (46), BrowseComp (1,266). Evolution is restricted to
code harnesses. Six creators: Opus 4.8, GPT-5.5, Gemini 3.1 Pro, DeepSeek V4 Pro,
Qwen 3.7 Max, Seed 2.0 Pro. Human-engineered references are the best verified
public system results per benchmark, explicitly *not* paired controls under a
common executor.

The Evolution protocol is worth noting because it models a real engineering
loop: a persistent git repo, an append-only feedback event stream, a fixed budget
of ten full paired evaluations, at most two five-task probes per round, no
controller-side accept/reject or rollback, and a `declare-final` call that only
accepts a commit with completed official evaluations on both benchmarks. The
creator decides everything: what to change, how to validate, when to submit, when
to stop. The advisory prompt even suggests keeping an external ledger because
conversation memory does not survive compaction.

## 7. What the paper claims to have established

**Creation: models can build runnable harnesses, and the distance to human
systems depends on the domain.**

- Under Self-Eval, Opus 4.8 leads with an average of 67.8 against a human
  reference of 86.2.
- Writing harnesses match the reference. MLE-bench harnesses exceed the selected
  reference (32.9 medal rate vs 24.0). Search and research show the largest gap.
  Code remains substantially behind (69.3 vs 80.0 on SWE-Pro for the best case).
- Edit size does not predict performance. Gemini adds the fewest lines (1,006)
  and gets the best Terminal-Bench score (68.8).
- State and memory are the clearest gap. Eleven of 18 code harnesses define a
  State class, one exposes a save interface, one implements checkpointing, and no
  checkpoint event appears in 26,679 recorded trajectories. Much generated
  structure is dead code: 124 of 587 writing features, 36 data mechanisms.
- Self-test count barely correlates with downstream score (Spearman 0.13 to
  0.26). Revision calls correlate at 0.57. Testing helps only when the creator
  reads the failure, makes a targeted change, and re-verifies.
- Execution cost varies about nineteen-fold on MLE-bench and higher cost does
  not reliably buy a higher score.

**Evolution: models can make useful local improvements, but robust, transferable
evolution is an open problem.**

- All five self-runtime lineages improve on the visible feedback pair. Held-out
  gains are smaller: +1.43 to +4.44 points, mean +3.11.
- Under a fixed Gemini executor only Opus improves on held-out tasks. The other
  three lineages regress, GPT-5.5 by 10.32 points.
- Of 64 official version switches, only two show gains clearly beyond the
  repeated-run noise band of roughly +/-4.75 points. Eight regress on both
  benchmarks.
- Feedback and held-out scores move in the same direction only 53.1% of the time.
  Only 2 of 9 declared final versions are held-out optimal. Visible feedback works
  for local search but is unreliable for final selection.
- Failure diagnosis is the weakest step. The trajectory inspection interface was
  called twice across all lineages. Creators rely on custom scripts and small
  probes, which can disagree with the full evaluation.
- The one clean positive example: Opus found that 99 of 100 runs reported success
  while only 48 passed, traced this to premature completion, and added a
  completion gate.

## 8. The underlying thesis

The conclusion states it directly: "If model weights are one place intelligence
accumulates, the harness is another: explicit, inspectable, testable, reusable,
and continually improvable through failure, feedback, and real engineering
pressure." The goal of the benchmark is to make that second place measurable.
The paper is careful to say it measures model-external learning and does not
claim heuristic learning replaces parameter training.

## 9. Stated limitations, and what they mean for reading the results

- Human references are uneven and not guaranteed optimal. Exceeding one means
  exceeding that external system, not human ability.
- Unified-Eval reduces but cannot remove executor effects.
- Evolution has one trajectory per creator-runtime cell, so no uncertainty
  estimates or population comparisons.
- Held-out evaluation in Evolution covers SWE-Pro only.
- The development environment `D` is fixed. Whether an evolved harness can serve
  as its own development environment for further evolution is left open. This is
  the recursive self-improvement question the title hints at, and the paper
  explicitly does not answer it.

## 10. Practical takeaways for harness engineering

These are the lessons the paper's evidence supports, independent of the
benchmark itself.

1. Treat the harness as a first-class engineering artifact with its own
   evaluation, not as configuration.
2. Separate the model that develops from the model that executes when judging a
   change. A change that helps one executor can break another.
3. Never let executor-specific constants (step caps, output limits, stopping
   heuristics) into the harness without making them configuration.
4. Add a verification gate before completion. Self-reported success is the most
   common lie in the data.
5. Measure both success and token cost. Cost is a design outcome, not noise.
6. Prefer small targeted edits driven by reading actual failure traces over large
   rewrites. Revision quality, not test volume or line count, predicts gains.
7. Expect evaluation noise of several points and do not select a final version on
   a single feedback run.
8. Audit for dead code. State and memory mechanisms are the most likely to be
   declared and never executed.
9. Keep an external ledger of versions, hypotheses, and outcomes. Context does not
   survive compaction; files and git history do.
