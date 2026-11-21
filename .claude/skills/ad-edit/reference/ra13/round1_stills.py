import os,sys,json,importlib.util,shutil
from pathlib import Path
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image,ImageDraw,ImageFilter
W=Path(__file__).resolve().parents[1];os.chdir(W)
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');SH=R/'.claude/skills/_shared'
sys.path[:0]=[str(SH),str(SH/'hyperframes')]
import softblue as B,vertical as VT
O=W/'round1/stills';O.mkdir(exist_ok=True,parents=True)
# Full-frame still conversion, crop audition only. Motion uses the exact ffmpeg look.
lines=Path('/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube').read_text().splitlines();n=int(next(s.split()[1] for s in lines if s.startswith('LUT_3D_SIZE')));rows=[list(map(float,s.split())) for s in lines if s and (s[0].isdigit() or s[0]=='-')];lut=np.asarray(rows).reshape(n,n,n,3)
def grade(im):
 a=np.asarray(im,float)/255;c=np.stack([a[:,:,2],a[:,:,1],a[:,:,0]])*(n-1);v=np.stack([map_coordinates(lut[:,:,:,k],c,order=1,mode='nearest') for k in range(3)],-1);l=v@np.array([.2126,.7152,.0722]);v=l[:,:,None]+(v-l[:,:,None])*1.12;v=np.clip(v,0,1)**(1/1.03);return Image.fromarray(np.uint8(v*255))
raw=Image.open(W/'source/raw-269.png').convert('RGB');full=grade(raw)
for name,cw,ch in [('wide',738,1312),('close',630,1120),('horizontal-wide',2144,1206),('horizontal-close',1728,972)]:
 cx=1110 if 'horizontal' not in name else 1080;x=int(cx-cw/2);y=1240
 full.crop((x,y,x+cw,y+ch)).resize((960,540) if 'horizontal' in name else (540,960),Image.LANCZOS).save(O/f'crop-{name}.jpg',quality=95)
# Use the maintained reference's unchanged phone shell/layout helper, never copy its template.
spec=importlib.util.spec_from_file_location('ra14_phone_helpers',R/'.claude/skills/ad-edit/reference/ra14/s63_stills.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
# Existing approved demo still content, without the previous video's caption.
for old,new in [('P1a','P1-options'),('P1b','P1-result'),('T1a','P2-meal'),('T1b','P2-workout')]:
 src=Image.open('/Volumes/Extreme/_edit_work/ra14/round1/stills/'+old+'.jpg').convert('RGB');im=B.field(0,1080,1920).convert('RGB');im.paste(src.crop((0,0,1080,1388)),(0,0));im.save(O/(new+'.jpg'),quality=94)
# Same-identity evidence for the before/goal pair.
for p,name,label in [(Path('/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets/dan_before_200lb.jpg'),'before','Real picture of me. Not AI-generated'),(R/'Media/example pictures/dan by pool.png','goal','AI-GENERATED')]:
 im=Image.open(p).convert('RGB');im.thumbnail((760,1260),Image.LANCZOS);f=B.field(0,1080,1920).convert('RGBA');f.paste(im,((1080-im.width)//2,180));B.disclosure(f,label,xy=(540,1500),anchor='mt');f.convert('RGB').save(O/(name+'.jpg'),quality=94)
shutil.copyfile(O/'goal.jpg',O/'P1-result.jpg')
# Existing shared CTA, exact requested words.
sc,meta=VT.cta_scenes('CTA',2.725,'Tap The Button Below','Get Started',hold_out=True)
VT.build(sc,W/'round1/hf',render=False,snap=1.2)
ov=Image.open(W/'round1/hf/stills/CTA.png').convert('RGBA');base=grade(Image.open(W/'source/raw-324.png').convert('RGB')).crop((741,1240,1479,2552)).resize((1080,1920),Image.LANCZOS).convert('RGBA')
x0,y0,x1,y1=meta['box'];mask=Image.new('L',base.size);ImageDraw.Draw(mask).rounded_rectangle((x0,y0,x1,y1),36,fill=235);base.paste(base.filter(ImageFilter.GaussianBlur(14)),(0,0),mask);Image.alpha_composite(base,ov).convert('RGB').save(O/'CTA.jpg',quality=94)
# Reference evidence copied only for comparison, not reused in the edit.
shutil.copyfile('/Volumes/Extreme/_edit_work/ra01/review-r3/sheets/cuts9_1.jpg',O/'reference-ra01-sheet.jpg')
shutil.copyfile('/Volumes/Extreme/_edit_work/wv01-edit/round10/sample/DRAFT - WV-01 round 10 - opening.mp4.framing_proof.jpg',O/'reference-wv01-sheet.jpg')
print('ROUND ONE STILLS READY',flush=True)
