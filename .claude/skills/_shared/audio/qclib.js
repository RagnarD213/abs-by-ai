// The one Node entry point to the shared audio standard (.claude/skills/_shared/audio).
//   const { requireStamp, gate } = require('<repo>/.claude/skills/_shared/audio/qclib.js');
//   const r = requireStamp(file);   // { ok, out }  -- ok=false means NOT DELIVERABLE
// Keeps ONE implementation (require_stamp.py); this only spawns it.
const path = require('path');
const { spawnSync } = require('child_process');
const HERE = __dirname;
function run(script, args) {
  const r = spawnSync('python3', [path.join(HERE, script), ...args], { encoding: 'utf8', maxBuffer: 16 * 1024 * 1024 });
  return { ok: r.status === 0, out: ((r.stdout || '') + (r.stderr || '')).trim() };
}
function requireStamp(file, opts = {}) {
  return run('require_stamp.py', [file, ...(opts.strict ? ['--strict'] : [])]);
}
function gate(file, opts = {}) {
  const a = [file];
  if (opts.synthetic) a.push('--synthetic');
  if (opts.ab) a.push('--ab', opts.ab);
  if (opts.video) a.push('--video', opts.video);
  return run('audio_gate.py', a);
}
function pickLav(file, opts = {}) {
  return run('pick_lav.py', [file, ...(opts.out ? ['--out', opts.out] : [])]);
}
function loadSource(file) {
  const fs = require('fs');
  const p = file.endsWith('.json') ? file : `${file}.audio_source.json`;
  if (!fs.existsSync(p)) throw new Error(`no audio_source.json for ${file} -- run pick_lav.py on it first`);
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}
module.exports = { requireStamp, gate, pickLav, loadSource, AUDIO_DIR: HERE };
