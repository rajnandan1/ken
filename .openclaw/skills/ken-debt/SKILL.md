---
name: ken-debt
description: "Harvest every ken: ceiling comment into one ledger, so brute-force deferrals get tracked instead of forgotten. One-shot report."
homepage: https://github.com/rajnandan1/ken
license: MIT
---

Every deliberate ken brute-force ceiling is marked with a `ken:` comment
naming its ceiling and upgrade trigger. This collects them into one ledger so
a deferral can't quietly become permanent.

## Scan

Grep the repo for comment markers, skipping `node_modules`, `.git`, and build
output:

`grep -rnE '(#|//) ?ken:' .`  (add other comment prefixes if your stack uses them)

Each hit is one ledger row. The comment prefix keeps prose that merely mentions
the convention out of the ledger.

## Output

One row per marker, grouped by file:

`<file>:<line>, <the brute-force form used>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

The convention is `ken: <ceiling>, <upgrade trigger>`, so pull the ceiling
and the trigger straight from the comment. Want an owner per row too? add
`git blame -L<line>,<line>`.

Flag the rot risk: any `ken:` comment that names no upgrade trigger gets a
`no-trigger` tag, those are the ones that silently rot.

End with `<N> markers, <M> with no trigger.` Nothing found: `No ken: debt. Clean ledger.`

## Boundaries

Reads and reports only, changes nothing. To persist it, ask and it writes the
ledger to a file (e.g. `KEN-DEBT.md`). One-shot. "stop ken-debt" or
"normal mode" to revert.
