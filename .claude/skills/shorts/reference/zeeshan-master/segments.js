// Precise in/out points for the V2 Shorts, resolved against Whisper word timestamps
// (never the rounded sentence marks in v2-transcript.txt).
const fs = require('fs');
const path = require('path');

const words = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'work', 'words.json'), 'utf8')
).chunks;

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
const flat = words.map((w) => norm(w.text)).join(' ');
// index map: char offset in `flat` -> word index
const offsets = [];
{
  let pos = 0;
  words.forEach((w, i) => {
    const t = norm(w.text);
    offsets.push({ start: pos, end: pos + t.length, i });
    pos += t.length + 1;
  });
}
const wordIndexAtChar = (c) => {
  for (const o of offsets) if (c >= o.start && c <= o.end) return o.i;
  return -1;
};

// Find the word-index range for a phrase. `nth` picks among repeats.
function find(phrase, nth = 0) {
  const p = norm(phrase);
  let from = 0, hit = -1;
  for (let k = 0; k <= nth; k++) {
    hit = flat.indexOf(p, from);
    if (hit === -1) throw new Error(`phrase not found (occurrence ${k}): "${phrase}"`);
    from = hit + 1;
  }
  const a = wordIndexAtChar(hit);
  const b = wordIndexAtChar(hit + p.length - 1);
  return { a, b, t0: words[a].timestamp[0], t1: words[b].timestamp[1] };
}

// Speech gaps, measured by work/vad.py. NOT silencedetect: this source carries a music
// bed the whole way and it swells, so "quiet in the mix" and "nobody is talking" are
// different questions here. See work/vad.py for the measurements that forced the change.
const SILENCE = JSON.parse(fs.readFileSync(path.join(__dirname, 'work', 'gaps.json'), 'utf8'));

const inGap = (t) => SILENCE.some(([a, b]) => t >= a - 0.02 && t <= b + 0.02);

// Cut point just BEFORE speech starts at `t`. `floor` is the end of the previous word:
// the snap may never cross it, or a sub-threshold gap between two sentences sends the
// search back past a whole phrase.
function snapIn(t, floor, preroll = 0.22) {
  let best = null;
  for (const [a, b] of SILENCE) {
    if (a > t + 0.25) break;
    if (b >= floor - 0.35 && b <= t + 0.25) best = [a, b];
  }
  if (!best) return Math.max(0, floor, t - 0.10);
  return Math.max(best[0] + 0.04, Math.min(best[1] - 0.04, best[1] - preroll));
}

// Cut point just AFTER speech ends at `t`. `ceil` is the start of the next word.
function snapOut(t, ceil, tail = 0.34) {
  for (const [a, b] of SILENCE) {
    if (b < t - 0.05) continue;
    if (a > ceil + 0.35) break;
    // Never cut before the LATER of "speech stopped" (VAD) and "the word ended" (Whisper).
    // The VAD gap can open a few frames early on a trailing fricative; taking the max keeps
    // the final consonant, and the clamp to b-0.04 keeps the cut inside the gap.
    const floorT = Math.max(a, t);
    return Math.min(b - 0.04, Math.max(a + 0.04, floorT + tail));
  }
  return Math.min(t + 0.12, ceil + 0.05);
}

const BAD = [];
// A live-round slice: music only, no speech to protect, so explicit in/out are used as is.
function musicPiece(start, end, label) {
  return { start, end, from: label, to: label, music: true };
}
// A piece = continuous run of source video, from the START of `from` to the END of `to`.
// `inAt` forces an explicit in-point. Needed where Whisper inflates a short word
// across a real pause (V6 "the" = 148.28-149.00 hides a measured 148.44-148.63 gap),
// so the word timestamp says "no silence here" while the audio plainly has one.
// The silence assertion below still applies, so this can't smuggle in a bad cut.
function piece(from, to = from, { nthFrom = 0, nthTo = 0, tail = 0.34, preroll = 0.22, inAt = null, outAt = null } = {}) {
  const f = find(from, nthFrom);
  const t = find(to, nthTo);
  if (t.t1 <= f.t0) throw new Error(`"${to}" ends before "${from}" starts`);
  const prev = words[f.a - 1];
  const next = words[t.b + 1];
  const start = inAt !== null ? inAt : snapIn(f.t0, prev ? prev.timestamp[1] : 0, preroll);
  const end = outAt !== null ? outAt : snapOut(t.t1, next ? next.timestamp[0] : t.t1 + 0.4, tail);
  if (end <= start) throw new Error(`snapped cut collapsed for "${from}"`);
  // Step 3 of the skill: a cut that is NOT inside measured silence clips a syllable.
  // Assert it rather than trusting the snap helpers' fallback branches.
  if (!inGap(start)) { const m = `IN cut ${start.toFixed(2)}s not in a speech gap: "${from}"`;
    if (process.env.REPORT) BAD.push(m); else throw new Error(m); }
  if (!inGap(end)) { const m = `OUT cut ${end.toFixed(2)}s not in a speech gap: "${to}"`;
    if (process.env.REPORT) BAD.push(m); else throw new Error(m); }
  return { start: +start.toFixed(2), end: +end.toFixed(2), from, to };
}

// SL-04 (2026-09-24). Dan picked A and F on 09-24 ("Let's do A, C, and F"; C vs D being
// confirmed, curls re-proposed as single-idea options). Titles are Dan-facing working titles.
// Each gives the viewer a takeaway: A which two muscles to prioritise, F the timed-set workout.
// Live-round pieces carry music only (no speech), so they are cut on explicit inAt/outAt
// and exempted from the speech-gap assertion by `music: true`.
const SEGMENTS = [
  {
    // REV 2 (Dan 2026-09-24): shoulders only. "Let's kill number one because of the triceps issue
    // and redo that one to make it focus on shoulders only" -> he picked option 2: the shoulders
    // talk plus the side-lateral SET-UP (weight + arm angle). The triceps talk is gone.
    id: 'A', slug: 'make-your-waist-look-smaller',
    title: 'Train Your Shoulders To Make Your Waist Look Smaller',
    pieces: [
      // inAt 27.60: "So, first of all," is dropped; VAD gap 27.57-27.71 sits before "you".
      piece('you want to be hitting your deltoids on a regular basis',
            'make your abs and your waist look better', { inAt: 27.60, outAt: 59.80 }),
      // inAt 213.15: gap 213.09-213.22 after "dumbbells."; "for this" resolves two lines later
      // ("So, with the side laterals"). outAt: gap 238.07-238.69 after "is what you want."
      piece("I'm doing 15 pounds", 'About that angle in your arms is what you want', { inAt: 213.15, outAt: 238.10 }),
    ],
  },
  {
    id: 'F', slug: 'two-minute-arm-pump',
    title: 'The 2-Minute Arm Pump Before You Take Your Shirt Off',
    pieces: [
      // inAt 100.40: Whisper inflates "This" to 99.98; VAD puts the first speech at 100.57.
      piece('This workout is also great to do before a photo shoot',
            'look visibly pumped and better when you take your shirt off', { inAt: 100.40, outAt: 114.80 }),
      piece('Like with most home workouts, I recommend time sets',
            'then do three or four rounds'),
      musicPiece(515.0, 519.0, 'live round: bicep curls'),
      musicPiece(546.0, 550.0, 'live round: side lateral raises'),
      musicPiece(575.3, 579.8, 'live round: overhead tricep extensions'),
    ],
  },
  {
    // Dan 2026-09-24 picked "raise your elbows, not your hands"; its set-up half moved into A.
    id: 'C', slug: 'raise-your-elbows-not-your-hands',
    title: 'Raise Your Elbows, Not Your Hands',
    pieces: [
      // REV 2 (reviewer 2026-09-24): open at "When they go to the top..." with Dan upright; the old
      // opening played the hook over his back while he set the weights down, and "the next mistake"
      // referred to a mistake this Short never set up. CTC puts "is" at 263.87-263.93 and "when" at
      // 264.37, and VAD measures silence 264.03-264.25.
      piece('when they go to the top', 'make sure there\'s no rocking', { inAt: 264.22, outAt: 292.62 }),
    ],
  },
  {
    // Curls option 1 (Dan 2026-09-24: "let's do 1 and 2").
    id: 'K', slug: 'stop-swinging-your-curls',
    title: 'Stop Swinging Your Curls',
    pieces: [
      // Split around Zeeshan's zoom-blur transition (sharpness drops 190.45-191.2): the 0.31 s of
      // silence 190.57-190.88 between "biceps." and "When" is removed, and the picture change
      // (card -> mid) sits on that join, so the blur is never on screen.
      piece('The most common mistake I see with the bicep curls', 'not really working your biceps', { inAt: 179.70, outAt: 190.57 }),
      piece('When you do your bicep curls', 'no momentum', { inAt: 190.88, outAt: 208.18 }),
    ],
  },
  {
    // Curls option 2, re-scoped so it does not repeat option 1: the two ways to curl and when to
    // use each (2:05-2:56), no swinging section.
    id: 'H', slug: 'how-to-do-bicep-curls',
    title: 'How To Do Bicep Curls',
    pieces: [
      piece("there's a couple different ways you can do these bicep curls", 'whichever way works the best for you is perfectly valid', { inAt: 125.20, outAt: 176.76 }),
    ],
  },
];

// HARD RULE for this batch: no source second may appear in two shorts.
{
  const spans = [];
  for (const s of SEGMENTS) for (const p of s.pieces) spans.push({ id: s.id, ...p });
  spans.sort((a, b) => a.start - b.start);
  for (let i = 1; i < spans.length; i++) {
    const ov = spans[i - 1].end - spans[i].start;
    // Two shorts that sit either side of the same pause share that pause's silence, so a
    // sub-frame overlap there is the SAME cut point, not repeated footage. Anything more is.
    if (ov > 0.001 && ov <= 0.35) {
      if (process.env.REPORT) console.log(`  (adjacent: ${spans[i - 1].id}/${spans[i].id} share ${ov.toFixed(2)}s of silence)`);
      continue;
    }
    if (ov > 0.001) {
      throw new Error(`source overlap: ${spans[i - 1].id} [${spans[i - 1].start}-${spans[i - 1].end}] ` +
        `and ${spans[i].id} [${spans[i].start}-${spans[i].end}]`);
    }
  }
}

module.exports = { SEGMENTS, words, find, BAD, SILENCE };
if (process.env.REPORT && BAD.length) { console.log('\nUNSNAPPED:'); BAD.forEach(b=>console.log('  '+b)); }


if (require.main === module) {
  let total = 0;
  for (const s of SEGMENTS) {
    const dur = s.pieces.reduce((a, p) => a + (p.end - p.start), 0);
    total += dur;
    console.log(`${s.id}  ${s.slug.padEnd(26)} ${dur.toFixed(1)}s  ${s.pieces.length} piece(s)`);
    for (const p of s.pieces) {
      const fmt = (t) => `${Math.floor(t / 60)}:${String((t % 60).toFixed(1)).padStart(4, '0')}`;
      // Print the real spoken words at each boundary so the cut can be checked, not assumed.
      // A word counts as spoken in the clip if most of it is inside. Anything only
      // partially included is a potential clipped syllable — report it rather than assume.
      const frac = (w) => {
        const dur = w.timestamp[1] - w.timestamp[0];
        if (dur <= 0) return 0;
        const ov = Math.min(w.timestamp[1], p.end) - Math.max(w.timestamp[0], p.start);
        return Math.max(0, ov) / dur;
      };
      const spoken = words.filter((w) => frac(w) > 0.5);
      const partial = words.filter((w) => frac(w) > 0.08 && frac(w) <= 0.5);
      const head = spoken.slice(0, 7).map((w) => w.text.trim()).join(' ');
      const tail = spoken.slice(-6).map((w) => w.text.trim()).join(' ');
      console.log(`      ${fmt(p.start)} -> ${fmt(p.end)}  (${(p.end - p.start).toFixed(1)}s)`);
      console.log(`        in : "${head} ..."`);
      console.log(`        out: "... ${tail}"`);
      if (partial.length) {
        console.log(`        ⚠ partial word audio: ${partial.map((w) =>
          `"${w.text.trim()}" ${(frac(w) * 100).toFixed(0)}%`).join(', ')}`);
      }
    }
  }
  console.log(`\ntotal ${total.toFixed(0)}s across ${SEGMENTS.length} shorts`);
}
