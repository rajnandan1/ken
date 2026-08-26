<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo.svg" width="220" alt="ken — Thompson-mode systems discipline">
  </picture>
</p>

<h1 align="center">ken</h1>

<p align="center">
  <em>Try it, and if it doesn't work, throw it out and do it again.</em>
</p>

Ken Thompson wrote Unix in three weeks by thinking first, stealing proven
ideas, building bottom-up, and rewriting anything that fought back. **ken**
puts that discipline inside your AI agent.

Not another "write less code" skill: [ponytail](https://github.com/DietrichGebert/ponytail)
already owns sizing, and ken is built to **complement** it (see below). Ken
governs *method* — how the code comes to exist:

```
The loop, in order, on every task:
1. Think first        → build the mental model before touching the code
2. Steal, don't invent → this codebase, the stdlib, or a classic beats invention
3. Build bottom-up    → from primitives you fully understand; layers are a morass
4. Brute force        → the plain algorithm until measurement proves it wrong
5. Try it             → working code settles arguments prose can't
6. Throw it out       → a unit on its third patch gets rewritten, not patched a fourth
```

Plus the rules the loop rests on: features default to no, interfaces few and
small, no layer that only translates, a minimal trusted base (vouch for a
dependency before using it — never paste code you can't explain line by line),
know every line, debug the model not the symptom, no ceremony. Every rule
traces to Thompson's own words — receipts in [PROVENANCE.md](PROVENANCE.md).

## Numbers

First measured round (2026-08-26; 3 arms × 5 tasks × 3 models × 3 repeats via
OpenRouter, single-shot; median LOC / executed-correctness gate):

| arm | haiku-4.5 | gpt-5.4-mini | gemini-3.5-flash | correctness |
|---|--:|--:|--:|--:|
| baseline (no skill) | 90 | 16 | 28 | 37/45 |
| ponytail | 9 | 7 | 10 | 45/45 |
| **ken** | **15** | **11** | **22** | **45/45** |

Ken cuts 31–83% of the code versus no skill and passed every executed
correctness check; all 8 gate failures in the run were baseline cells. Ponytail
stays smaller — it is the sizing skill; ken is the method skill. Single-shot
numbers overstate any skill's win (a bare model pads its answer with prose);
method, limits, and the full honesty notes: [benchmarks/results/](benchmarks/results/).
Nothing in this repo claims a number that wasn't measured — `/ken-gain` renders
only what `benchmarks/results/` contains.

## Install

Node.js must be on your PATH for the two tiny lifecycle hooks (skills still
work without it; activation just stays quiet).

### Claude Code

```
/plugin marketplace add rajnandan1/ken
```
```
/plugin install ken@ken
```

From a local clone: `claude plugin marketplace add /path/to/ken` then
`claude plugin install ken@ken`.

### Everyone else

Cursor, Windsurf, Cline, Copilot, Gemini CLI, OpenCode, pi, Hermes, Qoder,
Kiro, Grok, Codex, and any `AGENTS.md`-reading agent — see
[docs/agent-portability.md](docs/agent-portability.md). MCP-only hosts:
[ken-mcp/](ken-mcp/).

## Levels

| Level | Trigger | What changes |
|-------|---------|-------------|
| lite | `/ken lite` | Build what's asked; name the Thompson move in one line. |
| full | `/ken` | The loop enforced. Brute force until measured. Rewrite over third patch. Default. |
| ultra | `/ken ultra` | Darwinist: rewrite-first on rot, features argued in explicitly, no new dependencies. |

`/ken default <level>` persists across sessions (or `KEN_DEFAULT_MODE`, or
`~/.config/ken/config.json`). Off: say `stop ken`, or `/ken off`.

## Commands

`/ken` · `/ken-review` (method review: `rot:` `layer:` `unvouched:` `fancy:`
`ceremony:`) · `/ken-audit` (repo-wide) · `/ken-debt` (harvest `ken:`
brute-force ceilings) · `/ken-gain` (measured scoreboard) · `/ken-help`.

Deliberate brute-force ceilings are marked in code:

```js
// ken: linear scan; sort + bisect when n > 10k measured
```

## Runs alongside ponytail

Both installed? They complement instead of compete. When ponytail is active,
ken injects only its **delta** — think-first, steal-don't-invent, bottom-up,
brute-force ceilings, vouched dependencies, debug-the-model — plus one
arbitration rule: *a unit on its third patch gets the rewrite even though it's
a bigger diff; laziest-over-time beats laziest-today.* One engineer's voice,
not two. `stop ken` turns off only ken; `normal mode` turns off both; the
statusline badge shows `[KEN+PT]`.

## What ken never does

Brute force never overrides correctness: input validation at trust boundaries,
error handling that prevents data loss, security, accessibility, and anything
you explicitly asked for are never simplified away. And it never rewrites what
it doesn't yet understand — think-first is the gate.

## Uninstall

Each host's own uninstall removes the plugin files; `node scripts/uninstall.js`
cleans up what those can't see (mode flag, config, statusline entry — leaving
any other plugin's statusline segment intact).

## Provenance & credits

Rule-by-rule sourcing with ratings: [PROVENANCE.md](PROVENANCE.md) — including
the famous lines that could *not* be verified and are marked attributed.

Ken's plugin architecture is derived from
[ponytail](https://github.com/DietrichGebert/ponytail) by Dietrich Gebert (MIT
— see [LICENSE](LICENSE)), which pioneered the single-source-ruleset,
multi-host-adapter design ken reuses. The benchmark harness is ponytail's,
with ken arms and a rewrite behavior probe.

MIT © Raj Nandan Sharma
