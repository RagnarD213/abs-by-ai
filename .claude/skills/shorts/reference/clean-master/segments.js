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

// EIGHT shorts from the supplements long-form. Dan asked for the eight strongest of the
// 14 researched candidates; the letters are the shortlist's
// (Handoffs/assets/shorts-supplements-20260828/shortlist.md).
//
// Not built, and why: [F] ends on a Zepbound recommendation and Dan did not rule on the drug
// name; [I] carries "I just uncontrollably shit myself" AND a sentence that does not parse as
// transcribed; [L] needs a 248->180 word trim and names a third-party influencer; [N] is the
// bragging failure mode that killed v6-short1; [K] is the least distinctive; [P] is 29s.
//
// Every one hands the VIEWER something (skill Step 2's hard rule):
//   B the three to start with · A a method for choosing · E how to build the habit ·
//   D how much supplements actually matter · C which single one · J the dose ·
//   M which part of a test booster works · H the one he does not take but you should.
const SEGMENTS = [
  {
    id: 'B', slug: 'the-3-supplements-that-matter',
    title: 'The 3 Supplements That Actually Matter',
    pieces: [
      // Opens on his own question rather than the answer - "So let's say you're taking
      // nothing right now. How should you get started?" is the scroll-stopper and it needs
      // no context. Ends on "a totally fine supplement stack to start with", which closes
      // the loop; the next sentence starts the step-2 sequence and belongs to the long-form.
      piece("So let's say you're taking nothing right now",
            "that's a totally fine supplement stack to start with"),
    ],
  },
  {
    id: 'A', slug: 'let-ai-pick-your-supplements',
    title: 'Let AI Pick Your Supplements',
    pieces: [
      piece('You are not smart enough to understand scientific research',
            "Yet I still don't trust myself to analyze the scientific research"),
      // 78-98s is 20s of elaboration on the same point (nutrition scientists, "so much
      // research out there"). Cut: the short states the problem once and moves to the fix.
      piece('That is where AI comes in',
            'AI can read all scientific research ever done', { tail: 0.08 }),
      // ⚠ THE SOURCE CONTAINS A FALSE START HERE AND IT SURVIVED INTO THE DELIVERED MASTER:
      // "Don't get supplement recommendations from your..." (125.67-127.84), a 0.78s pause,
      // then the real take. Starting on the SECOND occurrence removes it. The phrase is
      // unique as written because the first attempt never reaches "ripped friend".
      piece("Don't get supplement recommendations from your ripped friend",
            'the ultimate authority, AI', { tail: 0.15 }),
    ],
  },
  {
    id: 'E', slug: 'stop-buying-a-big-supplement-stack',
    title: 'Stop Buying A Big Supplement Stack',
    pieces: [
      // Ends at "add in another one" rather than running to "add new supplements in slowly",
      // which is a restatement AND is where B starts - so the two shorts do not overlap.
      piece('So this is the biggest mistake I made when first getting into supplements',
            'then add in another one'),
    ],
  },
  {
    id: 'D', slug: 'supplements-are-only-5-percent',
    title: 'Supplements Are Only 5% Of Your Results',
    pieces: [
      // ⚠ ONE PIECE, NOT TWO, AND THE MEASUREMENT DECIDED IT. The plan was to cut the hook
      // line and splice past "We just went into all this" (a long-form reference), but the
      // 0.46s between "overall results." and "We" is NOT confirmed silence - it is a breath,
      // and both detectors agree, so no cut can be placed there without clipping. Keeping the
      // clause costs one mildly long-form-ish phrase and buys a take with no splice at all,
      // at 57s - dead centre of the 45-60s band the organic research found.
      // Trimmed at the head instead: "here's the bigger point that I do wanna emphasize
      // before I wrap up this video, guys" is dropped, so the short opens on the claim.
      piece('Supplements are only about 5% of your overall results',
            "compared to the benefit you're getting"),
    ],
  },
  {
    id: 'C', slug: 'if-you-take-one-take-fish-oil',
    title: 'If You Take One Supplement, Take Fish Oil',
    pieces: [
      // Trims the leading "...recommended by AI for those reasons", which is the tail of the
      // Thorne beat before it.
      piece('Fish oil is one of the most important supplements',
            'you have to be taking fish oil'),
    ],
  },
  {
    id: 'J', slug: 'you-need-5x-more-vitamin-d',
    title: 'You Need 5x More Vitamin D',
    pieces: [
      // ⚠ A 0.5s filler sits between these two pieces: Whisper hears "And B," at 286.34-286.86
      // with a 1.08s pause after it. Splicing it out joins two complete sentences and gives
      // the short a clean stat hook. Also drops "let's talk about the next supplement", which
      // only makes sense inside the long-form.
      piece('vitamin D. Critically, critically important',
            'vitamin D. Critically, critically important'),
      piece('about 70% of people are deficient in vitamin D',
            'you should be taking more than what they recommend'),
    ],
  },
  {
    id: 'M', slug: 'the-supplement-that-does-nothing',
    title: 'The Supplement That Does Almost Nothing',
    pieces: [
      piece("out of everything that I'm taking",
            'recommend the zinc part of this to everybody', { preroll: 0.12 }),
    ],
  },
  {
    id: 'H', slug: 'you-should-be-taking-creatine',
    title: 'You Should Be Taking Creatine',
    pieces: [
      // Trims the leading "...and more sleep overall", the tail of the deep-sleep beat.
      piece("one other supplement that I don't personally take",
            'unless you have stomach issues'),
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
