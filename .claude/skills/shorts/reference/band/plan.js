// Rebuild of V4 short1 "The 4 Ab Muscles" with a dedicated graphics band.
//
// The original put the title and four accumulating chips ON TOP of Dan. Measurement of
// the delivered file showed no region of the frame stays clear of him (best candidate was
// clear 33% of the time, 0% in its worst frame), so the fix is to MAKE space rather than
// hunt for it: his footage occupies the lower ~74%, and the top band is graphics-only.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const HERE = __dirname;
const V4 = path.join(HERE, '..', '..', 'V4 - The Ultimate 1 Minute Ab Workout(2).mp4 - READY FOR UPLOAD.mp4');
const FF = path.join(HERE, '../../../ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg');
const words = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'v4-words.json'), 'utf8')).chunks;

// ---- phrase lookup over the word timestamps -------------------------------------
const norm = (s) => s.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
const flat = words.map((w) => norm(w.text)).join(' ');
const offsets = [];
{ let p = 0; words.forEach((w, i) => { const t = norm(w.text); offsets.push({ s: p, e: p + t.length, i }); p += t.length + 1; }); }
const wordAt = (c) => { for (const o of offsets) if (c >= o.s && c <= o.e) return o.i; return -1; };
function find(phrase, nth = 0) {
  const q = norm(phrase);
  let from = 0, hit = -1;
  for (let k = 0; k <= nth; k++) { hit = flat.indexOf(q, from); if (hit === -1) throw new Error(`not found: ${phrase}`); from = hit + 1; }
  const a = wordAt(hit), b = wordAt(hit + q.length - 1);
  return { a, b, t0: words[a].timestamp[0], t1: words[b].timestamp[1] };
}

// ---- silence-snapped cut points --------------------------------------------------
const SILENCE = (() => {
  const txt = fs.readFileSync(path.join(HERE, 'silence.txt'), 'utf8');
  const out = []; let open = null;
  for (const line of txt.split('\n')) {
    const s = line.match(/silence_start:\s*([\d.]+)/), e = line.match(/silence_end:\s*([\d.]+)/);
    if (s) open = parseFloat(s[1]); else if (e && open !== null) { out.push([open, parseFloat(e[1])]); open = null; }
  }
  return out;
})();
function snapIn(t, floor, preroll = 0.22) {
  let best = null;
  for (const [a, b] of SILENCE) { if (b > t + 0.20) break; if (b >= floor - 0.05) best = [a, b]; }
  if (!best) return Math.max(0, floor, t - 0.10);
  return Math.max(best[0], best[1] - preroll, floor - 0.05);
}
function snapOut(t, ceil, tail = 0.34) {
  for (const [a, b] of SILENCE) { if (a < t - 0.20) continue; if (a > ceil + 0.05) break; return Math.min(b, a + tail, ceil + 0.05); }
  return Math.min(t + 0.12, ceil + 0.05);
}

const IN = find('There are four muscle groups within your abs');
const OUT = find("that's the transverse abdominis");
const START = +snapIn(IN.t0, words[IN.a - 1] ? words[IN.a - 1].timestamp[1] : 0).toFixed(2);
const END = +snapOut(OUT.t1, words[OUT.b + 1] ? words[OUT.b + 1].timestamp[0] : OUT.t1 + 0.4).toFixed(2);

// ---- chip reveal windows, in OUTPUT time -----------------------------------------
// One chip at a time. Chip 1 is held until chip 2 is named so the band is never empty.
const rel = (t) => +(t - START).toFixed(2);
const OBLIQUES_IN = rel(find('the internal obliques').t0);
const TRANSVERSE_IN = rel(find('And finally, there is the transverse abdominis').t0);
// He names internal and external ~1s apart, so syncing each chip to its own word leaves
// INTERNAL on screen for 1.08s — unreadable. Hand INTERNAL the whole naming phrase and
// switch to EXTERNAL the moment he finishes saying it; EXTERNAL then holds through
// "twisting motions or bending motions", which is exactly what its sub line says.
const OBLIQUES_MID = rel(find('and the external obliques').t1);
const CHIPS = [
  { n: 1, key: 'rectus',     title: 'RECTUS ABDOMINIS',     sub: 'THE SIX-PACK  ·  CRUNCHING MOTIONS',
    from: rel(find('First is the rectus abdominis').t0), to: OBLIQUES_IN },
  { n: 2, key: 'internal',   title: 'INTERNAL OBLIQUES',    sub: 'ROTATION  ·  CORE STABILITY',
    from: OBLIQUES_IN, to: OBLIQUES_MID },
  { n: 3, key: 'external',   title: 'EXTERNAL OBLIQUES',    sub: 'TWISTING  ·  BENDING',
    from: OBLIQUES_MID, to: TRANSVERSE_IN },
  { n: 4, key: 'transverse', title: 'TRANSVERSE ABDOMINIS', sub: 'DEEP CORE  ·  HOLDS EVERYTHING TOGETHER',
    from: TRANSVERSE_IN, to: +(END - START).toFixed(2) },
];

// ---- shots inside the segment ----------------------------------------------------
function detectShots() {
  const dur = +(END - START).toFixed(2);
  const r = spawnSync(FF, ['-hide_banner', '-nostats', '-loglevel', 'info',
    '-ss', String(START), '-i', V4, '-t', String(dur),
    '-vf', "select='gt(scene,0.18)',showinfo", '-an', '-f', 'null', '-'],
    { encoding: 'utf8', maxBuffer: 128 * 1024 * 1024 });
  const log = (r.stdout || '') + (r.stderr || '');
  if (!/showinfo/.test(log)) throw new Error('showinfo produced no output');  // stderr, not stdout
  const cuts = [...log.matchAll(/pts_time:([\d.]+)/g)].map((m) => parseFloat(m[1]))
    .filter((t) => t > 0.35 && t < dur - 0.2).sort((a, b) => a - b);
  const bounds = [0, ...cuts, dur];
  const shots = [];
  for (let i = 0; i < bounds.length - 1; i++) {
    const a = bounds[i], b = bounds[i + 1];
    if (b - a < 0.25) continue;
    shots.push({ i: shots.length, a: +a.toFixed(2), b: +b.toFixed(2),
                 absStart: +(START + a).toFixed(2), dur: +(b - a).toFixed(2) });
  }
  return shots;
}

module.exports = { V4, FF, START, END, CHIPS, detectShots, words };

if (require.main === module) {
  const shots = detectShots();
  console.log(`segment ${START}s -> ${END}s  (${(END - START).toFixed(1)}s)`);
  const spoken = words.filter((w) => w.timestamp[1] > START && w.timestamp[0] < END);
  console.log(`  in : "${spoken.slice(0, 8).map((w) => w.text.trim()).join(' ')} ..."`);
  console.log(`  out: "... ${spoken.slice(-7).map((w) => w.text.trim()).join(' ')}"`);
  console.log('\nchip windows (output time):');
  for (const c of CHIPS) console.log(`  ${c.n}. ${c.title.padEnd(22)} ${c.from.toFixed(2)} -> ${c.to.toFixed(2)}s`);
  console.log(`\n${shots.length} shots:`);
  for (const s of shots) console.log(`  ${s.i}: ${s.a}-${s.b} (${s.dur}s) @src ${s.absStart}`);
  fs.writeFileSync(path.join(HERE, 'shots.json'), JSON.stringify(shots, null, 1));
}
