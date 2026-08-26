# 2026-08-26 — Four-arm round: baseline / ponytail / ken / ponytail+ken

Second round of the day, adding the **combined arm**: ponytail's full SKILL.md
plus ken's delta, built by `arms/ponytail-ken.js` requiring
`getDeltaInstructions()` from the real hooks module — byte-for-byte what a
session injects when both plugins are active. 4 arms × 5 tasks × 3 models ×
3 repeats = 180 cells, 0 API errors, 4m04s. Same config as the
[morning three-arm round](2026-08-26-baseline-openrouter.md) otherwise.

## Code LOC (median per cell, n=15)

| arm | haiku-4.5 | gpt-5.4-mini | gemini-3.5-flash |
|---|--:|--:|--:|
| baseline (no skill) | 73 | 15 | 29 |
| ponytail | 7 | 7 | 7 |
| ken | 11 | 11 | 16 |
| **ponytail+ken** | **9** | **6** | **10** |

## Correctness gate (passes / cells)

| arm | haiku-4.5 | gpt-5.4-mini | gemini-3.5-flash | total |
|---|--:|--:|--:|--:|
| baseline (no skill) | 15/15 | 15/15 | 12/15 | 42/45 |
| ponytail | 15/15 | 14/15 | 15/15 | 44/45 |
| ken | 13/15 | 14/15 | 15/15 | 42/45 |
| **ponytail+ken** | **15/15** | **15/15** | **14/15** | **44/45** |

## Output tokens (median) / latency (median s)

| arm | haiku | gpt-5.4-mini | gemini-flash |
|---|--:|--:|--:|
| baseline | 1338 / 8.5 | 217 / 3.4 | 1846 / 11.7 |
| ponytail | 150 / 3.3 | 84 / 2.4 | 780 / 6.1 |
| ken | 235 / 3.8 | 174 / 2.5 | 853 / 6.8 |
| **ponytail+ken** | **170 / 3.4** | **80 / 2.1** | **863 / 6.5** |

## Reading these numbers honestly

- **The combined arm keeps ponytail's sizing while carrying ken's method.**
  Its LOC medians sit at ponytail's level (9/6/10 vs 7/7/7) — on gpt-5.4-mini
  it is the smallest arm outright — and far below solo ken (11/11/16). The
  delta costs almost nothing in tokens or latency. This is the configuration
  the plugins actually produce together, and it ties for the best correctness
  total of the round (44/45).
- **Run-to-run noise is real at repeat 3.** Versus the morning round, medians
  moved a few lines in both directions (baseline haiku 90→73, ken haiku
  15→11) and this round's 8 gate failures scattered across all four arms
  (3/1/3/1) where the morning's 8 were all baseline. Treat 1–3 LOC
  differences and single gate cells as temperature-1 variance; the robust
  findings are the order of magnitudes: every skill arm cuts baseline hard,
  and no arm collapses on correctness (worst cell: 13/15).
- Single-shot tier limits apply as always (chat answers, not agent sessions;
  prose-padded baselines). The combined arm's agentic behavior — where ken's
  rewrite/reuse/trace rules actually bite — is unmeasured until an agentic
  round runs.

Raw data: `benchmarks/output.json` (this run overwrites the morning file; the
morning entry's numbers remain recorded in its own results doc).
Reproduce: `OPENROUTER_API_KEY=... npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml --repeat 3`.
