# 2026-11-07: Iteration 7 verdict: PENDING. A diff-check clause and a deepening pass, on round 13.

The verdict rule below was committed before any data (see git history of this
file). Neither test has run yet.

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

Not run.
