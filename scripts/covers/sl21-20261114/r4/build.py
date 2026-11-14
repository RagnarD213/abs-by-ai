from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
import json,sys,numpy as np
w=Path('/Users/danrrose/Projects/_edit_work/sl21-covers/r4');root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(root/'scripts/covers/sl08-20261025'));import build as B
W,H=1080,1920;(w/'layouts').mkdir(exist_ok=True);(w/'qa').mkdir(exist_ok=True)
lines=['Why Restaurants','Make You Fat'];records=[]

def header(im,tm,v,ig):
 top=252 if ig else 96;spec={'A':B.DIN,'C':B.IMPACT,'D':B.FUTURA}[v];f=B.common(lines,spec,195,970);step=round(f.size*1.02);y=top+24;bottom=y+step+f.getbbox(lines[1],anchor='mt')[3]+32;d=ImageDraw.Draw(im)
 if v=='A':d.rectangle((0,top-10,W,bottom),fill=B.YEL)
 elif v=='C':d.rectangle((0,0,W,bottom+20),fill=(5,17,31));d.rectangle((50,top-10,300,top),fill=(255,116,38))
 else:d.rectangle((0,top-10,W,bottom),fill=(255,246,228))
 for i,t in enumerate(lines):
  c=(B.INK if i==0 else (191,22,22)) if v=='A' else (B.WHITE if i==0 else (255,153,55)) if v=='C' else (B.INK if i==0 else B.RED)
  B.text(im,tm,(540,y+i*step),t,f,c,anchor='mt')
 return bottom

def scene(src,top,bottom):
 raw=Image.open(src).convert('RGBA');raw=raw.resize((W,round(raw.height*W/raw.width)),Image.Resampling.LANCZOS);col=tuple(int(i) for i in np.array(raw.convert('RGB'))[:60].reshape(-1,3).mean(axis=0));im=Image.new('RGBA',(W,H),col+(255,));im.alpha_composite(raw,(0,max(0,H-raw.height)));m,faces=B.person_mask(im);ys=np.where(m.any(axis=1))[0];assert len(ys) and faces,'Person/face detection missing';hair=int(ys.min());ph=bottom-top;start=max(0,hair-90) if src.stem=='D' else min(max(0,hair-90),H-ph);crop=im.crop((0,start,W,min(H,start+ph)));floor=tuple(int(i) for i in np.array(im.convert('RGB'))[-50:].reshape(-1,3).mean(axis=0)) if src.stem=='D' else col;base=Image.new('RGBA',(W,H),floor+(255,));base.alpha_composite(crop,(0,top));return base,{'source_crop_y':start,'subject_top':top+hair-start,'scale':1.0,'full_source_width_preserved':True,'floor_field_extension':src.stem=='D'}

for src in sorted((w/'sources').glob('*')):
 if src.suffix not in ['.png','.jpg']:continue
 v=src.stem
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';tm=Image.new('L',(W,H));
  if v=='B':
   f=B.common(lines,B.AVENIR,195,990,3);step=int(f.size);limit=1608 if ig else 1790;lastheight=f.getbbox(lines[-1],anchor='mt',stroke_width=3)[3];y=limit-lastheight-step
   im,info=scene(src,240 if ig else 60,y-60);B.ramp(im,y-130,y-30,255,top_dark=False,col=(4,15,26))
   for i,t in enumerate(lines):B.text(im,tm,(540,y+i*step),t,f,B.WHITE if i==0 else B.CYAN,3,anchor='mt')
  else:
   end=header(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),v,ig);im,info=scene(src,end+45,H);header(im,tm,v,ig)
  m,faces=B.person_mask(im);assert faces;guards=[];ta=np.asarray(tm)>0
  for a,b,c,d in faces:
   fh=d-b;guards.append([max(0,a-20),max(0,b-round(.62*fh)-20),min(W,c+20),min(H,d+20)])
  overlap=sum(int(ta[b:d,a:c].sum()) for a,b,c,d in guards);assert overlap==0,(v,platform,overlap)
  bounds=tm.getbbox();assert bounds[0]>=20 and bounds[2]<=1060;assert bounds[1]>=(240 if ig else 50) and bounds[3]<=(1620 if ig else 1840)
  out=w/'layouts'/platform;out.mkdir(exist_ok=True);p=out/(v+'.png');im.convert('RGB').save(p);tm.save(w/'qa'/f'{v}-{platform}-type.png')
  if not ig:im.convert('RGB').save(p.with_suffix('.jpg'),quality=92);assert p.with_suffix('.jpg').stat().st_size<2_000_000
  records.append({'id':v,'platform':platform,'path':str(p),'sha256':B.sha(p),'copy':lines,'text_bounds':bounds,'faces':faces,'hair_guards':guards,'face_hair_text_pixels':overlap,**info});print(v,platform,'PASS',flush=True)
(w/'layout-manifest-private.json').write_text(json.dumps(records,indent=2));print('BUILT',len(records),flush=True)
s=Image.new('RGB',(1080,1020),'#111b28');d=ImageDraw.Draw(s)
for i,v in enumerate('ABCD'):
 for j,platform in enumerate(['instagram','youtube']):
  p=w/'layouts'/platform/(v+'.png');im=Image.open(p);im.thumbnail((270,480));s.paste(im,(i*270,j*510+25));d.text((i*270+5,j*510+5),v+' '+platform,fill='white')
s.save(w/'audit.jpg')
