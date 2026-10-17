from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import json, math
import numpy as np
B=Path(__file__).resolve().parent; OUT=B.parent/'R2'
MAN=Path.home()/'Library/Fonts/Manrope.ttf'; SYS=Path('/System/Library/Fonts/Supplemental')
QC=[]
def font(sz,kind='man'):
 if kind=='man':
  f=ImageFont.truetype(str(MAN),int(sz));f.set_variation_by_name('ExtraBold');return f
 files={'din':'DIN Condensed Bold.ttf','serif':'Georgia Bold.ttf','heavy':'Arial Black.ttf','impact':'Impact.ttf','italic':'Georgia Bold Italic.ttf'}
 return ImageFont.truetype(str(SYS/files[kind]),int(sz))
def fit(im,size,centering=(.5,.5)):return ImageOps.fit(im.convert('RGB'),size,Image.Resampling.LANCZOS,centering=centering)
def lines(c,words,rect,kind,colors,stroke=0,align='left',gap=.12):
 x,y,w,h=rect;size=int(h/len(words)*1.3)
 while size>10:
  f=font(size,kind);bbs=[f.getbbox(t,stroke_width=stroke) for t in words];widths=[a[2]-a[0] for a in bbs];heights=[a[3]-a[1] for a in bbs];g=int(size*gap)
  if max(widths)<=w and sum(heights)+g*(len(words)-1)<=h:break
  size-=1
 yy=y+(h-sum(heights)-g*(len(words)-1))/2;d=ImageDraw.Draw(c);boxes=[]
 for i,(t,b,ww,hh) in enumerate(zip(words,bbs,widths,heights)):
  xx=x if align=='left' else x+(w-ww)/2
  d.text((int(xx-b[0]),int(yy-b[1])),t,font=f,fill=colors[i%len(colors)],stroke_width=stroke,stroke_fill='#071c37')
  boxes.append([int(xx),int(yy),int(xx+ww),int(yy+hh)]);yy+=hh+g
 return boxes,size

def build(n,vertical):
 W,H=(1080,1920) if vertical else (1280,720);fmt='9x16' if vertical else '16x9'
 a=Image.open(B/'assets'/f'option{n}-{fmt}.png').convert('RGB');c=fit(a,(W,H));d=ImageDraw.Draw(c)
 if n==1:
  rect=(W*.05,H*.775,W*.90,H*.19) if vertical else (W*.035,H*.76,W*.93,H*.205)
  words=['Fire your','trainer.'] if vertical else ['Fire your trainer.']
  boxes,fs=lines(c,words,rect,'impact',['#ffe541','white'] if vertical else ['#ffe541'],stroke=4,align='center',gap=.07)
 elif n==2:
  words=['Fire your','trainer.'] if vertical else ['Fire your trainer.']
  rect=(W*.055,H*.035,W*.89,H*.175) if vertical else (W*.045,H*.025,W*.91,H*.18)
  boxes,fs=lines(c,words,rect,'heavy',['#e62728'],stroke=0,align='center',gap=.04)
 else:
  words=['Fire your','trainer.'] if vertical else ['Fire your trainer.']
  rect=(W*.06,H*.79,W*.88,H*.17) if vertical else (W*.04,H*.795,W*.92,H*.16)
  boxes,fs=lines(c,words,rect,'italic',['white','#50f0ff'] if vertical else ['#69f0ff'],stroke=2,align='center',gap=.09)
 out=OUT/f'option-{n}-{fmt}.jpg';c.save(out,quality=95,subsampling=0,optimize=True)
 qc={'option':n,'format':fmt,'size':[W,H],'font_size':fs,'text_boxes':boxes,'bytes':out.stat().st_size,'file':str(out),'pass':out.stat().st_size<2000000}
 QC.append(qc);print(json.dumps(qc));return c

def sheet():
 sw=1500;row=550;top=110;im=Image.new('RGB',(sw,top+row*3+20),'#e8edf4');d=ImageDraw.Draw(im)
 d.text((28,20),'Fire your trainer. Three New Designs',font=font(39),fill='#12233d')
 d.text((28,73),'AI Took Job AD Setup | Round 2 | Pick 1, 2 or 3',font=font(23),fill='#536179')
 names=['Original Bench-Press Frame','Dan Fired, Robot Takes Over','Dan Fired, AI Trainer From A Phone']
 for n in range(1,4):
  y=top+(n-1)*row;d.rounded_rectangle((15,y,sw-15,y+row-14),radius=14,fill='white')
  d.text((32,y+9),f'{n}. {names[n-1]}',font=font(27),fill='#142138')
  a=Image.open(OUT/f'option-{n}-16x9.jpg');a.thumbnail((845,475));im.paste(a,(32,y+49))
  a=Image.open(OUT/f'option-{n}-9x16.jpg');a.thumbnail((267,475));im.paste(a,(975,y+49))
  d.text((1270,y+220),'16:9',font=font(23),fill='#3b4b65');d.text((1270,y+255),'and 9:16',font=font(21),fill='#6c7890')
 im.save(OUT/'REVIEW-three-options-R2.jpg',quality=94)
if __name__=='__main__':
 OUT.mkdir(exist_ok=True)
 for n in range(1,4):
  for v in [False,True]:build(n,v)
 (B/'qc.json').write_text(json.dumps(QC,indent=2)+'\n');sheet()
 if not all(x['pass'] for x in QC):raise SystemExit('Thumbnail size check failed')
