#!/usr/bin/env node
// Generate the OpenClaw / ClawHub skill package (.openclaw/skills/) from the
// canonical skills/. OpenClaw skills are SKILL.md (frontmatter + body), the same
// format ken already uses, with one difference: `description` must be a single
// line under 160 chars. The canonical descriptions are long (tuned for Claude's
// skill picker), so each ships a short one here. The body is copied verbatim
// from skills/<name>/SKILL.md so the ruleset never drifts; only the frontmatter
// is rewritten.
//
// Run:  node scripts/build-openclaw-skills.js
// tests/openclaw-skills.test.js fails if the committed copies are stale.

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const HOMEPAGE = 'https://github.com/rajnandan1/ken';

const DESCRIPTIONS = {
  'ken': 'Thompson-mode discipline for any coding task: think first, build bottom-up, brute force until measured, rewrite over patch. Not for non-coding requests.',
  'ken-review': 'Review a diff for method violations: rot to rewrite, translate-only layers, unvouched deps, fancy over brute force. One line per finding.',
  'ken-audit': 'Audit the whole repo for Thompson-mode violations. A ranked list of what to rewrite, delete, or take back into the trusted base.',
  'ken-debt': 'Harvest every ken: ceiling comment into one ledger, so brute-force deferrals get tracked instead of forgotten. One-shot report.',
  'ken-gain': 'Show ken measured impact as a scoreboard from its own benchmark results. Honest empty state when none exist. One-shot display.',
  'ken-help': 'Quick reference for ken modes, skills, and commands. One-shot display.',
};

const NAMES = Object.keys(DESCRIPTIONS);

function sourceBody(name) {
  const src = fs.readFileSync(path.join(ROOT, 'skills', name, 'SKILL.md'), 'utf8').replace(/\r\n/g, '\n');
  const fm = src.match(/^---\n[\s\S]*?\n---\n?/);
  if (!fm) throw new Error(`skills/${name}/SKILL.md has no frontmatter`);
  return src.slice(fm[0].length);
}

function render(name) {
  const desc = DESCRIPTIONS[name];
  if (desc.length > 160 || desc.includes('\n') || desc.includes('"')) {
    throw new Error(`description for ${name} must be one line, no quotes, under 160 chars`);
  }
  const frontmatter =
    `---\nname: ${name}\ndescription: "${desc}"\nhomepage: ${HOMEPAGE}\nlicense: MIT\n---\n`;
  return frontmatter + sourceBody(name);
}

function outPath(name) {
  return path.join(ROOT, '.openclaw', 'skills', name, 'SKILL.md');
}

module.exports = { DESCRIPTIONS, NAMES, render, outPath, sourceBody };

if (require.main === module) {
  for (const name of NAMES) {
    const p = outPath(name);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, render(name));
    console.log('wrote', path.relative(ROOT, p).replace(/\\/g, '/'));
  }
}
