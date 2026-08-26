# 2026-08-26 — Iteration 2 verdict: REVERT. Wording can't reach root-cause.

Run `20260826-205653`: baseline vs **ken v1.2-candidate**, haiku, 3 repeats ×
10 tickets, **$3.42**. The candidate moved the root-cause rule to a
first-action, perceptual form — loop step 1 opened bug tickets with "find
every caller of the function you suspect," the debug rule led with "never
guard a single call site of a shared function" — the same
aspirational→procedural shape that took rewrite from 0/6 to 6/6 in
iteration 1. r9 was retired from scored reuse this round (0/24 then 24/24
across prior rounds — it verified prompt-following, not method), so reuse
is now /3.

## Result

| median of 3 runs | survival (of 9) | reuse (of 3) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
|---|--:|--:|--:|--:|--:|
| baseline | 8 | 3 | 1 | 0 | $0.52 |
| ken v1.2 | 8 | 3 | 1 | 2 | $0.62 |

**Pre-registered rule: keep iff root-cause improves with survival ≥ 8/9 and
rewrite = 2/2. Root-cause did not improve — r6 failed 3/3 again. VERDICT:
REVERT the v1.2 wording; keep the r9 retirement (a benchmark correction,
independent of the arm comparison).** The shipped ruleset remains v1.1.0.
Also noted: one ken run's rewrite wobbled to 1/2 (median held at 2/2) — the
v1.1 trigger is strong, not deterministic.

## The informative negative

Two different wordings — v1.1's mid-list procedure, v1.2's first-action
imperative — both failed to move r6, while the identical
aspirational→procedural treatment fixed rewrite on the first try. The
difference between the rules explains it: the rewrite trigger keys on
evidence **visible at the edit site** (the unit's own fix-comment trail);
the root-cause rule demands **cross-file exploration** (finding callers
elsewhere) that a single-shot session skimming toward the ticket-named site
never performs. This is a workflow-affordance limit, not a phrasing problem.
Wording iterations on this rule are exhausted — two measured failures — and
further candidates are structural (an enforced explore-before-edit step, or
multi-turn sessions) or acceptance: document that single-shot ken does not
reliably root-cause cross-file, and say so.

PROVENANCE and the ruleset carry the revert; every number above is in
`benchmarks/maintenance/runs/20260826-205653/` (per-round session records kept).
