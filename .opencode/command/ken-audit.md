---
description: Audit the whole repo for rot, translate-only layers, unvouched deps
---

Audit Thompson-mode method violations across the repository. Skip correctness review. Scan the whole tree and weigh files with dense fix-commit history. Rank findings by rewrite payoff, one line each: <tag> <what>. <the move>. [path]. Tags: rot (rewrite a unit with repeated patches), layer (delete a wrapper that adds no decision), unvouched (read or replace a dependency or pasted code nobody can explain), fancy (use the plain form at this scale), ceremony (remove process or config that serves itself). End with the removable lines, layers, and dependencies. If nothing needs work: 'Sound. Ship it.'
