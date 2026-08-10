// Render the rebuilt short1: per-shot clips into the block -> concat -> band graphics
// (persistent header + one chip at a time) -> captions -> wordmark.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { V4, FF, START, END, CHIPS, words } = require('./plan.js');

const HERE = __dirname;
const FONTS = path.join(HERE, '../../../ad-factory/the-upload/assembly/fonts');
const A = path.join(HERE, 'assets');
const BUILD = path.join(HERE, 'build');
const L = JSON.parse(fs.readFileSync(path.join(HERE, 'layout.json'), 'utf8'));
const C = JSON.parse(fs.readFileSync(path.join(HERE, 'crops.json'), 'utf8'));
const shots = JSON.parse(fs.readFileSync(path.join(HERE, 'shots.json'), 'utf8'));
const [CW, CH] = L.canvas;
const B = L.block, BD = L.band;
const SRC_W = 1920, SRC_H = 1080, FPS = 24;

const ff = (args, label) => {
  const r = spawnSync(FF, ['-nostdin', '-hide_banner', '-loglevel', 'error', '-y', ...args],
    { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) { console.error(`\nffmpeg failed: ${label}\n${r.stderr}\n`); throw new Error(label); }
};
const esc = (p) => p.replace(/\\/g, '\\\\').replace(/:/g, '\\:').replace(/'/g, "\\'");
// -loop 1 stills are infinite streams and overlay takes its FIRST input's framerate,
// so every still input is pinned to 24fps and every output is bounded by -t.
const still = (p) => ['-loop', '1', '-framerate', String(FPS), '-i', p];
const VENC = ['-r', String(FPS), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
              '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2'];

// ---------- captions, remapped to output time ----------
const t2ass = (t) => {
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60);
  const s = Math.floor(t % 60), cs = Math.round((t % 1) * 100);
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`;
};
function buildAss() {
  const ws = words.filter((w) => {
    const [a, b] = w.timestamp;
    if (b <= START || a >= END) return false;
    return (Math.min(b, END) - Math.max(a, START)) / Math.max(1e-6, b - a) > 0.5;
  }).map((w) => ({ text: w.text, timestamp: [w.timestamp[0] - START, w.timestamp[1] - START] }));

  const chunks = []; let cur = [];
  const flush = () => { if (cur.length) { chunks.push(cur); cur = []; } };
  for (const w of ws) {
    if (cur.length) {
      const gap = w.timestamp[0] - cur[cur.length - 1].timestamp[1];
      if (gap > 0.6 || cur.length >= 4) flush();
    }
    cur.push(w);
    const t = w.text.trim();
    if (/[.?!…]$/.test(t) || (/,$/.test(t) && cur.length >= 2)) flush();
  }
  flush();
  const ev = chunks.map((c, i) => {
    const s = c[0].timestamp[0];
    let e = c[c.length - 1].timestamp[1] + 0.15;
    if (i + 1 < chunks.length) e = Math.min(e, chunks[i + 1][0].timestamp[0]);
    if (e - s < 0.3) e = s + 0.3;
    let text = c.map((w) => w.text.trim()).join(' ')
      .replace(/\s+([.,!?%])/g, '$1').replace(/\s{2,}/g, ' ').trim()
      .replace(/\babs\b/gi, 'ABS').replace(/\bai\b/gi, 'AI');
    return `Dialogue: 0,${t2ass(s)},${t2ass(e)},Cap,,0,0,0,,${text}`;
  });
  return `[Script Info]
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
${ev.join('\n')}
`;
}

// ---------- per-shot clips ----------
fs.rmSync(BUILD, { recursive: true, force: true });
fs.mkdirSync(BUILD, { recursive: true });
const parts = [];
for (const s of shots) {
  const spec = L.shots[String(s.i)];
  const out = path.join(BUILD, `shot-${String(s.i).padStart(2, '0')}.mp4`);
  let fc;
  if (spec.t === 'fitcard') {
    // Top-aligned, NOT centred: a centred 16:9 card lands at y≈861-1424 and the caption
    // band starts around y=1150, so centring put captions straight across the artwork.
    const fh = Math.round(B.w * SRC_H / SRC_W / 2) * 2;
    fc = `[0:v]scale=${B.w}:${fh}:flags=lanczos,setsar=1[fit];` +
         `[1:v][fit]overlay=${B.x}:${B.y + L.fitcardTop},setsar=1[v]`;
  } else {
    const x0 = C.x0[String(s.i)];
    fc = `[0:v]crop=${C.cropW}:${SRC_H}:${x0}:0,scale=${B.w}:${B.h}:flags=lanczos,setsar=1[fit];` +
         `[1:v][fit]overlay=${B.x}:${B.y},setsar=1[v]`;
  }
  // Video only. The shot boundaries are picture cuts inside ONE continuous stretch of
  // audio, so slicing audio per shot would splice it back together across six independent
  // input seeks — measured at 23-34ms of per-shot offset, i.e. a small content jump at
  // every join. Audio is taken once, unbroken, in the finishing pass instead.
  ff(['-ss', String(s.absStart), '-i', V4, ...still(path.join(A, 'bg.png')),
      '-t', String(s.dur), '-filter_complex', fc, '-map', '[v]', '-an',
      ...VENC.filter((a, i, arr) => !['-c:a', '-b:a', '-ar', '-ac'].includes(arr[i - 1]) &&
                                    !['-c:a', '-b:a', '-ar', '-ac'].includes(a)),
      '-movflags', '+faststart', out], `shot ${s.i} (${spec.t})`);
  parts.push(out);
}
const list = path.join(BUILD, 'concat.txt');
fs.writeFileSync(list, parts.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n') + '\n');
const raw = path.join(BUILD, 'raw.mp4');
ff(['-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', raw], 'concat');

// ---------- band graphics + captions ----------
const assPath = path.join(BUILD, 'short1.ass');
fs.writeFileSync(assPath, buildAss());
const total = shots.reduce((a, s) => a + s.dur, 0);

// input 0 = concatenated video, input 1 = ONE continuous audio pull from the source
const inputs = ['-i', raw, '-ss', String(START), '-i', V4,
                ...still(path.join(A, 'header.png')), ...still(path.join(A, 'wordmark.png'))];
CHIPS.forEach((c) => inputs.push(...still(path.join(A, `chip-${c.key}.png`))));

let fc = `[0:v][2:v]overlay=0:${BD.headerY}:shortest=1:enable='gte(t,${BD.headerFrom})'[a];` +
         `[a][3:v]overlay=${L.wordmark.x}:${L.wordmark.y}:shortest=1[b0];`;
CHIPS.forEach((c, i) => {
  const src = `[${4 + i}:v]`, prev = `[b${i}]`, next = `[b${i + 1}]`;
  fc += `${prev}${src}overlay=${BD.chipX}:${BD.counterY}:shortest=1:` +
        `enable='between(t,${c.from},${c.to})'${next};`;
});
fc += `[b${CHIPS.length}]subtitles='${esc(assPath)}':fontsdir='${esc(FONTS)}'[v]`;

const outDir = path.join(HERE, 'out');
fs.mkdirSync(outDir, { recursive: true });
const final = path.join(outDir, 'short1_4-ab-muscles.mp4');
ff([...inputs, '-filter_complex', fc, '-map', '[v]', '-map', '1:a',
    '-t', total.toFixed(2), ...VENC, '-movflags', '+faststart', final], 'finish');

console.log(`short1 rebuilt -> ${final}`);
console.log(`  ${shots.length} shots, ${total.toFixed(1)}s, ${(fs.statSync(final).size / 1e6).toFixed(1)} MB`);
CHIPS.forEach((c) => console.log(`  chip ${c.n} ${c.title.padEnd(22)} ${c.from.toFixed(1)}-${c.to.toFixed(1)}s`));
