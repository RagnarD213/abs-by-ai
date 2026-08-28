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

// REV 2 (2026-08-28). Every talk crop below is now a MEASURED torso centre (Apple Vision
// person segmentation, median over the shot at 2 fps), not a guess off a thumbnail. The
// guesses were out by 291-508 px in the delivered frame; 0.36 on A-p0-s00 is the one Dan
// screenshotted.
//
// ⚠ THE METRIC OVER-FIRES ON A TRAVELLING MOVEMENT, AND MOST OF ITS FLAGS WERE REJECTED.
// An ab-wheel rollout travels across the frame, so the crop has to hold the whole path and
// the subject is CORRECTLY off centre for most of the shot. The audit flagged every rollout
// card in C, D and E at 100-316 px - including the five in short 2, which Dan reviewed and
// passed as having no centring issues. Adopting those would have clipped his feet at the
// kneeling end. Rejected: A-p0-s01, A-p1-s04, B-p0-s03 and every C/D/E demo card.
// The rule: CENTRE a static subject, CONTAIN a moving one.

const SHOTS = {
  // ---- A  why the $17 wheel beats crunches -------------------------------------------
  'A-p0-s00': { t: 'talk', x: 0.5089 },
  'A-p0-s01': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0], why: 'rollout at full extension - horizontal' },
  'A-p0-s02': { t: 'talk', x: 0.5055 },
  'A-p0-s03': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'archival infomercial on a TV - crop to the screen, the living room around it is dead space' },
  'A-p0-s04': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p0-s05': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p0-s06': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p0-s07': { t: 'card', cardCrop: [0.40, 1.0, 0.0, 0.82], why: 'infomercial title card' },
  'A-p1-s00': { t: 'talk', zoom: true, x: 0.50, why: 'two-line lower third from row 745' },
  'A-p1-s01': { t: 'card', cardCrop: [0.3059, 0.7659, 0.38, 0.90], why: 'REV 2 RE-CENTRED. The hand-picked [0.12,0.48] window measured 670px off - it framed the pool and left Dan at the edge. Vision puts his torso at 0.536; this is that centre with the window widened to 0.46 so the rollout still fits, and it is a bigger card.' },
  'A-p1-s02': { t: 'card', cardCrop: [0.2435, 0.7435, 0.10, 0.88], why: 'REV 2 RE-CENTRED. Was 466px off the other way. Torso measured at 0.494 across the whole shot, not the 0.7 a single mid-frame suggested.' },
  'A-p1-s03': { t: 'talk', x: 0.50 },
  'A-p1-s04': { t: 'card', cardCrop: [0.29, 0.94, 0.17, 1.0], why: 'rollout at full extension' },

  // ---- B  every ab muscle at once ----------------------------------------------------
  'B-p0-s00': { t: 'talk', x: 0.50 },
  'B-p0-s01': { t: 'talk', x: 0.5385, minX0: 540, why: 'his muscle-name pills stack down the LEFT edge (x 40-520); the window starts right of them so they are excluded whole, never half-cropped' },
  'B-p0-s02': { t: 'card', cardCrop: [0.16, 0.90, 0.22, 1.0], why: 'gym rollout - horizontal' },
  'B-p0-s03': { t: 'card', cardCrop: [0.16, 0.90, 0.22, 1.0], why: 'same gym shot' },
  'B-p0-s04': { t: 'talk', x: 0.5448, minX0: 540 },
  'B-p0-s05': { t: 'extern', file: '4921658-hd_1066_1920_25fps.mp4', in: 1.2, why: 'REV 2. Dan: the old crunch b-roll was off-centre and did not fit the vertical frame. Replaced with a NATIVE 1066x1920 clip (Pexels 4921658, free licence, no attribution) of a man doing floor crunches - on-rule for casting, reads unmistakably as a crunch, and full-bleed at 1.01x instead of a crop out of 16:9.' },
  'B-p0-s06': { t: 'talk', x: 0.5448, minX0: 540 },
  'B-p0-s07': { t: 'talk', x: 0.50 },
  'B-p0-s08': { t: 'card', cardCrop: [0.02, 0.99, 0.10, 0.98], why: 'gym rollout; his lower third here says exactly what this short says, so it is kept whole (x 0.097-0.969)' },
  'B-p0-s09': { t: 'talk', zoom: true, x: 0.4859, why: 'two-line lower third' },

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
};

// Benefit-first titles that sell to someone who never saw the source video.
// A short that OPENS on a card needs a 2-line headline (build-assets.py asserts it).
const META = {
  // REV 3 (2026-08-28): A and E are Dan's rev-2 wording. REV 2 note below still applies.
  // Dan: "the titles need to make sense to someone who hasn't watched
  // the video. A lot of the titles assume watching the long form, where we need to establish
  // that this is about the ab wheel." Every headline now names the ab wheel; D, E and B are
  // his exact wording, A is the same rule applied to the one he did not rewrite.
  A: { eyebrow: 'THE BEST HOME AB EXERCISE', title: 'WHY I LOVE\nTHE AB WHEEL' },
  B: { eyebrow: 'ULTIMATE HOME AB EXERCISE', title: 'WHY THE AB WHEEL\nBEATS CRUNCHES' },
  C: { eyebrow: 'FIX THIS FIRST', title: 'THE BIGGEST\nAB WHEEL MISTAKE' },
  D: { eyebrow: 'INTENSE HOME AB EXERCISE', title: 'HOW FAST TO ROLL OUT\nWITH THE AB WHEEL' },
  E: { eyebrow: 'MY FAVORITE HOME AB EXERCISE', title: 'HOW TO DO\nAB WHEEL ROLLOUTS' },
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
