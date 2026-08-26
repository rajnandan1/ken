---
name: ken-gain
description: >
    Show ken's measured impact as a compact scoreboard, from ken's own
    benchmark results in benchmarks/results/. One-shot display, not a
    persistent mode, and not a per-repo number. Trigger: /ken-gain,
    "ken gain", "what does ken save", "show ken impact", "ken scoreboard".
---

# Ken Gain

Display the scoreboard when invoked. One-shot: do NOT change mode, write flag
files, or persist anything.

## Source of truth

The only figures this card may show are medians from ken's own runs recorded
in `benchmarks/results/` of the ken repo. Render the recorded figures as plain
ASCII bars (bar length = measured range, label = exact figure).

If `benchmarks/results/` has no ken results yet, print:

```
  ken gain: no measured numbers yet.

  Nothing is claimed that wasn't measured. Run the harness in benchmarks/
  (see benchmarks/README.md; needs API keys in .env) to produce the first
  real entry.

  This repo, today:  /ken-debt  (the counted ceilings ledger)
                     /ken-audit (what's rewritable right now)
```

## Honesty boundary

Figures are benchmark medians, not this repo. NEVER print a per-repo savings
number ("you saved X lines/tokens here"): the unbuilt version was never
written, so there is no real baseline to subtract from in a live repo. The
only real per-repo figures come from `/ken-debt` (a counted ledger), and
this card points there instead of inventing one. Never render another
project's numbers as ken's.

## Boundaries

One-shot display. Edits nothing, changes no mode.
"stop ken" or "normal mode": revert.
