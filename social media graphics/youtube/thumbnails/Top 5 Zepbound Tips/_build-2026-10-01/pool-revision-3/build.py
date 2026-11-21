#!/usr/bin/env python3
"""Three new real portraits in the original RO-12 pool design. No generation."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np,json,hashlib
HERE=Path(__file__).resolve().parent
OLD=HERE.parent
ROOT=OLD.parents[4]
PH=ROOT/'photos/finalized social media photos'
W,H=1280,720
FONT='/Users/danielrose/Library/Fonts/Manrope.ttf'
WHITE=(255,255,250); YELLOW=(255,212,40); BLACK=(8,11,18)

def font(size):
 f=ImageFont.truetype(FONT,size);f.set_variation_by_name('ExtraBold');return f

def subject(src,mask,bottom):
 im=Image.open(src).convert('RGBA')
 if mask:
  a=Image.open(mask).convert('L').resize(im.size).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.65));im.putalpha(a)
 im=im.crop((0,0,im.width,round(im.height*bottom)))
 bbox=im.getchannel('A').point(lambda v:255 if v>127 else 0).getbbox()
 return im.crop(bbox)

def bg():
 im=ImageOps.fit(Image.open(OLD/'assets/pool-bg.png').convert('RGB'),(W,H))
 ar=np.asarray(im,dtype=float);x=np.arange(W)[None,:];y=np.arange(H)[:,None]
 a=np.broadcast_to(193*np.maximum(0,1-x/820)**1.25,(H,W)).copy()
 a+=35*np.maximum(0,1-y/400)**1.4;a=np.clip(a,0,235)/255
 return Image.fromarray((ar*(1-a[:,:,None])+np.array(BLACK)[None,None,:]*a[:,:,None]).astype('uint8')).convert('RGBA')

# Three relaxed studio sources, including one jeans photo. No raised arms or flexing.
# Blue-38 is cropped at the waistband seam before the brief leg openings.
choices=[('A','Jeans: relaxed hands','studio-white-42',PH/'_cutouts/studio-white-42_CUTOUT.png',None,.885),
         ('B','Studio: arms at sides','studio-blue-127',PH/'_cutouts/studio-blue-127_CUTOUT.png',None,.86),
         ('C','Studio: relaxed stance','studio-blue-38',PH/'_cutouts/studio-blue-38_CUTOUT.png',None,.71)]

rows=[]
for ident,label,source,path,mask,bottom in choices:
 canvas=bg();p=subject(path,mask,bottom)
 scale=min(540/p.width,700/p.height);p=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS)
 x=W-24-p.width;y=H-p.height
 layer=Image.new('RGBA',(W,H));layer.alpha_composite(p,(x,y));a=layer.getchannel('A')
 sh=Image.new('RGBA',(W,H));sh.putalpha(a.filter(ImageFilter.GaussianBlur(12)).point(lambda v:int(v*.6)));canvas.alpha_composite(sh);canvas.alpha_composite(layer)
 d=ImageDraw.Draw(canvas);d.rectangle((42,70,52,294),fill=YELLOW);boxes=[]
 for text,yy,start,color in [('ZEPBOUND',79,119,WHITE),('5 TIPS',191,166,YELLOW)]:
  size=start;f=font(size)
  while d.textbbox((0,0),text,font=f)[2]>545:size-=1;f=font(size)
  b=d.textbbox((0,0),text,font=f);tw=b[2]-b[0];hh=b[3]-b[1]
  d.text((75-b[0],yy-b[1]+5),text,font=f,fill=(0,0,0,150),stroke_width=2,stroke_fill=(0,0,0,160))
  d.text((72-b[0],yy-b[1]),text,font=f,fill=color)
  boxes.append((67,yy-5,72+tw+7,yy+hh+8))
 out=HERE/f'ro12-pool-R3-{ident}.jpg';canvas.convert('RGB').save(out,quality=95,subsampling=0)
 rendered=Image.open(out);rendered.resize((320,180),Image.Resampling.LANCZOS).save(HERE/f'ro12-pool-R3-{ident}-feed.jpg',quality=95)
 ma=np.asarray(a)>127;clear=[]
 for x0,y0,x1,y1 in boxes:
  cols=np.where(ma[y0:y1].any(0))[0];gap=int(cols.min()-x1) if len(cols) else 9999;assert gap>=25,(ident,gap);clear.append(gap)
 ys,xs=np.where(ma);assert ys.min()>=15 and xs.max()<=W-20
 assert rendered.size==(1280,720) and rendered.format=='JPEG' and out.stat().st_size<2000000
 rows.append(dict(id=ident,label=label,source=source,source_file=str(path),crop_bottom_fraction=bottom,file=out.name,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),text_clearance_px=min(clear),headroom_px=int(ys.min()),portrait_pixels='Real source, resized uniformly; no physique or face alteration',text_boxes=boxes))

sheet=Image.new('RGB',(2024,538),'#eef0f4');d=ImageDraw.Draw(sheet)
d.text((30,20),'TOP 5 ZEPBOUND TIPS | STUDIO PHOTO REVISION',font=font(32),fill=BLACK)
d.text((30,69),'Three relaxed studio photos. Same pool design. Pick A, B or C.',font=font(23),fill=BLACK)
for i,r in enumerate(rows):
 xx=30+i*668
 d.text((xx,126),f"{r['id']}. {r['label']}",font=font(21),fill=BLACK)
 sheet.paste(Image.open(HERE/r['file']).resize((640,360),Image.Resampling.LANCZOS),(xx,164))
sheet.save(HERE/'REVIEW_ro12_pool_R3.jpg',quality=95,subsampling=0)
(HERE/'manifest-QC.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
