# Provenance

Every rule in ken's ruleset (`skills/ken/SKILL.md`) traces to something Ken
Thompson said or did. This file is the trace. Research was done against the
sources themselves (fetched copies and scanned-book full-text search), not
quote aggregators.

**Ratings**

- **PRIMARY**: Thompson's own words, verified verbatim against a copy of the source.
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
| Deleting code is productive work | "One of my most productive days was throwing away 1,000 lines of code" is **UNVERIFIED**. Researchers found no primary source; the earliest visible carrier is an uncited 2003 epigraph. Ken uses the sentiment, grounded by the verified rewrite quotes, and never presents the wording as verbatim Thompson. | None located                   | ATTRIBUTED |

## Ken's own operationalizations (not Thompson quotes)

Measured iteration (see `benchmarks/results/`) showed the aspirational forms of
two corpus-traced rules did not change agent behavior, so v1.1 restates them as
procedures. These lines are **ken's own**, marked here so they are never read
as Thompson's words:

- "count the unit's fix-comment trail: three or more prior fixes … rewrite it,
  never add entry four" operationalizes the PRIMARY rewrite quotes (CaW 2009;
  IEEE 1999).
- the caller-enumeration / never-guard-a-single-call-site procedure and
  "smallest-correct beats smallest" operationalize the WITNESS
  debug-the-model account (InformIT 2012). (Three instruction forms, abstract,
  first-action, and tool-literal, all measured as non-firing and were
  reverted; the shipped wording keeps the honest aspiration, and the limit
  is documented in benchmarks/results/.)

## Persona

"I am a programmer. On my 1040 form, that is what I put down as my
occupation." Turing lecture, 1984. PRIMARY.

## Common misattributions

- **Doug McIlroy**: "Write programs that do one thing and do it well" (BSTJ 57(6), 1978).
- **Rob Pike**: The "5 Rules of Programming" ("Notes on Programming in C", 1989).
- **Brian Kernighan**: "Debugging is twice as hard as writing the code..." (with Plauger, 1978).
- **Dennis Ritchie**: "You are not expected to understand this," by his own account.
- **Kelly Johnson**: "Keep it simple, stupid," Lockheed Skunk Works.
- **Kernighan**: "The most effective debugging tool is still careful thought, coupled with judiciously placed print statements" ("Unix for Beginners", 1979).
