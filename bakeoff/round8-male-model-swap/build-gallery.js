// Round-8 blind gallery: 6 male cases, 4 candidates per row (the current
// production Gemini baseline + 3 challenger models), letters A-D shuffled.
//
// N-way shape (round-1 precedent), NOT 18 paired A/B rows. Two reasons, both
// recorded in AI_COORDINATION.md: it is a third of the labelling work, and the
// paired shape would have LEAKED the blind — the baseline image would appear in
// three separate rows, and a repeated image tells the labeller which candidate
// is the control.
//
// Invariants asserted, not hoped for:
//  - letters for any row already in key.json are PINNED (labels live in
//    localStorage keyed row:letter, so a reshuffle silently re-points an
//    answered verdict at a different model);
//  - every model appears in every slot position 1-2 times across the 6 rows, so
//    no model sits in slot A on every row and no model is systematically last;
//  - zero key entries and zero model names leak into the built HTML.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { CASES, ARMS } = require('./cases');

const OUT = path.join(__dirname, 'out');
const R5 = path.join(__dirname, '..', 'round5-prompt-ab');
const BASELINE_OUT = path.join(R5, 'out');
const PHOTOS = path.join(R5, 'photos');
const TMP = path.join(OUT, 'thumbs');
fs.mkdirSync(TMP, { recursive: true });

const THUMB_W = 460, THUMB_Q = 68;
function thumbDataUri(srcPath, tag) {
  const dest = path.join(TMP, `${tag}.jpg`);
  if (!fs.existsSync(dest)) {
    execFileSync('sips', ['-s', 'format', 'jpeg', '--resampleWidth', String(THUMB_W),
      '-s', 'formatOptions', String(THUMB_Q), srcPath, '--out', dest], { stdio: 'ignore' });
  }
  return 'data:image/jpeg;base64,' + fs.readFileSync(dest).toString('base64');
}

function imgPathFor(c, arm) {
  return arm.baseline
    ? path.join(BASELINE_OUT, `${c.id}__${arm.modelKey}__${arm.reuseSuffix}.jpg`)
    : path.join(OUT, `${c.id}__${arm.modelKey}.jpg`);
}

const keyPath = path.join(OUT, 'key.json');
const prevKey = fs.existsSync(keyPath) ? JSON.parse(fs.readFileSync(keyPath, 'utf8')) : {};

// Only rows where EVERY arm has an image — a partial row would make the pick
// meaningless (a model can't lose a comparison it wasn't in).
const rows = [];
for (const c of CASES) {
  const present = ARMS.filter((a) => fs.existsSync(imgPathFor(c, a)));
  if (present.length !== ARMS.length) {
    console.log(`skip ${c.id}: only ${present.length}/${ARMS.length} arms on disk`);
    continue;
  }
  rows.push({ rowId: c.id, c });
}

const LETTERS = ['A', 'B', 'C', 'D'];

// Deterministic per-row permutation from a salt.
function permFor(rowId, salt) {
  let h = 2166136261 >>> 0;
  for (const ch of (salt + rowId)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; }
  const pool = ARMS.map((a) => a.modelKey);
  const out = [];
  while (pool.length) {
    h ^= h << 13; h >>>= 0; h ^= h >> 17; h ^= h << 5; h >>>= 0;
    out.push(pool.splice(h % pool.length, 1)[0]);
  }
  return out;
}
function pinnedPerm(rowId) {
  const p = LETTERS.map((l) => prevKey[`${rowId}:${l}`]?.modelKey);
  return p.every(Boolean) ? p : null;
}

// Balance search over the FREE rows only. Pinned letters are sacred (they may
// already carry Dan's answers), so their contribution is counted but never
// changed — the search works around them.
const freeRows = rows.filter((r) => !pinnedPerm(r.rowId));
const pinnedRows = rows.filter((r) => pinnedPerm(r.rowId));

function slotCounts(assign) {
  const t = {};
  for (const a of ARMS) t[a.modelKey] = LETTERS.map(() => 0);
  for (const perm of assign) perm.forEach((mk, i) => { t[mk][i]++; });
  return t;
}
let SALT = 's0';
if (freeRows.length) {
  SALT = null;
  const pinnedPerms = pinnedRows.map((r) => pinnedPerm(r.rowId));
  outer: for (let s = 0; s < 20000; s++) {
    const all = pinnedPerms.concat(freeRows.map((r) => permFor(r.rowId, `s${s}`)));
    const t = slotCounts(all);
    // With 6 rows and 4 slots each model must land 1-2 times per slot.
    for (const counts of Object.values(t)) {
      for (const n of counts) if (n < 1 || n > 2) continue outer;
    }
    SALT = `s${s}`; break;
  }
  if (!SALT) throw new Error('no slot-balanced salt found over free rows');
}

const key = {};
const blocks = [];
const assign = [];
for (const r of rows) {
  const perm = pinnedPerm(r.rowId) || permFor(r.rowId, SALT);
  assign.push(perm);
  const cands = perm.map((modelKey, i) => {
    const letter = LETTERS[i];
    const arm = ARMS.find((a) => a.modelKey === modelKey);
    key[`${r.rowId}:${letter}`] = { modelKey, baseline: !!arm.baseline };
    return { letter, img: thumbDataUri(imgPathFor(r.c, arm), `${modelKey}__${r.rowId}`) };
  });
  blocks.push({
    id: r.rowId,
    title: r.c.desc,
    sub: `Intensity: ${r.c.intensityLabel} (${r.c.intensity}) - man - declared start: ${r.c.condition}`,
    before: thumbDataUri(path.join(PHOTOS, r.c.file), `before__${r.c.photoKey}`),
    cands,
  });
}
blocks.sort((a, b) => a.id.localeCompare(b.id));

// Pins must round-trip identically or an answered row has been re-pointed.
for (const [k, v] of Object.entries(prevKey)) {
  if (key[k] && key[k].modelKey !== v.modelKey) throw new Error(`pin violated: ${k}`);
}
fs.writeFileSync(keyPath, JSON.stringify(key, null, 2));

const t = slotCounts(assign);
console.log('slot balance (counts per A/B/C/D across rows):');
for (const [mk, counts] of Object.entries(t)) console.log(`  ${mk.padEnd(26)} ${counts.join(' ')}`);
console.log(`rows: ${blocks.length}, candidates: ${blocks.length * ARMS.length}`);

const TAGS = ['not enough change', 'not enough ab definition', 'too muscular', 'too much change',
  'looks fake', 'face drifted', 'skin tone right', 'just right'];

const html = `<title>Abs By AI - male model swap (blind)</title>
<style>
  :root {
    color-scheme: light dark;
    --bg:#f1f1f2; --panel:#ffffff; --fg:#17191c; --muted:#6a6f75; --line:#dcdde0;
    --accent:#3a6ea5; --pick:#2f7d5f; --mat:#1a1b1d;
    --sans: ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    --mono: ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#0e0f10; --panel:#17181a; --fg:#e9eaec; --muted:#989ca2; --line:#2a2c2f; --accent:#7aa6d6; --pick:#4fb489; }
  }
  :root[data-theme="dark"] { --bg:#0e0f10; --panel:#17181a; --fg:#e9eaec; --muted:#989ca2; --line:#2a2c2f; --accent:#7aa6d6; --pick:#4fb489; }
  :root[data-theme="light"] { --bg:#f1f1f2; --panel:#ffffff; --fg:#17191c; --muted:#6a6f75; --line:#dcdde0; --accent:#3a6ea5; --pick:#2f7d5f; }
  body { background:var(--bg); color:var(--fg); font:16px/1.55 var(--sans); margin:0; padding:0 0 132px; -webkit-text-size-adjust:100%; }
  .wrap { max-width:1100px; margin:0 auto; padding:32px 16px 0; }
  h1 { font-size:1.55rem; line-height:1.2; margin:0 0 10px; letter-spacing:-.015em; text-wrap:balance; }
  .lede { color:var(--muted); max-width:66ch; margin:0 0 22px; }
  .lede strong { color:var(--fg); }
  .steps { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px 20px 14px 34px; margin:0 0 8px; }
  .steps li { margin:5px 0; }
  .warn { color:var(--muted); font-size:.85rem; margin:10px 0 26px; }
  .case { border-top:1px solid var(--line); padding:26px 0; }
  .case h2 { font-size:1.08rem; margin:0 0 3px; letter-spacing:-.01em; text-wrap:balance; }
  .case .sub { color:var(--muted); font-size:.83rem; font-family:var(--mono); margin-bottom:16px; }
  .row { display:grid; grid-template-columns:minmax(130px,175px) 1fr; gap:22px; align-items:start; }
  @media (max-width:760px) { .row { grid-template-columns:1fr; } }
  .frame { background:var(--mat); border-radius:6px; overflow:hidden; display:block; }
  .frame img { width:100%; display:block; cursor:zoom-in; }
  .before .tag { font-family:var(--mono); font-size:.7rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-bottom:6px; }
  .cands { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:16px; }
  .cand { border:1px solid var(--line); border-radius:10px; padding:10px; background:var(--panel); display:flex; flex-direction:column; gap:9px; }
  .cand.best { border-color:var(--pick); box-shadow:inset 0 0 0 1px var(--pick); }
  .cand.acc { border-color:var(--accent); }
  .cand .ltr { font-family:var(--mono); font-size:.78rem; letter-spacing:.14em; color:var(--muted); }
  .cand.best .ltr, .cand.acc .ltr { color:var(--fg); }
  .btns { display:flex; gap:7px; flex-wrap:wrap; }
  button.pick, button.alt { font:inherit; font-size:.8rem; padding:5px 12px; border-radius:6px; border:1px solid var(--line); background:transparent; color:var(--fg); cursor:pointer; }
  button.pick:hover, button.alt:hover { border-color:var(--muted); }
  button.pick.on { background:var(--pick); border-color:var(--pick); color:#fff; }
  button.alt.on { background:var(--accent); border-color:var(--accent); color:#fff; }
  .chips { display:flex; flex-wrap:wrap; gap:4px; }
  .chip { font-size:.71rem; padding:3px 8px; border-radius:5px; border:1px solid var(--line); background:transparent; color:var(--muted); cursor:pointer; user-select:none; }
  .chip.on { background:var(--fg); color:var(--bg); border-color:var(--fg); }
  .note { width:100%; font:inherit; font-size:.8rem; padding:6px 8px; border-radius:6px; border:1px solid var(--line); background:var(--bg); color:var(--fg); box-sizing:border-box; }
  :focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
  .bar { position:fixed; left:0; right:0; bottom:0; background:var(--panel); border-top:1px solid var(--line); padding:12px 16px; display:flex; gap:12px; align-items:center; justify-content:space-between; flex-wrap:wrap; }
  #prog { font-family:var(--mono); font-size:.82rem; font-variant-numeric:tabular-nums; color:var(--muted); }
  .bar button { font:inherit; padding:9px 16px; border-radius:8px; border:0; background:var(--accent); color:#fff; cursor:pointer; font-weight:600; }
  .bar .ghost { background:transparent; color:var(--muted); border:1px solid var(--line); font-weight:400; }
  #outbox { width:100%; max-width:1100px; margin:12px auto 0; display:none; }
  #outbox textarea { width:100%; height:220px; font-family:var(--mono); font-size:.74rem; padding:10px; border-radius:8px; border:1px solid var(--line); background:var(--panel); color:var(--fg); box-sizing:border-box; }
  .zoom { position:fixed; inset:0; background:#0b0b0c; display:none; align-items:center; justify-content:center; z-index:50; padding:16px; cursor:zoom-out; }
  .zoom img { max-width:100%; max-height:100%; }
</style>
<div class="wrap">
  <h1>Four ways to build the same guy - which one is right?</h1>
  <p class="lede">We have tried four times to fix the weak male results by rewriting the instructions, and all four were measured failures. So this test changes the <strong>engine</strong> instead. Every image in a row was made from the <strong>identical instructions</strong> and the <strong>same before photo</strong> - the only difference is which AI engine drew it. One of the four in each row is <strong>what the app ships today</strong>; the other three are replacements. Which is which is hidden and shuffled per row.</p>
  <ol class="steps">
    <li><strong>Pick the best one</strong> in each row (green). If none is good enough to ship, pick nothing and say why in the note - "none of these" is a real answer.</li>
    <li>Mark any others <strong>Acceptable</strong> (blue) if you would ship them too.</li>
    <li>Tag what is wrong. The ones that decide this: <strong>not enough change</strong> and <strong>not enough ab definition</strong> - that is the exact complaint that has failed every previous fix.</li>
    <li>Hit <strong>Copy labels</strong> and paste the text back.</li>
  </ol>
  <p class="warn">Tap any image to enlarge. Answers save in this browser as you go.</p>
  ${blocks.map((b) => `
  <section class="case" data-case="${b.id}">
    <h2>${b.title}</h2>
    <div class="sub">${b.sub}</div>
    <div class="row">
      <div class="before"><div class="tag">Before</div><div class="frame"><img src="${b.before}" alt="before"></div></div>
      <div class="cands">
        ${b.cands.map((c) => `
        <div class="cand" data-c="${b.id}" data-l="${c.letter}">
          <span class="ltr">${c.letter}</span>
          <div class="frame"><img src="${c.img}" alt="candidate ${c.letter}"></div>
          <div class="btns">
            <button class="pick" type="button">Best</button>
            <button class="alt" type="button">Acceptable</button>
          </div>
          <div class="chips">${TAGS.map((t) => `<span class="chip" role="button" tabindex="0">${t}</span>`).join('')}</div>
          <input class="note" placeholder="why? (optional)">
        </div>`).join('')}
      </div>
    </div>
  </section>`).join('')}
  <div id="outbox"><textarea readonly></textarea></div>
</div>
<div class="bar">
  <span id="prog"></span>
  <span>
    <button class="ghost" type="button" id="reset">Clear all</button>
    <button type="button" id="copy">Copy labels</button>
  </span>
</div>
<div class="zoom" id="zoom"><img alt="enlarged"></div>
<script>
const KEY = 'absbyai-round8-male-model-swap';
const state = JSON.parse(localStorage.getItem(KEY) || '{}');
function get(c, l) { const k = c + ':' + l; return state[k] || (state[k] = { best:false, acceptable:false, tags:[], note:'' }); }
function save() { localStorage.setItem(KEY, JSON.stringify(state)); render(); }
function render() {
  document.querySelectorAll('.cand').forEach(el => {
    const s = get(el.dataset.c, el.dataset.l);
    el.classList.toggle('best', !!s.best);
    el.classList.toggle('acc', !!s.acceptable);
    el.querySelector('.pick').classList.toggle('on', !!s.best);
    el.querySelector('.alt').classList.toggle('on', !!s.acceptable);
    el.querySelectorAll('.chip').forEach(ch => ch.classList.toggle('on', s.tags.includes(ch.textContent)));
    const note = el.querySelector('.note');
    if (note.value !== s.note) note.value = s.note;
  });
  const cases = [...document.querySelectorAll('.case')];
  const done = cases.filter(sec => [...sec.querySelectorAll('.cand')].some(el => {
    const s = get(el.dataset.c, el.dataset.l);
    return s.best || s.acceptable || s.tags.length || s.note;
  })).length;
  document.getElementById('prog').textContent = done + ' of ' + cases.length + ' rows answered';
}
document.querySelectorAll('.cand').forEach(el => {
  const c = el.dataset.c, l = el.dataset.l;
  el.querySelector('.pick').onclick = () => {
    const cur = get(c, l).best;
    document.querySelectorAll('.cand[data-c="' + c + '"]').forEach(o => { get(c, o.dataset.l).best = false; });
    get(c, l).best = !cur;
    if (get(c, l).best) get(c, l).acceptable = false;
    save();
  };
  el.querySelector('.alt').onclick = () => { const s = get(c, l); s.acceptable = !s.acceptable; if (s.acceptable) s.best = false; save(); };
  el.querySelectorAll('.chip').forEach(ch => {
    const t = () => { const s = get(c, l), x = ch.textContent; s.tags = s.tags.includes(x) ? s.tags.filter(y => y !== x) : s.tags.concat(x); save(); };
    ch.onclick = t;
    ch.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } };
  });
  el.querySelector('.note').oninput = (e) => { get(c, l).note = e.target.value; localStorage.setItem(KEY, JSON.stringify(state)); };
  el.querySelector('img').onclick = () => {
    const z = document.getElementById('zoom');
    z.querySelector('img').src = el.querySelector('img').src; z.style.display = 'flex';
  };
});
document.querySelectorAll('.before img').forEach(img => { img.onclick = () => {
  const z = document.getElementById('zoom'); z.querySelector('img').src = img.src; z.style.display = 'flex'; }; });
document.getElementById('zoom').onclick = (e) => { e.currentTarget.style.display = 'none'; };
document.getElementById('reset').onclick = () => { if (confirm('Clear every label?')) { localStorage.removeItem(KEY); location.reload(); } };
document.getElementById('copy').onclick = async () => {
  const out = {};
  for (const [k, v] of Object.entries(state)) if (v.best || v.acceptable || v.tags.length || v.note) out[k] = v;
  const text = JSON.stringify(out, null, 1);
  const box = document.getElementById('outbox');
  box.style.display = 'block';
  box.querySelector('textarea').value = text;
  box.querySelector('textarea').select();
  try { await navigator.clipboard.writeText(text); document.getElementById('copy').textContent = 'Copied - paste to Claude'; }
  catch (e) { document.getElementById('copy').textContent = 'Select the text below and copy'; }
  box.scrollIntoView({ behavior: 'smooth' });
};
render();
</script>`;

const cut = html.indexOf('<script>');
const safe = html.slice(0, cut).replace(new RegExp('[^\\x00-\\x7F]', 'g'), (ch) => `&#${ch.charCodeAt(0)};`) + html.slice(cut);
const outFile = path.join(OUT, 'gallery.html');
fs.writeFileSync(outFile, safe);
console.log(`gallery.html: ${(fs.statSync(outFile).size / 1048576).toFixed(2)} MB`);

// ── Blinding check ──────────────────────────────────────────────────────────
// Nothing that identifies which letter is which model may survive into the page.
let leaks = [];
for (const k of Object.keys(key)) if (safe.includes(`"${k}"`)) leaks.push(`key entry ${k}`);
for (const a of ARMS) {
  if (safe.includes(a.modelKey)) leaks.push(`model slug ${a.modelKey}`);
  for (const word of ['Gemini', 'Nano Banana', 'Seedream', 'baseline', 'challenger', 'modelKey']) {
    if (safe.includes(word)) leaks.push(`word "${word}"`);
  }
}
leaks = [...new Set(leaks)];
console.log(leaks.length ? `BLINDING LEAK: ${leaks.join(', ')}` : 'blinding check: no key entries, model slugs or model names in HTML');
process.exitCode = leaks.length ? 1 : 0;
