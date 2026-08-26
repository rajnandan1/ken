---
name: ken-review
description: >
    Code review for Thompson-mode violations. Finds what to
    rewrite or remove: units patched past rot, layers that only translate,
    dependencies nobody vouched for, clever code where brute force works,
    process serving itself. One line per finding: location, what's wrong, the
    move. Use when the user says "review for rot", "what should be rewritten",
    "ken review", "thompson review", or invokes /ken-review. Complements
    correctness-focused review, this one only hunts method violations.
---

Review diffs for Thompson-mode violations. One line per finding: location,
what's wrong, the move. The diff's best outcome is fewer layers and a
smaller trusted base.

## Format

`L<line>: <tag> <what>. <the move>.`, or `<file>:L<line>: ...` for
multi-file diffs.

Tags:

- `rot:` unit on repeated patches; the next fix is a rewrite, not patch N+1. Name the rewrite's shape.
- `layer:` wrapper, adapter, or manager that adds no decision of its own. Delete it, move callers down a level.
- `unvouched:` dependency or pasted code nobody present can explain. Vouch for it (read it) or replace with a few lines you own.
- `fancy:` clever algorithm where the plain loop wins at this scale. Name the brute-force form; demand the measurement that justifies fancy.
- `ceremony:` process, abstraction, or config that serves the process itself. Remove it.

## Examples

❌ "This caching layer might benefit from reconsidering its abstraction
boundaries and perhaps simplifying the invalidation strategy."

✅ `L12-60: rot: third patch on this cache's invalidation. Rewrite on a plain dict + mtime check, ~25 lines.`

✅ `L4: unvouched: left-pad-like microdep imported unread. 3 lines inline, trusted base shrinks by one.`

✅ `svc.py:L88: layer: OrderManager delegates every call to OrderRepo. Delete, callers hit OrderRepo.`

✅ `L30-52: fancy: hand-rolled B-tree for 40 entries. Flat array + linear scan; ken: revisit when n > 10k measured.`

✅ `L71: ceremony: config flag nobody sets gates one constant. Inline the constant.`

## Scoring

End with the metrics that matter: `net: -<N> lines, -<M> layers, trusted base -<K> deps possible.`

If there is nothing to flag, say `Sound. Ship it.` and stop.

## Boundaries

Scope: Thompson-mode method violations only. Correctness bugs, security
holes, and performance are out of scope. Route them to a normal
review pass, not this one. A single smoke test or `assert`-based self-check
is the ken minimum, not ceremony, never flag it for removal.
Does not apply the fixes, only lists them.
"stop ken-review" or "normal mode": revert to verbose review style.
