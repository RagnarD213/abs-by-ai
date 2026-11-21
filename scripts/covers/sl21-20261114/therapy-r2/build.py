from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,sys,numpy as np
w=Path(__file__).parent
root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI')
sys.path.insert(0,str(root/'scripts/covers/sl08-20261025'))
import build as B
W,H=1080,1920
lines=["If You Can't Afford", "A Gym, You Can't", 'Afford Therapy']
cfg={
 'A':(B.DIN,(255,220,61),(12,24,31),(169,27,28),'left'),
 'B':(B.IMPACT,(8,24,42),(255,255,255),(66,225,230),'right'),
 'C':(B.FUTURA,(255,248,235),(20,28,35),(184,24,30),'right'),
 'D':(B.AVENIR,(6,21,26),(255,255,255),(255,166,55),'left')}
records=[]
(w/'qa').mkdir(exist_ok=True)
for v,(fontspec,bg,fg,accent,patient) in cfg.items():
 src=next(p for p in (w/'sources').glob(v+'.*') if p.suffix in ['.jpg','.png'])
 raw=Image.open(src).convert('RGBA');raw=raw.resize((W,round(raw.height*W/raw.width)),Image.Resampling.LANCZOS)
 _,rf=B.person_mask(raw);assert rf,(v,'no face')
 central=min(rf,key=lambda a:abs((a[0]+a[2])/2-W/2))
 a,b,c,d=central;fh=d-b;hair=b-round(.62*fh)-20
 wall=tuple(int(i) for i in np.array(raw.convert('RGB'))[:70].reshape(-1,3).mean(axis=0))
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';target=850 if ig else 700;shift=target-hair
  im=Image.new('RGBA',(W,H),wall+(255,));im.alpha_composite(raw,(0,shift))
  tm=Image.new('L',(W,H));bubblemask=Image.new('L',(W,H))
  top=252 if ig else 96;f=B.common(lines,fontspec,94,980)
  step=round(f.size*1.04);end=top+step*2+f.getbbox(lines[-1],anchor='mt')[3]+24
  draw=ImageDraw.Draw(im);draw.rectangle((0,0,W,end),fill=bg)
  for i,t in enumerate(lines):B.text(im,tm,(540,top+i*step),t,f,accent if i==2 else fg,anchor='mt')
  # Speech bubble lives in the upper wall. Its tail ends beside Dan's mouth,
  # outside his face and hair guard, on the side of the patient he addresses.
  by=target-265;bb=target-85;assert by>end+8,(v,platform,by,end)
  box=(90,by,990,bb);a,b,c,d=central;b+=shift;d+=shift
  tipx=(a-44) if patient=='left' else (c+44);tipy=round(b+.7*(d-b))
  basex=(a-100) if patient=='left' else (c+100)
  tail=[(basex-28,bb-5),(basex+28,bb-5),(tipx,tipy)]
  bd=ImageDraw.Draw(bubblemask);bd.rounded_rectangle(box,radius=34,fill=255);bd.polygon(tail,fill=255)
  shadow=bubblemask.filter(ImageFilter.GaussianBlur(10));sh=Image.new('RGBA',(W,H),(0,0,0,0));sh.putalpha(shadow.point(lambda x:round(x*.4)));im.alpha_composite(sh,(0,8))
  draw=ImageDraw.Draw(im);draw.polygon(tail,fill='white',outline=bg,width=5);draw.rounded_rectangle(box,radius=34,fill='white',outline=bg,width=5)
  sf=B.common(["You're getting",'scammed.'],B.DIN,80,810)
  sy=by+19;ss=round(sf.size*.94)
  for i,t in enumerate(["You're getting",'scammed.']):B.text(im,tm,(540,sy+i*ss),t,sf,(14,27,38) if i==0 else (181,24,27),anchor='mt')
  _,faces=B.person_mask(im);assert faces
  guards=[];ta=np.array(tm)>0;ba=np.array(bubblemask)>0
  for a,b,c,d in faces:
   fh=d-b;guards.append([max(0,a-20),max(0,b-round(.62*fh)-20),min(W,c+20),min(H,d+20)])
  overlap=sum(int(ta[b:d,a:c].sum()) for a,b,c,d in guards)
  bubble_overlap=sum(int(ba[b:d,a:c].sum()) for a,b,c,d in guards)
  assert overlap==0,(v,platform,'type',overlap)
  assert bubble_overlap==0,(v,platform,'bubble',bubble_overlap)
  bounds=tm.getbbox();assert bounds[0]>=20 and bounds[2]<=1060
  assert bounds[1]>=(240 if ig else 50) and bounds[3]<=(1620 if ig else 1840)
  out=w/'layouts'/platform;out.mkdir(parents=True,exist_ok=True);p=out/(v+'.png');im.convert('RGB').save(p)
  tm.save(w/'qa'/f'{v}-{platform}-type.png');bubblemask.save(w/'qa'/f'{v}-{platform}-bubble.png')
  if not ig:im.convert('RGB').save(p.with_suffix('.jpg'),quality=92);assert p.with_suffix('.jpg').stat().st_size<2_000_000
  records.append({'id':v,'platform':platform,'path':str(p),'sha256':B.sha(p),'headline':lines,'bubble':"You're getting scammed.",'text_bounds':bounds,'faces':faces,'hair_guards':guards,'face_hair_text_pixels':overlap,'face_hair_bubble_pixels':bubble_overlap,'full_source_width_preserved':True,'vertical_shift':shift,'central_source_face':central})
  print(v,platform,'PASS',flush=True)
(w/'layout-manifest-private.json').write_text(json.dumps(records,indent=2))
s=Image.new('RGB',(1080,1020),'#111b28');d=ImageDraw.Draw(s)
for i,v in enumerate(cfg):
 for j,platform in enumerate(['instagram','youtube']):
  p=w/'layouts'/platform/(v+'.png');im=Image.open(p);im.thumbnail((270,480));s.paste(im,(i*270,j*510+25));d.text((i*270+5,j*510+5),v+' '+platform,fill='white')
s.save(w/'audit.jpg');print('BUILT',len(records),flush=True)
