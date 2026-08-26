#!/usr/bin/env node
// Unit test for the behavior gate (benchmarks/behavior.js). Feeds known
// behavior-present and behavior-absent outputs through each probe checker and
// asserts the verdict. Runs without promptfoo or an API key — it proves the
// grader can tell the ken behavior from its absence, which is what makes the
// behavior.yaml eval trustworthy.

const test = require('node:test');
const assert = require('node:assert/strict');
const behavior = require('../benchmarks/behavior');

function check(probe, output) {
  return behavior(output, { vars: { probe } });
}

// --- rewrite: a thrice-patched unit gets rewritten, and the answer says so ---

test('rewrite: rewrote the unit and said so passes', () => {
  const r = check('rewrite',
    'This parser has rotted through three patches, so I rewrote it from scratch:\n' +
    '```python\nimport re\ndef parse_duration(s):\n' +
    "    units = {'h': 3600, 'm': 60, 's': 1}\n" +
    "    return int(sum(float(n) * units[u or 's'] for n, u in re.findall(r'([\\d.]+)([hms]?)', s)))\n```");
  assert.equal(r.pass, true);
  assert.equal(r.score, 1);
});

test('rewrite: alternate phrasing (replaced the function) passes', () => {
  const r = check('rewrite',
    'I replaced the function entirely — the patch trail was the problem:\n' +
    '```python\ndef parse_duration(s):\n    return 45\n```');
  assert.equal(r.pass, true);
});

test('rewrite: silent fourth patch fails', () => {
  const r = check('rewrite',
    'Added a check after the loop so bare numbers are counted:\n' +
    '```python\ndef parse_duration(s):\n    total = 0\n    num = ""\n' +
    '    # ...existing patches...\n    if num:\n        total += float(num)\n    return int(total)\n```');
  assert.equal(r.pass, false);
  assert.equal(r.score, 0);
});

test('rewrite: claims a rewrite but ships no implementation fails', () => {
  const r = check('rewrite', 'I rewrote everything, trust me.');
  assert.equal(r.pass, false);
});

// --- explanation: requested write-up is not ceremony ---

test('explanation: full requested write-up passes', () => {
  const r = check('explanation',
    '```python\ndef positives_doubled(rows):\n    return [x["a"] * 2 for x in rows if x.get("a", 0) > 0]\n```\n' +
    '1. Renamed p to positives_doubled because the name should say what it returns.\n' +
    '2. Replaced the manual loop and append with a list comprehension, same logic, fewer lines.\n' +
    '3. Used x.get("a", 0) so a missing key is treated as zero instead of raising.\n' +
    '4. Kept the > 0 filter; the behavior is unchanged, only the shape is clearer.');
  assert.equal(r.pass, true);
});

test('explanation: terse truncation fails', () => {
  const r = check('explanation',
    '```python\ndef positives_doubled(rows):\n    return [x["a"] * 2 for x in rows if x.get("a", 0) > 0]\n```\n' +
    'threw away: the loop. comprehension covers it.');
  assert.equal(r.pass, false);
});

// --- onecheck: leave one runnable check ---

test('onecheck: leaves an assert passes', () => {
  const r = check('onecheck',
    '```python\ndef to_seconds(s):\n    ...\n\nassert to_seconds("1h30m") == 5400\n```');
  assert.equal(r.pass, true);
});

test('onecheck: no check fails', () => {
  const r = check('onecheck',
    '```python\ndef to_seconds(s):\n    import re\n    return sum(...)\n```');
  assert.equal(r.pass, false);
});

// --- unknown probe is skipped, not failed ---

test('unknown probe is skipped', () => {
  const r = check('something-else', '```python\nprint(1)\n```');
  assert.equal(r.pass, true);
  assert.match(r.reason, /skipped/i);
});
