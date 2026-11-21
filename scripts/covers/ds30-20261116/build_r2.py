"""DS30 R2: four requested driver/meal scenes. Reuses R1 type helpers; never touches film."""
from pathlib import Path
import ast,json,hashlib,subprocess,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
ROOT=Path(__file__).resolve().parents[3];P=Path('/Volumes/Expansion/_edit_work/DS-30-setup/r2');OUT=P/'designed';W,H=1080,1920
FONT='/System/Library/Fonts/Supplemental/Impact.ttf';SMALL='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
# Import only the maintained helper definitions, with no R1 build side effects.
tree=ast.parse((Path(__file__).parent/'build.py').read_text());helper=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['text','shade']],type_ignores=[]);exec(compile(helper,'r1-layout-helpers','exec'))
sources={'a':P/'plates/a.png','b':P/'plates/b.png','c':P/'plates/c3.png','d':P/'google/d2.jpg'}
styles={'a':('#ffdb21','#141a22','#141a22','band'),'b':('#102d47','#ffffff','#69dcff','gradient'),'c':('#171d27','#fff6e7','#ffae70','line'),'d':('#fff1d7','#142b3c','#a4492b','cream')}
rows=[]
for k,src in sources.items():
 full=Image.open(src).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
 for platform in ['Instagram','YouTube']:
  ig=platform=='Instagram';bg,fg,accent,kind=styles[k]
  if ig:
   # Keep food and glass entirely in the profile crop without distorting the body.
   im=full.filter(ImageFilter.GaussianBlur(30));photo_scale=.86 if k=='d' else .9;small=full.resize((round(W*photo_scale),round(H*photo_scale)),Image.Resampling.LANCZOS);py={'a':100,'b':180,'c':100,'d':260}[k]
   mask=Image.new('L',small.size,255);md=ImageDraw.Draw(mask)
   for x in range(20):
    md.line((x,0,x,small.height),fill=int(255*x/20));md.line((small.width-1-x,0,small.width-1-x,small.height),fill=int(255*x/20))
   im.paste(small,((W-small.width)//2,py),mask)
  else:
   im=full.copy();py=0
   if k=='d':
    py=70;im=full.filter(ImageFilter.GaussianBlur(30));im.paste(full,(0,py))
  # Distinct layouts, identical complete title, no copy on hair/face or meal.
  if kind in ['band','cream']:
   ImageDraw.Draw(im).rectangle((0,0,W,575 if ig else 385),fill=bg)
  else:im=shade(im,550 if ig else 365,610 if ig else 420,[16,29,44] if kind=='gradient' else [23,29,39],.96)
  start=250 if ig else 96;d=ImageDraw.Draw(im)
  if kind=='line':d.rectangle((55,start,64,start+288),fill=accent)
  left=92 if kind=='line' else None;width=900 if kind=='line' else 960
  t=[text(im,'Make Time',start,118,fg,width=width,left=left),text(im,'For Exercise',start+115,116,accent,width=width,left=left),text(im,'With A Self-Driving Car',start+240,44,fg,SMALL,width=width,left=left)]
  assert min(x['box'][1] for x in t)>=(240 if ig else 90)
  assert max(x['box'][3] for x in t)<=1620
  f=OUT/f'{k}-{platform}.png';im.save(f);jpg=f.with_suffix('.jpg');im.save(jpg,quality=94,subsampling=0);assert jpg.stat().st_size<2_000_000
  grid=im.crop((0,240,W,1680));grid.save(OUT/f'{k}-{platform}-grid.jpg',quality=95)
  rows.append({'concept':k,'platform':platform,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'jpg_bytes':jpg.stat().st_size,'text':t,'source':str(src),'photo_scale':photo_scale if ig else 1,'photo_offset_y':py})
(P/'layout-manifest.json').write_text(json.dumps(rows,indent=2))
sheet=Image.new('RGB',(1600,1170),'#101c2a');d=ImageDraw.Draw(sheet)
for i,k in enumerate(sources):
 for j,plat in enumerate(['Instagram','YouTube']):
  im=Image.open(OUT/f'{k}-{plat}.png');im.thumbnail((190,338));x=i*400+j*195;sheet.paste(im,(x,35));d.text((x,10),k+' '+plat,fill='white')
 im=Image.open(OUT/f'{k}-Instagram-grid.jpg');im.thumbnail((380,507));sheet.paste(im,(i*400,410))
sheet.save(P/'layout-sheet.jpg',quality=95)
print('Built four new cover designs, eight paired layouts. Original film untouched.')
