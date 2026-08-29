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
// ⚠ THE VOICE CHAIN, rev 3. RIGHT CHANNEL ONLY, AS MONO.
//
// The camera records TWO MICROPHONES, not stereo: the left input is a room mic 7.58 ms late,
// and summing them combs the voice. Rev 1 and rev 2 both took the handoff's word that the
// clean master's audio "is already correct" - IT IS NOT. Measured, CUT_v1_graded_NO-GRAPHICS
// has L/R correlation +0.069 at a -7.58 ms lag, the same signature as the raw roll and as the
// file explicitly named *_PRE_AUDIOFIX. Only FINAL_supplements.mp4 ever got the 2026-08-23
// repair. So both earlier revisions shipped comb-filtered audio and Dan heard it.
//
// The right channel is also the best source available: SNR 29.8 dB against the summed pair's
// 26.6 and the repaired FINAL master's 19.9 (its treble shelf lifted the lav hiss).
//
// The EQ then brings our lav toward Muhammad's voice, which is Dan's reference. Measured
// against his cut, ours was 3.8 dB short of weight, 3.8 dB short of presence, 8.7 dB short of
// air and 12 dB short above 9 kHz - dull, which is exactly what "doesn't sound as good as
// Muhammad's" means. With this chain the octave-band shape difference falls from 4.05 dB RMS
// to 0.62, sibilance lands within 1.2 dB of his, and our noise floor stays 5.6 dB cleaner.
// Fitted and verified by work/voicechain.py.
const VOICE = fs.readFileSync(path.join(__dirname, 'work', 'voicechain.txt'), 'utf8').trim();
// A small residual correction for the raw-roll insert: same lav and same chain, so this is
// only the difference between two takes. work/fitraw.py.
const RAWFIT = fs.existsSync(path.join(__dirname, 'work', 'rawfit.txt'))
  ? fs.readFileSync(path.join(__dirname, 'work', 'rawfit.txt'), 'utf8').trim()
  : '';

const { FF, SRC, RAW, GRADE, FONTS, FPS, FPS_N } = require('./config.js');
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
  // ONE TREATMENT, `talk`. The clean master is a single locked kitchen camera with no burned
  // graphics, so there is nothing to preserve whole and nothing to avoid slicing.
  // An AI cover clip: native 9:16, so it fills the picture area at about 1:1 rather than
  // being cropped out of 16:9. Carries the AI GENERATED label per the standing rule.
  if (s.t === 'ai') {
    const ph = CH - L.dropTop;
    const f = path.join(__dirname, 'aigen', 'clips', s.file);
    if (!fs.existsSync(f)) throw new Error(`${s.name}: missing clip ${f}`);
    return {
      inputs: ['-loop', '1', '-framerate', FPS, '-i', path.join(A, 'j2-bg.png'),
               '-loop', '1', '-framerate', FPS, '-i', path.join(A, 'ai-label.png')],
      source: f, aiIn: s.aiIn ?? 0.6,
      // ⚠ crop biased UP (0.30 rather than centred). These clips are native 9:16 and the
      // picture area is shorter than 9:16, so filling the width crops 310 rows of height; taken
      // centrally that cut the subject's hairline on the two clips that frame a person.
      fc: `[0:v]setpts=PTS-STARTPTS,scale=${CW}:${ph}:force_original_aspect_ratio=increase,` +
          `crop=${CW}:${ph}:0:(ih-${ph})*0.30,setsar=1[pic];` +
          `[1:v][pic]overlay=0:${L.dropTop}:shortest=1[bg];` +
          `[bg][2:v]overlay=44:${L.dropTop + 34}:shortest=1,setsar=1[v]`,
      vf: null };
  }
  if (s.t !== 'talk') throw new Error(`unknown treatment ${s.t} on ${s.name}`);
  const T = L.talk;
  // ⚠ REV 2 - THE PUNCH. Every join in this batch is either a picture cut inherited from the
  // source edit (Dan: "awkward cut", "jump cut") or one we make by removing a pause. Measured,
  // both jump the picture by 5-12 mean-abs-difference against a 1.30 adjacent-frame baseline,
  // so a join has to be HIDDEN, not just made. Alternating wide/tight across each join reads
  // as a camera change rather than a glitch - the same fix the spray-tan longform applied to
  // 35 of its 43 joins. `tight` costs 1.87x upscale against 1.68x and is set so his head lands
  // at the same delivered y, i.e. only the FRAMING moves, not his position in frame.
  const tight = !!s.tight;
  const cw = tight ? T.tightW : T.cropW;
  const ch = tight ? T.tightH : T.cropH;
  const top = tight ? T.tightTop : T.cropTop;
  const cen = CROPS[s.name];
  if (cen == null) throw new Error(`${s.name}: no measured crop centre`);
  const x = Math.round(Math.min(Math.max(cen * SRC_W - cw / 2, 0), SRC_W - cw));
  const ph = CH - L.dropTop;
  // A raw-roll shot needs the EDL's own grade to match the master. Verified: a graded raw
  // frame correlates 0.9999 with the master frame it became.
  const grade = s.src === 'raw' ? `${GRADE},` : '';
  return {
    inputs: ['-loop', '1', '-framerate', FPS, '-i', path.join(A, 'j2-bg.png')],
    source: s.src === 'raw' ? RAW : SRC,
    // setpts=PTS-STARTPTS and shortest=1 are both load-bearing - see the git history.
    fc: `[0:v]setpts=PTS-STARTPTS,${grade}crop=${cw}:${ch}:${x}:${top},` +
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
    const args = ['-ss', String(s.t === 'ai' ? f.aiIn : s.absStart), '-i', f.source,
                  ...f.inputs, '-t', String(s.dur)];
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
    // Master and raw now come off the SAME lav through the SAME chain, so a raw insert needs
    // only a residual take-to-take correction rather than a whole different treatment.
    const raw = p.src === 'raw';
    const args = ['-ss', String(p.start), '-i', raw ? RAW : SRC,
                  '-t', String((p.end - p.start).toFixed(3)), '-vn'];
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
      if (raw) throw new Error('bleeping a raw-roll piece is not wired up');
      throw new Error('the rev-3 voice chain is not wired into the bleep branch');
      // the bleep branch already built a filter_complex; append the fades to its [a] output
      const k = args.indexOf('-filter_complex');
      args[k + 1] = args[k + 1].replace('[a]', '[amix]') + `;[amix]${fade}[a]`;
    } else {
      // ⚠ ONE -af ONLY. The raw-roll correction and the fades were being pushed as two
      // separate -af flags and ffmpeg honours the LAST one, so the raw EQ was silently
      // discarded and the inserted line kept its 1.45 dB tonal seam through three rebuilds.
      // Chain them instead.
      // ⚠ ONE -af ONLY - ffmpeg honours the last, and pushing the correction and the fades
      // separately silently discarded the correction for three rebuilds.
      args.push('-af', [VOICE, raw ? RAWFIT : '', fade].filter(Boolean).join(','));
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
