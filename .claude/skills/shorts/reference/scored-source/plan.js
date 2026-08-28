// Per-shot treatment plan for the ab-wheel Shorts.
//
// TREATMENTS
//   talk    - Dan on the locked backyard camera. Full-bleed 9:16 crop.
//   broll   - footage with NO burned text. Full-bleed 9:16 crop at a tuned offset.
//   card    - anything with text, a designed graphic, or a HORIZONTAL body pose. The whole
//             16:9 frame on the J2 tactical background, so nothing is sliced through.
//
// WHY THIS BATCH IS CARD-HEAVY, and it is not laziness. Two properties of the source:
//   1. The ab-wheel rollout is a horizontal movement. At full extension Dan spans 0.30-1.00
//      of the source width (measured at 128s, 158s, 238s, 262s); a 9:16 window is 0.317 of
//      it. Crop and you keep his head and lose the straight-body line, which IS the lesson.
//   2. The cut is a finished 16:9 product with graphics burned into the pixels. The top pill
//      is 1595px wide (83% of the frame) and the lower third 1210px; neither can be dodged
//      horizontally, so a shot carrying one is either shown whole or has the band cropped off.
// `cardCrop` [x0,x1,y0,y1] as fractions does the second job where a burned graphic is WRONG
// for the short it lands in - see F below, the only place that happens.
//
// `x` is the crop-window CENTRE as a fraction of frame width. null = auto (choose-crops.py).
const path = require('path');
const fs = require('fs');
const { SEGMENTS } = require('./segments.js');

// Dan stands almost dead centre on the backyard camera (measured x 760-1160 at 95s, centre
// 0.50). Kneeling shots move him right, so those get per-shot values below.
const TALK_X = 0.50;

const SHOTS = {
  // ---- A  why the $17 wheel beats crunches -------------------------------------------
  'A-p0-s00': { t: 'talk', x: 0.36 },
  'A-p0-s01': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0], why: 'rollout at full extension - horizontal' },
  'A-p0-s02': { t: 'talk', x: 0.42 },
  'A-p0-s03': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'archival infomercial on a TV - crop to the screen, the living room around it is dead space' },
  'A-p0-s04': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p0-s05': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p0-s06': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p0-s07': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p1-s00': { t: 'talk', zoom: true, x: 0.50, why: 'two-line lower third from row 745' },
  'A-p1-s01': { t: 'card', cardCrop: [0.12, 0.48, 0.38, 0.90], why: 'his rounded glow card holds a 16:9 shot inside a 16:9 frame - crop past BOTH to Dan, or he ends up a thumbnail inside a thumbnail' },
  'A-p1-s02': { t: 'card', cardCrop: [0.55, 0.93, 0.10, 0.88], why: 'med-ball crunch inside the same glow card - cropped to the subject' },
  'A-p1-s03': { t: 'talk', x: 0.50 },
  'A-p1-s04': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0], why: 'rollout at full extension' },

  // ---- B  every ab muscle at once ----------------------------------------------------
  'B-p0-s00': { t: 'talk', x: 0.50 },
  'B-p0-s01': { t: 'talk', x: 0.63, minX0: 540, why: 'his muscle-name pills stack down the LEFT edge (x 40-520); the window starts right of them so they are excluded whole, never half-cropped' },
  'B-p0-s02': { t: 'card', cardCrop: [0.16, 0.90, 0.22, 1.0], why: 'gym rollout - horizontal' },
  'B-p0-s03': { t: 'card', cardCrop: [0.16, 0.90, 0.22, 1.0], why: 'same gym shot' },
  'B-p0-s04': { t: 'talk', x: 0.63, minX0: 540 },
  'B-p0-s05': { t: 'card', cardCrop: [0.30, 0.94, 0.10, 0.95], why: 'crunch b-roll - horizontal pose, cropped to the subject (measured x 0.35-0.88, y 0.13-0.90)' },
  'B-p0-s06': { t: 'talk', x: 0.63, minX0: 540 },
  'B-p0-s07': { t: 'talk', x: 0.50 },
  'B-p0-s08': { t: 'card', cardCrop: [0.02, 0.99, 0.10, 0.98], why: 'gym rollout; his lower third here says exactly what this short says, so it is kept whole (x 0.097-0.969)' },
  'B-p0-s09': { t: 'talk', zoom: true, x: 0.50, why: 'two-line lower third' },

  // ---- C  the biggest mistake --------------------------------------------------------
  'C-p0-s00': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0], why: 'kneeling start position - the whole body line is the point' },
  // MEASURED CORRECTION. The first version of this crop trimmed the top 14% to "get closer",
  // which is self-defeating on a 16:9 source: cropping height makes the aspect WIDER, and a
  // wider card fitted to 1080 is SHORTER - 522px against 643px for the untrimmed frame. Every
  // "keep his graphic whole" shot now uses the same [0.03, 0.975, 0, 1]: full height, 2.5%
  // off each side, which is inside the widest burned graphic in the cut (a top pill runs
  // x 0.037-0.956, a lower third x 0.097-0.969).
  'C-p0-s01': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: '"Start without your back excessively arched" - his olive lower third is on screen in this shot and it spans x 0.10-0.97 (measured across five of them), so there is no horizontal crop that dodges it and no vertical one that keeps the extended body line. Full width, graphic whole, shorter stage' },
  'C-p0-s02': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0] },
  'C-p0-s03': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: '"Your arms need to be straight" - his olive lower third is on screen in this shot and it spans x 0.10-0.97 (measured across five of them), so there is no horizontal crop that dodges it and no vertical one that keeps the extended body line. Full width, graphic whole, shorter stage' },
  'C-p0-s04': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: '"Lock down arms and straight back" (measured x 0.217-0.926)' },

  // ---- D  tempo ----------------------------------------------------------------------
  'D-p0-s00': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: '"You have to rollout slowly with control"' },
  'D-p0-s01': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0], why: 'the too-fast demo - full extension' },
  'D-p0-s02': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0] },
  'D-p0-s03': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0], why: 'the correct-pace demo - full extension' },
  'D-p0-s04': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0] },

  // ---- E  beginner to advanced -------------------------------------------------------
  // The top pills here are CORRECT for this short and carry its structure, so they stay.
  'E-p0-s00': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: '"How to do this if you are a beginner" (measured x 0.188-0.911)' },
  'E-p0-s01': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: 'his "How Beginners Should Do It" pill is CORRECT here and carries this short structure, so the crop keeps it whole (measured x 0.104-0.928)' },
  'E-p0-s02': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: '"How Intermediate Guys Should Do It"' },
  'E-p0-s03': { t: 'card', cardCrop: [0.03, 0.975, 0.0, 1.0], why: '"How Advanced Guys Should Do It"' },
  'E-p0-s04': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0] },

  // ---- F  the standing bodybuilder version -------------------------------------------
  'F-p0-s00': { t: 'talk', zoom: true, x: 0.50, why: 'the previous beat\'s lower third is still on screen for 0.5s' },
  'F-p0-s01': { t: 'broll', x: 0.62, why: 'bodybuilder, a vertical subject - crops cleanly' },
  'F-p0-s02': { t: 'talk', x: 0.50 },
  'F-p1-s00': { t: 'card', cardCrop: [0.29, 0.94, 0.19, 1.0], why: 'the stale pill fades in at the tail of this shot' },
  // A STALE PILL. His cut still reads "How Intermediate Guys Should Do It" across the
  // standing-wall beat, which is wrong for this short and would be a factual error on
  // screen. Rows 0-190 are cropped off the card so it is gone rather than contradicted.
  'F-p1-s01': { t: 'card', cardCrop: [0.29, 0.94, 0.19, 1.0], why: 'STALE PILL. His cut still reads "How Intermediate Guys Should Do It" across the standing-wall beat, which is wrong for this short and would be a factual error on screen. The top 19% is cropped off so it is gone rather than contradicted.' },
  'F-p1-s02': { t: 'broll', x: 0.50, why: 'gym close-up, no text' },
  'F-p1-s03': { t: 'broll', x: 0.50 },
  'F-p1-s04': { t: 'card', cardCrop: [0.29, 0.94, 0.19, 1.0], why: 'stale top pill cropped off' },
};

// Benefit-first titles that sell to someone who never saw the source video.
// A short that OPENS on a card needs a 2-line headline (build-assets.py asserts it).
const META = {
  A: { eyebrow: 'CRUNCHES VS THE AB WHEEL', title: 'THE $17 TOOL THAT\nBEATS CRUNCHES' },
  B: { eyebrow: 'ONE MOVE, EVERY AB MUSCLE', title: 'CRUNCHES ONLY\nHIT ONE OF THESE' },
  C: { eyebrow: 'FIX THIS FIRST', title: 'THE BIGGEST\nAB WHEEL MISTAKE' },
  D: { eyebrow: 'TIME UNDER TENSION', title: "YOU'RE ROLLING\nOUT TOO FAST" },
  E: { eyebrow: 'PICK YOUR LEVEL', title: 'HOW FAR YOU\nSHOULD ROLL' },
  F: { eyebrow: 'BODYBUILDERS ONLY', title: 'DO NOT COPY\nTHIS AB MOVE' },
};

function loadShots() {
  const man = JSON.parse(fs.readFileSync(path.join(__dirname, 'shots', 'manifest.json'), 'utf8'));
  const missing = man.filter((m) => !SHOTS[m.name]).map((m) => m.name);
  if (missing.length) throw new Error(`unclassified shots: ${missing.join(', ')}`);
  const extra = Object.keys(SHOTS).filter((k) => !man.some((m) => m.name === k));
  if (extra.length) throw new Error(`plan references shots that do not exist: ${extra.join(', ')}`);
  return man.map((m) => ({ ...m, ...SHOTS[m.name] }));
}

module.exports = { SHOTS, META, TALK_X, loadShots, SEGMENTS };

if (require.main === module) {
  const shots = loadShots();
  const counts = shots.reduce((a, s) => ((a[s.t] = (a[s.t] || 0) + 1), a), {});
  console.log('shot treatments:', counts, `(${shots.length} total)`);
  for (const seg of SEGMENTS) {
    const mine = shots.filter((s) => s.seg === seg.id);
    const dur = mine.reduce((a, s) => a + s.dur, 0);
    console.log(` ${seg.id} ${seg.slug.padEnd(26)} ${dur.toFixed(1)}s  ` +
      mine.map((s) => (s.zoom ? s.t[0].toUpperCase() : s.t[0])).join(''));
  }
}
