#!/usr/bin/env python3
"""RO-12: five concepts, five design variations each. Real portraits preserved.
Supporting backgrounds generated with built-in imagegen; no upload or schedule.
Run from any directory. Final export waits for Dan's explicit choice.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
AS=HERE/'assets'; PH=ROOT/'photos/finalized social media photos'
W,H=1280,720
IMPACT='/System/Library/Fonts/Supplemental/Impact.ttf'
MANROPE='/Users/danielrose/Library/Fonts/Manrope.ttf'
WHITE=(255,255,250); BLACK=(8,11,18)

def font(size,heavy=True):
 f=ImageFont.truetype(IMPACT if heavy else MANROPE,size)
 if not heavy:f.set_variation_by_name('ExtraBold')
 return f

def portrait(path,mask=None,bottom=None):
 im=Image.open(path).convert('RGBA')
 if mask:
  a=Image.open(mask).convert('L').resize(im.size).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.65));im.putalpha(a)
 if bottom:im=im.crop((0,0,im.width,int(im.height*bottom)))
 return im.crop(im.getchannel('A').point(lambda p: 255 if p>127 else 0).getbbox())

P1=portrait(PH/'photo-125_FINAL_PRIMARY.jpg',AS/'photo-125_FINAL_PRIMARY.mask.png',.91)
P2=portrait(PH/'_cutouts/studio-white-90_CUTOUT.png',bottom=.76)
P3=portrait(PH/'_cutouts/studio-blue-109_CUTOUT.png',bottom=.70)
P4=portrait(AS/'master-0s.png',AS/'master-0s.mask.png')
P5=portrait(ROOT/'photos/dan transformation photos/photo-180_FINAL_PRIMARY copy.png',AS/'photo-180_FINAL_PRIMARY copy.mask.png',.96)

# Supporting pool scene is generated; Dan remains the original pool-shoot photo.
pool=ImageOps.fit(Image.open(AS/'pool-bg.png').convert('RGB'),(W,H))
green=Image.open(AS/'master-2s.png').convert('RGB').crop((0,0,450,1080)).resize((W,H),Image.Resampling.LANCZOS)
medical=ImageOps.fit(Image.open(AS/'medical-bg.png').convert('RGB'),(W,H))
protein=ImageOps.fit(Image.open(AS/'protein-bg.png').convert('RGB'),(W,H))

CONCEPTS=[
 dict(n=1,title='POOL PHOTO',p=P1,bg=pool,accent=(255,212,40),source='photo-125_FINAL_PRIMARY.jpg; generated supporting pool background',heavy=False,outline=False),
 dict(n=2,title='STUDIO: VIAL + SYRINGE',p=P2,bg=medical,accent=(45,220,255),source='studio-white-90_CUTOUT.png',heavy=True,outline=True),
 dict(n=3,title='STUDIO: TIMING + PROTEIN',p=P3,bg=protein,accent=(255,193,46),source='studio-blue-109_CUTOUT.png',heavy=True,outline=True),
 dict(n=4,title='AUTHENTIC VIDEO FRAME',p=P4,bg=green,accent=(99,204,255),source='approved master at 00:00.000',heavy=False,outline=False),
 dict(n=5,title='DESIGNER CHOICE: REAL NOW PHOTO',p=P5,bg=medical,accent=(255,214,32),source='real NOW photo from approved video: photo-180_FINAL_PRIMARY copy.png',heavy=True,outline=True),
]

def scrim(im,strength):
 ar=np.asarray(im,dtype=float)
 x=np.arange(W)[None,:];y=np.arange(H)[:,None]
 a=strength*np.maximum(0,1-x/820)**1.25
 a=np.broadcast_to(a,(H,W)).copy()
 a+=35*np.maximum(0,1-y/400)**1.4
 a=np.clip(a,0,235)/255
 return Image.fromarray((ar*(1-a[:,:,None])+np.array(BLACK)[None,None,:]*a[:,:,None]).astype('uint8')).convert('RGBA')

def place(canvas,p,variant,outline):
 maxw=[555,555,580,525,590][variant]; maxh=[704,700,700,662,704][variant]
 scale=min(maxw/p.width,maxh/p.height)
 p=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS)
 x=W-24-p.width;y=H-p.height
 # Frame has visible hair headroom; no out-of-frame expansion or invented body.
 layer=Image.new('RGBA',(W,H));layer.alpha_composite(p,(x,y))
 a=layer.getchannel('A')
 sh=Image.new('RGBA',(W,H),(0,0,0,0));sh.putalpha(a.filter(ImageFilter.GaussianBlur(12)).point(lambda z:int(z*.6)))
 canvas.alpha_composite(sh)
 if outline:
  edge=Image.new('RGBA',(W,H),(*WHITE,0));edge.putalpha(a.filter(ImageFilter.MaxFilter(15)));canvas.alpha_composite(edge)
 canvas.alpha_composite(layer)
 return a

def copy(canvas,v,accent,heavy,drug='ZEPBOUND'):
 d=ImageDraw.Draw(canvas);boxes=[]
 def text(s,x,y,size,color=WHITE,maxw=600,stroke=0):
  f=font(size,heavy)
  while d.textbbox((0,0),s,font=f,stroke_width=stroke)[2]>maxw:
   size-=1;f=font(size,heavy)
  b=d.textbbox((0,0),s,font=f,stroke_width=stroke);h=b[3]-b[1];tw=b[2]-b[0]
  d.text((x-b[0]+3,y-b[1]+5),s,font=f,fill=(0,0,0,150),stroke_width=stroke+2,stroke_fill=(0,0,0,160))
  d.text((x-b[0],y-b[1]),s,font=f,fill=color,stroke_width=stroke,stroke_fill=BLACK)
  boxes.append((x-5,y-5,x+tw+7,y+h+8));return tw,h
 if v==0:
  d.rectangle((42,70,52,294),fill=accent)
  text(drug,72,79,119,maxw=545,stroke=2 if heavy else 0)
  text('5 TIPS',72,191,166,accent,maxw=545,stroke=2 if heavy else 0)
 elif v==1:
  text('5',42,81,295,accent,maxw=174,stroke=3 if heavy else 0)
  text(drug,231,113,83,maxw=399,stroke=2 if heavy else 0)
  text('TIPS',231,206,143,maxw=399,stroke=2 if heavy else 0)
  d.line((48,378,621,378),fill=accent,width=6)
 elif v==2:
  text('5 '+drug,42,47,104,maxw=574,stroke=2 if heavy else 0)
  text('TIPS',42,158,213,accent,maxw=573,stroke=3 if heavy else 0)
 elif v==3:
  text(drug,42,79,129,maxw=591,stroke=2 if heavy else 0)
  d.rounded_rectangle((40,202,632,389),radius=18,fill=accent)
  text('5 TIPS',65,224,169,BLACK,maxw=540)
 elif v==4:
  d.polygon([(0,0),(625,0),(573,350),(0,381)],fill=(6,12,22,190))
  text(drug,42,73,119,maxw=573,stroke=2 if heavy else 0)
  text('5 TIPS',42,184,166,accent,maxw=573,stroke=2 if heavy else 0)
  d.line((42,328,573,328),fill=accent,width=6)
 return boxes

def build(c,v,drug='ZEPBOUND'):
 im=c['bg'].copy()
 if v==2:im=ImageOps.fit(im.resize((1382,778)),(W,H),centering=(0,1))
 canvas=scrim(im,145 if c['n'] in [2,3,5] else 193)
 mask=place(canvas,c['p'],v,c['outline'])
 boxes=copy(canvas,v,c['accent'],c['heavy'],drug)
 if c['n'] in [2,3,5]:
  d=ImageDraw.Draw(canvas);d.rounded_rectangle((12,12,W-13,H-13),radius=17,outline=WHITE,width=3)
 out=HERE/f"ro12-{c['n']}{'ABCDE'[v]}{'-GLP1' if drug=='GLP-1' else ''}.jpg"
 canvas.convert('RGB').save(out,quality=94,subsampling=0)
 # Check saved geometry against the exact real-person alpha used in rendering.
 ma=np.asarray(mask)>127
 clearance=[]
 for x0,y0,x1,y1 in boxes:
  band=ma[max(0,y0):min(H,y1)]
  cols=np.where(band.any(axis=0))[0]
  gap=9999 if not len(cols) else int(cols.min()-x1)
  assert gap>=25,(out.name,'text collision',gap)
  clearance.append(gap)
 assert min(box[0] for box in boxes)>=0 and max(box[2] for box in boxes)<W
 ys,xs=np.where(ma);assert ys.min()>=15,(out.name,'hair headroom',ys.min())
 assert out.stat().st_size<2000000
 Image.open(out).resize((320,180),Image.Resampling.LANCZOS).save(HERE/f'{out.stem}-feed.jpg',quality=94)
 return dict(id=f"{c['n']}{'ABCDE'[v]}"+(' GLP-1' if drug=='GLP-1' else ''),file=out.name,concept=c['title'],source=c['source'],text_clearance_px=min(clearance),hair_headroom_px=int(ys.min()),dimensions=[W,H],bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest())

results=[]
for c in CONCEPTS:
 for v in range(5):results.append(build(c,v))
alt=build(CONCEPTS[1],0,'GLP-1');results.append(alt)
(HERE/'manifest-QC.json').write_text(json.dumps(results,indent=2)+'\n')
# Five rows with a consistent concept per row. Labels outside artwork.
tw,th=384,216; gap=20; margin=28; sw=5*tw+4*gap+2*margin
sheet=Image.new('RGB',(sw,1924),'#eef0f4');d=ImageDraw.Draw(sheet)
d.text((margin,22),'TOP 5 ZEPBOUND TIPS | THUMBNAIL REVIEW',font=font(34,False),fill=BLACK)
d.text((margin,75),'Five variations per concept. Pick an ID, such as 2A. Pick two for an A/B test.',font=font(23,False),fill=BLACK)
for i,c in enumerate(CONCEPTS):
 y=132+i*295
 d.text((margin,y),f"{c['n']}. {c['title']}",font=font(24,False),fill=BLACK)
 for j in range(5):
  r=results[i*5+j];x=margin+j*(tw+gap)
  tile=Image.open(HERE/r['file']).resize((tw,th),Image.Resampling.LANCZOS)
  sheet.paste(tile,(x,y+40));d.text((x,y+262),r['id'],font=font(23,False),fill=BLACK)
 # Separate bigger row sheet for inspecting full photos and copy.
 group=Image.new('RGB',(1360,1330),'#eef0f4');gd=ImageDraw.Draw(group)
 gd.text((24,15),c['title'],font=font(26,False),fill=BLACK)
 for j in range(5):
  r=results[i*5+j];x=24+(j%2)*672;gy=66+(j//2)*418
  gd.text((x,gy),r['id'],font=font(25,False),fill=BLACK)
  group.paste(Image.open(HERE/r['file']).resize((640,360),Image.Resampling.LANCZOS),(x,gy+34))
 group.save(HERE/f"REVIEW_{c['n']}_detail.jpg",quality=94)
y=1632
d.text((margin,y),'ALTERNATE: 2A with GLP-1 wording',font=font(25,False),fill=BLACK)
sheet.paste(Image.open(HERE/alt['file']).resize((tw,th),Image.Resampling.LANCZOS),(margin,y+42))
d.text((margin+tw+32,y+80),'Same portrait and design as 2A.\nOnly the headline changes to 5 GLP-1 TIPS.\nFinal export waits for your pick.',font=font(24,False),fill=BLACK,spacing=16)
sheet.save(HERE/'REVIEW_ro12_thumbnails.jpg',quality=95,subsampling=0)
print(f'PASS: {len(results)} thumbnails, full-resolution + 320px feed checks saved.')
