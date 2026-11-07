from pathlib import Path
import sys,json,hashlib
from PIL import Image,ImageDraw,ImageOps,ImageFilter
import numpy as np
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');w=Path('/Users/danielrose/Projects/_edit_work/sl13-setup-20261107')
sys.path.insert(0,str(ROOT/'scripts/covers/sl08-20261025'))
import build as B
W,H=1080,1920
OUT=w/'layouts';OUT.mkdir(exist_ok=True)
COPY={'A':['Eat Protein','First'],'B':['Eat Less Without','Counting Calories'],'C':['Keep Your','Steps Up']}
TRIPLE={'A':['Eat','Protein','First'],'B':['Eat Less','Without Counting','Calories'],'C':['Keep','Your Steps','Up']}
REAL={'A':'studio-white-23','B':'studio-white-49','C':'studio-blue-247'}
B.STUDIO=REAL;B.COPY={k:(v,k,k) for k,v in COPY.items()};B.BADGES={k:'' for k in COPY}
B.DCOPY=TRIPLE
only=set(sys.argv[1:])
records=[r for r in json.loads((w/'layout-manifest-private.json').read_text()) if r['id'] not in only] if only else []
plan=json.loads((w/'generation-plan.json').read_text())
# The existing house builder supplies fonts, mask-drawing, gradients, fitting, and real-photo compositing.
def type_upper(im,tm,k,ig,style):
 top=252 if ig else 90
 if style=='yellow':
  f=B.common(COPY[k],B.DIN,190,960);step=int(f.size*.95)
  btm=top+50+2*step
  B.box(im,tm,(0,top-16,W,btm),B.YEL)
  for n,t in enumerate(COPY[k]):B.text(im,tm,(54,top+10+n*step),t,f,B.INK if n==0 else (195,24,24))
  return btm
 if style=='real':
  f=B.common(COPY[k],B.FUTURA,134,950,4);step=int(f.size*1.12)
  B.text(im,tm,(540,top),COPY[k][0],f,B.WHITE,4,anchor='ma')
  bb=f.getbbox(COPY[k][1],anchor='ma');y=top+step
  B.box(im,tm,(540+bb[0]-18,y+bb[1]-10,540+bb[2]+18,y+bb[3]+10),B.YEL,4)
  B.text(im,tm,(540,y),COPY[k][1],f,B.INK,anchor='ma')
  return y+bb[3]+10
 f=B.common(COPY[k],B.IMPACT,165,950,5);step=int(f.size*1.08)
 for n,t in enumerate(COPY[k]):B.text(im,tm,(58,top+n*step),t,f,B.WHITE if n==0 else B.CYAN,5)
 ImageDraw.Draw(im).rectangle((58,top-25,280,top-15),fill=B.CYAN)
 return top+2*step

def make(row,source,short,ident,style,origin):
 if not source.exists() or (only and ident not in only):return
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';tm=Image.new('L',(W,H))
  im=ImageOps.fit(Image.open(source).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA');info={}
  if style=='real':
   B.ramp(im,0,850,200)
   top=type_upper(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),short,ig,'real')+120
   info=B.studio(im,short,top);info['real_photo_source']=info.pop('source');pic=im.copy();type_upper(im,tm,short,ig,'real')
  elif style=='side':
   # A full-height charcoal side rail keeps type separate from the generated right-side subject.
   alpha=Image.new('RGBA',(W,H));d=ImageDraw.Draw(alpha);d.rectangle((0,0,440,H),fill=(4,15,27,235));im.alpha_composite(alpha)
   y=420 if ig else 240
   words={'A':['Eat','Protein','First'],'B':['Eat Less','Without','Counting','Calories'],'C':['Keep','Your','Steps','Up']}[short]
   f=B.common(words,B.DIN,170,375)
   for n,t in enumerate(words):B.text(im,tm,(40,y+n*int(f.size*1.12)),t,f,B.WHITE if n<len(words)-1 else B.YEL,2)
   ImageDraw.Draw(im).rectangle((40,y-28,240,y-20),fill=B.YEL);pic=None
  elif style=='bottom':
   # Reframe away from excess source sky so the large bottom title sits below the torso.
   pm,faces=B.person_mask(im);ys=np.where(pm.any(axis=1))[0];hair=int(ys.min()) if len(ys) else 400
   scale=.80
   sub=im.resize((round(W*scale),round(H*scale)),Image.Resampling.LANCZOS)
   shift=(265 if ig else 100)-round(hair*scale)
   base=im.filter(ImageFilter.GaussianBlur(30));base.alpha_composite(sub,((W-sub.width)//2,shift));im=base
   pic=im.copy();B.ramp(im,1120,1380,250,top_dark=False)
   lines=TRIPLE[short];f=B.common(lines,B.AVENIR,200,1000,4);step=int(f.size*.90)
   limit=1600 if ig else 1810;bb=f.getbbox(lines[-1],anchor='ma',stroke_width=4);last=limit-bb[3]
   y0=last-2*step
   for n,t in enumerate(lines):B.text(im,tm,(540,y0+n*step),t,f,B.WHITE if n<2 else B.CYAN,4,anchor='ma')
   info['picture_shift']=-shift
  else:
   btm=type_upper(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),short,ig,style)
   im,shift=B.drop_below(im,btm+120);info['picture_shift']=shift
   if style!='yellow':B.ramp(im,0,900,190)
   pic=im.copy();type_upper(im,tm,short,ig,style)
   if style=='frame':ImageDraw.Draw(im).rounded_rectangle((22,22,W-23,H-23),radius=18,outline=B.WHITE,width=4)
  target=OUT/short/platform;target.mkdir(parents=True,exist_ok=True)
  p=target/(ident+'.png');im.convert('RGB').save(p);tm.save(target/(ident+'.text-mask.png'))
  if platform=='youtube':im.convert('RGB').save(p.with_suffix('.jpg'),quality=92)
  face_mask,faces=B.person_mask(im);b=tm.getbbox()
  # Face boxes expanded above detected forehead to include hair and a generous guard.
  guards=[]
  for f in faces:
   x0,y0,x1,y1=map(int,f);fh=y1-y0
   guard=[max(0,x0-30),max(0,y0-int(fh*.60)-25),min(W,x1+30),min(H,y1+25)]
   guards.append(guard)
  ta=np.array(tm)>0;overlap=sum(int(ta[g[1]:g[3],g[0]:g[2]].sum()) for g in guards)
  records.append(dict(short=short,id=ident,platform=platform,path=str(p),sha256=B.sha(p),source=str(source),origin=origin,style=style,copy=COPY[short],text_bounds=b,faces=faces,hair_guards=guards,face_hair_text_pixels=overlap,**info))
for x in plan:make(x,Path(x['out']),x['short'],x['id'],x['layout'],'codex')
for k in 'ABC':
 for i,style in enumerate(['yellow','frame','bottom'],1):make({},w/'google'/k/f'g{i}.jpg',k,f'g{i}',style,'google')
(w/'layout-manifest-private.json').write_text(json.dumps(records,indent=2));print('BUILT',len(records),'layouts')
print('face/hair overlaps',[(r['short'],r['id'],r['platform'],r['face_hair_text_pixels']) for r in records if r['face_hair_text_pixels']])
for k in 'ABC':
 rows=[r for r in records if r['short']==k]
 ids=list(dict.fromkeys(r['id'] for r in rows));s=Image.new('RGB',(len(ids)*270,1000),'#1a2029');d=ImageDraw.Draw(s)
 for i,id in enumerate(ids):
  for j,plat in enumerate(['instagram','youtube']):
   r=next(r for r in rows if r['id']==id and r['platform']==plat);im=Image.open(r['path']);im.thumbnail((270,480));s.paste(im,(i*270,j*500));d.text((i*270+4,j*500+482),id+' '+plat,fill='white')
 s.save(w/(k+'-layout-audit.jpg'))
