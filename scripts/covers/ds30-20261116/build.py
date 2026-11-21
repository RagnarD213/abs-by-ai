"""DS30 covers, adapted from scripts/covers/ds41-20261114/build.py. Film untouched."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
ROOT=Path(__file__).resolve().parents[3]
P=Path('/Volumes/Expansion/_edit_work/DS-30-setup')
OUT=P/'designed';OUT.mkdir(exist_ok=True)
W,H=1080,1920
FONT='/System/Library/Fonts/Supplemental/Impact.ttf'
SMALL='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
SERIF='/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
styles={
'a':('#ffd51a','#111923','#111923','band'),
'b':('#102d47','#ffffff','#66ddff','gradient'),
'c':('#102b41','#ffffff','#73e0f0','real'),
'd':('#192027','#fff7ed','#ffc26c','bottom'),
'e':('#39151e','#fff5e1','#ff8b70','left'),
'f':('#f5e6d1','#222629','#a65730','rule'),
'g':('#f9f5df','#074d3a','#074d3a','editorial'),
'h':('#173d68','#ffffff','#b2e8ff','bottom2'),
}
def text(im,phrase,y,maxsize,color,font=FONT,width=960,left=None):
 d=ImageDraw.Draw(im)
 for size in range(maxsize,29,-1):
  f=ImageFont.truetype(font,size)
  if d.textlength(phrase,font=f)<=width:break
 b=d.textbbox((0,0),phrase,font=f);x=(W-d.textlength(phrase,font=f))/2
 xy=(round(x if left is None else left),round(y-b[1]));d.text(xy,phrase,font=f,fill=color)
 box=d.textbbox(xy,phrase,font=f)
 assert box[0]>=45 and box[2]<=1035,(phrase,box)
 return {'text':phrase,'box':list(box),'font_size':size,'font':font}
def lower(im,src,top,crop_frac=.22):
 src=src.crop((0,round(src.height*crop_frac),src.width,src.height))
 scale=max(W/src.width,(H-top)/src.height)
 src=src.resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS)
 left=(src.width-W)//2;im.paste(src.crop((left,0,left+W,H-top)),(0,top))
def shade(im,start,end,color,alpha):
 arr=np.asarray(im).astype(float);a=np.zeros(H)
 a[:start]=alpha;a[start:end]=np.linspace(alpha,0,end-start)
 return Image.fromarray(np.uint8(np.clip(arr*(1-a[:,None,None])+np.array(color)*a[:,None,None],0,255)))
records=[]
for k,(bg,fg,accent,kind) in styles.items():
 for platform in ['Instagram','YouTube']:
  ig=platform=='Instagram';top=660 if ig else 540;start=268 if ig else 108
  src=P/('google/'+k+'.jpg' if k in 'fgh' else 'plates/'+k+'.png')
  im=Image.new('RGB',(W,H),bg)
  if k=='c':
   back=Image.open(src).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
   im=shade(back,top-45,top+45,[10,33,52],.96)
   real=Image.open(ROOT/'photos/finalized social media photos/_cutouts/studio-gray-4_CUTOUT.png').convert('RGBA')
   real=real.crop(real.getbbox())
   target_h=H-(top+30)+110
   real=real.resize((round(real.width*target_h/real.height),target_h),Image.Resampling.LANCZOS)
   # Original person RGBA values only, resized and composited. No retouch or generation.
   x=35;y=top+30
   mask=real.getchannel('A');outline=mask.filter(ImageFilter.MaxFilter(17));white=Image.new('RGBA',real.size,'white');white.putalpha(outline)
   im.paste(white,(x,y),white);im.paste(real,(x,y),real)
   person_box=[x,y,x+real.width,y+real.height]
  elif k in 'dh':
   im=Image.open(src).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
   if k=='d' and ig:
    # Shift full source down 130 px to retain hair in the 3:4 tile, no extra cropping.
    shifted=Image.new('RGB',(W,H),'#182326');shifted.paste(im,(0,130));im=shifted
   overlay=Image.new('RGBA',(W,H));od=ImageDraw.Draw(overlay)
   bottom=1240 if ig else 1405
   for y in range(bottom-180,H):
    a=min(255,int(255*(y-(bottom-180))/180));od.line((0,y,W,y),fill=(17,30,44,a))
   im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
  elif k=='b':
   im=Image.open(src).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
   im=shade(im,400 if ig else 240,650,[10,31,49],.8)
  else:lower(im,Image.open(src).convert('RGB'),top)
  d=ImageDraw.Draw(im);t=[]
  if kind in ['bottom','bottom2']:
   base=1270 if ig else 1420
   t.append(text(im,'Make Time For',base,119,fg))
   t.append(text(im,'Exercise With A',base+122,114,accent))
   t.append(text(im,'Self-Driving Car',base+244,110,fg))
  elif kind=='left':
   d.rectangle((52,start,62,start+335),fill=accent)
   t.append(text(im,'Make Time',start,115,fg,SMALL,left=90,width=900))
   t.append(text(im,'For Exercise',start+130,112,fg,SMALL,left=90,width=900))
   t.append(text(im,'With A Self-Driving Car',start+280,51,accent,SMALL,left=90,width=900))
  elif kind=='editorial':
   d.line((70,start+4,1010,start+4),fill=accent,width=5)
   t.append(text(im,'Make Time',start+30,104,fg,SERIF))
   t.append(text(im,'For Exercise',start+150,99,fg,SERIF))
   t.append(text(im,'With A Self-Driving Car',start+285,48,accent,SMALL))
  else:
   if kind=='real':d.rectangle((60,start-20,1020,start-12),fill=accent)
   if kind=='rule':d.line((70,start+248,1010,start+248),fill=accent,width=5)
   t.append(text(im,'Make Time',start,128,fg))
   t.append(text(im,'For Exercise',start+140,126,accent))
   t.append(text(im,'With A Self-Driving Car',start+290,52,fg,SMALL))
  assert min(v['box'][1] for v in t)>=(240 if ig else 90)
  assert max(v['box'][3] for v in t)<=(1620 if ig else 1850)
  if k not in 'dh':assert max(v['box'][3] for v in t)<top-22
  f=OUT/f'{k}-{platform}.png';im.save(f)
  jpg=f.with_suffix('.jpg');im.save(jpg,quality=94,subsampling=0)
  assert jpg.stat().st_size<2_000_000
  mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask)
  for v in t:md.rectangle(v['box'],fill=255)
  mask.save(OUT/f'{k}-{platform}-textmask.png')
  im.crop((0,240,W,1680)).resize((270,360)).save(OUT/f'{k}-{platform}-grid.jpg',quality=94)
  records.append({'concept':k,'platform':platform,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'jpg':str(jpg),'jpg_bytes':jpg.stat().st_size,'text':t,'image_top':top,'original_real_person_pixels':k=='c','source_plate':str(src),'person_box':person_box if k=='c' else None})
(P/'layout-manifest.json').write_text(json.dumps(records,indent=2))
sheet=Image.new('RGB',(2160,1580),'#101b29');d=ImageDraw.Draw(sheet)
for i,k in enumerate(styles):
 for j,platform in enumerate(['Instagram','YouTube']):
  im=Image.open(OUT/f'{k}-{platform}.png').resize((205,365));x=(i%4)*540+j*210;y=(i//4)*790+45
  sheet.paste(im,(x,y));d.text((x,y-24),k+' '+platform,fill='white')
 crop=Image.open(OUT/f'{k}-Instagram-grid.jpg');sheet.paste(crop,((i%4)*540,(i//4)*790+425))
sheet.save(P/'layout-sheet.jpg',quality=96)
print('Built 16 paired 1080x1920 covers, JPEGs under 2MB, and Instagram grid crops.')
