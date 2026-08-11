// Per-shot treatment plan for the V3 "Top 10 Tips" Shorts.
//
// TREATMENTS
//   talk    - the presenter on the locked kitchen camera. Full-bleed 9:16 crop.
//   broll   - stock footage with NO text/UI/numbers. Full-bleed 9:16 crop at a tuned offset.
//   card    - anything containing text, a credit attribution, a designed graphic, or a
//             HORIZONTAL body pose. The whole 16:9 frame is scaled into the vertical frame
//             on the J2 tactical background, so nothing is sliced through.
//
// `x` is the crop-window CENTRE as a fraction of frame width (0.5 = centre). null = auto.
//
// `zoom: true` crops 87% of the source HEIGHT from the top instead of the full height.
// V3 burns a chapter lower-third ("05 Fast Until 2PM Every Day") across the bottom of the
// first shot of each tip. It spans roughly 0.24-0.82 of the width, so a centred 9:16 window
// slices it mid-sentence -- visible under our own captions and unreadable. Cropping from the
// top pushes that band out of frame entirely at the cost of ~13% headroom, which this
// framing has to spare. Our own title replaces the information anyway.
const path = require('path');
const fs = require('fs');
const { SEGMENTS } = require('./segments.js');

// The presenter sits marginally left of centre on the locked kitchen camera. Measured from
// the crop review sheet, not guessed; one value covers every talking-head shot in the video.
const TALK_X = 0.478;

const SHOTS = {
  // PER-VIDEO. One entry per shot in shots/manifest.json; loadShots() throws if any shot is
  // unclassified or if the plan names a shot that does not exist, so this cannot drift.
  //
  //   'A-p0-s00': { t: 'talk', zoom: true },
  //   'A-p0-s01': { t: 'broll', x: 0.55 },
  //   'B-p0-s02': { t: 'card' },
  //   'C-p0-s02': { t: 'card', cardCrop: [0.23, 0.76, 0.19, 0.80] },
  //
  // See ../../SKILL.md Step 4 for what each treatment means and when to use it.
};

// PER-VIDEO. Benefit-first titles that sell to someone who never saw the source video.
// A short that OPENS on a card needs a 2-line headline; build-assets.py asserts it.
const META = {
  // A: { title: 'STOP DOING\nAB EXERCISES', eyebrow: 'IF YOU CANT SEE THEM YET' },
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
    console.log(` ${seg.id} ${seg.slug.padEnd(28)} ${dur.toFixed(1)}s  ` +
      mine.map((s) => (s.zoom ? s.t[0].toUpperCase() : s.t[0])).join(''));
  }
}
