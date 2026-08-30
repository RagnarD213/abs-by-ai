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
// ⚠ REV 2 - `tight: true` IS THE PUNCH. Every short opens wide and alternates at every join.
// A join is either a picture cut inherited from the source edit (the four Dan called "awkward
// cut"/"jump cut") or one we make removing a pause; measured, both jump the picture 5-12 MAD
// against a 1.30 adjacent-frame baseline, so each is hidden by a framing change rather than
// left naked. Geometry in layout.json: 578x862 @ top 126 vs 644x960 @ top 120, chosen so his
// head lands at the same delivered y - only the framing moves.
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

  // ---- E ----------------------------------------------------------------
  'E-p0-s00': { t: 'talk', x: 0.6695, src: 'raw' },
  'E-p1-s00': { t: 'talk', x: 0.6848, tight: true },
  'E-ai-e1': { t: 'ai', aiIn: 1.6 },
  'E-p2-s00': { t: 'talk', x: 0.6848 },

  // ---- J ----------------------------------------------------------------
  'J-p0-s00': { t: 'talk', x: 0.6699 },
  'J-ai-j0': { t: 'ai', aiIn: 2.2 },
  'J-p1-s00': { t: 'talk', x: 0.6676, tight: true },
  'J-ai-j1': { t: 'ai', aiIn: 0.8 },
  'J-p2-s00': { t: 'talk', x: 0.6676 },
  'J-p2-s01': { t: 'talk', x: 0.6676, tight: true },

  // ---- A ----------------------------------------------------------------
  'A-p0-s00': { t: 'talk', x: 0.6707 },
  'A-p1-s00': { t: 'talk', x: 0.6707, tight: true },
  'A-p2-s00': { t: 'talk', x: 0.6750 },

  // ---- M ----------------------------------------------------------------
  'M-p0-s00': { t: 'talk', x: 0.6816 },
  'M-p0-s01': { t: 'talk', x: 0.6836, tight: true },
  'M-ai-m1': { t: 'ai', aiIn: 0.8 },
  'M-p1-s00': { t: 'talk', x: 0.6836 },

  // ---- C ----------------------------------------------------------------
  'C-p0-s00': { t: 'talk', x: 0.6730 },
  'C-ai-c1': { t: 'ai', aiIn: 0.8 },
  'C-p1-s00': { t: 'talk', x: 0.6730, tight: true },
  'C-ai-c2': { t: 'ai', aiIn: 0.6 },
  'C-p2-s00': { t: 'talk', x: 0.6852 },

  // ---- H ----------------------------------------------------------------
  'H-p0-s00': { t: 'talk', x: 0.6715 },
  'H-ai-h1': { t: 'ai', aiIn: 4.6 },
  'H-p1-s00': { t: 'talk', x: 0.6855, tight: true },
  'H-ai-h2': { t: 'ai', aiIn: 2.2 },
  'H-p2-s00': { t: 'talk', x: 0.6855 },

  // ---- D ----------------------------------------------------------------
  'D-p0-s00': { t: 'talk', x: 0.6871 },
  'D-ai-d1': { t: 'ai', aiIn: 1.8 },
  'D-p1-s00': { t: 'talk', x: 0.6871, tight: true },
  'D-p1-s01': { t: 'talk', x: 0.6969 },
  'D-ai-d2': { t: 'ai', aiIn: 0.2 },
  'D-p2-s00': { t: 'talk', x: 0.6969, tight: true },
};

// Benefit-first titles. Two rules applied, both from the ab-wheel rev-2 lessons: the HEADLINE
// must name the subject (a title that leaves it to the eyebrow does not survive the scroll),
// and every line is width-checked against the rendered font with >=20px of margin - the first
// draft of B measured 974px against a 976px limit.
const META = {
  B: { eyebrow: 'IF YOU ONLY TAKE THREE', title: 'THE 3 SUPPLEMENTS\nTHAT ACTUALLY MATTER' },
  // REV 2 - J, M and H are Dan's exact wording. M's headline does not fit at the batch's 98pt
  // (its long line measures 1352px against a 976px limit), so build-assets.py fits the TYPE to
  // his words rather than the other way round.
  A: { eyebrow: "YOU CAN'T UNDERSTAND THE STUDIES", title: 'LET AI PICK\nYOUR SUPPLEMENTS' },
  E: { eyebrow: 'MY BIGGEST MISTAKE', title: 'STOP BUYING A BIG\nSUPPLEMENT STACK' },
  D: { eyebrow: 'THE HARD TRUTH ABOUT PILLS', title: 'SUPPLEMENTS ARE ONLY\n5% OF YOUR RESULTS' },
  C: { eyebrow: 'THE MOST PROVEN SUPPLEMENT', title: 'IF YOU TAKE ONE THING\nTAKE FISH OIL' },
  J: { eyebrow: '70% OF MEN ARE DEFICIENT', title: 'WHY MEN MUST TAKE\nVITAMIN D' },
  M: { eyebrow: 'STOP TAKING THIS SUPPLEMENT', title: 'WHY TEST BOOSTERS ARE THE\nLEAST IMPORTANT SUPPLEMENT' },
  H: { eyebrow: "I DON'T TAKE CREATINE, BUT", title: 'YOU SHOULD BE\nTAKING CREATINE' },
};

function loadShots() {
  const man = JSON.parse(fs.readFileSync(path.join(__dirname, 'shots', 'manifest.json'), 'utf8'));
  // An AI cover clip is self-describing - it has no measured torso centre because it is not
  // Dan, and no punch because it IS the framing change.
  for (const m of man) if (m.src === 'ai' && !SHOTS[m.name]) SHOTS[m.name] = { t: 'ai', aiIn: m.aiIn };
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
