#!/usr/bin/env python3
"""Build the neutral DS-37 cover review; never expose the private model key."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/ds37-dr-mike-dial-20261103'
P=R/'blind-review';P.mkdir(exist_ok=True)
key=json.loads((R/'.blind-key.json').read_text())['labels']
TEXT={'A':'The Appetite Dial','B':'Dial It In','C':'Find Your Level','D':'A Smaller Appetite','E':'Keep The Protein','F':'At The Diner','G':'Poolside Control','H':'Control Panel'}
items=[]
for x in sorted(key,key=lambda s:int(s[1:])):
 k=re.search(r'letter (\w)',key[x]['note']).group(1)
 for pf in ['instagram','youtube']:
  im=Image.open(R/f'ds37/{pf}/ds-37_dr-mike-dial_cover-{k}.png').convert('RGB')
  im.save(P/f'{x}-{pf}.jpg',quality=94)
  if pf=='instagram':im.crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS).save(P/f'{x}-grid.jpg',quality=94)
 items.append((x,TEXT[k],k))
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',26)
for start in [0,4]:
 sheet=Image.new('RGB',(1200,1140),'#101823');d=ImageDraw.Draw(sheet)
 for j,(x,t,k) in enumerate(items[start:start+4]):
  for n,pf in enumerate(['instagram','youtube']):
   xx=j*300;yy=n*570
   d.text((xx+10,yy+12),f'{x} / {"Instagram" if n==0 else "YouTube"}',font=font,fill='white')
   im=Image.open(P/f'{x}-{pf}.jpg');im.thumbnail((280,500));sheet.paste(im,(xx+10,yy+55))
 sheet.save(P/f'choices-{start+1}-{start+4}.jpg',quality=95)
css='''*{box-sizing:border-box}body{margin:0;background:#101823;color:#f1f5f9;font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1240px;margin:auto;padding:30px 20px}h1{margin:0;font-size:34px}p{color:#cbd5e1;max-width:900px}a{color:#8bd7ff}section{padding:22px;margin:26px 0;background:#192536;border:1px solid #35465a;border-radius:14px}h2{margin:0 0 12px}.pair{display:grid;grid-template-columns:1fr 1fr .7fr;gap:20px;align-items:start}img{width:100%;height:auto;display:block;border-radius:6px}figure{margin:0;min-width:0}figcaption{margin-bottom:8px;font-size:14px;color:#cbd5e1}nav{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}nav a{padding:8px 18px;background:#23364d;border-radius:8px;text-decoration:none}.sheets{display:grid;grid-template-columns:1fr 1fr;gap:16px}small{color:#bcc8d8}@media(max-width:700px){main{padding:20px 12px}.pair{grid-template-columns:1fr 1fr;gap:12px}.grid{grid-column:1/3;max-width:230px}.sheets{grid-template-columns:1fr}h1{font-size:28px}}'''
h=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dr Mike Dial Cover Choices</title><style>{css}</style></head><body><main><h1>Tirzepatide Is An Appetite Dial</h1><p>Eight cover choices. Each has an Instagram layout, a YouTube Shorts layout and the Instagram profile-grid crop. Choose X1 to X8 in this chat.</p><p>Your approved 59.3-second film is finalized and its three copies are verified. Nothing is uploaded to publishing platforms or scheduled yet. Pick a cover here, then setup continues.</p><nav>']
for x,t,k in items:h.append(f'<a href="#{x}">{x}</a>')
h.append('</nav><div class="sheets">')
for n in ['1-4','5-8']:h.append(f'<a href="choices-{n}.jpg"><img src="choices-{n}.jpg" alt="Cover choices {n}"></a>')
h.append('</div>')
for x,t,k in items:
 h.append(f'<section id="{x}"><h2>{x}: {t}</h2><div class="pair">')
 for pf,title in [('instagram','Instagram'),('youtube','YouTube Shorts'),('grid','Instagram Profile Crop')]:
  h.append(f'<figure class="{"grid" if pf=="grid" else ""}"><figcaption>{title}</figcaption><a href="{x}-{pf}.jpg"><img loading="lazy" src="{x}-{pf}.jpg" alt="{x} {title}"></a></figure>')
 h.append('</div></section>')
h.append('<p>Reply in this chat with your chosen X number. Both platform layouts travel together. Setup continues after your pick.</p></main></body></html>')
(P/'index.html').write_text(''.join(h))
print('Neutral review ready:',P)
