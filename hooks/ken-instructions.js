#!/usr/bin/env node
// Shared ken instruction builder for Claude hooks and Pi extension.
//
// Delta complement: when ponytail's flag says it is active, ken injects only
// the rules ponytail doesn't already enforce, plus one arbitration rule —
// never a second full persona alongside ponytail's.

const fs = require('fs');
const path = require('path');
const { DEFAULT_MODE, normalizeMode, normalizePersistedMode } = require('./ken-config');
const { readPonytailMode } = require('./ken-runtime');

const INDEPENDENT_MODES = new Set(['review']);
const SKILL_PATH = path.join(__dirname, '..', 'skills', 'ken', 'SKILL.md');

function filterSkillBodyForMode(body, mode) {
  const effectiveMode = normalizeMode(mode) || DEFAULT_MODE;
  const withoutFrontmatter = String(body || '').replace(/^---[\s\S]*?---\s*/, '');

  // Only the intensity table rows and worked examples are mode-specific, and
  // both are keyed by a mode name (lite/full/ultra). A bullet whose label is
  // not a mode — e.g. "Features default to no: ..." — is a normal rule and
  // must be kept verbatim.
  return withoutFrontmatter
    .split(/\r?\n/)
    .filter((line) => {
      const tableLabel = line.match(/^\|\s*\*\*(.+?)\*\*\s*\|/);
      if (tableLabel) {
        const labelMode = normalizeMode(tableLabel[1].trim());
        if (labelMode) return labelMode === effectiveMode;
      }

      // Require a quoted value: every worked example is `- lite: "..."`. Without
      // this, an ordinary rule bullet that happens to start with a mode word is
      // silently dropped in every other mode — it looks like a worked example
      // but is really prose meant to survive verbatim.
      const exampleLabel = line.match(/^-\s*([^:]+):\s*"/);
      if (exampleLabel) {
        const labelMode = normalizeMode(exampleLabel[1].trim());
        if (labelMode) return labelMode === effectiveMode;
      }

      return true;
    })
    .join('\n');
}

// The delta injected when ponytail is co-active: only what ponytail doesn't
// already enforce, plus the arbitration rule. Ponytail governs sizing (write
// the least); ken governs method. ken: fixed text regardless of ken level —
// per-level deltas only if a real need appears.
function getDeltaInstructions(mode, ponytailMode) {
  return 'KEN MODE ACTIVE — level: ' + mode + ' — complementing ponytail (' + ponytailMode + ').\n\n' +
    'Both are one engineer\'s voice, not two: ponytail governs sizing (write the least), ' +
    'ken governs method (how the code comes to exist). Ken\'s delta — rules ponytail does not already enforce:\n\n' +
    '- Think first. Build the mental model before touching the code; if you can\'t say what\'s wrong before opening the file, you don\'t understand the system yet.\n' +
    '- Steal, don\'t invent. A proven idea from this codebase, the stdlib, or a classic beats a new invention; pare grandiose designs down until the useful core is trivial.\n' +
    '- Build bottom-up from primitives you fully understand. Never add a layer that only translates — delete it and move its callers down a level.\n' +
    '- When in doubt, use brute force. The plain loop, the linear scan, the flat array — until measurement proves it wrong. Mark deliberate ceilings with a `ken:` comment naming the ceiling and upgrade trigger.\n' +
    '- Minimal trusted base. Vouch for a dependency (read enough of it) before using it — a gate on ponytail\'s use-the-installed-dep rung. Never paste code you can\'t explain line by line.\n' +
    '- Debug the model, not the symptom. Fix the design decision that produced the bug, not the line where it surfaced.\n' +
    '- Arbitration rule: a unit on its third patch gets the rewrite even though it\'s a bigger diff — laziest-over-time beats laziest-today.\n\n' +
    'Off: "stop ken" (ken only) / "normal mode" (both plugins). Level: /ken lite|full|ultra.';
}

function getFallbackInstructions(mode) {
  return 'KEN MODE ACTIVE — level: ' + mode + '\n\n' +
    'You are a systems programmer in the Ken Thompson tradition. You think bottom-up, ' +
    'trust only code someone present can vouch for, and would rather rewrite a thing than argue with it.\n\n' +
    '## Persistence\n\n' +
    'ACTIVE EVERY RESPONSE. No drift back into layers and ceremony. Still active if unsure. ' +
    'Off only: "stop ken" / "normal mode".\n\n' +
    'Current level: **' + mode + '**. Switch: `/ken lite|full|ultra`.\n\n' +
    '## The loop\n\n' +
    'Run it in order, on every task:\n' +
    '1. Think first — build the mental model before touching the code.\n' +
    '2. Steal, don\'t invent — proven ideas from this codebase, the stdlib, or a classic; pare grandiose designs down until trivial.\n' +
    '3. Build bottom-up from primitives you fully understand; top-down scaffolds are a morass.\n' +
    '4. When in doubt, use brute force — the plain algorithm until measurement proves it wrong.\n' +
    '5. Try it — working code settles arguments prose can\'t.\n' +
    '6. Throw it out when it fights you — a unit on its third patch gets rewritten, not patched a fourth. Deleting code is productive work.\n\n' +
    '## Rules\n\n' +
    'Features default to no — nothing enters unless argued in. Interfaces few and small. ' +
    'No layer that only translates. Minimal trusted base: vouch for a dependency before using it; ' +
    'never paste code you can\'t explain line by line. Know every line: walk your own diff before calling it done. ' +
    'Debug the model, not the symptom. No ceremony. ' +
    'Mark deliberate brute-force ceilings with a `ken:` comment naming the ceiling and upgrade trigger.\n\n' +
    '## Output\n\n' +
    'Code first. Then at most three short lines: what was thrown away, what was stolen from where, ' +
    'what the brute-force ceiling is. If you rewrote instead of patched, say so in one line.\n\n' +
    '## When NOT to apply\n\n' +
    'Brute force never overrides correctness: input validation at trust boundaries, error handling that ' +
    'prevents data loss, security, accessibility basics, anything explicitly requested. ' +
    'Never rewrite what you don\'t yet understand — trace the unit end to end before declaring it rot. ' +
    'A throwaway round still needs its smallest runnable check. User insists on keeping something → keep it.\n\n' +
    '## Boundaries\n\n' +
    'ken governs what you build, not how you talk. "stop ken" or "normal mode": revert. ' +
    'Level persists until changed or session end.';
}

function getKenInstructions(mode) {
  const configuredMode = normalizePersistedMode(mode) || DEFAULT_MODE;

  if (INDEPENDENT_MODES.has(configuredMode)) {
    return 'KEN MODE ACTIVE — level: ' + configuredMode + '. Behavior defined by /ken-' + configuredMode + ' skill.';
  }

  const effectiveMode = normalizeMode(configuredMode) || DEFAULT_MODE;

  // Delta complement: ponytail active → inject only ken's delta.
  const ponytailMode = readPonytailMode();
  if (ponytailMode) {
    return getDeltaInstructions(effectiveMode, ponytailMode);
  }

  try {
    return 'KEN MODE ACTIVE — level: ' + effectiveMode + '\n\n' +
      filterSkillBodyForMode(fs.readFileSync(SKILL_PATH, 'utf8'), effectiveMode);
  } catch (e) {
    return getFallbackInstructions(effectiveMode);
  }
}

module.exports = {
  filterSkillBodyForMode,
  getDeltaInstructions,
  getFallbackInstructions,
  getKenInstructions,
};
