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

Not another "write less code" skill. Ken governs *method* — how the code
comes to exist:

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

## What ken measures

Ken makes method claims, so lines of code are not its benchmark. What it
measures instead: does the agent **rewrite** a thrice-patched unit instead of
adding patch four, **reuse** the project's helper instead of reinventing it,
fix the shared **root cause** instead of the named symptom, **vouch** for what
it depends on, and leave a **runnable check** behind. The behavior gates and
agentic quality tier in [benchmarks/](benchmarks/) measure exactly that; a
maintenance-over-time benchmark — scoring what *survives* a sequence of
tickets, not what gets written — is under design.

**Only measured numbers are claimed — including the ones that don't flatter
ken.** Measured so far ([haiku](benchmarks/results/2026-08-26-maintenance-v1-haiku.md) /
[sonnet](benchmarks/results/2026-08-26-maintenance-v1-sonnet.md) v1.0.0 rounds, then the
[iteration-1 verdict](benchmarks/results/2026-08-26-maintenance-v1_1-verdict.md)):
v1.0.0's aspirational rules changed nothing — no advantage on either model,
1 rewrite in 24 rot cells. Iteration 1 made two rules procedural and
re-measured under a pre-registered keep/revert rule: **the countable rewrite
trigger took rewrite-on-rot from 0/2 to 2/2 in all three runs** (baseline,
same tickets, same day: still 0/2) with survival up, so **v1.1 shipped**.
Still honest about what hasn't moved: root-cause remains stuck (ken guards
the named symptom despite the new enumeration rule) — iteration 2's target. That is
the benchmark doing its job; stronger models and ruleset iterations get
measured next, and every run lands in
[benchmarks/results/](benchmarks/results/) whatever it shows. `/ken-gain`
renders only what that directory contains.

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

Ken's plugin architecture and benchmark harness are derived from
[ponytail](https://github.com/DietrichGebert/ponytail) by Dietrich Gebert
(MIT — see [LICENSE](LICENSE)).

MIT © Raj Nandan Sharma
