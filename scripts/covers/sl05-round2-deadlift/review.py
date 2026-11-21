#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,html
R=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/sl05-covers-20261001/round2-deadlift'
rows=json.loads((R/'manifest.json').read_text())['outputs'];F='/System/Library/Fonts/Supplemental/Arial Bold.ttf';f=lambda s:ImageFont.truetype(F,s)
def path(n,v,p):return Path(next(x['path'] for x in rows if x['short']==n and x['variant']==v and x['platform']==p))
for p in ['instagram','youtube']:
 im=Image.new('RGB',(1250,2940),(16,21,29));d=ImageDraw.Draw(im)
 d.text((24,18),'SL-05 R2: DEADLIFT WARNING COVERS',font=f(40),fill='white');d.text((24,73),p.title()+' | One new image, two designs per short | Choose A or B',font=f(26),fill=(190,201,214))
 for row,n in enumerate(range(1,6)):
  y=128+row*555;d.text((24,y),f'SHORT {n}',font=f(30),fill='white')
  for col,v in enumerate('AB'):
   x=24+col*610;d.text((x,y+40),'A: Full color + red X' if v=='A' else 'B: Monochrome + prohibition',font=f(24),fill=(218,224,233));a=Image.open(path(n,v,p));a=a.crop((0,240,1080,1680)) if p=='instagram' else a;a.thumbnail((570,480));im.paste(a,(x,y+76))
 im.save(R/f'REVIEW_sl05_R2_{p}.jpg',quality=96)
for n in range(1,6):
 im=Image.new('RGB',(1180,1070),(16,21,29));d=ImageDraw.Draw(im);d.text((24,15),f'SHORT {n}: R2 DEADLIFT DESIGNS',font=f(37),fill='white')
 for i,v in enumerate('AB'):
  x=24+i*580;d.text((x,72),'A: Full color + red X' if v=='A' else 'B: Monochrome + prohibition',font=f(24),fill='white')
  for j,p in enumerate(['instagram','youtube']):
   xx=x+j*278;d.text((xx,111),p.title(),font=f(21),fill=(190,201,214));im.paste(Image.open(path(n,v,p)).resize((270,480),Image.Resampling.LANCZOS),(xx,143))
  d.text((x,646),'Instagram grid crop',font=f(21),fill=(190,201,214));im.paste(Image.open(path(n,v,'instagram')).crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS),(x,682))
 im.save(R/f'REVIEW_short{n}_R2_paired.jpg',quality=95)
page=['<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SL-05 R2 deadlift cover review</title><style>body{background:#10151d;color:#f5f7fa;font:17px Arial;margin:0;padding:24px}main{max-width:1240px;margin:auto}h1{font-size:32px}a{color:#8be2ff}nav{display:flex;gap:20px;flex-wrap:wrap}section{margin:44px 0}img.sheet{width:100%;max-width:1180px}.options{display:grid;grid-template-columns:1fr 1fr;gap:24px}.pair{display:flex;gap:12px}.pair a{width:50%}.pair img{width:100%}small{color:#bac7d5}@media(max-width:750px){.options{grid-template-columns:1fr}}</style></head><body><main><h1>SL-05 R2: deadlift warning covers</h1><p>Five new AI powerlifter photographs. Two designs per short, each with Instagram and YouTube layouts. A: full-color scene with a large red X. B: monochrome scene with a red prohibition mark.</p><h2>What I decided (overrule anything)</h2><p>The action now leads: straining face, thick powerlifter build, heavy bar and visible grip. The approved headline copy stays the same. Warning marks sit over the torso, clear of the face. The five new photographs use the approved video\'s powerlifter frame as the visual reference. Instagram keeps the athlete and bar within its profile crop.</p><p>Reply with five picks, such as 1A, 2B, 3A, 4B, 5A. Nothing exported as final, uploaded or scheduled.</p><nav>'+''.join(f'<a href="#short{n}">Short {n}</a>' for n in range(1,6))+'<a href="REVIEW_sl05_R2_instagram.jpg">Instagram grid review</a><a href="REVIEW_sl05_R2_youtube.jpg">YouTube review</a></nav>']
for n in range(1,6):
 page.append(f'<section id="short{n}"><h2>Short {n}</h2><div class="options">')
 for v in 'AB':
  page.append(f'<article><h3>{v}: '+('Full color + red X' if v=='A' else 'Monochrome + prohibition')+'</h3><small>Instagram | YouTube</small><div class="pair">')
  for p in ['instagram','youtube']:
   url=path(n,v,p).relative_to(R).as_posix();page.append(f'<a href="{html.escape(url)}" target="_blank"><img src="{html.escape(url)}" alt="Short {n}, R2 {v}, {p}"></a>')
  page.append('</div></article>')
 page.append(f'</div><p><a href="REVIEW_short{n}_R2_paired.jpg">View both layouts and actual Instagram grid crops</a></p><img class="sheet" src="REVIEW_short{n}_R2_paired.jpg" alt="Short {n} paired layout and grid check"></section>')
page.append('</main></body></html>');(R/'index.html').write_text(''.join(page));print('R2 gallery and two review sheets ready.')
