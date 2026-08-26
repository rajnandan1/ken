# Benchmark

Three arms (no skill, [ponytail](https://github.com/DietrichGebert/ponytail) vendored at `arms/ponytail-SKILL.md`, ken), three models, five everyday tasks. Code LOC is counted from fenced code blocks; tokens, cost, and latency come straight from the API.

Ponytail is the comparison arm on purpose: ken claims to be a *method* discipline where ponytail is a *sizing* discipline, and the benchmark exists to show whether that difference is measurable.

**Nothing in this file claims a number that wasn't measured. Every measured run lives in [results/](results/) with its date, model, and repeat count. `/ken-gain` renders only what results/ contains.**

## Reproduce

### Claude (Haiku / Sonnet / Opus)

Requires an Anthropic API key and **Node.js ≥ 22.22.0** (promptfoo's engine constraint,
check with `node --version` and upgrade if needed):

```bash
cp ../.env.example .env      # add your ANTHROPIC_API_KEY
npx promptfoo@latest eval -c promptfooconfig.yaml --env-file ../.env --repeat 10
npx promptfoo@latest view
```

`--env-file ../.env` is required because promptfoo reads `.env` from the current
directory (`benchmarks/`), not the repo root where the file lives.

### Behavior gates

Does the ruleset produce its behaviors (rewrite-over-patch, requested explanation,
one runnable check), not just carry the text? Baseline is the control arm:

```bash
npx promptfoo@latest eval -c behavior.yaml --env-file ../.env --repeat 10
```

### Local models via Ollama

No API key or promptfoo required. Runs against any model served by Ollama:

```bash
ollama pull llama3.2          # or any other model
python benchmarks/benchmark-local.py --model llama3.2 --repeat 3
```

### Agentic tier

Real headless Claude Code sessions editing seeded codebases — see [agentic/](agentic/).
Run `python agentic/run.py --selftest` first; it refuses to spend before the
instruments prove themselves.

Tasks: email validator, JS debounce, CSV sum, React countdown, FastAPI rate-limit (see `promptfooconfig.yaml`). Single-shot completions, default temperature.

## Metrics

| File | Metric | Behavior |
|------|--------|----------|
| `loc.js` | `loc` | Measurement - always passes, records line count |
| `correctness.js` | `correct` | Gate - fails if generated code doesn't work |
| `behavior.js` | `behavior` | Gate - fails if a probed ken behavior is absent |

`correctness.js` extracts fenced code blocks and runs per-task checks (spawns Python/Node for email, debounce, CSV; structural regex for React and FastAPI). A broken one-liner that scores great on LOC will fail on correctness.

> **Note:** The React countdown and FastAPI rate-limit checks are keyword/structural only (no runtime execution), so they verify plausible structure rather than full correctness. The email, debounce, and CSV checks execute the code.

### Prerequisites

Running the benchmark requires **Python 3** and **Node.js ≥ 22.22.0** (promptfoo's engine constraint; see [Reproduce](#reproduce)).

## Honesty notes

- Single-shot numbers count a chat answer's fenced code, against a bare model that may answer with several options plus commentary — they overstate any skill's win. The agentic tier (real sessions, real diffs, safety executed against adversarial input) is the defensible number. Read both.
- Cost reflects single-shot calls, not real multi-turn agent sessions; in a session the ruleset re-injects every turn. Treat these as generation numbers, not a session-cost promise.
- Never compare a ken number against a number produced by someone else's harness or another repo's run — reproduce first.
