#!/usr/bin/env python3
"""Three revised covers from real exercise imagery. Shared IG/YT config and copy.
Photo crops derive from the approved short2/short4 real-photo cover builders.
The squat enhancement is composited over torso only; real face/background stay original.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import hashlib,json,subprocess,tempfile
import numpy as np
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'Short-form video content/covers/review/ds55-five-minute-exercises-20261026/round2'
W,H=1080,1920
SUP=Path('/System/Library/Fonts/Supplemental')
FONTS={1:(SUP/'Impact.ttf',0),2:(SUP/'Futura.ttc',4),3:(SUP/'DIN Condensed Bold.ttf',0)}
COPY=['5 Minute','Home Workout']
PM=Path.home()/'.cache/absbyai/personmask/personmask'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(k,size):p,i=FONTS[k];return ImageFont.truetype(str(p),size,index=i)
def fit(k,t,size,width):
 for n in range(size,30,-1):
  f=font(k,n)
  if f.getlength(t)<=width:return f
 raise ValueError(t)
def screenshot():
 a=Image.open(OUT/'sources/squat-original.png').convert('RGB')
 b=Image.open(OUT/'sources/squat-retouched.png').convert('RGB').resize(a.size,Image.Resampling.LANCZOS)
 mask=Image.new('L',a.size);d=ImageDraw.Draw(mask)
 # Torso/shoulder definition only. Entire head, face, environment and clothing remain real source pixels.
 d.polygon([(470,585),(660,620),(720,755),(680,845),(635,954),(460,961),(440,815),(442,660)],fill=255)
 mask=mask.filter(ImageFilter.GaussianBlur(17))
 c=Image.composite(b,a,mask);c.save(OUT/'sources/squat-final-real.png');mask.save(OUT/'sources/squat-retouch-mask.png')
 return c

def real_panel(name,panel_y,crop):
 src=Image.open(OUT/'sources'/name).convert('RGB');x,y,ch=crop;cw=round(ch*W/(H-panel_y))
 assert x>=0 and y>=0 and x+cw<=src.width and y+ch<=src.height
 return src.crop((x,y,x+cw,y+ch)).resize((W,H-panel_y),Image.Resampling.LANCZOS),(x,y,x+cw,y+ch)

def build():
 screenshot();rows=[]
 for k in [1,2,3]:
  for platform in ['instagram','youtube']:
   ig=platform=='instagram';bg=['#131922','#082C39','#F2EEE4'][k-1]
   im=Image.new('RGB',(W,H),bg);tm=Image.new('L',(W,H));md=ImageDraw.Draw(tm);d=ImageDraw.Draw(im)
   if k==1:
    panel=780 if ig else 620
    photo,crop=real_panel('pushup-photo.jpg',panel,(350,180,2250));im.paste(photo,(0,panel))
    y=285 if ig else 100
    d.rectangle((54,y-30,67,y+335),fill='#F74533')
    size=[190,150];spacing=173;cols=['#FFFFFF','#F74533'];anchor='lt';xx=90
   elif k==2:
    panel=690 if ig else 540
    ph=H-panel;ch=2350;cw=round(ch*W/ph);x=2100-cw//2
    photo,crop=real_panel('toetouch-photo.jpg',panel,(x,250,ch));im.paste(photo,(0,panel))
    y=277 if ig else 92
    d.polygon([(35,y-25),(1045,y-25),(1045,y+300),(35,y+335)],fill='#42D6E2')
    size=[165,120];spacing=166;cols=['#073542','#073542'];anchor='mt';xx=540
   else:
    # Full real squat photograph, contained to preserve hair, hands and feet.
    src=Image.open(OUT/'sources/squat-final-real.png').crop((140,300,960,1770))
    panel=650 if ig else 490;ph=H-panel
    scale=ph/src.height;rw=round(src.width*scale);photo=src.resize((rw,ph),Image.Resampling.LANCZOS)
    im.paste(photo,((W-rw)//2,panel));crop=[140,300,960,1770]
    y=270 if ig else 80
    d.rectangle((50,y+145,1030,y+315),fill='#ED6738')
    size=[186,160];spacing=168;cols=['#17212A','#FFFFFF'];anchor='mt';xx=540
   picture=im.copy();bounds=[]
   for i,t in enumerate(COPY):
    f=fit(k,t,size[i],920 if k!=1 else 900);yy=y+spacing*i
    box=d.textbbox((xx,yy),t,font=f,anchor=anchor)
    d.text((xx,yy),t,font=f,anchor=anchor,fill=cols[i]);md.text((xx,yy),t,font=f,anchor=anchor,fill=255)
    bounds.append(list(box))
   assert all(35<=b[0]<b[2]<=1045 for b in bounds)
   assert all((240 if ig else 60)<=b[1]<b[3]<panel-25 for b in bounds)
   path=OUT/platform/f'five-minute-cover-{k}.png';path.parent.mkdir(exist_ok=True)
   im.save(path);picture.save(path.with_name(path.stem+'.picture.png'));tm.save(path.with_name(path.stem+'.text-mask.png'))
   if not ig:im.save(path.with_suffix('.jpg'),quality=93)
   rows.append({'choice':k,'platform':platform,'path':str(path),'sha256':sha(path),'text_bounds':bounds,'picture_top':panel,'source_crop':list(crop),'source':['photo-63_FINAL_PRIMARY.jpg','photo-44_FINAL_PRIMARY.jpg','B-p258-balanced.mp4 @0.5s'][k-1],'real_photo':True,'retouch':'Subscription torso-only enhancement; original face and environment preserved' if k==3 else 'Existing finalized real shoot photograph, no new retouch'})
 (OUT/'manifest.json').write_text(json.dumps({'status':'awaiting Dan pick','copy':COPY,'outputs':rows},indent=2))
 sheet=Image.new('RGB',(3*420,2*800),'#101722');dd=ImageDraw.Draw(sheet);lf=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),28)
 for row in rows:
  x=(row['choice']-1)*420;y=0 if row['platform']=='instagram' else 800
  dd.text((x+10,y+10),str(row['choice'])+' / '+row['platform'].title(),font=lf,fill='white')
  pic=Image.open(row['path']);pic.thumbnail((400,720));sheet.paste(pic,(x+10,y+58))
 sheet.save(OUT/'three-new-cover-choices.jpg',quality=95)
 print('Built 6 covers')
if __name__=='__main__':build()
