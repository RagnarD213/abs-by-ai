// Builds the BLIND labeling gallery: every candidate for every case, lettered
// randomly per case so model identity is invisible. Writes gallery.html (self
// contained, data-URI images) and key.json (letter → model, revealed after labels).
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { CASES } = require('./cases');
const { MODELS } = require('./adapters');

const OUT = path.join(__dirname, 'out', 'round1');
const PHOTOS = path.join(__dirname, 'photos');
const TMP = path.join(__dirname, 'out', 'thumbs');
fs.mkdirSync(TMP, { recursive: true });

const THUMB_W = Number(process.env.THUMB_W || 460);
const THUMB_Q = Number(process.env.THUMB_Q || 65);
// Split across two pages so neither artifact is a multi-megabyte download.
const PART = Number(process.env.PART || 0); // 0 = single page, 1 or 2 = half

function thumbDataUri(srcPath, tag) {
  const dest = path.join(TMP, `${tag}.jpg`);
  if (!fs.existsSync(dest)) {
    execFileSync('sips', ['-s', 'format', 'jpeg', '--resampleWidth', String(THUMB_W),
      '-s', 'formatOptions', String(THUMB_Q), srcPath, '--out', dest], { stdio: 'ignore' });
  }
  return 'data:image/jpeg;base64,' + fs.readFileSync(dest).toString('base64');
}

// Deterministic shuffle so re-running the build keeps the same letters.
function shuffle(arr, seedStr) {
  let seed = 0;
  for (const ch of seedStr) seed = (seed * 31 + ch.charCodeAt(0)) >>> 0;
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    seed = (seed * 1103515245 + 12345) >>> 0;
    const j = seed % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const results = JSON.parse(fs.readFileSync(path.join(OUT, 'results.json'), 'utf8'));
const LETTERS = 'ABCDEFGHIJKL'.split('');

const key = {};
const caseBlocks = [];

const half = Math.ceil(CASES.length / 2);
const selected = PART === 1 ? CASES.slice(0, half) : PART === 2 ? CASES.slice(half) : CASES;

for (const c of selected) {
  const cells = results.filter((r) => r.caseId === c.id && r.ok);
  if (!cells.length) continue;
  const ordered = shuffle(cells, c.id);
  const cands = ordered.map((cell, i) => {
    const letter = LETTERS[i];
    key[`${c.id}:${letter}`] = { model: cell.modelKey, label: cell.label, variant: cell.variant, latencyMs: cell.latencyMs };
    return {
      letter,
      img: thumbDataUri(path.join(OUT, cell.image), `${c.id}__${cell.modelKey}__${cell.variant}`),
    };
  });
  const failures = results.filter((r) => r.caseId === c.id && !r.ok)
    .map((r) => `${r.blocked ? 'BLOCKED' : 'failed'} (${r.variant})`);
  caseBlocks.push({
    id: c.id,
    title: `${c.desc}`,
    sub: `Intensity: ${c.intensityLabel} · ${c.gender} · start: ${c.condition}`,
    before: thumbDataUri(path.join(PHOTOS, c.file), `before__${c.photoKey}`),
    cands,
    failCount: failures.length,
  });
}

const keyPath = path.join(OUT, 'key.json');
const merged = fs.existsSync(keyPath) ? { ...JSON.parse(fs.readFileSync(keyPath, 'utf8')), ...key } : key;
fs.writeFileSync(keyPath, JSON.stringify(merged, null, 2));

const partSuffix = PART ? ` (part ${PART} of 2)` : '';
const html = `<title>Abs By AI — Round 1 blind model bake-off${partSuffix}</title>
<style>
  /* The whole page is a skin-tone judgement, so the chrome is deliberately
     desaturated: no warm paper, no tinted accents near the photos, and the mat
     behind every image is the SAME neutral in light and dark so a candidate's
     skin never reads differently just because the theme flipped. */
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
  .wrap { max-width:1180px; margin:0 auto; padding:32px 16px 0; }
  h1 { font-size:1.55rem; line-height:1.2; margin:0 0 10px; letter-spacing:-.015em; text-wrap:balance; }
  .lede { color:var(--muted); max-width:66ch; margin:0 0 22px; }
  .lede strong { color:var(--fg); }
  .steps { background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px 20px 14px 34px; margin:0 0 8px; }
  .steps li { margin:5px 0; }
  .warn { color:var(--muted); font-size:.85rem; margin:10px 0 26px; }

  .case { border-top:1px solid var(--line); padding:26px 0; }
  .case h2 { font-size:1.08rem; margin:0 0 3px; letter-spacing:-.01em; }
  .case .sub { color:var(--muted); font-size:.83rem; font-family:var(--mono); margin-bottom:16px; }
  .row { display:grid; grid-template-columns:minmax(140px,190px) 1fr; gap:22px; align-items:start; }
  @media (max-width:760px) { .row { grid-template-columns:1fr; } }

  .frame { background:var(--mat); border-radius:6px; overflow:hidden; display:block; }
  .frame img { width:100%; display:block; }
  .before .tag { font-family:var(--mono); font-size:.7rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-bottom:6px; }

  .cands { display:grid; grid-template-columns:repeat(auto-fill,minmax(196px,1fr)); gap:16px; }
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
  #outbox { width:100%; max-width:1180px; margin:12px auto 0; display:none; }
  #outbox textarea { width:100%; height:220px; font-family:var(--mono); font-size:.74rem; padding:10px; border-radius:8px; border:1px solid var(--line); background:var(--panel); color:var(--fg); box-sizing:border-box; }
  .zoom { position:fixed; inset:0; background:#0b0b0c; display:none; align-items:center; justify-content:center; z-index:50; padding:16px; cursor:zoom-out; }
  .zoom img { max-width:100%; max-height:100%; }
</style>
<div class="wrap">
  <h1>Round 1 — blind model bake-off${partSuffix}</h1>
  <p class="lede">${PART ? `<strong>This is page ${PART} of 2 — label this page, then do the other one. Your answers are saved together, so “Copy labels” on the second page gives you everything at once.</strong><br>` : ''}Six image models generated a transformation for each case below. Model names are hidden — the letters are shuffled per case, so A in one row is not the same model as A in the next. Your picks become the ground-truth data the judge gets rebuilt against.</p>
  <ol class="steps">
    <li><strong>Pick the best</strong> image in each row (green button).</li>
    <li>Optionally mark any other image <strong>Acceptable</strong> (blue) — one you'd be happy shipping.</li>
    <li>Tap the quick tags or type a few words on any image to say <strong>why</strong> — especially on ones you reject.</li>
    <li>When done, hit <strong>Copy labels</strong> at the bottom and paste the text back to Claude.</li>
  </ol>
  <p class="warn">Tap any image to enlarge. Your answers save in this browser as you go.</p>
  ${caseBlocks.map((b) => `
  <section class="case" data-case="${b.id}">
    <h2>${b.title}</h2>
    <div class="sub">${b.sub}${b.failCount ? ` · ${b.failCount} model(s) returned nothing for this case` : ''}</div>
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
          <div class="chips">
            ${['skin tone right', 'too tan', 'too muscular', 'not enough change', 'face drifted', 'looks fake', 'framing off', 'just right'].map((t) => `<span class="chip">${t}</span>`).join('')}
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
const KEY = 'absbyai-bakeoff-round1';
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
  const done = cases.filter(sec => [...sec.querySelectorAll('.cand')].some(el => get(el.dataset.c, el.dataset.l).best)).length;
  document.getElementById('prog').textContent = done + ' of ' + cases.length + ' cases labeled';
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
  el.querySelectorAll('.chip').forEach(ch => ch.onclick = () => {
    const s = get(c, l), t = ch.textContent;
    s.tags = s.tags.includes(t) ? s.tags.filter(x => x !== t) : s.tags.concat(t);
    save();
  });
  el.querySelector('.note').oninput = (e) => { get(c, l).note = e.target.value; localStorage.setItem(KEY, JSON.stringify(state)); };
  el.querySelector('img').onclick = () => {
    const z = document.getElementById('zoom');
    z.querySelector('img').src = el.querySelector('img').src;
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
  try { await navigator.clipboard.writeText(text); document.getElementById('copy').textContent = 'Copied \\u2014 paste to Claude'; }
  catch (e) { document.getElementById('copy').textContent = 'Select the text below and copy'; }
  box.scrollIntoView({ behavior: 'smooth' });
};
render();
</script>`;

// Typographic characters go out as numeric entities so the page renders correctly
// regardless of the charset the host page declares. The <script> block is left
// alone — entities don't decode inside it (its one em dash is a \u escape).
const cut = html.indexOf('<script>');
const NON_ASCII = new RegExp('[^\\x00-\\x7F]', 'g');
const safeHtml = html.slice(0, cut).replace(NON_ASCII, (ch) => `&#${ch.charCodeAt(0)};`) + html.slice(cut);

const outFile = path.join(OUT, PART ? `gallery-part${PART}.html` : 'gallery.html');
fs.writeFileSync(outFile, safeHtml);
const bytes = fs.statSync(outFile).size;
console.log(`gallery.html written: ${(bytes / 1048576).toFixed(2)} MB, ${caseBlocks.length} cases, ${Object.keys(key).length} candidates`);
