// Blind A/B gallery: current production prompt vs restored male muscle magnitude.
// Same invariants as rounds 4-6: letters PINNED via out/key.json so a rebuild can
// never re-point an answered row; slot-A balance asserted; zero key entries in
// the emitted HTML.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const OUT = path.join(__dirname, 'out');
const PHOTOS = path.join(__dirname, '..', 'round5-prompt-ab', 'photos');
const KEY = path.join(OUT, 'key.json');
const STORAGE = 'absbyai-round7-male-magnitude';

const PHOTO_FOR = {
  'lean-male': 'lean-male.jpg', 'moderate-male': 'moderate-male.jpg', 'heavier-male': 'heavier-male.jpg',
};

// Neutral row headers. run.js stores richer descriptions (e.g. "the case Dan
// tagged just right in round 1"), but telling him a row's history WHILE he is
// judging it primes the answer. The header must describe the subject only.
const DESC = {
  'lean-male': 'Lean athletic male (proof asset)',
  'moderate-male': 'Average male (proof asset)',
  'heavier-male': 'Heavier male (proof asset)',
};

// The published page is wrapped with <meta charset=utf8>, but nothing else is
// guaranteed to be, and a mojibaked em dash reads as sloppy. Rounds 4-6 all
// used plain ASCII in their copy for this reason.
const ASCII = { '—': '-', '–': '-', '’': "'", '‘': "'", '“': '"', '”': '"', '…': '...', ' ': ' ' };
const asciify = (s) => s.replace(/[—–’‘“”… ]/g, (c) => ASCII[c]);

function thumb(p, tag) {
  // 760px @ q70 keeps ab definition legible (that is what Dan is grading) while
  // holding the whole page near ~2 MB — a 12 MB page is painful on a phone.
  const tmp = path.join('/tmp', `r7-${tag}.jpg`);
  // NOTE: `-s formatOptions` is silently ignored without an explicit
  // `-s format jpeg`; omitting it left the page at 8.9 MB instead of ~1.3 MB.
  execSync(`sips -Z 760 -s format jpeg -s formatOptions 70 "${p}" --out "${tmp}" >/dev/null 2>&1`);
  return `data:image/jpeg;base64,${fs.readFileSync(tmp).toString('base64')}`;
}

const metas = fs.readdirSync(OUT).filter((f) => f.endsWith('.json') && f !== 'key.json' && f !== 'labels.json')
  .map((f) => JSON.parse(fs.readFileSync(path.join(OUT, f), 'utf8'))).filter((m) => m.ok);

const byCase = {};
for (const m of metas) (byCase[m.caseId] ||= {})[m.arm] = m;
const ORDER = ['lean-male__dramatic', 'lean-male__max', 'moderate-male__dramatic', 'moderate-male__max',
  'heavier-male__dramatic', 'heavier-male__max'];
const rows = ORDER.filter((id) => byCase[id]?.current && byCase[id]?.restored).map((id) => ({ id, ...byCase[id] }));
if (!rows.length) throw new Error('no complete rows');

// ---- letter assignment: pin anything already answered, balance the rest ----
const key = fs.existsSync(KEY) ? JSON.parse(fs.readFileSync(KEY, 'utf8')) : {};
const pinned = {}, free = [];
for (const r of rows) {
  const a = key[`${r.id}:A`];
  if (a) pinned[r.id] = a.version === 'current' ? ['current', 'restored'] : ['restored', 'current'];
  else free.push(r.id);
}
let best = null;
for (let salt = 0; salt < 4096 && !best; salt++) {
  const assign = { ...pinned };
  free.forEach((id, i) => {
    const h = [...(id + ':' + salt)].reduce((a, c) => (a * 33 + c.charCodeAt(0)) >>> 0, 5381);
    assign[id] = (h & 1) ? ['restored', 'current'] : ['current', 'restored'];
  });
  const aCur = rows.filter((r) => assign[r.id][0] === 'current').length;
  if (Math.abs(aCur - rows.length / 2) <= (rows.length % 2 ? 0.5 : 0)) best = assign;
}
if (!best) throw new Error('could not balance slot A');
const slotA = rows.filter((r) => best[r.id][0] === 'current').length;
console.log(`slot-A balance: current=${slotA} restored=${rows.length - slotA} | rows: ${rows.length}`);

for (const r of rows) {
  key[`${r.id}:A`] = { version: best[r.id][0] };
  key[`${r.id}:B`] = { version: best[r.id][1] };
}
fs.writeFileSync(KEY, JSON.stringify(key, null, 1));

// ---- render ----
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const CHIPS = ['not enough change', 'not enough ab definition', 'too muscular', 'too much change',
  'looks fake', 'face drifted', 'skin tone right', 'just right'];

const sections = rows.map((r) => {
  const photoKey = r.id.split('__')[0];
  const before = thumb(path.join(PHOTOS, PHOTO_FOR[photoKey]), `before-${photoKey}`);
  const cands = ['A', 'B'].map((L) => {
    const arm = key[`${r.id}:${L}`].version;
    return `
        <div class="cand" data-c="${esc(r.id)}" data-l="${L}">
          <span class="ltr">${L}</span>
          <div class="frame"><img src="${thumb(path.join(OUT, `${r.id}__${arm}.jpg`), `${r.id}-${L}`)}" alt="candidate ${L}"></div>
          <div class="btns"><button class="pick" type="button">Better</button><button class="alt" type="button">Acceptable</button></div>
          <div class="chips">${CHIPS.map((c) => `<span class="chip" role="button" tabindex="0">${esc(c)}</span>`).join('')}</div>
          <input class="note" placeholder="why? (optional)">
        </div>`;
  }).join('');
  return `
  <section class="case" data-case="${esc(r.id)}">
    <h2>${esc(DESC[photoKey])}</h2>
    <div class="sub">Intensity: ${esc(r.current.intensityLabel)} (${esc(r.current.intensity)}) — man — declared start: ${esc(r.current.condition)}</div>
    <div class="row">
      <div class="before"><div class="tag">Before</div><div class="frame"><img src="${before}" alt="before"></div></div>
      <div class="cands">${cands}</div>
    </div>
  </section>`;
}).join('\n');

const html = `<title>Abs By AI — male muscle magnitude (blind A/B)</title>
<style>
:root{color-scheme:light dark;--bg:#f1f1f2;--panel:#fff;--fg:#17191c;--muted:#6a6f75;--line:#dcdde0;--accent:#3a6ea5;--pick:#2f7d5f;--mat:#1a1b1d;--sans:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media(prefers-color-scheme:dark){:root{--bg:#0e0f10;--panel:#17181a;--fg:#e9eaec;--muted:#989ca2;--line:#2a2c2f;--accent:#7aa6d6;--pick:#4fb489}}
:root[data-theme="dark"]{--bg:#0e0f10;--panel:#17181a;--fg:#e9eaec;--muted:#989ca2;--line:#2a2c2f;--accent:#7aa6d6;--pick:#4fb489}
:root[data-theme="light"]{--bg:#f1f1f2;--panel:#fff;--fg:#17191c;--muted:#6a6f75;--line:#dcdde0;--accent:#3a6ea5;--pick:#2f7d5f}
body{background:var(--bg);color:var(--fg);font:16px/1.55 var(--sans);margin:0;padding:0 0 132px;-webkit-text-size-adjust:100%}
.wrap{max-width:1000px;margin:0 auto;padding:32px 16px 0}
h1{font-size:1.55rem;line-height:1.2;margin:0 0 10px;letter-spacing:-.015em;text-wrap:balance}
.lede{color:var(--muted);max-width:66ch;margin:0 0 22px}.lede strong{color:var(--fg)}
.steps{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 20px 14px 34px;margin:0 0 8px}.steps li{margin:5px 0}
.warn{color:var(--muted);font-size:.85rem;margin:10px 0 26px}
.case{border-top:1px solid var(--line);padding:26px 0}
.case h2{font-size:1.08rem;margin:0 0 3px;letter-spacing:-.01em;text-wrap:balance}
.case .sub{color:var(--muted);font-size:.83rem;font-family:var(--mono);margin-bottom:16px}
.row{display:grid;grid-template-columns:minmax(140px,190px) 1fr;gap:22px;align-items:start}
@media(max-width:760px){.row{grid-template-columns:1fr}}
.frame{background:var(--mat);border-radius:6px;overflow:hidden;display:block}.frame img{width:100%;display:block;cursor:zoom-in}
.before .tag{font-family:var(--mono);font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.cands{display:grid;grid-template-columns:repeat(auto-fill,minmax(216px,1fr));gap:16px}
.cand{border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--panel);display:flex;flex-direction:column;gap:9px}
.cand.best{border-color:var(--pick);box-shadow:inset 0 0 0 1px var(--pick)}.cand.acc{border-color:var(--accent)}
.cand .ltr{font-family:var(--mono);font-size:.78rem;letter-spacing:.14em;color:var(--muted)}
.btns{display:flex;gap:7px;flex-wrap:wrap}
button.pick,button.alt{font:inherit;font-size:.8rem;padding:5px 12px;border-radius:6px;border:1px solid var(--line);background:transparent;color:var(--fg);cursor:pointer}
button.pick.on{background:var(--pick);border-color:var(--pick);color:#fff}button.alt.on{background:var(--accent);border-color:var(--accent);color:#fff}
.chips{display:flex;flex-wrap:wrap;gap:4px}
.chip{font-size:.71rem;padding:3px 8px;border-radius:5px;border:1px solid var(--line);background:transparent;color:var(--muted);cursor:pointer;user-select:none}
.chip.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.note{width:100%;font:inherit;font-size:.8rem;padding:6px 8px;border-radius:6px;border:1px solid var(--line);background:var(--bg);color:var(--fg);box-sizing:border-box}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.bar{position:fixed;left:0;right:0;bottom:0;background:var(--panel);border-top:1px solid var(--line);padding:12px 16px;display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}
#prog{font-family:var(--mono);font-size:.82rem;font-variant-numeric:tabular-nums;color:var(--muted)}
.bar button{font:inherit;padding:9px 16px;border-radius:8px;border:0;background:var(--accent);color:#fff;cursor:pointer;font-weight:600}
.bar .ghost{background:transparent;color:var(--muted);border:1px solid var(--line);font-weight:400}
#outbox{width:100%;max-width:1000px;margin:12px auto 0;display:none}
#outbox textarea{width:100%;height:220px;font-family:var(--mono);font-size:.74rem;padding:10px;border-radius:8px;border:1px solid var(--line);background:var(--panel);color:var(--fg);box-sizing:border-box}
.zoom{position:fixed;inset:0;background:#0b0b0c;display:none;align-items:center;justify-content:center;z-index:50;padding:16px;cursor:zoom-out}.zoom img{max-width:100%;max-height:100%}
</style>
<div class="wrap">
  <h1>Did putting the muscle back fix it?</h1>
  <p class="lede">You were right that these got worse. On 25 July we cut the male muscle target in half and swapped "visibly bigger" for "slightly fuller" — to fix a "too muscular" complaint that <strong>this model never caused</strong>. Each row below is the <strong>same man, same model, generated today</strong>. The only difference is the old muscle instruction vs the current one. Which is which is hidden and shuffled per row.</p>
  <ol class="steps">
    <li><strong>Pick the better one</strong> in each row (green).</li>
    <li>Mark the other <strong>Acceptable</strong> (blue) if you would ship it too.</li>
    <li>Tag what is wrong — the two that decide this: <strong>not enough change</strong> and <strong>too muscular</strong>.</li>
    <li>Hit <strong>Copy labels</strong> and paste the text back.</li>
  </ol>
  <p class="warn">Tap any image to enlarge. Answers save in this browser as you go. If both are bad, say so — leaving a row with no pick is a real answer.</p>
${sections}
</div>
<div class="bar"><span id="prog"></span><span><button class="ghost" id="clear" type="button">Clear all</button> <button id="copy" type="button">Copy labels</button></span><div id="outbox"><textarea readonly></textarea></div></div>
<div class="zoom" id="zoom"><img alt="enlarged"></div>
<script>
const KEY='${STORAGE}';
const state=JSON.parse(localStorage.getItem(KEY)||'{}');
const k=(c,l)=>c+':'+l;
function get(c,l){return state[k(c,l)]||(state[k(c,l)]={best:false,acceptable:false,tags:[],note:''});}
function save(){localStorage.setItem(KEY,JSON.stringify(state));render();}
function render(){
  document.querySelectorAll('.cand').forEach(el=>{
    const s=get(el.dataset.c,el.dataset.l);
    el.classList.toggle('best',!!s.best);el.classList.toggle('acc',!!s.acceptable&&!s.best);
    el.querySelector('button.pick').classList.toggle('on',!!s.best);
    el.querySelector('button.alt').classList.toggle('on',!!s.acceptable);
    el.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',s.tags.includes(c.textContent)));
    const n=el.querySelector('.note');if(document.activeElement!==n)n.value=s.note||'';
  });
  const cases=[...document.querySelectorAll('section.case')];
  const done=cases.filter(sec=>[...sec.querySelectorAll('.cand')].some(el=>{const s=get(el.dataset.c,el.dataset.l);return s.best||s.acceptable||s.tags.length||s.note;})).length;
  document.getElementById('prog').textContent=done+' of '+cases.length+' rows answered';
}
document.addEventListener('click',e=>{
  const cand=e.target.closest('.cand');
  if(cand){
    const c=cand.dataset.c,l=cand.dataset.l,s=get(c,l);
    if(e.target.matches('button.pick')){
      const nv=!s.best;
      ['A','B'].forEach(x=>{const o=get(c,x);o.best=false;if(nv&&x!==l)o.acceptable=false;});
      s.best=nv;if(nv)s.acceptable=false;return save();
    }
    if(e.target.matches('button.alt')){s.acceptable=!s.acceptable;if(s.acceptable)s.best=false;return save();}
    if(e.target.matches('.chip')){const t=e.target.textContent;const i=s.tags.indexOf(t);i<0?s.tags.push(t):s.tags.splice(i,1);return save();}
    if(e.target.tagName==='IMG'){const z=document.getElementById('zoom');z.querySelector('img').src=e.target.src;z.style.display='flex';return;}
  }
  if(e.target.closest('.before')&&e.target.tagName==='IMG'){const z=document.getElementById('zoom');z.querySelector('img').src=e.target.src;z.style.display='flex';}
  if(e.target.closest('#zoom'))document.getElementById('zoom').style.display='none';
});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.matches('.chip'))e.target.click();});
document.addEventListener('input',e=>{if(e.target.matches('.note')){get(e.target.closest('.cand').dataset.c,e.target.closest('.cand').dataset.l).note=e.target.value;localStorage.setItem(KEY,JSON.stringify(state));}});
document.getElementById('clear').onclick=()=>{if(confirm('Clear all answers?')){localStorage.removeItem(KEY);for(const kk in state)delete state[kk];save();}};
document.getElementById('copy').onclick=async()=>{
  const out={};document.querySelectorAll('.cand').forEach(el=>{out[k(el.dataset.c,el.dataset.l)]=get(el.dataset.c,el.dataset.l);});
  const txt=JSON.stringify(out,null,1);
  try{await navigator.clipboard.writeText(txt);document.getElementById('copy').textContent='Copied!';setTimeout(()=>document.getElementById('copy').textContent='Copy labels',1500);}
  catch(_){const b=document.getElementById('outbox');b.style.display='block';b.querySelector('textarea').value=txt;b.querySelector('textarea').select();}
};
render();
</script>`;

const outPath = path.join(OUT, 'gallery.html');
fs.writeFileSync(outPath, asciify(html));

// ---- blinding assertion ----
const written = fs.readFileSync(outPath, 'utf8');
const leaked = Object.keys(key).filter((kk) => written.includes(kk));
const armWords = (written.match(/\brestored\b/g) || []).length + (written.match(/"current"/g) || []).length;
const nonAscii = (written.match(/[^\x00-\x7F]/g) || []).length;
console.log(`gallery.html: ${(fs.statSync(outPath).size / 1e6).toFixed(2)} MB, ${rows.length} rows`);
console.log(`blinding: key entries = ${leaked.length} (must be 0) | arm words = ${armWords} (must be 0) | non-ASCII chars = ${nonAscii} (must be 0)`);
if (leaked.length || armWords || nonAscii) { console.error('GALLERY ASSERTION FAILURE'); process.exitCode = 1; }
