// Combined arm: ponytail's full SKILL.md plus ken's delta — exactly what a
// real session injects when both plugins are active (ponytail's SessionStart
// emits its full persona; ken detects the flag and adds only its delta). The
// delta comes from the real hooks module, so this arm can never drift from
// what sessions actually receive.
const fs = require('fs');
const path = require('path');
const { getDeltaInstructions } = require('../../hooks/ken-instructions');
const ponytail = fs.readFileSync(path.join(__dirname, 'ponytail-SKILL.md'), 'utf8');
const system = ponytail + '\n\n' + getDeltaInstructions('full', 'full');
module.exports = ({ vars }) => [
  { role: 'system', content: system },
  { role: 'user', content: vars.task },
];
