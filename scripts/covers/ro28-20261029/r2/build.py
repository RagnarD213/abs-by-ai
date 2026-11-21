from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np
import json,subprocess,hashlib
from scipy.ndimage import distance_transform_edt
HERE=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Why Zepbound Improves Your Health Even If Youre Ripped/_build-2026-10-29/r2')
OUT=HERE.parents[1]
W,H=1280,720
SUP=Path('/System/Library/Fonts/Supplemental')
PM=Path.home()/'.cache/absbyai/personmask/personmask'
FONT={'A1':(SUP/'DIN Condensed Bold.ttf',0),'A2':(SUP/'Impact.ttf',0),'A3':(Path('/System/Library/Fonts/Avenir Next Condensed.ttc'),8)}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(k,size):
 path,index=FONT[k];return ImageFont.truetype(str(path),size,index=index)
def put(im,tm,k,t,x,y,size,maxw,col):
 while True:
  font=f(k,size);b=font.getbbox(t);tw=b[2]-b[0];th=b[3]-b[1]
  if tw<=maxw:break
  size-=1
 d=ImageDraw.Draw(im);md=ImageDraw.Draw(tm);pos=(x-b[0],y-b[1]);d.text((pos[0]+2,pos[1]+3),t,font=font,fill='#060A10')
 d.text(pos,t,font=font,fill=col);md.text(pos,t,font=font,fill=255,stroke_width=4)
 return [x,y,x+tw,y+th]
def fade(im,right=False):
 a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[4,13,27];xs=np.linspace(0,1,W)
 alpha=np.clip((xs-.49)/.13,0,1) if right else np.clip((.47-xs)/.14,0,1)
 a[:,:,3]=(alpha*233)[None,:].astype(np.uint8)
 return Image.alpha_composite(im,Image.fromarray(a))
def build(k):
 src=HERE/'assets'/f'{k}.png';im=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
 pp=HERE/f'picture-{k}.png';im.save(pp);mp=HERE/f'person-{k}.png'
 subprocess.run([str(PM),str(pp),str(mp)],check=True,capture_output=True)
 mask=np.array(Image.open(mp).convert('L').resize((W,H)))>100
 tm=Image.new('L',(W,H));boxes=[]
 if k=='A1':
  im=fade(im);d=ImageDraw.Draw(im);d.rectangle((30,140,555,332),fill='#FFD400')
  for t,x,y,size,mw,col in [('Why',44,32,98,500,'white'),('Ripped Men',44,162,127,495,'#0D1116'),('Should Take',44,365,101,500,'white'),('Zepbound',44,497,133,500,'#FFD400')]:boxes.append(put(im,tm,k,t,x,y,size,mw,col))
 elif k=='A2':
  im=fade(im,True)
  for t,x,y,size,mw,col in [('Why',763,61,96,475,'#FFFFFF'),('Ripped Men',763,185,99,475,'#50E2EA'),('Should Take',763,326,86,475,'#FFFFFF'),('Zepbound',763,470,106,475,'#FFFFFF')]:boxes.append(put(im,tm,k,t,x,y,size,mw,col))
  ImageDraw.Draw(im).rectangle((763,617,1235,627),fill='#50E2EA')
 elif k=='A3':
  ImageDraw.Draw(im).rectangle((0,0,W,215),fill='#FFD400')
  for t,y,size,col in [('Why Ripped Men Should',12,95,'#09141F'),('Take Zepbound',118,91,'#9D1C12')]:
   bb=f(k,size).getbbox(t);xx=(W-(bb[2]-bb[0]))//2
   boxes.append(put(im,tm,k,t,xx,y,size,1200,col))
 dest=OUT/f'RO28-R2-{k}.jpg';im.convert('RGB').save(dest,quality=96,subsampling=0);tm.save(HERE/f'text-{k}.png')
 text=np.array(tm)>0;clear=float(distance_transform_edt(~mask)[text].min());overlap=int((text&mask).sum())
 result={'choice':k,'file':dest.name,'sha256':sha(dest),'source_sha256':sha(src),'dimensions':[W,H],'bytes':dest.stat().st_size,'minimum_person_text_clearance_px':round(clear,2),'overlap_pixels':overlap,'text_boxes':boxes,'copy':'Why Ripped Men Should Take Zepbound','pass':clear>=20 and overlap==0 and dest.stat().st_size<2000000}
 print(json.dumps(result));return result
if __name__=='__main__':
 import sys
 keys=sys.argv[1:] or ['A1','A2','A3'];res=[build(k) for k in keys]
 if keys==['A1','A2','A3']:
  (HERE/'qc.json').write_text(json.dumps(res,indent=2)+'\n')
  sheet=Image.new('RGB',(1640,1120),'#101923');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),30)
  d.text((28,19),'Why Ripped Men Should Take Zepbound: Three Designs',font=font,fill='white')
  labels={'A1':'1: Confident Half-Smile','A2':'2: Playful Surprise','A3':'3: Broad Smile'}
  for i,r in enumerate(res):
   x=30+i*810 if i<2 else 435;y=78 if i<2 else 600
   d.text((x,y),labels[r['choice']],font=font,fill='#FFD400')
   sheet.paste(Image.open(OUT/r['file']).resize((770,433),Image.Resampling.LANCZOS),(x,y+44))
  sheet.save(OUT/'REVIEW-three-revised-thumbnails.jpg',quality=94)
