# 2026-08-30: Trusted-base probe lands (r11); first round scored with it

Run `20260830-212707`: baseline vs ken (v1.2.0 ruleset, **unchanged**), haiku,
3 repeats × 11 tickets, **$3.98**. The ken arm loaded the PR branch via
`KEN_PLUGIN_DIR`; cache tokens per round (90k–194k) show the injected ruleset
on the ken arm. Selftest passed before spend: good ref 10/10 · 4/4 · 2/2 ·
2/2 · 1/1; the lazy twin caught on every rate, `unvouched ['flask']`.

## What changed

Instrument only. The README listed vouch among the five measured behaviors and
no instrument scored it. Round 11 (`r11-http-api`) asks for an HTTP JSON API
in a project that is stdlib-only and declares no dependencies; nothing in the
prompt names `http.server` or a framework. The scorer parses every source file
with `ast` and flags any top-level import that is neither stdlib nor a project
module. `probe_pass` = no unvouched import **and** the visible test passes.
New rate: **trusted-base**. Survival is now scored over rounds 1..10 (of 10);
the tables before this one used 1..9.

## Pre-registered rule

The probe is kept on selftest alone: the lazy twin passes every visible test
of every other round and is caught here. Live-model discrimination is
**reported, never a keep criterion**. No ruleset wording changed in this round,
so no KEEP/REVERT verdict on wording applies.

## Result

| median of 3 runs | survival (of 10) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | trusted-base (of 1) | cost/run |
| ---------------- | ---------------: | -----------: | ----------------: | --------------------: | ------------------: | -------: |
| baseline         |                9 |            4 |                 1 |                     0 |                   1 |    $0.65 |
| ken              |                8 |            4 |                 1 |                 **2** |                   1 |    $0.68 |

## r11, cell by cell

- **baseline:** two of three served the routes on `http.server`. Run #1 wrote
  `from flask import Flask, request` (`unvouched: ['flask']`). Its visible test
  passed only because the benchmark host's Python ships Flask; on CI's 3.12 it
  dies on line 6. A dependency nobody chose, and the class of failure the probe
  exists to count.
- **ken:** three of three stdlib. Run #2 failed the visible test (HTTP 400): it
  wired both routes to `money.balances` and `money.deposit()`, which do not
  exist (balances live in `accounts.py`), and hand-parsed `sys.argv` instead of
  using `argparse` like the rest of the CLI. Vouched and wrong; 0/1 by the
  visible-pass clause.
- Both arms sit at 1/1 median, so this round does not discriminate at median.
  Across this round plus six single-shot field sessions run before the probe
  landed: baseline reached for Flask 3/6, ken 0/6. Direction, not significance.

## Survival: where the rewrite's point went

Ken's rewrite trigger fired 2/2 in two runs and 1/2 in one (the haiku variance
seen in the v1.4 round). Two of the six ken rot cells passed the round's
visible tests and lost a **hidden** earlier-fixed case:

- run #0, r4: the `parse_duration` rewrite returns the wrong total for
  `"10m30"` (bare trailing seconds after a unit).
- run #1, r8: the `import_rows` rewrite drops headerless files and rows with
  extra columns, the cases fixes #19 and #66 had covered.

Baseline added patch four in all six rot cells and kept every case: the trail
it left alone was also the spec. That is the survival gap (ken 8/10 in two
runs, baseline 9/10 in all three). Under `--disallowedTools Bash` the agent
cannot run the check ken's own rule demands of a throwaway round, so a
rewrite here is a rewrite without a runnable check. The rule is doing what it
says; the harness removes the tool that makes it safe. Interactive sessions,
where the agent runs the tests, are the unmeasured case.

Root-cause: r6 failed 6/6 across both arms again (every session guarded
`transfer`, `_debit` untouched); r2 passed 6/6. Reuse 4/4 on both arms, as in
the v1.4 round.

Raw data: `benchmarks/maintenance/runs/20260830-212707/` (workspaces kept,
per-round session records kept; `--rescore` recomputes offline).
