// Behavior gate: does the ken ruleset actually PRODUCE its behaviors, not just
// carry the text? One check per probe (vars.probe), each targeting a
// load-bearing ken rule:
//   rewrite      - "a unit on its third patch gets rewritten, not patched a
//                   fourth" + the output rule "if you rewrote instead of
//                   patched, say so in one line"
//   explanation  - "explanation the user explicitly asked for is not ceremony"
//   onecheck     - "a throwaway round still needs its smallest runnable check"
//
// Heuristic graders, same spirit as loc.js / correctness.js. The graders
// themselves are proven by tests/behavior.test.js (RED/GREEN, no API key).
//
// Metric: `behavior` (1 = behavior present, 0 = absent).

function proseOf(text) {
  return String(text || '').replace(/```[\s\S]*?```/g, ' ').replace(/\s+/g, ' ').trim();
}

const CHECKS = {
  // Rewrites the thrice-patched unit and says so, instead of silently adding
  // patch four. Needs both: a delivered implementation (fenced code defining
  // the function) and an explicit rewrite signal in the prose.
  rewrite(output) {
    const t = String(output || '');
    const hasImpl = /```[a-zA-Z0-9_+-]*\r?\n[\s\S]*?def\s+parse_duration[\s\S]*?```/.test(t);
    const saidRewrite = /\brewr(?:ote|itten|ite)\b|\breplaced? the (?:whole |entire )?(?:function|unit|implementation|parser)\b|\bfrom scratch\b|\bthrew (?:it |the old (?:one|version) )?away\b/i.test(proseOf(t));
    if (hasImpl && saidRewrite) return { pass: true, reason: 'Rewrote the rotten unit and said so.' };
    if (!hasImpl) return { pass: false, reason: 'No delivered parse_duration implementation.' };
    return { pass: false, reason: 'Patched silently; no rewrite signal on a thrice-patched unit.' };
  },

  // Gives the explanation the user explicitly asked for instead of truncating.
  explanation(output) {
    const p = proseOf(output);
    const words = p ? p.split(' ').length : 0;
    const structured = /(\d+[.)]\s|[-*]\s)/.test(String(output || '')) || /\bbecause\b|\bwhy\b|\bso that\b|renamed|extracted|inlined|removed|replaced/i.test(p);
    return words >= 45 && structured
      ? { pass: true, reason: `Gave the requested write-up (${words} words of prose).` }
      : { pass: false, reason: `Truncated the requested explanation (${words} words of prose).` };
  },

  // Leaves ONE runnable check behind for non-trivial logic.
  onecheck(output) {
    const t = String(output || '');
    const hasCheck = /\bassert\b|def\s+test_|if\s+__name__|unittest|pytest|console\.assert|\bexpect\(|\bdescribe\(|\bit\(/.test(t);
    return hasCheck
      ? { pass: true, reason: 'Left a runnable check (assert/test/demo).' }
      : { pass: false, reason: 'No runnable check left behind.' };
  },
};

module.exports = (output, context) => {
  const probe = context && context.vars && context.vars.probe;
  const check = CHECKS[probe];
  if (!check) return { pass: true, score: 1, reason: `Unknown probe '${probe}', skipped` };
  const r = check(output);
  return { pass: r.pass, score: r.pass ? 1 : 0, reason: r.reason };
};
