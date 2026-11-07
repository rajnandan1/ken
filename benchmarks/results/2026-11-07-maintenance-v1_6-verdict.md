# 2026-11-07: Iteration 6 verdict: PENDING. Interface probe (r13) and one candidate clause.

The verdict rule below was committed before any data (see git history of this
file). No live session has played round 13 yet.

## What changed

A post by Chris (`@_khrus`) reports that the prompt "deepen modules and simplify
interfaces" gives his best results: a deep module has a small interface that
hides a lot of behavior. The idea is Ousterhout's, from _A Philosophy of Software
Design_. The post carries no numbers. Five ideas from the post, its replies, and
Matt Pocock's linked `DEEPENING.md` looked worth adding.

1. **Instrument (kept regardless of verdict, unless Stage 1 finds the ticket
   does not tempt):** round 13, `r13-line-discount`, a new scored rate named
   `interface`. Before this round, no probe covered `Interfaces few and small`
   or `No layer that only translates`.
2. **Ruleset candidate (v1.6):** one clause, below.

## What the kept workspaces show

Before any spend, the five shapes were scanned in the 102 workspaces kept in
`benchmarks/maintenance/runs/`: 36 multi-round workspaces (18 baseline, 18 ken;
30 haiku, 6 sonnet) and 66 one-round workspaces from the speculative-placement
runs. The scanner found every shape planted in a fixture.

| Clause | Shape scanned | Scanned | Found |
| ------ | ------------- | ------: | ----: |
| 1. Callers know less | `reports.py` reads `["items"]` and calls `parse_amount` itself | 36 | **36** |
| 2. Deletion test | a function that only forwards its own parameters | 102 | 0 |
| 3. Drop parameters | a parameter never read, or the same literal at every source call | 102 | 0 |
| 4. One adapter is hypothetical | any class, so any interface with one implementation | 36 | 0 |
| 5. Check at the interface | an agent test that touches a private name, in 4 agent test files | 36 | 0 |

The scan returned two other hits, and neither counts. Round 10 requires
`tax_due`'s optional rate, and `textutils.truncate` matched a file object's
`f.truncate()` by name.

Clause 1 has a target on every multi-round workspace, and the logic already
exists twice: `reports.py` computes a line total, and `invoice_total` computes
it again. Clauses 2 to 5 have no target in this benchmark. Zero here says
`ledgerd` cannot measure them. It does not say agents never write these shapes.
An always-loaded clause with no measured target costs tokens on every turn, so
clauses 2 to 5 stay out of this candidate.

## The five clauses

| # | Wording | Would extend | Status |
| - | ------- | ------------ | ------ |
| 1 | Count what callers must know: order, flags, data layout, derived values. When a change would edit the same logic in two places, move it into the one unit that owns it and have both call it. | `Interfaces few and small` | **Candidate v1.6** |
| 2 | Test: if deleting it pushes no complexity back onto its callers, it goes. | `No layer that only translates` | Held, no target |
| 3 | Drop a parameter the unit can work out itself, that every caller passes the same way, or that nobody reads. | `Interfaces few and small` | Held, no target |
| 4 | Add an interface when two implementations need it today. A test double counts as the second. | `No layer that only translates` | Held, no target |
| 5 | The check calls the unit's interface, so it survives a rewrite. | The runnable-check rule | Held, no target |

Clauses 2 to 4 fit `/ken-review`, which loads on demand and reviews code no
agent wrote this session. That is a separate change. None of the five is
Thompson's: a KEEP adds a `PROVENANCE.md` note saying so and naming Ousterhout
and `DEEPENING.md`.

## The probe

`r13-line-discount` asks for a per-line percentage discount that invoice totals
and the invoice report both use, with the report's format unchanged. The prompt
never says where the rule lives, so the temptation comes from the code the
agent reads. The shortest fix adds a fourth tuple field and teaches `reports.py`
the discount. A deep fix keeps the rule in `invoices.py`, and `reports.py` asks
for finished lines.

`probe_pass` = visible test passes **and** hidden test passes **and**
`discount_leaks` is empty. The hidden test rounds each line on its own, so a
report and a total that disagree fail it. `discount_leaks` flags source outside
`invoices.py` with a discount variable or parameter, a discount string key,
index 3, or a named fourth tuple target. Calls into `invoices.py` stay clean.

Checked without spend: the selftest passes (good ref interface 1/1, bad ref 0/1
by the leak alone, with its hidden test passing). `discount_leaks` returned 0
false hits on all 102 workspaces. Each branch passed a throwaway case.

## Pre-registered verdict rule

**Stage 1: round 13 alone.** Haiku, 10 sessions per arm, each on a fresh copy of
one of `runs/20260828-170553/baseline__r{0,1,2}`, cycled. The arms are baseline,
shipped ken, and ken v1.6-candidate. All three start from the same code, so only
the ruleset differs. The candidate sentence is verified verbatim in the injected
ruleset first.

- Baseline passes 8 or more of 10: **STOP**. The ticket does not tempt. Rewrite
  the ticket, and run nothing else.
- Shipped ken passes 8 or more of 10: **STOP**. Ken already does this. Clause 1
  is a no-op and stays out.
- The candidate does not beat shipped ken at one-sided Fisher p < 0.05:
  **REVERT** clause 1. Keep the probe.
- Otherwise, go to Stage 2.

**Stage 2: regression guard.** Baseline vs ken v1.6-candidate, haiku, 3 repeats
× 13 tickets, `KEN_PLUGIN_DIR` at the working tree. It exists because the v1.5
clause saved every rewrite it touched and still cost two rewrites.

- **KEEP** iff ken passes interface in at least 2 of 3 runs and its medians reach
  survival ≥ 8/10, reuse 4/4, root-cause 1/2, rewrite 2/2, and trusted-base 1/1.
  These are ken's `20260830-212707` medians, the last run on shipped wording.
- Any other outcome: **REVERT** clause 1. Keep the probe.

Reported regardless of verdict: each session's `leaks` list, the irreversible
rate (no measured median exists yet), and the clone-density curve.

## Result

Not run.
