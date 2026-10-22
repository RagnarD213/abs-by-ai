#!/usr/bin/env python3
"""SL-09 covers round 2 review: REVIEW_r2.jpg and index.html (round 1 page kept as round1.html). Rows: short 1 F/G/H, short 3 E
with the new bottom picture, short 4 F/G/H, then the two locked picks (short 2 C, short 5 D) for reference."""
from pathlib import Path
import json,sys,html,shutil
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).parent));from build import COPY,R,BADGES
F='/System/Library/Fonts/Supplemental/Arial Bold.ttf';font=lambda s:ImageFont.truetype(F,s)
ROWS=[('s1',['F','G','H'],'Pick one'),('s3',['E'],'Your pick E, with the new bottom picture: confirm'),('s4',['F','G','H'],'Pick one'),
 ('s2',['C'],'Locked: your pick C'),('s5',['D'],'Locked: your pick D')]
LAB={('s1','F'):'F: yellow band on top',('s1','G'):'G: headline at the bottom',('s1','H'):'H: headline top left, white frame',
 ('s3','E'):'E: two pictures, you below',('s4','F'):'F: yellow band on top',('s4','G'):'G: headline at the bottom',('s4','H'):'H: two pictures, sleep chart below',
 ('s2','C'):'C: yellow band on top',('s5','D'):'D: headline at the bottom'}
SUB={('s1','F'):'AI you, zombie tired, barbell at the collarbone with a stack of plates',('s1','G'):'AI you, zombie tired, pressing two huge dumbbells',
 ('s1','H'):'AI you, zombie tired, barbell halfway up with huge plates',('s3','E'):'Top: speeding at night. Bottom: AI you wired awake in bed, keys on the nightstand',
 ('s4','F'):'AI you, shirtless zombie at the table, coffee and a weak thumbs up',('s4','G'):'AI you, same scene, table in shadow below',
 ('s4','H'):'Top: AI you at the table with coffee and a thumbs up. Bottom: the spiky sleep chart',('s2','C'):'AI you on the bed with the crashing chart',('s5','D'):'The ring and the strap side by side'}
get=lambda k,v,pl:Image.open(R/pl/f'{COPY[k][1]}_cover-{v}.png')
cw,ch=236,420;colw=2*cw+14+28;rowh=ch+86
im=Image.new('RGB',(3*colw+40,150+len(ROWS)*rowh),(18,23,31));d=ImageDraw.Draw(im)
d.text((24,16),'OURA RING REVIEW SHORTS: COVERS ROUND 2',font=font(40),fill='white')
d.text((24,70),'Each choice twice: Instagram / TikTok / Facebook layout (left), YouTube layout (right).',font=font(26),fill=(185,198,209))
web=R/'web';web.mkdir(exist_ok=True)
for r,(k,vs,note) in enumerate(ROWS):
 y=130+r*rowh;n=int(k[1]);d.text((24,y),f'Short {n}: {COPY[k][2]}   ({note})',font=font(30),fill=(255,214,0))
 for c,v in enumerate(vs):
  x=24+c*colw;d.text((x,y+44),LAB[(k,v)],font=font(23),fill=(213,228,238))
  for j,pl in enumerate(['instagram','youtube']):
   g=get(k,v,pl);im.paste(g.resize((cw,ch),Image.Resampling.LANCZOS),(x+j*(cw+14),y+78))
   g.resize((540,960),Image.Resampling.LANCZOS).save(web/f'{COPY[k][1]}_{v}_{pl}.jpg',quality=88)
im.save(R/'REVIEW_r2.jpg',quality=90)
if (R/'index.html').exists() and not (R/'round1.html').exists():shutil.copy(R/'index.html',R/'round1.html')
h=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Oura Shorts Covers R2</title>',
'<style>body{background:#12171f;color:#e8eef4;font:16px/1.45 -apple-system,Helvetica,Arial,sans-serif;margin:0;padding:24px}h1{font-size:26px;margin:0 0 6px}h2{color:#ffd600;font-size:21px;margin:34px 0 4px}p{margin:4px 0 10px;color:#b9c6d1;max-width:1100px}.row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.c{background:#1b232e;border-radius:10px;padding:10px}.c b{display:block;margin-bottom:2px}.c small{display:block;color:#9fb0bf;min-height:38px;margin-bottom:6px}.pair{display:flex;gap:6px}.pair figure{margin:0;flex:1}.pair img{width:100%;border-radius:6px;display:block}figcaption{font-size:11px;color:#8fa1b1;text-align:center;margin-top:2px}a{color:#8fd3ff}@media(max-width:900px){.row{grid-template-columns:1fr}}</style>',
'<h1>Oura Ring Review Shorts: covers round 2</h1>',
'<p>Short 1 and short 4: three new designs each, AI images of you as a sleep-deprived zombie. Short 3: your pick E with the new bottom picture. Shorts 2 and 5 are locked. Reply with one letter for short 1 and short 4, and OK (or changes) for short 3. Click any picture to open it larger. <a href="round1.html">Round 1 page</a></p>']
for k,vs,note in ROWS:
 h.append(f'<h2>Short {k[1]}: {html.escape(COPY[k][2])} <span style="color:#8fa1b1;font-size:15px">({html.escape(note)})</span></h2><p>Cover copy: {html.escape(BADGES[k])} / {html.escape(" ".join(COPY[k][0]))}</p><div class="row">')
 for v in vs:
  h.append(f'<div class="c"><b>{html.escape(LAB[(k,v)])}</b><small>{html.escape(SUB[(k,v)])}</small><div class="pair">'+''.join(f'<figure><a href="web/{COPY[k][1]}_{v}_{pl}.jpg" target="_blank"><img loading="lazy" src="web/{COPY[k][1]}_{v}_{pl}.jpg"></a><figcaption>{"Instagram" if pl=="instagram" else "YouTube"}</figcaption></figure>' for pl in ['instagram','youtube'])+'</div></div>')
 h.append('</div>')
(R/'index.html').write_text('\n'.join(h));print('round 2 review built')
