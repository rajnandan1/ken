# 2026-11-07: Iteration 7 verdict: REVERT both. The diff-check clause passed 0 of 10, the deepening pass 2 of 10.

The verdict rule below was committed in `c33465f`, before either test ran.

## What changed

Iteration 6 found a real gap. On round 13, shipped ken and baseline both wrote
the discount rule in two places in 10 of 10 sessions, and the v1.6 clause changed
nothing ([note](2026-11-07-maintenance-v1_6-verdict.md)). That clause asked the
agent to notice the duplication before it wrote the code. Ken's rewrite rule
works from evidence the agent can see in the file, so this round tries two forms
that act on finished code.

## Test 1: a clause in `Know every line`

One sentence goes after "as Thompson walked his day's code each night.":

> If your diff writes the same logic twice, move it into one unit before you
> finish.

**Setup:** the same as iteration 6's Stage 1. Haiku, 10 sessions, round 13 alone,
each on a fresh copy of `runs/20260828-170553/baseline__r{0,1,2}`, cycled, with
the same `interface` scorer. The control is iteration 6's shipped ken arm, which
passed 0 of 10. The candidate sentence is verified verbatim in a live session
first.

## Test 2: a deepening pass

**Setup:** one second session on a fresh copy of each of the 10 finished
`runs/20261107-stage1/ken-shipped__s{0..9}` workspaces, all of which leaked.
Haiku, shipped ken loaded. The whole ticket prompt is:

> Deepen modules and simplify interfaces in `invoices.py` and `reports.py`.

Those are the two source files round 13 changed, which is the scope of a pass
over a pull request. A session passes when `interface` passes **and** the number
of rounds 1..10 that survive does not drop below the count before the pass.

## Pre-registered verdict rule

Each test stands alone. The bar is one-sided Fisher p < 0.05 against 0 of 10,
which means **at least 4 of 10** sessions pass.

- **Test 1 reaches the bar:** the clause goes to the iteration 6 Stage 2 guard
  (baseline vs candidate, haiku, 3 repeats × 13 tickets, same KEEP medians). It
  does not ship before that guard passes. Stage 2 is a separate spend.
- **Test 1 misses the bar:** **REVERT** the clause.
- **Test 2 reaches the bar:** the pass works on finished code. Adding it to
  `/ken-review` is a separate change, because `/ken-review` loads on demand and
  adds no always-on rule.
- **Test 2 misses the bar:** **REVERT** the idea.
- **Both miss the bar:** stop. Wording does not close this gap on haiku, and the
  probe stays as the record of it.

Reported regardless of verdict: each session's `leaks` list, whether the formula
stayed out of `reports.py`, and for Test 2 the surviving rounds before and after.
The formula count does not decide anything.

## Result

Run `20261107-iter7`: claude-haiku-4-5-20251001, 10 sessions per test, **$2.73**
including $0.02 for two canary sessions.

| Test | passed | leaked | round 13 tests passed | cost |
| ---- | -----: | -----: | --------------------: | ---: |
| Control, shipped ken (iteration 6) | 0 of 10 | 10 | 10 of 10 | $1.14 |
| Test 1, diff-check clause | 0 of 10 | 10 | 10 of 10 | $1.26 |
| Test 2, deepening pass | 2 of 10 | 8 | 10 of 10 | $1.45 |

**Pre-registered rule:** neither test reached 4 of 10. Test 2 against the control
is one-sided Fisher p = 0.24. **VERDICT: REVERT both. Stop. Wording does not close
this gap on haiku, and the probe stays. The shipped ruleset does not change.**

## What the sessions did

A live session quoted the Test 1 clause word for word before the test ran. All
10 sessions still leaked.

The location of the formula was reported, and it does not decide anything:

| Arm | Formula only in `invoices.py` |
| --- | ----------------------------: |
| Shipped ken, before any pass | 1 of 10 |
| Test 1, diff-check clause | 3 of 10 |
| Test 2, same workspaces after the pass | **8 of 10** |

The pass did remove the duplicated formula in most sessions. The `interface`
rate stayed low because `reports.py` still named `discount` in 6 of those 8
sessions. Two sessions went further, and `reports.py` asks `invoices.py` for
finished lines. These are the first passes in 50 sessions.

The pass also did damage. Two of the 10 sessions deleted working functions, and
the round 13 tests did not notice:

- `deepen__s5` deleted `export_filename` and `filter_invoices`, which lost rounds
  3 and 9.
- `deepen__s7` deleted `statement`, which lost round 5. It also wrote an
  `ARCHITECTURE.md` that nobody asked for.

Across the 10 sessions, source grew by 100 lines net (+338, -238), and every
session added a test file. The post reports reduced line counts, and this run did
not reproduce that.

## If someone retries

The pass removed the duplicate at a cost of two broken sessions. These sessions
could not run tests, because the harness disables Bash. A real pass can run them.
The next candidate scores the formula's location instead of `interface`, allows
Bash, and pre-registers both. Not run; features default to no.

Raw data: `benchmarks/maintenance/runs/20261107-iter7/` (workspaces kept).
