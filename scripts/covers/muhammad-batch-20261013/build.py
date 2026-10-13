#!/usr/bin/env python3
"""Muhammad dedicated Shorts: five cover choices per short, two layouts each (Instagram grid, YouTube).
A pool photo, B studio cutout on a Codex scene, C/D/E three Codex designs, each its own layout:
C yellow band on top, D headline stacked at the bottom, E two panels with a black band across the middle.
Real photos are never redrawn: Codex makes plates only; cutouts, photos and all type are layered in code."""
from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np
P=Path(__file__).resolve().parents[3];R=P/'Short-form video content/covers/review/muhammad-batch-20261013';PH=P/'photos/finalized social media photos';CUT=PH/'_cutouts';W,H=1080,1920
IMPACT='/System/Library/Fonts/Supplemental/Impact.ttf';ARIAL='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
# key: (badge, [headline line 1, line 2], file slug, post title)
COPY={'ds-12':('LOOKSMAXXING',['TOP 3 WAYS','TO LOOKSMAX'],'ds-12_top-3-ways-to-looksmax','Top 3 Ways To Looksmax'),
 'ds-23':('WIDER SHOULDERS',['HOW TO DO','SIDE LATERALS'],'ds-23_how-to-do-side-laterals','How To Do Side Laterals'),
 'ds-08':('MY STORY',['I WAS 200 POUNDS','AT 38'],'ds-08_i-was-200-pounds-at-38','I Was 200 Pounds At 38'),
 'ds-09':('TOO BUSY?',['HOW TO MAKE TIME','TO WORK OUT'],'ds-09_how-to-make-time-to-work-out','How To Make Time To Work Out'),
 'ds-22':('SIX-PACK ABS',['HOW TO USE','THE AB WHEEL'],'ds-22_how-to-use-the-ab-wheel','How To Use The Ab Wheel'),
 'ds-14':('GET LEAN',['3 WAYS TO','REDUCE ALCOHOL'],'ds-14_3-ways-to-reduce-alcohol','3 Ways To Reduce Alcohol'),
 'ds-24':('SHOULDERS',['HOW TO DO','REAR DELT FLYS'],'ds-24_how-to-do-rear-delt-flys','How To Do Rear Delt Flys'),
 'ds-21':('BIGGER ARMS',['HOW TO DO','HAMMER CURLS'],'ds-21_how-to-do-hammer-curls','How To Do Hammer Curls')}
ORDER=list(COPY)
# pool photo: person-mask bbox as fractions (x0,x1,top,ymax) of the full photo
POOL={'ds-12':('photo-10',(0.1631,0.7656,0.2314,0.9998)),'ds-23':('photo-223',(.2996,.8136,.0972,.9998)),'ds-08':('photo-221',(.1489,.7539,.1638,.9998)),
 'ds-09':('photo-258',(.1940,.9996,.1753,.9998)),'ds-22':('photo-251',(.1270,.7779,.0833,.9998)),'ds-14':('photo-14',(0.2381,0.7703,0.2615,0.9998)),
 'ds-24':('photo-13',(.1296,.7073,.2258,.9998)),'ds-21':('photo-125',(.0357,.9760,.2148,.9998))}
STUDIO={'ds-12':'studio-blue-111','ds-23':'studio-gray-79','ds-08':'studio-white-23','ds-09':'studio-blue-169','ds-22':'studio-gray-4','ds-14':'studio-white-42','ds-24':'studio-blue-247','ds-21':'studio-blue-123'}
ACC={'A':((40,220,255),(18,170,196)),'B':((255,214,0),(255,54,54))}
KIND={'A':'Pool photo','B':'Studio photo on topic scene','C':'Codex design 1: yellow band','D':'Codex design 2: headline at the bottom','E':'Codex design 3: two panels'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(path,size):return ImageFont.truetype(path,size)
def fit(txt,path,start,maxw,stroke=0):
 for size in range(start,23,-2):
  f=font(path,size);b=f.getbbox(txt,stroke_width=stroke)
  if b[2]-b[0]<=maxw:return f
 raise ValueError(txt)
def text(canvas,mask,xy,txt,f,fill,stroke=0,sf=(8,11,15),anchor='la'):
 ImageDraw.Draw(canvas).text(xy,txt,font=f,fill=fill,stroke_width=stroke,stroke_fill=sf,anchor=anchor);ImageDraw.Draw(mask).text(xy,txt,font=f,fill=255,stroke_width=stroke,stroke_fill=255,anchor=anchor)
def box(canvas,mask,xyxy,fill,radius=0):
 ImageDraw.Draw(canvas).rounded_rectangle(xyxy,radius=radius,fill=fill);ImageDraw.Draw(mask).rounded_rectangle(xyxy,radius=radius,fill=255)
def copy_house(canvas,mask,k,ig,kind):
 badge,lines=COPY[k][:2];by=256 if ig else 70;ty=330 if ig else 144;accent,bcol=ACC[kind]
 f=fit(badge,ARIAL,40,890);bw=f.getbbox(badge)[2]
 ImageDraw.Draw(canvas).rounded_rectangle((55,by-5,55+bw+46,by+62),radius=14,fill=bcol);text(canvas,mask,(78,by+5),badge,f,(255,255,255))
 fs=[fit(ln,IMPACT,170,958,6) for ln in lines];common=min(x.size for x in fs);f=font(IMPACT,common);step=round(common*0.96)
 for i,ln in enumerate(lines):text(canvas,mask,(57,ty+i*step),ln,f,(255,255,250) if i==0 else accent,6)
def copy_band(canvas,mask,k,ig):   # C: solid yellow band on top, black and red type
 badge,lines=COPY[k][:2];top=236 if ig else 52;sz=min(fit(l,IMPACT,160,940).size for l in lines);f=font(IMPACT,sz);step=round(sz*1.0)
 fb=fit(badge,ARIAL,40,890);bw=fb.getbbox(badge)[2];bh=62+16+2*step+36
 box(canvas,mask,(0,top,W,top+bh),(255,214,0));ImageDraw.Draw(canvas).rectangle((52,top+22,52+bw+46,top+84),fill=(12,12,12));text(canvas,mask,(75,top+26),badge,fb,(255,214,0))
 for i,ln in enumerate(lines):text(canvas,mask,(54,top+80+i*step-6),ln,f,(12,12,12) if i==0 else (200,30,30))
def copy_bottom(canvas,mask,k,ig):   # D: centred stack low in the frame, white then cyan, on a dark ramp
 badge,lines=COPY[k][:2];base=1556 if ig else 1680
 a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[4,7,12]
 for y in range(1000,H):a[y,:,3]=int(235*min(1,(y-1000)/330)**1.1)
 canvas.alpha_composite(Image.fromarray(a))
 sz=min(fit(l,IMPACT,176,980,6).size for l in lines);f=font(IMPACT,sz);step=round(sz*0.98);y2=base-step;y1=y2-step
 text(canvas,mask,(W//2,y1),lines[0],f,(255,255,250),6,anchor='ma');text(canvas,mask,(W//2,y2),lines[1],f,(40,220,255),6,anchor='ma')
 fb=fit(badge,ARIAL,38,800);bw=fb.getbbox(badge)[2];x0=(W-bw-52)//2;yb=y1-78
 ImageDraw.Draw(canvas).rounded_rectangle((x0,yb,x0+bw+52,yb+60),radius=30,fill=(255,255,250));text(canvas,mask,(x0+26,yb+9),badge,fb,(8,11,15))
def copy_middle(canvas,mask,k,ig):   # E: black band across the middle, red rules, line 1 white, line 2 red-on-white chip
 badge,lines=COPY[k][:2];y0,y1=812,1108
 box(canvas,mask,(0,y0,W,y1),(8,9,12));d=ImageDraw.Draw(canvas);d.rectangle((0,y0,W,y0+10),fill=(235,38,38));d.rectangle((0,y1-10,W,y1),fill=(235,38,38))
 f1=fit(lines[0],IMPACT,112,960);f2=fit(lines[1],IMPACT,130,930)
 text(canvas,mask,(W//2,y0+30),lines[0],f1,(255,255,250),anchor='ma')
 b=f2.getbbox(lines[1],anchor='ma');cy=y0+30+f1.size+8;pad=18
 d.rounded_rectangle((W//2+b[0]-pad-8,cy+b[1]-pad+6,W//2+b[2]+pad+8,cy+b[3]+pad-2),radius=10,fill=(255,255,250));text(canvas,mask,(W//2,cy),lines[1],f2,(215,28,28),anchor='ma')
def plate(k,which,gradient):
 p=R/'assets/gen'/f'{k}-{which}.png';im=ImageOps.fit(Image.open(p).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
 if (k,which)==('ds-24','d'):  # the back sat too low for the headline: shrink it, seat it at the top on black (its own background is black)
  sm=im.resize((round(W*0.74),round(H*0.74)),Image.Resampling.LANCZOS);im=Image.new('RGBA',(W,H),(3,3,5,255));im.paste(sm,((W-sm.width)//2,150))
 if gradient:
  a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[4,7,12]
  for y in range(H):a[y,:,3]=int(205*max(0,1-y/820)**0.85)
  im.alpha_composite(Image.fromarray(a))
 return im,p
def pool(k,ig):
 stem,(x0,x1,top,ymax)=POOL[k];p=PH/(stem+'_FINAL_PRIMARY.jpg');raw=Image.open(p).convert('RGB');sw,sh=raw.size
 py=738 if ig else 574;ph=H-py;asp=W/ph;bw=(x1-x0)*sw;limit=1640 if ig else 1800
 y=int(max(0,top*sh-0.03*sh));abs_b=(top+0.56*(ymax-top))*sh
 ch=int(max(0.52*sh,bw*1.06/asp,(abs_b-y)*ph/(limit-py)));cw=int(ch*asp)
 if cw>sw:cw=sw;ch=int(cw/asp)
 cx=int((x0+x1)/2*sw);x=max(0,min(cx-cw//2,sw-cw));y=min(y,sh-ch)
 pic=raw.crop((x,y,x+cw,y+ch)).resize((W,ph),Image.Resampling.LANCZOS);kk=ph/ch
 return pic,py,dict(source=str(p),source_sha256=sha(p),source_crop=[x,y,x+cw,y+ch],photo_top=py,source_head_y=round(top*sh),rendered_head_y=round(py+(top*sh-y)*kk,1))
def studio(im,k,ig):
 stem=STUDIO[k];p=CUT/(stem+'_CUTOUT.png');sub=Image.open(p).convert('RGBA');b=sub.getchannel('A').getbbox();sub=sub.crop(b)
 top=738 if ig else 574;kk=min(1000/sub.width,(1700-top)/(sub.height*0.62));sub=sub.resize((round(sub.width*kk),round(sub.height*kk)),Image.Resampling.LANCZOS)
 pad=22;bx=Image.new('RGBA',(sub.width+2*pad,sub.height+2*pad));bx.alpha_composite(sub,(pad,pad));alpha=bx.getchannel('A');x=(W-sub.width)//2-pad;y=top-pad
 sh=Image.new('RGBA',bx.size,(0,0,0));sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(15)).point(lambda q:int(q*0.35)));im.alpha_composite(sh,(x+8,y+12))
 line=Image.new('RGBA',bx.size,(255,255,250));line.putalpha(alpha.filter(ImageFilter.MaxFilter(17)));im.alpha_composite(line,(x,y));im.alpha_composite(bx,(x,y))
 return dict(source=str(p),source_sha256=sha(p),scale=round(kk,4),subject_top=top)
def build(keys):
 mp=R/'manifest.json';old=json.loads(mp.read_text())['outputs'] if mp.exists() else [];records=[r for r in old if r['short'] not in keys]
 for k in keys:
  for v in 'ABCDE':
   for platform in ['instagram','youtube']:
    ig=platform=='instagram';out=R/platform;out.mkdir(exist_ok=True);slug=f'{COPY[k][2]}_cover-{v}';p=out/(slug+'.png');tm=Image.new('L',(W,H))
    if v=='A':
     im=Image.new('RGBA',(W,H),(7,15,25));pic,py,info=pool(k,ig);im.paste(pic,(0,py));copy_house(im,tm,k,ig,'A')
    elif v=='B':
     im,gp=plate(k,'studio',True);info=studio(im,k,ig);info['plate']=str(gp);copy_house(im,tm,k,ig,'B')
    elif v=='C':
     im,gp=plate(k,'c',False);info=dict(plate=str(gp));copy_band(im,tm,k,ig)
    elif v=='D':
     im,gp=plate(k,'d',False);info=dict(plate=str(gp));copy_bottom(im,tm,k,ig)
    else:
     im,gp=plate(k,'e',False);info=dict(plate=str(gp));copy_middle(im,tm,k,ig)
    d=ImageDraw.Draw(im)
    if v in 'AB':d.rounded_rectangle((24,24,W-25,H-25),radius=22,outline=(255,255,250),width=4);d.line((45,1872,1035,1872),fill=ACC[v][0],width=6)
    im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
    ph=R/'phone'/platform;ph.mkdir(parents=True,exist_ok=True);Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(ph/(slug+'.jpg'),quality=95)
    records.append(dict(short=k,variant=v,platform=platform,path=str(p),sha256=sha(p),kind=KIND[v],copy={'badge':COPY[k][0],'headline':COPY[k][1]},**info))
 mp.write_text(json.dumps({'status':'awaiting Dan picks','outputs':records},indent=1)+'\n');print('built',len(records))
if __name__=='__main__':build(sys.argv[1:] or ORDER)
