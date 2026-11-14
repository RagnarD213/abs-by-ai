from pathlib import Path
import sys,json,hashlib,subprocess
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np
w=Path('/Users/danrrose/Projects/_edit_work/sl21-covers');root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI')
sys.path.insert(0,str(root/'scripts/covers/sl08-20261025'));import build as B
W,H=1080,1920
out=w/'layouts';out.mkdir(exist_ok=True);(w/'qa').mkdir(exist_ok=True)
COPY={'1':["Restaurants Don't","Care About Your","Fitness Goals"],'2':["You Don't Deserve","A Vacation Until","You're Ripped"],'3':["If You Can't Afford","A Gym, You Can't","Afford Therapy"]}
REAL={'1':'studio-white-57','2':'studio-blue-247','3':'studio-blue-123'}
only=set(sys.argv[1:])
mp=w/'layout-manifest-private.json'
records=[r for r in json.loads(mp.read_text()) if r['id'] not in only] if only and mp.exists() else []
def sourcegeo(src):
 cache=w/'qa'/f'{src.stem}-source.json'
 if cache.exists():return json.loads(cache.read_text())
 im=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS);pm,faces=B.person_mask(im)
 ys=np.where(pm.any(axis=1))[0];hair=int(ys.min()) if len(ys) else 500
 r={'hair':hair,'faces':faces};cache.write_text(json.dumps(r));return r

def header(im,tm,k,v,ig):
 top=252 if ig else 96;lines=COPY[k]
 spec={'A':B.DIN,'C':B.FUTURA,'D':B.ABLACK,'E':B.IMPACT,'F':B.DIN,'H':B.IMPACT}.get(v,B.DIN)
 f=B.common(lines,spec,158 if v in 'ACF' else 144,970,0);step=int(f.size*.98 if v in 'ACF' else f.size*1.04)
 height=f.getbbox(lines[-1],anchor='lt')[3]+2*step
 y=top+28;bottom=y+height+30
 # backgrounds are not included in the type mask, which measures actual lettering only.
 d=ImageDraw.Draw(im)
 if v=='A':d.rectangle((0,top,W,bottom),fill=B.YEL)
 elif v=='C':d.rectangle((0,top-10,W,bottom),fill=(249,246,231))
 elif v=='D':d.rectangle((0,top-10,W,bottom),fill=(218,255,229))
 elif v=='F':d.rectangle((0,top-10,W,bottom),fill=(255,246,230));d.rectangle((48,bottom-6,1032,bottom),fill=B.RED)
 elif v=='H':d.rectangle((0,top-10,W,bottom),fill=(18,58,215))
 else:
  d.rectangle((0,0,W,bottom+45),fill=(5,17,31));d.rectangle((54,top+9,245,top+16),fill=B.YEL)
 for i,t in enumerate(lines):
  c=(B.INK if i<2 else (184,24,25)) if v=='A' else ((B.INK if i<2 else (18,95,80)) if v=='D' else (B.RED if v=='F' else (B.INK if v=='C' else B.WHITE)))
  B.text(im,tm,(540,y+i*step),t,f,c,anchor='mt')
 return bottom

def scene(src,top,bottom):
 im=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA');geo=sourcegeo(src);start=max(0,geo['hair']-85)
 crop=im.crop((0,start,W,H));ph=bottom-top;scale=max(W/crop.width,ph/crop.height);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
 xx=(W-crop.width)//2
 # Simple field continuation behind the photo; no repeated/blurred subject.
 col=tuple(int(x) for x in np.asarray(im.convert('RGB'))[:70].reshape(-1,3).mean(axis=0));base=Image.new('RGBA',(W,H),col+(255,));base.alpha_composite(crop,(xx,top))
 faces=[[int(a*scale+xx),int((b-start)*scale+top),int(c*scale+xx),int((d-start)*scale+top)] for a,b,c,d in geo['faces']]
 return base,{'source_crop_y':start,'scale':scale,'subject_hair_top':int((geo['hair']-start)*scale+top),'faces':faces}

def real(im,k,top):
 src=root/'photos/finalized social media photos/_cutouts'/(REAL[k]+'_CUTOUT.png');sub=Image.open(src).convert('RGBA');bb=sub.getchannel('A').getbbox();sub=sub.crop(bb)
 scale=min(985/sub.width,(1710-top)/(sub.height*.72));sub=sub.resize((round(sub.width*scale),round(sub.height*scale)),Image.Resampling.LANCZOS)
 pad=14;bx=Image.new('RGBA',(sub.width+pad*2,sub.height+pad*2));bx.alpha_composite(sub,(pad,pad));a=bx.getchannel('A');line=Image.new('RGBA',bx.size,'white');line.putalpha(a.filter(ImageFilter.MaxFilter(17)))
 x=(W-sub.width)//2-pad;y=top-pad;im.alpha_composite(line,(x,y));im.alpha_composite(bx,(x,y))
 return {'real_source':str(src),'real_source_sha256':B.sha(src),'source_pixels_preserved':True,'subject_hair_top':top}

for src in sorted((w/'sources').glob('*')):
 if src.suffix not in ['.jpg','.png']:continue
 ident=src.stem;k,v=ident[0],ident[1];
 if only and ident not in only:continue
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';tm=Image.new('L',(W,H));blank=Image.new('RGBA',(W,H))
  if v in 'BG':
   f=B.common(COPY[k],B.AVENIR if v=='B' else B.IMPACT,163,990,3);step=int(f.size*1.0);limit=1608 if ig else 1800;bh=f.getbbox(COPY[k][-1],anchor='mt',stroke_width=3)[3];y=limit-bh-2*step
   im,info=scene(src,240 if ig else 60,y-50);B.ramp(im,y-120,y-30,255,top_dark=False,col=(4,15,26))
   for i,t in enumerate(COPY[k]):B.text(im,tm,(540,y+i*step),t,f,B.WHITE if i<2 else (B.CYAN if v=='B' else (197,247,72)),3,anchor='mt')
  else:
   end=header(blank,tm,k,v,ig);tm=Image.new('L',(W,H))
   if v=='C':
    im=ImageOps.fit(Image.open(src).convert('RGBA'),(W,H),method=Image.Resampling.LANCZOS);B.ramp(im,0,800,180);info=real(im,k,end+55)
   else:im,info=scene(src,end+45,H)
   header(im,tm,k,v,ig)
  # Actual final-image detection independently validates face/hair clearance.
  pm,faces=B.person_mask(im);guards=[];ta=np.asarray(tm)>0
  for a,b,c,d in faces:
   fh=d-b;guards.append([max(0,a-20),max(0,b-round(.62*fh)-20),min(W,c+20),min(H,d+20)])
  overlap=sum(int(ta[b:d,a:c].sum()) for a,b,c,d in guards)
  text_bounds=tm.getbbox();assert text_bounds and text_bounds[0]>=20 and text_bounds[2]<=1060
  assert text_bounds[1]>=240 if ig else text_bounds[1]>=50
  assert text_bounds[3]<=1620 if ig else text_bounds[3]<=1840
  dest=out/k/platform;dest.mkdir(parents=True,exist_ok=True);p=dest/(ident+'.png');im.convert('RGB').save(p);tm.save(w/'qa'/f'{ident}-{platform}-text.png')
  if platform=='youtube':im.convert('RGB').save(p.with_suffix('.jpg'),quality=92);assert p.with_suffix('.jpg').stat().st_size<2_000_000
  records.append({'id':ident,'short':int(k),'platform':platform,'file':str(p),'sha256':B.sha(p),'source':str(src),'copy':COPY[k],'text_bounds':text_bounds,'faces':faces,'hair_guards':guards,'face_hair_text_pixels':overlap,**info})
  print(ident,platform,'overlap',overlap,flush=True)
(w/'layout-manifest-private.json').write_text(json.dumps(records,indent=2))
for k in '123':
 ids=sorted(set(r['id'] for r in records if str(r['short'])==k));s=Image.new('RGB',(len(ids)*270,1000),'#101721');d=ImageDraw.Draw(s)
 for i,ident in enumerate(ids):
  for j,platform in enumerate(['instagram','youtube']):
   p=out/k/platform/(ident+'.png');im=Image.open(p).resize((270,480),Image.Resampling.LANCZOS);s.paste(im,(i*270,j*500));d.text((i*270+6,j*500+483),ident+' '+platform,fill='white')
 s.save(w/f'{k}-audit.jpg')
print('BUILD_DONE',len(records),flush=True)
