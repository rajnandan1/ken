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

### Maintenance-over-time (`maintenance/`) — the flagship

A sequence of 10 realistic tickets against ONE persistent codebase (`ledgerd`):
the agent's output is the substrate for every later round, a git commit lands
per round, and the headline is **Survival** — the end-of-run pass rate of all
earlier tickets' tests (visible + hidden). Scored deterministic rates: reuse
(planted-helper divergence probes), root-cause (hidden sibling-caller tests),
rewrite-on-rot (sentinel patch-trails). Erosion/churn/clone-density/cost are
reported as curves, never scored. No LLM judges anywhere.

```bash
cd benchmarks/maintenance
python run.py --selftest     # scripted good/bad reference agents through the
                             # full pipeline — no API; the bad twin passes every
                             # VISIBLE test and must be caught by every rate
python run.py --run --arms baseline,ken --repeats 3 --model haiku
```

Until a measured round lands in [results/](results/), ken claims no numbers.

### Prerequisites

**Node.js ≥ 22.22.0** for promptfoo (behavior gates), **Python 3** and the
`claude` CLI for the agentic tiers.
