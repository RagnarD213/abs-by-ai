// One loudness for the whole batch.
//
// Muhammad's master runs -15.9 LUFS with an LRA of 13.6 - a deliberately dynamic bed that
// swells and drops between sections. Cutting six shorts out of different sections therefore
// produced six different loudnesses (-13.2 to -18.0 LUFS, a 4.8 dB spread), which a viewer
// scrolling from one to the next hears immediately.
//
// Two-pass loudnorm to -14 LUFS / -1.5 dBTP, then alimiter. Not a fresh master: the pass is
// as close to a linear gain as loudnorm will give, and the limiter is there because D needs
// +4 dB against a -2.2 dBTP peak and would otherwise clip. Video is copied, not re-encoded.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { SEGMENTS } = require('./segments.js');
const { FF } = require('./config.js');
const OUT = path.join(__dirname, 'out');
const I = -14, TP = -1.5, LRA = 11;

for (const seg of SEGMENTS) {
  const f = path.join(OUT, `${seg.id.toLowerCase()}_${seg.slug}.mp4`);
  if (!fs.existsSync(f)) { console.log(`${seg.id} missing`); continue; }
  const m = spawnSync(FF, ['-hide_banner', '-i', f, '-af',
    `loudnorm=I=${I}:TP=${TP}:LRA=${LRA}:print_format=json`, '-f', 'null', '-'],
    { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 });
  const err = m.stderr;
  // The measured JSON is the LAST object in stderr. Never write to this stream from a shim.
  const j = JSON.parse(err.slice(err.lastIndexOf('{'), err.lastIndexOf('}') + 1));
  const af = `loudnorm=I=${I}:TP=${TP}:LRA=${LRA}:measured_I=${j.input_i}:measured_TP=${j.input_tp}:` +
    `measured_LRA=${j.input_lra}:measured_thresh=${j.input_thresh}:offset=${j.target_offset}:linear=true,` +
    `alimiter=level=disabled:limit=${(10 ** (TP / 20)).toFixed(4)}`;
  const tmp = f.replace(/\.mp4$/, '.norm.mp4');
  const r = spawnSync(FF, ['-hide_banner', '-loglevel', 'error', '-y', '-i', f,
    '-af', af, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2',
    '-movflags', '+faststart', tmp], { encoding: 'utf8' });
  if (r.status !== 0) { console.error(r.stderr); throw new Error(`${seg.id} normalize failed`); }
  fs.renameSync(tmp, f);
  console.log(`${seg.id}  ${(+j.input_i).toFixed(1)} -> ${I} LUFS   (TP was ${(+j.input_tp).toFixed(1)}, LRA ${j.input_lra})`);
}
