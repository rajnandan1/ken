# 2026-08-26: Iteration 1 verdict: KEEP. The countable rewrite trigger works.

Run `20260826-203814`: baseline vs **ken v1.1**, haiku, 3 repeats × 10 tickets,
**$3.38**. The ken arm loaded the working tree via `KEN_PLUGIN_DIR` (v1.1
phrases verified in the injected ruleset pre-run). Both arms faced the same
sharpened tickets (r9 reworded), so arm differences attribute to the ruleset.

**v1.1 changes two rules from aspirations to procedures** (chosen from the
[evidence dossier](2026-08-26-maintenance-v1-sonnet.md), pre-registered
verdict rule: keep only if root-cause and/or rewrite improve without survival
regressing):

1. count the unit's fix-comment trail: ≥3 prior fixes → rewrite, never entry four
2. list callers/callees before a bug edit; fix the shared helper
3. smallest-correct beats smallest

## Result

| median of 3 runs | survival (of 9) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
| ---------------- | --------------: | -----------: | ----------------: | --------------------: | -------: |
| baseline         |               8 |            4 |                 1 |                     0 |    $0.50 |
| **ken v1.1**     |               8 |            4 |                 1 |                 **2** |    $0.62 |

vs the v1.0.0 haiku round: ken rewrite **0/2 → 2/2 in all three runs** (6/6
rot cells, from 1/24 cells across all prior runs); ken survival 7/9 → 8/9.
Baseline, same tickets, same day: 0/2 rewrites in all three runs. The arm
difference isolates the trigger from the ticket wording.

**The pre-registered rule yields KEEP v1.1.** Rewrite rose from 0/2 to 2/2,
survival rose from 7/9 to 8/9, and no measured rate regressed. Version 1.1.0 ships.

## Iteration 2 targets

- **Root-cause stayed at 1/2.** Ken guarded `transfer` (the named symptom)
  3/3 despite the new caller-enumeration line; baseline also went 0/3 this
  round (its earlier 2/3 looks like n=3 variance). The enumeration rule as
  worded did not change agent behavior. Candidate: make it a required first action ("your
  first edit must name the callers you checked"), or accept single-session
  haiku may reject each wording. Measure the candidate.
- **r9 passes 24/24** (both arms 4/4 after the sharpened prompt). It
  measures prompt-following only and gives both arms the same score.
  Candidate: retire it to reported status in v2 of the ticket set.
- Rewrites raised median cost per run from $0.50 to $0.62. The score does not
  judge cost.

Raw data: `benchmarks/maintenance/runs/20260826-203814/` (the harness persisted
per-round session records).
