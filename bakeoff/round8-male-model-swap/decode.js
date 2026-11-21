// Decodes Dan's blind labels against out/key.json and applies the PRE-REGISTERED
// four-part bar from AI_COORDINATION.md verbatim. Zero API calls.
//
// Bar (a) is the only one decided here — (b) coverage and (c) latency were
// measured by run.js and are re-read from the per-cell records so the verdict is
// computed from data, never from memory of what the numbers were.
const fs = require('fs');
const path = require('path');
const { CASES, ARMS } = require('./cases');

const OUT = path.join(__dirname, 'out');
const key = JSON.parse(fs.readFileSync(path.join(OUT, 'key.json'), 'utf8'));
const labels = JSON.parse(fs.readFileSync(path.join(OUT, 'labels.json'), 'utf8'));

const models = ARMS.map((a) => a.modelKey);
const label = Object.fromEntries(ARMS.map((a) => [a.modelKey, a.label]));
const blank = () => Object.fromEntries(models.map((m) => [m, 0]));
const best = blank(), acc = blank(), rejected = blank();
const tags = Object.fromEntries(models.map((m) => [m, {}]));

const rows = [...new Set(Object.keys(key).map((k) => k.split(':')[0]))].sort();
const perRow = {};

for (const k of Object.keys(key)) {
  const [rowId, letter] = k.split(':');
  const mk = key[k].modelKey;
  const l = labels[k] || { best: false, acceptable: false, tags: [] };
  if (l.best) { best[mk]++; (perRow[rowId] = perRow[rowId] || {}).best = mk; }
  if (l.acceptable) acc[mk]++;
  if (!l.best && !l.acceptable) rejected[mk]++;
  for (const t of l.tags || []) tags[mk][t] = (tags[mk][t] || 0) + 1;
  ((perRow[rowId] = perRow[rowId] || {}).cells = perRow[rowId].cells || {})[mk] =
    l.best ? 'BEST' : l.acceptable ? 'acceptable' : 'rejected';
}

// ── Per-row decode ──────────────────────────────────────────────────────────
console.log('\n=== ROW BY ROW (decoded) ===\n');
for (const rowId of rows) {
  const r = perRow[rowId];
  console.log(rowId);
  for (const m of models) {
    const flag = r.cells[m] === 'BEST' ? ' <-- BEST' : '';
    console.log(`   ${r.cells[m].padEnd(11)} ${label[m]}${flag}`);
  }
  if (!r.best) console.log('   (no best pick in this row)');
  console.log('');
}

// ── Bar (a) ─────────────────────────────────────────────────────────────────
console.log('=== BAR (a) LOOKS — best picks out of 6 rows ===');
console.log('   pre-registered: a candidate must produce a best pick in MORE THAN 1 of 6 rows.');
console.log('   baselines to beat: Gemini scored 1 of 6 (round 5) and 0 of 6 (round 6).\n');
const rowsWithAnyBest = rows.filter((r) => perRow[r].best).length;
for (const m of models) {
  const pass = best[m] > 1;
  console.log(`   ${String(best[m])} best · ${acc[m]} acceptable · ${rejected[m]} rejected   ${label[m]}   ${m === 'gemini-2.5-flash-image' ? '(BASELINE)' : pass ? 'PASSES (a)' : 'fails (a)'}`);
}
console.log(`\n   rows with any best pick: ${rowsWithAnyBest} of ${rows.length}`);

// ── Tags ────────────────────────────────────────────────────────────────────
console.log('\n=== TAGS BY MODEL ===');
for (const m of models) {
  const t = Object.entries(tags[m]).sort((a, b) => b[1] - a[1]);
  console.log(`   ${label[m]}`);
  console.log(`      ${t.length ? t.map(([k, v]) => `${k} x${v}`).join(' · ') : '(none)'}`);
}

// ── Bars (b) and (c), re-read from the recorded cells ───────────────────────
console.log('\n=== BARS (b) COVERAGE and (c) LATENCY — from run records ===');
for (const arm of ARMS) {
  const recs = CASES.map((c) => {
    const p = arm.baseline
      ? path.join(__dirname, '..', 'round5-prompt-ab', 'out', `${c.id}__${arm.modelKey}__${arm.reuseSuffix}.json`)
      : path.join(OUT, `${c.id}__${arm.modelKey}.json`);
    return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8')) : null;
  }).filter(Boolean);
  const blocks = recs.filter((r) => r.blocked).length;
  const retries = recs.filter((r) => r.safetyRetry || r.geminiSafetyRetry).length;
  const ms = recs.map((r) => r.latencyMs).filter(Boolean).sort((a, b) => a - b);
  const med = ms.length ? ms[Math.floor(ms.length / 2)] / 1000 : 0;
  console.log(`   ${label[arm.modelKey]}`);
  console.log(`      ok ${recs.filter((r) => r.ok).length}/${recs.length} · blocks ${blocks} · safety-retries ${retries} · median ${med.toFixed(1)}s · (b) ${blocks === 0 && retries === 0 ? 'PASS' : 'CHECK'} · (c) ${med < 25 ? 'PASS' : 'FAIL'}`);
}

// ── Bar (d) ─────────────────────────────────────────────────────────────────
console.log('\n=== BAR (d) ANCHOR-ROLE COMPATIBILITY ===');
for (const arm of ARMS) {
  const ok = arm.variant === 'full';
  console.log(`   ${label[arm.modelKey]}: ${ok ? 'PASS — takes the full prompt, drop-in anchor' : 'CONDITIONAL — condensed-only (4000-char ceiling), shipping it needs a conscious anchor re-architecture'}`);
}

// ── Verdict ─────────────────────────────────────────────────────────────────
console.log('\n=== VERDICT ===');
const winners = models.filter((m) => m !== 'gemini-2.5-flash-image' && best[m] > 1);
if (!winners.length) {
  console.log('   NO candidate clears bar (a). Pre-registered outcome: SHIP NOTHING.');
} else {
  const top = winners.sort((a, b) => best[b] - best[a] || acc[b] - acc[a])[0];
  console.log(`   Candidates clearing (a): ${winners.map((m) => `${label[m]} (${best[m]})`).join(', ')}`);
  console.log(`   Leading candidate: ${label[top]} — ${best[top]} best, ${acc[top]} acceptable, ${rejected[top]} rejected`);
  console.log(`   Baseline it must replace: ${label['gemini-2.5-flash-image']} — ${best['gemini-2.5-flash-image']} best, ${acc['gemini-2.5-flash-image']} acceptable, ${rejected['gemini-2.5-flash-image']} rejected`);
}
