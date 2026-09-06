# Evolution ledger (full, controller view)

Held-out columns are never shown to the creator. A candidate 'improves' only when its feedback gain exceeds the H0 noise band.

| version | commit | round | feedback mean | Δ vs H0 | noise band | fb fail-rate | held-out mean | Δ vs H0 | ho fail-rate | diff (+/-) | verdict | hypothesis |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H0 | 68f903e4 | 0 | 0.9167 | 0.0 | 0.1909 | 0.0833 | 0.875 | 0.0 | 0.125 |  | baseline | baseline from Creation |
| H1 | 158b5158 | 1 | 1.0 | 0.0833 | 0.1909 | 0.0 | 0.9931 | 0.1181 | 0.0 | 17 files changed, 159 insertions(+), 15 deletions(-) | within noise band | The single change with the most held-out upside is a **JSON repair layer in `parse_action`**: structurally repair a reply that is unambiguously an action object |
| H2 | e38a4ff4 | 2 | 1.0 | 0.0833 | 0.1909 | 0.0 | 1.0 | 0.125 | 0.0 | 20 files changed, 137 insertions(+), 16 deletions(-) | within noise band | The single change with the most held-out upside is to make the harness **enforce the provenance contract the scorer enforces, and preserve it on every exit path |

## Round notes

### H1 (round 1, commit 158b5158)

- creator: {'duration_s': 404.5, 'cost_usd': 2.5431245, 'turns': 42, 'is_error': False, 'summary': 'Done. Summary:\n\n**Diagnosis.** Every one of the four failed feedback runs died the same way, and it wasn\'t a statistics error at all. The executor emits action JSON with exactly one closing brace too few whenever `args` contains a long string. I replayed all 20 logged `model_reply` records through the old `parse_action` with a string-aware brace scan: **16 of 16** failing replies had `unclosed_depth == 1`, `ends_inside_string == False` — complete, correct payloads (plan checklists, full pandas pipelines with `save_as="analysis.py"`) discarded for one missing character. Three in a row tripped `max_parse_failures` and the run ended with no claims and no `analysis.py`. Short replies parsed fine; only the long turns carrying the analysis broke. 4/48 runs = the exact 8.3% gap to 0.9167.\n\nCompounding it: the parse-error observation was a constant string, so the model re-emitted byte-identical replies (`fb_003_correlation_r2` steps 4 and 5) until the budget tripped.\n\n**Change.** A repair layer in `harness/lifecycle.py` — a single string-aware scanner backing `_objects` (step over stray objects/prose instead of the naive first-`{`-to-last-`}` slice) and `repair_json` (close an unterminated string, trim a dangling `,` or `"key":`, append the closers the open stack implies; never invent keys or values). `parse_action` tries strict first, then repair, and tags the action `_repaired`. `_diagnose` replaces the constant error text with the concrete defect. `harness/execution.py` logs a `parse_repair` event and warns the model in-line that repair can truncate arguments, so the audit trail never claims a clean parse it didn\'t get.\n\n**Verification.** Offline replay: 20/20 replies now parse (16 repaired), every recovered `code` argument compiles, `save_as` preserved. Negative tests confirm repair doesn\'t manufacture actions from prose, empty replies, or objects with no `tool`. `run_dev.py`: 1.0 on all three dev tasks, all gates passed, no step-count regression — and `dev_001_logistic` hit the bug live, with a `parse_repair` at step 1 that under the old parser would have been the first of the three fatal parse errors.\n\n**Expectation.** Feedback score should move from 0.9167 toward 1.0, with a similar ~8% recovery on held-out runs. Risk is bounded: repaired submissions still face `verify_submission`, which re-runs `analysis.py` and compares its output to the claims.'}
- diagnosis check: cites ['fb_003_correlation', 'fb_004_logistic', 'fb_013_paired', 'fb_016_multi']
- audit: clean
- smoke (dev): {'mean_score': 1.0, 'timeouts': 0}
- feedback per task: {"fb_001_ttest": 1.0, "fb_002_ols": 1.0, "fb_003_correlation": 1.0, "fb_004_logistic": 1.0, "fb_005_anova": 1.0, "fb_006_chisq": 1.0, "fb_007_paired": 1.0, "fb_008_cox": 1.0, "fb_009_mh_stratified": 1.0, "fb_010_multi_bh": 1.0, "fb_011_ols_interaction": 1.0, "fb_012_mannwhitney": 1.0, "fb_013_paired": 1.0, "fb_015_mh_stratified": 1.0, "fb_014_cox": 1.0, "fb_016_multi_bh": 1.0}
- held-out per task: {"ho_001_ttest": 1.0, "ho_002_ols": 1.0, "ho_003_correlation": 1.0, "ho_004_logistic": 1.0, "ho_005_anova": 1.0, "ho_006_chisq": 1.0, "ho_007_multi_bh": 1.0, "ho_008_mannwhitney": 1.0, "ho_009_cox": 1.0, "ho_010_ols_interaction": 1.0, "ho_011_paired": 1.0, "ho_012_mh_stratified": 0.8889, "ho_013_multi_bh": 1.0, "ho_014_mannwhitney": 1.0, "ho_016_ols_interaction": 1.0, "ho_015_cox": 1.0}

Changelog:

# Changelog — round 1

## Hypothesis

All four failed runs in the feedback packet (`fb_003_correlation` r2, `fb_004_logistic` r2,
`fb_013_paired` r2, `fb_016_multi_bh` r1 — 4 of 48 runs, exactly the 8.3% gap to the 0.9167 mean)
died from a single syntactic defect: the executor emits action JSON with one closing brace too few
whenever the reply nests a long string inside `args`. Replaying every logged `model_reply` through
the old `parse_action` and scanning brace depth outside of strings showed **16 of 16** failing
replies with `unclosed_depth == 1` and `ends_inside_string == False` — complete, correct payloads
(plan checklists, full pandas pipelines with `save_as="analysis.py"`) thrown away for one missing
character. Three in a row tripped `max_parse_failures` and the run ended with no `claims.json` and
no `analysis.py`.

Hypothesis: a structural repair layer at the single point every reply passes through removes this
whole class of run-ending error, converting those four zeros to the 1.0 the same tasks scored on
their other repeats, and will do the same on held-out tasks — the defect is a property of how the
executor decodes long nested JSON, not of any task, and it fires precisely on the
`run_python`/`submit` turns that carry the analysis.

## What changed

**`harness/lifecycle.py`** — action parsing gained a repair layer:

- `_scan(text, start)`: one string-aware walk reporting the open-delimiter stack, whether the text
  ends inside a string or on a dangling escape, and where the first top-level value closed.
- `_objects(text)`: every complete top-level `{...}` object in order plus a trailing incomplete
  one, so a stray object or prose around the action is stepped over rather than swallowed by the
  old naive first-`{`-to-last-`}` slice.
- `repair_json(text)`: closes an unterminated string, trims a dangling `,` or `"key":`, and appends
  the closers implied by the open stack. It only ever appends delimiters or trims an incomplete
  trailing token — it never invents keys or values.
- `parse_action`: per candidate, strict parse → then repaired parse. Returns the action annotated
  with `_repaired` (a human-readable description) when repair was used, so the caller can log it.
- `_as_action`: shared normalisation of both the nested and the flat reply shape; coerces a
  non-object `args` to `{}` instead of passing it to `Tools.call`.
- `_diagnose(text)`: replaces the constant `ParseError` sentence with the concrete defect
  (N unclosed delimiters and whic

### H2 (round 2, commit e38a4ff4)

- creator: {'duration_s': 523.7, 'cost_usd': 3.0785495, 'turns': 50, 'is_error': False, 'summary': "Done. Round 2 complete.\n\n## What I found\n\nThe feedback set is saturated (mean 1.0, provenance 1.0) and `feedback/runs/` is empty — no failed runs to read. So the diagnosis came from the ledger arithmetic plus the scored contract in `score.py`, backed by trajectories I generated with `run_dev.py`.\n\nThe ledger tells the real story: H0's four 0.67 tasks (`fb_003`, `fb_004`, `fb_013`, `fb_016`) have 5/7/9/8 claim slots, so 0.67 isn't a per-claim fraction — it's one repeat out of three scoring **0.0**, matching the 0.0833 run fail-rate exactly. This harness loses score in whole runs. H1 closed one of the two ways `score.py` zeroes a run (submit nothing). The other was still wide open:\n\n- **The gate was weaker than the scorer.** `verify.py` ran `analysis.py` in the *live* workdir, which by then holds everything `write_file` and `run_python(save_as=…)` created. `score.py` re-runs it in a pristine copy of the task dir. A script reading a cleaned CSV passed the gate and scored 0.\n- **Every non-passing exit shipped knowingly-inconsistent artefacts.** `finalize` wrote `state.best_claims` — the claims the gate had just *rejected* — next to a script printing different numbers. Guaranteed provenance failure, guaranteed 0, even when the numbers were mostly right.\n\n## What I changed\n\nOne mechanism, threaded through: a `reproduce()` sandbox in `verify.py` that mirrors the scorer's isolation exactly. `execution.py` snapshots the task directory before any tool can write; the gate now reproduces there and rejects in-workdir dependencies with an actionable message. `finalize` gained `_reconcile`: when the gate never passed, it walks candidate scripts (submitted first, then the scratch scripts that printed numeric JSON — newly tracked in `state.claim_scripts`), keeps the first that reproduces, ships it as `analysis.py`, and writes `claims.json` from *its* output restricted to the task slots. Slots the script doesn't print are omitted, since one non-reproduced claim zeroes the whole run. Two sentences in the prompt and tool spec make the rule discoverable.\n\n`status` still derives solely from whether the gate passed — reconciliation never asserts success.\n\n## Verification\n\n`run_dev.py`: 1.0 / 1.0 / 1.0 before and after, provenance ok, **zero** new gate rejections, same step counts. The dev tasks are too easy to exercise the recovery paths, so I checked those directly against `score.py`'s real scorer: the dependent script is now rejected (was passing); a self-contained one still passes; a budget-exhausted run promotes its scratch script and scores 1.0 `partial` where it previously had no `analysis.py` at all; a gate-exhausted run with contradictory claims (`m=99.0` vs script's `2.0`) is realigned and scores 1.0 where it previously scored 0; and with nothing reproducible the old fallback is untouched.\n\nI expect no movement on the feedback set — it's already at ceiling. The gain, if any, is held-out: a class of silent zeros removed, and exhausted runs converted from 0 to p"}
- diagnosis check: cites ['fb_003_correlation', 'fb_004_logistic', 'fb_013_paired', 'fb_016_multi']
- audit: clean
- smoke (dev): {'mean_score': 1.0, 'timeouts': 0}
- feedback per task: {"fb_001_ttest": 1.0, "fb_002_ols": 1.0, "fb_003_correlation": 1.0, "fb_004_logistic": 1.0, "fb_005_anova": 1.0, "fb_006_chisq": 1.0, "fb_007_paired": 1.0, "fb_008_cox": 1.0, "fb_009_mh_stratified": 1.0, "fb_010_multi_bh": 1.0, "fb_011_ols_interaction": 1.0, "fb_012_mannwhitney": 1.0, "fb_013_paired": 1.0, "fb_014_cox": 1.0, "fb_015_mh_stratified": 1.0, "fb_016_multi_bh": 1.0}
- held-out per task: {"ho_001_ttest": 1.0, "ho_002_ols": 1.0, "ho_003_correlation": 1.0, "ho_004_logistic": 1.0, "ho_005_anova": 1.0, "ho_006_chisq": 1.0, "ho_007_multi_bh": 1.0, "ho_008_mannwhitney": 1.0, "ho_009_cox": 1.0, "ho_010_ols_interaction": 1.0, "ho_011_paired": 1.0, "ho_013_multi_bh": 1.0, "ho_012_mh_stratified": 1.0, "ho_014_mannwhitney": 1.0, "ho_016_ols_interaction": 1.0, "ho_015_cox": 1.0}

Changelog:

# Changelog — round 2

## Hypothesis

This harness loses score in units of *whole runs*, not per-claim drift: the H0→H1 ledger's four 0.67
tasks (`fb_003_correlation`, `fb_004_logistic`, `fb_013_paired`, `fb_016_multi_bh`) each had one
repeat scoring 0.0, matching the 0.0833 run fail-rate. `score.py:112-134` offers exactly two ways to
zero a run: submit nothing, or submit claims that `analysis.py` — re-run in a **clean copy of the task
directory** — does not reproduce. H1 closed the first. This round closes the second: make the harness
enforce and preserve the provenance contract the scorer enforces, on every exit path.

## What changed

**V — `harness/verify.py`**
- New `reproduce(code, workdir, baseline_files, cfg)`: copies only the files the task shipped with
  into a temp dir, writes the script as `analysis.py`, runs it there, returns `(printed_json, log)`.
  This is the same isolation `score.py:70-75` uses.
- `verify_submission` takes `baseline_files` and reproduces via that sandbox instead of
  `run_command(..., cwd=workdir)`. The live workdir contains everything `write_file` and
  `run_python(save_as=...)` created during the run, so the old check could pass a script that the
  scorer would fail. Rejection text now names the isolation, so an executor that read an intermediate
  file gets an actionable message and can still fix it inside its budget.

**E — `harness/execution.py`**
- Snapshots `baseline_files = list_tree(workdir)` once, before any tool can write (excluding the
  output directory when it sits inside the workdir), and threads it into `verify_submission` and
  `finalize`.

**L — `harness/lifecycle.py`**
- `finalize` gained `_reconcile`: when the gate never passed (gate exhaustion, step/time budget, LLM
  failure), it walks candidate scripts — the submitted one first, then the saved `scratch_NN.py`
  scripts that printed numeric JSON, newest first — keeps the first that reproduces in the clean
  sandbox, writes it as `analysis.py`, and writes `claims.json` from *its* printed values restricted
  to the task's slots. Previously these exits shipped `state.best_claims`, i.e. the claims the gate
  had just **rejected**, next to a script printing different numbers — a guaranteed provenance failure
  and therefore a guaranteed 0. Slots the script does not print are now omitted rather than
  submitted, because under `score.py:120-127` one non-reproduced claim zeroes the whole run.
  If no candidate reproduces, the old best-effort behaviour is unch

