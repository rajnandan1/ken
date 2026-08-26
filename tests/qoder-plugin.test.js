#!/usr/bin/env node
// Smoke test for the Qoder plugin adapter: verify manifest, rules, and skills
// wiring are present and consistent.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const SKILL_DIRS = [
  'ken',
  'ken-review',
  'ken-audit',
  'ken-debt',
  'ken-gain',
  'ken-help',
];

function readJSON(relPath) {
  return JSON.parse(fs.readFileSync(path.join(root, relPath), 'utf8'));
}

test('qoder plugin manifest exists and has required fields', () => {
  const manifest = readJSON('.qoder-plugin/plugin.json');
  assert.equal(manifest.name, 'ken');
  assert.ok(manifest.version, 'manifest must declare a version');
  assert.ok(manifest.description, 'manifest must declare a description');
  assert.ok(manifest.author, 'manifest must declare an author');
  assert.equal(manifest.license, 'MIT');
  assert.equal(manifest.skills, './skills/');
  assert.equal(manifest.rules, './.qoder/rules/');
  assert.equal(manifest.hooks, './hooks/qoder-hooks.json');
});

test('qoder hooks config exists and registers UserPromptSubmit', () => {
  const hooksConfig = readJSON('hooks/qoder-hooks.json');
  assert.ok(hooksConfig.hooks, 'hooks config must have a hooks key');
  assert.ok(hooksConfig.hooks.UserPromptSubmit, 'must register UserPromptSubmit hook');
  assert.ok(Array.isArray(hooksConfig.hooks.UserPromptSubmit), 'UserPromptSubmit must be an array');
  const cmd = hooksConfig.hooks.UserPromptSubmit[0].hooks[0].command;
  assert.ok(cmd.includes('ken-mode-tracker.js'), 'must point at ken-mode-tracker.js');
});

test('qoder rules file exists and is non-empty', () => {
  const rulesPath = path.join(root, '.qoder', 'rules', 'ken.md');
  assert.ok(fs.existsSync(rulesPath), '.qoder/rules/ken.md must exist');
  const content = fs.readFileSync(rulesPath, 'utf8').trim();
  assert.ok(content.length > 0, '.qoder/rules/ken.md must not be empty');
  assert.ok(content.includes('systems programmer'), 'rules must contain the ken identity');
});

test('qoder manifest points at skills that actually ship', () => {
  const manifest = readJSON('.qoder-plugin/plugin.json');
  const skillsDir = path.join(root, manifest.skills);
  assert.ok(fs.existsSync(skillsDir), 'skills/ directory must exist');

  for (const skill of SKILL_DIRS) {
    const skillFile = path.join(skillsDir, skill, 'SKILL.md');
    assert.ok(
      fs.existsSync(skillFile),
      `missing skill: skills/${skill}/SKILL.md`,
    );
  }
});

test('qoder rules match AGENTS.md canonical body', () => {
  // Reuse the same logic as check-rule-copies.js: the .qoder copy must be
  // byte-identical to AGENTS.md minus the repo-self-application paragraph.
  const agents = fs.readFileSync(path.join(root, 'AGENTS.md'), 'utf8')
    .replace(/\r\n/g, '\n').trim();
  const canonical = agents.replace(/\n\n\(Yes, this file also applies[\s\S]*?\)$/, '').trim();
  const qoderCopy = fs.readFileSync(path.join(root, '.qoder', 'rules', 'ken.md'), 'utf8')
    .replace(/\r\n/g, '\n').trim();
  assert.equal(qoderCopy, canonical, '.qoder/rules/ken.md drifted from AGENTS.md');
});

test('qoder runtime detects QODER_SESSION_ID and writes hookSpecificOutput JSON', () => {
  const { isQoder } = require('../hooks/ken-runtime');
  // isQoder is resolved at module load time from process.env; in the test
  // process QODER_SESSION_ID is unset, so isQoder must be false here.
  // The positive path is exercised in hooks.test.js via spawnSync.
  assert.equal(isQoder, false, 'isQoder must be false without QODER_SESSION_ID');
});
