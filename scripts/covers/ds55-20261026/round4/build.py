#!/usr/bin/env python3
"""Two native top-header designs over the selected unchanged screenshot.
A uses the actual shared Soft Blue Light glass renderer and its native Poppins font.
B fills the entire headroom with a custom cream/orange type composition.
These are cover stills; no movie graphic or approved film is modified.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'Short-form video content/covers/review/ds55-five-minute-exercises-20261026/round4'
sys.path.insert(0,str(ROOT/'.claude/skills/_shared'));import softblue as SB
SB.FONTS=str(ROOT/'Media/codex-video-trial/assets/fonts')
W,H=1080,1920
DIN=Path('/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf')
POPPINS=ROOT/'Media/codex-video-trial/assets/fonts/Poppins-Bold.ttf'
SOURCE=OUT/'sources/selected-picture.png'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(path,size):return ImageFont.truetype(str(path),size)
def fit(path,s,size,width):
 for n in range(size,25,-1):
  f=font(path,n)
  if f.getlength(s)<=width:return f
 raise ValueError(s)
def drawtext(im,mask,xy,s,f,col):
 d=ImageDraw.Draw(im);md=ImageDraw.Draw(mask);box=d.textbbox(xy,s,font=f,anchor='lt');d.text(xy,s,font=f,fill=col,anchor='lt');md.text(xy,s,font=f,fill=255,anchor='lt');return list(box)
def build():
 src=Image.open(SOURCE).convert('RGB');rows=[]
 for k in ['A','B']:
  for platform in ['instagram','youtube']:
   ig=platform=='instagram';im=src.copy();tm=Image.new('L',(W,H));bounds=[]
   if k=='A':
    # Exact shared 54% blue glass mix, background blur, rounded hairline and pale specular line.
    SB.glass(im,(36,30,1044,605),1.0,u=2,radius=18)
    d=ImageDraw.Draw(im)
    y1,y2=(250,435) if ig else (124,344)
    d.rounded_rectangle((66,y1,76,y2+120),radius=5,fill=SB.CYAN)
    bounds.append(drawtext(im,tm,(108,y1),'5 Minute',fit(POPPINS,'5 Minute',170 if ig else 185,880),SB.CYAN))
    bounds.append(drawtext(im,tm,(108,y2),'Home Workout',fit(POPPINS,'Home Workout',139,885),SB.WHITE))
    info={'shared_component':'softblue.glass','glass_blue_mix':.54,'glass_mask_alpha':235,'glass_colour':list(SB.GLASS_TINT),'font':'Poppins Bold','card_bounds':[36,30,1044,605]}
   else:
    d=ImageDraw.Draw(im);cream='#FFF0D3';orange='#EE713D';ink='#14242A'
    d.rectangle((0,0,W,610),fill=cream)
    bar=192 if ig else 72
    d.polygon([(0,0),(W,0),(W,bar-45),(0,bar+34)],fill=orange)
    d.line((38,590,1042,590),fill=ink,width=5)
    if ig:
     bounds.append(drawtext(im,tm,(54,247),'5',font(DIN,420),ink))
     bounds.append(drawtext(im,tm,(320,262),'Minute',font(DIN,155),ink))
     bounds.append(drawtext(im,tm,(320,442),'Home Workout',fit(DIN,'Home Workout',135,710),orange))
    else:
     bounds.append(drawtext(im,tm,(44,99),'5',font(DIN,650),ink))
     bounds.append(drawtext(im,tm,(386,162),'Minute',font(DIN,180),ink))
     bounds.append(drawtext(im,tm,(386,385),'Home Workout',fit(DIN,'Home Workout',150,655),orange))
    info={'font':'DIN Condensed Bold','header_bounds':[0,0,W,610],'fill':'Warm cream with orange angled top band, full headroom'}
   assert all(25<=b[0]<b[2]<=1055 for b in bounds),bounds
   assert all((240 if ig else 70)<=b[1]<b[3]<582 for b in bounds),bounds
   p=OUT/platform/f'five-minute-header-{k}.png';im.save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
   if not ig:im.save(p.with_suffix('.jpg'),quality=93)
   # Exact preservation proof on the entire area containing Dan, beginning above his hair.
   eq=np.array_equal(np.array(im)[620:],np.array(src)[620:]);assert eq
   rows.append(dict(choice=k,platform=platform,path=str(p),sha256=sha(p),source_sha256=sha(SOURCE),text_bounds=bounds,photo_below620_identical=eq,full_screen_vertical=True,**info))
 (OUT/'manifest.json').write_text(json.dumps({'status':'awaiting Dan approval of revised header','selected_base':'round3 choice2','same_copy':['5 Minute','Home Workout'],'outputs':rows},indent=2))
 sheet=Image.new('RGB',(840,1600),'#111926');d=ImageDraw.Draw(sheet);f=font('/System/Library/Fonts/Supplemental/Arial Bold.ttf',28)
 for r in rows:
  x=['A','B'].index(r['choice'])*420;y=0 if r['platform']=='instagram' else 800;d.text((x+10,y+10),r['choice']+' / '+r['platform'].title(),font=f,fill='white');im=Image.open(r['path']);im.thumbnail((400,720));sheet.paste(im,(x+10,y+58))
 sheet.save(OUT/'two-top-graphic-choices.jpg',quality=95)
 print('Built two paired top-graphic options; photo below620px exactly preserved')
if __name__=='__main__':build()
