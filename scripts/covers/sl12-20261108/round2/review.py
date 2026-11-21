"""Paired review for four real A screenshots and the selected B food repair."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[4]
R=Path('/Volumes/Extreme/_edit_work/SL-12/setup/round2')
PAGE=Path('/Volumes/Extreme/_edit_work/SL-12/round1/asset-review/setup')
PAGE.mkdir(parents=True,exist_ok=True)
names={x['label']:x['exercise'] for x in json.loads((R/'selected-sources.json').read_text())}
for key in ['A1','A2','A3','A4','BX2']:
    for platform in ['instagram','youtube']:
        shutil.copyfile(R/'covers'/key/(platform+'.jpg'),PAGE/(key+'-'+platform+'.jpg'))
    shutil.copyfile(R/'covers'/key/'profile.jpg',PAGE/(key+'-profile.jpg'))
shutil.copyfile(R/'four-real-choices.jpg',PAGE/'A-four-real-choices.jpg')
# Before/after source proof, no inventing or redrawing the subject.
proof=Image.new('RGB',(1200,4*360),'#101922');dr=ImageDraw.Draw(proof)
for n,key in enumerate(['A1','A2','A3','A4']):
    for j,kind in enumerate(['original','touched-up']):
        im=Image.open(R/'sources'/(key+'-'+kind+'.png')).convert('RGB');im.thumbnail((590,320))
        proof.paste(im,(j*600,n*360+30));dr.text((j*600+10,n*360+5),key+' '+kind,fill='white')
proof.save(PAGE/'source-touchups.jpg',quality=94)

s='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keep Your Muscle: Revised Covers</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b121a;color:#edf4fc;font:16px/1.45 system-ui}main{max-width:1250px;margin:auto;padding:18px}h1{font-size:26px;line-height:1.12;margin:6px 0 12px}h2{font-size:24px;line-height:1.18}p{max-width:800px}a{color:#8bd9ff}.hold{border-left:4px solid #f5cd4d;background:#1a2635;padding:10px 14px}.nav{position:sticky;top:0;z-index:2;background:#0b121af2;padding:12px 0;display:flex;gap:22px}.grid{display:grid;grid-template-columns:1fr;gap:18px}article{padding:14px;background:#17212e;border:1px solid #304257;border-radius:14px}h3{font-size:23px;margin:0 0 4px}.exercise{color:#bdd0df;margin:0 0 8px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start}.pair img{width:100%;height:auto;border-radius:5px}.caption{color:#b8cbdc;font-size:13px;margin:7px 0}small{font-size:12px}section{scroll-margin-top:65px;margin-top:22px}details{margin-top:24px}details img{max-width:100%}.note{font-size:14px;color:#bdd0df}@media(min-width:900px){main{padding:28px}.grid{grid-template-columns:1fr 1fr}}
</style></head><body><main><h1>Keep Your Muscle<br>Revised Cover Choices</h1>
<p>Choose <b>A1, A2, A3 or A4</b>. Approve the revised <b>B X2 Instagram</b> cover below.</p><p class="hold">Publishing stays held until the parent is confirmed public on or after December 6.</p><nav class="nav"><a href="#A">A: Four New Designs</a><a href="#B">B: Foods Visible</a></nav><section id="A"><h2>A: Four Real Lifting Screenshots</h2><p class="note">Four different photographs and designs, with photographic touch-ups. The earlier A options are replaced.</p><p><a href="A-four-real-choices.jpg">View all four together</a></p><div class="grid">'''
for key in ['A1','A2','A3','A4']:
    s+=f'''<article><h3>{key}</h3><p class="exercise">{names[key]}</p><div class="pair"><div><p class="caption">Instagram profile tile</p><a href="{key}-instagram.jpg"><img src="{key}-profile.jpg" alt="{key} Instagram profile crop"><small>Open full Instagram cover</small></a></div><div><p class="caption">YouTube cover</p><a href="{key}-youtube.jpg"><img src="{key}-youtube.jpg" alt="{key} YouTube cover"></a></div></div></article>'''
s+='''</div></section><section id="B"><h2>B X2: Keep The Foods Visible</h2><p>The YouTube cover is your approved original. Instagram now fits the same whole food scene inside its profile crop.</p><article><div class="pair"><div><p class="caption">Revised Instagram profile tile</p><a href="BX2-instagram.jpg"><img src="BX2-profile.jpg" alt="B X2 revised Instagram with three food plates and shaker visible"><small>Open full Instagram cover</small></a></div><div><p class="caption">Approved YouTube cover, unchanged</p><a href="BX2-youtube.jpg"><img src="BX2-youtube.jpg" alt="B X2 unchanged approved YouTube cover"></a></div></div></article></section><details><summary>Original A Screenshots And Touch-Ups</summary><p>Exposure, contrast, color and sharpening adjustments. The people, poses, clothing and equipment come from the actual frames.</p><a href="source-touchups.jpg"><img src="source-touchups.jpg" alt="Four original video frames beside their photographic touch-ups"></a></details><p>Reply with your A choice and whether the revised B Instagram cover is approved. Your video edits remain approved. No revised cover has been installed or scheduled.</p></main></body></html>'''
old=PAGE/'index.html'
if old.exists() and not (R/'previous-review-page.html').exists():shutil.copyfile(old,R/'previous-review-page.html')
old.write_text(s)
print('Revised cover page built at',PAGE)
