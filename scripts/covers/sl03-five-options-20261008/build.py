#!/usr/bin/env python3
"""SL-03 Daily Salad: five cover choices per short (A pool, B studio, C video screenshot, D/E Codex designs), two layouts each.
Real photos are never redrawn: Codex makes plates only; cutouts, photos, frames and all type are layered in code."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np
P=Path(__file__).resolve().parents[3];R=P/'Short-form video content/covers/review/sl03-covers-20261008';PH=P/'photos/finalized social media photos';CUT=PH/'_cutouts';W,H=1080,1920
IMPACT='/System/Library/Fonts/Supplemental/Impact.ttf';ARIAL='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
COPY={1:('INTERMITTENT FASTING',['BREAK YOUR FAST','WITH THIS'],'break-your-fast-with-this'),
 2:('MEAL PREP',['THE $20 SALAD YOU','CAN MAKE FOR $4'],'the-20-dollar-salad-for-4'),
 3:('MEAL PREP',['KEEP YOUR SALADS','FRESH FOR 7 DAYS'],'keep-salads-fresh-7-days'),
 4:('DAILY SALAD',['STOP BUYING','SALAD DRESSING'],'stop-buying-salad-dressing'),
 5:('AI MACRO TRACKING',['TRACK A WEEK OF MEALS','FROM 1 PHOTO'],'track-a-week-of-meals-from-1-photo'),
 6:('AI CALORIE TRACKING',['THE ONE LINE THAT','MAKES IT ACCURATE'],'the-one-line-that-makes-it-accurate')}
# pool photo: person-mask bbox as fractions (x0,x1,top) of the full photo
POOL={1:('photo-247',(.1284,.7468,.1227,.9994)),2:('photo-273',(.0856,.8342,.1142,.9530)),3:('photo-244',(.3124,.8379,.1239,.9628)),
      4:('photo-228',(.2077,.9517,.1966,.9994)),5:('photo-276',(.0792,.7787,.1172,.9719)),6:('photo-289',(.1658,.7878,.1667,.9872))}
STUDIO={1:'studio-blue-110',2:'studio-blue-34',3:'studio-white-4',4:'studio-blue-213',5:'studio-white-57',6:'studio-white-84'}
SHOT={1:'short1-t12.0.png',2:'short2-t6.25.png',3:'short3-t27.5.png',4:'short4-t34.25.png',5:'short5-t17.5.png',6:'short6-t49.75.png'}
ACC={'A':((36,139,197),(18,170,196)),'B':((255,214,0),(255,54,54)),'C':((40,220,255),(18,170,196)),'D':((255,214,0),(255,54,54)),'E':((20,20,20),None)}
KIND={'A':'Pool photo','B':'Studio photo on topic scene','C':'Video screenshot','D':'Codex design 1','E':'Codex design 2'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(path,size):return ImageFont.truetype(path,size)
def fit(txt,path,start,maxw,stroke=0):
 for size in range(start,23,-2):
  f=font(path,size);b=f.getbbox(txt,stroke_width=stroke)
  if b[2]-b[0]<=maxw:return f
 raise ValueError(txt)
def text(canvas,mask,xy,txt,f,fill,stroke=0,sf=(8,11,15)):
 ImageDraw.Draw(canvas).text(xy,txt,font=f,fill=fill,stroke_width=stroke,stroke_fill=sf);ImageDraw.Draw(mask).text(xy,txt,font=f,fill=255,stroke_width=stroke,stroke_fill=255)
def draw_copy(canvas,mask,n,platform,kind):
 badge,lines,_=COPY[n];ig=platform=='instagram';by=256 if ig else 70;ty=330 if ig else 144
 accent,bcol=ACC[kind]
 if kind=='E':  # solid yellow band, black type: a different design language from the others
  band_top=(236 if ig else 52);f1=fit(lines[0],IMPACT,160,940);f2=fit(lines[1],IMPACT,160,940);sz=min(f1.size,f2.size);f=font(IMPACT,sz);step=round(sz*1.0)
  fb=fit(badge,ARIAL,40,890);bw=fb.getbbox(badge)[2]
  d=ImageDraw.Draw(canvas);bh=62+16+2*step+36
  d.rectangle((0,band_top,W,band_top+bh),fill=(255,214,0));ImageDraw.Draw(mask).rectangle((0,band_top,W,band_top+bh),fill=255)
  d.rectangle((52,band_top+22,52+bw+46,band_top+84),fill=(12,12,12));text(canvas,mask,(75,band_top+26),badge,fb,(255,214,0))
  for i,ln in enumerate(lines):text(canvas,mask,(54,band_top+80+i*step-6),ln,f,(12,12,12) if i==0 else (200,30,30))
  return accent
 f=fit(badge,ARIAL,40,890);b=f.getbbox(badge);bw=b[2]-b[0]
 ImageDraw.Draw(canvas).rounded_rectangle((55,by-5,55+bw+46,by+62),radius=14,fill=bcol);text(canvas,mask,(78,by+5),badge,f,(255,255,255))
 fs=[fit(ln,IMPACT,170,958,6) for ln in lines];common=min(x.size for x in fs);f=font(IMPACT,common);step=round(common*0.96)
 for i,ln in enumerate(lines):text(canvas,mask,(57,ty+i*step),ln,f,(255,255,250) if i==0 else accent,6)
 return accent
def plate(n,which,gradient=True):
 p=R/'assets/gen'/f'S{n}-{which}.png';full=ImageOps.fit(Image.open(p).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
 if (n,which)==(3,'x'):  # first container sat under the headline: shrink the plate, sit it lower on a blurred, darkened copy of itself
  bg=full.filter(ImageFilter.GaussianBlur(40)).point(lambda q:int(q*0.45));sm=full.resize((round(W*0.86),round(H*0.86)),Image.Resampling.LANCZOS)
  m=Image.new('L',sm.size,255);md=ImageDraw.Draw(m)
  for i in range(60):md.rectangle((i,i,sm.width-i,sm.height-i),outline=int(255*i/60))
  bg.paste(sm,((W-sm.width)//2,H-sm.height-8),m);full=bg
 im=full.convert('RGBA')
 if gradient:
  a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[4,7,12]
  for y in range(H):a[y,:,3]=int(205*max(0,1-y/820)**0.85)
  im.alpha_composite(Image.fromarray(a))
 return im,p
def pool(n,platform):
 stem,(x0,x1,top,ymax)=POOL[n];p=PH/(stem+'_FINAL_PRIMARY.jpg');raw=Image.open(p).convert('RGB');sw,sh=raw.size
 ig=platform=='instagram';py=738 if ig else 574;ph=H-py;asp=W/ph;bw=(x1-x0)*sw;limit=1640 if ig else 1800
 y=int(max(0,top*sh-0.03*sh));assert y<top*sh;abs_b=(top+0.56*(ymax-top))*sh   # abs bottom (waistband) estimated from the person mask
 ch=int(max(0.52*sh,bw*1.06/asp,(abs_b-y)*ph/(limit-py)));cw=int(ch*asp)
 if cw>sw:cw=sw;ch=int(cw/asp)
 cx=int((x0+x1)/2*sw);x=max(0,min(cx-cw//2,sw-cw));y=min(y,sh-ch)
 pic=raw.crop((x,y,x+cw,y+ch)).resize((W,ph),Image.Resampling.LANCZOS);k=ph/ch
 return pic,py,dict(source=str(p),source_sha256=sha(p),source_crop=[x,y,x+cw,y+ch],photo_top=py,source_head_y=round(top*sh),rendered_head_y=round(py+(top*sh-y)*k,1),rendered_abs_bottom=round(py+(abs_b-y)*k,1),full_body_width_in_crop=round(bw/cw,3))
def studio(im,n,platform):
 stem=STUDIO[n];p=CUT/(stem+'_CUTOUT.png');sub=Image.open(p).convert('RGBA');b=sub.getchannel('A').getbbox();sub=sub.crop(b)
 top=738 if platform=='instagram' else 574;k=min(1000/sub.width,(1700-top)/(sub.height*0.62));sub=sub.resize((round(sub.width*k),round(sub.height*k)),Image.Resampling.LANCZOS)
 pad=22;box=Image.new('RGBA',(sub.width+2*pad,sub.height+2*pad));box.alpha_composite(sub,(pad,pad));alpha=box.getchannel('A');x=(W-sub.width)//2-pad;y=top-pad
 sh=Image.new('RGBA',box.size,(0,0,0));sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(15)).point(lambda q:int(q*0.35)));im.alpha_composite(sh,(x+8,y+12))
 line=Image.new('RGBA',box.size,(255,255,250));line.putalpha(alpha.filter(ImageFilter.MaxFilter(17)));im.alpha_composite(line,(x,y));im.alpha_composite(box,(x,y))
 sm=Image.new('L',(W,H));sm.paste(alpha,(x,y))
 return sm,dict(source=str(p),source_sha256=sha(p),source_alpha_crop=list(b),scale=round(k,4),subject_top=top,subject_width=sub.width,subject_height=sub.height)
def shot(n,platform):
 p=R/'sources'/SHOT[n];raw=Image.open(p).convert('RGB');py=738 if platform=='instagram' else 574;ph=H-py;y0=320
 pic=raw.crop((0,y0,W,y0+ph));return pic,py,dict(source=str(p),source_sha256=sha(p),crop=[0,y0,W,y0+ph],photo_top=py,timestamp=SHOT[n].split('-t')[1][:-4])
def build():
 records=[]
 for n in range(1,7):
  for v in 'ABCDE':
   for platform in ['instagram','youtube']:
    out=R/platform;out.mkdir(exist_ok=True);slug=f'daily-salad-short{n}_{COPY[n][2]}_cover-{v}';p=out/(slug+'.png');tm=Image.new('L',(W,H));sm=None;extra={}
    if v=='A':
     im=Image.new('RGBA',(W,H),(7,15,25));pic,py,info=pool(n,platform);im.paste(pic,(0,py))
    elif v=='B':
     im,gp=plate(n,'studio');sm,info=studio(im,n,platform);info['plate']=str(gp);info['plate_sha256']=sha(gp)
    elif v=='C':
     im=Image.new('RGBA',(W,H),(7,15,25));pic,py,info=shot(n,platform);im.paste(pic,(0,py))
     ramp=Image.new('L',(W,35));d=ImageDraw.Draw(ramp)
     for y in range(35):d.line((0,y,W,y),fill=round(80*(1-y/35)))
     im.paste(Image.new('RGBA',(W,35),(7,12,20)),(0,py),ramp)
    elif v=='D':
     im,gp=plate(n,'x');info=dict(plate=str(gp),plate_sha256=sha(gp))
    else:
     im,gp=plate(n,'y',gradient=False);info=dict(plate=str(gp),plate_sha256=sha(gp))
     if n==4:  # red X over the three store-dressing bottles (drawn in code, not generated)
      dd=ImageDraw.Draw(im)
      for a,b in [((70,930),(380,1330)),((380,930),(70,1330))]:
       dd.line([a,b],fill=(0,0,0),width=44);dd.line([a,b],fill=(238,40,40),width=30)
    accent=draw_copy(im,tm,n,platform,v);d=ImageDraw.Draw(im)
    if v!='E':d.rounded_rectangle((24,24,W-25,H-25),radius=22,outline=(255,255,250),width=4);d.line((45,1872,1035,1872),fill=accent if v!='E' else (255,214,0),width=6)
    im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
    if sm is not None:(R/'composite-masks'/platform).mkdir(parents=True,exist_ok=True);sm.save(R/'composite-masks'/platform/(slug+'.png'))
    g=R/'grid-crops';g.mkdir(exist_ok=True)
    if platform=='instagram':Image.open(p).crop((0,240,1080,1680)).save(g/(slug+'.png'))
    ph=R/'phone'/platform;ph.mkdir(parents=True,exist_ok=True);Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(ph/(slug+'.jpg'),quality=95)
    records.append(dict(short=n,variant=v,platform=platform,path=str(p),sha256=sha(p),kind=KIND[v],copy={'badge':COPY[n][0],'headline':COPY[n][1]},**info))
 (R/'manifest.json').write_text(json.dumps({'status':'awaiting Dan picks','outputs':records},indent=1)+'\n');print('built',len(records))
if __name__=='__main__':build()
