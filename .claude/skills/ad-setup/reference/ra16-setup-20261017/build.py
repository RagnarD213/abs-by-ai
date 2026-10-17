from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import json, math
import numpy as np
B=Path(__file__).resolve().parent; OUT=B.parent
MAN=Path.home()/'Library/Fonts/Manrope.ttf'; SYS=Path('/System/Library/Fonts/Supplemental')
QC=[]
def font(sz,kind='man'):
 if kind=='man':
  f=ImageFont.truetype(str(MAN),int(sz));f.set_variation_by_name('ExtraBold');return f
 files={'din':'DIN Condensed Bold.ttf','serif':'Georgia Bold.ttf','heavy':'Arial Black.ttf'}
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

def person(c,n,rect,keep):
 p=Image.open(B/'cut'/('pool.png' if n==1 else 'studio.png')).convert('RGBA')
 p=p.crop(p.getchannel('A').point(lambda v:255 if v>100 else 0).getbbox());p=p.crop((0,0,p.width,round(p.height*keep)))
 x,y,w,h=rect;s=min(w/p.width,h/p.height);p=p.resize((round(p.width*s),round(p.height*s)),Image.Resampling.LANCZOS)
 px=round(x+(w-p.width)/2);py=round(y+h-p.height)
 mask=Image.new('L',c.size);mask.paste(p.getchannel('A'),(px,py))
 c=c.convert('RGBA')
 if n==2:
  halo=Image.new('RGBA',c.size,'#fffaf3');halo.putalpha(mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(3)));c=Image.alpha_composite(c,halo)
 c.alpha_composite(p,(px,py));return c.convert('RGB'),np.asarray(mask)>100

def clear(mask,boxes):
 if mask is None:return None
 ys,xs=np.where(mask);ds=[]
 for x0,y0,x1,y1 in boxes:
  dist=np.hypot(np.maximum(np.maximum(x0-xs,xs-x1),0),np.maximum(np.maximum(y0-ys,ys-y1),0));ds.append(float(dist.min()))
 return round(min(ds),1)

def build(n,vertical):
 W,H=(1080,1920) if vertical else (1280,720);sz=(W,H);mask=None
 a=Image.open(B/'assets'/f'option{n}.png').convert('RGB')
 if n==1:
  c=fit(a,sz);arr=np.array(c).astype(float)
  ramp=np.maximum(0,1-np.arange(H if vertical else W)/((H if vertical else W)*.7))*.84
  arr=arr*(1-(ramp[:,None,None] if vertical else ramp[None,:,None]))+np.array([1,31,36])*(ramp[:,None,None] if vertical else ramp[None,:,None]);c=Image.fromarray(arr.astype('uint8'))
  c,mask=person(c,n,(W*.49,H*.03,W*.50,H*.97) if not vertical else (W*.04,H*.42,W*.92,H*.58),.68)
  boxes,fs=lines(c,['AI TOOK','MY JOB'] if not vertical else ['AI TOOK','MY JOB'],(W*.045,H*.18,W*.43,H*.64) if not vertical else (W*.065,H*.075,W*.87,H*.28),'din',['white','#ffe65b'],stroke=1,align='left' if not vertical else 'center',gap=.14)
 elif n==2:
  c=fit(a,sz);band=round(H*(.72 if vertical else .70))
  c,mask=person(c,n,(W*.02,H*.03,W*.96,band-H*.03),.80 if vertical else .67)
  d=ImageDraw.Draw(c);d.rectangle((0,band,W,H),fill='#fffaf3');mask[band:]=False
  d.polygon([(0,band),(W*.15,band),(W*.10,H),(0,H)],fill='#e42e28')
  boxes,fs=lines(c,['AI TOOK','MY JOB'] if vertical else ['AI TOOK MY JOB'],(W*.18,band+H*.035,W*.78,H-band-H*.07),'heavy',['#141515'],align='center',gap=.08)
 elif n==3:
  if not vertical:
   c=Image.new('RGB',sz,'#082451');panel=fit(a,(round(W*.62),H),centering=(.5,.48));c.paste(panel,(round(W*.38),0))
   d=ImageDraw.Draw(c);d.line((W*.355,H*.09,W*.355,H*.91),fill='#e8cda0',width=2)
   boxes,fs=lines(c,['AI Took','My Job'],(W*.035,H*.20,W*.29,H*.6),'serif',['#fff1d4'],gap=.22)
  else:
   band=round(H*.27);c=Image.new('RGB',sz,'#fff1d4');c.paste(fit(a,(W,H-band)),(0,band))
   boxes,fs=lines(c,['AI Took','My Job'],(W*.06,H*.035,W*.88,band-H*.075),'serif',['#082451'],align='center',gap=.13)
 elif n==4:
  c=Image.new('RGB',sz,'#1b0a35')
  if vertical:
   band=round(H*.30);c.paste(fit(a,(W,H-band),centering=(.5,.64)),(0,band))
   boxes,fs=lines(c,['AI TOOK','MY JOB'],(W*.07,H*.035,W*.86,band-H*.075),'man',['#b8ffed','white'],align='left',gap=.08)
  else:
   c.paste(fit(a,(round(W*.55),H),centering=(.5,.67)),(round(W*.45),0))
   d=ImageDraw.Draw(c);d.rounded_rectangle((W*.035,H*.13,W*.48,H*.89),radius=22,fill='#a8ffde')
   boxes,fs=lines(c,['AI','TOOK','MY JOB'],(W*.065,H*.18,W*.38,H*.66),'man',['#240c48'],align='left',gap=.08)
 else:
  if vertical:
   c=fit(a,sz,centering=(.5,.65));d=ImageDraw.Draw(c);d.rectangle((0,0,W,H*.265),fill='#f5eddb')
   d.rectangle((W*.06,H*.04,W*.075,H*.23),fill='#f86d19')
   boxes,fs=lines(c,['AI Took','My Job'],(W*.12,H*.045,W*.82,H*.18),'heavy',['#181817'],align='left',gap=.15)
  else:
   c=Image.new('RGB',sz,'#f5eddb');c.paste(fit(a,(round(W*.60),H),centering=(.5,.7)),(round(W*.4),0))
   d=ImageDraw.Draw(c);d.rectangle((W*.045,H*.12,W*.065,H*.88),fill='#f86d19')
   boxes,fs=lines(c,['AI Took','My Job'],(W*.09,H*.20,W*.32,H*.6),'heavy',['#181817'],align='left',gap=.20)
 name=f'option-{n}-'+('9x16' if vertical else '16x9')+'.jpg';c.save(OUT/name,quality=94,subsampling=0,optimize=True)
 distance=clear(mask,boxes)
 result={'option':n,'format':'9x16' if vertical else '16x9','file':name,'size':list(sz),'font_size':fs,'text_boxes':boxes,'person_text_clearance_px':distance,'bytes':(OUT/name).stat().st_size,'pass':(distance is None or distance>=25) and (OUT/name).stat().st_size<2000000}
 QC.append(result);print(json.dumps(result));return c

def sheet():
 sw=1500;row=550;top=108;pad=24;im=Image.new('RGB',(sw,top+row*5+20),'#e9edf3');d=ImageDraw.Draw(im)
 d.text((pad,20),'AI Took My Job: Five Thumbnail Choices',font=font(38),fill='#152139')
 d.text((pad,70),'Each number includes a horizontal and a vertical version.',font=font(23),fill='#526178')
 names=['Real Pool Photo','Real Studio Photo','AI Dan Hands Over The Job','The Robot Trainer','The Empty Trainer Chair']
 for i in range(5):
  y=top+i*row;d.rounded_rectangle((15,y,sw-15,y+row-14),radius=15,fill='white')
  d.text((pad+8,y+10),f'{i+1}. {names[i]}',font=font(27),fill='#142138')
  h=Image.open(OUT/f'option-{i+1}-16x9.jpg');h.thumbnail((845,475));im.paste(h,(pad+8,y+49))
  v=Image.open(OUT/f'option-{i+1}-9x16.jpg');v.thumbnail((267,475));im.paste(v,(975,y+49))
  d.text((1270,y+220),'16:9',font=font(23),fill='#3b4b65');d.text((1270,y+255),'and 9:16',font=font(21),fill='#6c7890')
 im.save(OUT/'REVIEW-five-options.jpg',quality=93)
if __name__=='__main__':
 for n in range(1,6):
  for v in [False,True]:build(n,v)
 (B/'qc.json').write_text(json.dumps(QC,indent=2)+'\n');sheet()
 if not all(x['pass'] for x in QC):raise SystemExit('Thumbnail clearance or size check failed')
