# 2026-08-26 — Maintenance-over-time v1, first measured round (haiku)

`benchmarks/maintenance/`, run `20260826-193017`: baseline vs ken, 3 repeats
each × 10 sequential tickets against one persistent `ledgerd` workspace.
60 headless Claude Code sessions, claude-haiku-4-5, **$3.19 total**,
~25 min wall clock. Instruments selftested green immediately before the run
(good ref 9/9 · 4/4 · 2/2 · 2/2; lazy twin caught on every rate).

**Arm validity verified:** a probe session with the identical ken-arm flags
answered "Ken mode active at full intensity — Thompson-mode systems
discipline…", with the injected ruleset visible as ~7.8k cache-creation
tokens. The ken arm really was running ken.

## The result: no ken advantage in this configuration

| median of 3 runs | survival (of 9) | reuse (of 4) | root-cause (of 2) | rewrite-on-rot (of 2) | cost/run |
|---|--:|--:|--:|--:|--:|
| baseline | **8** | 3 | **2** | 0 | $0.55 |
| ken | 7 | 3 | 1 | 0 | $0.51 |

Per-round failure map (end-of-run):

- **r9 search (reuse probe): 6/6 sessions failed** — every run on both arms
  hand-rolled `.lower()` matching; the hidden accent probe (`'cafe'` must find
  `'Café Olé'`) caught them all. This is also both arms' shared survival loss.
- **r4 + r8 (rewrite-on-rot): 6/6 sessions patched, 0 rewrote.** The tickets
  say outright that the unit "has already been patched three times"; ken's
  third-patch rule is verbatim in its injected ruleset. Every session added
  patch four (the patches work — those rounds survive — but the sentinel
  trails remain in all 12 rot cells).
- **r6 overdraw (root-cause probe): ken 0/3, baseline 2/3.** All three ken
  runs guarded `transfer` (the named symptom) and left the shared `_debit`
  unguarded, so the hidden `withdraw` test failed; baseline fixed `_debit`
  in two of three runs. n=3 — treat as directional, not significant — but
  the direction is against ken.
- r1, r3, r7 reuse probes passed on both arms (the planted helpers are
  discoverable enough that even baseline uses them at this codebase size).

## Reading this honestly

1. **Carrying the ruleset is not producing the method.** On haiku, ken's
   injected text — including an explicit rewrite-on-third-patch rule facing a
   ticket that says "patched three times" — did not change patch/rewrite
   behavior, reuse behavior, or root-cause behavior. This is the exact
   failure mode the benchmark was built to detect, and it detected it on the
   first measured round, in ken's own repo, against ken.
2. **The instrument separates method when method differs** (selftest: 9/9 vs
   2/9), so the null here is a finding about the arm, not the ruler.
3. **Limits:** one model (haiku — the cheapest; instruction-following depth
   is part of what's being measured), one seed codebase, n=3, single-session
   rounds (no conversation memory across tickets). Stronger models and
   ruleset iterations are the obvious next measurements — each behind its own
   cost gate, each recorded here whatever it shows.

Raw data: `benchmarks/maintenance/runs/20260826-193017/results.json` (kept
locally; workspaces preserved for `--rescore`).
Reproduce: `cd benchmarks/maintenance && python run.py --run --arms baseline,ken --repeats 3 --model haiku`.
