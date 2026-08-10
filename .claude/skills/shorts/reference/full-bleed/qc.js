// Automated QC for the rendered Shorts. Checks the things that are cheap to get wrong:
// container specs, duration drift, dead/black frames, and the audio splice in the
// two segments that are stitched from non-contiguous pieces of the source.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { SEGMENTS } = require('./segments.js');
const { loadShots } = require('./plan.js');

const FF = path.join(__dirname, '../../ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg');
const FP = path.join(__dirname, '../../Media/video_edit/bin/ffprobe');
const OUT = path.join(__dirname, 'out');

const run = (bin, args) => {
  const r = spawnSync(bin, args, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  return (r.stdout || '') + (r.stderr || '');
};

let fail = 0;
const check = (ok, msg) => { if (!ok) { fail++; console.log(`   ✗ ${msg}`); } return ok; };

for (const seg of SEGMENTS) {
  const f = path.join(OUT, `${seg.id.toLowerCase()}_${seg.slug}.mp4`);
  console.log(`\n${seg.id}  ${path.basename(f)}`);
  if (!fs.existsSync(f)) { console.log('   ✗ MISSING'); fail++; continue; }

  const v = run(FP, ['-v', 'error', '-select_streams', 'v:0', '-show_entries',
    'stream=width,height,r_frame_rate', '-show_entries', 'format=duration',
    '-of', 'default=noprint_wrappers=1', f]);
  const a = run(FP, ['-v', 'error', '-select_streams', 'a:0', '-show_entries',
    'stream=codec_name,sample_rate,channels', '-of', 'default=noprint_wrappers=1', f]);
  const g = (s, k) => (s.match(new RegExp(`${k}=([^\\s]+)`)) || [])[1];

  const dur = parseFloat(g(v, 'duration'));
  const expect = loadShots().filter((s) => s.seg === seg.id).reduce((x, s) => x + s.dur, 0);
  check(g(v, 'width') === '1080' && g(v, 'height') === '1920', `dims ${g(v,'width')}x${g(v,'height')}`);
  check(g(v, 'r_frame_rate') === '24/1', `fps ${g(v, 'r_frame_rate')}`);
  check(g(a, 'codec_name') === 'aac' && g(a, 'sample_rate') === '48000' && g(a, 'channels') === '2',
    `audio ${g(a,'codec_name')} ${g(a,'sample_rate')} ${g(a,'channels')}ch`);
  check(Math.abs(dur - expect) < 0.25, `duration ${dur.toFixed(2)}s vs planned ${expect.toFixed(2)}s`);

  // Dead-frame check: no frame should be effectively black (a compositing bug shows up here).
  const bl = run(FF, ['-hide_banner', '-nostats', '-loglevel', 'info', '-i', f,
    '-vf', 'blackdetect=d=0.15:pic_th=0.98:pix_th=0.10', '-an', '-f', 'null', '-']);
  const blacks = [...bl.matchAll(/black_start:([\d.]+) black_end:([\d.]+)/g)]
    .map((m) => `${(+m[1]).toFixed(2)}-${(+m[2]).toFixed(2)}s`);
  check(blacks.length === 0, `black frames at ${blacks.join(', ')}`);

  // Audio splice on the stitched segments. Comparing RMS either side of the join is
  // NOT the right test — the cut is deliberately placed in silence, so silence->speech
  // always reads as a big step. What matters is that the splice itself lands in silence,
  // because a cut through speech is what clicks. Measure the window ON the join.
  if (seg.pieces.length > 1) {
    let off = 0;
    for (let i = 0; i < seg.pieces.length - 1; i++) {
      off += seg.pieces[i].end - seg.pieces[i].start;
      // Level is the wrong measure — Dan talks continuously, so any window wide enough
      // to span the join contains the next word's onset regardless of splice quality.
      // A bad splice is a DISCONTINUITY, so compare the largest sample-to-sample jump
      // at the join against the same measure at four control points in the same file.
      const samples = (ss, d) => {
        const r = spawnSync(FF, ['-hide_banner', '-loglevel', 'error', '-ss', String(ss),
          '-i', f, '-t', String(d), '-vn', '-ac', '1', '-ar', '48000', '-f', 's16le', '-'],
          { maxBuffer: 32 * 1024 * 1024 });
        const b = r.stdout;
        const out = [];
        for (let k = 0; k + 1 < b.length; k += 2) out.push(b.readInt16LE(k));
        return out;
      };
      const maxJump = (s) => s.reduce((m, v, k) => (k ? Math.max(m, Math.abs(v - s[k - 1])) : 0), 0);
      const atJoin = maxJump(samples(off - 0.02, 0.04));
      const ctrl = [off - 3, off - 2, off + 2, off + 3]
        .filter((t) => t > 0.1 && t < dur - 0.1).map((t) => maxJump(samples(t, 0.04)));
      const ratio = atJoin / Math.max(1, Math.max(...ctrl));
      console.log(`   join ${off.toFixed(2)}s: sample jump ${atJoin} vs controls ` +
        `[${ctrl.join(', ')}] = ${ratio.toFixed(2)}x`);
      check(ratio < 3, `audible click at the ${off.toFixed(2)}s splice (${ratio.toFixed(1)}x control)`);
    }
  }

  const ass = fs.readFileSync(path.join(__dirname, 'build', seg.id, `${seg.id}.ass`), 'utf8');
  const n = (ass.match(/^Dialogue:/gm) || []).length;
  const last = [...ass.matchAll(/^Dialogue: 0,\d:(\d\d):(\d\d\.\d\d)/gm)].pop();
  const lastT = last ? +last[1] * 60 + +last[2] : 0;
  check(lastT <= dur + 0.1, `last caption at ${lastT.toFixed(2)}s runs past the ${dur.toFixed(2)}s video`);
  console.log(`   ${dur.toFixed(1)}s · ${n} captions · ${(fs.statSync(f).size / 1e6).toFixed(1)} MB`);
}

console.log(fail === 0 ? '\nQC PASS — all checks green' : `\nQC: ${fail} check(s) failed`);
process.exit(fail === 0 ? 0 : 1);
