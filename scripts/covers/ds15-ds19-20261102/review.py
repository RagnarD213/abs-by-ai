#!/usr/bin/env python3
"""Publish paired cover choices with neutral labels and no generation provenance."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,re
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'Short-form video content/covers/review/jiu-jitsu-battle-ropes-20261102'
PUB=OUT/'blind-review';PUB.mkdir(exist_ok=True)
F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',24)
css='''*{box-sizing:border-box}body{margin:0;background:#101823;color:#f1f5f9;font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1240px;margin:auto;padding:30px 20px}h1{font-size:34px;line-height:1.2}h2{font-size:30px}p{color:#cbd5e1;max-width:940px}a{color:#8bd7ff}.notice,article{padding:22px;margin:24px 0;background:#192536;border:1px solid #35465a;border-radius:14px}h3{margin:0 0 12px}.pair{display:grid;grid-template-columns:1fr 1fr .7fr;gap:20px;align-items:start}img{width:100%;height:auto;display:block;border-radius:6px}figure{margin:0;min-width:0}figcaption{margin-bottom:8px;font-size:14px;color:#cbd5e1}nav{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}nav a{padding:8px 18px;background:#23364d;border-radius:8px;text-decoration:none}.sheets{display:grid;grid-template-columns:1fr 1fr;gap:16px}section{margin-top:48px;border-top:2px solid #49617e;padding-top:16px}@media(max-width:700px){main{padding:20px 12px}.pair{grid-template-columns:1fr 1fr;gap:12px}.grid{grid-column:1/3;max-width:230px}.sheets{grid-template-columns:1fr}h1{font-size:28px}}'''
h=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jiu Jitsu And Battle Ropes Cover Choices</title><style>{css}</style></head><body><main><h1>Jiu Jitsu And Battle Ropes</h1><p>Choose one cover for each Short. Each set has your five standard designs plus three comparison options, shuffled as X1 to X8. Check the Instagram, YouTube Shorts and Instagram profile-grid versions below.</p><div class="notice"><strong>Waiting for your cover picks and Muhammad’s HQ exports.</strong><p>Both V2 edits are finalized. Your HQ request is the latest Upwork message, and the shared HD folder has neither export yet. The available 18.5 MB files are review copies. HQ comparison, backups, upload and queue placement remain pending. No film reapproval is requested.</p></div><nav><a href="#ds15">Jiu Jitsu Choices</a><a href="#ds19">Battle Ropes Choices</a></nav>']
for key,title,slug in [('ds15','Does Jiu Jitsu Get You Abs?','ds-15_jiu-jitsu'),('ds19','How To Use Battle Ropes','ds-19_battle-ropes')]:
 labels=json.loads((OUT/key/'.blind-key.json').read_text())['labels'];items=[]
 for x in sorted(labels,key=lambda v:int(v[1:])):
  k=re.search(r'letter (\w)',labels[x]['note']).group(1)
  for pf in ['instagram','youtube']:
   im=Image.open(OUT/key/pf/f'{slug}_cover-{k}.png').convert('RGB');im.save(PUB/f'{key}-{x}-{pf}.jpg',quality=94)
   if pf=='instagram':im.crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS).save(PUB/f'{key}-{x}-grid.jpg',quality=94)
  items.append(x)
 for start in [0,4]:
  sheet=Image.new('RGB',(1200,1140),'#101823');d=ImageDraw.Draw(sheet)
  for j,x in enumerate(items[start:start+4]):
   for n,pf in enumerate(['instagram','youtube']):
    xx=j*300;yy=n*570;d.text((xx+10,yy+12),f'{x} / {"Instagram" if n==0 else "YouTube"}',font=F,fill='white');im=Image.open(PUB/f'{key}-{x}-{pf}.jpg');im.thumbnail((280,500));sheet.paste(im,(xx+10,yy+55))
  sheet.save(PUB/f'{key}-choices-{start+1}-{start+4}.jpg',quality=95)
 h.append(f'<section id="{key}"><h2>{title}</h2><p>Choose {"Jiu Jitsu" if key=="ds15" else "Battle Ropes"}: X1 to X8.</p><div class="sheets">')
 for part in ['1-4','5-8']:h.append(f'<a href="{key}-choices-{part}.jpg"><img src="{key}-choices-{part}.jpg" alt="{title} choices {part}"></a>')
 h.append('</div><nav>')
 for x in items:h.append(f'<a href="#{key}-{x}">{x}</a>')
 h.append('</nav>')
 for x in items:
  h.append(f'<article id="{key}-{x}"><h3>{x}</h3><div class="pair">')
  for pf,caption in [('instagram','Instagram'),('youtube','YouTube Shorts'),('grid','Instagram Profile Crop')]:h.append(f'<figure class="{"grid" if pf=="grid" else ""}"><figcaption>{caption}</figcaption><a href="{key}-{x}-{pf}.jpg"><img loading="lazy" src="{key}-{x}-{pf}.jpg" alt="{title}: {x}, {caption}"></a></figure>')
  h.append('</div></article>')
 h.append('</section>')
h.append('<p>Reply in this chat, for example: “Jiu Jitsu X2, Battle Ropes X6.” After your picks and the matching HQ exports, setup continues here.</p></main></body></html>');(PUB/'index.html').write_text(''.join(h))
print(PUB)
