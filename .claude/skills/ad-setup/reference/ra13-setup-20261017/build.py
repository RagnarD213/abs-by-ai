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
  halo=Image.new('RGBA',c.size,'#98ff27');halo.putalpha(mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(3)));c=Image.alpha_composite(c,halo)
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
  if not vertical:
   ramp=np.maximum(0,1-np.arange(W)/(W*.72))*.68;arr=arr*(1-ramp[None,:,None])+np.array([3,26,51])[None,None,:]*ramp[None,:,None]
  else:
   ramp=np.maximum(0,1-np.arange(H)/(H*.53))*.78;arr=arr*(1-ramp[:,None,None])+np.array([3,26,51])[None,None,:]*ramp[:,None,None]
  c=Image.fromarray(arr.astype('uint8'))
  r=(W*.49,H*.04,W*.53,H*.96) if not vertical else (W*.02,H*.39,W*.96,H*.61)
  c,mask=person(c,n,r,.70)
  rect=(W*.045,H*.14,W*.45,H*.71) if not vertical else (W*.06,H*.055,W*.88,H*.29)
  boxes,fs=lines(c,['WHY MOST','GUYS NEVER','GET ABS'] if not vertical else ['WHY MOST GUYS','NEVER GET ABS'],rect,'din',['white','white','#ffdd35'],stroke=2,align='left' if not vertical else 'center')
 elif n==2:
  c=fit(a,sz);band=round(H*(.66 if vertical else .68))
  c,mask=person(c,n,(W*.05,H*.04,W*.9,band-H*.04),.80 if vertical else .59)
  d=ImageDraw.Draw(c);d.rectangle((0,band,W,H),fill='#b0ff2e');d.rectangle((0,band,W,band+max(3,round(H*.008))),fill='white');mask[band:]=False
  boxes,fs=lines(c,['WHY MOST','GUYS NEVER','GET ABS'] if vertical else ['WHY MOST GUYS','NEVER GET ABS'],(W*.04,band+max(30,H*.025),W*.92,H-band-max(56,H*.05)),'heavy',['#10150c'],align='center',gap=.10)
 elif n==3:
  if not vertical:
   c=Image.new('RGB',sz,'#05216b');panel=fit(a,(round(W*.51),H));c.paste(panel,(round(W*.49),0))
   d=ImageDraw.Draw(c);d.line((W*.475,H*.08,W*.475,H*.92),fill='#99cfff',width=3)
   boxes,fs=lines(c,['Why Most','Guys Never','Get Abs'],(W*.045,H*.10,W*.39,H*.8),'serif',['#fff1cf'],gap=.13)
  else:
   band=round(H*.265);c=Image.new('RGB',sz,'#fff1cf');c.paste(fit(a,(W,H-band)),(0,band))
   boxes,fs=lines(c,['Why Most Guys','Never Get Abs'],(W*.05,H*.03,W*.90,band-H*.06),'serif',['#06236d'],align='center',gap=.15)
 elif n==4:
  c=Image.new('RGB',sz,'#f3e8cf')
  if vertical:c=fit(a,sz)
  else:c.paste(fit(a,(round(W*.62),H)),(round(W*.38),0))
  sw,sh=(round(W*.88),round(H*.30)) if vertical else (round(W*.53),round(H*.69))
  sticker=Image.new('RGBA',(sw,sh),'#e72d37');d=ImageDraw.Draw(sticker);d.rectangle((8,8,sw-8,sh-8),outline='#f9edda',width=4)
  _,fs=lines(sticker,['WHY MOST','GUYS NEVER','GET ABS'],(sw*.065,sh*.06,sw*.87,sh*.88),'man',['#fff4df'],align='left',gap=.08)
  sticker=sticker.rotate(4,resample=Image.Resampling.BICUBIC,expand=True)
  x=round(W*.05);y=round(H*.65) if vertical else round(H*.10)
  c=c.convert('RGBA');c.alpha_composite(sticker,(x,y));c=c.convert('RGB');boxes=[[x,y,x+sticker.width,y+sticker.height]]
 else:
  c=fit(a,sz,centering=(.5,.72))
  if not vertical:
   bg=fit(a,sz).filter(ImageFilter.GaussianBlur(35)); fg=ImageOps.contain(a,sz,Image.Resampling.LANCZOS)
   # The source scene keeps its full height; a soft edge blends it into atmospheric sides.
   layer=Image.new('RGBA',sz);x=(W-fg.width)//2;layer.paste(fg,(x,0));m=Image.new('L',sz);md=ImageDraw.Draw(m);md.rectangle((x+30,0,x+fg.width-30,H),fill=255);m=m.filter(ImageFilter.GaussianBlur(22));layer.putalpha(m);c=Image.alpha_composite(bg.convert('RGBA'),layer).convert('RGB')
  # Darken only the headline region, leaving the maze and the man visible.
  arr=np.array(c).astype(float);ramp=np.maximum(0,1-np.arange(H)/(H*.60))*.90;arr*=1-ramp[:,None,None];c=Image.fromarray(arr.astype('uint8'))
  boxes,fs=lines(c,['WHY MOST GUYS','NEVER GET ABS'],(W*.045,H*.045,W*.91,H*(.245 if vertical else .28)),'din',['#ffe0a0','white'],align='center',stroke=2,gap=.09)
 name=f'option-{n}-'+('9x16' if vertical else '16x9')+'.jpg';c.save(OUT/name,quality=94,subsampling=0,optimize=True)
 distance=clear(mask,boxes)
 result={'option':n,'format':'9x16' if vertical else '16x9','file':name,'size':list(sz),'font_size':fs,'text_boxes':boxes,'person_text_clearance_px':distance,'bytes':(OUT/name).stat().st_size,'pass':(distance is None or distance>=25) and (OUT/name).stat().st_size<2000000}
 QC.append(result);print(json.dumps(result));return c

def sheet():
 sw=1760;row=626;top=120;pad=32;im=Image.new('RGB',(sw,top+row*5+24),'#e9edf3');d=ImageDraw.Draw(im)
 d.text((pad,24),'Most Guys Abs: Pick One Thumbnail',font=font(42),fill='#152139')
 d.text((pad,78),'Five unique designs. Each choice includes horizontal and vertical.',font=font(23),fill='#526178')
 names=['Real Pool Photo','Real Studio Photo','AI Dan With His Plan','Generic Plans Fail','Working Without A Map']
 for i in range(5):
  y=top+i*row;d.rounded_rectangle((20,y,sw-20,y+row-16),radius=15,fill='white')
  d.text((pad+10,y+12),f'{i+1}. {names[i]}',font=font(27),fill='#142138')
  h=Image.open(OUT/f'option-{i+1}-16x9.jpg');h.thumbnail((985,555));im.paste(h,(pad+10,y+57))
  v=Image.open(OUT/f'option-{i+1}-9x16.jpg');v.thumbnail((302,537));im.paste(v,(1090,y+57))
  d.text((1430,y+215),'16:9',font=font(26),fill='#3b4b65');d.text((1430,y+255),'and',font=font(21),fill='#6c7890');d.text((1430,y+290),'9:16',font=font(26),fill='#3b4b65')
 im.save(OUT/'REVIEW-five-options.jpg',quality=93)
if __name__=='__main__':
 for n in range(1,6):
  for v in [False,True]:build(n,v)
 (B/'qc.json').write_text(json.dumps(QC,indent=2)+'\n');sheet()
 if not all(x['pass'] for x in QC):raise SystemExit('Thumbnail clearance or size check failed')
