// Word-timed captions for the V2 Shorts.
// Grouping/style is the canonical spec lifted from channel-intro/cut-shorts.js.
// The only new thing: source time is remapped onto the OUTPUT timeline, because
// segments B and I are stitched from two non-contiguous pieces of the source.
const fs = require('fs');
const path = require('path');
const { SEGMENTS } = require('./segments.js');
// Caption TIMES come from the CTC forced alignment of the source words (work/ctc_source.py);
// Whisper's own onsets run 130-420 ms early in continuous speech on this mix.
const words = JSON.parse(fs.readFileSync(path.join(__dirname, 'work', 'words_aligned.json'), 'utf8')).chunks;
const { BLEEP_WORDS } = require('./bleeps.js');

// [pattern, replacement]. Applied to the finished caption text, after the ABS/AI casing.
const FIXES = [
  [/\btime sets\b/gi, 'timed sets'],
  [/\bGym Boss\b/g, 'Gymboss'],
  // SL-05: Whisper's spellings vs Zeeshan's pills and the description
  [/\bsix -pack\b/gi, 'six-pack'],
  [/\bT -bar\b/g, 'T-bar'],
  [/\bpower lifter\b/gi, 'powerlifter'],
  [/\bdead lifting\b/gi, 'deadlifting'],
];

const MARGIN_V = JSON.parse(fs.readFileSync(path.join(__dirname, 'layout.json'), 'utf8')).captionMarginV;
const t2ass = (t) => {
  // round 2: round to centiseconds FIRST. Rounding the fraction alone wrote 30.995 as "0:00:30.100", an invalid time,
  // and libass dropped that cue (short 2, "And that means you").
  const c = Math.round(t * 100);
  const h = Math.floor(c / 360000), m = Math.floor((c % 360000) / 6000), s = Math.floor((c % 6000) / 100), cs = c % 100;
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`;
};

// Map every word that is audible in the short onto output time.
function segWords(seg) {
  const out = [];
  let offset = 0;
  for (const p of seg.pieces) {
    // Live-round pieces are music with sung vocals and no speech from Dan: no captions.
    if (p.music) { offset += p.end - p.start; continue; }
    for (const w of words) {
      const [a, b] = w.timestamp;
      if (b <= p.start || a >= p.end) continue;
      // Most of the word must be inside the piece, or a boundary fragment gets a caption
      // for audio the viewer never hears.
      const ov = Math.min(b, p.end) - Math.max(a, p.start);
      if (ov / Math.max(1e-6, b - a) <= 0.5) continue;
      out.push({
        // a piece marked `continues` carries on the previous piece's sentence (SL-04 round 3: "laterals, | if you guys"):
        // its first word is not capitalised, and the mid-sentence lower-casing below applies to it
        first: !p.continues && !out.some((o) => o.piece === p) ,
        piece: p,
        pieceEnd: offset + (p.end - p.start),
        text: w.text,
        timestamp: [offset + Math.max(0, a - p.start), offset + Math.min(p.end - p.start, b - p.start)],
      });
    }
    offset += p.end - p.start;
  }
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
    if (prev && (/^\s*[.,!?%]/.test(w.text) || /^\s*-\w/.test(w.text))) {   // SL-05: '-bar' joins 'T' (T-bar)
      prev.text = prev.text.replace(/\s+$/, '') + w.text.trim();
      prev.timestamp = [prev.timestamp[0], w.timestamp[1]];
    } else {
      ws.push({ text: w.text, timestamp: [...w.timestamp], first: w.first, pieceEnd: w.pieceEnd });
    }
  }
  // Per-WORD fixes before chunking (a two-word fix can straddle a chunk boundary).
  for (let i = 0; i < ws.length; i++) {
    const t = ws[i].text.trim().toLowerCase();
    // SL-05: 'power' + 'lifter' is one word on screen (Zeeshan's pills say POWERLIFTER); join before chunking
    if (t === 'power' && ws[i + 1] && /^lifter/i.test(ws[i + 1].text.trim())) {
      ws[i].text = ws[i].text.replace(/power/i, (m) => m + ws[i + 1].text.trim()); ws[i].timestamp[1] = ws[i + 1].timestamp[1]; ws.splice(i + 1, 1); continue; }
    // Whisper doubles a token at a stutter ("don" + "don't", both at source 265.9); the delivered
    // audio says "don't" once. Drop the fragment.
    if (t === 'don' && ws[i + 1] && /^don't/i.test(ws[i + 1].text.trim())) { ws.splice(i, 1); i--; continue; }
    // Dan says "time sets"; his own chip and the description read "Timed Sets".
    if (t === 'time' && ws[i + 1] && /^sets\b/i.test(ws[i + 1].text.trim())) ws[i].text = ws[i].text.replace(/time/i, 'timed');
    // Whisper capitalises after its own sentence splits ("first You can do", "that So you're"):
    // mid-sentence, lower-case it (never "I", "I'm", "I'll", "AI").
    if (!ws[i].first && i > 0 && /^\s*[A-Z][a-z]/.test(ws[i].text) && !/[.?!]\s*$/.test(ws[i - 1].text)
        && !/^\s*(I|I'm|I'll|I've|I'd)\b/.test(ws[i].text)) ws[i].text = ws[i].text.replace(/^(\s*)([A-Z])/, (m, s, ch) => s + ch.toLowerCase());
    // a verbatim stutter ("as as") prints once
    if (i > 0 && t && t === ws[i - 1].text.trim().toLowerCase()) { ws.splice(i, 1); i--; continue; }
    // A piece can start mid-sentence ("you want to be..."): capitalise its first word.
    if (ws[i].first) ws[i].text = ws[i].text.replace(/^(\s*)([a-z])/, (m, s, ch) => s + ch.toUpperCase());
  }
  const chunks = [];
  let cur = [];
  const flush = () => { if (cur.length) { chunks.push(cur); cur = []; } };
  for (const w of ws) {
    const [start] = w.timestamp;
    if (cur.length) {
      const prevEnd = cur[cur.length - 1].timestamp[1];
      // four words a cue, except that a short sentence-ending word joins a 4-word cue instead of flashing alone
      // (SL-04 round-3 review: "top." was up for 6 frames after "like this at the"). Opt-in per short (seg.joinShortEnd)
      // so the finalized shorts rebuild exactly as approved
      const endsShort = seg.joinShortEnd && /[.?!…]$/.test(w.text.trim()) && w.text.trim().length <= 5;
      if (start - prevEnd > 0.6 || (cur.length >= 4 && !(cur.length === 4 && endsShort))) flush();
      // SL-05 round 2d: on a close shot under the tall bar a two-line cue sits on his chin. seg.oneLine = [[t0, t1, maxChars]]
      // (output time): inside it a cue is closed before it would pass maxChars, so it stays on one line
      else if (seg.breakBefore && seg.breakBefore.some((t) => Math.abs(start - t) < 0.06)) flush();   // explicit cue breaks (output time)
      else if (seg.oneLine && seg.oneLine.some(([a, b, n]) => start >= a && start < b && (cur.map((x) => x.text.trim()).join(' ') + ' ' + w.text.trim()).length > n)) flush();
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
    // Minimum hold FIRST, then the clamp to the next cue (DS-17 lesson): the other order
    // overlaps two cues and libass stacks the second one above the first.
    if (end - start < 0.3) end = start + 0.3;
    if (i + 1 < chunks.length) end = Math.min(end, chunks[i + 1][0].timestamp[0]);
    // a cue never runs past the audio join its last word ends at (round-2 review, short 3: "the side laterals."
    // held 3 frames into the next piece's picture)
    // (SL-05 round 2e: the LAST cue of a short holds through the final frame; a player that parks on the last frame showed no caption)
    if (c[c.length - 1].pieceEnd) end = (seg.oneLine || seg.breakBefore || seg.lastCueToEnd) && i === chunks.length - 1 ? c[c.length - 1].pieceEnd + 0.1 : Math.min(end, c[c.length - 1].pieceEnd - 0.02);
    // ASS times are centiseconds and libass rounds to nearest: 42.405 printed 42.41 and held the cue on the first frame
    // (42.409) of the next shot (SL-04 round 3). Floor it for shorts that opt in, so finalized ones rebuild as approved.
    const lastHold = seg.lastCueToEnd && i === chunks.length - 1;   // SL-05: the last cue stays through the final frame
    if (seg.joinShortEnd && c[c.length - 1].pieceEnd && !lastHold) end = Math.min(end, Math.floor((c[c.length - 1].pieceEnd - 0.02) * 100) / 100);
    // never past the picture (gate captions:within_runtime): the last cue ends 2 frames early
    // (lastHold: it ends inside the final frame instead, still within the runtime)
    end = Math.min(end, Math.floor((seg.pieces.reduce((a, p) => a + (p.end - p.start), 0) - (lastHold ? 0.012 : 0.07)) * 100) / 100);
    let text = c.map((w) => w.text.trim()).join(' ');
    // Whisper tokenises "p.m." as ["p", ".m."], which joins to "p .m.". Re-close any
    // punctuation that ended up with a space in front of it.
    text = text.replace(/\s+([.,!?%])/g, '$1').replace(/\s{2,}/g, ' ').trim();
    // STANDING RULE (Dan, 2026-08-28): captions print "abs" in lower case, never "ABS".
    // The uppercase rule dated from video #1 and he has now killed it batch-wide. "AI" stays
    // upper case - it is an initialism, "abs" is just a word.
    text = text.replace(/\babs\b/gi, 'abs').replace(/\bai\b/gi, 'AI');
    // Whisper mis-hearings, checked against the audio. Burning a wrong word in 86pt is the
    // one caption fault a viewer cannot ignore, and it has bitten this pipeline before.
    for (const [wrong, right] of FIXES) text = text.replace(wrong, right);
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
Style: Cap,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,7,3,2,60,60,${MARGIN_V},1

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
