#!/usr/bin/env python3
"""Five-choice SL-05 review. Native layout over real photos and generated scene plates."""
from pathlib import Path
import json,hashlib,shutil,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np
P=Path(__file__).resolve().parents[3];R=P/'Short-form video content/covers/review/sl05-covers-20261001';CUT=P/'photos/finalized social media photos/_cutouts';W,H=1080,1920
IMPACT='/System/Library/Fonts/Supplemental/Impact.ttf';ARIAL='/System/Library/Fonts/Supplemental/Arial Bold.ttf';MANROPE='/Users/danielrose/Library/Fonts/Manrope.ttf'
COPY={
 1:('STOP DOING DEADLIFTS',['MORE INJURIES THAN','EVERY OTHER LIFT'],'deadlifts-cause-more-injuries'),
 2:('BUILD MORE MUSCLE',['SAFER LIFTS WIN','LONG TERM'],'safer-lifts-build-more-muscle'),
 3:('WANT AN AESTHETIC BODY?',['DEADLIFTS BUILD A','POWERLIFTER BODY'],'deadlifts-build-a-powerlifter-body'),
 4:('SKIP THE DEADLIFT',['2 BACK EXERCISES','TO DO INSTEAD'],'two-back-exercises-instead-of-deadlifts'),
 5:('SKIP THE DEADLIFT',['TRAIN LEGS WITHOUT','DEADLIFTS'],'train-legs-without-deadlifts')}
SOURCES={
 1:{'B':('studio-blue-249',3300),'C':('studio-blue-201',3580),'E':('studio-blue-127',3420)},
 2:{'B':('studio-blue-145',3320),'C':('studio-white-23',3480),'E':('studio-blue-9',3430)},
 3:{'B':('studio-gray-79',3920),'C':('studio-blue-53',3770),'E':('studio-white-59',3300)},
 4:{'B':('studio-white-13',3270),'C':('studio-blue-249',3300),'E':('studio-gray-9',3300)},
 5:{'B':('studio-white-23',3480),'C':('studio-blue-145',3320),'E':('studio-blue-127',3420)}}
SCREENS={1:('short1-122.png',122,440,1470,None),2:('short2-264.png',264,430,1460,None),3:('short3-334.png',334,480,1500,None),4:('short4-406.png',406,405,1450,None),5:('short5-456.png',456,440,1480,None)}
POOL={1:('photo-13',(0.44,0.185,0.65),925,[880,2050,1670,2700]),2:('photo-221',(0.45,0.13,0.75),671,[775,2100,1740,2780]),3:('photo-14',(0.50,0.22,0.65),1071,[1000,2310,1800,2930]),4:('photo-223',(0.55,0.075,0.82),398,[1000,2050,1740,2700]),5:('photo-13',(0.44,0.185,0.65),925,[880,2050,1670,2700])}
records=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(path,size):
 f=ImageFont.truetype(path,size)
 if path==MANROPE:f.set_variation_by_name('ExtraBold')
 return f
def fit(txt,path,start,maxw,stroke=0):
 for size in range(start,23,-2):
  f=font(path,size);b=f.getbbox(txt,stroke_width=stroke)
  if b[2]-b[0]<=maxw:return f
 raise ValueError(txt)
def text(canvas,mask,xy,txt,f,fill,stroke=0):
 d=ImageDraw.Draw(canvas);md=ImageDraw.Draw(mask)
 d.text(xy,txt,font=f,fill=fill,stroke_width=stroke,stroke_fill=(8,11,15));md.text(xy,txt,font=f,fill=255,stroke_width=stroke,stroke_fill=255)
def draw_copy(canvas,mask,n,platform,kind):
 badge,lines,_=COPY[n];ig=platform=='instagram';by=256 if ig else 70;ty=330 if ig else 144
 accent=(255,214,0) if kind=='B' else ((40,220,255) if kind in ['C','D'] else (36,139,197))
 if kind=='E':
  f=fit(badge,ARIAL,38,935);ImageDraw.Draw(canvas).line((60,by+49,250,by+49),fill=(36,139,197),width=8);text(canvas,mask,(60,by),badge,f,(18,33,47));path=MANROPE;maxsize=126;stroke=0
 else:
  f=fit(badge,ARIAL,40,890);b=f.getbbox(badge);bw=b[2]-b[0];ImageDraw.Draw(canvas).rounded_rectangle((55,by-5,55+bw+46,by+62),radius=14,fill=((255,54,54) if kind=='B' else (18,170,196)));text(canvas,mask,(78,by+5),badge,f,(255,255,255));path=IMPACT;maxsize=170;stroke=6
 fs=[fit(ln,path,maxsize,958,stroke) for ln in lines];common=min(f.size for f in fs);f=font(path,common);step=round(common*0.96)
 for i,ln in enumerate(lines):
  color=((18,33,47) if i==0 else (26,113,165)) if kind=='E' else ((255,255,250) if i==0 else accent)
  text(canvas,mask,(57,ty+i*step),ln,f,color,stroke)
 return accent

def scene(kind):
 if kind=='E':
  a=np.zeros((H,W,3),np.uint8)
  for y in range(H):a[y,:,:]=[round(245-10*y/H),round(249-9*y/H),round(252-7*y/H)]
  im=Image.fromarray(a).convert('RGBA');d=ImageDraw.Draw(im);d.ellipse((40,735,1050,1760),fill=(216,234,245),outline=(172,207,227),width=3);d.line((70,1820,1010,1820),fill=(36,139,197),width=6);return im
 p=R/'assets'/('gym-red.png' if kind=='B' else 'gym-blue.png');im=ImageOps.fit(Image.open(p).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
 a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[4,7,12]
 for y in range(H):a[y,:,3]=int(150*max(0,1-y/760)**0.8)
 im.alpha_composite(Image.fromarray(a));return im

def place_studio(im,n,v,platform):
 stem,abs_y=SOURCES[n][v];p=CUT/(stem+'_CUTOUT.png');sub=Image.open(p).convert('RGBA');b=sub.getchannel('A').getbbox();x0,y0,x1,y1=b;top=738 if platform=='instagram' else 574;abs_target=1628 if platform=='instagram' else 1558
 k=min((abs_target-top)/(abs_y-y0),976/(x1-x0));sub=sub.crop(b);sub=sub.resize((round(sub.width*k),round(sub.height*k)),Image.Resampling.LANCZOS)
 # Padding keeps the white outline intact rather than clipped at alpha bounds.
 pad=22;box=Image.new('RGBA',(sub.width+2*pad,sub.height+2*pad));box.alpha_composite(sub,(pad,pad));alpha=box.getchannel('A');x=(W-sub.width)//2-pad;y=top-pad
 shadow=Image.new('RGBA',box.size,(0,0,0));shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(15)).point(lambda q:int(q*0.35)))
 im.alpha_composite(shadow,(x+8,y+12))
 if v!='E':
  line=Image.new('RGBA',box.size,(255,255,250));line.putalpha(alpha.filter(ImageFilter.MaxFilter(17)));im.alpha_composite(line,(x,y))
 im.alpha_composite(box,(x,y));sm=Image.new('L',(W,H));sm.paste(alpha,(x,y))
 return sm,dict(source=str(p),source_sha256=sha(p),source_alpha_crop=list(b),subject_position=[x+pad,top],scale=k,source_abs_bottom=abs_y,rendered_abs_bottom=round(top+(abs_y-y0)*k,1),portrait_unchanged=True)

def screen(im,n,platform):
 source,t,x0,x1,abs_y=SCREENS[n];p=R/'assets'/f'screenshot-{n}-enhanced.png';raw=Image.open(p).convert('RGB');raw=raw.resize((1920,1080),Image.Resampling.LANCZOS)
 py=788 if platform=='instagram' else 624;ph=H-py;cw=x1-x0;ch=round(cw*ph/W)
 if ch>1080:ch=1080;cw=round(ch*W/ph);cx=(x0+x1)/2;x0=round(cx-cw/2);x1=x0+cw
 crop=[x0,0,x1,ch];pic=raw.crop(crop).resize((W,ph),Image.Resampling.LANCZOS);im.paste(pic,(0,py))
 # A short transition along the picture edge, entirely above the photographed hair.
 ramp=Image.new('L',(W,35));d=ImageDraw.Draw(ramp)
 for y in range(35):d.line((0,y,W,y),fill=round(80*(1-y/35)))
 im.paste(Image.new('RGBA',(W,35),(7,12,20)),(0,py),ramp)
 return dict(source=str((R/'sources'/source).resolve()),source_sha256=sha(R/'sources'/source),timestamp_seconds=t,enhanced_source=str(p),enhanced_sha256=sha(p),crop=crop,photo_top=py,rendered_abs_bottom=None)

def pool(im,n,platform):
 stem,(cx,top,height),hair,ab=POOL[n];p=P/'photos/finalized social media photos'/(stem+'_FINAL_PRIMARY.jpg');raw=Image.open(p).convert('RGB');sw,sh=raw.size;py=738 if platform=='instagram' else 574;ph=H-py;ch=int(sh*height);cw=int(ch*W/ph);x=max(0,min(int(sw*cx)-cw//2,sw-cw));y=max(0,min(int(sh*top),sh-ch));assert y<hair
 im.paste(raw.crop((x,y,x+cw,y+ch)).resize((W,ph),Image.Resampling.LANCZOS),(0,py))
 k=W/cw;box=[round((ab[0]-x)*k,1),round(py+(ab[1]-y)*k,1),round((ab[2]-x)*k,1),round(py+(ab[3]-y)*k,1)]
 return dict(source=str(p),source_sha256=sha(p),source_crop=[x,y,x+cw,y+ch],photo_top=py,source_hair_y=hair,rendered_hair_y=round(py+(hair-y)*k,1),rendered_abs_region=box,rendered_abs_bottom=box[3])

for n in [1,2,3,4,5]:
 for v in ['A','B','C','D','E']:
  for platform in ['instagram','youtube']:
   out=R/platform;out.mkdir(exist_ok=True);slug=f'stop-deadlifting-short{n}_{COPY[n][2]}_cover-{v}';p=out/(slug+'.png');tm=Image.new('L',(W,H));sm=None
   im=scene(v) if v in ['B','C','E'] else Image.new('RGBA',(W,H),(7,15,25))
   if v=='A':info=pool(im,n,platform)
   elif v=='D':info=screen(im,n,platform)
   else:sm,info=place_studio(im,n,v,platform)
   accent=draw_copy(im,tm,n,platform,v);d=ImageDraw.Draw(im)
   if v!='E':d.rounded_rectangle((24,24,W-25,H-25),radius=22,outline=(255,255,250),width=4);d.line((45,1872,1035,1872),fill=accent,width=6)
   im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
   if sm is not None:
    (R/'composite-masks'/platform).mkdir(parents=True,exist_ok=True);sm.save(R/'composite-masks'/platform/(slug+'.png'))
   grid=R/'grid-crops';grid.mkdir(exist_ok=True)
   if platform=='instagram':Image.open(p).crop((0,240,1080,1680)).save(grid/(slug+'.png'))
   phone=R/'phone'/platform;phone.mkdir(parents=True,exist_ok=True);Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(phone/(slug+'.jpg'),quality=95)
   records.append(dict(short=n,variant=v,platform=platform,path=str(p),sha256=sha(p),kind={'A':'Pool photo','B':'Studio / red gym','C':'Studio / blue home gym','D':'Enhanced video screenshot','E':'Designer choice / clean editorial'}[v],copy={'badge':COPY[n][0],'headline':COPY[n][1]},**info))
manifest={'status':'awaiting Dan picks','options_per_video':5,'platforms':['instagram','youtube'],'outputs':records,'generation':{'tool':'built-in image_gen','cost_usd':None,'cost_note':'Dollar cost not reported by built-in tool; no external paid API calls.'}}
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built 50 review PNGs.')
