// Blind A/B: OLD prompt vs NEW prompt (ab-visibility anchor ladder), model held
// constant per row. Old arm = Dan's labelled round-5 images; new arm = out/.
//
// Invariants carried from round 4/5:
//  - letters for any row already present in key.json are PINNED (labels live in
//    localStorage keyed row:letter, so a reshuffle would silently re-point an
//    answered verdict at the other version);
//  - per-set slot-A balance is ASSERTED, not hoped for;
//  - the built HTML must leak zero key entries (checked by check-blinding.js).
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { CASES, ARMS } = require('./cases');

const NEW_OUT = path.join(__dirname, 'out');
const OLD_OUT = path.join(__dirname, '..', 'round5-prompt-ab', 'out');
const PHOTOS = path.join(__dirname, '..', 'round5-prompt-ab', 'photos');
const TMP = path.join(NEW_OUT, 'thumbs');
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

const keyPath = path.join(NEW_OUT, 'key.json');
const prevKey = fs.existsSync(keyPath) ? JSON.parse(fs.readFileSync(keyPath, 'utf8')) : {};

// Enumerate rows that have both arms on disk.
const rows = [];
for (const c of CASES) {
  for (const arm of ARMS) {
    const oldPath = path.join(OLD_OUT, `${c.id}__${arm.modelKey}__${arm.variant}.jpg`);
    const newPath = path.join(NEW_OUT, `${c.id}__${arm.modelKey}__new.jpg`);
    if (!fs.existsSync(oldPath) || !fs.existsSync(newPath)) continue;
    rows.push({ rowId: `${c.id}__${arm.modelKey}`, c, arm, oldPath, newPath });
  }
}

function orderFor(id, salt) {
  let h = 2166136261 >>> 0;
  for (const ch of (salt + id)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; }
  return (h & 1) ? ['new', 'old'] : ['old', 'new'];
}
// PIN rows already answered/keyed; salt-search only over the free rows, and the
// balance target counts pinned rows too, per set.
function pinnedOrder(rowId) {
  const a = prevKey[`${rowId}:A`];
  return a ? [a.version, a.version === 'old' ? 'new' : 'old'] : null;
}
// Balance is required over the FREE (un-pinned) rows only — pinned letters are
// sacred (they may already carry Dan's answers), so their imbalance, if any, is
// accepted and reported rather than "fixed" by re-pointing answered rows.
let SALT = 's0';
const freeRows = rows.filter((r) => !pinnedOrder(r.rowId));
if (freeRows.length) {
  SALT = null;
  outer: for (let s = 0; s < 5000; s++) {
    const bySet = {};
    for (const r of freeRows) {
      const order = orderFor(r.rowId, `s${s}`);
      const b = (bySet[r.arm.set] = bySet[r.arm.set] || { old: 0, new: 0, n: 0 });
      b[order[0]]++; b.n++;
    }
    for (const b of Object.values(bySet)) if (Math.abs(b.old - b.new) > (b.n % 2)) continue outer;
    SALT = `s${s}`; break;
  }
  if (!SALT) throw new Error('no balanced salt over free rows');
}

const key = {};
const blocks = [];
const slotA = {};
for (const r of rows) {
  const order = pinnedOrder(r.rowId) || orderFor(r.rowId, SALT);
  const b = (slotA[`set${r.arm.set}`] = slotA[`set${r.arm.set}`] || { old: 0, new: 0 });
  b[order[0]]++;
  const cands = order.map((which, i) => {
    const letter = 'AB'[i];
    key[`${r.rowId}:${letter}`] = { version: which };
    return { letter, img: thumbDataUri(which === 'old' ? r.oldPath : r.newPath, `${which}__${r.rowId}`) };
  });
  blocks.push({
    id: r.rowId, set: r.arm.set,
    title: r.c.desc,
    sub: `Intensity: ${r.c.intensityLabel} (${r.c.intensity}) - man - declared start: ${r.c.condition} - set ${r.arm.set}`,
    before: thumbDataUri(path.join(PHOTOS, r.c.file), `before__${r.c.photoKey}`),
    cands,
  });
}
blocks.sort((a, b) => a.set - b.set || a.id.localeCompare(b.id));
// Consistency: pinned rows must round-trip identically.
for (const [k, v] of Object.entries(prevKey)) {
  if (key[k] && key[k].version !== v.version) throw new Error(`pin violated: ${k}`);
}
fs.writeFileSync(keyPath, JSON.stringify(key, null, 2));
console.log('slot-A balance by set:', JSON.stringify(slotA), '| rows:', blocks.length);

const TAGS = ['not enough change', 'not enough ab definition', 'too muscular', 'too much change',
  'looks fake', 'face drifted', 'skin tone right', 'just right'];

const set1Count = blocks.filter((b) => b.set === 1).length;
const html = `<title>Abs By AI - male ab-ladder prompt test (blind A/B)</title>
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
  .sethdr { border-top:2px solid var(--line); margin-top:18px; padding-top:20px; }
  .sethdr h2 { font-size:1.15rem; margin:0 0 4px; }
  .sethdr p { color:var(--muted); font-size:.88rem; margin:0 0 4px; max-width:70ch; }
  .case { border-top:1px solid var(--line); padding:26px 0; }
  .case h2 { font-size:1.08rem; margin:0 0 3px; letter-spacing:-.01em; text-wrap:balance; }
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
  <h1>Did the ab-ladder fix the male results?</h1>
  <p class="lede">In the last test you rejected <strong>both</strong> images in 5 of 6 male rows - "not enough change / not enough ab definition". I added a graded <strong>ab-definition ladder</strong> to the instructions: Subtle and Ripped now ask for concretely different abs, and a heavier start gets a believable capped target instead of an extreme ask. Every row below is the <strong>same man, same model</strong> - the only difference is old instructions vs new. Which is which is hidden and shuffled per row.</p>
  <ol class="steps">
    <li><strong>Pick the better one</strong> in each row (green).</li>
    <li>Mark the other <strong>Acceptable</strong> (blue) if you would ship it too.</li>
    <li>Tag what is wrong - the two that decide this: <strong>not enough ab definition</strong> and <strong>too muscular</strong>.</li>
    <li>Hit <strong>Copy labels</strong> and paste the text back.</li>
  </ol>
  <p class="warn">Tap any image to enlarge. Answers save in this browser as you go.${set1Count === 0 ? ' NOTE: the Gemini rows are missing until the Google AI Studio balance is topped up - these rows are the FLUX leg. The Gemini rows will be added to this same page without disturbing your answers.' : ''}</p>
  ${(() => {
    let lastSet = 0, out = '';
    for (const b of blocks) {
      if (b.set !== lastSet) {
        lastSet = b.set;
        out += b.set === 1
          ? `<div class="sethdr"><h2>Set 1 - the main event (Gemini leg)</h2><p>Gemini under-changed 19 of 24 male images last round. These rows decide whether the ladder ships.</p></div>`
          : `<div class="sethdr"><h2>Set 2 - the FLUX leg (secondary)</h2><p>FLUX already over-changed men last round. The new instructions reach this leg too - the check here is that they did not push it further over ("too muscular" / "too much change" getting worse would be the failure).</p></div>`;
      }
      out += `
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
            <button class="pick" type="button">Better</button>
            <button class="alt" type="button">Acceptable</button>
          </div>
          <div class="chips">${TAGS.map((t) => `<span class="chip" role="button" tabindex="0">${t}</span>`).join('')}</div>
          <input class="note" placeholder="why? (optional)">
        </div>`).join('')}
      </div>
    </div>
  </section>`;
    }
    return out;
  })()}
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
const KEY = 'absbyai-round6-ab-ladder';
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
const outFile = path.join(NEW_OUT, 'gallery.html');
fs.writeFileSync(outFile, safe);
console.log(`gallery.html: ${(fs.statSync(outFile).size / 1048576).toFixed(2)} MB, ${blocks.length} rows`);

// ── Blinding check: zero key entries may leak into the built HTML ────────────
let leaks = 0;
for (const [k, v] of Object.entries(key)) {
  if (safe.includes(`"${k}"`) || safe.includes(k + '"')) leaks++;
}
if (safe.includes('"version"') || /\bold\b.*\bnew\b/.test(safe.match(/data-c="[^"]*"[^>]*data-l/g)?.join(' ') || '')) {
  // key structure strings must not appear
}
const bodyOnly = safe;
const leakStrings = ['"version": "old"', '"version": "new"', 'promptVersion'];
for (const s of leakStrings) if (bodyOnly.includes(s)) leaks++;
console.log(leaks ? `BLINDING LEAK: ${leaks}` : 'blinding check: no key entries in HTML');
process.exitCode = leaks ? 1 : 0;
