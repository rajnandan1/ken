---
description: Review changes for Thompson-mode violations: rot, layers, unvouched deps
---

Review the current changes for Thompson-mode method violations. Skip correctness review. Use one line per finding: L<line>: <tag> <what>. <the move>. Tags: rot (rewrite a unit with repeated patches and name its shape), layer (delete a wrapper that adds no decision and move callers down), unvouched (read or replace a dependency or pasted code nobody can explain), fancy (name the plain loop that wins at this scale), ceremony (remove process, abstraction, or config serving itself). End with the removable lines, layers, and dependencies. If nothing needs work: 'Sound. Ship it.'
