// Phase 2 — round-1 grid.
//  Primary pass : 12 cases × 6 models, each model on its designated prompt variant.
//  Variant pass : 4 representative cases × 6 models on the OTHER prompt variant,
//                 to answer "does the prompt variant matter per model?" without
//                 doubling the spend.
// Every cell is cached on disk, so a rerun after a failure never re-spends.
const fs = require('fs');
const path = require('path');
const { CASES } = require('./cases');
const { MODELS } = require('./adapters');
const { runCell } = require('./runner');

const OUT = path.join(__dirname, 'out', 'round1');
fs.mkdirSync(OUT, { recursive: true });

const VARIANT_SUBSET = ['lean-male__max', 'heavier-male__max', 'heavier-female__max', 'dan-real__max'];
const other = (v) => (v === 'full' ? 'condensed' : 'full');

const jobs = [];
for (const c of CASES) {
  for (const modelKey of Object.keys(MODELS)) {
    jobs.push({ caseObj: c, modelKey, variant: MODELS[modelKey].promptVariant, pass: 'primary' });
  }
}
for (const id of VARIANT_SUBSET) {
  const c = CASES.find((x) => x.id === id);
  for (const modelKey of Object.keys(MODELS)) {
    jobs.push({ caseObj: c, modelKey, variant: other(MODELS[modelKey].promptVariant), pass: 'variant' });
  }
}

(async () => {
  const results = [];
  let aborted = null;
  // Group by case so the 6 models fire in parallel per case (2 Google + 4 Replicate).
  const byCase = new Map();
  for (const j of jobs) {
    const k = `${j.pass}:${j.caseObj.id}`;
    if (!byCase.has(k)) byCase.set(k, []);
    byCase.get(k).push(j);
  }

  let n = 0;
  for (const [key, group] of byCase) {
    if (aborted) break;
    console.log(`\n=== ${key} (${++n}/${byCase.size})`);
    const recs = await Promise.all(group.map((j) =>
      runCell({ caseObj: j.caseObj, modelKey: j.modelKey, variant: j.variant, outDir: OUT })
        .then((r) => ({ ...r, pass: j.pass }))
        .catch((e) => ({ caseId: j.caseObj.id, modelKey: j.modelKey, variant: j.variant, ok: false, error: e.message, pass: j.pass }))
    ));
    for (const r of recs) {
      results.push(r);
      console.log(`  ${r.ok ? 'ok  ' : 'FAIL'} ${r.modelKey.padEnd(24)} ${String(r.variant).padEnd(10)} ${r.ok ? ((r.latencyMs / 1000).toFixed(1) + 's') : r.error}${r.blocked ? ' [BLOCKED]' : ''}${r.outOfCredit ? ' [402 OUT OF CREDIT]' : ''}`);
      if (r.outOfCredit) aborted = 'Replicate returned 402 — out of credit';
    }
    fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify(results, null, 2));
    await new Promise((r) => setTimeout(r, 1500));
  }

  const okCount = results.filter((r) => r.ok).length;
  const cost = results.reduce((s, r) => s + (r.nominalCost || 0), 0);
  console.log(`\nDONE ${okCount}/${results.length} images, nominal spend ~$${cost.toFixed(2)}`);
  if (aborted) console.log(`ABORTED: ${aborted}`);
})();
