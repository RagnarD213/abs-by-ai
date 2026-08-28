// Per-shot treatment plan for the supplements Shorts.
//
// ONE TREATMENT, `talk`. The source is our own clean master - a single locked kitchen camera
// with no burned graphics anywhere - so there is nothing to preserve whole, nothing to slice,
// and no card/pip/extern case. (Cutting from the DELIVERED master instead would have been a
// different job: the 8/27 rebuild took it to 43% insert coverage, so nearly half of every
// short would have been a full-frame graphic forced into a card.)
//
// ⚠ THERE IS NO TALK_X, DELIBERATELY. A single batch-wide centre is exactly what shipped 10
// off-centre Shorts on 2026-08-27, caught by Dan on v2-short3. Every `x` below is a MEASURED
// torso-block centre (Apple Vision person segmentation, median over 6 frames of that beat),
// and the shot list is cut on the source EDL's own splices, so each take Dan stood slightly
// differently for gets its own value.
//
// ⚠ AND THE MEASUREMENT OVERTURNED THE ESTIMATE. The handoff put him at x 0.60-0.63 from
// frame grabs; Vision says 0.6676-0.6969. That is 129px of source, ~192px in the delivered
// frame - i.e. building to the estimate would have reproduced the exact fault this batch
// exists to avoid.
//
// The spread across beats is 56px of source / 84px delivered, which is above the ~35px
// "invisible" threshold, so the per-beat values genuinely matter. Within a beat his sway is
// only 7-21px, so a per-beat CONSTANT is enough and no pan is needed - a pan on a locked
// tripod reads as a mistake.
//
// Silhouette containment was checked against every window: 18 of 20 shots clip nothing at
// all, and the other two clip a gesturing hand by 27-33px of source on one sampled frame.
// That is normal in a vertical talking head and is not what Dan flagged - his complaint was
// asymmetry ("one of my arms is cut off and there's space on the other side"), which
// centring on the torso is what fixes.
const path = require('path');
const fs = require('fs');
const { SEGMENTS } = require('./segments.js');

const SHOTS = {
  // ---- B ----------------------------------------------------------------
  'B-p0-s00': { t: 'talk', x: 0.6871 },

  // ---- A ----------------------------------------------------------------
  'A-p0-s00': { t: 'talk', x: 0.6707 },
  'A-p1-s00': { t: 'talk', x: 0.6707 },
  'A-p2-s00': { t: 'talk', x: 0.6750 },

  // ---- E ----------------------------------------------------------------
  'E-p0-s00': { t: 'talk', x: 0.6848 },

  // ---- D ----------------------------------------------------------------
  'D-p0-s00': { t: 'talk', x: 0.6871 },
  'D-p0-s01': { t: 'talk', x: 0.6969 },

  // ---- C ----------------------------------------------------------------
  'C-p0-s00': { t: 'talk', x: 0.6730 },
  'C-p0-s01': { t: 'talk', x: 0.6852 },

  // ---- J ----------------------------------------------------------------
  'J-p0-s00': { t: 'talk', x: 0.6699 },
  'J-p1-s00': { t: 'talk', x: 0.6676 },
  'J-p1-s01': { t: 'talk', x: 0.6676 },

  // ---- M ----------------------------------------------------------------
  'M-p0-s00': { t: 'talk', x: 0.6816 },
  'M-p0-s01': { t: 'talk', x: 0.6836 },

  // ---- H ----------------------------------------------------------------
  'H-p0-s00': { t: 'talk', x: 0.6715 },
  'H-p0-s01': { t: 'talk', x: 0.6855 },
};

// Benefit-first titles. Two rules applied, both from the ab-wheel rev-2 lessons: the HEADLINE
// must name the subject (a title that leaves it to the eyebrow does not survive the scroll),
// and every line is width-checked against the rendered font with >=20px of margin - the first
// draft of B measured 974px against a 976px limit.
const META = {
  B: { eyebrow: 'IF YOU ONLY TAKE THREE', title: 'THE 3 SUPPLEMENTS\nTHAT ACTUALLY MATTER' },
  A: { eyebrow: "YOU CAN'T UNDERSTAND THE STUDIES", title: 'LET AI PICK\nYOUR SUPPLEMENTS' },
  E: { eyebrow: 'MY BIGGEST MISTAKE', title: 'STOP BUYING A BIG\nSUPPLEMENT STACK' },
  D: { eyebrow: 'THE HARD TRUTH ABOUT PILLS', title: 'SUPPLEMENTS ARE ONLY\n5% OF YOUR RESULTS' },
  C: { eyebrow: 'THE MOST PROVEN SUPPLEMENT', title: 'IF YOU TAKE ONE THING\nTAKE FISH OIL' },
  J: { eyebrow: '70% OF PEOPLE ARE DEFICIENT', title: 'YOU NEED 5X MORE\nVITAMIN D' },
  M: { eyebrow: 'MOST TEST BOOSTERS DO NOTHING', title: 'THE SUPPLEMENT THAT\nDOES ALMOST NOTHING' },
  H: { eyebrow: "THE ONE I DON'T TAKE", title: 'YOU SHOULD BE\nTAKING CREATINE' },
};

function loadShots() {
  const man = JSON.parse(fs.readFileSync(path.join(__dirname, 'shots', 'manifest.json'), 'utf8'));
  const missing = man.filter((m) => !SHOTS[m.name]).map((m) => m.name);
  if (missing.length) throw new Error(`unclassified shots: ${missing.join(', ')}`);
  const extra = Object.keys(SHOTS).filter((k) => !man.some((m) => m.name === k));
  if (extra.length) throw new Error(`plan references shots that do not exist: ${extra.join(', ')}`);
  return man.map((m) => ({ ...m, ...SHOTS[m.name] }));
}

module.exports = { SHOTS, META, loadShots, SEGMENTS };

if (require.main === module) {
  const shots = loadShots();
  console.log(`${shots.length} shots, all talk`);
  for (const seg of SEGMENTS) {
    const mine = shots.filter((s) => s.seg === seg.id);
    const dur = mine.reduce((a, s) => a + s.dur, 0);
    const xs = mine.map((s) => s.x);
    console.log(` ${seg.id} ${seg.slug.padEnd(34)} ${dur.toFixed(1)}s  ${mine.length} shot(s)  ` +
      `x ${Math.min(...xs).toFixed(4)}-${Math.max(...xs).toFixed(4)}`);
  }
}
