#!/usr/bin/env python3
"""Tighten selected Soft Blue Light header around its measured text bounds."""
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('header_r4',Path(__file__).resolve().parents[1]/'round4/build.py');R4=importlib.util.module_from_spec(spec);spec.loader.exec_module(R4)
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
ROOT=R4.ROOT;OUT=ROOT/'Short-form video content/covers/review/ds55-five-minute-exercises-20261026/round5';W,H=1080,1920
SOURCE=OUT/'sources/selected-picture.png';PAD=24;GAP=24
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build():
 src=Image.open(SOURCE).convert('RGB');rows=[]
 for platform in ['instagram','youtube']:
  ig=platform=='instagram';im=src.copy();mask=Image.new('L',(W,H));d=ImageDraw.Draw(im)
  f1=R4.fit(R4.POPPINS,'5 Minute',170 if ig else 185,880);f2=R4.fit(R4.POPPINS,'Home Workout',139,885)
  y1=250 if ig else 124
  b1=d.textbbox((108,y1),'5 Minute',font=f1,anchor='lt');y2=b1[3]+GAP;b2=d.textbbox((108,y2),'Home Workout',font=f2,anchor='lt')
  box=(36,b1[1]-PAD,1044,b2[3]+PAD)
  R4.SB.glass(im,box,1.0,u=2,radius=18)
  ImageDraw.Draw(im).rounded_rectangle((66,b1[1],76,b2[3]),radius=5,fill=R4.SB.CYAN)
  bounds=[R4.drawtext(im,mask,(108,y1),'5 Minute',f1,R4.SB.CYAN),R4.drawtext(im,mask,(108,y2),'Home Workout',f2,R4.SB.WHITE)]
  assert box[1]==bounds[0][1]-PAD and box[3]==bounds[-1][3]+PAD
  assert bounds[1][1]-bounds[0][3]==GAP
  assert all((240 if ig else 70)<=b[1]<b[3]<582 for b in bounds)
  p=OUT/platform/'five-minute-header-A-tight.png';im.save(p);mask.save(p.with_name(p.stem+'.text-mask.png'))
  if not ig:im.save(p.with_suffix('.jpg'),quality=93)
  assert np.array_equal(np.array(im)[620:],np.array(src)[620:])
  rows.append(dict(platform=platform,path=str(p),sha256=sha(p),source_sha256=sha(SOURCE),text_bounds=bounds,font_sizes=[f1.size,f2.size],card_bounds=list(box),top_padding=PAD,bottom_padding=PAD,interline_gap=GAP,photo_below620_identical=True))
 (OUT/'manifest.json').write_text(json.dumps({'status':'awaiting approval of revised pair','selected_style':'Soft Blue Light A','outputs':rows},indent=2))
 sh=Image.new('RGB',(840,800),'#111926');d=ImageDraw.Draw(sh);f=R4.font('/System/Library/Fonts/Supplemental/Arial Bold.ttf',28)
 for i,r in enumerate(rows):
  d.text((i*420+10,10),r['platform'].title(),font=f,fill='white');im=Image.open(r['path']);im.thumbnail((400,720));sh.paste(im,(i*420+10,58))
 sh.save(OUT/'tightened-A-both-layouts.jpg',quality=95)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':build()
