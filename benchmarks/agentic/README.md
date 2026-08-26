# Agentic benchmark

The single-shot benchmark (`../promptfooconfig.yaml`) measures one prompt, one completion.
That does not reflect how a coding agent is actually used, and counting lines of a
conversational answer (which dumps multiple options and commentary) inflates the baseline.

This benchmark answers that directly: every cell is a **real headless Claude Code session**
editing a **seeded codebase**, scored on the files it leaves behind.

## What is different

| | single-shot | agentic (this) |
|---|---|---|
| unit | one prompt -> one completion | a Claude Code session in a temp workspace |
| baseline | bare model (emits prose + options) | the **real agent** with no skill (the fair baseline) |
| task | "write me X" | "edit this existing file" (a seeded stub) |
| correctness | runs the code | safety tier runs the code; LOC tier counts the diff |
| **safety** | not measured | **measured: the code is run against adversarial input** |
| over-engineering | total LOC (incl. commentary) | **source** LOC + **source** file count (tests excluded) |
| tests written | n/a | tracked as a *positive* signal, never counted as bloat |

## Arms

`baseline` (no skill) · `ken` (plugin, real SessionStart activation) · `ponytail` (plugin —
the comparison arm) · `yagni-oneliner` ("Follow YAGNI principles, and prefer one-liner
solutions." — the seven-word control: if one line of prompt matches ken, the benchmark
should show it).

Skills are plugins activated by a SessionStart hook. To test exactly one at a time the runner
excludes the user's globally-enabled plugins (`--setting-sources project,local`) and loads one
plugin from its cache dir (`--plugin-dir`). ken and ponytail must both be installed (or set
`KEN_PLUGIN_DIR` / `PONYTAIL_PLUGIN_DIR`).

## Tasks

Same instrument set as the reference harness, unchanged — they are skill-agnostic:

- **Safety tier** (deterministic, stdlib-only, adversarial input executed): `todo-null`,
  `safe-path`, `critic-email`, `rate-limit`, `sql-user`, `auth-token`, `csv-sum`, `cache`.
- **Quality tier** (reuse the project's helper; fix the shared root cause, not the named
  symptom): `reuse-slug`, `reuse-money`, `trace-transfer`, `trace-amount`. These probe
  exactly ken's steal-don't-invent and debug-the-model rules.
- **Open/vibe tier** (LOC only): `open-*`, `vibe-*`.
- **Real-repo tier**: `tmpl-*` — needs a clone of
  [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) at
  `cd83fc1`; point `KEN_TMPL` at it or drop it at `fixtures/full-stack-fastapi-template`.

Every deterministic instrument ships a `good` and a `bad` reference and is verified by
`--selftest` (good must pass, bad must be caught) **before any API call**.

## Judges

- `judge.py` — over-engineering (0-3), fixed model at temperature 0, published rubric, must
  cite the unnecessary construct; validated by `--selftest` before scoring anything real.
- `complete.py` — completeness (0-3): a low-LOC arm whose completeness also drops is doing
  less, not less-bloated. `--selftest-offline` proves the gate logic with no API key.

## Reproduce

Needs the `claude` CLI, Python 3, and an authenticated Claude Code:

```bash
python run.py --selftest                                    # prove the instruments, no API -- run first
python run.py --task safe-path,critic-email,rate-limit,sql-user,auth-token,csv-sum,cache \
  --arms baseline,ken,ponytail,yagni-oneliner --models haiku --runs 4 --workers 6
python run.py --rescore runs/<stamp>                        # recompute metrics offline, no API
```

Agents only **write code**: `--strict-mcp-config` removes MCP tools and `--disallowedTools Bash`
blocks running anything. Each cell runs `bypassPermissions` in its own fresh workspace under
`runs/<stamp>/` (gitignored, kept), so any metric change is re-applied offline with `--rescore`.

## Results

No agentic run has been recorded for ken yet. The first one lands in
[../results/](../results/) with its full configuration; nothing is claimed before that.
