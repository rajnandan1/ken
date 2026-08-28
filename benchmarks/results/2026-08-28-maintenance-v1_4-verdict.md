# 2026-08-28: Iteration 4 verdict: REVERT wording, keep the probe

Run `20260828-170553`: baseline vs ken v1.4-candidate, haiku, 3 repeats ×
10 tickets, **$3.40**. The verdict rule below was pre-registered before any
data.

## What changed

A field report showed an agent under ken re-declaring a sibling module's
operator sets; review caught it. The benchmark could not see this class:
its three reuse probes pass 3/3 on **both** arms (saturated). Two changes:

1. **Instrument (kept regardless of verdict):** the retired r9-search ticket
   is replaced by r9-filter-invoices. The seed gains `filtering.py` — shared
   operator tables used by the CLI, with two reinvention divergences: quirky
   op names (`ne`, `exact`) and case-insensitive text matching. The hidden
   probe passes only through the tables (or an exact behavioral clone).
   Selftest: good ref 4/4 reuse, adversarial lazy twin passes every visible
   test and scores 0/4. Reuse is scored /4 from this version.
2. **Ruleset candidate (v1.4):** loop step 2 gains a first-action form —
   "Before writing a new function, constant table, or format, search this
   codebase for it; the concept usually already lives a few files over —
   import it and name the file you took it from." Same treatment that fixed
   the rewrite rule (v1.1); the field report singled out the question-form
   as the actionable shape.

## Pre-registered verdict rule

Config: baseline vs ken v1.4-candidate, haiku, 3 repeats × 10 tickets,
`KEN_PLUGIN_DIR` pointing at the working tree.

- **KEEP** the wording iff ken's reuse median reaches **4/4** with survival
  median ≥ 8/9 and rewrite median 2/2, **and** baseline's reuse median stays
  below 4/4. r9 is the targeted cell.
- If **both** arms reach 4/4 at median, the new probe failed to discriminate
  on live models: wording unproven → **REVERT** wording, keep the probe.
- Any other outcome → **REVERT** wording, keep the probe.

## Result

| median of 3 runs | survival (of 9) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
| ---------------- | --------------: | -----------: | ----------------: | --------------------: | -------: |
| baseline         |               8 |        **4** |                 1 |                     0 |    $0.55 |
| ken v1.4         |               8 |        **4** |                 1 |                     1 |    $0.59 |

**The r9 probe passed 6/6 across both arms. Pre-registered rule: both arms
at 4/4 median means the probe failed to discriminate on live models, so the
wording is unproven. VERDICT: REVERT the wording; the probe and the /4
scoring stay. The shipped ruleset remains the v1.1 wording plus the
(unmeasured) scope-precedence clause.**

## What the saturation means

The probe discriminates against genuine laziness — the scripted lazy twin
passes every visible test and scores 0/4 — but live haiku follows the
ticket's pointer ("exactly the operators the app's filters already
support") to `filtering.py` in both arms, so the cell measures
prompt-following again, not method. The field miss this probe was built
from had **no** such pointer: nothing in that ticket named the sibling
module. Weakening the pointer to match reproduces the r9-search disease
(failure too implicit to attribute to method — why r9-search was retired).
After two designs from opposite directions, the discriminating window for a
single-shot reuse probe between "too implicit to attribute" and "explicit
enough that everyone follows it" looks narrow to nonexistent. This is the
root-cause finding again from the reuse side: behavior tracks what the
edit-site evidence makes visible, not the injected method rules.

Secondary observations, not verdict criteria: ken's rewrite median dipped
to 1/2 this round (1, 1, 2 across runs — haiku variance; the KEEP rule
would have failed on this clause too), and one baseline run posted 9/9
survival with root-cause 2/2, the usual baseline noise.

Raw data: `benchmarks/maintenance/runs/20260828-170553/` (workspaces kept).
