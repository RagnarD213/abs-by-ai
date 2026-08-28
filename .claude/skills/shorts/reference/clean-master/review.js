// 540p review copies, each SCANNED FOR SILENT SECONDS before it is sent.
//
// Standing rule since the ad-1 rev-4 incident: a mux can silently truncate the audio stream
// under a full-length video and exit 0, and the review copy is what Dan actually watches -
// so the copy itself gets the check, not just the master.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { FF, FFPROBE } = require('./config.js');
const rows = JSON.parse(fs.readFileSync(path.join(__dirname, 'work', 'delivered.json'), 'utf8'));
const DIR = path.join(__dirname, 'review');
fs.mkdirSync(DIR, { recursive: true });
const SRC = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content';

let fail = 0;
for (const r of rows) {
  const src = path.join(SRC, r.name);
  const out = path.join(DIR, r.name.replace(/\.mp4$/, '_540p.mp4'));
  const enc = spawnSync(FF, ['-hide_banner', '-loglevel', 'error', '-y', '-i', src,
    '-vf', 'scale=540:960:flags=lanczos', '-c:v', 'libx264', '-preset', 'medium', '-crf', '26',
    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out],
    { encoding: 'utf8' });
  if (enc.status !== 0) { console.error(enc.stderr); throw new Error(`encode failed: ${r.name}`); }

  // audio-stream length vs video, then a per-second RMS scan for any dead second
  const g = (f, sel, ent) => spawnSync(FFPROBE, ['-v', 'error', '-select_streams', sel,
    '-show_entries', ent, '-of', 'csv=p=0', f], { encoding: 'utf8' }).stdout.trim();
  const vd = parseFloat(g(out, 'v:0', 'format=duration'));
  const ad = parseFloat(g(out, 'a:0', 'stream=duration'));
  const pcm = spawnSync(FF, ['-hide_banner', '-loglevel', 'error', '-i', out, '-vn', '-ac', '1',
    '-ar', '8000', '-f', 's16le', '-'], { maxBuffer: 64 * 1024 * 1024 }).stdout;
  let silent = 0, minDb = 0;
  for (let s = 0; (s + 1) * 8000 * 2 <= pcm.length; s++) {
    let sum = 0;
    for (let k = s * 8000; k < (s + 1) * 8000; k++) { const v = pcm.readInt16LE(k * 2) / 32768; sum += v * v; }
    const db = 10 * Math.log10(Math.max(1e-12, sum / 8000));
    if (db < -50) silent++;
    if (s === 0 || db < minDb) minDb = db;
  }
  const ok = silent === 0 && Math.abs(vd - ad) < 0.15;
  if (!ok) fail++;
  console.log(`  ${ok ? 'OK ' : '✗  '} ${path.basename(out).padEnd(58)} ` +
    `${vd.toFixed(1)}s  a/v delta ${(vd - ad).toFixed(3)}s  silent seconds ${silent}  ` +
    `quietest ${minDb.toFixed(1)} dB  ${(fs.statSync(out).size / 1e6).toFixed(1)} MB`);
}
console.log(fail === 0 ? '\nreview copies clean' : `\n${fail} review copy problem(s)`);
process.exit(fail === 0 ? 0 : 1);
