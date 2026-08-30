# Benchmark

Ken makes **method** claims, not sizing claims: rewrite rot instead of patching
it again, reuse the project's helper instead of reinventing it, fix the shared
root cause instead of the named symptom, vouch for dependencies, leave a
runnable check. Lines of code measure none of that, so ken carries no LOC
benchmark.

**This repo claims measured numbers. [results/](results/) records each run's
date, model, and configuration. `/ken-gain` renders that record.**

## What exists today

### Behavior gates (`behavior.yaml` + `behavior.js`)

Three probes test whether the ruleset produces its stated behaviors. Each
probe covers one ken rule and uses baseline as the control arm:

- `rewrite`: a thrice-patched unit gets rewritten (and the answer says so),
  without a fourth patch
- `explanation`: the agent gives the user a full requested write-up
- `onecheck`: non-trivial logic leaves one runnable check behind

```bash
npx promptfoo@latest eval -c benchmarks/behavior.yaml --env-file ../.env --repeat 10
```

`tests/behavior.test.js` proves the graders (RED/GREEN, no
API key).

### Agentic tiers (`agentic/`)

Real headless Claude Code sessions editing seeded codebases, scored on the
files left behind. The **quality tier** measures ken's axes: reuse
the project helper (`reuse-slug`, `reuse-money`), fix the shared root cause
(`trace-transfer`, `trace-amount`). The **safety tier** executes produced
code against adversarial input. Every instrument proves itself with
`--selftest` before any API spend. See [agentic/](agentic/).

### Maintenance-over-time (`maintenance/`)

A sequence of 11 realistic tickets against ONE persistent codebase (`ledgerd`):
the agent's output is the substrate for every later round, a git commit lands
per round. **Survival** records the end-of-run pass rate of all
earlier tickets' tests (visible + hidden). Scored deterministic rates: reuse
(planted-helper divergence probes), root-cause (hidden sibling-caller tests),
rewrite-on-rot (sentinel patch-trails), trusted-base (the HTTP API ticket:
no import outside the stdlib and the project anywhere in source). Erosion/
churn/clone-density/cost are reported as curves, never scored. No LLM judges
anywhere.

The trusted-base probe landed 2026-08-30 as round 11, so survival is now
scored over rounds 1..10; the v1 result tables in [results/](results/) keep
their rounds 1..9 denominator.

```bash
cd benchmarks/maintenance
python run.py --selftest     # scripted good/bad reference agents through the
                             # full pipeline; no API; the bad twin passes every
                             # VISIBLE test and must be caught by every rate
python run.py --run --arms baseline,ken --repeats 3 --model haiku
```

Ken claims a number after a measured round lands in [results/](results/).

### Prerequisites

**Node.js ≥ 22.22.0** for promptfoo (behavior gates), **Python 3** and the
`claude` CLI for the agentic tiers.
