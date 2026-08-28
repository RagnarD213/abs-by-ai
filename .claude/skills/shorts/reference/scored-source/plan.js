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

// REV 4 (2026-08-28). Dan: "I go off the side... center this clip so my entire body is visible", plus a standing rule to check for graphics that are cropped or only partly visible.
//
// ⚠ MEASURED, AND IT OVERTURNS THE REV-2/3 CROPS. Apple Vision silhouettes over every
// frame of every shot say that DURING A ROLLOUT HE SPANS 0.03-0.97 OF THE 16:9 WIDTH -
// his hands and the wheel reach the far left, his shoes the far right. The old demo crop
// [0.29,0.94] was set from eyeballed extremes and cut his hands off on every rep. And
// Muhammad's own graphics are just as wide: the left muscle panel runs to x0.39, the
// lower thirds to x0.94, the top pills to x0.96.
//
// So on this source there is no crop that is both tighter than the frame and safe. Every
// backyard card is now the FULL FRAME. It is not a compromise - it is the only window
// that keeps his whole body in shot AND every burned graphic whole, and it makes the card
// size identical across the batch. Insets (the TV, the extern clip) are the exception,
// and each is verified to contain its own content whole.
//
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
  'A-p0-s01': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'rollout - he spans 0.028-0.892, so anything narrower than the frame cuts his hands' },
  'A-p0-s02': { t: 'talk', x: 0.5055 },
  'A-p0-s03': { t: 'card', cardCrop: [0.51, 1.0, 0.0, 0.70], why: 'the TV screen is the graphic; measured x 0.55-0.99, so this window holds it whole and larger' },
  'A-p0-s04': { t: 'card', cardCrop: [0.51, 1.0, 0.0, 0.70] },
  'A-p0-s05': { t: 'card', cardCrop: [0.51, 1.0, 0.0, 0.70] },
  'A-p0-s06': { t: 'card', cardCrop: [0.51, 1.0, 0.0, 0.70] },
  'A-p0-s07': { t: 'card', cardCrop: [0.51, 1.0, 0.0, 0.70] },
  'A-p1-s00': { t: 'talk', zoom: true, x: 0.5, why: 'two-line lower third from row 745 - the zoom window excludes it whole' },
  'A-p1-s01': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'his rounded glow card is itself a graphic - shown whole rather than cropped into' },
  'A-p1-s02': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'same glow card, med-ball crunch; he spans 0.056-0.770' },
  'A-p1-s03': { t: 'talk', x: 0.5 },
  'A-p1-s04': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'rollout - spans 0.147-0.846' },

  // ---- B  every ab muscle at once ----------------------------------------------------
  'B-p0-s00': { t: 'talk', x: 0.5 },
  'B-p0-s01': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'his muscle-name panel runs from x0 to x0.39 and he stands at 0.37-0.70 - no window excludes the panel without cutting him, so the frame is shown whole. THIS IS THE 0:10 / 0:19 ARTEFACT DAN SAW: the old minX0 sliced the panel and left a white pill fragment at the frame edge.' },
  'B-p0-s02': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'gym rollout - spans 0.022-0.999' },
  'B-p0-s03': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'same continuous take as s02, same window' },
  'B-p0-s04': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'muscle panel' },
  'B-p0-s05': { t: 'extern', file: '4921658-hd_1066_1920_25fps.mp4', in: 1.2, why: 'REV 2. Dan: the old crunch b-roll was off-centre and did not fit the vertical frame. Replaced with a NATIVE 1066x1920 clip (Pexels 4921658, free licence, no attribution) of a man doing floor crunches - on-rule for casting, reads unmistakably as a crunch, and full-bleed at 1.01x instead of a crop out of 16:9.' },
  'B-p0-s06': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'muscle panel' },
  'B-p0-s07': { t: 'talk', x: 0.5 },
  'B-p0-s08': { t: 'card', cardCrop: [0, 1, 0, 1], why: 'gym rollout under a lower third that runs x 0.054-0.940' },
  'B-p0-s09': { t: 'talk', zoom: true, x: 0.4859, why: 'two-line lower third - excluded by the zoom window' },

  // ---- C  the biggest mistake --------------------------------------------------------
  'C-p0-s00': { t: 'card', cardCrop: [0, 1, 0, 1] },
  // MEASURED CORRECTION. The first version of this crop trimmed the top 14% to "get closer",
  // which is self-defeating on a 16:9 source: cropping height makes the aspect WIDER, and a
  // wider card fitted to 1080 is SHORTER - 522px against 643px for the untrimmed frame. Every
  // "keep his graphic whole" shot now uses the same [0.03, 0.975, 0, 1]: full height, 2.5%
  // off each side, which is inside the widest burned graphic in the cut (a top pill runs
  // x 0.037-0.956, a lower third x 0.097-0.969).
  'C-p0-s01': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'C-p0-s02': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'C-p0-s03': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'C-p0-s04': { t: 'card', cardCrop: [0, 1, 0, 1] },

  // ---- D  tempo ----------------------------------------------------------------------
  'D-p0-s00': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'D-p0-s01': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'D-p0-s02': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'D-p0-s03': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'D-p0-s04': { t: 'card', cardCrop: [0, 1, 0, 1] },

  // ---- E  beginner to advanced -------------------------------------------------------
  // The top pills here are CORRECT for this short and carry its structure, so they stay.
  'E-p0-s00': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'E-p0-s01': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'E-p0-s02': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'E-p0-s03': { t: 'card', cardCrop: [0, 1, 0, 1] },
  'E-p0-s04': { t: 'card', cardCrop: [0, 1, 0, 1] },
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
