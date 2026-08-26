---
name: ken-help
description: >
  Quick-reference card for all ken modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /ken-help,
  "ken help", "what ken commands", "how do I use ken".
---

# Ken Help

Display this reference card when invoked. One-shot, do NOT change mode,
write flag files, or persist anything.

## Levels

| Level | Trigger | What changes |
|-------|---------|-------------|
| **Lite** | `/ken lite` | Build what's asked, name the Thompson move (the rewrite, the brute-force cut) in one line. |
| **Full** | `/ken` | The loop enforced: think first → steal → bottom-up → brute force → try it → throw it out. Default. |
| **Ultra** | `/ken ultra` | Darwinist: rewrite-first on rot, features argued in explicitly, no new dependencies at all. |

Level sticks until changed or session end.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **ken** | `/ken` | Thompson mode itself. Think, steal, build bottom-up, brute force, rewrite. |
| **ken-review** | `/ken-review` | Method review: `L42: rot: third patch on this unit. Rewrite, ~25 lines.` |
| **ken-audit** | `/ken-audit` | Whole-repo method audit: ranked list of what to rewrite or remove. |
| **ken-debt** | `/ken-debt` | Harvest `ken:` ceiling comments into a tracked ledger. |
| **ken-gain** | `/ken-gain` | Measured-impact scoreboard from ken's own benchmark results. |
| **ken-help** | `/ken-help` | This card. |

Codex uses `@ken`, `@ken-review`, and `@ken-help`; Claude Code and OpenCode
use the slash-command forms above (OpenCode ships all six as slash commands).

## Ponytail

Ken complements ponytail: when both are active, ponytail governs sizing
(write the least) and ken governs method (how the code comes to exist) — ken
injects only its delta, one engineer's voice, not two.

## Deactivate

Say "stop ken" (ken only) or "normal mode" (also turns off ponytail).
Resume anytime with `/ken`. `/ken off` also works.

## Configure Default Mode

Default mode = `full`, auto-active every session. Change it:

**Environment variable** (highest priority):
```bash
export KEN_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/ken/config.json`, Windows: `%APPDATA%\ken\config.json`):
```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation on session start, activate manually
with `/ken` when wanted.

Resolution: env var > config file > `full`.

## Update

Enable auto-update once: open `/plugin`, go to Marketplaces, pick ken, Enable auto-update. Claude Code then pulls new versions at startup (run `/reload-plugins` when it prompts). Manual refresh: `/plugin marketplace update ken` then `/reload-plugins`.

If `/plugin` is not recognized, your Claude Code is out of date. Update it (`npm install -g @anthropic-ai/claude-code@latest`, or `brew upgrade claude-code`) and restart. Other hosts use their own update flow.

## More

Full docs + provenance for every rule: the ken repo's README.md and PROVENANCE.md.
