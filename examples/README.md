# Examples

Real model output, verbatim from benchmark runs — the same task answered by the same model
with no skill (`## Without Ken`) and with ponytail (`## With Ken`), so you can
compare side by side. Model: Claude Haiku 4.5, temperature 1, source `benchmarks/output.json`.

These are not hand-written. Reproduce them yourself:
`npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml`. Method, all three models, and
median-of-10 numbers: [../benchmarks/](../benchmarks/).

| Example | Without (LOC) | With (LOC) |
|---|--:|--:|
| [Email Validation](email-validation.md) | 68 | 8 |
| [Debounce](debounce.md) | 82 | 11 |
| [CSV Sum](csv-sum.md) | 14 | 7 |
| [Countdown Timer](react-countdown.md) | 241 | 30 |
| [Rate Limiting](rate-limit.md) | 117 | 50 |
