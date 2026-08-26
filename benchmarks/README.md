# Benchmark

Ken makes **method** claims, not sizing claims: rewrite rot instead of patching
it again, reuse the project's helper instead of reinventing it, fix the shared
root cause instead of the named symptom, vouch for dependencies, leave a
runnable check. Lines of code measure none of that, so ken carries no LOC
benchmark.

**Nothing in this repo claims a number that wasn't measured. Every measured
run lives in [results/](results/) with its date, model, and configuration.
`/ken-gain` renders only what results/ contains.**

## What exists today

### Behavior gates (`behavior.yaml` + `behavior.js`)

Does the ruleset *produce* its behaviors, not just carry the text? Three
probes, each a ken rule, with baseline as the control arm:

- `rewrite` — a thrice-patched unit gets rewritten (and the answer says so),
  not silently patched a fourth time
- `explanation` — a write-up the user explicitly asked for is given in full
- `onecheck` — non-trivial logic leaves one runnable check behind

```bash
npx promptfoo@latest eval -c benchmarks/behavior.yaml --env-file ../.env --repeat 10
```

The graders are proven separately by `tests/behavior.test.js` (RED/GREEN, no
API key).

### Agentic tiers (`agentic/`)

Real headless Claude Code sessions editing seeded codebases, scored on the
files left behind. The **quality tier** measures ken's axes directly — reuse
the project helper (`reuse-slug`, `reuse-money`), fix the shared root cause
(`trace-transfer`, `trace-amount`) — and the **safety tier** executes produced
code against adversarial input. Every instrument proves itself with
`--selftest` before any API spend. See [agentic/](agentic/).

## What's being built

The flagship measurement is under design: a **maintenance-over-time**
benchmark — a sequence of tickets against the same codebase, scoring what
*survives*: correctness after N rounds, whether rot triggers rewrites, reuse
rate, root-cause rate. Solving for the code that lasts, not the code that is
written. Until it produces numbers, ken claims none.

### Prerequisites

**Node.js ≥ 22.22.0** for promptfoo (behavior gates), **Python 3** and the
`claude` CLI for the agentic tiers.
