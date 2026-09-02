// Automated QC for the rendered Shorts. Checks the things that are cheap to get wrong:
// container specs, duration drift, dead/black frames, and the audio splice in the
// two segments that are stitched from non-contiguous pieces of the source.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const AUDIO = require('/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/qclib.js');
const { SEGMENTS } = require('./segments.js');
const { loadShots } = require('./plan.js');
const { BLEEPS, BLEEP_WORDS } = require('./bleeps.js');

const { FF, FFPROBE: FP, FPS } = require('./config.js');
const L = JSON.parse(fs.readFileSync(path.join(__dirname, 'layout.json'), 'utf8'));
const OUT = path.join(__dirname, 'out');

const run = (bin, args) => {
  const r = spawnSync(bin, args, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  return (r.stdout || '') + (r.stderr || '');
};

let fail = 0;
const check = (ok, msg) => { if (!ok) { fail++; console.log(`   ✗ ${msg}`); } return ok; };

const ONLY = process.argv.slice(2);
for (const seg of (ONLY.length ? SEGMENTS.filter((s) => ONLY.includes(s.id)) : SEGMENTS)) {
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
  check(g(v, 'r_frame_rate') === FPS, `fps ${g(v, 'r_frame_rate')} (expected ${FPS})`);
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

  // Bleeps: assert the censored window really is a ~1kHz tone in the FINISHED file, and
  // that the word never appears in the burned-in captions.
  const segBleeps = BLEEPS[seg.id] || [];
  if (segBleeps.length) {
    let off = 0, outWins = [];
    for (const p of seg.pieces) {
      for (const b of segBleeps) {
        if (b[1] > p.start && b[0] < p.end) {
          outWins.push([off + Math.max(0, b[0] - p.start), off + Math.min(p.end - p.start, b[1] - p.start)]);
        }
      }
      off += p.end - p.start;
    }
    for (const [a0, b0] of outWins) {
      const r = spawnSync(FF, ['-hide_banner', '-loglevel', 'error', '-ss', String(a0 + 0.04),
        '-i', f, '-t', String(Math.max(0.12, b0 - a0 - 0.08)), '-vn', '-ac', '1', '-ar', '48000',
        '-f', 's16le', '-'], { maxBuffer: 32 * 1024 * 1024 });
      const buf = r.stdout; const N = Math.floor(buf.length / 2);
      const x = new Float64Array(N);
      for (let k = 0; k < N; k++) x[k] = buf.readInt16LE(k * 2) / 32768;
      // Goertzel at 1000 Hz vs total energy — a cheap purity test, no FFT needed.
      const w = 2 * Math.PI * 1000 / 48000; const coeff = 2 * Math.cos(w);
      let s1 = 0, s2 = 0, tot = 0;
      for (let k = 0; k < N; k++) { const v = x[k] * (0.5 - 0.5 * Math.cos(2 * Math.PI * k / (N - 1)));
        const s0 = v + coeff * s1 - s2; s2 = s1; s1 = s0; tot += x[k] * x[k]; }
      const mag = Math.sqrt(s1 * s1 + s2 * s2 - coeff * s1 * s2) / (N / 2);
      const rms = Math.sqrt(tot / N);
      // A Hann window has coherent gain 0.5, so a PURE sine of rms R yields a Goertzel
      // magnitude of R*sqrt(2)*0.5 = 0.707R, not R. Normalising against that puts a pure
      // tone at 1.0 and broadband speech near 0. (The first version compared mag/rms and
      // flagged a verified-pure 1kHz tone as impure at 0.71 -- the metric was wrong, not
      // the audio.)
      const purity = mag / Math.max(1e-9, rms * Math.SQRT1_2);
      console.log(`   bleep ${a0.toFixed(2)}-${b0.toFixed(2)}s: 1kHz mag ${mag.toFixed(3)}, rms ${rms.toFixed(3)}, purity ${purity.toFixed(2)}`);
      check(purity > 0.85 && rms > 0.03, `bleep at ${a0.toFixed(2)}s is not a clear audible 1kHz tone`);
    }
  }

  // Loudness. The source is a finished, already-mastered mix, so the shorts are checked
  // rather than re-normalised - a second loudnorm pass on top of his would squash it.
  const ln = run(FF, ['-hide_banner', '-nostats', '-i', f, '-af', 'ebur128=peak=true',
    '-f', 'null', '-']);
  const I = parseFloat((ln.match(/I:\s*(-?[\d.]+) LUFS/g) || []).pop()?.match(/(-?[\d.]+)/)[1]);
  const TP = parseFloat((ln.match(/Peak:\s*(-?[\d.]+) dBFS/g) || []).pop()?.match(/(-?[\d.]+)/)[1]);
  console.log(`   loudness ${I} LUFS, true peak ${TP} dBTP`);
  // ⚠ THE AUDIO GATE STAMP (2026-09-02). The -22..-10 window above let every rejected batch through;
  // loudness was never what Dan rejected on. _shared/audio/audio_gate.py measures the delivered
  // file against Muhammad's ad (comb, room, tone, floor, dryness, loudness, spread, true peak,
  // silence, length) and writes <file>.audio_gate.json with the file's sha256. No stamp, a stamp
  // for a different build, or a FAIL verdict = NOT DELIVERABLE. finishaudio.py runs the gate.
  {
    const st = AUDIO.requireStamp(f);
    check(st.ok, `audio gate stamp: ${st.out.split('\n').pop()}`);
  }
  check(TP <= 0.0, `true peak ${TP} dBTP is over 0`);

  // The stage is the whole point of this batch's layout: assert the caption band never
  // reaches into it. ASS MarginV 690 with 86pt/2 lines puts the top of a two-line caption
  // around y1015; the stage bottom is y=${L.card.y + L.card.h}.
  check(L.card.y + L.card.h <= 1010,
    `stage bottom y=${L.card.y + L.card.h} runs into the caption band`);

  const ass = fs.readFileSync(path.join(__dirname, 'build', seg.id, `${seg.id}.ass`), 'utf8');
  for (const w of (BLEEP_WORDS[seg.id] || [])) {
    check(!new RegExp(`\\b${w}\\b`, 'i').test(ass), `captions still print the bleeped word "${w}"`);
  }
  const n = (ass.match(/^Dialogue:/gm) || []).length;
  const last = [...ass.matchAll(/^Dialogue: 0,\d:(\d\d):(\d\d\.\d\d)/gm)].pop();
  const lastT = last ? +last[1] * 60 + +last[2] : 0;
  check(lastT <= dur + 0.1, `last caption at ${lastT.toFixed(2)}s runs past the ${dur.toFixed(2)}s video`);
  console.log(`   ${dur.toFixed(1)}s · ${n} captions · ${(fs.statSync(f).size / 1e6).toFixed(1)} MB`);
}

console.log(fail === 0 ? '\nQC PASS — all checks green' : `\nQC: ${fail} check(s) failed`);
process.exit(fail === 0 ? 0 : 1);
