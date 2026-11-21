// Per-model tallies for the round-1 grid: success/block rate (split male vs
// female), latency, and nominal spend.
const fs = require('fs');
const path = require('path');
const { CASES } = require('./cases');
const { MODELS } = require('./adapters');

const results = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', 'round1', 'results.json'), 'utf8'));
const caseById = Object.fromEntries(CASES.map((c) => [c.id, c]));

const rows = [];
for (const m of Object.keys(MODELS)) {
  const cells = results.filter((r) => r.modelKey === m);
  const male = cells.filter((r) => caseById[r.caseId]?.gender === 'male');
  const female = cells.filter((r) => caseById[r.caseId]?.gender === 'female');
  const lat = cells.filter((r) => r.ok).map((r) => r.latencyMs).sort((a, b) => a - b);
  rows.push({
    model: m,
    ok: `${cells.filter((r) => r.ok).length}/${cells.length}`,
    male_ok: `${male.filter((r) => r.ok).length}/${male.length}`,
    female_ok: `${female.filter((r) => r.ok).length}/${female.length}`,
    blocked: cells.filter((r) => r.blocked).length,
    other_fail: cells.filter((r) => !r.ok && !r.blocked).length,
    median_s: lat.length ? (lat[Math.floor(lat.length / 2)] / 1000).toFixed(1) : '—',
    max_s: lat.length ? (lat[lat.length - 1] / 1000).toFixed(1) : '—',
    nominal_$: cells.reduce((s, r) => s + (r.nominalCost || 0), 0).toFixed(2),
  });
}
console.table(rows);
const errs = results.filter((r) => !r.ok);
if (errs.length) {
  console.log('\nFailures:');
  for (const e of errs) console.log(` ${e.caseId} · ${e.modelKey} · ${e.variant} → ${e.blocked ? '[BLOCKED] ' : ''}${e.error}`);
}
console.log(`\nTotal nominal spend: $${results.reduce((s, r) => s + (r.nominalCost || 0), 0).toFixed(2)} over ${results.filter((r) => r.ok).length} images`);
