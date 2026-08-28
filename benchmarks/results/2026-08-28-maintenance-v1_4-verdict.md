# 2026-08-28: Iteration 4: subtle-reuse probe + steal-rule wording

RUN IN PROGRESS — this header pre-registers the verdict rule before any data.

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

(pending)
