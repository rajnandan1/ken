# 2026-08-26 — Maintenance-over-time v1, sonnet round: the null replicates

Same configuration as the [haiku round](2026-08-26-maintenance-v1-haiku.md),
model claude-sonnet-4-6: baseline vs ken, 3 repeats × 10 tickets, 60 sessions,
**$6.07**. Run `20260826-195226`. This round records cache tokens per round
(~100k/round median on both arms), so arm activation is auditable in-data.

## Result

| median of 3 runs | survival (of 9) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
|---|--:|--:|--:|--:|--:|
| baseline | **8** | 3 | **2** | 0 | $1.00 |
| ken | 7 | 3 | 1 | 0 | $1.04 |

The stronger model did not rescue the ruleset: the haiku null replicates
almost line for line.

- **r6 root-cause: ken 0/3 again (0/6 across both models; baseline 3/6).**
  Inspected diff from a kept workspace: ken's fix is two lines guarding
  `transfer` — the ticket's named symptom — with the shared `_debit` untouched,
  so the hidden `withdraw` test fails. The consistency across models suggests
  a ruleset interaction, not model depth: ken's minimality pressure (brute
  force, smallest change) may be steering toward the local guard and beating
  its own "debug the model, not the symptom" rule. Testable by iteration.
- **Rewrite-on-rot: 1 rewrite in 24 rot cells across both rounds** — and the
  one rewrite came from a ken arm (sonnet run #0, r8). The rewrite rule is
  otherwise inert in single-shot sessions even when the ticket names the
  three-patch trail.
- **r9 accent-insensitive search: 6/6 failed again** (12/12 across models).
  Every session hand-rolls `.lower()` matching. Worth an honesty review of the
  probe itself: the expectation ("the way users expect search to work across
  the app") may be too implicit to attribute the failure to method.

## Standing conclusion after two models

On this seed, injecting ken v1.0.0's ruleset does not change maintenance
method — and on the root-cause probe the direction is against ken, twice.
The next measured step is ruleset iteration: make the rewrite and root-cause
rules operational, re-run, keep what moves these numbers. Every iteration
lands here, whatever it shows.

Raw data: `benchmarks/maintenance/runs/20260826-195226/` (workspaces kept).
