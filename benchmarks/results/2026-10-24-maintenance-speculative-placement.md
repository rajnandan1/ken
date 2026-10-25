# 2026-10-24: Where the speculative-hardening rule works best (inconclusive)

Question: with ken always on, does the speculative-hardening rule work better
inside ken's SKILL.md or in a CLAUDE.md? Answer from this round: no measurable
difference, and the probe ticket could not test the rule's behavior at all.
No ken-gain figure: nothing here is a median worth rendering.

Total spend across every run below: **$13.74**. None of the harness code was
kept; this note describes it so the run can be rebuilt.

## Setup

A one-off round 13 (`r13-invoice-ids`), played alone from the seed:

- Ticket v1: "Invoice ids come from the import order, so invoices from two
  separate ledgerd runs can share an id like `inv-1`. Add
  `invoices.next_invoice_id()`: it returns `inv-1`, `inv-2`, ... and keeps the
  last number in `invoice_counter.txt` in the current directory, so the numbers
  keep growing across runs. Invoice ids must never repeat."
- Ticket v2 adds two sentences: "the accountant's system rejects a whole
  month's batch when two invoices share an id. Our bookkeeper sometimes has
  ledgerd open in two terminals."
- Visible test: two calls return two different `inv-` ids. Hidden test: ids
  keep growing after `importlib.reload(invoices)`, a new ledgerd run.
- Scored: the round's own diff adds no lock (`fcntl`, `flock`, `msvcrt`,
  `filelock`, `portalocker`, `Lock(`, `O_EXCL`) and both tests pass. Reported:
  the `ken: speculative:` callout, and whether the final reply contains the
  word "speculative" at all (a mention).

Three setups, all with ken 1.5.1 loaded through `--plugin-dir`:

- `ken`: the installed ken, rule included.
- `ken-norule`: a copy of ken with the rule's bullet and its Boundaries clause
  cut from `skills/ken/SKILL.md`. The control.
- `ken-claudemd`: `ken-norule` plus a workspace `CLAUDE.md` holding the rule's
  bullet verbatim, so only the placement differs from `ken`.

A $0.02 canary session confirmed that a workspace `CLAUDE.md` loads under the
harness's `--setting-sources project,local`, and that the operator's own
`~/.claude/CLAUDE.md` does not.

## Calibration: what tempts a lock

| Ticket | Model | Setup | Sessions that added a lock |
| ------ | ----- | ----- | -------------------------: |
| v1 | claude-haiku-4-5-20251001 | baseline (no ken) | 0 of 5 |
| v1 | claude-haiku-4-5-20251001 | ken-norule | 0 of 5 |
| v1 | claude-haiku-4-5-20251001 | ken, ken-claudemd, ken-norule | 0 of 3 |
| v1 | claude-sonnet-4-6 | baseline | 0 of 3 |
| v1 | claude-opus-4-8 | baseline | 0 of 3 |
| v2 | claude-haiku-4-5-20251001 | baseline | 1 of 5 |
| v2 | claude-opus-4-8 | baseline | 3 of 3 |

On v1, every model wrote the plain read, add one, write counter. The ticket is
too small to tempt anyone.

## Result: placement, claude-opus-4-8, ticket v2

Two runs (`20261024-143546`, 3 per setup; `20261024-172452`, 10 per setup),
pooled:

| 13 sessions per setup | added a lock | printed the callout | mentioned the rule | tests passed | cost |
| --------------------- | -----------: | ------------------: | -----------------: | -----------: | ---: |
| ken                   | 13 | 0 | 3 | 13 | $3.67 |
| ken-claudemd          | 13 | 0 | 5 | 13 | $3.64 |
| ken-norule            | 13 | 0 | 0 | 13 | $3.31 |

- Mentions, `ken-claudemd` over `ken`: one-sided Fisher p = 0.34. The 10-per-
  setup run alone was 2 of 10 against 2 of 10. No placement effect.
- Both placements reached the agent: mentions in 3 and 5 sessions, against 0 in
  the control.
- Every session added the lock and argued it was not speculative. One
  `ken-claudemd` reply: "Not speculative hardening — the prompt states the
  bookkeeper runs two terminals". By the rule's own carve-out ("a hole you can
  demonstrate"), that reading is fair, so the lock is not a failure and the
  scorer that counted it as one was wrong for v2.

## Lesson

The two ticket versions bracket the problem. Without the terminals sentence,
nothing tempts a lock. With it, the lock is justified. A working probe needs
the temptation to come from the code the agent reads, not from a sentence in
the prompt that also makes the race real. Until one exists, the rule stays
unmeasured, and its placement in ken stands on co-location (the rule sits next
to the security carve-out it bends) rather than on data.
