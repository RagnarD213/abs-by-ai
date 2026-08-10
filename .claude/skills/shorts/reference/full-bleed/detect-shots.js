// Find every shot boundary inside each chosen Short segment, then pull one representative
// frame per shot. This is how we catch the 16:9 graphics / B-roll / PiP overlays that a
// blind 9:16 centre crop would slice through.
const fs = require('fs');
const path = require('path');
const { execFileSync, spawnSync } = require('child_process');
const { SEGMENTS } = require('./segments.js');

const FF = path.join(__dirname, '../../ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg');
const SRC = path.join(__dirname, '../V2 - How To Get Real Six Pack Abs With AI(2) - READY FOR UPLOAD.mp4');
const OUT = path.join(__dirname, 'shots');
fs.mkdirSync(OUT, { recursive: true });

const SCENE_THRESHOLD = 0.18; // deliberately low — a PiP appearing is a small frame delta

const manifest = [];

for (const seg of SEGMENTS) {
  seg.pieces.forEach((p, pi) => {
    const dur = +(p.end - p.start).toFixed(2);
    // scene changes, reported relative to the trimmed piece
    // NOTE: ffmpeg writes showinfo to STDERR. execFileSync returns stdout only, which
    // silently yielded "0 cuts" for every segment on the first pass — use spawnSync.
    const r = spawnSync(FF, [
      '-hide_banner', '-nostats', '-loglevel', 'info',
      '-ss', String(p.start), '-i', SRC, '-t', String(dur),
      '-vf', `select='gt(scene,${SCENE_THRESHOLD})',showinfo`,
      '-an', '-f', 'null', '-',
    ], { encoding: 'utf8', maxBuffer: 128 * 1024 * 1024 });
    const log = (r.stdout || '') + (r.stderr || '');
    if (!/showinfo/.test(log)) throw new Error(`showinfo produced no output for ${seg.id} p${pi}`);
    const cuts = [...log.matchAll(/pts_time:([\d.]+)/g)]
      .map((m) => parseFloat(m[1])).filter((t) => t <= dur + 0.5).sort((x, y) => x - y);

    // shot list = [0, ...cuts, dur]
    const bounds = [0, ...cuts.filter((c) => c > 0.35 && c < dur - 0.2), dur];
    const shots = [];
    for (let i = 0; i < bounds.length - 1; i++) {
      const a = bounds[i], b = bounds[i + 1];
      if (b - a < 0.25) continue;                 // ignore flicker
      shots.push({ a: +a.toFixed(2), b: +b.toFixed(2), mid: +((a + b) / 2).toFixed(2) });
    }

    shots.forEach((s, si) => {
      const name = `${seg.id}-p${pi}-s${String(si).padStart(2, '0')}`;
      const img = path.join(OUT, name + '.jpg');
      execFileSync(FF, [
        '-hide_banner', '-loglevel', 'error', '-y',
        '-ss', String(+(p.start + s.mid).toFixed(2)), '-i', SRC,
        '-frames:v', '1', '-vf', 'scale=480:-1', img,
      ]);
      manifest.push({ seg: seg.id, piece: pi, shot: si, name,
                      absStart: +(p.start + s.a).toFixed(2), dur: +(s.b - s.a).toFixed(2) });
    });

    console.log(`${seg.id} piece ${pi}: ${dur.toFixed(1)}s -> ${shots.length} shot(s)  ` +
      shots.map((s) => `${s.a}-${s.b}`).join(' | '));
  });
}

fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 1));
console.log(`\n${manifest.length} shot frames written to shots/`);
