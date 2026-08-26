---
name: ken-audit
description: "Audit the whole repo for Thompson-mode violations. A ranked list of what to rewrite, delete, or take back into the trusted base."
homepage: https://github.com/rajnandan1/ken
license: MIT
---

ken-review, repo-wide. Scan the whole tree instead of a diff. Rank findings
biggest rewrite payoff first.

## Tags

Same as ken-review:

- `rot:` unit patched past rot; next fix is a rewrite. Name the rewrite's shape.
- `layer:` wrapper/adapter/manager adding no decision. Delete, move callers down.
- `unvouched:` dependency or pasted code nobody can explain. Read it or replace it.
- `fancy:` clever where the plain form wins at this scale. Name the brute-force form.
- `ceremony:` process, abstraction, or config serving itself. Remove it.

## Hunt

Files with the densest fix-commit history (rot lives where patches pile up:
`git log --format= --name-only | sort | uniq -c | sort -rn | head`),
wrappers that only delegate, dependencies used for one call, hand-rolled
cleverness at small n, translate-only layers between the caller and the work,
config nobody sets.

## Output

One line per finding, ranked: `<tag> <what>. <the move>. [path]`.
End with `net: -<N> lines, -<M> layers, trusted base -<K> deps possible.`
Nothing to flag: `Sound. Ship it.`

## Boundaries

Scope: Thompson-mode method violations only. Correctness bugs, security
holes, and performance are explicitly out of scope. Route them to a normal
review pass. Lists findings, applies nothing. One-shot.
