// Decodes Dan's blind labels against key.json and reports the full-vs-condensed
// result. Usage:  node decode.js labels.json
//
// Decision rule (from the handoff, fixed BEFORE the labels were seen so the
// result cannot be rationalised after the fact):
//   - full and condensed statistically indistinguishable  -> replace full with
//     condensed everywhere (one prompt, lower latency, one thing to tune)
//   - full still wins somewhere                            -> record where, ship nothing
//
// "Both marked acceptable and no better-pick" counts as an explicit TIE, which is
// evidence FOR convergence, not a missing answer.
const fs = require('fs');
const path = require('path');

const labelsPath = process.argv[2] || path.join(__dirname, 'out', 'labels.json');
const key = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', 'key.json'), 'utf8'));
const labels = JSON.parse(fs.readFileSync(labelsPath, 'utf8'));

// Group the flat `row:letter` label map back into rows.
const rows = {};
for (const [k, v] of Object.entries(labels)) {
  const i = k.lastIndexOf(':');
  const rowId = k.slice(0, i), letter = k.slice(i + 1);
  const meta = key[k];
  if (!meta) { console.log(`WARN  label for unknown key ${k} — ignored`); continue; }
  rows[rowId] = rows[rowId] || { rowId, meta: {}, cands: {} };
  rows[rowId].cands[meta.variant] = { letter, ...v };
  rows[rowId].meta = {
    modelKey: meta.modelKey, set: meta.set, caseId: meta.caseId,
    gender: meta.gender, condition: meta.condition, intensity: meta.intensity,
  };
}

const verdicts = [];
for (const r of Object.values(rows)) {
  const f = r.cands.full, c = r.cands.condensed;
  let winner;
  if (f?.best && !c?.best) winner = 'full';
  else if (c?.best && !f?.best) winner = 'condensed';
  else if (f?.acceptable && c?.acceptable) winner = 'tie-both-ok';
  else if (!f?.best && !c?.best && !f?.acceptable && !c?.acceptable) winner = 'neither';
  else winner = 'tie';
  verdicts.push({
    ...r.meta, rowId: r.rowId, winner,
    fullTags: f?.tags || [], condTags: c?.tags || [],
    fullNote: f?.note || '', condNote: c?.note || '',
    fullAcceptable: !!f?.acceptable, condAcceptable: !!c?.acceptable,
  });
}

function tally(list) {
  const t = { full: 0, condensed: 0, 'tie-both-ok': 0, tie: 0, neither: 0 };
  for (const v of list) t[v.winner]++;
  return t;
}
const line = (label, t, n) => {
  const decisive = t.full + t.condensed;
  const pct = decisive ? ` · of ${decisive} decisive rows condensed=${(100 * t.condensed / decisive).toFixed(0)}%` : '';
  console.log(`  ${label.padEnd(26)} full=${t.full} condensed=${t.condensed} tie=${t.tie + t['tie-both-ok']} neither=${t.neither}  (n=${n})${pct}`);
};

console.log(`\n=== ROUND 5: full vs condensed prompt — ${verdicts.length} labelled rows ===\n`);
const s1 = verdicts.filter((v) => v.set === 1);
const s2 = verdicts.filter((v) => v.set === 2);

console.log('OVERALL');
line('all rows', tally(verdicts), verdicts.length);
console.log('\nBY SET  (set 1 = Gemini, the leg whose prompt would change; set 2 = FLUX control)');
if (s1.length) line('set 1 — Gemini', tally(s1), s1.length);
if (s2.length) line('set 2 — FLUX (male)', tally(s2), s2.length);

console.log('\nBY SEX  (set 1 only)');
for (const g of ['male', 'female']) {
  const sub = s1.filter((v) => v.gender === g);
  if (sub.length) line(g, tally(sub), sub.length);
}
console.log('\nBY TIER  (set 1 only)');
for (const [k, lbl] of [['dramatic', 'Subtle (dramatic)'], ['max', 'Ripped (max)']]) {
  const sub = s1.filter((v) => v.intensity === k);
  if (sub.length) line(lbl, tally(sub), sub.length);
}
console.log('\nBY SEX x TIER  (set 1 only — where a regression would hide)');
for (const g of ['male', 'female']) {
  for (const k of ['dramatic', 'max']) {
    const sub = s1.filter((v) => v.gender === g && v.intensity === k);
    if (sub.length) line(`${g} ${k}`, tally(sub), sub.length);
  }
}

// The pre-registered hypothesis: condensed DROPS the no-tan guard and the
// skin-tone-preservation rule, so if it regresses anywhere it should be on tone.
console.log('\nSKIN-TONE CHECK  (the pre-registered hypothesis)');
const tagCount = (list, which, tag) =>
  list.filter((v) => (which === 'full' ? v.fullTags : v.condTags).includes(tag)).length;
for (const tag of ['too tan', 'skin tone right']) {
  console.log(`  ${tag.padEnd(20)} full=${tagCount(verdicts, 'full', tag)}  condensed=${tagCount(verdicts, 'condensed', tag)}`);
}
console.log('\nALL TAG TOTALS');
const allTags = new Set(verdicts.flatMap((v) => [...v.fullTags, ...v.condTags]));
for (const tag of [...allTags].sort()) {
  console.log(`  ${tag.padEnd(28)} full=${tagCount(verdicts, 'full', tag)}  condensed=${tagCount(verdicts, 'condensed', tag)}`);
}

console.log('\nPER-ROW');
for (const v of verdicts.sort((a, b) => a.set - b.set || a.rowId.localeCompare(b.rowId))) {
  console.log(`  [set ${v.set}] ${v.rowId.padEnd(46)} ${v.winner.toUpperCase()}`);
  if (v.fullNote) console.log(`      full:      "${v.fullNote}"`);
  if (v.condNote) console.log(`      condensed: "${v.condNote}"`);
}

// ── Decision ─────────────────────────────────────────────────────────────────
// Two-sided sign test on the decisive rows only (ties carry no directional
// information). Small n, so this bounds confidence rather than proving parity.
function signTestP(a, b) {
  const n = a + b;
  if (!n) return 1;
  const C = (n, k) => { let r = 1; for (let i = 0; i < k; i++) r = r * (n - i) / (i + 1); return r; };
  let p = 0;
  const lo = Math.min(a, b);
  for (let k = 0; k <= lo; k++) p += C(n, k) * Math.pow(0.5, n);
  return Math.min(1, 2 * p);
}
const t1 = tally(s1);
const p1 = signTestP(t1.full, t1.condensed);
console.log('\n=== DECISION (set 1, the shippable question) ===');
console.log(`  decisive rows: full=${t1.full} condensed=${t1.condensed} · two-sided sign test p=${p1.toFixed(3)}`);
const decisive1 = t1.full + t1.condensed;
const lean = decisive1 ? Math.max(t1.full, t1.condensed) / decisive1 : 0;
const leader = t1.full >= t1.condensed ? 'full' : 'condensed';
if (decisive1 === 0) {
  console.log('  -> every row tied. Strongest possible convergence signal: REPLACE full with condensed.');
} else if (p1 > 0.05 && lean >= 0.75) {
  // With n this small, p>0.05 does NOT mean parity — a 7-1 split is p=0.07 and is
  // plainly a lean, not a tie. Report the direction and refuse to call convergence.
  console.log(`  -> UNDERPOWERED, NOT converged: ${(100 * lean).toFixed(0)}% of decisive rows went to ${leader.toUpperCase()}.`);
  console.log(`     p=${p1.toFixed(3)} only because n=${decisive1} is too small to reach significance.`);
  console.log('     Do NOT read this as parity. ' + (leader === 'full'
    ? 'Full is still ahead -> ship NOTHING.'
    : 'Condensed is ahead -> gather a few more rows before replacing the prompt.'));
} else if (p1 > 0.05) {
  console.log('  -> NOT statistically distinguishable at p<0.05, and no strong lean: the variants');
  console.log('     have converged on Dan\'s eye. Handoff rule says REPLACE full with condensed');
  console.log('     everywhere — but check the BY SEX x TIER split above first: a clean sweep for');
  console.log('     full in any one cell is a real regression even when the pooled test is flat.');
} else if (t1.condensed > t1.full) {
  console.log('  -> CONDENSED wins significantly. Replace full with condensed everywhere.');
} else {
  console.log('  -> FULL still wins significantly. Ship NOTHING; record where full matters.');
}
console.log('');
