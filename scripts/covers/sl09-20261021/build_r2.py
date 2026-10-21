#!/usr/bin/env python3
"""SL-09 covers round 2 (Dan, 2026-10-21; prompts_r2.py has his words). Three new designs for short 1 and short 4, each on a new
AI image of Dan as a sleep-deprived zombie: F the yellow band on top (C's type), G the headline at the bottom (D's type), H the left
stack with the white frame on short 1 (A's type) and the two panels on short 4 (E's type: Dan at the table above, the spiky sleep
chart below). Short 3 E keeps its top panel and gets the new bottom picture of Dan wired awake in bed. Records go into manifest.json
beside round 1, so qc.py measures them the same way."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build as b
from build import R,W,H,COPY,WHITE
GEN=R/'assets/gen'
def gen(name,size=(W,H),centering=(0.5,0.5)):
 p=GEN/f'{name}.png';return ImageOps.fit(Image.open(p).convert('RGB'),size,method=Image.Resampling.LANCZOS,centering=centering).convert('RGBA'),p
def panels(k,top=None,bottom=None):
 """E layout with either panel replaced by a new picture fitted to the panel's exact size; the other panel stays as round 1 cut it."""
 im,gp=b.plate(k,'e');s0,s1=b.strip(im);c=(s0+s1)//2;half=max(185,(s1-s0)//2+24);gap=34
 out=b.open_strip(im,s0,s1,c-half,c+half);used=[str(gp)]
 if top:
  t,tp=gen(top,(W,c-half-gap),(0.5,0.35));out.alpha_composite(t,(0,0));used.append(str(tp))
 if bottom:
  hb=H-(c+half+gap);t,tp=gen(bottom,(W,hb),(0.5,0.4));out.alpha_composite(t,(0,c+half+gap));used.append(str(tp))
 return out,(c-half,c+half),used
def clear_top(im,need):
 """Slide the picture down until its first busy row (the top of the plates) sits below the type, filling above with the plain top colour."""
 import numpy as np
 a=np.asarray(im.convert('L'),dtype=np.float32);busy=np.where(a.std(axis=1)>22)[0];top=int(busy.min()) if len(busy) else H
 if top>=need:return im,0
 sh=need-top;col=tuple(int(v) for v in np.asarray(im.convert('RGB'))[:40].reshape(-1,3).mean(axis=0))
 out=Image.new('RGBA',(W,H),col+(255,));out.alpha_composite(im.crop((0,0,W,H-sh)),(0,sh));return out,sh
def make(k,v,platform):
 ig=platform=='instagram';tm=Image.new('L',(W,H));blank=lambda:(Image.new('RGBA',(W,H)),Image.new('L',(W,H)))
 if (k,v) in [('s1','F'),('s4','F')]:
  im,gp=gen(f'{k}-f');bb=b.lay_C(*blank(),k,ig);im,shift=b.drop_below(im,bb+50);info=dict(plate=str(gp),picture_shift=shift)
  pic=im.copy();b.lay_C(im,tm,k,ig)
 elif (k,v) in [('s1','G'),('s4','G')]:
  im,gp=gen(f'{k}-g');info=dict(plate=str(gp));pic=im.copy();b.lay_D(im,tm,k,ig)
 elif (k,v)==('s1','H'):
  im,gp=gen('s1-h');bottom=b.lay_A(*blank(),k,ig);im,shift=clear_top(im,bottom+40)
  b.ramp(im,0,760 if ig else 560,225);info=dict(plate=str(gp),picture_shift=shift);pic=im.copy();b.lay_A(im,tm,k,ig)
  ImageDraw.Draw(im).rounded_rectangle((24,24,W-25,H-25),radius=22,outline=WHITE,width=4)
 elif (k,v)==('s4','H'):
  im,band,used=panels('s4',top='s4-h');info=dict(plates=used,band=list(band));pic=im.copy();b.lay_E(im,tm,k,ig,band)
 elif (k,v)==('s3','E'):
  im,band,used=panels('s3',bottom='s3-e2');info=dict(plates=used,band=list(band));pic=im.copy();b.lay_E(im,tm,k,ig,band)
 else:raise ValueError((k,v))
 return im,tm,pic,info
ROUND2=[('s1','F'),('s1','G'),('s1','H'),('s3','E'),('s4','F'),('s4','G'),('s4','H')]
KIND2={'F':'AI image of Dan, design 1','G':'AI image of Dan, design 2','H':'AI image of Dan, design 3','E':'Codex two panels, Dan below'}
if __name__=='__main__':
 mp=R/'manifest.json';m=json.loads(mp.read_text());rec=[r for r in m['outputs'] if (r['short'],r['variant']) not in ROUND2]
 for k,v in ROUND2:
  for platform in ['instagram','youtube']:
   im,tm,pic,info=make(k,v,platform);slug=f'{COPY[k][1]}_cover-{v}';p=R/platform/(slug+'.png')
   im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'));pic.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
   ph=R/'phone'/platform;Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(ph/(slug+'.jpg'),quality=95)
   rec.append(dict(short=k,variant=v,platform=platform,path=str(p),sha256=b.sha(p),kind=KIND2[v],round=2,has_person=True,
    copy={'badge':b.BADGES[k],'headline':COPY[k][0]},**info))
 m['outputs']=rec;m['status']='round 2: awaiting Dan picks for shorts 1, 3 and 4';mp.write_text(json.dumps(m,indent=1)+'\n');print('built',len(ROUND2)*2)
