#!/usr/bin/env python3
"""SL-17 Short 3 ("Every Man Should Train A Martial Art") cover round 2 (2026-10-23). Dan turned down A-E: "Show me three new
designs with a real photo of me with a black belt." Three real photos from his Photos library (black-belt promotion
2024-12-14 with his instructor, and 2024-12-21 in his gi with the black belt), never redrawn; type set in code:
  F yellow band on top, DIN Condensed black and red, the promotion photo with his instructor full width below
  G his real seated cutout with a white outline on the Codex dojo scene (s3-studio), centred Futura, line 2 on a yellow marker
  H over-the-shoulder photo in a top panel, solid black type panel below with a red rule, Impact white with the second line red
Adds F, G, H for s3 to manifest.json beside A-E (kept for the record)."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw,ImageFilter,ImageOps
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build import (W,H,R,COPY,BADGES,WHITE,INK,RED,YEL,IMPACT,ARIAL,font,fit,common,text,box,ramp,plate,lay_B,lay_C,
                   person_mask,sha)
K='s3';SRC=R/'sources/blackbelt'
PHOTO={'F':SRC/'promotion-with-instructor_2024-12-14.jpg','G':SRC/'seated-mat_2024-12-21.jpg','H':SRC/'over-shoulder_2024-12-21.jpg'}
KIND={'F':'Real black-belt photo (promotion day, with his instructor)','G':'Real black-belt photo cut out on an AI dojo scene',
      'H':'Real black-belt photo, photo panel over a type panel'}
def blur_bg(im):
 bg=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(40)).convert('RGBA')
 bg.alpha_composite(Image.new('RGBA',(W,H),(6,9,14,190)));return bg
def build_F(ig):
 raw=Image.open(PHOTO['F']).convert('RGB');canvas=blur_bg(raw);tm=Image.new('L',(W,H))
 bb=lay_C(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),K,ig)
 m,_=person_mask(raw);top=np.where(m.any(axis=1))[0].min()            # hair top of the taller person, source rows
 k=W/raw.width;pic=raw.resize((W,round(raw.height*k)),Image.Resampling.LANCZOS)
 y0=bb+40-round(top*k)                                                   # hair sits 40 px under the band
 canvas.alpha_composite(pic.convert('RGBA'),(0,y0));pic_only=canvas.copy();lay_C(canvas,tm,K,ig)
 return canvas,tm,pic_only,dict(source_crop='full width',paste_y=y0,source_hair_top=int(top))
def build_G(ig):
 canvas,gp=plate(K,'studio');ramp(canvas,0,900,215);tm=Image.new('L',(W,H))
 bottom=lay_B(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),K,ig)
 raw=Image.open(PHOTO['G']).convert('RGB');m,_=person_mask(raw)
 a=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
 sub=raw.convert('RGBA');sub.putalpha(a);sub=sub.crop(a.getbbox())
 top=bottom+44;lim=(1700 if ig else 1890)-top;kk=min(1000/sub.width,lim/sub.height)
 sub=sub.resize((round(sub.width*kk),round(sub.height*kk)),Image.Resampling.LANCZOS)
 pad=22;bx=Image.new('RGBA',(sub.width+2*pad,sub.height+2*pad));bx.alpha_composite(sub,(pad,pad));al=bx.getchannel('A')
 x=(W-sub.width)//2-pad;y=top-pad
 sh=Image.new('RGBA',bx.size,(0,0,0));sh.putalpha(al.filter(ImageFilter.GaussianBlur(15)).point(lambda q:int(q*0.4)));canvas.alpha_composite(sh,(x+8,y+12))
 line=Image.new('RGBA',bx.size,WHITE);line.putalpha(al.filter(ImageFilter.MaxFilter(17)));canvas.alpha_composite(line,(x,y));canvas.alpha_composite(bx,(x,y))
 pic_only=canvas.copy();lay_B(canvas,tm,K,ig)
 return canvas,tm,pic_only,dict(plate=str(gp),scale=round(kk,4),subject_top=top)
def build_H(ig):
 raw=Image.open(PHOTO['H']).convert('RGB');tm=Image.new('L',(W,H));canvas=Image.new('RGBA',(W,H),(8,9,12,255))
 p0,p1=(150,1110) if ig else (0,1190)                                   # photo panel rows
 m,faces=person_mask(raw);ys=np.where(m.any(axis=1))[0];top=ys.min()
 ph=p1-p0;cw=round(raw.width*0.80);ch=round(cw*ph/W);fx=(faces[0][0]+faces[0][2])//2 if faces else raw.width//2
 x=max(0,min(fx-cw//2,raw.width-cw));y=max(0,top-round(0.05*ch))
 pic=raw.crop((x,y,x+cw,y+ch)).resize((W,ph),Image.Resampling.LANCZOS);canvas.alpha_composite(pic.convert('RGBA'),(0,p0))
 d=ImageDraw.Draw(canvas);d.rectangle((0,p1,W,p1+12),fill=RED)
 pic_only=canvas.copy();lines=COPY[K][0]
 fb=font(ARIAL,40);y=p1+52;text(canvas,tm,(W//2,y),BADGES[K],fb,(235,60,60),anchor='ma');y+=74
 f=common(lines,IMPACT,170,980);step=round(f.size*1.04)
 text(canvas,tm,(W//2,y),lines[0],f,WHITE,anchor='ma');text(canvas,tm,(W//2,y+step),lines[1],f,(235,40,40),anchor='ma')
 return canvas,tm,pic_only,dict(source_crop=[x,y,x+cw,y+ch],photo_panel=[p0,p1])
def main():
 mp=R/'manifest.json';man=json.loads(mp.read_text());recs=[r for r in man['outputs'] if not (r['short']==K and r['variant'] in 'FGH')]
 for v,fn in [('F',build_F),('G',build_G),('H',build_H)]:
  for platform in ['instagram','youtube']:
   ig=platform=='instagram';canvas,tm,pic,info=fn(ig);slug=f'{COPY[K][1]}_cover-{v}';p=R/platform/(slug+'.png')
   canvas.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'));pic.convert('RGB').save(p.with_name(p.stem+'.picture.png'))
   ph=R/'phone'/platform;ph.mkdir(parents=True,exist_ok=True);Image.open(p).resize((270,480),Image.Resampling.LANCZOS).save(ph/(slug+'.jpg'),quality=95)
   recs.append(dict(short=K,variant=v,platform=platform,path=str(p),sha256=sha(p),kind=KIND[v],has_person=True,round=2,
     source=str(PHOTO[v]),source_sha256=sha(PHOTO[v]),copy={'badge':BADGES[K],'headline':COPY[K][0]},**info))
 man['outputs']=recs;mp.write_text(json.dumps(man,indent=1)+'\n');print('built s3 F G H')
if __name__=='__main__':main()
