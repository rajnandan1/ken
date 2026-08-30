# 2026-08-30: Iteration 5 verdict: REVERT. The clause saved every rewrite it touched and cost two rewrites.

The verdict rule below was committed before any data (see git history of this file).

## What the trusted-base round showed

Run `20260830-212707` ([results](2026-08-30-maintenance-v1_5-trusted-base.md)):
ken rewrite 2/2 at median, survival 8/10 against baseline's 9/10. Two of six
ken rot rewrites passed the round's visible tests and lost a hidden case.
Read from the kept workspaces, neither loss was a fix-comment case:

- **r8, run #1:** the `import_rows` rewrite filters junk with
  `len(line) != 2`. The old unit read `line[0], line[1]` and tolerated extra
  columns. The rewrite **narrowed** what the unit accepted; nothing in the
  ticket asked for that.
- **r4, run #0:** the `parse_duration` rewrite tries `float(s)` on the whole
  string first, then falls back to the unit loop, which never flushes a
  trailing bare number. `"10m30"` returns 600. That case is the ticket's new
  semantics (bare number = seconds) applied in combination with a unit; the
  old code got it wrong too, and no comment or visible test named it. Only
  running the check catches it, and the harness disables Bash.

Baseline's patch four kept every case in all six cells, because the code it
refused to delete was also the spec.

## Candidate (v1.5)

Loop step 6 gains one sentence, after "never add entry four":

> The old unit is the spec for everything the ticket leaves alone: a rewrite
> keeps every input it accepted (narrowing needs the ticket to ask), and those
> inputs become asserts in the unit's check before the old code goes.

Same treatment as v1.1: an aspiration ("never rewrite what you don't yet
understand") restated as a procedure keyed to evidence at the edit site (the
old unit's own branches and reads). It targets the r8 class. The r4 class is
out of reach for wording and is not a target.

## Pre-registered verdict rule

Config: baseline vs ken v1.5-candidate, haiku, 3 repeats × 11 tickets,
`KEN_PLUGIN_DIR` at the working tree, the trusted-base probe in place.

- **KEEP** iff ken's survival median reaches **≥ 9/10** with rewrite median
  still **2/2** and no other rate below the `20260830-212707` medians (reuse
  4/4, root-cause 1/2, trusted-base 1/1).
- Any other outcome → **REVERT** the sentence. Reported regardless of verdict:
  the r8 hidden-test pass count on the ken arm (2/3 last round), since that
  cell is the one the clause targets.

## Result

Run `20260830-215651`: baseline vs ken v1.5-candidate, haiku, 3 repeats × 11
tickets, **$4.03**. The candidate sentence was verified verbatim in the
injected ruleset before the run.

| median of 3 runs | survival (of 10) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | trusted-base (of 1) | cost/run |
| ---------------- | ---------------: | -----------: | ----------------: | --------------------: | ------------------: | -------: |
| baseline         |                9 |            4 |                 1 |                     0 |                   1 |    $0.65 |
| ken v1.5         |                9 |            4 |                 1 |                 **1** |                   1 |    $0.71 |

**Pre-registered rule: KEEP needs survival ≥ 9/10 (met: 9, 9, 9) and rewrite
2/2 (not met: 1, 2, 1). VERDICT: REVERT the sentence. The shipped ruleset
stays at the v1.1 wording plus the scope-precedence clause.**

## What the targeted cell did

Where a rewrite happened, the clause worked. Ken rewrote four rot cells this
round and lost **0** hidden cases (2 of 6 last round). Every r8 rewrite filters
junk with `len(line) < 2`, none narrowed the importer; every r4 rewrite returns
630 for `"10m30"`, so the untargeted class held too. r8 hidden passed 3/3 on
the ken arm (2/3 last round). One ken run left `tests/test_csvio.py` and
`tests/test_parsing.py` behind, the asserts the clause asked for.

The cost: the rewrite trigger fired in 4 of 6 rot cells (5/6 last round, 6/6
in the v1.1 round). Ken #0 patched r8 and ken #2 patched r4, both keeping the
three-comment trail while their answers open with "rewrote:". The clause makes
a rewrite more work (enumerate inputs, write asserts) and haiku, which cannot
run anything here, may be taking the cheaper branch. Or it is haiku variance:
the v1.4 round posted 1, 1, 2 with no such clause. n=3 cannot tell them
apart, and the rule was written to require both numbers.

Survival: ken's one remaining loss in every run is r6, the root-cause miss
(0/6 again, both arms; baseline #2 posted 2/2 and 10/10, the usual baseline
noise). Reuse 4/4 and trusted-base 1/1 on both arms; r11 produced no
unvouched import in any of the six sessions this round.

## If someone retries

The narrowing half of the sentence ("a rewrite keeps every input it
accepted; narrowing needs the ticket to ask") is the part that maps to the
measured loss; the asserts half is the part that adds work. The next
candidate is the narrowing sentence alone. Not run; features default to no.

Raw data: `benchmarks/maintenance/runs/20260830-215651/` (workspaces kept).
