# 2026-08-30: Iteration 5, v1.5 candidate: a rewrite keeps what the old unit accepted

Pre-registered before any data. Result appended below once the round lands.

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
