#!/usr/bin/env python3
"""Round 2 (Dan, 2026-10-08): short 1 option E with the clock at 2:00 (E2), short 6 retitled with a new design (F). Reuses build.py."""
import importlib.util,json
from pathlib import Path
from PIL import Image,ImageDraw
spec=importlib.util.spec_from_file_location('b',Path(__file__).with_name('build.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
R=b.R;rows=[]
b.COPY[6]=('MEAL PREP',['MAKE AI CALORIE','TRACKING ACCURATE'],'make-ai-calorie-tracking-accurate')
def plate_from(path,gradient,shrink=None):
 full=b.ImageOps.fit(Image.open(path).convert('RGB'),(b.W,b.H),method=Image.Resampling.LANCZOS)
 if shrink:  # sit the plate lower so the photographing phone clears the Instagram headline
  bg=full.filter(b.ImageFilter.GaussianBlur(40)).point(lambda q:int(q*0.45));sm=full.resize((round(b.W*shrink),round(b.H*shrink)),Image.Resampling.LANCZOS)
  m=Image.new('L',sm.size,255);md=ImageDraw.Draw(m)
  for i in range(60):md.rectangle((i,i,sm.width-i,sm.height-i),outline=int(255*i/60))
  bg.paste(sm,((b.W-sm.width)//2,b.H-sm.height-8),m);full=bg
 im=full.convert('RGBA')
 if gradient:
  import numpy as np;a=np.zeros((b.H,b.W,4),np.uint8);a[:,:,:3]=[4,7,12]
  for y in range(b.H):a[y,:,3]=int(205*max(0,1-y/820)**0.85)
  im.alpha_composite(Image.fromarray(a))
 return im
for n,v,src,kind,grad,layout in [(1,'E2',R/'assets/rev2/S1-y2.png','Codex design 2, clock at 2:00',False,'E'),(6,'F',R/'assets/rev2/S6-n1.png','Codex design (phone photo + typed line)',True,'D')]:
 for pl in ['instagram','youtube']:
  out=R/pl;slug=f'daily-salad-short{n}_{b.COPY[n][2]}_cover-{v}';p=out/(slug+'.png');tm=Image.new('L',(b.W,b.H))
  im=plate_from(src,grad,0.87 if (n==6 and pl=='instagram') else None);accent=b.draw_copy(im,tm,n,pl,layout);d=ImageDraw.Draw(im)
  if layout!='E':d.rounded_rectangle((24,24,b.W-25,b.H-25),radius=22,outline=(255,255,250),width=4);d.line((45,1872,1035,1872),fill=accent,width=6)
  im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
  if pl=='instagram':im.convert('RGB').crop((0,240,1080,1680)).save(R/'grid-crops'/(slug+'.png'))
  rows.append(dict(short=n,variant=v,platform=pl,path=str(p),sha256=b.sha(p),kind=kind,plate=str(src),plate_sha256=b.sha(src),copy={'badge':b.COPY[n][0],'headline':b.COPY[n][1]}))
(R/'manifest-rev2.json').write_text(json.dumps({'status':'awaiting Dan approval','outputs':rows},indent=1)+'\n');print('built',len(rows))
