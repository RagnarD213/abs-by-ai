// Blind A/B gallery: FULL prompt vs CONDENSED prompt, model held constant within
// a row. Only the prompt differs between the two images the user compares, so a
// pick is a direct vote on the prompt variant with no model-identity confound.
//
// Two invariants this file must preserve (both have bitten before):
//   1. PIN the letter assignment of any row already present in key.json. Labels
//      live in localStorage keyed by `row:letter`; letting the salt search
//      reshuffle an answered row silently re-points a verdict at the other
//      variant. Adding rows to a published gallery is only safe because of this.
//   2. ASSERT the slot-A balance PER SET. A naive shuffle once put one variant in
//      slot A on every row, stacking every candidate against the same position
//      bias. Balance is asserted, not hoped for.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { CASES: ALL_CASES, VARIANTS, armsFor } = require('./cases');

const OUT = path.join(__dirname, 'out');
const PHOTOS = path.join(__dirname, 'photos');
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

// ── Enumerate the rows that actually have BOTH variants on disk ───────────────
const CASES = ALL_CASES.filter((c) => !c.excluded);
const rows = [];
for (const c of CASES) {
  for (const arm of armsFor(c)) {
    const files = {};
    let complete = true;
    for (const v of VARIANTS) {
      const f = path.join(OUT, `${c.id}__${arm.modelKey}__${v}.jpg`);
      if (!fs.existsSync(f)) { complete = false; break; }
      files[v] = f;
    }
    if (!complete) continue;
    rows.push({ rowId: `${c.id}__${arm.modelKey}`, c, arm, files });
  }
}
rows.sort((a, b) => a.arm.set - b.arm.set || a.rowId.localeCompare(b.rowId));

// ── Letter assignment: pinned for known rows, balanced salt for the rest ──────
const KEY_FILE = path.join(OUT, 'key.json');
const existingKey = fs.existsSync(KEY_FILE) ? JSON.parse(fs.readFileSync(KEY_FILE, 'utf8')) : {};

function pinnedOrder(rowId) {
  const a = existingKey[`${rowId}:A`], b = existingKey[`${rowId}:B`];
  if (a && b) return [a.variant, b.variant];
  return null;
}
function saltOrder(rowId, salt) {
  let h = 2166136261 >>> 0;
  for (const ch of (salt + rowId)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; }
  return (h & 1) ? ['full', 'condensed'] : ['condensed', 'full'];
}

const free = rows.filter((r) => !pinnedOrder(r.rowId));
// Balance is asserted per set, counting the already-pinned rows too, so a
// re-publish that adds rows keeps the overall split honest.
function balanceFor(salt) {
  const per = {};
  for (const r of rows) {
    const order = pinnedOrder(r.rowId) || saltOrder(r.rowId, salt);
    per[r.arm.set] = per[r.arm.set] || { full: 0, condensed: 0 };
    per[r.arm.set][order[0]]++;
  }
  return per;
}
function balanced(per) {
  return Object.entries(per).every(([set, c]) => {
    const n = rows.filter((r) => String(r.arm.set) === set).length;
    return Math.abs(c.full - c.condensed) <= (n % 2 === 0 ? 0 : 1);
  });
}

let SALT = null;
for (let s = 0; s < 5000 && SALT === null; s++) {
  if (balanced(balanceFor(`s${s}`))) SALT = `s${s}`;
}
if (!SALT) {
  // Only reachable if pinned rows alone are already lopsided; report rather than
  // silently publishing an unbalanced gallery.
  throw new Error('no salt achieves per-set slot-A balance (pinned rows may be lopsided)');
}

const key = {};
const blocks = [];
const perSetBalance = balanceFor(SALT);

for (const r of rows) {
  const order = pinnedOrder(r.rowId) || saltOrder(r.rowId, SALT);
  const cands = order.map((variant, i) => {
    const letter = 'AB'[i];
    key[`${r.rowId}:${letter}`] = {
      variant,
      modelKey: r.arm.modelKey,
      set: r.arm.set,
      caseId: r.c.id,
      gender: r.c.gender,
      condition: r.c.condition,
      intensity: r.c.intensity,
    };
    return { letter, img: thumbDataUri(r.files[variant], `${variant}__${r.rowId}`) };
  });
  const who = r.c.gender === 'female' ? 'woman' : 'man';
  blocks.push({
    rowId: r.rowId,
    set: r.arm.set,
    title: r.c.desc,
    sub: `${r.c.intensityLabel} (${r.c.intensity}) - ${who} - declared start: ${r.c.condition}`,
    before: thumbDataUri(path.join(PHOTOS, r.c.file), `before__${r.c.photoKey}`),
    cands,
  });
}

fs.writeFileSync(KEY_FILE, JSON.stringify(key, null, 2));

// ── Assertions, printed loudly ────────────────────────────────────────────────
let fail = 0;
const ck = (ok, msg) => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${msg}`); if (!ok) fail++; };
console.log(`salt: ${SALT} · rows: ${rows.length} (${free.length} newly assigned, ${rows.length - free.length} pinned)`);
for (const [set, c] of Object.entries(perSetBalance)) {
  const n = rows.filter((r) => String(r.arm.set) === set).length;
  ck(Math.abs(c.full - c.condensed) <= (n % 2 === 0 ? 0 : 1),
     `set ${set}: slot-A balance full=${c.full} condensed=${c.condensed} of ${n} rows`);
}
ck(Object.keys(key).length === rows.length * 2, `key.json has 2 entries per row (${Object.keys(key).length})`);
// Every row must contain exactly one full and one condensed.
ck(rows.every((r) => {
  const vs = ['A', 'B'].map((l) => key[`${r.rowId}:${l}`].variant).sort();
  return vs[0] === 'condensed' && vs[1] === 'full';
}), 'every row pairs exactly one full against one condensed');

const setCounts = rows.reduce((a, r) => (a[r.arm.set] = (a[r.arm.set] || 0) + 1, a), {});
console.log('rows per set:', JSON.stringify(setCounts));

const TAGS = ['not enough change', 'too much change', 'too muscular', 'too tan',
  'skin tone right', 'looks fake', 'face drifted', 'not enough ab definition', 'just right'];

const SET_INTRO = {
  1: { h: 'Set 1 &mdash; please do these first', p: 'These 12 rows decide the question on their own. If you only have time for one set, do this one.' },
  2: { h: 'Set 2 &mdash; optional', p: 'A cross-check on a second image model. Useful but not required &mdash; skip it if you are short on time.' },
};

let lastSet = null;
const bodyBlocks = blocks.map((b) => {
  let head = '';
  if (b.set !== lastSet) {
    lastSet = b.set;
    const s = SET_INTRO[b.set];
    head = `<div class="setsplit"><h2>${s.h}</h2><p>${s.p}</p></div>`;
  }
  return head + `
  <section class="case" data-case="${b.rowId}">
    <h3>${b.title}</h3>
    <div class="sub">${b.sub}</div>
    <div class="row">
      <div class="before"><div class="tag">Before</div><div class="frame"><img src="${b.before}" alt="before"></div></div>
      <div class="cands">
        ${b.cands.map((c) => `
        <div class="cand" data-c="${b.rowId}" data-l="${c.letter}">
          <span class="ltr">${c.letter}</span>
          <div class="frame"><img src="${c.img}" alt="candidate ${c.letter}"></div>
          <div class="btns">
            <button class="pick" type="button">Better</button>
            <button class="alt" type="button">Acceptable</button>
          </div>
          <div class="chips">${TAGS.map((t) => `<span class="chip" role="button" tabindex="0">${t}</span>`).join('')}</div>
          <input class="note" placeholder="why? (optional)">
        </div>`).join('')}
      </div>
    </div>
  </section>`;
}).join('');

const html = `<title>Abs By AI - short vs long instructions (blind A/B)</title>
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
  .wrap { max-width:1000px; margin:0 auto; padding:32px 16px 0; }
  h1 { font-size:1.55rem; line-height:1.2; margin:0 0 10px; letter-spacing:-.015em; text-wrap:balance; }
  .lede { color:var(--muted); max-width:66ch; margin:0 0 22px; }
  .lede strong { color:var(--fg); }
  .steps { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px 20px 14px 34px; margin:0 0 8px; }
  .steps li { margin:5px 0; }
  .warn { color:var(--muted); font-size:.85rem; margin:10px 0 26px; }
  .setsplit { margin:34px 0 4px; padding:16px 18px; background:var(--panel); border:1px solid var(--line); border-radius:10px; }
  .setsplit h2 { font-size:1.12rem; margin:0 0 4px; letter-spacing:-.01em; }
  .setsplit p { margin:0; color:var(--muted); font-size:.88rem; max-width:62ch; }
  .case { border-top:1px solid var(--line); padding:26px 0; }
  .case h3 { font-size:1.08rem; margin:0 0 3px; letter-spacing:-.01em; text-wrap:balance; font-weight:600; }
  .case .sub { color:var(--muted); font-size:.83rem; font-family:var(--mono); margin-bottom:16px; }
  .row { display:grid; grid-template-columns:minmax(140px,190px) 1fr; gap:22px; align-items:start; }
  @media (max-width:760px) { .row { grid-template-columns:1fr; } }
  .frame { background:var(--mat); border-radius:6px; overflow:hidden; display:block; }
  .frame img { width:100%; display:block; cursor:zoom-in; }
  .before .tag { font-family:var(--mono); font-size:.7rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-bottom:6px; }
  .cands { display:grid; grid-template-columns:repeat(auto-fill,minmax(216px,1fr)); gap:16px; }
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
  #outbox { width:100%; max-width:1000px; margin:12px auto 0; display:none; }
  #outbox textarea { width:100%; height:220px; font-family:var(--mono); font-size:.74rem; padding:10px; border-radius:8px; border:1px solid var(--line); background:var(--panel); color:var(--fg); box-sizing:border-box; }
  .zoom { position:fixed; inset:0; background:#0b0b0c; display:none; align-items:center; justify-content:center; z-index:50; padding:16px; cursor:zoom-out; }
  .zoom img { max-width:100%; max-height:100%; }
</style>
<div class="wrap">
  <h1>Short instructions or long ones?</h1>
  <p class="lede">We send the image model a long, detailed instruction sheet. We also have a <strong>short</strong> version of it. Back in round 1 you picked the short version 8 times out of 10 &mdash; but that was before I removed the tan instruction and halved the muscle numbers, which were most of what the short version was leaving out. So the two may have converged, and I want your eyes rather than my guess.</p>
  <p class="lede">Every row below is the <strong>same person, same model, same settings</strong>. The only difference is long instructions vs short ones &mdash; hidden, and shuffled per row.</p>
  <ol class="steps">
    <li><strong>Pick the better one</strong> in each row (green).</li>
    <li>Mark the other <strong>Acceptable</strong> (blue) if you would ship it too.</li>
    <li>If they look <strong>the same to you, that is a real answer</strong> &mdash; mark both Acceptable and leave the note blank. Convergence is the outcome I am testing for.</li>
    <li><strong>Skin tone matters most on this one.</strong> The short version drops the "do not add a tan" rule, so use the <em>too tan</em> / <em>skin tone right</em> tags freely.</li>
    <li>Hit <strong>Copy labels</strong> and paste the text back.</li>
  </ol>
  <p class="warn">Tap any image to enlarge. Answers save in this browser as you go. Nothing ships unless you say the short version is at least as good.</p>
  ${bodyBlocks}
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
const KEY = 'absbyai-prompt-ab-round5';
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
console.log(`\ngallery.html: ${(fs.statSync(outFile).size / 1048576).toFixed(2)} MB, ${blocks.length} rows`);
console.log(fail ? `${fail} assertion(s) FAILED` : 'all gallery assertions passed');
process.exitCode = fail ? 1 : 0;
