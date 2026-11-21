#!/usr/bin/env python3
"""SL-16 Intermittent Fasting Shorts (2026-10-27, from SL-08 builder); mix of 2026-10-25: A/B AI Dan, C real studio, D split, E AI Dan. Old notes follow. SL-08 Calories Not Losing Weight Shorts: five cover choices per short (2026-10-23; builder copied from SL-18), two layouts each (Instagram
grid, YouTube). Layout family copied from SL-09 / SL-07, where Dan picked C most often; new copy, photos and Codex pictures.
Mix per VIDEO-RULES (2026-10-13): A real pool photo, B real studio cutout on a Codex scene, C AI image of Dan acting the
title out, D and E Codex's own designs. Five unique designs, all in title case:
  A pool photo full bleed, Impact left stack (white, cyan line 2), cyan eyebrow rule, white frame
  B studio cutout with white keyline on a Codex scene, Futura centred, line 2 black on a yellow marker box
  C yellow band on top, DIN Condensed, black and red
  D headline stacked at the bottom, Avenir Next Condensed Heavy, white and cyan, white pill badge
  E two panels, black band across the middle with red rules, Arial Black, line 2 red on a white chip
Real photos are never redrawn: Codex makes plates only; cutouts, photos and all type are layered in code."""
from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent));from root import P,R,PH,CUT
W,H=1080,1920
SUP='/System/Library/Fonts/Supplemental/'
IMPACT=(SUP+'Impact.ttf',0);ARIAL=(SUP+'Arial Bold.ttf',0);ABLACK=(SUP+'Arial Black.ttf',0);DIN=(SUP+'DIN Condensed Bold.ttf',0)
FUTURA=(SUP+'Futura.ttc',4);AVENIR=('/System/Library/Fonts/Avenir Next Condensed.ttc',8)
# The eyebrow is each short's own on-screen eyebrow, in capitals (VIDEO-RULES 2026-10-20: eyebrows stay in CAPITALS).
BADGES={'s1': 'INTERMITTENT FASTING', 's2': 'AFTERNOON CRASH', 's3': 'ALCOHOL', 's4': 'STICK TO THE PLAN'}
COPY={'s1': (['How To Start Fasting:', 'Just Skip Breakfast'], 'fasting-short1-how-to-start-fasting-just-skip-breakfast', 'How To Start Fasting: Just Skip Breakfast'), 's2': (['Carbs Are Killing', 'Your Workday'], 'fasting-short2-carbs-are-killing-your-workday', 'Carbs Are Killing Your Workday'), 's3': (['Never Break Your Fast', 'With Alcohol'], 'fasting-short3-never-break-your-fast-with-alcohol', 'Never Break Your Fast With Alcohol'), 's4': (['Life Will Punch You', 'In The Face'], 'fasting-short4-life-will-punch-you-in-the-face', 'Life Will Punch You In The Face')}
ORDER=list(COPY)
DCOPY={}
XOUT=set()
POOL={}
TIGHT={}
SPEEDO={}
STUDIO={'s1': 'studio-white-23', 's2': 'studio-gray-79', 's3': 'studio-blue-213', 's4': 'studio-blue-74'}
KIND={'A':'AI image of Dan 1','B':'AI image of Dan 2','C':'Real studio photo on an AI scene','D':'Codex choice: wrong vs right split','E':'Codex choice: AI image of Dan 3'}
CYAN=(40,220,255);YEL=(255,214,0);RED=(225,32,32);INK=(10,11,14);WHITE=(255,255,250)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(spec,size):return ImageFont.truetype(spec[0],size,index=spec[1])
def fit(txt,spec,start,maxw,stroke=0):
 for size in range(start,23,-2):
  f=font(spec,size);b=f.getbbox(txt,stroke_width=stroke)
  if b[2]-b[0]<=maxw:return f
 raise ValueError(txt)
def common(lines,spec,start,maxw,stroke=0):return font(spec,min(fit(l,spec,start,maxw,stroke).size for l in lines))
def text(canvas,mask,xy,txt,f,fill,stroke=0,sf=(8,11,15),anchor='la'):
 ImageDraw.Draw(canvas).text(xy,txt,font=f,fill=fill,stroke_width=stroke,stroke_fill=sf,anchor=anchor);ImageDraw.Draw(mask).text(xy,txt,font=f,fill=255,stroke_width=stroke,stroke_fill=255,anchor=anchor)
def box(canvas,mask,xyxy,fill,radius=0):
 ImageDraw.Draw(canvas).rounded_rectangle(xyxy,radius=radius,fill=fill);ImageDraw.Draw(mask).rounded_rectangle(xyxy,radius=radius,fill=255)
def ramp(canvas,y0,y1,alpha,top_dark=True,col=(4,7,12)):
 a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=col
 for y in range(H):
  t=(y1-y)/(y1-y0) if top_dark else (y-y0)/(y1-y0)
  a[y,:,3]=int(alpha*min(1,max(0,t))**0.9)
 canvas.alpha_composite(Image.fromarray(a))
def plate(k,which):
 p=R/'assets/gen'/f'{k}-{which}.png';return ImageOps.fit(Image.open(p).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA'),p
import subprocess,tempfile,os
PM=os.path.expanduser('~/.cache/absbyai/personmask/personmask')
def person_mask(im):
 with tempfile.TemporaryDirectory() as t:
  a,b=os.path.join(t,'i.png'),os.path.join(t,'m.png');im.convert('RGB').save(a)
  faces=json.loads(subprocess.run([PM,a,b],capture_output=True,text=True,check=True).stdout)['faces']
  return np.array(Image.open(b).convert('L'))>127,faces
def drop_below(im,top_needed):
 """C: slide the AI picture down until the man's hair clears the band by top_needed (fill above with the plate's own plain top colour)."""
 m,_=person_mask(im);ys=np.where(m.any(axis=1))[0]
 if not len(ys) or ys.min()>=top_needed:return im,0
 sh=int(top_needed-ys.min());col=tuple(int(v) for v in np.asarray(im.convert('RGB'))[:60].reshape(-1,3).mean(axis=0))
 out=Image.new('RGBA',(W,H),col+(255,));out.alpha_composite(im.crop((0,0,W,H-sh)),(0,sh));return out,sh
def open_strip(im,s0,s1,b0,b1,gap=34):
 """E: move each Codex panel away from the type band so nothing in a panel sits under it."""
 out=Image.new('RGBA',(W,H),(0,0,0,255));top=im.crop((0,0,W,s0));bot=im.crop((0,s1,W,H))
 out.alpha_composite(top,(0,b0-gap-s0));out.alpha_composite(bot,(0,b1+gap));return out
# ---- type layouts -------------------------------------------------------------------------------------------------
def lay_A(canvas,mask,k,ig):   # left stack: cyan rule + eyebrow, Impact white / cyan
 lines=COPY[k][0];by=250 if ig else 64;ty=by+70
 fb=font(ARIAL,40);ImageDraw.Draw(canvas).rectangle((58,by+6,68,by+50),fill=CYAN);text(canvas,mask,(86,by+4),BADGES[k],fb,CYAN,3)
 f=common(lines,IMPACT,150,950,6);step=round(f.size*1.0)
 for i,ln in enumerate(lines):text(canvas,mask,(58,ty+i*step),ln,f,WHITE if i==0 else CYAN,6)
 return ty+2*step
def lay_B(canvas,mask,k,ig):   # centred: yellow eyebrow, white Futura line 1 with black outline, line 2 black on a yellow box
 lines=COPY[k][0];by=252 if ig else 64
 fb=font(ARIAL,38);text(canvas,mask,(W//2,by),BADGES[k],fb,YEL,3,anchor='ma')
 f1=fit(lines[0],FUTURA,128,960,5);f2=fit(lines[1],FUTURA,128,900)
 y1=by+60;text(canvas,mask,(W//2,y1),lines[0],f1,WHITE,5,anchor='ma')
 y2=y1+f1.size+26;b=f2.getbbox(lines[1],anchor='ma');pad=20
 box(canvas,mask,(W//2+b[0]-pad,y2+b[1]-14,W//2+b[2]+pad,y2+b[3]+14),YEL,8);text(canvas,mask,(W//2,y2),lines[1],f2,INK,anchor='ma')
 return y2+b[3]+14
def lay_C(canvas,mask,k,ig):   # solid yellow band on top, DIN black and red
 lines=COPY[k][0];top=236 if ig else 48;f=common(lines,DIN,190,960);step=round(f.size*0.92)
 fb=font(ARIAL,36);bw=fb.getbbox(BADGES[k])[2];bh=24+60+12+2*step+18
 box(canvas,mask,(0,top,W,top+bh),YEL);ImageDraw.Draw(canvas).rectangle((54,top+24,54+bw+40,top+82),fill=INK);text(canvas,mask,(74,top+33),BADGES[k],fb,YEL)
 for i,ln in enumerate(lines):text(canvas,mask,(54,top+100+i*step),ln,f,INK if i==0 else (196,24,24))
 return top+bh
def lay_D_r2(canvas,mask,k,ig):   # Dan R2: no eyebrow; STOP DATING in huge red Impact caps across the full width; the rest white title case below
 lines=DCOPY[k];limit=1608 if ig else 1728;ramp(canvas,980,1300,245,top_dark=False)
 f1=fit(lines[0],IMPACT,400,1040,8);f2=common(lines[1:],AVENIR,240,1000,5);step=round(f2.size*0.98)
 b1=f1.getbbox(lines[0],stroke_width=8,anchor='ma')
 y3=limit-f2.getbbox(lines[2],stroke_width=5,anchor='ma')[3];y2=y3-step;y1=y2-18-(b1[3])
 text(canvas,mask,(W//2,y1),lines[0],f1,RED,8,sf=(8,8,10),anchor='ma')
 for ln,y in zip(lines[1:],(y2,y3)):text(canvas,mask,(W//2,y),ln,f2,WHITE,5,anchor='ma')
 return y1+b1[1]
def lay_D(canvas,mask,k,ig):
 if k in DCOPY:return lay_D_r2(canvas,mask,k,ig)
 return lay_D_r1(canvas,mask,k,ig)
def lay_D_r1(canvas,mask,k,ig):   # centred stack low in the frame on a dark ramp, Avenir Heavy white / cyan, white pill badge
 lines=DCOPY.get(k,COPY[k][0]);limit=1608 if ig else 1728;big=k in DCOPY;ramp(canvas,1000 if big else 1020,1340 if big else 1380,240,top_dark=False)
 f=common(lines,AVENIR,200 if big else 160,1000 if big else 990,5);step=round(f.size*(0.98 if big else 1.0))
 yl=limit-f.getbbox(lines[-1],stroke_width=5,anchor='ma')[3];ys=[yl-(len(lines)-1-i)*step for i in range(len(lines))]
 for i,(ln,y) in enumerate(zip(lines,ys)):text(canvas,mask,(W//2,y),ln,f,WHITE if i<len(lines)-1 or len(lines)==2 and i==0 else CYAN,5,anchor='ma')
 if len(lines)==2:text(canvas,mask,(W//2,ys[1]),lines[1],f,CYAN,5,anchor='ma')
 fb=font(ARIAL,44 if big else 36);bw=fb.getbbox(BADGES[k])[2];x0=(W-bw-56)//2;yb=ys[0]-(96 if big else 80);bh=72 if big else 60
 box(canvas,mask,(x0,yb,x0+bw+56,yb+bh),WHITE,bh//2);text(canvas,mask,(x0+28,yb+(12 if big else 10)),BADGES[k],fb,INK)
 return yb
def lay_Btop(canvas,mask,k,ig):   # centred stack at the top, white pill badge, Avenir Heavy white / cyan
 lines=COPY[k][0];top=240 if ig else 56;fb=font(ARIAL,36);bw=fb.getbbox(BADGES[k])[2];x0=(W-bw-56)//2
 box(canvas,mask,(x0,top,x0+bw+56,top+60),WHITE,30);text(canvas,mask,(x0+28,top+10),BADGES[k],fb,INK)
 f=common(lines,AVENIR,170,990,5);step=round(f.size*1.0);y=top+84
 for i,ln in enumerate(lines):text(canvas,mask,(W//2,y+i*step),ln,f,WHITE if i==0 else CYAN,5,anchor='ma')
 return y+len(lines)*step+10
def red_x(im):
 """Draw a red X over the right-hand person (the woman) on a two-person plate, found with the person mask (not text)."""
 from scipy.ndimage import label
 m,faces=person_mask(im);faces=sorted(faces,key=lambda f:f[0]);f=faces[-1]
 lab,n=label(m);cx,cy=(f[0]+f[2])//2,(f[1]+f[3])//2;comp=lab==lab[cy,cx] if lab[cy,cx] else m
 cols=np.where(comp.any(axis=0))[0];x0=max(int(cols.min()),(faces[0][2]+f[0])//2 if len(faces)>1 else 0);x1=int(cols.max())
 y0=int(f[1]-0.25*(f[3]-f[1]));y1=min(int(np.where(comp.any(axis=1))[0].max()),1040)
 pad=20;x0,x1,y0,y1=x0-pad,min(W-30,x1+pad),y0-pad,y1+pad
 ov=Image.new('RGBA',(W,H));d=ImageDraw.Draw(ov)
 for w,c in [(64,(10,10,12,200)),(44,RED+(255,))]:
  d.line((x0,y0,x1,y1),fill=c,width=w);d.line((x1,y0,x0,y1),fill=c,width=w)
 im.alpha_composite(ov);return [x0,y0,x1,y1]
def strip(im):
 """Find Codex's black middle strip (rows that are near black edge to edge) in the fitted plate; returns (y0, y1)."""
 a=np.asarray(im.convert('L'),dtype=np.float32);dark=(a<28).mean(axis=1)>0.97;ys=[y for y in range(500,1400) if dark[y]]
 if not ys:return 840,1080
 runs=[];s=ys[0];prev=ys[0]
 for y in ys[1:]:
  if y!=prev+1:runs.append((s,prev));s=y
  prev=y
 runs.append((s,prev));return max(runs,key=lambda r:r[1]-r[0])
def lay_E(canvas,mask,k,ig,band):   # black band across the middle with red rules, Arial Black white / red on a white chip
 lines=COPY[k][0];y0,y1=band;d=ImageDraw.Draw(canvas)
 box(canvas,mask,(0,y0,W,y1),(8,9,12));d.rectangle((0,y0,W,y0+10),fill=RED);d.rectangle((0,y1-10,W,y1),fill=RED)
 fb=font(ARIAL,32);f1=fit(lines[0],ABLACK,92,980);f2=fit(lines[1],ABLACK,96,900)
 inner=50+f1.size+22+f2.size+24;y=y0+10+max(14,((y1-y0-20)-inner)//2)
 text(canvas,mask,(W//2,y),BADGES[k],fb,(255,120,120),anchor='ma');y+=50
 text(canvas,mask,(W//2,y),lines[0],f1,WHITE,anchor='ma');y+=f1.size+22
 b=f2.getbbox(lines[1],anchor='ma');pad=18
 d.rounded_rectangle((W//2+b[0]-pad,y+b[1]-12,W//2+b[2]+pad,y+b[3]+12),radius=10,fill=WHITE);text(canvas,mask,(W//2,y),lines[1],f2,(205,24,24),anchor='ma')
 return y+b[3]+12
# ---- pictures -----------------------------------------------------------------------------------------------------
BOX=json.loads((R/'sources/pool_boxes.json').read_text())
def pool(k,ig,photo_top):
 """Real pool pixels, local Vision alpha, on the subscription-generated background."""
 stem=POOL[k];src=PH/(stem+'_FINAL_PRIMARY.jpg');p=R/'sources/cutouts'/(stem+'_CUTOUT.png');raw=Image.open(p).convert('RGBA')
 b=raw.getchannel('A').getbbox();source_head_y=b[1]
 # Preserve all available source hair. Standing photos in real swim shorts need no brief crop;
 # photo-122 already ends at lower abs in its camera framing. Seated photo-241 stays uncropped.
 if stem in ['photo-273','photo-244','photo-247']: b=(b[0],b[1],b[2],min(b[3],round(raw.height*0.82)))
 if stem=='photo-223': b=(b[0],b[1],b[2],round(raw.height*0.696)) # native y2850: lower waistband seam, before leg openings
 sub=raw.crop(b);limit=1630 if ig else 1850
 scale=(H-photo_top)/sub.height;sub=sub.resize((round(sub.width*scale),round(sub.height*scale)),Image.Resampling.LANCZOS)
 canvas,_=plate(k,'pool');ramp(canvas,0,950,225)
 x=(W-sub.width)//2;y=photo_top
 # A soft bottom fade avoids an artificial straight edge when a waist-cropped portrait ends.
 # Body extends naturally past the bottom canvas edge; no fading of the physique.
 shadow=Image.new('RGBA',sub.size,(0,0,0));shadow.putalpha(sub.getchannel('A').filter(ImageFilter.GaussianBlur(14)).point(lambda q:int(q*.38)));canvas.alpha_composite(shadow,(x+10,y+12));canvas.alpha_composite(sub,(x,y))
 info=dict(source=str(src),source_sha256=sha(src),cutout=str(p),cutout_sha256=sha(p),plate=str(R/'assets/gen'/f'{k}-pool.png'),source_crop=list(b),source_head_y=source_head_y,rendered_head_y=y,photo_top=photo_top,photo_bottom=y+sub.height,source_pixels_preserved=True)
 return canvas,info
def studio(im,k,top):
 stem=STUDIO[k];p=CUT/(stem+'_CUTOUT.png');sub=Image.open(p).convert('RGBA');b=sub.getchannel('A').getbbox();sub=sub.crop(b)
 kk=min(980/sub.width,(1720-top)/(sub.height*0.66));sub=sub.resize((round(sub.width*kk),round(sub.height*kk)),Image.Resampling.LANCZOS)
 pad=22;bx=Image.new('RGBA',(sub.width+2*pad,sub.height+2*pad));bx.alpha_composite(sub,(pad,pad));alpha=bx.getchannel('A');x=(W-sub.width)//2-pad;y=top-pad
 sh=Image.new('RGBA',bx.size,(0,0,0));sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(15)).point(lambda q:int(q*0.4)));im.alpha_composite(sh,(x+8,y+12))
 line=Image.new('RGBA',bx.size,WHITE);line.putalpha(alpha.filter(ImageFilter.MaxFilter(17)));im.alpha_composite(line,(x,y));im.alpha_composite(bx,(x,y))
 return dict(source=str(p),source_sha256=sha(p),scale=round(kk,4),subject_top=top)
def build(keys):
 mp=R/'manifest.json';old=json.loads(mp.read_text())['outputs'] if mp.exists() else [];records=[r for r in old if r['short'] not in keys]
 for k in keys:
  for v in 'ABCDE':
   for platform in ['instagram','youtube']:
    ig=platform=='instagram';out=R/platform;out.mkdir(exist_ok=True);slug=f'{COPY[k][1]}_cover-{v}';p=out/(slug+'.png');tm=Image.new('L',(W,H))
    if v=='A':   # AI Dan 1 under the yellow band
     im,gp=plate(k,'a');bb=lay_C(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig);im,shift=drop_below(im,bb+50)
     info=dict(plate=str(gp),picture_shift=shift,has_person=True);pic=im.copy();lay_C(im,tm,k,ig)
    elif v=='B':   # AI Dan 2, headline at the bottom
     im,gp=plate(k,'b');ramp(im,0,700,190);bb=lay_Btop(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig);im,shift=drop_below(im,bb+50)
     info=dict(plate=str(gp),picture_shift=shift,has_person=True);pic=im.copy();lay_Btop(im,tm,k,ig)
    elif v=='C':   # real studio cutout on a Codex scene
     im,gp=plate(k,'c');ramp(im,0,900,215);bottom=lay_B(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig)
     info=studio(im,k,bottom+40);info['plate']=str(gp);info['has_person']=True;pic=im.copy();lay_B(im,tm,k,ig)
    elif v=='D':   # wrong vs right split, title in the black band
     im,gp=plate(k,'d');s0,s1=strip(im);c=(s0+s1)//2;half=max(185,(s1-s0)//2+24);info=dict(plate=str(gp),codex_strip=[int(s0),int(s1)])
     im=open_strip(im,s0,s1,c-half,c+half);pic=im.copy();lay_E(im,tm,k,ig,(c-half,c+half))
    else:   # AI Dan 3, Impact left stack, white frame
     im,gp=plate(k,'e');ramp(im,0,900,200);bb=lay_A(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig);im,shift=drop_below(im,bb+50)
     info=dict(plate=str(gp),picture_shift=shift,has_person=True);pic=im.copy();lay_A(im,tm,k,ig)
     ImageDraw.Draw(im).rounded_rectangle((24,24,W-25,H-25),radius=22,outline=WHITE,width=4)
    im.convert('RGB').save(p);
    if platform=='youtube':im.convert('RGB').save(p.with_suffix('.jpg'),quality=92);
    tm.save(p.with_name(p.stem+'.text-mask.png'));pic.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
    ph=R/'phone'/platform;ph.mkdir(parents=True,exist_ok=True);Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(ph/(slug+'.jpg'),quality=95)
    records.append(dict(short=k,variant=v,platform=platform,path=str(p),sha256=sha(p),kind=KIND[v],copy={'badge':BADGES[k],'headline':DCOPY.get(k,COPY[k][0]) if v=='D' else COPY[k][0]},**info))
 mp.write_text(json.dumps({'status':'awaiting Dan picks','outputs':records},indent=1)+'\n');print('built',len(records))
if __name__=='__main__':build(sys.argv[1:] or ORDER)
