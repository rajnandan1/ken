---
name: ken-gain
description: "Show ken measured impact as a scoreboard from its own benchmark results. Honest empty state when none exist. One-shot display."
homepage: https://github.com/rajnandan1/ken
license: MIT
---

# Ken Gain

Display the scoreboard when invoked. One-shot: do NOT change mode, write flag
files, or persist anything.

## Source of truth

The only figures this card may show are medians from ken's own runs recorded
in `benchmarks/results/` of the ken repo. Read them; render what's actually
there as plain ASCII bars (bar length = measured range, label = exact figure).

If `benchmarks/results/` has no ken results yet, say exactly that:

```
  ken gain — no measured numbers yet.

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
this card points there instead of inventing one. Never render ponytail's
published numbers as ken's.

## Boundaries

One-shot display. Edits nothing, changes no mode.
"stop ken" or "normal mode": revert.
