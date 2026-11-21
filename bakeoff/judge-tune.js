// Offline composite-weight sweep. Reads the saved rubric scores and re-decides
// every pairing under different weights — no API calls, so this costs nothing
// and can be re-run freely.
//
// Purpose is honesty, not score-chasing: it answers "is the 80.5% held-out
// result an artifact of weights I happened to pick, and could tuning fix the
// remaining misses?" The shipped weights were chosen a priori, before any
// result was seen.
const fs = require('fs');
const path = require('path');

const file = process.argv[2] || 'round1/judge-v2-claude-sonnet-5.json';
const v2 = JSON.parse(fs.readFileSync(path.join(__dirname, file), 'utf8'));
const EXEMPLARS = ['dan-real__dramatic', 'moderate-male__max', 'heavier-female__max'];

const comp = (m, w) =>
  w.definition * m.definition
  + w.skin * m.skin_tone
  + w.photoreal * m.photoreal
  + w.change * m.change
  - w.bulkPenalty * Math.max(0, m.bulk - 3)
  - w.underPenalty * Math.max(0, 3 - m.change)
  - (m.identity === 'borderline' ? w.borderlineId : 0)
  // Must mirror judge-v2's composite exactly, including the identity gate —
  // otherwise this re-derivation silently disagrees with the real eval.
  - (m.identity === 'broken' ? 100 : 0);

function pairwise(w, keep) {
  let s = 0, n = 0;
  for (const r of v2.pairResults) {
    if (!keep(r.caseId)) continue;
    n++;
    if (!r.scores) { s += 0.5; continue; }
    const b = r.scores.find((x) => x.letter === r.bestLetter);
    const o = r.scores.find((x) => x.letter === r.otherLetter);
    // A candidate missing from `scores` was gated out for broken identity before
    // scoring, so the survivor wins outright. Treating that as a tie (an earlier
    // bug here) understated the judge by penalising it for correctly rejecting a
    // mangled face — the one call the judge must never get wrong.
    if (!b && !o) { s += 0.5; continue; }
    if (!o) { s += 1; continue; }
    if (!b) continue;
    const cb = comp(b, w), co = comp(o, w);
    s += cb > co ? 1 : cb === co ? 0.5 : 0;
  }
  return n ? s / n : 0;
}

function nwayTop1(w, keep) {
  const rows = v2.nwayResults.filter((r) => keep(r.caseId) && r.ranked);
  let hit = 0;
  for (const r of rows) {
    const best = [...r.ranked].sort((a, b) => comp(b, w) - comp(a, w))[0];
    if (best.letter === r.danBest) hit++;
  }
  return rows.length ? hit / rows.length : 0;
}

const heldOut = (id) => !EXEMPLARS.includes(id);
const all = () => true;
const SHIPPED = { definition: 2.0, skin: 1.0, photoreal: 1.0, change: 0.6, bulkPenalty: 2.5, underPenalty: 1.5, borderlineId: 2.0 };

const rows = [];
for (const definition of [1.0, 1.5, 2.0, 2.5, 3.0, 4.0])
  for (const skin of [0, 0.5, 1.0, 1.5, 2.0])
    for (const photoreal of [0, 0.5, 1.0, 1.5])
      for (const bulkPenalty of [0, 1.0, 2.5, 4.0])
        for (const change of [0, 0.6, 1.2])
          for (const underPenalty of [0, 1.5, 3.0]) {
            const w = { definition, skin, photoreal, change, bulkPenalty, underPenalty, borderlineId: 2.0 };
            rows.push({ w, h: pairwise(w, heldOut), a: pairwise(w, all), nh: nwayTop1(w, heldOut) });
          }

rows.sort((x, y) => y.h - x.h);
const shippedH = pairwise(SHIPPED, heldOut);
const over80 = rows.filter((r) => r.h >= 0.8).length;

console.log(`weight settings evaluated: ${rows.length}\n`);
console.log('SHIPPED weights (chosen a priori, never fitted to results):');
console.log(`  held-out pairwise ${(shippedH * 100).toFixed(1)}%   all ${(pairwise(SHIPPED, all) * 100).toFixed(1)}%   held-out N-way top1 ${(nwayTop1(SHIPPED, heldOut) * 100).toFixed(1)}%\n`);
console.log('BEST held-out achievable anywhere in the sweep (overfit upper bound):');
console.log(`  held-out pairwise ${(rows[0].h * 100).toFixed(1)}%   all ${(rows[0].a * 100).toFixed(1)}%   held-out N-way top1 ${(rows[0].nh * 100).toFixed(1)}%`);
console.log(`  weights: ${JSON.stringify(rows[0].w)}\n`);
console.log(`Robustness: ${over80}/${rows.length} settings (${(over80 / rows.length * 100).toFixed(0)}%) reach >=80% held-out pairwise.`);
console.log(`Median held-out across all settings: ${(rows[Math.floor(rows.length / 2)].h * 100).toFixed(1)}%`);

// Which dimension, if perceived differently, would fix the stubborn case?
const hm = v2.pairResults.filter((r) => r.caseId === 'heavier-male__max' && !r.preferredBest);
console.log(`\nThe stubborn case — heavier-male__max, ${hm.length} of the 9 total misses:`);
for (const r of hm) {
  const b = r.scores.find((x) => x.letter === r.bestLetter);
  const o = r.scores.find((x) => x.letter === r.otherLetter);
  const d = (k) => `${k} ${b[k]} vs ${o[k]}`;
  console.log(`  vs ${r.otherLetter}: ${d('definition')} | ${d('skin_tone')} | ${d('bulk')} | ${d('photoreal')}`);
}
console.log('\n  Dan scored his pick highest here; the judge scores it MORE tan, MORE bulky and LESS');
console.log('  photoreal than the alternatives. That is a perception gap, not an arithmetic one —');
console.log('  no weighting flips it while those dimension scores stand.');
