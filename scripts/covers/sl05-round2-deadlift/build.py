#!/usr/bin/env python3
"""SL-05 R2: five generated deadlift photographs, two warning designs, two platforms."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps,ImageEnhance
import numpy as np,json,hashlib
P=Path(__file__).resolve().parents[3];R=P/'Short-form video content/covers/review/sl05-covers-20261001/round2-deadlift';W,H=1080,1920
F='/System/Library/Fonts/Supplemental/Impact.ttf';A='/System/Library/Fonts/Supplemental/Arial Bold.ttf';RED=(245,42,43)
COPY={1:('STOP DOING DEADLIFTS',['MORE INJURIES THAN','EVERY OTHER LIFT'],'deadlifts-cause-more-injuries'),2:('BUILD MORE MUSCLE',['SAFER LIFTS WIN','LONG TERM'],'safer-lifts-build-more-muscle'),3:('WANT AN AESTHETIC BODY?',['DEADLIFTS BUILD A','POWERLIFTER BODY'],'deadlifts-build-a-powerlifter-body'),4:('SKIP THE DEADLIFT',['2 BACK EXERCISES','TO DO INSTEAD'],'two-back-exercises-instead-of-deadlifts'),5:('SKIP THE DEADLIFT',['TRAIN LEGS WITHOUT','DEADLIFTS'],'train-legs-without-deadlifts')}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fit(txt,path,start,maxw,stroke=0):
 for size in range(start,25,-1):
  f=ImageFont.truetype(path,size);b=f.getbbox(txt,stroke_width=stroke)
  if b[2]-b[0]<=maxw:return f
 raise ValueError(txt)
def text(im,tm,xy,txt,f,fill,stroke=0):
 ImageDraw.Draw(im).text(xy,txt,font=f,fill=fill,stroke_width=stroke,stroke_fill=(8,11,16))
 ImageDraw.Draw(tm).text(xy,txt,font=f,fill=255,stroke_width=stroke,stroke_fill=255)
records=[]
for n in range(1,6):
 src=R/'assets'/f'short{n}-powerlifter.png';raw=Image.open(src).convert('RGB');pm=np.array(Image.open(R/'source-masks'/f'short{n}-powerlifter.mask.png'))>127;ys,xs=np.where(pm);hair=int(ys.min());crop=(0,max(0,hair-75),raw.width,raw.height)
 for v in 'AB':
  for platform in ['instagram','youtube']:
   ig=platform=='instagram';by=260 if ig else 88;ty=346 if ig else 174;stage_top=660 if ig else 510;stage_bottom=1670 if ig else 1840
   if v=='A':
    wall=raw.crop((0,0,raw.width,max(100,hair-100)));im=ImageOps.fit(wall,(W,H),method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(18));im=ImageEnhance.Brightness(im).enhance(.58).convert('RGBA')
   else:im=Image.new('RGBA',(W,H),(244,242,236))
   pic=raw.crop(crop);k=min((stage_bottom-stage_top)/pic.height,1010/pic.width);size=(round(pic.width*k),round(pic.height*k));pic=pic.resize(size,Image.Resampling.LANCZOS);x=(W-size[0])//2;y=stage_top+(stage_bottom-stage_top-size[1])//2
   if v=='B':pic=ImageOps.grayscale(pic).convert('RGB');pic=ImageEnhance.Contrast(pic).enhance(1.10)
   alpha=Image.new('L',size,255);ad=ImageDraw.Draw(alpha)
   if v=='A':
    for yy in range(45):ad.line((0,yy,size[0],yy),fill=round(255*yy/44))
   else:
    ImageDraw.Draw(im).rounded_rectangle((x-14,y-14,x+size[0]+14,y+size[1]+14),radius=12,fill=(255,255,255),outline=RED,width=5)
   im.paste(pic,(x,y),alpha)
   head_y=y+(hair-crop[1])*k;center=(round(x+raw.width*.53*k),round(head_y+580*k));mark=Image.new('RGBA',(W,H));d=ImageDraw.Draw(mark)
   if v=='A':
    span=round(245*k);width=round(58*k)
    for aa,bb in [((center[0]-span,center[1]-span),(center[0]+span,center[1]+span)),((center[0]+span,center[1]-span),(center[0]-span,center[1]+span))]:
     d.line((aa,bb),fill=(10,10,10,240),width=width+12);d.line((aa,bb),fill=RED+(255,),width=width)
   else:
    rad=round(310*k);width=max(18,round(38*k));d.ellipse((center[0]-rad,center[1]-rad,center[0]+rad,center[1]+rad),outline=RED+(255,),width=width);dd=round(rad*.69);d.line((center[0]-dd,center[1]+dd,center[0]+dd,center[1]-dd),fill=RED+(255,),width=width)
   im.alpha_composite(mark)
   tm=Image.new('L',(W,H));badge,lines,slug=COPY[n];bf=fit(badge,A,40,935);b=bf.getbbox(badge);ImageDraw.Draw(im).rounded_rectangle((54,by-5,54+b[2]-b[0]+44,by+60),radius=10,fill=RED);text(im,tm,(76,by+4),badge,bf,(255,255,255))
   stroke=5 if v=='A' else 0;fs=min(fit(ln,F,152,962,stroke).size for ln in lines);ff=ImageFont.truetype(F,fs);step=round(fs*1.01)
   for i,ln in enumerate(lines):text(im,tm,(54,ty+i*step),ln,ff,(255,255,247) if v=='A' and i==0 else ((255,211,36) if v=='A' else (24,28,33) if i==0 else RED),stroke)
   ImageDraw.Draw(im).line((44,1878,1036,1878),fill=RED,width=7)
   if v=='A':ImageDraw.Draw(im).rounded_rectangle((23,23,1056,1896),radius=16,outline=(255,255,255),width=3)
   out=R/platform;out.mkdir(parents=True,exist_ok=True);name=f'stop-deadlifting-short{n}_{slug}_cover-R2{v}.png';p=out/name;im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'));mark.getchannel('A').save(p.with_name(p.stem+'.warning-mask.png'))
   phone=R/'phone'/platform;phone.mkdir(parents=True,exist_ok=True);im.convert('RGB').resize((270,480),Image.Resampling.LANCZOS).save(phone/(p.stem+'.jpg'),quality=95)
   grid=R/'grid-crops';grid.mkdir(exist_ok=True)
   if ig:im.convert('RGB').crop((0,240,1080,1680)).save(grid/name)
   records.append(dict(short=n,variant=v,platform=platform,path=str(p),sha256=sha(p),source=str(src),source_sha256=sha(src),source_crop=list(crop),source_hair_y=hair,subject_photo_box=[x,y,x+size[0],y+size[1]],rendered_hair_y=round(head_y,1),scale=k,warning_center=list(center),copy={'badge':badge,'headline':lines},kind='Color / big red X' if v=='A' else 'Monochrome / red prohibition mark'))
m={'round':2,'status':'awaiting Dan picks','requested_mix':'Dan rejected R1 and requested one new powerlifter deadlift image and two designs for each short. This overrides the prior five-photo mix.','generation':{'tool':'built-in image_gen','new_images':5,'cost_usd':None,'external_metered_spend_usd':0},'outputs':records}
(R/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Built 20 R2 review covers.')
