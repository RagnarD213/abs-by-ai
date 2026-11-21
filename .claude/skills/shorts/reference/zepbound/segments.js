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
  const rw = require('./config.js').RAW_WORDS;
  // No raw-roll transcript for this batch (the Zepbound roll C1513 has never been transcribed
  // at word level) - rawPiece() is simply unavailable until one exists.
  if (!rw || !fs.existsSync(rw)) return [];
  const d = JSON.parse(fs.readFileSync(rw, 'utf8'));
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

// EIGHT shorts from "02 - My Honest Zepbound Update". Picked for a viewer takeaway each (a
// tactic, a number, a decision), never for "Dan is in shape". Every join is either an inherited
// source splice or a removed false start / clause, and every one is hidden by the punch
// alternation in plan.js. Dan said "cut 6-8" and is not at the keyboard, so these are MY picks
// from a 14-candidate shortlist (in SHORTS.md) - any swap is a re-render of one short.

// ⚠ EVERY PIECE END THAT RAN PAST A SOURCE SPLICE IS PINNED WITH outAt (and two heads with inAt).
// The long-form edit cut its pauses tight, so the pause after a beat's last word IS the join,
// and snapOut's 0.34s tail walked 0.04-0.30s into the next take on eleven boundaries - a
// one-to-nine-frame flash of a different take right before the cut. Each override sits inside the
// measured gap and 20 ms before the frame-measured splice (work/splices.json). The silence
// assertion still applies to every override.
const SEGMENTS = [
  {
    id: 'A', slug: 'the-shot-that-killed-my-urge-to-drink',
    title: 'The Shot That Killed My Urge To Drink',
    pieces: [
      // his own "knockout argument" line is the hook
      piece('The biggest reason, the knockout argument', "Most weeks I'd be more towards the 10 side", { outAt: 615.90 }),
      // ⚠ TWO TAKES, ONE SENTENCE. Take 1 (616.1) runs "That means going out on dates having one or
      // two and then having a blowout party night where we..." and dies; take 2 (621.4) restarts
      // "That means having, going out on dates..." with a stumble and no measured gap before
      // "going". Neither take is clean end to end, so the sentence is built from the clean half of
      // each: take 1 up to the measured gap after "two" (618.36-618.60), take 2 from the gap inside
      // its "and" (623.90-624.20) onward. Both joins are inside confirmed silence.
      // outAt 618.45: Whisper times the following "and" from 618.30 while measured silence runs
      // 618.36-618.60, i.e. the word really starts at the gap's end. Cutting at 618.45 keeps it
      // under 50% inside so it is neither heard nor captioned here (it is spoken in the next piece).
      piece('That means going out on dates having one or two', 'That means going out on dates having one or two',
            { outAt: 618.45 , inAt: 615.94 }),
      piece('and then having a blowout party night maybe once or twice per week',
            'eliminated those blowout party nights altogether'),
      // ⚠ second false start removed: "I don't even feel the need to have more than one or two
      // drinks when I..." (633.8) restarts complete at 637.6.
      piece("I don't even feel the need to have more than one or two drinks when I go out",
            'consider Zepbound as a means to reduce that', { outAt: 651.13 }),
    ],
  },
  {
    id: 'B', slug: 'inject-thursday-evening',
    title: 'Inject Thursday Evening. Here Is Why',
    pieces: [
      piece('So I have found the optimal time for me to inject', 'That is the best time', { outAt: 1244.09 }),
    ],
  },
  {
    id: 'C', slug: 'start-at-1-mg-not-2-5',
    title: 'Start Your GLP-1 At 1 Mg, Not 2.5',
    pieces: [
      piece('So if I was going back in time and I was doing this again',
            "I don't think they're correct about that though", { outAt: 1316.66 }),
      // the "for context, the maximum dose ... 15 milligrams" aside (1317-1329) is dropped
      piece('The reason I would start like that though',
            'Two to 2.5 you won\'t have any of these side effects', { outAt: 1356.17 }),
    ],
  },
  {
    id: 'D', slug: 'why-the-needle-beats-the-pen',
    title: 'Why The Needle Beats The Pen',
    pieces: [
      piece('Next thing is you have to decide do you want a quick pen or a needle',
            'transition into the needle for a couple different reasons'),
      // junkscan: a 2.13s dead stretch (1014.77-1016.90) between "reasons." and "The needle is
      // superior" - the longest pause in the batch, removed; the join is hidden by the punch.
      piece('The needle is superior to the quick pen',
            'you can adjust your dose very subtly as necessary'),
    ],
  },
  {
    id: 'E', slug: 'dont-go-above-2-5-mg',
    title: "Don't Go Above 2.5 Mg",
    pieces: [
      piece("Here's another mistake I made on Zepbound which I want you to avoid",
            'more necessary for people who are of severe obesity', { inAt: 1543.35 }),
      // "They need to deal with those side effects because if they don't, if they don't lose that
      // weight quickly they're going to die..." (1568-1577) dropped: a stumble, and it lands the
      // short under 60s.
      piece('You though are probably not obese', 'get the same results in the end', { outAt: 1594.54 }),
      // a stray "Legitimately," (1594.9-1595.3) - a false start before the real sentence - sits
      // between two measured gaps and is cut out.
      piece("I would say that unless you're legitimately obese", 'I would not recommend going above 2.5'),
    ],
  },
  {
    id: 'F', slug: 'lose-fat-not-muscle-the-protein-target',
    title: 'Lose Fat, Not Muscle: The Protein Target',
    pieces: [
      piece("Okay so let's talk about the biggest risk to your physique",
            "you haven't really accomplished anything"),
      // the bulk/cut-cycle riff (1641-1653) is dropped to land under 60s
      piece('So because of this on the Zetbound, consuming fewer calories',
            'then you can hit your protein for the day', { outAt: 1699.01 }),
    ],
  },
  {
    id: 'G', slug: 'compounded-vs-brand-name',
    title: 'Compounded Vs Brand Name',
    pieces: [
      piece('You can get shady, compounded Zepbound', "that's probably the highest quality product"),
      // the legal-status riff (804-825) is dropped
      piece('Compounded Zepbound is going to be cheaper', 'worth spending the extra money on brand name', { outAt: 866.55 }),
    ],
  },
  {
    id: 'H', slug: 'why-i-take-a-glp-1-with-six-pack-abs',
    title: 'Why I Take A GLP-1 With Six Pack Abs',
    pieces: [
      // opens on "Everyone should take Zepbound, even people who are already ripped" - the
      // strongest hook in the video - and carries the not-medical-advice beat in full.
      // measured gap 423.83-424.33 sits right before "everyone"
      piece('everyone should take Zepbound, even people who are already ripped',
            'that is a very, very realistic result to get', { outAt: 468.88 }),
      // "So my old flawed thinking was..." (469-477) dropped
      piece("If you're ripped and you take Zepbound, you're not sacrificing your health",
            'simultaneously making your appearance better'),
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
