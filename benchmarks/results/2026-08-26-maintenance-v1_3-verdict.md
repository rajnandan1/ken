# 2026-08-26: Iteration 3 verdict: REVERT. Close the instruction avenue.

Run `20260826-211428`: baseline vs **ken v1.3-candidate**, haiku, 3 repeats ×
10 tickets, **$3.61**. The candidate tested the third and last cheap
instruction class for the root-cause rule: **tool-literal**, "grep the
codebase for the name of the function you are about to change and read every
caller that comes back." The countable rewrite trigger uses the same concreteness.

## Result

| median of 3 runs | survival (of 9) | reuse (of 3) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
| ---------------- | --------------: | -----------: | ----------------: | --------------------: | -------: |
| baseline         |               8 |            3 |                 1 |                     0 |    $0.54 |
| ken v1.3         |               8 |            3 |                 1 |                     2 |    $0.65 |

**Pre-registered rule: keep iff root-cause median reaches 2/2 with survival
≥ 8/9 and rewrite 2/2. r6 failed 3/3 again. VERDICT: REVERT. The shipped
ruleset remains v1.1.0, and the instruction avenue for this rule is
closed.**

## Result across iterations

Across three iterations, **nine of nine ken runs guarded the ticket-named
call site** with `_debit` untouched, under three distinct instruction forms:

| form | wording shape                                                            | r6 result |
| ---- | ------------------------------------------------------------------------ | --------: |
| v1.1 | abstract procedure, mid-rules ("list its callers and callees…")          |       0/3 |
| v1.2 | first-action imperative, in the loop ("never guard a single call site…") |       0/3 |
| v1.3 | tool-literal ("grep the codebase for the name… read every caller")       |       0/3 |

The same aspirational→procedural treatment fixed the rewrite rule
on its first try (0/2 → 2/2, holding across three rounds at median). Each of
the last two rounds had one missed rot cell.

**On haiku single-shot sessions, no tested injected instruction induces cross-file
caller exploration before an edit.** Rules fire when their evidence is
visible at the edit site; they do not create exploration that the session
did not attempt. Remaining options are structural (enforced
explore-before-edit machinery, multi-turn maintenance sessions) or
acceptance; per ken's own features-default-to-no, neither is built until
someone argues it in.

Raw data: `benchmarks/maintenance/runs/20260826-211428/`.

## Addendum (2026-08-28): field report, unmeasured

One field report from an interactive (multi-turn, tool-rich) session shows
the root-cause rule firing: the agent placed one validator in the shared
choke point instead of per-view patches, then swept the callers and found
two more broken ones, and credited the framing to ken's bug-fix rule. An
anecdote, not a number — but consistent with the limit above being specific
to single-shot sessions, not to the rule. The same report surfaced a real
miss the benchmark cannot see: the agent re-declared a sibling module's
operator sets instead of importing them, while the benchmark's reuse probes
pass 3/3 on both arms (saturated). That instrument gap is fixed in the next
benchmark version (subtle-reuse probe replacing the retired r9).
