const fs = require('node:fs');
const assert = require('node:assert/strict');

for (const file of ['README.md', 'Student-Lab.md']) {
  const content = fs.readFileSync(file, 'utf8');
  for (const [, target] of content.matchAll(/\]\(([^)]+)\)/g)) {
    if (!/^(https?:|#)/.test(target)) {
      assert.ok(fs.existsSync(target), `Missing ${target} in ${file}`);
    }
  }
}
assert.equal(fs.readFileSync('Week10-Slides.pptx').subarray(0, 4).toString('hex'), '504b0304');
console.log('Handout links and PowerPoint package verified.');
