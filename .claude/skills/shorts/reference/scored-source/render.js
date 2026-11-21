// Render the V2 Shorts: one 1080x1920 clip per shot -> concat -> wordmark + title + captions.
// Geometry comes from layout.json, which preview.py also reads, so what was reviewed is
// what gets encoded.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { SEGMENTS } = require('./segments.js');
const { loadShots, TALK_X } = require('./plan.js');
const { buildAss } = require('./captions.js');
const { BLEEPS } = require('./bleeps.js');

const { FF, SRC, FONTS, FPS, FPS_N } = require('./config.js');
// ⚠ DO NOT USE THIS PIPELINE FOR AUDIO (2026-09-02): it pulled the source's default stream with no
// channel selection and no chain. It stays for its picture code only. The pull below now takes the
// lav per audio_source.json; tone/loudness/gate still have to run (clean-master/finishaudio.py) or
// qc.js refuses the unstamped file.
const AUDIO = require('/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/qclib.js');
const SRCA = AUDIO.loadSource(SRC);
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
    // zoom crops from the TOP of the frame to drop a burned-in bottom lower-third.
    const cw = s.zoom ? L.talk.dropZoomW : L.talk.dropW;
    const ch = s.zoom ? L.talk.zoomH : SRC_H;
    let x = Math.round(Math.min(Math.max((CROPS[s.name] ?? TALK_X) * SRC_W - cw / 2, 0), SRC_W - cw));
    // minX0: this shot carries a burned graphic down the LEFT edge of the source frame.
    // The window is forced right of it so the graphic is excluded whole, never half-cropped.
    if (s.minX0 != null) {
      if (s.minX0 + cw > SRC_W) throw new Error(`${s.name}: minX0 ${s.minX0} leaves no room for a ${cw}px window`);
      x = Math.max(x, s.minX0);
    }
    // DROP. The picture fills 1080 x (1920-dropTop) and sits at the BOTTOM of the canvas, on
    // the J2 field, so the title has a band of its own and never lands on his face or abs.
    const ph = CH - L.dropTop;
    return { inputs: ['-loop', '1', '-framerate', FPS, '-i', path.join(A, 'j2-bg.png')],
      fc: `[0:v]setpts=PTS-STARTPTS,crop=${cw}:${ch}:${x}:0,scale=${CW}:${ph}:flags=lanczos,setsar=1[pic];` +
          `[1:v][pic]overlay=0:${L.dropTop}:shortest=1,setsar=1[v]`,
      vf: null };
  }
  // A NATIVE-VERTICAL clip from a different file. Dan, rev 2: "get new B-roll or stock
  // footage that fits in that vertical frame". Every other treatment carves 9:16 out of a
  // 16:9 source and pays an upscale for it; this one is already 9:16, so it goes full-bleed
  // at close to 1:1 and is the sharpest picture in the batch.
  if (s.t === 'extern') {
    const f = path.join(__dirname, 'broll', s.file);
    if (!fs.existsSync(f)) throw new Error(`${s.name}: missing extern clip ${f}`);
    // A light lift only. The clip measures Y 89 against 152 for Dan's backyard shots; his own
    // cut already ranges 58-172 across b-roll, so this is not a match-grade, just enough that a
    // dark gym does not read as a different video. Measured after, not guessed.
    const ph = CH - L.dropTop;
    return { inputs: ['-loop', '1', '-framerate', FPS, '-i', path.join(A, 'j2-bg.png')],
      extern: f, externIn: s.in ?? 0,
      fc: `[0:v]setpts=PTS-STARTPTS,scale=${CW}:-2:flags=lanczos,crop=${CW}:${ph}:0:(ih-${ph})/2,` +
          `eq=brightness=0.045:contrast=1.03:saturation=1.06,setsar=1[pic];` +
          `[1:v][pic]overlay=0:${L.dropTop}:shortest=1,setsar=1[v]`,
      vf: null };
  }
  if (s.t === 'card') {
    const c = L.card;
    const chip = path.join(A, `chip-${s.name}.png`);
    const inputs = ['-loop', '1', '-framerate', FPS, '-i', path.join(A, 'j2-bg.png')];
    // cardCrop trims a flat border BEFORE the card scale. Two source shots are mostly
    // dead fill -- the bubble-gut photo is 70% white surround, the target graphic 65%
    // black -- so scaling the whole frame put a postage stamp inside a big empty card.
    // Measured content bounds, not eyeballed.
    const cc = s.cardCrop;
    const pre = cc
      ? `crop=iw*${(cc[1] - cc[0]).toFixed(4)}:ih*${(cc[3] - cc[2]).toFixed(4)}:` +
        `iw*${cc[0].toFixed(4)}:ih*${cc[2].toFixed(4)},`
      : '';
    // force_original_aspect_ratio keeps a cropped card from being stretched; it is a no-op
    // for a full 16:9 frame, which fits the 1000x562 box exactly.
    // setpts=PTS-STARTPTS is load-bearing too. `-ss` leaves the first decoded frame with a
    // non-zero PTS; the looped background starts at 0, so overlay emitted ONE bare-background
    // frame before the picture arrived. That was the black frame at n=48 of short C - a card
    // shot's own first frame, not a concat artefact.
    let fc =
      `[0:v]setpts=PTS-STARTPTS,${pre}scale=${c.w}:${c.h}:force_original_aspect_ratio=decrease:flags=lanczos,setsar=1[fit];` +
      // shortest=1 is load-bearing. [1:v] is a `-loop 1` still, i.e. an INFINITE stream, and
      // overlay follows its FIRST input - so the last frame or two of every card shot rendered
      // as bare background. It showed up as a 2-frame black flash at 1.58s in short C.
      `[1:v][fit]overlay=${c.x}+(${c.w}-overlay_w)/2:${c.y}+(${c.h}-overlay_h)/2:shortest=1`;
    if (fs.existsSync(chip)) {
      inputs.push('-loop', '1', '-framerate', FPS, '-i', chip);
      fc += `[t];[t][2:v]overlay=(W-w)/2:${c.chipY}:shortest=1`;
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
      `[0:v]setpts=PTS-STARTPTS,split=2[a][b];` +
      `[a]crop=${gw}:${gh}:${box[0]}:${box[1]},scale=-2:${p.gfxH}:flags=lanczos[g];` +
      `[b]crop=${danCropW}:${SRC_H}:${srcX0}:0,scale=${p.danW}:${p.danH}:flags=lanczos[d];` +
      `[1:v][g]overlay=(W-w)/2:${p.gfxTop}[t1];[t1][d]overlay=${p.danX}:${p.danY},setsar=1[v]`;
    return { inputs: ['-loop', '1', '-framerate', FPS, '-i', path.join(A, 'j2-bg.png')], fc, vf: null };
  }
  throw new Error(`unknown treatment ${s.t}`);
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
    const args = f.extern
      ? ['-ss', String(f.externIn), '-i', f.extern, ...f.inputs, '-t', String(s.dur)]
      : ['-ss', String(s.absStart), '-i', SRC, ...f.inputs, '-t', String(s.dur)];
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
    const args = ['-ss', String(p.start), '-i', SRC, '-t', String((p.end - p.start).toFixed(3)), '-vn', '-map', SRCA.map];
    // Bleep windows are in SOURCE time; shift them into this piece's local time.
    const local = segBleeps
      .filter((b) => b[1] > p.start && b[0] < p.end)
      .map((b) => [Math.max(0, b[0] - p.start), Math.min(p.end - p.start, b[1] - p.start)]);
    if (local.length) {
      const cond = local.map(([a, b]) => `between(t,${a.toFixed(3)},${b.toFixed(3)})`).join('+');
      args.push(
        '-f', 'lavfi', '-i', 'sine=frequency=1000:sample_rate=48000',
        '-filter_complex',
        `${SRCA.fc_label}${SRCA.filter},volume=0:enable='${cond}'[sp];` +
        // ffmpeg's `sine` source emits at amplitude 0.125 (-18 dBFS), NOT full scale, so a
        // naive volume=0.20 produced a tone ~11x quieter than the speech around it and the
        // bleep was barely audible. 2.0 puts the peak at ~0.25, comfortably above the
        // surrounding dialogue. Measured, not assumed.
        `[1:a]volume=2.0,volume=0:enable='not(${cond})'[tone];` +
        `[sp][tone]amix=inputs=2:duration=first:normalize=0[a]`,
        '-map', '[a]');
    }
    // The source is SCORED. A hard in-point drops the viewer mid-bar, a hard out stops the
    // bed dead, and an internal splice jumps it. Fade the head and tail of the whole short
    // and dip 60 ms either side of every internal join. Durations are untouched (no
    // acrossfade), so picture and sound stay frame-locked.
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
      args.push('-af', [SRCA.filter, fade].join(','));
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
