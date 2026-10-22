#!/usr/bin/env python3
"""SL-15 covers round 2 (Dan, 2026-10-22): "For short number one, I want two new designs: two side-by-side comparisons of two
different poses of me, pale versus tan. Use the same comparisons that we used with the spray tanning video." Short 2 is locked on C.
The RO-19 film's real pairs (gfx P01 and P04, `/Volumes/Extreme/_edit_work/ro19/photos/`), with the film's own chips:
  F  P01 double biceps (pale_intro / tan_125): Impact headline on top, two framed cards side by side, chips under each, charcoal
     field with a bronze glow.
  G  P04 arms down (pale3_down, the untinted original / tan2_down): the two photos edge to edge as one split strip with a white
     divider, chips under each half, DIN Condensed headline below on black, amber rules.
Real photos only, never redrawn; all type set in code. Records go into manifest.json beside round 1, so qc.py measures them."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build as b
from build import R,W,H,COPY,WHITE,INK,IMPACT,DIN,ARIAL,font,fit,common,text,box
PH=Path('/Volumes/Extreme/_edit_work/ro19/photos')
AMBER=(255,170,60);GREY=(196,204,214)
# crop boxes (x0, y0, x1, y1) in each source, measured on a grid with Apple Vision face boxes (2026-10-22): hair whole, fists
# whole, both halves the same body size; P04 halves keep the film's crops (same box on the untinted pale original).
PAIRS={'F':dict(pale=('pale_intro.jpg',(179,100,2829,3633)),tan=('tan_125.jpg',(147,0,2722,3433)),film='P01'),
       'G':dict(pale=('pale3_down.jpg',588),tan=('tan2_down.jpg',640),film='P04')}   # G: face centre x; full height, width from the strip's aspect
CHIPS=('Before The Tan','After The Tan')
def photo(name,crop,size):
 p=PH/name;return Image.open(p).convert('RGB').crop(crop).resize(size,Image.Resampling.LANCZOS).convert('RGBA'),dict(source=str(p),source_sha256=b.sha(p),source_crop=list(crop))
def chip(canvas,mask,cx,y,label,fill,ink):
 f=font(ARIAL,34);bb=f.getbbox(label);w=bb[2]-bb[0]+52
 box(canvas,mask,(cx-w//2,y,cx+w//2,y+60),fill,30);text(canvas,mask,(cx,y+12),label,f,ink,anchor='ma');return y+60
def field(top_col,bot_col,glow=None):
 a=np.zeros((H,W,3),np.float32);t=np.linspace(0,1,H)[:,None,None];a[:]=np.array(top_col)*(1-t)+np.array(bot_col)*t
 if glow:
  yy,xx=np.mgrid[0:H,0:W];gx,gy,r,col=glow;d=np.clip(1-np.hypot(xx-gx,yy-gy)/r,0,1)[...,None]**1.6;a=a+d*np.array(col)
 return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert('RGBA')
def make_F(k,ig):
 im=field((14,16,22),(8,9,12),(W//2,1000,900,(70,40,10)));tm=Image.new('L',(W,H));lines=COPY[k][0]
 top=262 if ig else 330
 f=common(lines,IMPACT,140,980,6);y=top+62
 cy=y+2*round(f.size*1.0)+70;cw,chh=500,667;gap=24;x0=(W-2*cw-gap)//2;infos={}
 for j,side in enumerate(['pale','tan']):
  name,crop=PAIRS['F'][side];ph,info=photo(name,crop,(cw,chh));infos[side]=info;x=x0+j*(cw+gap)
  sh=Image.new('RGBA',(cw+40,chh+40),(0,0,0,0));ImageDraw.Draw(sh).rounded_rectangle((20,24,cw+20,chh+24),radius=22,fill=(0,0,0,150))
  im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)),(x-20,cy-20))
  m=Image.new('L',(cw,chh));ImageDraw.Draw(m).rounded_rectangle((0,0,cw-1,chh-1),radius=20,fill=255);ph.putalpha(m)
  im.alpha_composite(ph,(x,cy));ImageDraw.Draw(im).rounded_rectangle((x-3,cy-3,x+cw+2,cy+chh+2),radius=22,outline=WHITE if j==0 else AMBER,width=6)
 pic=im.copy()   # the picture layer for qc: cards only, before any type
 fb=font(ARIAL,38);text(im,tm,(W//2,top),b.BADGES[k],fb,AMBER,3,anchor='ma')
 for i,ln in enumerate(lines):text(im,tm,(W//2,y+i*round(f.size*1.0)),ln,f,WHITE if i==0 else AMBER,6,anchor='ma')
 for j in range(2):chip(im,tm,x0+j*(cw+gap)+cw//2,cy+chh+40,CHIPS[j],GREY if j==0 else AMBER,INK)
 return im,tm,pic,dict(pair=PAIRS['F']['film'],pale=infos['pale'],tan=infos['tan'])
def make_G(k,ig):
 im=Image.new('RGBA',(W,H),(6,7,9,255));tm=Image.new('L',(W,H));lines=COPY[k][0]
 sy=250 if ig else 110;hw,hh=(540,780) if ig else (540,900);infos={}
 for j,side in enumerate(['pale','tan']):
  name,cx=PAIRS['G'][side];cw=round(1500*hw/hh);x0=max(0,min(cx-cw//2,1200-cw))
  ph,info=photo(name,(x0,0,x0+cw,1500),(hw,hh));infos[side]=info;im.alpha_composite(ph,(j*hw,sy))
 d=ImageDraw.Draw(im);d.rectangle((W//2-4,sy,W//2+4,sy+hh),fill=WHITE);d.rectangle((0,sy+hh,W,sy+hh+10),fill=AMBER)
 pic=im.copy();y=sy+hh+34
 for j in range(2):chip(im,tm,j*hw+hw//2,y,CHIPS[j],GREY if j==0 else AMBER,INK)
 y+=60+(36 if ig else 48);fb=font(ARIAL,36);text(im,tm,(W//2,y),b.BADGES[k],fb,AMBER,anchor='ma');y+=56
 f=common(lines,DIN,170,1000);step=round(f.size*0.95)
 for i,ln in enumerate(lines):text(im,tm,(W//2,y+i*step),ln,f,WHITE if i==0 else AMBER,anchor='ma')
 return im,tm,pic,dict(pair=PAIRS['G']['film'],pale=infos['pale'],tan=infos['tan'])
ROUND2=[('s1','F'),('s1','G')]
KIND2={'F':'Real pale vs tan pair (film P01), cards','G':'Real pale vs tan pair (film P04), split strip'}
if __name__=='__main__':
 mp=R/'manifest.json';m=json.loads(mp.read_text());rec=[r for r in m['outputs'] if (r['short'],r['variant']) not in ROUND2]
 for k,v in ROUND2:
  for platform in ['instagram','youtube']:
   ig=platform=='instagram';im,tm,pic,info=(make_F if v=='F' else make_G)(k,ig);slug=f'{COPY[k][1]}_cover-{v}';p=R/platform/(slug+'.png')
   im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'));pic.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
   ph=R/'phone'/platform;Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(ph/(slug+'.jpg'),quality=95)
   rec.append(dict(short=k,variant=v,platform=platform,path=str(p),sha256=b.sha(p),kind=KIND2[v],round=2,has_person=True,
    copy={'badge':b.BADGES[k],'headline':COPY[k][0],'chips':list(CHIPS)},**info))
 m['outputs']=rec;m['status']='round 2: short 1 F/G awaiting Dan pick; short 2 C picked';mp.write_text(json.dumps(m,indent=1)+'\n');print('built',len(ROUND2)*2)
