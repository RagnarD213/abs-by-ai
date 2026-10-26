#!/usr/bin/env python3
"""Three full-bleed real squat screenshot designs, with matched IG/YT copy.
Warm graded photographic retouches come from the Codex subscription helper.
Only native typography and overlays are added here. Approved video is never opened for write.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np
import hashlib,json
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'Short-form video content/covers/review/ds55-five-minute-exercises-20261026/round3'
W,H=1080,1920
SUP=Path('/System/Library/Fonts/Supplemental')
FONTS={1:(SUP/'Impact.ttf',0),2:(SUP/'Futura.ttc',4),3:(SUP/'DIN Condensed Bold.ttf',0)}
COPY=['5 Minute','Home Workout']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(k,size):p,i=FONTS[k];return ImageFont.truetype(str(p),size,index=i)
def fit(k,s,size,width):
 for n in range(size,30,-1):
  f=font(k,n)
  if f.getlength(s)<=width:return f
 raise ValueError(s)
def fade(im,mask,y0,y1,maximum,top=False):
 a=np.zeros((H,W,4),dtype=np.uint8);a[:,:,:3]=[9,19,25]
 for y in range(H):
  t=(y1-y)/(y1-y0) if top else (y-y0)/(y1-y0)
  a[y,:,3]=round(maximum*max(0,min(1,t)))
 im.alpha_composite(Image.fromarray(a));mask.paste(Image.fromarray(a[:,:,3]))
def text(im,mask,xy,s,f,col,stroke=0):
 d=ImageDraw.Draw(im);md=ImageDraw.Draw(mask);box=d.textbbox(xy,s,font=f,anchor='lt',stroke_width=stroke)
 d.text(xy,s,font=f,fill=col,anchor='lt',stroke_width=stroke,stroke_fill='#10222E');md.text(xy,s,font=f,fill=255,anchor='lt',stroke_width=stroke)
 return list(box)
def build():
 rows=[]
 for k in [1,2,3]:
  src=OUT/'sources'/f'{k}-retouched.png';picture=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
  picture.save(OUT/'sources'/f'{k}-picture.png')
  for platform in ['instagram','youtube']:
   ig=platform=='instagram';im=picture.convert('RGBA');mask=Image.new('L',(W,H));gm=Image.new('L',(W,H));bounds=[]
   if k==1:
    y=1350 if ig else 1580
    fade(im,gm,y-130,y+245,228)
    for i,s in enumerate(COPY):bounds.append(text(im,mask,(62,y+i*132),s,fit(k,s,145,950),['#FFF4DD','#FFA553'][i],3))
   elif k==2:
    y=265 if ig else 95
    fade(im,gm,0,600 if ig else 450,170,top=True)
    d=ImageDraw.Draw(im);d.line((64,y-25,1010,y-25),fill='#58DCE2',width=9);ImageDraw.Draw(gm).line((64,y-25,1010,y-25),fill=255,width=9)
    for i,s in enumerate(COPY):bounds.append(text(im,mask,(62,y+i*165),s,fit(k,s,160 if i==0 else 127,950),['#FFF4DD','#69E2E8'][i],2))
   else:
    y=1190 if ig else 1400
    fade(im,gm,y-20,y+420,218)
    bounds.append(text(im,mask,(50,y),'5',font(k,400),'#FFD951',2))
    bounds.append(text(im,mask,(305,y+90),'Minute',font(k,118),'#FFECC5',1))
    bounds.append(text(im,mask,(305,y+244),'Home Workout',fit(k,'Home Workout',118,715),'#FFFFFF',1))
   assert all(25<=b[0]<b[2]<=1055 for b in bounds)
   assert all((240 if ig else 55)<=b[1]<b[3]<(1630 if ig else 1875) for b in bounds),bounds
   p=OUT/platform/f'five-minute-cover-{k}.png';p.parent.mkdir(exist_ok=True)
   im.convert('RGB').save(p);picture.save(p.with_name(p.stem+'.picture.png'));mask.save(p.with_name(p.stem+'.text-mask.png'));gm.save(p.with_name(p.stem+'.graphic-mask.png'))
   if not ig:im.convert('RGB').save(p.with_suffix('.jpg'),quality=93)
   rows.append(dict(choice=k,platform=platform,path=str(p),sha256=sha(p),source=str(src),source_sha256=sha(src),full_bleed=True,rendered_crop='Same full9:16 photograph, no containment panel',text_bounds=bounds,source_graded_clip_time=[.5,1.,2.][k-1]))
 (OUT/'manifest.json').write_text(json.dumps({'status':'awaiting Dan review','headline':COPY,'outputs':rows},indent=2))
 sh=Image.new('RGB',(1260,1600),'#111926');d=ImageDraw.Draw(sh);f=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),28)
 for x in rows:
  xx=(x['choice']-1)*420;yy=0 if x['platform']=='instagram' else 800;d.text((xx+10,yy+10),str(x['choice'])+' / '+x['platform'].title(),font=f,fill='white')
  img=Image.open(x['path']);img.thumbnail((400,720));sh.paste(img,(xx+10,yy+58))
 sh.save(OUT/'three-full-screen-cover-choices.jpg',quality=95)
 print('Built six full-screen covers')
if __name__=='__main__':build()
