# 2026-08-26 — Iteration 1 verdict: KEEP. The countable rewrite trigger works.

Run `20260826-203814`: baseline vs **ken v1.1**, haiku, 3 repeats × 10 tickets,
**$3.38**. The ken arm loaded the working tree via `KEN_PLUGIN_DIR` (v1.1
phrases verified in the injected ruleset pre-run). Both arms faced the same
sharpened tickets (r9 reworded), so arm differences attribute to the ruleset.

**v1.1 changed two rules from aspirations to procedures** (chosen from the
[evidence dossier](2026-08-26-maintenance-v1-sonnet.md), pre-registered
verdict rule: keep only if root-cause and/or rewrite improve without survival
regressing):

1. count the unit's fix-comment trail — ≥3 prior fixes → rewrite, never entry four
2. list callers/callees before a bug edit; fix the shared helper
3. smallest-correct beats smallest

## Result

| median of 3 runs | survival (of 9) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
|---|--:|--:|--:|--:|--:|
| baseline | 8 | 4 | 1 | 0 | $0.50 |
| **ken v1.1** | 8 | 4 | 1 | **2** | $0.62 |

vs the v1.0.0 haiku round: ken rewrite **0/2 → 2/2 in all three runs** (6/6
rot cells, from 1/24 cells across all prior runs); ken survival 7/9 → 8/9.
Baseline, same tickets, same day: still 0/2 rewrites in all three runs — the
trigger, not the ticket wording, made the difference.

**Verdict, applied as pre-registered: KEEP v1.1.** Rewrite improved massively,
survival improved, nothing regressed. Versions bumped to 1.1.0.

## What didn't move — iteration 2's targets

- **Root-cause is still stuck.** Ken guarded `transfer` (the named symptom)
  3/3 despite the new caller-enumeration line; baseline also went 0/3 this
  round (its earlier 2/3 looks like n=3 variance). The enumeration rule as
  worded does not fire. Candidate: make it a required first action ("your
  first edit must name the callers you checked"), or accept single-session
  haiku may not comply with any wording — measure, don't guess.
- **r9 now passes 24/24** (both arms 4/4 after the sharpened prompt) — it
  verifies prompt-following, not method, and no longer discriminates in
  either direction. Candidate: retire it to reported status in v2 of the
  ticket set.
- Rewrites cost slightly more per run ($0.62 vs $0.50) — the price of
  actually rewriting. Reported, not judged.

Raw data: `benchmarks/maintenance/runs/20260826-203814/` (per-round session
records now persisted).
