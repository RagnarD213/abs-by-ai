#!/usr/bin/env node
// Macro-tracker eval harness.
//
// Measures estimation bias of /api/analyze-meal against weighed ground truth.
//
// Setup: create a folder of meal cases. Each case is a photo plus a truth
// file with the same basename:
//
//   eval/meals/chicken-rice.jpg
//   eval/meals/chicken-rice.json      ← weighed truth:
//     { "calories": 620, "protein_g": 48, "carbs_g": 55, "fat_g": 18,
//       "note": "optional note passed to the analyzer, e.g. '200g chicken'" }
//
// "note" is optional — omit it to test pure photo estimation. Truth macros
// other than calories are optional too; missing ones are skipped in stats.
//
// Run:
//   node eval/meal-eval.js eval/meals                 # against prod
//   BACKEND_URL=http://localhost:3000 node eval/meal-eval.js eval/meals
//
// Output: per-meal table + aggregate bias (mean signed % error), MAE %, and
// hit-rate within ±15%, for calories and each macro. A consistent signed bias
// is fixable via the server's calibration factor; a wide MAE is noise.

const fs = require('fs');
const path = require('path');

const BACKEND_URL = process.env.BACKEND_URL || 'https://absbyai.com';
const dir = process.argv[2];
if (!dir) { console.error('Usage: node eval/meal-eval.js <folder-of-photo+json-pairs>'); process.exit(1); }

const MIMES = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };
const FIELDS = ['calories', 'protein_g', 'carbs_g', 'fat_g'];

async function analyzeCase(photoPath, truth) {
  const ext = path.extname(photoPath).toLowerCase();
  const body = {
    photoBase64: fs.readFileSync(photoPath).toString('base64'),
    photoMime: MIMES[ext],
    note: truth.note || undefined,
    deviceId: 'eval-harness', // excluded from real users; free-tier counting applies
  };
  const res = await fetch(`${BACKEND_URL}/api/analyze-meal`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(process.env.EVAL_AUTH_TOKEN ? { Authorization: `Bearer ${process.env.EVAL_AUTH_TOKEN}` } : {}),
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  if (!data.isFood) throw new Error('model said not food');
  return data.totals;
}

function pctErr(est, truth) { return truth > 0 ? ((est - truth) / truth) * 100 : null; }

(async () => {
  const files = fs.readdirSync(dir).filter(f => MIMES[path.extname(f).toLowerCase()]);
  if (!files.length) { console.error(`No photos found in ${dir}`); process.exit(1); }

  const rows = [];
  const errs = Object.fromEntries(FIELDS.map(f => [f, []]));

  for (const f of files) {
    const base = f.slice(0, -path.extname(f).length);
    const truthPath = path.join(dir, base + '.json');
    if (!fs.existsSync(truthPath)) { console.warn(`skip ${f}: no ${base}.json`); continue; }
    const truth = JSON.parse(fs.readFileSync(truthPath, 'utf8'));
    process.stdout.write(`analyzing ${base}... `);
    try {
      const est = await analyzeCase(path.join(dir, f), truth);
      const row = { meal: base };
      for (const field of FIELDS) {
        if (typeof truth[field] !== 'number') continue;
        const estVal = Math.round(est[field]); // totals keys: calories, protein_g, carbs_g, fat_g
        const e = pctErr(estVal, truth[field]);
        row[field] = `${estVal}/${truth[field]} (${e >= 0 ? '+' : ''}${e.toFixed(0)}%)`;
        errs[field].push(e);
      }
      rows.push(row);
      console.log('ok');
    } catch (e) {
      rows.push({ meal: base, error: e.message });
      console.log(`FAILED: ${e.message}`);
    }
  }

  console.log('\nPer-meal (estimated/truth):');
  console.table(rows);

  console.log('Aggregate:');
  for (const field of FIELDS) {
    const e = errs[field];
    if (!e.length) continue;
    const mean = e.reduce((a, b) => a + b, 0) / e.length;
    const mae = e.reduce((a, b) => a + Math.abs(b), 0) / e.length;
    const within15 = (e.filter(x => Math.abs(x) <= 15).length / e.length) * 100;
    console.log(
      `  ${field.padEnd(10)} n=${e.length}  bias ${mean >= 0 ? '+' : ''}${mean.toFixed(1)}%  ` +
      `MAE ${mae.toFixed(1)}%  within ±15%: ${within15.toFixed(0)}%`
    );
  }
  console.log('\nA consistent bias (e.g. +20% calories) → adjust the calibration factor in server.js.');
})();
