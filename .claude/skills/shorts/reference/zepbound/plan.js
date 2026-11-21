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
  // ---- A ----------------------------------------------------------------
  'A-p0-s00': { t: 'talk', x: 0.5242 },
  'A-p1-s00': { t: 'talk', x: 0.5227, tight: true },
  'A-p2-s00': { t: 'talk', x: 0.5133 },
  'A-p2-s01': { t: 'talk', x: 0.5258, tight: true },
  'A-p3-s00': { t: 'talk', x: 0.5219 },

  // ---- B ----------------------------------------------------------------
  'B-p0-s00': { t: 'talk', x: 0.5188 },
  'B-p0-s01': { t: 'talk', x: 0.5161, tight: true },
  'B-p0-s02': { t: 'talk', x: 0.5000 },

  // ---- C ----------------------------------------------------------------
  'C-p0-s00': { t: 'talk', x: 0.5422 },
  'C-p1-s00': { t: 'talk', x: 0.5398, tight: true },
  'C-p1-s01': { t: 'talk', x: 0.5469 },

  // ---- D ----------------------------------------------------------------
  'D-p0-s00': { t: 'talk', x: 0.5172 },
  'D-p1-s00': { t: 'talk', x: 0.5227, tight: true },

  // ---- E ----------------------------------------------------------------
  'E-p0-s00': { t: 'talk', x: 0.5078 },
  'E-p1-s00': { t: 'talk', x: 0.4992, tight: true },
  'E-p2-s00': { t: 'talk', x: 0.5312 },

  // ---- F ----------------------------------------------------------------
  'F-p0-s00': { t: 'talk', x: 0.5141 },
  'F-p1-s00': { t: 'talk', x: 0.5016, tight: true },
  'F-p1-s01': { t: 'talk', x: 0.5109 },

  // ---- G ----------------------------------------------------------------
  'G-p0-s00': { t: 'talk', x: 0.5297 },
  'G-p1-s00': { t: 'talk', x: 0.5290, tight: true },

  // ---- H ----------------------------------------------------------------
  'H-p0-s00': { t: 'talk', x: 0.5219 },
  'H-p0-s01': { t: 'talk', x: 0.5078, tight: true },
  'H-p1-s00': { t: 'talk', x: 0.5391 },
};

// Benefit-first titles. Two rules applied, both from the ab-wheel rev-2 lessons: the HEADLINE
// must name the subject (a title that leaves it to the eyebrow does not survive the scroll),
// and every line is width-checked against the rendered font with >=20px of margin - the first
// draft of B measured 974px against a 976px limit.
const META = {
  // Benefit-first, the subject named in the HEADLINE, and - Dan's standing copy rule - NO DRUG
  // NAME IN ANY GRAPHIC. He says it freely on camera; it never reaches the screen. "GLP-1" is
  // the drug class, "weight loss shot" is plain English; neither is a brand or generic name.
  A: { eyebrow: 'THE KNOCKOUT ARGUMENT', title: 'THE SHOT THAT KILLED\nMY URGE TO DRINK' },
  B: { eyebrow: 'WHEN TO TAKE YOUR GLP-1', title: 'INJECT THURSDAY\nEVENING. HERE IS WHY' },
  C: { eyebrow: 'AVOID THE SIDE EFFECTS', title: 'START YOUR GLP-1 AT\n1 MG, NOT 2.5' },
  D: { eyebrow: 'GLP-1 PEN VS NEEDLE', title: 'WHY THE NEEDLE\nBEATS THE PEN' },
  E: { eyebrow: 'THE DOSE MISTAKE I MADE', title: "DON'T GO ABOVE\n2.5 MG" },
  F: { eyebrow: 'THE REAL RISK ON A GLP-1', title: 'LOSE FAT, NOT MUSCLE:\nTHE PROTEIN TARGET' },
  G: { eyebrow: 'BEFORE YOU BUY A GLP-1', title: 'COMPOUNDED VS\nBRAND NAME' },
  H: { eyebrow: 'MY DOCTOR WOULD SAY NO', title: 'WHY I TAKE A GLP-1\nWITH SIX PACK ABS' },
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
