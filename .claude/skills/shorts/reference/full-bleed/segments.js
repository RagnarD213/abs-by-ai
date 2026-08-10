// Precise in/out points for the V2 Shorts, resolved against Whisper word timestamps
// (never the rounded sentence marks in v2-transcript.txt).
const fs = require('fs');
const path = require('path');

const words = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'v2-words.json'), 'utf8')
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

// A piece = continuous run of source video, from the START of `from` to the END of `to`.
function piece(from, to = from, { nthFrom = 0, nthTo = 0 } = {}) {
  const f = find(from, nthFrom);
  const t = find(to, nthTo);
  if (t.t1 <= f.t0) throw new Error(`"${to}" ends before "${from}" starts`);
  const prev = words[f.a - 1];
  const next = words[t.b + 1];
  const start = snapIn(f.t0, prev ? prev.timestamp[1] : 0);
  const end = snapOut(t.t1, next ? next.timestamp[0] : t.t1 + 0.4);
  if (end <= start) throw new Error(`snapped cut collapsed for "${from}"`);
  return { start: +start.toFixed(2), end: +end.toFixed(2), from, to };
}

const SEGMENTS = [
  {
    id: 'A', slug: 'sean-ray-vision-board',
    title: 'The Vision Board That Built Mike Chang',
    pieces: [piece('I remember when I met Mike Chang', 'this is real')],
  },
  {
    id: 'B', slug: 'sugar-free-gum-trick',
    title: 'The AI Trick That Killed My Late-Night Snacking',
    // Deliberately skips the marijuana/alcohol clause: setup line, hard cut, then the payoff.
    pieces: [
      piece('You can also tell AI about the cheap foods that are the biggest problem for you'),
      piece('So what I do now, based on the advice of AI', 'that AI has helped me'),
    ],
  },
  {
    id: 'D', slug: 'ask-ai-to-interview-you',
    title: 'Ask The AI To Interview YOU',
    pieces: [piece('Not only that, after they answer all those questions',
                   'the key to designing a great workout program with AI, deep context')],
  },
  {
    id: 'E', slug: 'supplements-3-percent',
    title: 'Supplements Are Only 3% Of Your Results',
    pieces: [piece('Back in the 80s and the 90s', 'and still getting great results')],
  },
  {
    id: 'G', slug: 'hire-a-maid-not-a-trainer',
    title: 'Hire A Maid, Not A Personal Trainer',
    pieces: [piece('Human personal trainers are extremely expensive', 'Use free AI tools instead')],
  },
  {
    id: 'I', slug: 'macro-tracking-obsolete',
    title: 'The Old Way To Track Macros Is Obsolete',
    pieces: [
      piece('AI can track your macros', 'all your macros in one place'),
      piece('I personally, however, have always been an opponent', 'doing no tracking at all'),
    ],
  },
  {
    id: 'J', slug: 'chicken-soup-trick',
    title: 'Make AI Macro Estimates Way More Accurate',
    pieces: [piece("Here's another way that you can make these AI macro estimates more accurate",
                   "what's in the soup")],
  },
];

module.exports = { SEGMENTS, words, find };

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
