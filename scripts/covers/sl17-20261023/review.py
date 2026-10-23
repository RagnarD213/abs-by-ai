#!/usr/bin/env python3
"""SL-17 Top 1% Shorts (adapted from SL-09). One review page (index.html) and one sheet (REVIEW_all.jpg) with every cover choice, both layouts, one numbered row per short."""
from pathlib import Path
import json,sys,html
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).parent));from build import COPY,ORDER,R,POOL,STUDIO,BADGES
F='/System/Library/Fonts/Supplemental/Arial Bold.ttf';font=lambda s:ImageFont.truetype(F,s)
m=json.loads((R/'manifest.json').read_text())['outputs'];keys=[k for k in ORDER if any(a['short']==k for a in m)]
kinds={'A':'A: Pool shoot photo','B':'B: Studio shoot photo','C':'C: AI image of you','D':'D: Codex choice 1','E':'E: Codex choice 2'}
get=lambda k,v,pl:Image.open(R/pl/f'{COPY[k][1]}_cover-{v}.png')
cw,ch=236,420;colw=2*cw+14+28;rowh=ch+86
im=Image.new('RGB',(5*colw+40,150+len(keys)*rowh),(18,23,31));d=ImageDraw.Draw(im)
d.text((24,16),f'TOP 1% SHORTS: FIVE COVER CHOICES PER SHORT ({5*len(keys)} total)',font=font(40),fill='white')
d.text((24,70),'Each choice shown twice: Instagram / TikTok / Facebook layout (left), YouTube layout (right). One letter per short.',font=font(26),fill=(185,198,209))
for r,k in enumerate(keys):
 y=130+r*rowh;d.text((24,y),f'Short {r+1}: {COPY[k][2]}',font=font(32),fill=(255,214,0))
 for c,v in enumerate('ABCDE'):
  x=24+c*colw;d.text((x,y+44),kinds[v],font=font(23),fill=(213,228,238))
  for j,pl in enumerate(['instagram','youtube']):im.paste(get(k,v,pl).resize((cw,ch),Image.Resampling.LANCZOS),(x+j*(cw+14),y+78))
im.save(R/'REVIEW_all.jpg',quality=90)
web=R/'web';web.mkdir(exist_ok=True)
for k in keys:
 for v in 'ABCDE':
  for pl in ['instagram','youtube']:get(k,v,pl).resize((540,960),Image.Resampling.LANCZOS).save(web/f'{COPY[k][1]}_{v}_{pl}.jpg',quality=88)
note=json.loads((R/'notes.json').read_text()) if (R/'notes.json').exists() else {}
h=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Top 1 Percent Covers</title>',
'<style>body{background:#12171f;color:#e8eef4;font:16px/1.45 -apple-system,Helvetica,Arial,sans-serif;margin:0;padding:24px}h1{font-size:26px;margin:0 0 6px}h2{color:#ffd600;font-size:21px;margin:34px 0 4px}p{margin:4px 0 10px;color:#b9c6d1;max-width:1100px}.row{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}.c{background:#1b232e;border-radius:10px;padding:10px}.c b{display:block;margin-bottom:2px}.c small{display:block;color:#9fb0bf;min-height:38px;margin-bottom:6px}.pair{display:flex;gap:6px}.pair figure{margin:0;flex:1}.pair img{width:100%;border-radius:6px;display:block}figcaption{font-size:11px;color:#8fa1b1;text-align:center;margin-top:2px}ol{color:#b9c6d1;max-width:1100px}@media(max-width:1100px){.row{grid-template-columns:repeat(2,1fr)}}</style>',
f'<h1>Top 1% Shorts: cover choices ({len(keys)} shorts, {5*len(keys)} choices)</h1>',
'<p>Each choice is shown in both layouts: Instagram, TikTok and Facebook on the left, YouTube on the right. They count as one choice. Reply with one letter per short, for example "1 C, 2 A, 3 D". Click any picture to open it larger.</p>',
'<h2 style="color:#fff">What I decided (overrule anything)</h2><ol>'+''.join(f'<li>{html.escape(t)}</li>' for t in note.get('decided',[]))+'</ol>']
for r,k in enumerate(keys):
 h.append(f'<h2>Short {r+1}: {html.escape(COPY[k][2])}</h2><p>Cover copy: {html.escape(BADGES[k])} / {html.escape(" ".join(COPY[k][0]))}</p><div class="row">')
 for v in 'ABCDE':
  sub={'A':f'Real pool photo ({POOL[k]})','B':f'Real studio photo ({STUDIO[k]}) on an AI scene, white outline'}.get(v) or note.get('designs',{}).get(k,{}).get(v,'AI design')
  h.append(f'<div class="c"><b>{kinds[v]}</b><small>{html.escape(sub)}</small><div class="pair">'+''.join(f'<figure><a href="web/{COPY[k][1]}_{v}_{pl}.jpg" target="_blank"><img loading="lazy" src="web/{COPY[k][1]}_{v}_{pl}.jpg"></a><figcaption>{"Instagram" if pl=="instagram" else "YouTube"}</figcaption></figure>' for pl in ['instagram','youtube'])+'</div></div>')
 h.append('</div>')
(R/'index.html').write_text('\n'.join(h));print('review built',len(keys),'shorts')
