// Word-timed captions for the V2 Shorts.
// Grouping/style is the canonical spec lifted from channel-intro/cut-shorts.js.
// The only new thing: source time is remapped onto the OUTPUT timeline, because
// segments B and I are stitched from two non-contiguous pieces of the source.
const fs = require('fs');
const path = require('path');
const { SEGMENTS, words } = require('./segments.js');

const t2ass = (t) => {
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60);
  const s = Math.floor(t % 60), cs = Math.round((t % 1) * 100);
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`;
};

// Map every word that is audible in the short onto output time.
function segWords(seg) {
  const out = [];
  let offset = 0;
  for (const p of seg.pieces) {
    for (const w of words) {
      const [a, b] = w.timestamp;
      if (b <= p.start || a >= p.end) continue;
      // Most of the word must be inside the piece, or a boundary fragment gets a caption
      // for audio the viewer never hears.
      const ov = Math.min(b, p.end) - Math.max(a, p.start);
      if (ov / Math.max(1e-6, b - a) <= 0.5) continue;
      out.push({
        text: w.text,
        timestamp: [offset + Math.max(0, a - p.start), offset + Math.min(p.end - p.start, b - p.start)],
      });
    }
    offset += p.end - p.start;
  }
  return out.sort((x, y) => x.timestamp[0] - y.timestamp[0]);
}

function buildAss(seg) {
  const ws = segWords(seg);
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
    // Whisper tokenises "p.m." as ["p", ".m."], which joins to "p .m.". Re-close any
    // punctuation that ended up with a space in front of it.
    text = text.replace(/\s+([.,!?%])/g, '$1').replace(/\s{2,}/g, ' ').trim();
    text = text.replace(/\babs\b/gi, 'ABS').replace(/\bai\b/gi, 'AI');
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
