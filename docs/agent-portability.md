# Agent Portability

Ken is an agent-portable skill distribution. The skills in `skills/` hold the
core behavior; host-specific files are adapters that make that behavior easy to
load in a given agent.

## Supported Adapters

| Host | Files | Notes |
|------|-------|-------|
| Claude Code | `.claude-plugin/plugin.json`, `commands/`, `hooks/claude-codex-hooks.json`, `hooks/` | Full plugin install with session activation, mode tracking, commands, and statusline support. |
| Codex | `.codex-plugin/plugin.json`, `hooks/claude-codex-hooks.json`, `hooks/`, `skills/` | Plugin install with the same skills plus lifecycle hooks for activation and mode tracking. |
| Grok Build | root `plugin.json`, `.grok-plugin/marketplace.json`, `skills/`, `commands/` | `grok plugin install rajnandan1/ken --trust`, then enable. Grok auto-invokes ken from its coding-task skill description; `/ken` makes activation explicit. Lifecycle hooks are not used because passive hook output cannot inject instructions. |
| OpenCode | `.opencode/plugins/ken.mjs`, `.opencode/command/`, `hooks/`, `skills/` | Server plugin injects the ruleset each turn via `experimental.chat.system.transform` and persists `/ken` switches; reuses the shared instruction builder. |
| pi | `pi-extension/`, `skills/`, `hooks/` | Package extension: injects the ruleset each turn through the shared instruction builder and registers the `/ken` commands. |
| Hermes Agent | `plugin.yaml`, `__init__.py`, `skills/` | Native Hermes plugin: injects active mode through `pre_llm_call`, rewrites gateway `/ken-*` skill commands into agent prompts, registers `/ken` mode switching, and exposes bundled skills as `ken:<skill>`. |
| Gemini CLI | `gemini-extension.json`, `AGENTS.md`, `commands/`, `skills/` | Extension manifest points `contextFileName` at `AGENTS.md` for always-on rules and reuses `commands/*.toml` and `skills/`, which Gemini CLI auto-discovers. The Claude/Codex hook map is not placed at Gemini's auto-discovered `hooks/hooks.json` path. |
| Cursor | `.cursor/rules/ken.mdc` | Always-on project rule. |
| Windsurf | `.windsurf/rules/ken.md` | Project rule. |
| Cline | `.clinerules/ken.md` | Project rule. |
| GitHub Copilot | `.github/copilot-instructions.md` | Repository instruction file. |
| GitHub Copilot CLI | `.github/plugin/`, `AGENTS.md`, `.github/copilot-instructions.md` | Plugin-supported (`copilot plugin marketplace add rajnandan1/ken` + `copilot plugin install ken@ken`). Fallback instruction mode: per-project from `AGENTS.md` or `.github/copilot-instructions.md` (instruction-tier, no `/ken` levels or hooks). |
| Kiro | `.kiro/steering/ken.md` | Steering rule; copy globally or into a project. |
| Qoder | `.qoder/rules/ken.md`, `.qoder-plugin/plugin.json`, `hooks/qoder-hooks.json`, `skills/`, `AGENTS.md` | Qoder auto-loads `AGENTS.md` as always-on context; `.qoder/rules/ken.md` provides per-project rules; the plugin manifest points at `skills/`. Full plugin-tier: `hooks/qoder-hooks.json` template registers `UserPromptSubmit` (mode activation + ruleset injection) and `PreToolUse` with `task\|Task` matcher (subagent injection). |
| AGENTS.md hosts (Antigravity, CodeWhale, Zed, Amp, Jules, Junie, VS Code Codex ext, …) | `AGENTS.md` | Any agent that reads `AGENTS.md` from the repo root gets the compact always-on ruleset. Instruction-tier: no `/ken` levels or hooks. |
| Generic agents | `AGENTS.md` or `skills/*/SKILL.md` | Copy the compact rule file or load the skill files directly. |

## Adapter Rule

Keep adapters thin. When a host supports skills or hooks, point it at the
existing `skills/` and `hooks/` files. When a host only supports project
instructions, keep its copied rule text aligned with `AGENTS.md`
(`scripts/check-rule-copies.js` enforces this).

## Portable Behavior

- `skills/ken/SKILL.md`: Thompson-mode systems discipline (the loop)
- `skills/ken-review/SKILL.md`: method review — rot, layers, unvouched deps
- `skills/ken-audit/SKILL.md`: whole-repo method audit
- `skills/ken-debt/SKILL.md`: harvest `ken:` brute-force ceilings into a tracked ledger
- `skills/ken-gain/SKILL.md`: measured-impact scoreboard from ken's own benchmark results
- `skills/ken-help/SKILL.md`: quick reference
- `AGENTS.md`: compact always-on instruction set for agents without skill support
