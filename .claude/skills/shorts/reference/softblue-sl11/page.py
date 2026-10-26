import json,html,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'review'
items=json.loads((R/'items-context.json').read_text())
titles={'A':'How To Do A Standing Stomach Vacuum','B':'Stop Holding Your Breath During Stomach Vacuums','C':'Start With One 20-Second Vacuum Every Morning'}
esc=html.escape
srt=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.srt').read_text()
def sec(x):
 h,m,s=map(float,x.replace(',','.').split(':'));return h*3600+m*60+s
cues=[]
for b in re.split(r'\n\s*\n',srt.strip()):
 ls=b.splitlines();a,z=ls[1].split(' --> ');cues.append((sec(a),sec(z),' '.join(ls[2:])))
def speech(a,b):return ' '.join(t for x,y,t in cues if x<b and y>a)
cards=[]
for S in titles:
 cards.append(f'<h2>{S}. {esc(titles[S])}</h2><div class="grid">')
 for it in [x for x in items if x['short']==S]:
  a=it['context_parent_start'];b=a+it['context_frames']/(30000/1001)
  text=it['point'] or titles[S]
  near=f'<p><a target="_blank" href="stills/{S}-near.jpg">Compare the closer crop</a></p>' if it['id'].endswith('title') and S != 'C' else ''
  cards.append(f'''<article><a target="_blank" href="{it['file']}"><img src="{it['file']}" loading="lazy"></a><p class="tag">{esc(it['id'])} · Parent {int(it['t']//60)}:{int(it['t']%60):02d}</p><h3>{esc(text)}</h3><p>{esc(it['note'])}</p><button onclick="play('{it['context']}','{esc(it['id'])}')">Play It Moving, In Context</button>{near}<details><summary>Speech before / during / after</summary><p><b>Before:</b> {esc(speech(a-3,a))}</p><p><b>During:</b> {esc(speech(a,b))}</p><p><b>After:</b> {esc(speech(b,b+3))}</p></details></article>''')
 cards.append('</div>')
page='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Vacuum · A, B, C · Graphics Review</title>
<style>*{box-sizing:border-box}body{font:17px/1.55 system-ui;background:#edf4fa;color:#16324c;margin:0}main{max-width:1450px;margin:auto;padding:40px 490px 80px 36px}h1{font-size:40px;line-height:1.15}h2{margin:40px 0 18px;font-size:27px}.lead{font-size:20px}.box{padding:20px;border:1px solid #bfd5e6;border-radius:14px;background:white;margin:18px 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px}.grid article{background:white;border:1px solid #bfd5e6;border-radius:12px;padding:12px}.grid img{width:100%;height:auto;border-radius:6px}.tag{color:#54748f;font-size:13px}h3{font-size:18px;line-height:1.3}button{padding:11px 13px;border:0;border-radius:8px;background:#166292;color:white;font:inherit;cursor:pointer}a{color:#135f94}details{font-size:14px;margin-top:12px}#dock{position:fixed;right:25px;top:25px;width:410px;background:#102b43;color:white;border-radius:14px;padding:16px;box-shadow:0 8px 30px #17365033}#dock video{width:100%;max-height:72vh;background:black}textarea{width:100%;height:170px;font:inherit;padding:12px}@media(max-width:1100px){main{padding:24px;max-width:1000px}#dock{position:sticky;top:0;right:auto;width:100%;z-index:3}#dock video{max-height:55vh}.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:650px){.grid{grid-template-columns:1fr}h1{font-size:30px}}</style>
<aside id="dock"><div id="now">Choose a moving example below</div><video id="player" controls playsinline preload="none" poster="stills/A-title.jpg" src="context/A-title-context.mp4"></video><p>Context examples and the isolated exercise demonstration. These are not the complete Shorts.</p></aside>
<main><p class="tag">CONTENT · THE VACUUM SFC R1 · A, B AND C SELECTED</p><h1>The Vacuum: Framing And Graphics</h1><p class="lead">Review the titles, crops and teaching graphics before the three complete cuts.</p>
<div class="box"><b>Already selected:</b> A, B and C. The original film's colour and voice are retained. No covers or uploads are included.<br><b>Not finished:</b> the complete Shorts, final caption timing, final delivery checks and full-file audit.</div>
<div class="box"><h2 style="margin-top:0">Your Decisions</h2><ol><li>Approve this framing and graphic set, or name what to change.</li><li>Record B's approved opening below at the next studio shoot. It has not been filmed.</li></ol></div>
<div class="box"><h3>B's Approved Studio Opening</h3><p>“Here's a mistake I see with a lot of beginners when they first start doing stomach vacuums.”</p><p>Dan approved this exact line on 26 October. Read it twice at the next studio shoot with the clip-on mic. The current B examples use the original film speech, not a substitute opening.</p></div>
<div class="box"><h3>The Exercise Demonstration</h3><p>The complete original draw-in, hold and release. Its silence is intentional. This isolated source example has no title; each finished Short will keep its own title.</p><button onclick="play('context/whole-exercise-source.mp4','Whole exercise source · 22 seconds')">Watch The Complete Movement</button></div><h2>What I Decided (Overrule Anything)</h2><ul><li>Use real exercise footage from this film for the openings and demonstrations.</li><li>Keep the exercise and hands visible. Most views stay wider; B’s recovery instruction and C’s title use a deliberate closer crop. Graphics and captions stay below the action. The timer, recovery and progression bars sit lower to clear hand movements; their captions use one short line.</li><li>Rebuild the built-in horizontal graphics for the phone frame, using the approved Soft Blue Light HyperFrames templates.</li><li>Keep the original look and voice. No new AI scenes or paid generation.</li><li>Show the wider teaching crop as the main option. Closer comparisons are available for A and B. C stays wide enough to keep both elbows visible.</li></ul>
'''+''.join(cards)+'''
<h2>Your Reply</h2><textarea id="reply">Framing and graphics: approved / changes:
B opening: wording approved; studio recording pending.
</textarea><button onclick="copyReply()">Copy Reply</button><p id="copied"></p><p>Prepared 26 October 2026. This approval covers the shown assets and crops. Finished-film approval remains separate.</p></main>
<script>function play(src,name){let p=document.getElementById('player');p.src=src;p.load();document.getElementById('now').textContent=name;p.play().catch(()=>{});}async function copyReply(){await navigator.clipboard.writeText(document.getElementById('reply').value);document.getElementById('copied').textContent='Copied. Paste your reply in the chat.'}</script>'''
(D/'index.html').write_text(page)
print(D/'index.html')
