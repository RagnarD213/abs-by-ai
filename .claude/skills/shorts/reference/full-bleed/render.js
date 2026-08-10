// Render the V2 Shorts: one 1080x1920 clip per shot -> concat -> wordmark + title + captions.
// Geometry comes from layout.json, which preview.py also reads, so what was reviewed is
// what gets encoded.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { SEGMENTS } = require('./segments.js');
const { loadShots, TALK_X } = require('./plan.js');
const { buildAss } = require('./captions.js');

const FF = path.join(__dirname, '../../ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg');
const SRC = path.join(__dirname, '../V2 - How To Get Real Six Pack Abs With AI(2) - READY FOR UPLOAD.mp4');
const FONTS = path.join(__dirname, '../../ad-factory/the-upload/assembly/fonts');
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

// Expand the shot list, splitting any pip shot whose graphic animates in late.
function renderShots(segId) {
  const out = [];
  for (const s of loadShots().filter((x) => x.seg === segId)) {
    const pb = L.pipBoxes[s.name];
    if (s.t === 'pip' && pb && pb.from && pb.from > s.absStart + 0.05) {
      const lead = +(pb.from - s.absStart).toFixed(2);
      out.push({ ...s, t: 'talk', dur: lead });
      out.push({ ...s, t: 'pip', absStart: pb.from, dur: +(s.dur - lead).toFixed(2) });
    } else {
      out.push(s);
    }
  }
  return out;
}

function shotFilter(s) {
  if (s.t === 'talk' || s.t === 'broll') {
    const cw = L.talk.cropW;
    const x = Math.round(Math.min(Math.max((CROPS[s.name] ?? TALK_X) * SRC_W - cw / 2, 0), SRC_W - cw));
    return { inputs: [], fc: null,
      vf: `crop=${cw}:${SRC_H}:${x}:0,scale=${CW}:${CH}:flags=lanczos,setsar=1` };
  }
  if (s.t === 'card') {
    const c = L.card;
    const chip = path.join(A, `chip-${s.name}.png`);
    const inputs = ['-loop', '1', '-framerate', String(FPS), '-i', path.join(A, 'j2-bg.png')];
    let fc = `[0:v]scale=${c.w}:${c.h}:flags=lanczos,setsar=1[fit];[1:v][fit]overlay=${c.x}:${c.y}`;
    if (fs.existsSync(chip)) {
      inputs.push('-loop', '1', '-framerate', String(FPS), '-i', chip);
      fc += `[t];[t][2:v]overlay=(W-w)/2:${c.chipY}`;
    }
    return { inputs, fc: fc + ',setsar=1[v]', vf: null };
  }
  if (s.t === 'pip') {
    const p = L.pip;
    const box = L.pipBoxes[s.name].box;
    const gw = box[2] - box[0], gh = box[3] - box[1];
    const srcX0 = L.pipBoxes[s.name].srcX0;
    const danCropW = Math.round(SRC_H * (p.danW / p.danH));
    if (srcX0 < box[2]) throw new Error(`${s.name}: Dan crop would duplicate the PiP graphic`);
    if (srcX0 + danCropW > SRC_W) throw new Error(`${s.name}: Dan crop runs past the frame`);
    const fc =
      `[0:v]split=2[a][b];` +
      `[a]crop=${gw}:${gh}:${box[0]}:${box[1]},scale=-2:${p.gfxH}:flags=lanczos[g];` +
      `[b]crop=${danCropW}:${SRC_H}:${srcX0}:0,scale=${p.danW}:${p.danH}:flags=lanczos[d];` +
      `[1:v][g]overlay=(W-w)/2:${p.gfxTop}[t1];[t1][d]overlay=${p.danX}:${p.danY},setsar=1[v]`;
    return { inputs: ['-loop', '1', '-framerate', String(FPS), '-i', path.join(A, 'j2-bg.png')], fc, vf: null };
  }
  throw new Error(`unknown treatment ${s.t}`);
}

// Source is 24fps. `-loop 1` stills default to 25fps, and overlay adopts the framerate of
// its FIRST input — so card/pip shots (bg png first) came out 25fps, and concat -c copy
// then stamped the whole short 25fps whenever it opened on one. Pin 24 everywhere.
const FPS = 24;
const VENC = ['-r', String(FPS), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
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
    const args = ['-ss', String(s.absStart), '-i', SRC, ...f.inputs, '-t', String(s.dur)];
    if (f.fc) args.push('-filter_complex', f.fc, '-map', '[v]', '-map', '0:a');
    else args.push('-vf', f.vf, '-map', '0:v', '-map', '0:a');
    args.push(...VENC, '-movflags', '+faststart', out);
    ff(args, `${seg.id} shot ${i} (${s.name} ${s.t})`);
    parts.push(out);
  });

  const list = path.join(dir, 'concat.txt');
  fs.writeFileSync(list, parts.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n') + '\n');
  const raw = path.join(dir, 'raw.mp4');
  ff(['-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', raw], `${seg.id} concat`);

  const { ass } = buildAss(seg);
  const assPath = path.join(dir, `${seg.id}.ass`);
  fs.writeFileSync(assPath, ass);

  const outDir = path.join(__dirname, 'out');
  fs.mkdirSync(outDir, { recursive: true });
  const final = path.join(outDir, `${seg.id.toLowerCase()}_${seg.slug}.mp4`);
  const T = L.titleSeconds;
  const segDur = shots.reduce((a, s) => a + s.dur, 0);
  ff([
    '-i', raw,
    '-loop', '1', '-framerate', String(FPS), '-i', path.join(A, 'wordmark.png'),
    '-loop', '1', '-framerate', String(FPS), '-i', path.join(A, `title-${seg.id}.png`),
    '-filter_complex',
    // shortest=1 on both overlays is load-bearing: the wordmark and title are `-loop 1`
    // stills, i.e. INFINITE streams. Without it ffmpeg never reaches EOF and encodes forever.
    `[2:v]format=rgba,fade=t=out:st=${(T - 0.35).toFixed(2)}:d=0.35:alpha=1[ttl];` +
    `[0:v][1:v]overlay=${L.wordmark.x}:${L.wordmark.y}:shortest=1[w];` +
    `[w][ttl]overlay=0:0:shortest=1:enable='lt(t,${T})'[o];` +
    `[o]subtitles='${esc(assPath)}':fontsdir='${esc(FONTS)}'[v]`,
    '-map', '[v]', '-map', '0:a', '-t', String(segDur.toFixed(2)),
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
