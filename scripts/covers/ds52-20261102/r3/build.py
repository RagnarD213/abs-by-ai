#!/usr/bin/env python3
"""Three natural, heavier type treatments on the exact selected R2 design 3."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'Short-form video content/covers/review/ds52-zepbound-free-20261102';OUT=BASE/'r3';OUT.mkdir(exist_ok=True)
SUP=Path('/System/Library/Fonts/Supplemental');MAN=Path.home()/'Library/Fonts/Manrope.ttf';HEL=Path('/System/Library/Fonts/HelveticaNeue.ttc')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(name,size):
 if name=='manrope':
  f=ImageFont.truetype(str(MAN),size);f.set_variation_by_name('ExtraBold');return f
 if name=='impact':return ImageFont.truetype(str(SUP/'Impact.ttf'),size)
 return ImageFont.truetype(str(HEL),size,index=9 if name=='heavy' else 1)
def fitted(t,name,maxsize,width,height):
 for s in range(maxsize,25,-1):
  f=font(name,s);b=f.getbbox(t,anchor='lt')
  if b[2]-b[0]<=width and b[3]-b[1]<=height:return f
 raise ValueError(t)
def text(im,mask,t,name,size,x,y,width,height,color,center=False):
 f=fitted(t,name,size,width,height);d=ImageDraw.Draw(im);b=f.getbbox(t,anchor='lt');tw=b[2]-b[0];xx=round(x+(width-tw)/2) if center else x
 d.text((xx,y),t,font=f,anchor='lt',fill=color);ImageDraw.Draw(mask).text((xx,y),t,font=f,anchor='lt',fill=255)
 box=d.textbbox((xx,y),t,font=f,anchor='lt');assert box[0]>=70 and box[2]<=1010 and box[1]>=1200 and box[3]<=1750
 return {'text':t,'font':f.getname(),'font_size':f.size,'bounds':list(box),'natural_proportions':True}
rows=[]
for pf in ['instagram','youtube']:
 ig=pf=='instagram';src=BASE/f'r2/{pf}/Zepbound-Free-Design-3-{pf}.png';original=Image.open(src).convert('RGB');y=1220 if ig else 1270;bottom=1680 if ig else 1770
 for n in ['A','B','C']:
  im=original.copy();d=ImageDraw.Draw(im)
  # Exact existing panel geometry; the selected photograph and background above it are copied unchanged.
  d.rounded_rectangle((42,y-32,1038,bottom),radius=24,fill='#F2EBDD')
  for xx in range(70,1030,40):d.ellipse((xx-11,y-43,xx+11,y-21),fill='#073B2C')
  mask=Image.new('L',im.size);tx=[]
  if n=='A':
   tx.append(text(im,mask,'Why Zepbound','manrope',124,80,y+18,920,112,'#123C30',True))
   tx.append(text(im,mask,'Is Actually','manrope',96,80,y+151,920,88,'#123C30',True))
   tx.append(text(im,mask,'Free','manrope',238,80,y+248,920,183,'#12734A',True))
  elif n=='B':
   tx.append(text(im,mask,'Why Zepbound','impact',174,80,y+32,920,155,'#123C30',True))
   d.rounded_rectangle((70,y+218,1010,y+421),radius=12,fill='#123C30')
   tx.append(text(im,mask,'Is Actually Free','impact',165,88,y+247,904,156,'#FFFFFF',True))
  else:
   tx.append(text(im,mask,'Why Zepbound','heavy',173,80,y+14,920,145,'#123C30'))
   tx.append(text(im,mask,'Is Actually','bold',104,80,y+163,920,97,'#123C30'))
   tx.append(text(im,mask,'Free','heavy',257,80,y+270,920,167,'#12734A'))
  dd=OUT/pf;dd.mkdir(exist_ok=True);p=dd/f'Zepbound-Free-Text-{n}-{pf}.png';im.save(p);im.save(p.with_suffix('.jpg'),quality=95);mask.save(p.with_name(p.stem+'-text-mask.png'))
  # All changes stay in the existing receipt. No transformed text, no altered photo pixels.
  a=np.array(im);b=np.array(original);diff=np.any(a!=b,axis=2);outside=diff.copy();outside[y-43:bottom+1,42:1039]=False
  assert not outside.any();assert all(t['bounds'][3]<=(1680 if ig else 1770) for t in tx)
  assert p.with_suffix('.jpg').stat().st_size<2_000_000
  if ig:im.crop((0,240,1080,1680)).save(OUT/f'Text-{n}-profile.jpg',quality=95)
  im.resize((270,480),Image.Resampling.LANCZOS).save(OUT/f'Text-{n}-{pf}-phone.jpg',quality=95)
  rows.append({'variant':n,'platform':pf,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'jpeg_sha256':sha(p.with_suffix('.jpg')),'jpeg_bytes':p.with_suffix('.jpg').stat().st_size,'source_cover':str(src.relative_to(ROOT)),'source_sha256':sha(src),'text':tx,'changed_pixels_outside_existing_receipt':int(outside.sum()),'unchanged_above_receipt':not diff[:y-43].any(),'natural_font_proportions':True})
manifest={'status':'awaiting exact revised text pick','chosen_design':'R2 design 3, image from original X3','copy':'Why Zepbound Is Actually Free','new_generation_calls':0,'outputs':rows}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
sheet=Image.new('RGB',(1080,1330),'#121B27');d=ImageDraw.Draw(sheet);f=font('manrope',24)
for r in rows:
 i='ABC'.index(r['variant']);j=0 if r['platform']=='instagram' else 1;x=i*360;yy=j*665
 d.text((x+12,yy+15),f"{r['variant']} / {'Instagram' if j==0 else 'YouTube'}",font=f,fill='white');im=Image.open(ROOT/r['path']);im.thumbnail((328,583));sheet.paste(im,(x+16,yy+63))
sheet.save(OUT/'three-text-choices.jpg',quality=95)
profile=Image.new('RGB',(900,440),'#121B27');d=ImageDraw.Draw(profile)
for i,n in enumerate('ABC'):
 im=Image.open(OUT/f'Text-{n}-profile.jpg');im.thumbnail((280,373));profile.paste(im,(i*300+10,50));d.text((i*300+10,13),n,font=f,fill='white')
profile.save(OUT/'profile-crops.jpg',quality=95)
print('Three text variants built, six covers. No image changes outside receipt. No distorted type.')
