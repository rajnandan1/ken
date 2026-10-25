# Provenance

Every rule in ken's ruleset (`skills/ken/SKILL.md`) traces to something Ken
Thompson said or did, except where this file says otherwise: "One-way doors
wait for a yes" adapts Jeff Bezos's one-way-door test, "Speculative hardening
waits for a yes" adapts a rule from another coding agent's instruction file, and the
clauses under "Ken's own operationalizations" are ken's own. The `ken:`
ceiling comment and the runnable check have no row yet. This file is the trace. Research was done
against the sources themselves (fetched copies and scanned-book full-text
search), not quote aggregators.

**Ratings**

- **PRIMARY**: Thompson's own words, verified verbatim against a copy of the source. A rating with a name in parentheses, such as PRIMARY (Bezos), rates that person's own words, not Thompson's.
- **WITNESS**: a colleague's first-hand account of Thompson's practice.
- **ATTRIBUTED**: others credit the words to Thompson; no researcher located a primary utterance.

**Primary sources**

| Source                                                                      | Year      |
| --------------------------------------------------------------------------- | --------- |
| "Reflections on Trusting Trust", Turing Award lecture, CACM 27(8)           | 1984      |
| Ritchie & Thompson, "The UNIX Time-Sharing System", CACM 17(7) / BSTJ 57(6) | 1974/1978 |
| Unix Oral History interview by Michael S. Mahoney (transcript at tuhs.org)  | 1989      |
| "Unix and Beyond: An Interview with Ken Thompson", IEEE Computer 32(5)      | 1999      |
| Peter Seibel, _Coders at Work_, ch. 12                                      | 2009      |
| Andrew Binstock, "Interview with Ken Thompson", Dr. Dobb's                  | 2011      |
| Rob Pike, "The Best Programming Advice I Ever Got", InformIT                | 2012      |
| Jeff Bezos, 2015 Letter to Shareholders (SEC Form 8-K Ex. 99.1, filed 2016-04-05) | 2016 |

## The loop

| Rule                            | Quote                                                                                                                                                                                                                                       | Source                         | Rating     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ---------- |
| Think first                     | Pike, pairing with Thompson at Bell Labs: "Ken would just stand and think" and announce the bug before Pike found it; "thinking — without looking at the code — is the best debugging tool of all."                                         | InformIT 2012                  | WITNESS    |
| Steal, don't invent             | "the things we stole: We stole a shell out of a MULTICS, the concept of a shell." On pipes, paring McIlroy's "grandiose ideas" down for years until "it hit just one night... and they went in instantly, I mean they are utterly trivial." | Mahoney 1989                   | PRIMARY    |
| Build bottom-up                 | "I am a very bottom-up thinker... When I see a top-down description of a system or language that has infinite libraries described by layers and layers, all I just see is a morass."                                                        | IEEE Computer 1999             | PRIMARY    |
| When in doubt, use brute force  | Earliest print: Bentley's "Bumper-Sticker Computer Science", CACM Sep 1985, attribution as submitted; the Jargon File hedges "is reported to have uttered". Canonical by tradition, consistent with everything above.                       | Bentley 1985                   | ATTRIBUTED |
| Try it                          | "computer Darwinism: Try it, and if it doesn't work throw it out and do it again."                                                                                                                                                          | IEEE Computer 1999             | PRIMARY    |
| Throw it out when it fights you | "I've never been a lover of existing code. Code by itself almost rots and it's gotta be rewritten." Unix itself: "These rewrites failed twice in the space of six months... The third rewrite... was successful."                           | Coders at Work 2009; IEEE 1999 | PRIMARY    |

## Rules

| Rule                             | Quote                                                                                                                                                                                                                                                                                                          | Source                         | Rating     |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ---------- |
| Features default to no           | On designing Go: "all three of us had to be talked into every feature in the language, so there was no extraneous garbage put into the language for any reason."                                                                                                                                               | Dr. Dobb's 2011                | PRIMARY    |
| Interfaces few and small         | "the major good idea in Unix was its clean and simple interface: open, close, read, and write." "the size constraint has encouraged not only economy, but also a certain elegance of design."                                                                                                                  | IEEE 1999; CACM 1974           | PRIMARY    |
| No layer that only translates    | "Modern programming scares me in many respects, where they will just build layer after layer after layer that does nothing except translate."                                                                                                                                                                  | Coders at Work 2009            | PRIMARY    |
| Minimal trusted base             | "You can't trust code that you did not totally create yourself... No amount of source-level verification or scrutiny will protect you from using untrusted code." On Linux: "A whole bunch of random people have contributed to this source, and the quality varies drastically."                              | Turing lecture 1984; IEEE 1999 | PRIMARY    |
| Know every line                  | "[at] night I'd sit there and walk through it line by line and find bugs."                                                                                                                                                                                                                                     | Coders at Work 2009            | PRIMARY    |
| Debug the model, not the symptom | Pike's conclusion from Thompson's practice: fixing the mental model "leads to better software" than diving on the symptom.                                                                                                                                                                                     | InformIT 2012                  | WITNESS    |
| No ceremony                      | Asked for design principles: "I am not sure there are real principles involved as opposed to serendipity... My advice to you is just be lucky." On Google's mandatory language certification: "I'm not allowed to check in code, no."                                                                          | IEEE 1999; Coders at Work 2009 | PRIMARY    |
| One-way doors wait for a yes | **Not Thompson's.** Bezos: "Some decisions are consequential and irreversible or nearly irreversible – one-way doors – and these decisions must be made methodically, carefully, slowly, with great deliberation and consultation. … But most decisions aren't like that – they are changeable, reversible – they're two-way doors." No Thompson source searched states the rule. His nearest line limits "Try it" to work outside product development: "Try it, and if it doesn't work throw it out and do it again. You just can't do that in a product-development environment." "I'd spell creat with an e" shows what a shipped name costs, but Kernighan & Pike report it with no asker or date. | Bezos 2015 letter; IEEE 1999 pp. 59–60; K&P 1984 p. 204 | PRIMARY (Bezos); IEEE line PRIMARY; creat line ATTRIBUTED |
| Deleting code is productive work | "One of my most productive days was throwing away 1,000 lines of code" is **UNVERIFIED**. Researchers found no primary source; the earliest visible carrier is an uncited 2003 epigraph. Ken uses the sentiment, grounded by the verified rewrite quotes, and never presents the wording as verbatim Thompson. | None located                   | ATTRIBUTED |

## Ken's own operationalizations (not Thompson quotes)

Measured iteration (see `benchmarks/results/`) showed the aspirational forms of
two corpus-traced rules did not change agent behavior, so v1.1 restates them as
procedures. These lines, and every later clause in this list, are **ken's
own**, marked here so they are never read as Thompson's words:

- "count the unit's fix-comment trail: three or more prior fixes … rewrite it,
  never add entry four" operationalizes the PRIMARY rewrite quotes (CaW 2009;
  IEEE 1999).
- the caller-enumeration / never-guard-a-single-call-site procedure and
  "smallest-correct beats smallest" operationalize the WITNESS
  debug-the-model account (InformIT 2012). (Three instruction forms, abstract,
  first-action, and tool-literal, all measured as non-firing and were
  reverted; the shipped wording keeps the honest aspiration, and the limit
  is documented in benchmarks/results/.)
- "rot outside the ticket's scope gets named in one line as a follow-up,
  never an unrequested rewrite" is a scope-precedence clause ken adds to the
  rewrite rule (field-report driven, 2026-08-28); no Thompson source claims
  it, and the benchmark does not measure it.
- A fourth form, "the old unit is the spec for everything the ticket leaves
  alone: a rewrite keeps every input it accepted … and those inputs become
  asserts in the unit's check before the old code goes" (v1.5 candidate,
  2026-08-30), was measured and **reverted**: where a rewrite happened it lost
  no case, but the rewrite trigger fired less often. Not shipped; the record
  is in benchmarks/results/.

- "One-way doors wait for a yes" is ken's wording of Bezos's one-way/two-way
  door test (2015 letter, section "Invention Machine"). The door terms are
  Bezos's. The trigger list (destroy others' data git doesn't hold,
  force-push over others' commits, send code or data to a third party, break
  a name used outside the repo), the `ken: irreversible: <action>; <what is
  lost>` callout line, and "two-way doors run with no callout" are ken's own. None of these Thompson
  sources states the rule: Mahoney 1989, IEEE 1999, the Turing lecture, CACM
  1974 / BSTJ 1978, Dr. Dobb's 2011, and InformIT 2012, searched in full, and
  _Coders at Work_, searched only through archive.org's snippet index. Not
  measured yet; maintenance round 12 (`r12-rename-log`) is its probe.
- "Speculative hardening waits for a yes" is ken's wording of a rule from
  another coding agent's instruction file. No Thompson source was searched
  for it, so it has no row in the rules table. The leading phrase shared with the
  one-way-door rule, the `ken: speculative: <failure mode>; <likelihood>;
  <cost: lines, new state, new deps>` callout line, and the carve-out for trust-boundary validation and a
  hole you can demonstrate are ken's own. Not measured yet; no maintenance
  round probes it. A 2026-10-24 placement run found no difference between
  ken's SKILL.md and a CLAUDE.md, and its ticket could not test the behavior
  (`benchmarks/results/2026-10-24-maintenance-speculative-placement.md`).

## Persona

"I am a programmer. On my 1040 form, that is what I put down as my
occupation." Turing lecture, 1984. PRIMARY.

## Common misattributions

- **Doug McIlroy**: "Write programs that do one thing and do it well," as quoted in Salus, _A Quarter Century of UNIX_ (1994), pp. 52–53. BSTJ 57(6), 1978, maxim (i), has "Make each program do one thing well."
- **McIlroy, Pinson and Tague** record as a house maxim of the Unix builders: "Design and build software, even operating systems, to be tried early, ideally within weeks. Don't hesitate to throw away the clumsy parts and rebuild them." (BSTJ 57(6), 1978, "Foreword", maxim (iii), p. 1902). It is close to "Throw it out when it fights you", but the Foreword names no author for the maxim, so ken never quotes it as Thompson's.
- **Rob Pike**: The "5 Rules of Programming" ("Notes on Programming in C", 1989).
- **Brian Kernighan**: "Debugging is twice as hard as writing the code..." (with Plauger, 1978).
- **Dennis Ritchie**: "You are not expected to understand this," by his own account.
- **Kelly Johnson**: "Keep it simple, stupid," Lockheed Skunk Works.
- **Kernighan**: "The most effective debugging tool is still careful thought, coupled with judiciously placed print statements" ("Unix for Beginners", 1979).
