#!/usr/bin/env python3
"""SL-15 covers round 5 review: REVIEW_r5.jpg and index.html (round 2 page kept as round2.html). Short 1 H/I/K (F's photos, new copy), short 2 C locked."""
from pathlib import Path
import json,sys,html,shutil
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).parent));from build import COPY,R,BADGES
F='/System/Library/Fonts/Supplemental/Arial Bold.ttf';font=lambda s:ImageFont.truetype(F,s)
ROWS=[('s1',['K'],'Your pick K, revised: confirm'),('s2',['C'],'Locked: your pick C')]
LAB={('s1','H'):'H: diagonal split, headline on top',('s1','I'):'I: diagonal split, headline at the bottom',('s1','K'):'K round 5: larger photo; YouTube fills to the bottom',('s2','C'):'C: yellow band on top'}
SUB={('s1','H'):'Cut-outs of you with a white outline: pale on cool slate, tanned on warm bronze',('s1','I'):'The same idea the other way round, headline on black below',
 ('s1','K'):'Instagram photo larger; YouTube laid out like Instagram, your photo to the bottom edge, print moved down (0 px overlap with your body)',('s2','C'):'AI you, tanned, in the shade of a beach umbrella'}
CUR={'s1':'SPRAY TANNING / How A Spray Tan Makes You Look More Ripped'}
get=lambda k,v,pl:Image.open(R/pl/f'{COPY[k][1]}_cover-{v}.png')
cw,ch=236,420;colw=2*cw+14+28;rowh=ch+86
im=Image.new('RGB',(3*colw+40,150+len(ROWS)*rowh),(18,23,31));d=ImageDraw.Draw(im)
d.text((24,16),'MY FIRST SPRAY TAN SHORTS: COVERS ROUND 5',font=font(40),fill='white')
d.text((24,70),'Each choice twice: Instagram / TikTok / Facebook layout (left), YouTube layout (right).',font=font(26),fill=(185,198,209))
web=R/'web';web.mkdir(exist_ok=True)
for r,(k,vs,note) in enumerate(ROWS):
 y=130+r*rowh;n=int(k[1]);d.text((24,y),f'Short {n}: {COPY[k][2]}   ({note})',font=font(30),fill=(255,214,0))
 for c,v in enumerate(vs):
  x=24+c*colw;d.text((x,y+44),LAB[(k,v)],font=font(23),fill=(213,228,238))
  for j,pl in enumerate(['instagram','youtube']):
   g=get(k,v,pl);im.paste(g.resize((cw,ch),Image.Resampling.LANCZOS),(x+j*(cw+14),y+78))
   g.resize((540,960),Image.Resampling.LANCZOS).save(web/f'{COPY[k][1]}_{v}_{pl}.jpg',quality=88)
im.save(R/'REVIEW_r5.jpg',quality=90)
if (R/'index.html').exists() and not (R/'round4.html').exists():shutil.copy(R/'index.html',R/'round4.html')
h=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Spray Tan Shorts Covers R5</title>',
'<style>body{background:#12171f;color:#e8eef4;font:16px/1.45 -apple-system,Helvetica,Arial,sans-serif;margin:0;padding:24px}h1{font-size:26px;margin:0 0 6px}h2{color:#ffd600;font-size:21px;margin:34px 0 4px}p{margin:4px 0 10px;color:#b9c6d1;max-width:1100px}.row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.c{background:#1b232e;border-radius:10px;padding:10px}.c b{display:block;margin-bottom:2px}.c small{display:block;color:#9fb0bf;min-height:38px;margin-bottom:6px}.pair{display:flex;gap:6px}.pair figure{margin:0;flex:1}.pair img{width:100%;border-radius:6px;display:block}figcaption{font-size:11px;color:#8fa1b1;text-align:center;margin-top:2px}a{color:#8fd3ff}@media(max-width:900px){.row{grid-template-columns:1fr}}</style>',
'<h1>My First Spray Tan Shorts: covers round 5</h1>',
'<p>Short 1: K with your round 5 notes: the Instagram photo is larger; on YouTube your photo now runs to the bottom, the layout matches Instagram and the photo sits lower. Short 2 is locked on C. Reply OK (or changes). Click any picture to open it larger. <a href="round4.html">Round 4 page</a></p>']
for k,vs,note in ROWS:
 h.append(f'<h2>Short {k[1]}: {html.escape(COPY[k][2])} <span style="color:#8fa1b1;font-size:15px">({html.escape(note)})</span></h2><p>Cover copy: {html.escape(CUR.get(k,BADGES[k]+" / "+" ".join(COPY[k][0])))}</p><div class="row">')
 for v in vs:
  h.append(f'<div class="c"><b>{html.escape(LAB[(k,v)])}</b><small>{html.escape(SUB[(k,v)])}</small><div class="pair">'+''.join(f'<figure><a href="web/{COPY[k][1]}_{v}_{pl}.jpg" target="_blank"><img loading="lazy" src="web/{COPY[k][1]}_{v}_{pl}.jpg"></a><figcaption>{"Instagram" if pl=="instagram" else "YouTube"}</figcaption></figure>' for pl in ['instagram','youtube'])+'</div></div>')
 h.append('</div>')
(R/'index.html').write_text('\n'.join(h));print('round 2 review built')
