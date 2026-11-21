#!/usr/bin/env python3
"""Four designed layouts around Dan's chosen X3 image; no generation or person repainting."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np, json,hashlib,subprocess
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'Short-form video content/covers/review/ds52-zepbound-free-20261102'
OUT=BASE/'r2';OUT.mkdir(exist_ok=True)
SRC=BASE/'sources/D.png';W,H=1080,1920
SUP=Path('/System/Library/Fonts/Supplemental')
FONTS={'cond':SUP/'DIN Condensed Bold.ttf','impact':SUP/'Impact.ttf','sans':Path.home()/'Library/Fonts/Manrope.ttf','serif':SUP/'Baskerville.ttc'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(name,size):
 f=ImageFont.truetype(str(FONTS[name]),int(size))
 if name=='sans':f.set_variation_by_name('ExtraBold')
 return f
def fit(word,name,size,width):
 while size>20:
  f=font(name,size)
  if f.getbbox(word)[2]<=width:return f
  size-=1
 raise ValueError(word)
def bg(c0,c1,spot=None):
 yy,xx=np.mgrid[0:H,0:W];a=np.clip(yy/H,0,1)[...,None]
 ar=np.array(c0)[None,None,:]*(1-a)+np.array(c1)[None,None,:]*a
 ar=np.broadcast_to(ar,(H,W,3)).copy()
 if spot:
  x,y,rad,col,strength=spot;t=np.exp(-(((xx-x)/rad)**2+((yy-y)/rad)**2)*2)[...,None]*strength
  ar=ar*(1-t)+np.array(col)[None,None,:]*t
 return Image.fromarray(np.uint8(np.clip(ar,0,255))).convert('RGBA')
def make_cutout():
 im=Image.open(SRC).convert('RGB');a=np.array(im).astype(float);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
 blue=(b>r*1.12)&(b>g*1.08)&(b>14)
 seed=np.zeros(blue.shape,bool);seed[:,0]=seed[:,-1]=True;seed[0,:]=seed[-1,:]=True
 rm=ndimage.binary_propagation(seed&blue,mask=blue)
 alpha=np.uint8(~rm)*255
 # Remove disconnected background fringes and preserve hard interior person/prop pixels.
 alpha=Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.45))
 ar=np.array(alpha).astype(float)
 # The source already fades naturally into navy below the shorts. End on those same shorts.
 fade=np.clip((1155-np.arange(im.height))/100,0,1);ar*=fade[:,None]
 cut=im.convert('RGBA');cut.putalpha(Image.fromarray(np.uint8(ar)))
 cut=cut.crop((0,50,941,1155));cut.save(OUT/'same-image-cutout.png')
 return cut
CUT=make_cutout()
RECORD=[]
def label(im,tm,text,x,y,size=120,name='cond',color='white',width=960,anchor='lt',stroke=0):
 f=fit(text,name,size,width);d=ImageDraw.Draw(im);m=ImageDraw.Draw(tm)
 d.text((x,y),text,font=f,fill=color,anchor=anchor,stroke_width=stroke,stroke_fill=color)
 m.text((x,y),text,font=f,fill=255,anchor=anchor,stroke_width=stroke)
 b=d.textbbox((x,y),text,font=f,anchor=anchor,stroke_width=stroke)
 RECORD.append({'text':text,'box':list(b)})
 return b
def display_word(im,tm,text,x,y,width,height,color,name='impact'):
 f=font(name,360);b=f.getbbox(text);layer=Image.new('RGBA',(b[2]+12,b[3]-b[1]+12));d=ImageDraw.Draw(layer)
 d.text((6,6-b[1]),text,font=f,fill=color)
 box=layer.getchannel('A').getbbox();layer=layer.crop(box).resize((width,height),Image.Resampling.LANCZOS)
 im.alpha_composite(layer,(x,y));tm.paste(Image.fromarray(np.maximum(np.array(tm.crop((x,y,x+width,y+height))),np.array(layer.getchannel('A')))),(x,y))
 RECORD.append({'text':text,'box':[x,y,x+width,y+height]})
def person(im,width,head,x=None):
 p=CUT.resize((width,round(CUT.height*width/CUT.width)),Image.Resampling.LANCZOS)
 # Source hair starts around y=89; cutout begins at50.
 y=round(head-(89-50)*width/941);x=(W-width)//2 if x is None else x
 # Grounded local shadow stays behind the original person pixels.
 shadow=Image.new('RGBA',im.size);z=Image.new('RGBA',p.size,(0,0,0,180));z.putalpha(p.getchannel('A').point(lambda v:round(v*.4)))
 shadow.alpha_composite(z,(x+8,y+18));shadow=shadow.filter(ImageFilter.GaussianBlur(22));im.alpha_composite(shadow)
 im.alpha_composite(p,(x,y))
 return {'width':width,'xy':[x,y],'hair_target':head,'scale':width/941}
def finish(im,tm,n,pf,placement):
 d=OUT/pf;d.mkdir(exist_ok=True)
 p=d/f'Zepbound-Free-Design-{n}-{pf}.png';im.convert('RGB').save(p)
 im.convert('RGB').save(p.with_suffix('.jpg'),quality=95)
 tm.save(p.with_name(p.stem+'-text-mask.png'))
 if pf=='instagram':im.crop((0,240,1080,1680)).convert('RGB').save(OUT/f'Design-{n}-profile.jpg',quality=95)
 row={'design':n,'platform':pf,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'jpeg_sha256':sha(p.with_suffix('.jpg')),'bytes':p.stat().st_size,'jpeg_bytes':p.with_suffix('.jpg').stat().st_size,'text':RECORD.copy(),'placement':placement}
 assert all(36<=b['box'][0]<b['box'][2]<=1044 for b in RECORD),RECORD
 assert all((240 if pf=='instagram' else 50)<=b['box'][1]<b['box'][3]<=(1680 if pf=='instagram' else 1840) for b in RECORD),RECORD
 assert row['jpeg_bytes']<2_000_000
 return row
rows=[]
for pf in ['instagram','youtube']:
 ig=pf=='instagram';top=260 if ig else 90
 for n in [1,2,3,4]:
  RECORD.clear();tm=Image.new('L',(W,H));off=0 if ig else -150
  if n==1:
   im=bg((10,39,128),(3,10,28),(540,1050,850,(33,102,226),.75));d=ImageDraw.Draw(im)
   # A fine editorial frame, broad halo and one restrained electric accent.
   d.ellipse((-380,620,1450,2350),outline='#2358BC',width=3)
   d.line((64,top-10,1016,top-10),fill='#B6F33C',width=5)
   label(im,tm,'Why Zepbound',64,top+35,130,'sans',width=950)
   label(im,tm,'Is Actually',64,top+182,105,'sans',color='#D7E5FF',width=950)
   display_word(im,tm,'Free',64,top+302,952,198,'#C2F34C')
   pl=person(im,970,head=790 if ig else 620)
   # Small corner brackets give the hero a deliberate photographic frame.
   d=ImageDraw.Draw(im);d.line((60,1590,60,1640,130,1640),fill='#9FCD44',width=3)
   d.line((1020,1590,1020,1640,950,1640),fill='#9FCD44',width=3)
  elif n==2:
   im=bg((239,233,220),(223,217,204));d=ImageDraw.Draw(im)
   # A magazine-like offset column with quiet rules and a full-width hero picture.
   d.rectangle((0,0,27,H),fill='#D13B25');d.line((65,top-12,1015,top-12),fill='#1B2328',width=2)
   label(im,tm,'Why Zepbound',64,top+20,135,'serif',color='#20292D',width=950)
   label(im,tm,'Is Actually',68,top+164,100,'sans',color='#20292D',width=900)
   d=ImageDraw.Draw(im);d.line((68,top+291,470,top+291),fill='#C83220',width=6)
   # Portrait off the central axis and an oversized red lower word create an editorial cover.
   pl=person(im,890,head=625 if ig else 430,x=158)
   free_y=1460 if ig else 1520
   display_word(im,tm,'Free',64,free_y,952,185,'#C83220')
   d=ImageDraw.Draw(im);d.line((64,free_y-27,1016,free_y-27),fill='#C83220',width=2)
  elif n==3:
   im=bg((8,47,37),(2,21,20),(540,600,1000,(26,92,64),.8));d=ImageDraw.Draw(im)
   d.rounded_rectangle((54,top-12,1026,1790 if not ig else 1700),radius=34,outline='#769B7B',width=2)
   # Subject is above a receipt whose notched edge explains the money angle without extra claims.
   pl=person(im,960,head=280 if ig else 125)
   y=1220 if ig else 1270
   panel=Image.new('RGBA',(W,H));pd=ImageDraw.Draw(panel)
   pd.rounded_rectangle((42,y-32,1038,1770 if not ig else 1680),radius=24,fill='#F2EBDD')
   for x in range(70,1030,40):pd.ellipse((x-11,y-43,x+11,y-21),fill='#073B2C')
   im.alpha_composite(panel)
   label(im,tm,'Why Zepbound',80,y+18,149,'cond',color='#123C30',width=920)
   label(im,tm,'Is Actually',80,y+153,84,'sans',color='#254B3C',width=920)
   display_word(im,tm,'Free',80,y+260,920,175,'#12734A')
   # A thin double rule and generous inset finish the receipt treatment.
   d=ImageDraw.Draw(im);d.line((650,y+187,990,y+187),fill='#B4B39F',width=2);d.line((650,y+197,990,y+197),fill='#B4B39F',width=2)
  else:
   im=bg((18,19,23),(7,8,11),(620,900,900,(88,22,24),.9));d=ImageDraw.Draw(im)
   # An angled red title field and circular spotlight create depth around the same portrait.
   d.polygon([(0,0),(1080,0),(1080,top+460),(0,top+610)],fill='#C8302D')
   d.line((0,top+618,1080,top+468),fill='#F18D75',width=4)
   label(im,tm,'Why Zepbound',65,top+12,174,'cond',width=950)
   label(im,tm,'Is Actually Free',65,top+193,174,'cond',width=950)
   pl=person(im,980,head=780 if ig else 595)
   # The headline is upper left; diagonal architecture continues behind the cash and pen.
   d=ImageDraw.Draw(im);d.line((56,1520,56,1630,180,1630),fill='#D8453F',width=5)
  rows.append(finish(im,tm,n,pf,pl))
manifest={'status':'awaiting Dan revised-design pick','source_image':str(SRC.relative_to(ROOT)),'source_sha256':sha(SRC),'same_image_preserved':True,'generation_calls':0,'copy':'Why Zepbound Is Actually Free','outputs':rows}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
sheet=Image.new('RGB',(1440,2*680),'#121924');dr=ImageDraw.Draw(sheet);f=font('sans',26)
for row in rows:
 i=row['design']-1;j=0 if row['platform']=='instagram' else 1;x=i*360;y=j*680
 dr.text((x+14,y+15),f"{i+1} / {'Instagram' if j==0 else 'YouTube'}",font=f,fill='white')
 im=Image.open(ROOT/row['path']);im.thumbnail((334,594));sheet.paste(im,(x+13,y+65))
sheet.save(OUT/'four-designs.jpg',quality=95)
print('Built eight revised covers, source image unchanged')
