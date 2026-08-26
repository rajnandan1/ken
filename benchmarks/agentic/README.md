# Agentic benchmark

The single-shot benchmark (`../promptfooconfig.yaml`) measures one prompt and one completion.
Coding agents work across sessions, and conversational answers inflate the baseline with
options and commentary.

Each benchmark cell runs a **headless Claude Code session**
editing a **seeded codebase**, scored on the files it leaves behind.

## What is different

|                  | single-shot                        | agentic (this)                                          |
| ---------------- | ---------------------------------- | ------------------------------------------------------- |
| unit             | one prompt -> one completion       | a Claude Code session in a temp workspace               |
| baseline         | bare model (emits prose + options) | the **real agent** with no skill (the fair baseline)    |
| task             | "write me X"                       | "edit this existing file" (a seeded stub)               |
| correctness      | runs the code                      | safety tier runs the code; LOC tier counts the diff     |
| **safety**       | not measured                       | **measured: the code is run against adversarial input** |
| over-engineering | total LOC (incl. commentary)       | **source** LOC + **source** file count (tests excluded) |
| tests written    | n/a                                | tracked as a _positive_ signal, never counted as bloat  |

## Arms

`baseline` (no skill) · `ken` (plugin, real SessionStart activation) · `yagni-oneliner`
("Follow YAGNI principles, and prefer one-liner solutions."). The seven-word control tests
whether one line of prompt can match ken.

Skills are plugins activated by a SessionStart hook. To test one skill per run, the runner
excludes plugins from the user's settings (`--setting-sources project,local`) and loads the
ken plugin from its cache dir (`--plugin-dir`); ken must be installed (or set `KEN_PLUGIN_DIR`).

## Tasks

The benchmark uses the reference harness's skill-agnostic instruments:

- **Safety tier** (deterministic, stdlib-only, adversarial input executed): `todo-null`,
  `safe-path`, `critic-email`, `rate-limit`, `sql-user`, `auth-token`, `csv-sum`, `cache`.
- **Quality tier** (reuse the project's helper; fix the shared root cause, not the named
  symptom): `reuse-slug`, `reuse-money`, `trace-transfer`, `trace-amount`. These probe
  ken's steal-don't-invent and debug-the-model rules.
- **Open/vibe tier** (LOC only): `open-*`, `vibe-*`.
- **Real-repo tier**: `tmpl-*` needs a clone of
  [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) at
  `cd83fc1`; point `KEN_TMPL` at it or drop it at `fixtures/full-stack-fastapi-template`.

Every deterministic instrument includes `good` and `bad` references. `--selftest` requires
the good reference to pass and catches the bad reference **before any API call**.

## Judges

- `judge.py`: over-engineering (0-3), fixed model at temperature 0, published rubric, must
  cite the unnecessary construct; validated by `--selftest` before scoring anything real.
- `complete.py`: completeness (0-3). A low-LOC arm whose completeness drops is doing
  less, not less-bloated. `--selftest-offline` proves the gate logic with no API key.

## Reproduce

Needs the `claude` CLI, Python 3, and an authenticated Claude Code:

```bash
python run.py --selftest                                    # prove the instruments, no API; run first
python run.py --task safe-path,critic-email,rate-limit,sql-user,auth-token,csv-sum,cache \
  --arms baseline,ken,yagni-oneliner --models haiku --runs 4 --workers 6
python run.py --rescore runs/<stamp>                        # recompute metrics offline, no API
```

Agents only **write code**: `--strict-mcp-config` removes MCP tools and `--disallowedTools Bash`
blocks running anything. Each cell runs `bypassPermissions` in its own fresh workspace under
`runs/<stamp>/` (gitignored, kept), so any metric change is re-applied offline with `--rescore`.

## Results

The first recorded agentic run will land in [../results/](../results/) with
its full configuration. Ken will claim results after that run.
