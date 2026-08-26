#!/usr/bin/env node
// Smoke test for the Copilot plugin adapter: keep command wiring minimal and
// ensure the debt command is part of the shared command surface.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const REQUIRED_COMMAND_FILES = [
  'ken.toml',
  'ken-review.toml',
  'ken-audit.toml',
  'ken-debt.toml',
  'ken-gain.toml',
  'ken-help.toml',
];

function readJSON(relPath) {
  return JSON.parse(fs.readFileSync(path.join(root, relPath), 'utf8'));
}

test('copilot plugin command directory includes ken-debt', () => {
  const manifest = readJSON('.github/plugin/plugin.json');
  assert.equal(manifest.name, 'ken');
  assert.equal(manifest.commands, 'commands/');

  for (const file of REQUIRED_COMMAND_FILES) {
    assert.ok(
      fs.existsSync(path.join(root, manifest.commands, file)),
      `missing command file: ${manifest.commands}${file}`,
    );
  }
});
