# 2026-08-26 — First baseline round (OpenRouter, 3 models, repeat 3)

The first measured ken numbers. Single-shot tier: `promptfooconfig.openrouter.yaml`,
3 arms (baseline / ponytail / ken) × 5 tasks × 3 models × 3 repeats = 135 cells,
0 API errors, 3m14s wall clock, 237,933 total tokens. Cost telemetry was not
reported per-cell by the OpenRouter route, so output tokens stand in for cost below.

- Arms: `arms/baseline.js` (no skill), `arms/ponytail.js` (vendored ponytail v4.9.0
  SKILL.md), `arms/ken.js` (ken v1.0.0 SKILL.md). System-prompt injection, single
  completion, default temperature (gpt-5.4-mini: provider default).
- Models via OpenRouter: `anthropic/claude-haiku-4.5`, `openai/gpt-5.4-mini`,
  `google/gemini-3.5-flash`.
- Metrics: `loc.js` (median non-blank, non-comment LOC from fenced blocks) and
  `correctness.js` (executed gate for email/debounce/CSV; structural for React/FastAPI).

## Code LOC (median per cell, n=15 per cell)

| arm | haiku-4.5 | gpt-5.4-mini | gemini-3.5-flash |
|---|--:|--:|--:|
| baseline (no skill) | 90 | 16 | 28 |
| ponytail | 9 | 7 | 10 |
| **ken** | **15** | **11** | **22** |

## Correctness gate (passes / cells)

| arm | haiku-4.5 | gpt-5.4-mini | gemini-3.5-flash |
|---|--:|--:|--:|
| baseline (no skill) | 12/15 | 15/15 | 10/15 |
| ponytail | 15/15 | 15/15 | 15/15 |
| **ken** | **15/15** | **15/15** | **15/15** |

All 8 failed cells in the run were baseline cells (executed code crashing the
harness checks). Neither skill arm failed a single gate.

## Output tokens (median) and latency (median seconds)

| arm | haiku tok / s | gpt-5.4-mini tok / s | gemini-flash tok / s |
|---|--:|--:|--:|
| baseline | 1375 / 7.9 | 197 / 3.1 | 1798 / 12.8 |
| ponytail | 137 / 2.9 | 91 / 1.8 | 580 / 5.3 |
| **ken** | **267 / 3.7** | **104 / 2.3** | **889 / 6.6** |

## Reading these numbers honestly

- **Versus baseline**, ken cuts code 31–83% (haiku 90→15, gemini 28→22,
  gpt-5.4-mini 16→11), output tokens 47–81%, and goes 45/45 on the correctness
  gate where baseline drops 8 cells. On chatty models (haiku, gemini) the
  baseline number includes multi-option answers and commentary — the usual
  single-shot inflation; the gap is real but overstated.
- **Versus ponytail**, ken is consistently *larger* (roughly 1.5–2× LOC) and
  slower. That is the designed difference, not a surprise: ponytail is a sizing
  discipline (write the least), ken is a method discipline (think, steal,
  bottom-up, brute force, rewrite). Nothing in this tier exercises ken's
  distinct organs — rewrite-over-patch, trusted-base vouching, translate-layer
  deletion, debug-the-model. Those need the behavior gates (`behavior.yaml`)
  and the agentic tier.
- **Hypothesis tested and rejected**: ken's extra lines over ponytail are NOT
  explained by its runnable-check rule — a check marker appears in only 5/45
  ken outputs (ponytail 4/45, baseline 0/45). In single-shot chat, neither
  skill reliably triggers the check discipline; that rule targets agent
  sessions that write files.
- Repeat 3 is a small n. Medians are stable at this size for LOC but treat
  single-cell differences as noise.

Raw data: `benchmarks/output.json` (eval ID eval-uO1-2026-08-26T10:12:25).
Reproduce: `OPENROUTER_API_KEY=... npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml --repeat 3`.
