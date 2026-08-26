# 2026-08-26: Maintenance-over-time v1, first measured round (haiku)

`benchmarks/maintenance/`, run `20260826-193017`: baseline vs ken, 3 repeats
each × 10 sequential tickets against one persistent `ledgerd` workspace.
60 headless Claude Code sessions, claude-haiku-4-5, **$3.19 total**,
~25 min wall clock. The instruments passed selftest before the run
(good ref 9/9 · 4/4 · 2/2 · 2/2; lazy twin caught on every rate).

**A probe verified the arm:** a session with the same ken-arm flags
answered "Ken mode active at full intensity — Thompson-mode systems
discipline…", with the injected ruleset visible as ~7.8k cache-creation
tokens. The ken arm ran ken.

## The result: no ken advantage in this configuration

| median of 3 runs | survival (of 9) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
| ---------------- | --------------: | -----------: | ----------------: | --------------------: | -------: |
| baseline         |           **8** |            3 |             **2** |                     0 |    $0.55 |
| ken              |               7 |            3 |                 1 |                     0 |    $0.51 |

Per-round failure map (end-of-run):

- **r9 search (reuse probe): 6/6 sessions failed.** Each run on both arms
  hand-rolled `.lower()` matching; the hidden accent probe (`'cafe'` must find
  `'Café Olé'`) caught them all. This is also both arms' shared survival loss.
- **r4 + r8 (rewrite-on-rot): 6/6 sessions patched, 0 rewrote.** The tickets
  say outright that the unit "has already been patched three times"; ken's
  third-patch rule is verbatim in its injected ruleset. Every session added
  patch four. The patches work and those rounds survive, but the sentinel
  trails remain in all 12 rot cells.
- **r6 overdraw (root-cause probe): ken 0/3, baseline 2/3.** All three ken
  runs guarded `transfer` (the named symptom) and left the shared `_debit`
  unguarded, so the hidden `withdraw` test failed; baseline fixed `_debit`
  in two of three runs. The n=3 result gives direction without significance;
  the direction is against ken.
- r1, r3, r7 reuse probes passed on both arms (the planted helpers are
  discoverable enough that even baseline uses them at this codebase size).

## Interpretation

1. **On haiku, the injected ruleset did not produce the method.** An explicit
   rewrite-on-third-patch rule faced a ticket that says "patched three times,"
   yet patch/rewrite, reuse, and root-cause behavior did not change. The first
   measured round detected the failure mode the benchmark targets.
2. **The instrument separates method when method differs** (selftest: 9/9 vs
   2/9), so the instrument can distinguish method changes. The arm produced
   the null result.
3. **Limits:** one model (haiku, the cheapest; instruction-following depth
   is part of what's being measured), one seed codebase, n=3, single-session
   rounds (no conversation memory across tickets). Later measurements can
   cover stronger models and ruleset iterations. Each needs its own cost gate
   and a published result.

Raw data: `benchmarks/maintenance/runs/20260826-193017/results.json` (kept on
the machine that ran the benchmark; workspaces preserved for `--rescore`).
Reproduce: `cd benchmarks/maintenance && python run.py --run --arms baseline,ken --repeats 3 --model haiku`.
