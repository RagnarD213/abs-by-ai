// Offline joint weight sweep: can any composite-weight setting fix the female
// misses WITHOUT dropping the male held-out eval below 80%? Reads the saved
// rubric scores from both evals — no API calls, $0, freely re-runnable.
//
// Also sweeps an extra `overPenalty` dimension (penalty per point of change
// above 4) that the shipped composite does not have, to test whether a
// "too much change" penalty — the exact complaint behind the female Subtle
// misses — could be principled rather than score-chasing.
const fs = require('fs');
const path = require('path');

const male = JSON.parse(fs.readFileSync(path.join(__dirname, 'round1/judge-v2-claude-sonnet-5.json'), 'utf8'));
const female = JSON.parse(fs.readFileSync(path.join(__dirname, 'judge-v2-female-claude-sonnet-5.json'), 'utf8'));
const EXEMPLARS = ['dan-real__dramatic', 'moderate-male__max', 'heavier-female__max'];

const comp = (m, w) =>
  w.definition * m.definition
  + w.skin * m.skin_tone
  + w.photoreal * m.photoreal
  + w.change * m.change
  - w.bulkPenalty * Math.max(0, m.bulk - 3)
  - w.underPenalty * Math.max(0, 3 - m.change)
  - (w.overPenalty || 0) * Math.max(0, m.change - 4)
  - (m.identity === 'borderline' ? w.borderlineId : 0)
  - (m.identity === 'broken' ? 100 : 0);

function pairwise(results, w, keep = () => true) {
  let s = 0, n = 0;
  for (const r of results) {
    if (!keep(r)) continue;
    n++;
    if (!r.scores) { s += 0.5; continue; }
    const b = r.scores.find((x) => x.letter === r.bestLetter);
    const o = r.scores.find((x) => x.letter === r.otherLetter);
    if (!b && !o) { s += 0.5; continue; }
    if (!o) { s += 1; continue; }
    if (!b) continue;
    const cb = comp(b, w), co = comp(o, w);
    s += cb > co ? 1 : cb === co ? 0.5 : 0;
  }
  return n ? s / n : 0;
}

const maleHeldOut = (r) => !EXEMPLARS.includes(r.caseId);
const SHIPPED = { definition: 2.0, skin: 1.0, photoreal: 1.0, change: 0.6, bulkPenalty: 2.5, underPenalty: 1.5, borderlineId: 2.0, overPenalty: 0 };

console.log('SHIPPED weights:');
console.log(`  male held-out ${(pairwise(male.pairResults, SHIPPED, maleHeldOut) * 100).toFixed(1)}%   female all-14 ${(pairwise(female.pairResults, SHIPPED) * 100).toFixed(1)}%   female Subtle ${(pairwise(female.pairResults, SHIPPED, (r) => r.intensity === 'dramatic') * 100).toFixed(1)}%\n`);

const rows = [];
for (const definition of [1.0, 1.5, 2.0, 2.5, 3.0, 4.0])
  for (const skin of [0, 0.5, 1.0, 1.5, 2.0])
    for (const photoreal of [0, 0.5, 1.0, 1.5])
      for (const bulkPenalty of [0, 1.0, 2.5, 4.0])
        for (const change of [0, 0.6, 1.2])
          for (const underPenalty of [0, 1.5, 3.0])
            for (const overPenalty of [0, 1.5, 3.0, 6.0]) {
              const w = { definition, skin, photoreal, change, bulkPenalty, underPenalty, borderlineId: 2.0, overPenalty };
              rows.push({
                w,
                maleH: pairwise(male.pairResults, w, maleHeldOut),
                fem: pairwise(female.pairResults, w),
                femSub: pairwise(female.pairResults, w, (r) => r.intensity === 'dramatic'),
              });
            }

console.log(`settings evaluated: ${rows.length}`);
const ok = rows.filter((r) => r.maleH >= 0.8);
ok.sort((x, y) => y.fem - x.fem || y.femSub - x.femSub);
console.log(`settings keeping male held-out >= 80%: ${ok.length}`);
console.log('\nBest female agreement among male-safe settings:');
for (const r of ok.slice(0, 5)) {
  console.log(`  female ${(r.fem * 100).toFixed(1)}%  (Subtle ${(r.femSub * 100).toFixed(1)}%)  male ${(r.maleH * 100).toFixed(1)}%  ${JSON.stringify(r.w)}`);
}
const bestAny = [...rows].sort((x, y) => y.fem - x.fem)[0];
console.log(`\nBest female agreement anywhere (ignoring male): ${(bestAny.fem * 100).toFixed(1)}% (Subtle ${(bestAny.femSub * 100).toFixed(1)}%, male ${(bestAny.maleH * 100).toFixed(1)}%)  ${JSON.stringify(bestAny.w)}`);
