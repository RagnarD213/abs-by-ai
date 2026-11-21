// Builds the BLIND round-2 labeling gallery: two candidates per case, lettered
// randomly per case so model identity is invisible. Writes gallery.html
// (self-contained, data-URI images) and key.json (letter -> model).
//
// Design is deliberately inherited from round 1: Dan has already labeled with
// this interface, and the desaturated chrome is load-bearing — the whole page is
// a body/skin-tone judgement, so the mat behind every image is the SAME neutral
// in light and dark and no tinted accent sits next to a photo.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { CASES } = require('./cases');

const OUT = path.join(__dirname, 'out');
const PHOTOS = path.join(__dirname, 'photos');
const TMP = path.join(__dirname, 'out', 'thumbs');
fs.mkdirSync(TMP, { recursive: true });

const THUMB_W = Number(process.env.THUMB_W || 460);
const THUMB_Q = Number(process.env.THUMB_Q || 68);

function thumbDataUri(srcPath, tag) {
  const dest = path.join(TMP, `${tag}.jpg`);
  if (!fs.existsSync(dest)) {
    execFileSync('sips', ['-s', 'format', 'jpeg', '--resampleWidth', String(THUMB_W),
      '-s', 'formatOptions', String(THUMB_Q), srcPath, '--out', dest], { stdio: 'ignore' });
  }
  return 'data:image/jpeg;base64,' + fs.readFileSync(dest).toString('base64');
}

// Deterministic per-case order (re-running keeps the same letters), but SEARCHED
// for a salt that puts each model in slot A on half the rows. The obvious
// hash-and-shuffle put Seedream in slot A on all six rows, which both leaks the
// model identity across rows and stacks every candidate against the same
// position bias. Balance is asserted below, not assumed.
function orderFor(cells, seedStr, salt) {
  let h = 2166136261 >>> 0;                       // FNV-1a
  for (const ch of (salt + seedStr)) {
    h ^= ch.charCodeAt(0);
    h = Math.imul(h, 16777619) >>> 0;
  }
  const a = cells.slice().sort((x, y) => x.modelKey.localeCompare(y.modelKey));
  return (h & 1) ? [a[1], a[0]] : a;
}

// Pick the smallest salt that balances slot A across the whole grid.
function findBalancedSalt(caseIds, cellsFor) {
  for (let s = 0; s < 500; s++) {
    const counts = {};
    let usable = 0;
    for (const id of caseIds) {
      const cells = cellsFor(id);
      if (cells.length !== 2) continue;
      usable++;
      const first = orderFor(cells, id, `s${s}`)[0].modelKey;
      counts[first] = (counts[first] || 0) + 1;
    }
    if (!usable) return `s${s}`;
    if (Object.values(counts).every((n) => Math.abs(n - usable / 2) <= 0.5)) return `s${s}`;
  }
  throw new Error('no balanced salt found');
}

const results = JSON.parse(fs.readFileSync(path.join(OUT, 'results.json'), 'utf8'));
const LETTERS = 'AB'.split('');

const key = {};
const caseBlocks = [];

const cellsFor = (id) => results.filter((r) => r.caseId === id && r.ok);
// Excluded cases keep their generated images on disk but never reach the gallery.
const SHOWN = CASES.filter((c) => !c.excluded);

// Letters already published MUST NOT move. Dan's labels live in localStorage
// keyed by `case:letter`, so reshuffling a row he has already answered would
// silently re-point his verdict at the other model. Existing rows keep their
// assignment; only genuinely new rows get a letter, chosen to keep the overall
// slot-A split as even as the already-fixed rows allow.
const keyPath = path.join(OUT, 'key.json');
const priorKey = fs.existsSync(keyPath) ? JSON.parse(fs.readFileSync(keyPath, 'utf8')) : {};
const pinnedFirst = (id) => priorKey[`${id}:A`]?.model || null;

const newIds = SHOWN.filter((c) => cellsFor(c.id).length === 2 && !pinnedFirst(c.id)).map((c) => c.id);
const slotA = {};
for (const c of SHOWN) {
  const m = pinnedFirst(c.id);
  if (m) slotA[m] = (slotA[m] || 0) + 1;
}
const SALT = findBalancedSalt(newIds, cellsFor);

for (const c of SHOWN) {
  const cells = cellsFor(c.id);
  if (!cells.length) continue;
  const pinned = pinnedFirst(c.id);
  const ordered = pinned
    ? [...cells].sort((x, y) => (x.modelKey === pinned ? -1 : y.modelKey === pinned ? 1 : 0))
    : orderFor(cells, c.id, SALT);
  const cands = ordered.map((cell, i) => {
    const letter = LETTERS[i];
    key[`${c.id}:${letter}`] = { model: cell.modelKey, label: cell.label, variant: cell.variant, latencyMs: cell.latencyMs };
    return {
      letter,
      img: thumbDataUri(path.join(OUT, cell.image), `${c.id}__${cell.modelKey}__${cell.variant}`),
    };
  });
  const failures = results.filter((r) => r.caseId === c.id && !r.ok);
  caseBlocks.push({
    id: c.id,
    title: c.desc,
    sub: `Intensity: ${c.intensityLabel} (${c.intensity}) - woman - declared start: ${c.condition}`,
    before: thumbDataUri(path.join(PHOTOS, c.file), `before__${c.photoKey}`),
    cands,
    failCount: failures.length,
  });
}

fs.writeFileSync(path.join(OUT, 'key.json'), JSON.stringify(key, null, 2));

const TAGS = ['not enough change', 'too much / unrealistic', 'looks fake', 'face drifted',
  'too muscular / masculine', 'body shape wrong', 'skin tone right', 'just right'];

const html = `<title>Abs By AI - female model test (blind)</title>
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
  @media (prefers-reduced-motion: reduce) { * { scroll-behavior:auto !important; } }
</style>
<div class="wrap">
  <h1>Female model test - round 2, four different women</h1>
  <p class="lede">Same question as last time, on <strong>four different women</strong> instead of one - different builds, skin tones and lighting, which is the coverage the first round was missing. Each row shows one woman transformed by <strong>two different models</strong>. Names are hidden and the letters are shuffled per row, so A in one row is not the same model as A in the next. <strong>Rows you have already answered keep their answers and their letters</strong> - only the two new lean rows at the bottom need labelling.</p>
  <ol class="steps">
    <li><strong>Pick the one you would rather show a paying customer</strong> (green button).</li>
    <li>Mark the other <strong>Acceptable</strong> (blue) if you would also be happy shipping it.</li>
    <li>If <strong>neither</strong> is good enough, pick nothing and say why in the note - that is a real answer.</li>
    <li>Tap the quick tags or type a few words to say <strong>why</strong>.</li>
    <li>Hit <strong>Copy labels</strong> at the bottom and paste the text back to Claude.</li>
  </ol>
  <p class="warn">Tap any image to enlarge. Answers save in this browser as you go, so you can label some rows now and the rest later - including rows added after you started.</p>
  ${caseBlocks.map((b) => `
  <section class="case" data-case="${b.id}">
    <h2>${b.title}</h2>
    <div class="sub">${b.sub}${b.failCount ? ` - ${b.failCount} model(s) returned nothing` : ''}</div>
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
          <div class="chips">
            ${TAGS.map((t) => `<span class="chip" role="button" tabindex="0">${t}</span>`).join('')}
          </div>
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
const KEY = 'absbyai-bakeoff-round3-female';
const state = JSON.parse(localStorage.getItem(KEY) || '{}');
function cellKey(c, l) { return c + ':' + l; }
function get(c, l) { return state[cellKey(c, l)] || (state[cellKey(c, l)] = { best: false, acceptable: false, tags: [], note: '' }); }
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
    const toggle = () => {
      const s = get(c, l), t = ch.textContent;
      s.tags = s.tags.includes(t) ? s.tags.filter(x => x !== t) : s.tags.concat(t);
      save();
    };
    ch.onclick = toggle;
    ch.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); } };
  });
  el.querySelector('.note').oninput = (e) => { get(c, l).note = e.target.value; localStorage.setItem(KEY, JSON.stringify(state)); };
  el.querySelector('img').onclick = () => {
    const z = document.getElementById('zoom');
    z.querySelector('img').src = el.querySelector('img').src;
    z.style.display = 'flex';
  };
});
document.querySelectorAll('.before img').forEach(img => {
  img.onclick = () => {
    const z = document.getElementById('zoom');
    z.querySelector('img').src = img.src;
    z.style.display = 'flex';
  };
});
document.getElementById('zoom').onclick = (e) => { e.currentTarget.style.display = 'none'; };
document.getElementById('reset').onclick = () => { if (confirm('Clear every label?')) { localStorage.removeItem(KEY); location.reload(); } };
document.getElementById('copy').onclick = async () => {
  const out = {};
  for (const [k, v] of Object.entries(state)) {
    if (v.best || v.acceptable || v.tags.length || v.note) out[k] = v;
  }
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
const NON_ASCII = new RegExp('[^\\x00-\\x7F]', 'g');
const safeHtml = html.slice(0, cut).replace(NON_ASCII, (ch) => `&#${ch.charCodeAt(0)};`) + html.slice(cut);

const outFile = path.join(OUT, 'gallery.html');
fs.writeFileSync(outFile, safeHtml);
console.log(`gallery.html: ${(fs.statSync(outFile).size / 1048576).toFixed(2)} MB, ${caseBlocks.length} cases, ${Object.keys(key).length} candidates`);
