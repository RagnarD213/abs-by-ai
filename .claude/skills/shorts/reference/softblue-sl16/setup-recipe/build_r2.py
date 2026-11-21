#!/usr/bin/env python3
"""SL-16 cover round 2 (Dan 2026-10-27). Reuses build.py layouts.
s1 F (yellow band) and G (Impact left, white frame): trash-can breakfast. s2 A2: picked A with the new title.
s3 A2: picked A, revised picture (offered drink turned down, water beside him). s4 new title, F yellow band (salad),
G centred top stack (simple plate vs clutter), H Impact left + frame (crumpled meal plan)."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build as B
from PIL import Image,ImageDraw
B.COPY['s2']=(['Why Carbs Destroy','Your Productivity'],'fasting-short2-why-carbs-destroy-your-productivity','Why Carbs Destroy Your Productivity')
B.COPY['s4']=(['Why You Need A Simple','Nutrition Plan'],'fasting-short4-why-you-need-a-simple-nutrition-plan','Why You Need A Simple Nutrition Plan')
B.BADGES['s4']='NUTRITION'
JOBS=[('s1','F','r2f','C'),('s1','G','r2g','A'),('s2','A2','a','C'),('s3','A2','r2a','C'),('s4','F','r2f','C'),('s4','G','r2g','Btop'),('s4','H','r2h','A')]
W,H=B.W,B.H;R=B.R
def make(k,v,src,lay,ig,tm):
 im,gp=B.plate(k,src)
 if lay=='C':
  bb=B.lay_C(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig);im,sh=B.drop_below(im,bb+50);pic=im.copy();B.lay_C(im,tm,k,ig)
 elif lay=='Btop':
  B.ramp(im,0,700,190);bb=B.lay_Btop(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig);im,sh=B.drop_below(im,bb+50);pic=im.copy();B.lay_Btop(im,tm,k,ig)
 else:
  B.ramp(im,0,900,200);bb=B.lay_A(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig);im,sh=B.drop_below(im,bb+50);pic=im.copy();B.lay_A(im,tm,k,ig)
  ImageDraw.Draw(im).rounded_rectangle((24,24,W-25,H-25),radius=22,outline=B.WHITE,width=4)
 return im,pic,dict(plate=str(gp),picture_shift=sh,has_person=True,layout=lay)
recs=[]
for k,v,src,lay in JOBS:
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';out=R/platform;slug=f'{B.COPY[k][1]}_cover-{v}';p=out/(slug+'.png');tm=Image.new('L',(W,H))
  im,pic,info=make(k,v,src,lay,ig,tm);im.convert('RGB').save(p)
  if not ig:im.convert('RGB').save(p.with_suffix('.jpg'),quality=92)
  tm.save(p.with_name(p.stem+'.text-mask.png'));pic.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
  recs.append(dict(short=k,variant=v,platform=platform,path=str(p),sha256=B.sha(p),kind='round 2',copy={'badge':B.BADGES[k],'headline':B.COPY[k][0]},**info))
(R/'manifest-r2.json').write_text(json.dumps({'status':'awaiting Dan approval of round 2','outputs':recs},indent=1)+'\n');print('built',len(recs))
