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

// REV 2 (2026-08-28): FIVE shorts. Dan cut the sixth - the standing bodybuilder variation -
// outright: "This is essentially an example of what not to do, but it doesn't really make
// sense in this video." Its source range 55.48-62.10 and 252.03-277.07 is now unused.
//
// FIVE shorts from the ab-wheel cut. Chosen so that NO SECOND OF SOURCE IS USED TWICE —
// Dan's requirement was six that do not annoy a viewer who sees all of them. Verified by
// the overlap assertion below, which throws rather than warns.
//
// Each one carries a takeaway the VIEWER walks away with (skill Step 2's hard rule):
//   A tension vs a crunch · B which muscles it hits · C the two form faults ·
//   D tempo · E how far to roll at your level.
const SEGMENTS = [
  {
    id: 'A', slug: 'ab-wheel-beats-crunches',
    title: 'Why The $17 Ab Wheel Beats Crunches',
    pieces: [
      // outAt: his cut blooms to white 12.61-13.95 as the section changes. The snap would
      // land the out at 12.72, i.e. ON the white frame. Speech is over at 12.27 (VAD).
      piece('This $17 infomercial gimmick is one of the best pieces of equipment',
            'most things sold on infomercial are scams', { outAt: 12.52 }),
      // outAt: same reason - the next bloom runs 43.38-44.98. 43.30 is 0.12s of tail on a
      // word VAD puts down at 43.18, and the frame there is 5% over base, invisible.
      // inAt: the rev-2 transcript times "So" 0.5s later than the rev-1 one did and the snap
      // then clipped 46% off "let's". 22.12 is the rev-1 in-point and sits inside the measured
      // gap 21.67-22.34, so the approved opening is reproduced exactly.
      piece("talk about why the ab wheel is so awesome",
            "That's why the ab wheel beats crunches", { inAt: 22.12, outAt: 43.30 }),
    ],
  },
  {
    id: 'B', slug: 'hits-every-ab-muscle',
    title: 'This Hits Every Ab Muscle At Once',
    pieces: [
      // inAt: this section is entered THROUGH a white bloom (peak 64.5, resolved by 64.62).
      // Whisper starts "This" at 64.40 but VAD puts the first speech at 64.60, so opening at
      // 64.50 costs no syllable and the flash resolving into Dan reads as a designed open.
      piece('This ab wheel is also going to hit all of your ab muscles at once',
            'a great total ab exercise', { inAt: 64.50 }),
    ],
  },
  {
    id: 'C', slug: 'biggest-ab-wheel-mistake',
    title: 'The Biggest Ab Wheel Mistake',
    pieces: [
      piece("So when you're doing this, you want to start in this position",
            'So locked out arms and straight back'),
    ],
  },
  {
    id: 'D', slug: 'youre-rolling-too-fast',
    title: "You're Rolling Out Way Too Fast",
    pieces: [
      piece('Next detail here, you wanna roll out slowly and with control',
            'enable you to get a lot more out of this exercise'),
    ],
  },
  {
    id: 'E', slug: 'beginner-to-advanced',
    title: 'Beginner To Advanced Ab Rollout',
    pieces: [
      piece("So let's talk about how to do this if you're a beginner",
            "until you're all the way at full extension"),
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
