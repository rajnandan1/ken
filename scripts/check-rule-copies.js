#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');

function read(relPath) {
  return fs.readFileSync(path.join(root, relPath), 'utf8').replace(/\r\n/g, '\n').trim();
}

function stripFrontmatter(text) {
  return text.replace(/^---\n[\s\S]*?\n---\n*/, '').trim();
}

const agents = read('AGENTS.md');
const canonical = agents.replace(/\n\n\(Yes, this file also applies[\s\S]*?\)$/, '').trim();

// Compact copies: same body as AGENTS.md, host-specific frontmatter stripped.
const copies = [
  ['.cursor/rules/ken.mdc', stripFrontmatter],
  ['.windsurf/rules/ken.md', text => text.trim()],
  ['.clinerules/ken.md', text => text.trim()],
  ['.agents/rules/ken.md', text => text.trim()],
  ['.qoder/rules/ken.md', text => text.trim()],
  ['.github/copilot-instructions.md', text => text.trim()],
  ['.kiro/steering/ken.md', stripFrontmatter],
];

let failed = false;

for (const [relPath, normalize] of copies) {
  const actual = normalize(read(relPath));
  if (actual !== canonical) {
    console.error(`${relPath} drifted from AGENTS.md`);
    failed = true;
  }
}

// SKILL.md is the runtime source of truth and is longer than the compact body,
// so it cannot be byte-compared. ken: canary, not full equality. Assert the
// load-bearing rules survive verbatim in both the source and AGENTS.md. Changing
// a rule's wording trips this, which is the reminder to propagate it everywhere.
// Upgrade path: generate the copies from SKILL.md if this ever misses a real drift.
const INVARIANTS = [
  'use brute force',                 // the core maxim
  'third patch',                     // rewrite-over-patch trigger
  'only translates',                 // no translate-only layers
  'explain line by line',            // minimal trusted base / vouching
  'runnable check',                  // throwaway rounds still need their check
  // safety carve-outs: pin each so a reword in either file can't silently drop
  // one. Continuous substrings present in both files ("input validation at
  // trust" because "boundaries" wraps a line in SKILL.md).
  'input validation at trust',
  'prevents data loss',
  'security',
  'accessibility',
];

const skill = read('skills/ken/SKILL.md');
const sources = [['skills/ken/SKILL.md', skill], ['AGENTS.md', agents]];
for (const phrase of INVARIANTS) {
  for (const [label, text] of sources) {
    if (!text.includes(phrase)) {
      console.error(`${label} is missing rule invariant: "${phrase}"`);
      failed = true;
    }
  }
}

if (failed) {
  console.error('Update the copied rule text, AGENTS.md, or SKILL.md so the shared rules match.');
  process.exit(1);
}

console.log(`Rule copies match AGENTS.md; ${INVARIANTS.length} rule invariants present in SKILL.md and AGENTS.md.`);
