#!/usr/bin/env python3
"""Chest Flies covers. Local typography/compositing per coverimage workflow.
Original real-photo pixels retained; no film changes. Source assets live outside Git.
Layout helpers adapted from ds02-03-07-11-20261026/build.py and round2.py.
"""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter,ImageEnhance
import numpy as np
R=Path(__file__).resolve().parents[3]
W=Path('/Users/danielrose/Projects/_edit_work/DS78-cover-setup')
O=R/'Short-form video content/covers/review/ds78-chest-flies-20261109'
S=W/'sources'; OUT=O/'designs';OUT.mkdir(parents=True,exist_ok=True)
SUP='/System/Library/Fonts/Supplemental/'
FONTS={'din':(SUP+'DIN Condensed Bold.ttf',0),'impact':(SUP+'Impact.ttf',0),'serif':(SUP+'Georgia Bold.ttf',0),'sans':('/System/Library/Fonts/Avenir Next.ttc',1),'heavy':('/System/Library/Fonts/Avenir Next Condensed.ttc',8)}
SIZE=(1080,1920)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(name,size):
 p,i=FONTS[name];return ImageFont.truetype(p,size,index=i)
def fit(s,name,cap,width):
 for n in range(cap,24,-1):
  f=font(name,n)
  if f.getbbox(s)[2]<=width:return f
 raise ValueError(s)
def text(im,mask,s,name,cap,x,y,width=960,color='#ffffff',anchor='mt',stroke=0):
 f=fit(s,name,cap,width);d=ImageDraw.Draw(im);m=ImageDraw.Draw(mask)
 d.text((x,y),s,font=f,fill=color,anchor=anchor,stroke_width=stroke,stroke_fill='#07101a')
 m.text((x,y),s,font=f,fill=255,anchor=anchor,stroke_width=stroke,stroke_fill=255)
 return d.textbbox((x,y),s,font=f,anchor=anchor,stroke_width=stroke)
def ramp(im,y0,y1,alpha=245,bottom=False,col=(3,8,16)):
 ar=np.zeros((1920,1080,4),dtype=np.uint8);ar[:,:,:3]=col
 for y in range(1920):
  t=(y-y0)/(y1-y0) if bottom else (y1-y)/(y1-y0)
  ar[y,:,3]=int(alpha*min(1,max(0,t)))
 im.alpha_composite(Image.fromarray(ar))
def plate(k):
 p=S/(k+('.jpg' if k.startswith('G') else '.png'))
 return ImageOps.fit(Image.open(p).convert('RGB'),SIZE,method=Image.Resampling.LANCZOS).convert('RGBA')
def shift(im,dy):
 # Top extension only, from image's own dark header. No person copied or generated.
 out=Image.new('RGBA',SIZE,im.getpixel((500,30)));out.alpha_composite(im,(0,dy));return out
records=[]
for k in ['A','B','C','D','E','G1','G2','G3']:
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';t=260 if ig else 106;mask=Image.new('L',SIZE);b=[]
  if k=='C':
   im=plate('Cbg');cut=Image.open(R/'photos/finalized social media photos/_cutouts/studio-white-23_CUTOUT.png').convert('RGBA')
   cut=cut.crop((120,200,2630,4540));cut.thumbnail((760,1260),Image.Resampling.LANCZOS)
   # A crisp white outline outside the real cutout, preserving the subject.
   a=cut.getchannel('A');outline=a.filter(ImageFilter.MaxFilter(15));ol=Image.new('RGBA',cut.size,'white');ol.putalpha(outline)
   xy=(1080-cut.width-40,650 if ig else 560);im.alpha_composite(ol,xy);im.alpha_composite(cut,xy)
   ramp(im,t-20,t+340)
   d=ImageDraw.Draw(im);d.rectangle((60,t-10,76,t+275),fill='#ec3e3a')
   b.append(text(im,mask,'How To Do','sans',108,565,t,width=900))
   b.append(text(im,mask,'Chest Flies','sans',150,565,t+136,width=900,color='#ffffff'))
  elif k=='D':
   src=Image.open(W/'squeeze-2.3.jpg').convert('RGB')
   src=ImageEnhance.Brightness(src).enhance(1.12);src=ImageEnhance.Color(src).enhance(1.10)
   src=src.filter(ImageFilter.UnsharpMask(1.3,115,3))
   # The source is an already approved Color C finished library master, not raw.
   photo=src.crop((600,0,2500,2160));photo=ImageOps.fit(photo,(1080,1290),method=Image.Resampling.LANCZOS)
   im=Image.new('RGBA',SIZE,'#0b0c10');top=615 if ig else 455;im.alpha_composite(photo.convert('RGBA'),(0,top))
   bandtop=248 if ig else 88;bandbottom=top
   ImageDraw.Draw(im).rectangle((0,bandtop,1080,bandbottom),fill='#ffdc00')
   b.append(text(im,mask,'How To Do','din',180,540,bandtop+38,color='#111418'))
   b.append(text(im,mask,'Chest Flies','din',180,540,bandtop+191,color='#b91f26'))
  else:
   im=plate(k)
   if k=='A':
    ramp(im,t-50,t+360)
    b.append(text(im,mask,'How To Do','serif',112,540,t,color='#eee2c7'))
    b.append(text(im,mask,'Chest Flies','serif',136,540,t+130,color='#eee2c7'))
    ImageDraw.Draw(im).rectangle((365,t+301,715,t+310),fill='#d6a557')
   elif k=='B':
    ramp(im,t-30,t+350)
    ImageDraw.Draw(im).rectangle((58,t-10,68,t+285),fill='#42c8f2')
    b.append(text(im,mask,'How To Do','din',168,100,t,width=920,anchor='lt'))
    b.append(text(im,mask,'Chest Flies','din',186,100,t+151,width=920,anchor='lt',color='#55d4f9'))
   elif k=='E':
    # Bottom-title layout: larger picture, no eyebrow, three balanced lines.
    big=im.resize((1210,2151),Image.Resampling.LANCZOS);im=big.crop((65,0,1145,1920))
    y=1190 if ig else 1435;ramp(im,y-190,y+35,bottom=True)
    b.append(text(im,mask,'How To Do','heavy',125,540,y))
    b.append(text(im,mask,'Chest','heavy',200,540,y+116,color='#ff554b'))
    b.append(text(im,mask,'Flies','heavy',190,540,y+273))
   elif k=='G1':
    im=shift(im,170 if ig else 40);ramp(im,t-50,t+320)
    ImageDraw.Draw(im).rounded_rectangle((52,t-6,445,t+75),radius=3,fill='#d57530')
    b.append(text(im,mask,'How To Do','sans',59,248,t+8,width=350,color='#ffffff'))
    b.append(text(im,mask,'Chest Flies','heavy',160,53,t+102,width=960,anchor='lt',color='#fff1dc'))
   elif k=='G2':
    # Ivory editorial masthead, not a repeat of the cyan condensed layout.
    ramp(im,t-60,t+320)
    b.append(text(im,mask,'How To Do','serif',104,540,t,color='#f5eee0'))
    b.append(text(im,mask,'Chest Flies','serif',126,540,t+124,color='#f5eee0'))
    ImageDraw.Draw(im).line((90,t+284,990,t+284),fill='#a4bccb',width=3)
   elif k=='G3':
    # Photo remains uncropped vertically; headline on a cobalt field above the hair.
    im=shift(im,245 if ig else 90)
    bt=245 if ig else 65;ImageDraw.Draw(im).rectangle((0,bt,1080,bt+320),fill='#1643b5')
    b.append(text(im,mask,'How To Do','impact',132,540,bt+31))
    b.append(text(im,mask,'Chest Flies','impact',152,540,bt+166,color='#ffffff'))
  path=OUT/f'{k}-{platform}.png';im.convert('RGB').save(path);mask.save(OUT/f'{k}-{platform}.mask.png')
  if not ig:im.convert('RGB').save(path.with_suffix('.jpg'),quality=93)
  # Real-photo options are excluded from the model scorecard.
  records.append(dict(design=k,platform=platform,path=str(path),sha256=sha(path),bytes=path.stat().st_size,text_boxes=b,text_mask=str(OUT/f'{k}-{platform}.mask.png'),source=('google' if k.startswith('G') else 'codex'),comparison_eligible=k not in ['C','D']))
(O/'manifest-private.json').write_text(json.dumps(records,indent=2))
# Contact sheets for editor checks only, before neutral labels.
for platform in ['instagram','youtube']:
 out=Image.new('RGB',(2160,1040),'#1b2330');d=ImageDraw.Draw(out)
 for i,k in enumerate(['A','B','C','D','E','G1','G2','G3']):
  im=Image.open(OUT/f'{k}-{platform}.png');im.thumbnail((270,480));out.paste(im,(i*270,30));d.text((i*270+5,5),k,fill='white')
 out.crop((0,0,2160,520)).save(W/f'layout-{platform}.jpg',quality=94)
print('Built 16 covers, masks and private manifest:',O)
