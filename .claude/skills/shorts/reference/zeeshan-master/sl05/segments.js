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

// SL-05 (2026-09-30). Dan: "I like all five." Every in/out below is MEASURED: speech-band envelope
// (work/env.py) + local Whisper small.en on the spliced audio (work/splice_test.py), not Whisper word marks.
// Titles are Dan-facing working titles; eyebrow/headline copy lives in plan.js META.
const SEGMENTS = [
  {
    id: 'S1', joinShortEnd: true, slug: 'deadlifts-cause-more-injuries',
    title: 'Deadlifts Cause More Injuries Than Every Other Lift',
    pieces: [
      // in 116.95: gap 116.52-117.03 ("The" voices 117.03). Zeeshan's zoom blur runs 116.77-117.13 (first sharp frame 117.167), so the plan holds that frame 7 frames.
      // round 2 (reviewer): in 116.95 -> 117.27. Zeeshan's zoom blur runs to ~117.3 and "The" (117.03-117.23) was spoken over a held ghost frame;
      // the short now opens on "Number one drawback..." ("number" voices 117.31), first frame Laplacian 172 vs 220 sharp.
      { start: 117.27, end: 139.75, from: 'number one drawback of deadlifts', to: 'high risk of injury exercise', measuredOut: true },
      // in 193.40: envelope -15 dB 193.12-193.56, "But" voices 193.60 (Whisper put it at 193.06, wrong).
      // Splice test: "It's really a high risk of injury exercise. But what you don't realize..."
      piece("But what you don't realize", 'This is how most people end up quitting', { inAt: 193.40, outAt: 227.80 }),
    ],
  },
  {
    id: 'S2', joinShortEnd: true, oneLine: [[33.0, 60, 24]],   // the close shot under the 4-line bar: no two-line captions (round-4 review: 'periodically / getting injured and' sat on his chin)
    slug: 'safer-lifts-build-more-muscle',
    title: 'Safer Lifts Build MORE Muscle Long Term',
    pieces: [
      // the cold open over Zeeshan's labelled AI deadlift clip; "deadlifts." ends 2.62, gap 2.70-3.10
      { start: 0.45, end: 2.95, from: 'Stop doing deadlifts', to: 'Stop doing deadlifts', measuredOut: true },  // round 2: 0.76 s of silence before "Stop" trimmed to 0.31  // file start
      // gap 240.29-240.96 before "Now, avoiding"
      piece('Now, avoiding injuries is very important', 'you will actually build more muscle with the safer exercises', { inAt: 240.74, outAt: 288.44 }  /* round 2: 288.74 -> 288.44, "exercises." ends 288.40 (gap to 288.91); less of Zeeshan's blur-out */),
    ],
  },
  {
    id: 'S3', joinShortEnd: true, lastCueToEnd: true, slug: 'deadlifts-build-a-powerlifter-body',
    title: 'Deadlifts Build A Powerlifter Body, Not An Aesthetic One',
    pieces: [
      piece('Deadlifts build a thick power lifter', 'we want to be ripped', { inAt: 295.68, outAt: 316.08 }),
      // in 324.87: the 20 ms trough between "that." (324.77-324.86) and "If" (from 324.89), -16 dB.
      // Splice test: "...we want to be ripped. If you use a very narrow grip, then..."
      // round 2: out 338.61 -> 338.31. 338.61 kept a quiet "You can" (CTC 338.51-338.73, captioned "You") and 8 frames of
      // Zeeshan's zoom blur (Laplacian 214 -> 44 from 338.07); 338.31 is inside the VAD gap 338.27-338.81 after "direction." (338.27).
      /* round 2b (reviewer, by envelope): out back to 338.61. "direc-" ends 338.26, the "sh" runs 338.28-338.48, the "-n" 338.50-338.56, trough 338.60-338.62, "You" from 338.64; 338.31 clipped the word to "direct". The caption "You" came from a CTC time on the "-tion" (re-timed in words_aligned). */
      /* round 2d (two reviewers, envelope + CTC): out 338.46. The "sh" of "direction" runs to 338.48 and a bump at 338.50-338.57 reads as the next word "You" on CTC and the spectrogram; 338.31 gave "direct", 338.61 let "You" in. */
      { start: 321.60, end: 338.46,   /* round 2 (reviewer: the short never said what is being gripped): in 324.87 -> 321.60, adding "Now, there are ways with your deadlift that you can counteract that." (gap 321.21-321.71) */ from: 'Now, there are ways with your deadlift', to: 'less in that power lifter direction', measuredOut: true },
      // in 349.80: dip 349.72-349.88 after "aesthetics.", "If" voices 349.90
      // out 363.56: the one silence Short 3 and Short 4 share (363.50-363.62, "better." ends 363.48, "So" 363.64)
      piece('If you care about aesthetics', 'better for making you look better', { inAt: 349.88, outAt: 363.525 }  /* round 2e (reviewer, 5-12 kHz band): in 349.80 -> 349.88, the "s" of the previous word "aesthetics" ran 349.81-349.87; out 363.525, "better" ends 363.51 and the "s" of "So" starts 363.525 */  /* round 2: 363.56 -> 363.50, Zeeshan's own cut sits at 363.53 and left two stray frames */),
    ],
  },
  {
    id: 'S4', joinShortEnd: true, slug: 'two-back-exercises-instead-of-deadlifts',
    title: '2 Back Exercises To Do Instead Of Deadlifts',
    pieces: [
      // out 369.38: "instead?" tail ends 369.35, "I'm" voices 369.41 (trough -7 dB, 369.37-369.39)
      { start: 363.56, end: 369.38, from: "So if I've convinced you", to: 'what should you be doing instead', measuredOut: true },
      // in 374.08: gap 373.91-374.14 before "So with the T-bar row". Splice test reads
      // "...what should you be doing instead? So with the T-bar row, what you're going to..."
      piece('So with the T -bar row', 'build those lats', { inAt: 374.08, outAt: 427.40 }),
    ],
  },
  {
    id: 'S5', joinShortEnd: true, capLow: [[31.70, 35.79]], breakBefore: [34.42, 35.21, 35.82, 36.73, 37.49],   // one-line cues in the tight close: 'with deadlifts | building more muscle | to begin with' (round-4 review: the two-line cue reached his chin);   // captions drop to the old line (MarginV 330) on the MID close, where no bar is up: at 520 they sat on his chin (round-3 review)
    slug: 'train-legs-without-deadlifts',
    title: 'Train Legs Without Deadlifts',
    pieces: [
      // in 427.90: "Now," is dropped (voiced 427.46-427.80, dip -8 dB 427.84-427.96, "deadlifts" from 427.98).
      // Junk pass: the stutter "but, but" (463.52-464.00) is cut 463.70-464.05; splice reads
      // "...building more muscle to begin with, then periodically getting injured and getting set back."
      { start: 427.90, end: 463.70, from: 'deadlifts are also powerful', to: 'to begin with but', measuredOut: true },
      // round 2: out 466.69 -> 466.52: 466.69 carried a soft "The" (Whisper 466.50-466.58, CTC 466.61) from the next sentence; "back." ends 466.45
      { start: 464.05, end: 466.56, from: 'then periodically getting injured', to: 'getting set back', measuredOut: true, continues: true, junkCut: [463.70, 464.05] },
    ],
  },
];

// Round-1 look sample (SL05_SAMPLE=1): the first ~9 s of Short 1, to "...in the gyms." (gap 125.51-126.28).
if (process.env.SL05_SAMPLE) {
  const s1 = SEGMENTS.find((s) => s.id === 'S1');
  SEGMENTS.length = 0;
  SEGMENTS.push({ ...s1, pieces: [{ ...s1.pieces[0], end: 125.90, to: 'most common way that people get injured in the gyms' }] });
}

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
