// Render the V2 Shorts: one 1080x1920 clip per shot -> concat -> wordmark + title + captions.
// Geometry comes from layout.json, which preview.py also reads, so what was reviewed is
// what gets encoded.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { SEGMENTS } = require('./segments.js');
const { loadShots } = require('./plan.js');
const { buildAss } = require('./captions.js');
const { BLEEPS } = require('./bleeps.js');

const { FF, SRC, FONTS, FPS, FPS_N } = require('./config.js');
const A = path.join(__dirname, 'assets');
const BUILD = path.join(__dirname, 'build');
const L = JSON.parse(fs.readFileSync(path.join(__dirname, 'layout.json'), 'utf8'));
const CROPS = JSON.parse(fs.readFileSync(path.join(__dirname, 'shots', 'crops.json'), 'utf8'));
const [CW, CH] = L.canvas;
const SRC_W = 1920, SRC_H = 1080;

const ff = (args, label) => {
  const r = spawnSync(FF, ['-hide_banner', '-loglevel', 'error', '-y', ...args], { encoding: 'utf8' });
  if (r.status !== 0) {
    console.error(`\nffmpeg failed: ${label}\n${r.stderr}\n`);
    throw new Error(`ffmpeg failed: ${label}`);
  }
};
const esc = (p) => p.replace(/\\/g, '\\\\').replace(/:/g, '\\:').replace(/'/g, "\\'");

const renderShots = (segId) => loadShots().filter((x) => x.seg === segId);

function shotFilter(s) {
  // ONE TREATMENT. The clean master is a single locked kitchen camera with no burned
  // graphics anywhere, so there is nothing to preserve whole and nothing to avoid slicing -
  // every shot is a full-bleed 9:16 crop. (The delivered master would have been a different
  // job entirely: 43% insert coverage, i.e. nearly half of every short forced into a card.)
  if (s.t !== 'talk') throw new Error(`unknown treatment ${s.t} on ${s.name}`);
  const T = L.talk;
  const cw = T.cropW, ch = T.cropH, top = T.cropTop;
  const cen = CROPS[s.name];
  if (cen == null) throw new Error(`${s.name}: no measured crop centre`);
  const x = Math.round(Math.min(Math.max(cen * SRC_W - cw / 2, 0), SRC_W - cw));
  // DROP. Picture fills 1080 x (1920-dropTop) at the BOTTOM of the canvas, on the J2 field,
  // so the title has a band of its own and never lands on his face or abs (Dan, 2026-08-28).
  const ph = CH - L.dropTop;
  return {
    inputs: ['-loop', '1', '-framerate', FPS, '-i', path.join(A, 'j2-bg.png')],
    // setpts=PTS-STARTPTS is load-bearing: `-ss` leaves the first decoded frame with a
    // non-zero PTS while the looped background starts at 0, and overlay then emits one bare
    // background frame before the picture. shortest=1 is load-bearing too - the background
    // is an infinite `-loop 1` still and overlay follows its FIRST input.
    fc: `[0:v]setpts=PTS-STARTPTS,crop=${cw}:${ch}:${x}:${top},` +
        `scale=${CW}:${ph}:flags=lanczos,setsar=1[pic];` +
        `[1:v][pic]overlay=0:${L.dropTop}:shortest=1,setsar=1[v]`,
    vf: null };
}

// `-loop 1` stills default to 25fps and overlay adopts its FIRST input's rate, so card
// shots (bg png first) come out 25fps and concat -c copy then stamps the whole short 25.
// FPS is pinned on every still input and every encode. It is 30000/1001, not the 24 the
// earlier batches used - see config.js.
const VENC = ['-r', FPS, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
              '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2'];

function renderSegment(seg) {
  const dir = path.join(BUILD, seg.id);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });

  const shots = renderShots(seg.id);
  const parts = [];
  shots.forEach((s, i) => {
    const out = path.join(dir, `shot-${String(i).padStart(2, '0')}.mp4`);
    const f = shotFilter(s);
    // VIDEO ONLY. Audio is pulled once per PIECE below and laid over the concatenated
    // video. Cutting audio per shot re-splices it across N independent input seeks, which
    // measured 23-34ms of drift per cut on the V4 rebuild - a small content jump at every
    // picture cut. Shot boundaries are picture cuts inside CONTINUOUS audio.
    const args = ['-ss', String(s.absStart), '-i', SRC, ...f.inputs, '-t', String(s.dur)];
    if (f.fc) args.push('-filter_complex', f.fc, '-map', '[v]', '-an');
    else args.push('-vf', f.vf, '-map', '0:v', '-an');
    args.push(...VENC, '-movflags', '+faststart', out);
    ff(args, `${seg.id} shot ${i} (${s.name} ${s.t})`);
    parts.push(out);
  });

  const list = path.join(dir, 'concat.txt');
  fs.writeFileSync(list, parts.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n') + '\n');
  const raw = path.join(dir, 'raw.mp4');
  ff(['-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', raw], `${seg.id} concat`);

  // ---- audio: one continuous pull per PIECE, concatenated as WAV ------------------
  // WAV rather than AAC so the joins carry no encoder priming gap; it is encoded once,
  // at the end, in the finishing pass.
  const segBleeps = BLEEPS[seg.id] || [];
  const wavs = [];
  seg.pieces.forEach((p, pi) => {
    const w = path.join(dir, `aud-${pi}.wav`);
    const args = ['-ss', String(p.start), '-i', SRC, '-t', String((p.end - p.start).toFixed(3)), '-vn'];
    // Bleep windows are in SOURCE time; shift them into this piece's local time.
    const local = segBleeps
      .filter((b) => b[1] > p.start && b[0] < p.end)
      .map((b) => [Math.max(0, b[0] - p.start), Math.min(p.end - p.start, b[1] - p.start)]);
    if (local.length) {
      const cond = local.map(([a, b]) => `between(t,${a.toFixed(3)},${b.toFixed(3)})`).join('+');
      args.push(
        '-f', 'lavfi', '-i', 'sine=frequency=1000:sample_rate=48000',
        '-filter_complex',
        `[0:a]volume=0:enable='${cond}'[sp];` +
        // ffmpeg's `sine` source emits at amplitude 0.125 (-18 dBFS), NOT full scale, so a
        // naive volume=0.20 produced a tone ~11x quieter than the speech around it and the
        // bleep was barely audible. 2.0 puts the peak at ~0.25, comfortably above the
        // surrounding dialogue. Measured, not assumed.
        `[1:a]volume=2.0,volume=0:enable='not(${cond})'[tone];` +
        `[sp][tone]amix=inputs=2:duration=first:normalize=0[a]`,
        '-map', '[a]');
    }
    // ⚠ This source has NO music bed (unlike the ab-wheel cut), so the fades are short -
    // they exist only to stop a splice ticking, not to hide a bar starting mid-phrase.
    // Durations are untouched (no acrossfade), so picture and sound stay frame-locked.
    const AU = L.audio;
    const pd = p.end - p.start;
    const fIn = pi === 0 ? AU.fadeIn : AU.joinFade;
    const fOut = pi === seg.pieces.length - 1 ? AU.fadeOut : AU.joinFade;
    const fade = `afade=t=in:st=0:d=${fIn},afade=t=out:st=${(pd - fOut).toFixed(3)}:d=${fOut}`;
    if (local.length) {
      // the bleep branch already built a filter_complex; append the fades to its [a] output
      const k = args.indexOf('-filter_complex');
      args[k + 1] = args[k + 1].replace('[a]', '[amix]') + `;[amix]${fade}[a]`;
    } else {
      args.push('-af', fade);
    }
    args.push('-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', w);
    ff(args, `${seg.id} audio piece ${pi}${local.length ? ' (bleeped)' : ''}`);
    wavs.push(w);
  });
  const audio = path.join(dir, 'audio.wav');
  if (wavs.length === 1) fs.copyFileSync(wavs[0], audio);
  else {
    const alist = path.join(dir, 'aconcat.txt');
    fs.writeFileSync(alist, wavs.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n') + '\n');
    ff(['-f', 'concat', '-safe', '0', '-i', alist, '-c', 'copy', audio], `${seg.id} audio concat`);
  }

  const { ass } = buildAss(seg);
  const assPath = path.join(dir, `${seg.id}.ass`);
  fs.writeFileSync(assPath, ass);

  const outDir = path.join(__dirname, 'out');
  fs.mkdirSync(outDir, { recursive: true });
  const final = path.join(outDir, `${seg.id.toLowerCase()}_${seg.slug}.mp4`);
  const segDur = shots.reduce((a, s) => a + s.dur, 0);
  ff([
    '-i', raw,
    '-loop', '1', '-framerate', FPS, '-i', path.join(A, 'wordmark.png'),
    '-loop', '1', '-framerate', FPS, '-i', path.join(A, `title-${seg.id}.png`),
    '-i', audio,
    '-filter_complex',
    // shortest=1 on both overlays is load-bearing: the wordmark and title are `-loop 1`
    // stills, i.e. INFINITE streams. Without it ffmpeg never reaches EOF and encodes forever.
    // The title HOLDS for the whole short - no fade. It lives on the black field above the
    // picture, so it costs the picture nothing and it stops the top band reading as dead space.
    `[0:v][1:v]overlay=${L.wordmark.x}:${L.wordmark.y}:shortest=1[w];` +
    `[w][2:v]overlay=0:0:shortest=1[o];` +
    `[o]subtitles='${esc(assPath)}':fontsdir='${esc(FONTS)}'[v]`,
    '-map', '[v]', '-map', '3:a', '-t', String(segDur.toFixed(2)),
    ...VENC, '-movflags', '+faststart', final,
  ], `${seg.id} finish`);

  const size = fs.statSync(final).size / 1e6;
  console.log(`  ${seg.id} -> ${path.basename(final)}  ${shots.length} shots, ${size.toFixed(1)} MB`);
  return final;
}

if (require.main === module) {
  const only = process.argv.slice(2);
  const todo = only.length ? SEGMENTS.filter((s) => only.includes(s.id)) : SEGMENTS;
  for (const seg of todo) {
    console.log(`rendering ${seg.id} ${seg.slug} ...`);
    renderSegment(seg);
  }
}
