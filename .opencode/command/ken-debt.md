---
description: Harvest ken: ceiling comments into a tracked ledger
---

Harvest each `ken:` comment into a ceilings ledger. Grep the whole tree for comment markers (grep -rnE '(#|//) ?ken:' ., skipping node_modules/.git/build output). Group one row per marker by file: <file>:<line>: <the brute-force form used>. ceiling: <the limit named in the comment>. upgrade: <the trigger to revisit>. Tag a marker without an upgrade trigger as no-trigger. End with the marker count and the number without a trigger. If none exist: 'No ken: debt. Clean ledger.' Report only; change nothing.
