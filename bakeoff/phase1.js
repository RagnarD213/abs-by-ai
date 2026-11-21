// Phase 1 — verify every adapter returns one image on the lean-male proof photo
// at Ripped intensity, using each model's designated prompt variant.
const fs = require('fs');
const path = require('path');
const { CASES } = require('./cases');
const { MODELS } = require('./adapters');
const { runCell } = require('./runner');

const OUT = path.join(__dirname, 'out', 'phase1');
fs.mkdirSync(OUT, { recursive: true });

const caseObj = CASES.find((c) => c.id === 'lean-male__max');

(async () => {
  const results = [];
  for (const modelKey of Object.keys(MODELS)) {
    const variant = MODELS[modelKey].promptVariant;
    process.stdout.write(`→ ${modelKey} (${variant}) ... `);
    const rec = await runCell({ caseObj, modelKey, variant, outDir: OUT });
    results.push(rec);
    console.log(rec.ok
      ? `OK ${(rec.latencyMs / 1000).toFixed(1)}s`
      : `FAIL ${rec.error}${rec.blocked ? ' [blocked]' : ''}${rec.outOfCredit ? ' [402 OUT OF CREDIT]' : ''}${rec.throttled ? ' [429 throttled]' : ''}`);
    await new Promise((r) => setTimeout(r, 3000));
  }
  fs.writeFileSync(path.join(OUT, 'summary.json'), JSON.stringify(results, null, 2));
  const okCount = results.filter((r) => r.ok).length;
  console.log(`\n${okCount}/${results.length} adapters returned an image`);
})();
