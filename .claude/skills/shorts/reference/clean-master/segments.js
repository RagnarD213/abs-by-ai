// Precise in/out points for the supplements Shorts, resolved against Whisper word
// timestamps (never the 820-cue delivered SRT, which is cue-level, not word-level).
const fs = require('fs');
const path = require('path');

const words = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'work', 'words.json'), 'utf8')
).chunks;

const norm = (s) => s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
// ⚠ Some tokens normalise to NOTHING - Whisper emits "%" as its own word, so "70%" arrives
// as ["70", "%"]. Joining every token unconditionally put a DOUBLE space in the search text
// ("70  of people"), and no phrase containing a percentage could ever be found. Build the
// search text from non-empty tokens only, keeping each one's original word index so the
// in/out points still resolve to the right word.
const offsets = [];
const parts = [];
{
  let pos = 0;
  words.forEach((w, i) => {
    const t = norm(w.text);
    if (!t) return;
    offsets.push({ start: pos, end: pos + t.length, i });
    parts.push(t);
    pos += t.length + 1;
  });
}
const flat = parts.join(' ');
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

// Cut-point ground truth: the INTERSECTION of work/vad.py's speech-band map and plain
// silencedetect -26dB/0.05 (work/gaps.py). Unlike the ab-wheel source this cut has NO music
// bed, so silencedetect is valid here and comes for free as an independent control; the two
// agree on 85% of silencedetect's intervals. Intersecting them means every cut point is both
// "nobody is talking" and "nothing is audible". 1083 confirmed gaps, 244.6s, median 0.154s.
const SILENCE = JSON.parse(fs.readFileSync(path.join(__dirname, 'work', 'gaps.json'), 'utf8'));

const inGap = (t) => SILENCE.some(([a, b]) => t >= a - 0.02 && t <= b + 0.02);

// Cut point just BEFORE speech starts at `t`. `floor` is the end of the previous word:
// the snap may never cross it, or a sub-threshold gap between two sentences sends the
// search back past a whole phrase.
function snapIn(t, floor, preroll = 0.22) {
  let best = null;
  for (const [a, b] of SILENCE) {
    if (a > t + 0.25) break;
    if (b < floor - 0.35) continue;
    // A gap that ENDS before the word's claimed start is the normal case.
    // ⚠ A gap that CONTAINS the claimed start is the other one, and it has to be accepted or
    // the snap walks back to the previous pause and swallows a whole sentence. Whisper
    // stretches short words backwards across real pauses (the skill records "the" spanning a
    // measured silence on V6); here it timed E's opening "So" at 996.24 while the measured
    // pause runs to 996.708, and without this clause E opened on "...from there. So this is
    // the biggest mistake" - a fragment of the previous sentence. When the claimed start is
    // inside measured silence, the word really begins at the gap's END.
    if (b <= t + 0.25 || (a <= t + 0.05 && b > t)) best = [a, b];
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


// ---------------------------------------------------------------------------------------
// A piece taken from the RAW ROLL instead of the master. Rev 2 only: Dan asked for a better
// take on E's opening line and the alternative is a take the editor discarded, so it exists
// only in C1514.MP4. Its words come from the raw roll's own transcript. `pre` is how much
// silence to hold before the first word.
const RAWW = (() => {
  const d = JSON.parse(fs.readFileSync(require('./config.js').RAW_WORDS, 'utf8'));
  const segs = d.segments || d;
  const out = [];
  for (const s of segs) for (const w of (s.words || []))
    out.push({ text: w.word, timestamp: [w.start, w.end] });
  return out;
})();
function rawPiece(from, to, { pre = 0.20, tail = 0.30 } = {}) {
  const norm = (x) => x.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
  // ⚠ Keep the index map. Filtering empty tokens out of the search list while indexing back
  // into the UNFILTERED one put this phrase 2.2s early - the same off-by-N that the "%" token
  // caused in the master's own phrase finder.
  const flat = [], map = [];
  RAWW.forEach((w, i) => { const t = norm(w.text); if (t) { flat.push(t); map.push(i); } });
  const idx = (phrase) => {
    const p = norm(phrase).split(' ');
    for (let i = 0; i + p.length <= flat.length; i++)
      if (p.every((t, k) => flat[i + k] === t)) return i;
    throw new Error(`raw phrase not found: "${phrase}"`);
  };
  const a = idx(from), b = idx(to) + norm(to).split(' ').length - 1;
  const start = +(RAWW[map[a]].timestamp[0] - pre).toFixed(3);
  const end = +(RAWW[map[b]].timestamp[1] + tail).toFixed(3);
  const words = RAWW.filter((w) => w.timestamp[1] > start && w.timestamp[0] < end)
    .map((w) => ({ text: w.text, timestamp: [w.timestamp[0], w.timestamp[1]] }));
  return { start, end, from, to, src: 'raw', words };
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

// EIGHT shorts from the supplements long-form. REV 2 — Dan's notes of 2026-08-28.
//
// ⚠ EVERY JOIN IN THIS FILE IS DELIBERATE AND EVERY ONE IS HIDDEN BY A PUNCH (plan.js).
// Dan flagged four "awkward cut"/"jump cut" timecodes and two "junk footage" ones; a scan
// found 8 inherited source splices and 14 pauses over 0.55s across the batch. Measured, a
// pause removal jumps the picture as much as an inherited splice does (4.97-12.46 against a
// 1.30 adjacent-frame baseline), because he moves while he is not talking — so pauses are
// removed only where they are genuinely long, and every resulting join alternates wide/tight.
const SEGMENTS = [
  {
    id: 'B', slug: 'the-3-supplements-that-matter',
    title: 'The 3 Supplements That Actually Matter',
    pieces: [
      // ⚠ REV 3, Dan: "still has that junk take in the beginning, from 000 to 001". Rev 2 cut
      // the 0.95s hesitation but KEPT the fragment either side of it, so the short opened on
      // "So let's say" alone - 1.1s of him mid-gesture with his eyes up, then a cut. The whole
      // fragment is gone now and the short opens on the line itself, which is also a stronger
      // hook: a direct statement and a question rather than a hypothetical.
      // outAt: the source splices to the next beat at 1088.46 and running past it would
      // inherit a jump cut in the last quarter second.
      piece("you're taking nothing right now",
            "that's a totally fine supplement stack to start with",
            { inAt: 1047.88, outAt: 1088.42 }),
    ],
  },
  {
    id: 'E', slug: 'stop-buying-a-big-supplement-stack',
    title: 'Stop Buying A Big Supplement Stack',
    pieces: [
      // ⚠ REV 2, Dan: "the take used was a little bit awkward. See if you can find a better
      // take for the first 3 seconds." There is one, and it is only in the raw roll — the
      // editor discarded it. In the used take he opens looking down with a half-lidded
      // expression; in this one he holds eye contact throughout. Its line also reads better
      // straight into "I bought a huge stack like this".
      rawPiece('So I would have to say the biggest mistake I made when taking supplements is',
               'So I would have to say the biggest mistake I made when taking supplements is',
               { tail: 0.22 }),
      piece('I bought a huge stack like this', "I just wasn't consistent"),
      // the 0.75s pause after "consistent." is the longest in this short
      piece("It's better to take one or two supplements", 'then add in another one'),
    ],
  },
  {
    id: 'J', slug: 'why-men-must-take-vitamin-d',
    title: 'Why Men Must Take Vitamin D',
    pieces: [
      piece('vitamin D. Critically, critically important',
            'vitamin D. Critically, critically important'),
      piece('about 70% of people are deficient in vitamin D',
            'So many benefits just from daily vitamin D supplementation'),
      piece('I recommend Athletic Greens liquid vitamin D',
            'you should be taking more than what they recommend'),
    ],
  },
  {
    id: 'A', slug: 'let-ai-pick-your-supplements',
    title: 'Let AI Pick Your Supplements',
    pieces: [
      piece('You are not smart enough to understand scientific research',
            "Yet I still don't trust myself to analyze the scientific research"),
      piece('That is where AI comes in',
            'AI can read all scientific research ever done', { tail: 0.08 }),
      piece("Don't get supplement recommendations from your ripped friend",
            'the ultimate authority, AI', { tail: 0.15 }),
    ],
  },
  {
    id: 'M', slug: 'why-test-boosters-matter-least',
    title: 'Why Test Boosters Are The Least Important Supplement',
    pieces: [
      piece("out of everything that I'm taking",
            'it has other health benefits too', { preroll: 0.12 }),
      // ⚠ REV 2, Dan: "an unnecessarily large, long pause at 0:35. That is junk footage."
      // Measured at 1.24s — the longest in the batch. Removed here.
      // outAt: the source splices at 724.03 and the old cut ran 0.27s past it.
      piece('And then finally, it has zinc',
            'recommend the zinc part of this to everybody', { outAt: 724.00 }),
    ],
  },
  {
    id: 'C', slug: 'if-you-take-one-take-fish-oil',
    title: 'If You Take One Supplement, Take Fish Oil',
    pieces: [
      piece('Fish oil is one of the most important supplements',
            'If you\'re only going to take one supplement, it should be fish oil'),
      // ⚠ REV 2, Dan: "There's an awkward cut at 0:26." Measured: the source splice at 446.68
      // lands INSIDE the word "Especially," (446.62-447.02), so the delivered audio was a
      // half-word followed by the next take restarting on the same word. Both the stutter and
      // the splice are cut out here; the short keeps one clean "especially".
      piece('Fish oil improves your heart health',
            'the most proven supplement that you can take', { outAt: 446.66 }),
      piece("especially if you're not eating a lot of fish right now",
            'you have to be taking fish oil', { inAt: 447.08 }),
    ],
  },
  {
    id: 'H', slug: 'you-should-be-taking-creatine',
    title: 'You Should Be Taking Creatine',
    pieces: [
      // ⚠ REV 2, Dan: "There's junk footage and an awkward cut at 0:10." Measured: the source
      // splices at 946.31 into a 0.28s dead spot, and the take either side REPEATS "for muscle
      // building". Cutting the whole "and not just for muscle building," clause removes the
      // repetition, the dead air and the inherited jump cut at once, and the sentence still
      // lists all three benefits.
      piece("one other supplement that I don't personally take",
            'Creatine is proven to have tremendous benefits for muscle building',
            { outAt: 945.26 }),
      piece('for your brain health and your heart health as well at higher doses',
            'the level of diarrhea and gas that I get', { inAt: 948.10 }),
      piece('For you, though, that probably', 'unless you have stomach issues'),
    ],
  },
  {
    id: 'D', slug: 'supplements-are-only-5-percent',
    title: 'Supplements Are Only 5% Of Your Results',
    pieces: [
      piece('Supplements are only about 5% of your overall results',
            "It's only about 5%"),
      piece('On the other hand, though',
            'so I always iron my clothes before I go out on a date'),
      // outAt: the source splices at 1302.50 and the old cut ran 0.3s past it.
      piece('For that same reason', "compared to the benefit you're getting",
            { outAt: 1302.44 }),
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
