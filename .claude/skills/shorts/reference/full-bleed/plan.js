// Per-shot treatment plan for the V2 Shorts.
//
// TREATMENTS
//   talk    - Dan on the locked kitchen camera. Full-bleed 9:16 crop. Reads as native vertical.
//   broll   - stock footage with NO text/UI/numbers. Full-bleed 9:16 crop at a tuned offset;
//             cropping plain footage looks like a vertical video, not a chopped one.
//   card    - anything containing text, numbers, a phone UI or a designed graphic. The WHOLE
//             16:9 frame is scaled to fit inside the vertical frame on the locked J2 tactical
//             background, so nothing is ever sliced through.
//   pip     - Dan plus a corner graphic that falls outside the crop. Crop to Dan, then
//             re-composite the graphic at a legible size inside the vertical frame.
//
// `x` is the crop-window CENTRE as a fraction of frame width (0.5 = centre). null = auto.
const path = require('path');
const fs = require('fs');
const { SEGMENTS } = require('./segments.js');

// Dan sits marginally left of centre on the locked kitchen camera; measured, not guessed
// (see review-crops.py output). One value covers every talking-head shot in the video.
const TALK_X = 0.478;

const SHOTS = {
  // ---- A: Sean Ray vision board -------------------------------------------------
  'A-p0-s00': { t: 'talk' },
  'A-p0-s01': { t: 'broll', x: 0.50 },  // oiled torso close-up
  'A-p0-s02': { t: 'talk' },
  'A-p0-s03': { t: 'broll', x: 0.45 },  // cable machine, subject left
  'A-p0-s04': { t: 'talk' },
  'A-p0-s05': { t: 'talk' },
  'A-p0-s06': { t: 'pip'  },            // Sean Ray photo, top-left
  'A-p0-s07': { t: 'talk' },
  'A-p0-s08': { t: 'broll', x: 0.50 },  // torso close-up
  'A-p0-s09': { t: 'pip'  },            // blue-shorts physique, top-left
  'A-p0-s10': { t: 'talk' },
  'A-p0-s11': { t: 'broll', x: null },  // man in forest

  // ---- B: sugar-free gum --------------------------------------------------------
  'B-p0-s00': { t: 'broll', x: 0.38 },  // man with phone outdoors
  'B-p1-s00': { t: 'talk' },
  'B-p1-s01': { t: 'card' },            // flip clock reading 11:00 — numbers must stay whole
  'B-p1-s02': { t: 'talk' },
  'B-p1-s03': { t: 'broll', x: null },  // gum container
  'B-p1-s04': { t: 'talk' },

  // ---- D: ask the AI to interview you -------------------------------------------
  'D-p0-s00': { t: 'talk' },
  'D-p0-s01': { t: 'broll', x: 0.52 },  // pull-up / abs
  'D-p0-s02': { t: 'talk' },

  // ---- E: supplements are 3% ----------------------------------------------------
  'E-p0-s00': { t: 'broll', x: null },  // bronze physique statue
  'E-p0-s01': { t: 'broll', x: 0.45 },  // capsules on a table
  'E-p0-s02': { t: 'talk' },
  'E-p0-s03': { t: 'broll', x: null },  // blister packs in a bag
  'E-p0-s04': { t: 'talk' },
  'E-p0-s05': { t: 'broll', x: null },  // man on a machine
  'E-p0-s06': { t: 'broll', x: 0.42 },  // hands with a bottle
  'E-p0-s07': { t: 'broll', x: 0.68 },  // pills in a palm
  'E-p0-s08': { t: 'talk' },

  // ---- G: hire a maid -----------------------------------------------------------
  'G-p0-s00': { t: 'broll', x: null },  // hands counting money
  'G-p0-s01': { t: 'talk' },
  'G-p0-s02': { t: 'broll', x: 0.45 },  // housekeeper in a room
  'G-p0-s03': { t: 'broll', x: null },  // hand wiping a surface
  'G-p0-s04': { t: 'broll', x: null },  // man walking with a gym bag
  'G-p0-s05': { t: 'talk' },

  // ---- I: macro tracking is obsolete --------------------------------------------
  'I-p0-s00': { t: 'card' },            // carries the "02 AI can track your macros" lower third
  'I-p0-s01': { t: 'talk' },
  'I-p0-s02': { t: 'broll', x: 0.58 },  // cereal bowl
  'I-p0-s03': { t: 'talk' },
  'I-p0-s04': { t: 'broll', x: null },  // plate of food
  'I-p0-s05': { t: 'card' },            // phone health dashboard — UI + numbers
  'I-p0-s06': { t: 'talk' },
  'I-p1-s00': { t: 'talk' },
  'I-p1-s01': { t: 'card' },            // carrot on a scale — the readout is the point
  'I-p1-s02': { t: 'talk' },
  'I-p1-s03': { t: 'talk' },

  // ---- J: chicken soup trick ----------------------------------------------------
  'J-p0-s00': { t: 'card' },            // phone stats screen
  'J-p0-s01': { t: 'talk' },
  'J-p0-s02': { t: 'broll', x: 0.28 },  // fried chicken + soup bowls
  'J-p0-s03': { t: 'talk' },
  'J-p0-s04': { t: 'broll', x: null },  // plate with fork and spoon
  'J-p0-s05': { t: 'talk' },
  'J-p0-s06': { t: 'broll', x: null },  // real app screen recording — portrait phone on white
  'J-p0-s07': { t: 'broll', x: null },  // ditto, longer
  'J-p0-s08': { t: 'talk' },
};

// Titles + the on-screen hook line for each short.
const META = {
  A: { title: 'THE VISION BOARD\nTHAT BUILT\nMIKE CHANG', eyebrow: 'HOW AI REPLACED IT' },
  B: { title: 'THE TRICK THAT\nKILLED MY\nNIGHT SNACKING', eyebrow: 'AI NUTRITIONIST' },
  D: { title: 'MAKE THE AI\nINTERVIEW\nYOU', eyebrow: 'THE PROMPT NOBODY USES' },
  E: { title: 'SUPPLEMENTS ARE\nONLY 3% OF\nYOUR RESULTS', eyebrow: 'WHAT ACTUALLY WORKS' },
  G: { title: 'HIRE A MAID,\nNOT A\nPERSONAL TRAINER', eyebrow: 'WHERE THE MONEY GOES' },
  // I and J OPEN on a card shot, whose top edge is at y=420. A 3-line headline runs to
  // y=455 and lands on the card. Two lines end at ~353 and clear it.
  I: { title: 'THE FOOD SCALE\nIS OBSOLETE', eyebrow: 'JUST TAKE A PHOTO' },
  J: { title: 'MAKE AI MACROS\nMORE ACCURATE', eyebrow: 'THE CHICKEN SOUP FIX' },
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
      mine.map((s) => s.t[0]).join(''));
  }
}
