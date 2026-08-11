// Precise in/out points for the V2 Shorts, resolved against Whisper word timestamps
// (never the rounded sentence marks in v2-transcript.txt).
const fs = require('fs');
const path = require('path');

const words = JSON.parse(
  fs.readFileSync(path.join(__dirname, '<slug>-words.json'  // set per video), 'utf8')
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

// Real silence intervals measured from the source audio (silencedetect -32dB, 0.12s).
// Whisper's word timestamps are contiguous, so there is no gap to pad into — padding
// outward always clips a partial syllable off the neighbouring word. Cutting inside
// measured silence is the only way to get a clean in/out.
const SILENCE = (() => {
  const txt = fs.readFileSync(path.join(__dirname, 'silence.txt'), 'utf8');
  const out = [];
  let open = null;
  for (const line of txt.split('\n')) {
    const s = line.match(/silence_start:\s*([\d.]+)/);
    const e = line.match(/silence_end:\s*([\d.]+)/);
    if (s) open = parseFloat(s[1]);
    else if (e && open !== null) { out.push([open, parseFloat(e[1])]); open = null; }
  }
  return out;
})();

// Cut point just BEFORE speech starts at `t`. `floor` is the end of the previous word:
// the snap may never cross it, or a sub-threshold gap between two sentences sends the
// search back past a whole phrase (this is what dragged "...they get started" into D).
//
// The lookahead is deliberately TIGHT (0.20). Widening it to catch pauses hidden inside
// Whisper-inflated words was tried and is WORSE: it starts the clip 0.3-0.5s late and
// clips the first word instead ("This" 48%, "use" 47%). Where a boundary has no measured
// silence, move the editorial in/out point to where Dan actually breathes -- or set
// inAt/outAt explicitly -- rather than loosening this.
function snapIn(t, floor, preroll = 0.22) {
  let best = null;
  for (const [a, b] of SILENCE) {
    if (b > t + 0.20) break;
    if (b >= floor - 0.05) best = [a, b];
  }
  if (!best) return Math.max(0, floor, t - 0.10);
  return Math.max(best[0], best[1] - preroll, floor - 0.05);
}

// Cut point just AFTER speech ends at `t`. `ceil` is the start of the next word.
function snapOut(t, ceil, tail = 0.34) {
  for (const [a, b] of SILENCE) {
    if (a < t - 0.20) continue;
    if (a > ceil + 0.05) break;
    return Math.min(b, a + tail, ceil + 0.05);
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
  const inSilence = (t) => SILENCE.some(([a, b]) => t >= a - 0.02 && t <= b + 0.02);
  if (!inSilence(start)) { const m = `IN cut ${start.toFixed(2)}s not in silence: "${from}"`;
    if (process.env.REPORT) BAD.push(m); else throw new Error(m); }
  if (!inSilence(end)) { const m = `OUT cut ${end.toFixed(2)}s not in silence: "${to}"`;
    if (process.env.REPORT) BAD.push(m); else throw new Error(m); }
  return { start: +start.toFixed(2), end: +end.toFixed(2), from, to };
}

const SEGMENTS = [
  {
    id: 'A', slug: 'no-abs-until-you-see-abs',
    title: 'Stop Doing Ab Exercises',
    pieces: [
      piece("don't do any ab exercises until you can see your abs",
            'to save you a whole lot of time', { inAt: 126.14 }),
      piece("But if you're fat, on the other hand", "that's what generates that effect"),
    ],
  },
  {
    id: 'B', slug: 'vacuum-exercises',
    title: 'Do This Instead Of Crunches',
    pieces: [piece('use vacuum exercises instead of traditional ab exercises',
                   'that will make your belly fat look smaller', { inAt: 247.88 })],
  },
  {
    id: 'C', slug: 'bubble-gut-vacuums',
    title: 'Why Bodybuilders Suck Their Stomach In',
    pieces: [piece('Furthermore, the type of people who do this ab exercise are typically bodybuilders',
                   "it's just that beginners typically don't do it")],
  },
  {
    id: 'D', slug: 'liquid-calories-milk',
    title: 'Milk Is Not A Health Food',
    pieces: [piece('avoid all liquid calories, including protein shakes',
                   "That's why I don't consume any milk")],
  },
  {
    id: 'E', slug: 'whey-protein-insulin',
    title: 'Whey Protein Is Making You Fat',
    // Must include the leading "Now," -- without it the previous-word floor sits AFTER
    // the 477.43-477.70 pause and snapIn falls through to its no-silence fallback.
    pieces: [piece("Now, a lot of people don't know this, but whey protein can actually spike your insulin",
                   'you should avoid the whey protein and any kind of liquid calorie')],
  },
  {
    id: 'F', slug: 'jelly-bean-vs-soda',
    title: 'Jelly Beans Beat Soda',
    pieces: [piece("And here's a study to kind of drive this home for you guys",
                   'the same amount of sugar and solid calories')],
  },
  {
    id: 'G', slug: 'fast-until-2pm',
    title: 'Why I Skip Breakfast Every Day',
    pieces: [
      piece('fast until 2 p.m.', 'come down to consuming fewer calories'),
      piece('On the other hand, if you fast until 2 p.m., skip breakfast',
            'to sustain a lean body and six pack abs'),
    ],
  },
  {
    id: 'H', slug: 'break-fast-low-carb',
    title: 'Never Start Your Day With Carbs',
    pieces: [
      piece('break your fast with a low-carb meal or salad',
            "here's why you want to do this"),
      piece('If you break your fast with a low carb meal', 'you break that cycle'),
    ],
  },
  {
    id: 'I', slug: 'weigh-yourself-every-day',
    title: 'If You Ain\'t Tracking, You\'re Slacking',
    pieces: [
      piece('weigh yourself every day, even on vacation, no exceptions',
            'what gets measured gets managed'),
      // Must start at the Brandon Carter attribution: opening on "What he says..."
      // leaves the pronoun with no antecedent in a standalone short.
      piece("So I've changed that to a new way of saying it that I learned from Brandon Carter",
            'if you let things slide to that point'),
    ],
  },
  {
    id: 'K', slug: 'eight-hours-is-not-sleep',
    title: '8 Hours In Bed Is Not 8 Hours Of Sleep',
    pieces: [piece('use a sleep tracker to track and improve your sleep',
                   'or these more sophisticated metrics')],
  },
  {
    id: 'L', slug: 'train-abs-every-day',
    title: 'Train Abs EVERY Single Day',
    pieces: [piece('Once you are lean, train abs every day to maximize your ab definition',
                   'with my drop sets as well')],
  },
];

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
