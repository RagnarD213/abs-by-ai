// Shot boundaries for the supplements Shorts.
//
// ⚠ THIS DOES NOT SCENE-DETECT, AND THAT IS THE POINT. The other batches infer cuts from a
// 320x180 `scene` score, which on the ab-wheel build landed a boundary 0.60s early and gave
// 18 frames of b-roll a talking-head crop - a timing bug that presented as a framing bug.
// Here the source is OUR OWN cut and its EDL lists every splice, so the boundaries are known
// exactly rather than inferred.
//
// The EDL's cumulative positions are NOT usable raw: render.py rounds each of the 62 ranges
// to whole frames and the error accumulates monotonically to +1.137s by the end of the video
// (which is exactly the 1.149s by which the EDL undershoots the master's duration). So
// work/splices.py measures each boundary as a full-frame-rate frame-difference peak inside a
// window around its prediction, and asserts the correction is monotonic. Every one of the 61
// boundaries came back at 3.2x-22x the local median difference. work/splices.json is that
// table; this file just intersects it with the chosen pieces.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { SEGMENTS } = require('./segments.js');
const { FF, SRC, RAW, GRADE } = require('./config.js');

const OUT = path.join(__dirname, 'shots');
fs.mkdirSync(OUT, { recursive: true });
const SPLICES = JSON.parse(fs.readFileSync(path.join(__dirname, 'work', 'splices.json'), 'utf8'))
  .map((s) => s.cut);
const MASTER = 1409.523;
const EDGES = [...SPLICES, MASTER];

// A cut this close to a piece edge is the piece's own in/out point, not an internal shot
// change; splitting there makes a sliver shot with its own crop.
const MIN_SHOT = 0.40;

const manifest = [];
for (const seg of SEGMENTS) {
  seg.pieces.forEach((p, pi) => {
    // A raw-roll piece has no relationship to the master's splice table - it is one
    // continuous take straight off the camera, so it is always exactly one shot.
    const inner = p.src === 'raw' ? []
      : EDGES.filter((c) => c > p.start + MIN_SHOT && c < p.end - MIN_SHOT);
    const bounds = [p.start, ...inner, p.end];
    for (let i = 0; i < bounds.length - 1; i++) {
      const a = bounds[i], b = bounds[i + 1];
      const name = `${seg.id}-p${pi}-s${String(i).padStart(2, '0')}`;
      // the EDL beat this shot belongs to, so plan.js can look up its measured torso centre
      const beat = p.src === 'raw' ? -1 : SPLICES.filter((c) => c <= a + 0.001).length - 1;
      const src = p.src === 'raw' ? RAW : SRC;
      const vf = p.src === 'raw' ? `${GRADE},scale=480:-1` : 'scale=480:-1';
      execFileSync(FF, ['-hide_banner', '-loglevel', 'error', '-y',
        '-ss', String(+((a + b) / 2).toFixed(3)), '-i', src,
        '-frames:v', '1', '-vf', vf, path.join(OUT, name + '.jpg')]);
      manifest.push({ seg: seg.id, piece: pi, shot: i, name, beat,
                      src: p.src || 'master',
                      absStart: +a.toFixed(3), dur: +(b - a).toFixed(3) });
    }
    console.log(`${seg.id} piece ${pi}: ${(p.end - p.start).toFixed(1)}s -> ` +
      `${bounds.length - 1} shot(s) at beats ` +
      manifest.filter((m) => m.seg === seg.id && m.piece === pi).map((m) => m.beat).join(','));
  });
}
// ---- AI cover clips over the joins (rev 3) -------------------------------------------
// Each insert straddles a piece join, taking `pre` off the outgoing shot and the remainder
// off the incoming one, so the running time is unchanged and the audio underneath never moves.
const INSERTS = require('./inserts.js');
for (const ins of INSERTS) {
  const clip = path.join(__dirname, 'aigen', 'clips', `${ins.clip}.mp4`);
  if (!fs.existsSync(clip)) { console.log(`  insert ${ins.clip}: clip missing, skipped`); continue; }
  const before = manifest.filter((m) => m.seg === ins.seg && m.piece === ins.afterPiece).pop();
  const afterIdx = manifest.findIndex((m) => m.seg === ins.seg && m.piece === ins.afterPiece + 1);
  if (!before || afterIdx < 0) throw new Error(`insert ${ins.clip}: no join after piece ${ins.afterPiece}`);
  const after = manifest[afterIdx];
  const post = ins.dur - ins.pre;
  if (before.dur <= ins.pre + 0.5 || after.dur <= post + 0.5)
    throw new Error(`insert ${ins.clip}: neighbouring shots too short to give it room`);
  before.dur = +(before.dur - ins.pre).toFixed(3);
  after.absStart = +(after.absStart + post).toFixed(3);
  after.dur = +(after.dur - post).toFixed(3);
  manifest.splice(afterIdx, 0, {
    seg: ins.seg, piece: ins.afterPiece, shot: 99, name: `${ins.seg}-ai-${ins.clip}`,
    beat: -2, src: 'ai', file: `${ins.clip}.mp4`, absStart: 0, dur: ins.dur, aiIn: ins.in ?? 0.6,
  });
  console.log(`  insert ${ins.clip} into ${ins.seg} at the piece ${ins.afterPiece}/${ins.afterPiece+1} join: ${ins.dur}s`);
}

fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 1));
console.log(`\n${manifest.length} shots across ${SEGMENTS.length} shorts`);
