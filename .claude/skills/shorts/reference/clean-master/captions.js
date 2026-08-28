// Word-timed captions for the V2 Shorts.
// Grouping/style is the canonical spec lifted from channel-intro/cut-shorts.js.
// The only new thing: source time is remapped onto the OUTPUT timeline, because
// segments B and I are stitched from two non-contiguous pieces of the source.
const fs = require('fs');
const path = require('path');
const { SEGMENTS, words } = require('./segments.js');
const { BLEEP_WORDS } = require('./bleeps.js');

// [pattern, replacement]. Applied to the finished caption text, after the ABS/AI casing.
// Whisper mis-hearings on THIS roll, each checked against the other two independent
// transcriptions of the same audio (pass b, and the delivered 820-cue SRT) before being
// applied. Burning a wrong word in 86pt is the one caption fault a viewer cannot ignore.
// ⚠ APPLIED PER WORD, BEFORE CHUNKING - not to the finished caption line. A chunk is at most
// four words, so a two-word mis-hearing can straddle a chunk boundary and a line-level regex
// then never sees it: "phytoplasmic acne" survived exactly that way on the first attempt.
const WORD_FIXES = [
  // pass a alone heard "phytoplasmic acne"; pass b AND the delivered 820-cue SRT both read
  // "fighting cystic acne", and he says "cystic acne" twice elsewhere in the video.
  [/^phytoplasmic$/i, 'fighting cystic'],
  // the brand is Thorne. Every Whisper run drops the e.
  [/^Thorn$/, 'Thorne'],
];

const t2ass = (t) => {
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60);
  const s = Math.floor(t % 60), cs = Math.round((t % 1) * 100);
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`;
};

// Map every word that is audible in the short onto output time.
function segWords(seg) {
  const out = [];
  let offset = 0;
  seg.pieces.forEach((p, pi) => {
    for (const w of words) {
      const [a, b] = w.timestamp;
      if (b <= p.start || a >= p.end) continue;
      // ⚠ ZERO-DURATION WORDS. Whisper emits a=b for a small number of words (9 of 4719 on
      // this roll). The overlap test below then computes 0/1e-6 = 0, which is <= 0.5, so the
      // word was SILENTLY DROPPED FROM THE CAPTIONS while remaining in the audio. That is how
      // "creatine is not an option for me" became "not an for me", and it also ate a word in
      // A, C, E and M. Caught by reading the finished caption text, not by any gate. A word
      // with no duration is inside the piece if its START is; give it a nominal 120ms so the
      // chunker and the >=0.3s minimum still behave.
      const zero = b - a <= 0.0001;
      if (zero) {
        if (a < p.start || a >= p.end) continue;
      } else {
        // Most of the word must be inside the piece, or a boundary fragment gets a caption
        // for audio the viewer never hears.
        const ov = Math.min(b, p.end) - Math.max(a, p.start);
        if (ov / Math.max(1e-6, b - a) <= 0.5) continue;
      }
      const bb = zero ? Math.min(p.end, a + 0.12) : b;
      out.push({
        text: w.text,
        timestamp: [offset + Math.max(0, a - p.start), offset + Math.min(p.end - p.start, bb - p.start)],
        piece: pi,
      });
    }
    offset += p.end - p.start;
  });
  return out.sort((x, y) => x.timestamp[0] - y.timestamp[0]);
}

function buildAss(seg) {
  const raw = segWords(seg);
  // Whisper tokenises "2 p.m." as ["2", "p", ".m."]. The existing regex re-closes the
  // space only WITHIN a caption chunk; when the chunk boundary fell between "p" and
  // ".m." the short opened on a caption reading just ".m.". Merge any token that begins
  // with punctuation into the one before it, before chunking.
  const ws = [];
  for (const w of raw) {
    const prev = ws[ws.length - 1];
    // Also merges a HYPHEN-initial token: Whisper splits "sub-step" into ["sub", "-step"],
    // which joined to "sub -step" on screen. Same class of fault as the ".m." case.
    if (prev && /^\s*[.,!?%-]/.test(w.text)) {
      prev.text = prev.text.replace(/\s+$/, '') + w.text.trim();
      prev.timestamp = [prev.timestamp[0], w.timestamp[1]];
    } else {
      ws.push({ text: w.text, timestamp: [...w.timestamp], piece: w.piece });
    }
  }
  for (const w of ws) {
    const lead = w.text.match(/^\s*/)[0];
    const core = w.text.trim();
    const tail = core.match(/[.,!?]*$/)[0];
    const bare = core.slice(0, core.length - tail.length);
    for (const [wrong, right] of WORD_FIXES) {
      if (wrong.test(bare)) w.text = lead + bare.replace(wrong, right) + tail;
    }
  }

  const chunks = [];
  let cur = [];
  const flush = () => { if (cur.length) { chunks.push(cur); cur = []; } };
  for (const w of ws) {
    const [start] = w.timestamp;
    if (cur.length) {
      const prevEnd = cur[cur.length - 1].timestamp[1];
      if (start - prevEnd > 0.6 || cur.length >= 4) flush();
    }
    cur.push(w);
    const txt = w.text.trim();
    if (/[.?!…]$/.test(txt) || (/,$/.test(txt) && cur.length >= 2)) flush();
  }
  flush();

  const events = [];
  chunks.forEach((c, i) => {
    const start = c[0].timestamp[0];
    let end = c[c.length - 1].timestamp[1] + 0.15;
    if (i + 1 < chunks.length) end = Math.min(end, chunks[i + 1][0].timestamp[0]);
    if (end - start < 0.3) end = start + 0.3;
    let text = c.map((w) => w.text.trim()).join(' ');
    // A piece can start mid-sentence in the source, so its first caption arrives lower-case
    // ("vitamin D. Critically..." / "about 70% of people..." both open a short in J). Capitalise
    // the opening word of every piece - it is the first thing the viewer reads.
    if (i === 0 || c[0].piece !== chunks[i - 1][chunks[i - 1].length - 1].piece) {
      text = text.charAt(0).toUpperCase() + text.slice(1);
    }
    // Whisper tokenises "p.m." as ["p", ".m."], which joins to "p .m.". Re-close any
    // punctuation that ended up with a space in front of it.
    text = text.replace(/\s+([.,!?%])/g, '$1').replace(/\s{2,}/g, ' ').trim();
    // STANDING RULE (Dan, 2026-08-28): captions print "abs" in lower case, never "ABS".
    // The uppercase rule dated from video #1 and he has now killed it batch-wide. "AI" stays
    // upper case - it is an initialism, "abs" is just a word.
    text = text.replace(/\babs\b/gi, 'abs').replace(/\bai\b/gi, 'AI');
    // Bleeping the audio but printing the word in 86pt captions would defeat the point.
    // BLEEP_WORDS is per-segment so it only masks where the audio is actually bleeped.
    for (const w of (BLEEP_WORDS[seg.id] || [])) {
      text = text.replace(new RegExp(`\\b${w}\\b`, 'gi'), '[BLEEP]');
    }
    events.push(`Dialogue: 0,${t2ass(start)},${t2ass(end)},Cap,,0,0,0,,${text}`);
  });

  const ass = `[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,7,3,2,60,60,690,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
${events.join('\n')}
`;
  return { ass, chunks: chunks.length, words: ws.length };
}

module.exports = { buildAss, segWords };

if (require.main === module) {
  const dir = path.join(__dirname, 'build');
  fs.mkdirSync(dir, { recursive: true });
  for (const seg of SEGMENTS) {
    const { ass, chunks, words: n } = buildAss(seg);
    const p = path.join(dir, `${seg.id}.ass`);
    fs.writeFileSync(p, ass);
    const dur = seg.pieces.reduce((a, x) => a + (x.end - x.start), 0);
    console.log(`${seg.id} ${seg.slug.padEnd(26)} ${n} words, ${chunks} caption chunks over ${dur.toFixed(1)}s`);
  }
}
