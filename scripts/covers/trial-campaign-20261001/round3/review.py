"""Self-contained round-3 review, with only two pending decisions."""
from pathlib import Path
import base64, json, re

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
R = ROOT/'social media graphics/youtube/thumbnails/_trial-campaign-20261001/round3'
manifest = json.loads((R/'manifest.json').read_text())

def card(code, title, source, path, decision=None, recommended=False):
    pick = ''
    if decision:
        pick = f'<label class="pick"><input type="radio" name="{decision}" value="{code}"> Choose {code}</label>'
    return f'''<article><div class="meta">{code}{' <b>RECOMMENDED</b>' if recommended else ''}</div><h3>{title}</h3>
    <button class="image" aria-label="Enlarge {code}" onclick="enlarge(this)"><img src="{path}" alt="{code}: {title}"></button>
    <p class="source">{source}</p>{pick}</article>'''

ad13 = card('13-R3B','Continuous gray background','photo-10 | Real pool portrait | Existing robot scene','options/13-R3B-16x9.jpg','ad13',True)
ad6 = card('6-R2A','Original photo, unchanged','studio-blue-171 | Real jeans-and-glasses photo','references/6-R2A-16x9.jpg','ad6')
ad6 += card('6-R3B','AI age edit','studio-blue-171 | Subtle salt-and-pepper hair, face and neck edit; original body','options/6-R3B-16x9.jpg','ad6',True)
locked = ''
titles = {'RA-R2A':'RA-01: AI Got Me Abs','10-R2A':'Ad 10: Busy Dad Fitness','4-R2A':'Ad 4: Confident Smirk','3-R2A':'Ad 3: Stop Paying Human Trainers'}
for code,title in titles.items():
    rows = [x for x in manifest['locked_approvals'] if x['choice']==code]
    locked += f'<article><div class="meta">APPROVED AND LOCKED</div><h3>{title}</h3><button class="image" onclick="enlarge(this)"><img src="references/{code}-16x9.jpg" alt="{code}, approved"></button><p>{code}</p><details><summary>Approved formats</summary><div class="formats">'
    for row in rows:
        locked += f'<button class="image" onclick="enlarge(this)"><img src="{row["path"]}" alt="{code} {row["aspect"]}"><span>{row["aspect"]}</span></button>'
    locked += '</div></details></article>'

html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Trial Campaign AD Thumbnails R3</title><style>
:root{color-scheme:dark;font-family:Arial,sans-serif;background:#10151a;color:#f3f5f7}*{box-sizing:border-box}body{max-width:1440px;margin:0 auto;padding:32px 28px 70px}h1{font-size:38px;margin:8px 0}h2{margin:0 0 12px;font-size:26px}h3{font-size:18px;margin:9px 0 14px}p,li{line-height:1.55;color:#c5cfd8}header{margin-bottom:28px}.eyebrow,.meta{font-size:12px;letter-spacing:.08em;color:#a9b8c6;font-weight:bold}.meta b{color:#ffc94c;margin-left:12px}.decided{background:#1d2730;padding:22px;border-radius:12px;margin:25px 0}.decided h2{font-size:20px}.decided ul{padding-left:20px;margin-bottom:0}section{margin:36px 0 46px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.single{max-width:960px}article{border:1px solid #36424d;border-radius:12px;padding:18px;background:#172028;min-width:0}.image{display:block;width:100%;padding:0;border:0;background:transparent;color:inherit;cursor:zoom-in}.image img{width:100%;display:block;border-radius:5px}.source{font-size:13px;margin:14px 0}.pick{display:block;background:#2b3944;padding:13px;border-radius:7px;cursor:pointer;font-weight:bold}input{accent-color:#ffcd4c;width:18px;height:18px;vertical-align:middle;margin-right:8px}article:has(input:checked){border-color:#ffcd4c;box-shadow:0 0 0 1px #ffcd4c}button.action,select{background:#283847;color:#fff;border:1px solid #637789;border-radius:6px;padding:10px 16px;cursor:pointer}button.action.primary{background:#ffd05a;color:#151b20;border:0;font-weight:bold}.toolbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:20px 0}.phone .grid{justify-content:start}.phone article .image{width:320px;max-width:100%;margin:auto}.phone .single{max-width:720px}.locked{grid-template-columns:repeat(4,minmax(0,1fr))}.locked h3{font-size:16px}.locked p{font-size:13px}.formats{display:flex;gap:10px;padding-top:12px}.formats .image{width:33%}.formats img{height:100px;object-fit:contain}details{margin:18px 0}summary{cursor:pointer;color:#b7cce0;padding:8px 0}.reference{max-width:720px;margin-top:12px}.note{font-size:14px}textarea{display:block;width:100%;min-height:110px;background:#10171e;border:1px solid #657887;border-radius:8px;padding:15px;color:white;font:16px/1.5 Arial;margin:16px 0}dialog{background:#121a22;border:1px solid #718497;color:#fff;max-width:96vw;width:1320px;border-radius:10px}dialog::backdrop{background:#000c}dialog img{display:block;max-width:100%;max-height:83vh;margin:auto;object-fit:contain}dialog button{float:right;margin-bottom:12px}#status{color:#ffd05a;min-height:22px}@media(max-width:760px){body{padding:22px 15px}.grid,.locked{grid-template-columns:1fr}h1{font-size:30px}.locked{grid-template-columns:repeat(2,minmax(0,1fr))}.locked article{padding:10px}}
</style></head><body>
<header><div class="eyebrow">TRIAL CAMPAIGN 24316364155 | OCTOBER 1, 2026</div><h1>Trial Campaign AD Thumbnails R3</h1><p>Two remaining decisions. Four approved ads stay locked.</p></header>
<div class="decided"><h2>What I decided (overrule anything)</h2><ul>
<li>Ad 13: reuse the original gray texture to remove the black top stripe. Keep the robot, portrait, headline and placement.</li>
<li>Ad 6: keep dark hair dominant, with scattered gray strands and temples. Add mild face and neck texture; retain the original physique, hands and clothing.</li>
<li>My picks: <strong>13-R3B and 6-R3B</strong>. The age edit makes the 40+ message clearer while keeping the jeans-and-glasses pose you liked.</li>
</ul></div>
<div class="toolbar"><button class="action" id="size" onclick="toggleSize()">Show 320px phone views</button><span class="note">Click any image to enlarge. Recommendations are creative judgments, not test results.</span></div>
<section><h2>1. Ad 13: confirm the background fix</h2><div class="single">__AD13__</div>
<details><summary>Previous robot version and gray-background reference</summary><div class="grid reference">__OLD13__</div></details>
<label class="pick single"><input type="radio" name="ad13" value="revise">Ad 13 still needs a revision</label></section>
<section><h2>2. Ad 6: choose the version</h2><p>Same gym, headline, outline, pose and original body. Only the hair, face and neck differ.</p><div class="grid">__AD6__</div>
<details><summary>Closer look at the age edit</summary><div class="reference"><button class="image" onclick="enlarge(this)"><img src="qa/ad6-head-comparison.jpg" alt="Original head on the left, AI age edit on the right"></button><p class="note">Original at left. AI age edit at right.</p></div></details></section>
<section><h2>Your two decisions</h2><p>Selections stay in this browser. Copy the reply and send it in chat.</p><textarea id="reply" aria-label="Reply to copy" readonly></textarea><button class="action primary" id="copy" onclick="copyReply()">Copy reply</button> <button class="action" onclick="clearPicks()">Clear picks</button><p id="status" aria-live="polite"></p></section>
<section><h2>Approved references, unchanged</h2><p class="note">Already approved. No further choice needed. Original JPG bytes preserved across all eight approved layouts.</p><div class="grid locked">__LOCKED__</div></section>
<p class="note">Review only. One Codex subscription image generation. No final exports or installation in this round.</p>
<dialog id="zoom"><button class="action" onclick="document.getElementById('zoom').close()">Close</button><img id="zoomImage" alt="Enlarged thumbnail"></dialog>
<script>
const key='trial-campaign-thumbnails-round3-20261001';
function update(save=true){const a=document.querySelector('input[name="ad13"]:checked')?.value;const b=document.querySelector('input[name="ad6"]:checked')?.value;document.getElementById('reply').value='Ad 13: '+(a==='revise'?'Needs revision: [describe change]':a?'Approve '+a:'[confirm 13-R3B or describe change]')+'\\nAd 6: '+(b?'Choose '+b:'[choose 6-R2A original or 6-R3B AI age edit]')+'\\nKeep RA-R2A, 10-R2A, 4-R2A and 3-R2A approved and unchanged.';if(save){try{localStorage.setItem(key,JSON.stringify({ad13:a,ad6:b}))}catch(e){}}}
document.querySelectorAll('input').forEach(x=>x.addEventListener('change',()=>update()));
try{const saved=JSON.parse(localStorage.getItem(key)||'{}');for(const [name,value]of Object.entries(saved)){const el=[...document.querySelectorAll('input')].find(x=>x.name===name&&x.value===value);if(el)el.checked=true}}catch(e){}update(false);
function toggleSize(){const on=document.body.classList.toggle('phone');document.getElementById('size').textContent=on?'Show large views':'Show 320px phone views'}
function enlarge(button){const im=button.querySelector('img');document.getElementById('zoomImage').src=im.src;document.getElementById('zoomImage').alt=im.alt;document.getElementById('zoom').showModal()}
async function copyReply(){const el=document.getElementById('reply');try{await navigator.clipboard.writeText(el.value);document.getElementById('status').textContent='Copied. Paste your decisions in chat.'}catch(e){el.select();document.getElementById('status').textContent='Reply selected. Press Command+C to copy.'}}
function clearPicks(){document.querySelectorAll('input').forEach(x=>x.checked=false);try{localStorage.removeItem(key)}catch(e){}update(false);document.getElementById('status').textContent='Picks cleared.'}
</script></body></html>'''
old = card('13-R2B','Previous version','Reference only','references/13-R2B-16x9.jpg') + card('13-R2A','Gray texture reference','Reference only','references/13-R2A-16x9.jpg')
for key,value in [('__AD13__',ad13),('__AD6__',ad6),('__OLD13__',old),('__LOCKED__',locked)]:html=html.replace(key,value)
assert '\u2014' not in html and '\u2013' not in html
(R/'index.html').write_text(html)
def embed(match):
    path=R/match.group(1)
    return 'src="data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
(R/'review-offline.html').write_text(re.sub(r'src="([^"]+\.jpg)"',embed,html))
print('Review page and offline review written.')
