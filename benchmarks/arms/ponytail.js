// Ponytail arm: DietrichGebert/ponytail SKILL.md (MIT) as the system prompt,
// vendored at arms/ponytail-SKILL.md so runs are reproducible without the
// ponytail repo present. The comparison arm ken must justify itself against.
const fs = require('fs');
const path = require('path');
const system = fs.readFileSync(path.join(__dirname, 'ponytail-SKILL.md'), 'utf8');
module.exports = ({ vars }) => [
  { role: 'system', content: system },
  { role: 'user', content: vars.task },
];
