from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter
import numpy as np
from scipy.ndimage import distance_transform_edt
HERE=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Why Zepbound Improves Your Health Even If Youre Ripped/_build-2026-10-29')
OUT=HERE.parent
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
W,H=1280,720
SUP=Path('/System/Library/Fonts/Supplemental')
PM=Path.home()/'.cache/absbyai/personmask/personmask'
FONTS={'A':SUP/'DIN Condensed Bold.ttf','B':SUP/'Impact.ttf','C':Path.home()/'Library/Fonts/Manrope.ttf','D':SUP/'Arial Bold.ttf','E':Path('/System/Library/Fonts/Avenir Next Condensed.ttc')}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(k,size):
 f=ImageFont.truetype(str(FONTS[k]),size,index=8 if k=='E' else 0)
 if k=='C':f.set_variation_by_name('ExtraBold')
 return f
def width(f,t):
 b=f.getbbox(t);return b[2]-b[0]
def put(im,tm,k,text,x,y,size,maxwidth,color,stroke=0):
 while width(font(k,size),text)+2*stroke>maxwidth:size-=1
 f=font(k,size);b=f.getbbox(text);pos=(x-b[0],y-b[1]);d=ImageDraw.Draw(im);md=ImageDraw.Draw(tm)
 if stroke:d.text((pos[0]+3,pos[1]+4),text,font=f,fill='#000000',stroke_width=stroke+1,stroke_fill='#000000')
 d.text(pos,text,font=f,fill=color,stroke_width=stroke,stroke_fill='#09101A')
 md.text(pos,text,font=f,fill=255,stroke_width=stroke+5)
 return [x-stroke,y-stroke,x+width(f,text)+stroke,y+b[3]-b[1]+stroke]
def fade(im,side='left',strength=220):
 a=np.zeros((H,W,4),dtype=np.uint8);a[:,:,:3]=[4,12,24]
 x=np.linspace(0,1,W);v=np.clip((.57-x)/.22,0,1) if side=='left' else np.clip((x-.43)/.2,0,1)
 a[:,:,3]=(strength*v)[None,:].astype(np.uint8)
 return Image.alpha_composite(im,Image.fromarray(a))
def picture(k):
 if k!='C':return ImageOps.fit(Image.open(HERE/'assets'/f'ai-{k}.png').convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
 im=Image.new('RGBA',(W,H),'#0A1624')
 d=ImageDraw.Draw(im);d.polygon([(0,0),(610,0),(650,720),(0,720)],fill='#162D42')
 src=ROOT/'photos/finalized social media photos/_cutouts/studio-white-32_CUTOUT.png'
 raw=Image.open(src).convert('RGBA');b=raw.getchannel('A').getbbox();b=(b[0],b[1],b[2],int(raw.height*.73))
 sub=raw.crop(b);scale=710/sub.height;sub=sub.resize((round(sub.width*scale),710),Image.Resampling.LANCZOS)
 # The real photograph is resized and composited only. No generated pixels replace the person.
 x=35;y=28
 a=Image.new('L',(W,H));a.paste(sub.getchannel('A'),(x,y))
 glow=Image.new('RGBA',(W,H),'#53D9ED');glow.putalpha(a.filter(ImageFilter.GaussianBlur(17)).point(lambda v:round(v*.35)))
 im=Image.alpha_composite(im,glow);im.alpha_composite(sub,(x,y))
 (HERE/'real-source.json').write_text(json.dumps({'source':str(src),'sha256':sha(src),'crop':b,'scale':scale,'position':[x,y],'person_pixels_preserved':True},indent=2))
 return im
def build(k):
 im=picture(k);im.convert('RGB').save(HERE/f'picture-{k}.jpg',quality=97)
 mp=HERE/f'person-{k}.png'
 subprocess.run([str(PM),str(HERE/f'picture-{k}.jpg'),str(mp)],check=True,capture_output=True)
 person=np.array(Image.open(mp).convert('L').resize((W,H)))>100
 tm=Image.new('L',(W,H));boxes=[]
 if k=='A':
  im=fade(im);d=ImageDraw.Draw(im)
  d.rectangle((32,197,560,365),fill='#FFD400')
  boxes += [put(im,tm,k,'Zepbound',47,218,142,488,'#09101A')]
  boxes += [put(im,tm,k,'Even If',47,395,112,500,'white')]
  boxes += [put(im,tm,k,"You're Ripped?",47,520,115,500,'#FFD400')]
 elif k=='B':
  im=fade(im,'right',245)
  for t,y,size,col in [('Zepbound',80,133,'white'),('Even If',225,119,'#D8E4F3'),("You're",365,123,'white'),('Ripped?',505,151,'#FFD244')]:boxes.append(put(im,tm,k,t,690,y,size,545,col))
  ImageDraw.Draw(im).rectangle((690,672,1230,682),fill='#FFD244')
 elif k=='C':
  for t,y,size,col in [('Zepbound',130,104,'#52DDEB'),('Even If',276,81,'white'),("You're",395,94,'white'),('Ripped?',518,117,'white')]:boxes.append(put(im,tm,k,t,650,y,size,570,col))
  ImageDraw.Draw(im).rectangle((650,93,1210,101),fill='#52DDEB')
 elif k=='D':
  ImageDraw.Draw(im).rectangle((0,0,W,192),fill='#FFD400')
  boxes.append(put(im,tm,k,'Zepbound',32,47,124,640,'#101114'))
  boxes.append(put(im,tm,k,"Even If You're",712,31,62,530,'#101114'))
  boxes.append(put(im,tm,k,'Ripped?',712,104,91,530,'#A41F16'))
 elif k=='E':
  im=fade(im,'left',235)
  for t,y,size,col in [('Zepbound',336,123,'white'),('Even If',469,90,'#F1B44E'),("You're Ripped?",572,100,'white')]:boxes.append(put(im,tm,k,t,42,y,size,560,col))
 im.convert('RGB').save(OUT/f'RO28-thumbnail-{k}.jpg',quality=95,subsampling=0)
 tm.save(HERE/f'text-{k}.png')
 text=np.array(tm)>0
 overlap=int((text & person).sum());dist=distance_transform_edt(~person);clearance=float(dist[text].min()) if text.any() else 0
 p=OUT/f'RO28-thumbnail-{k}.jpg'
 result={'letter':k,'file':p.name,'size':[W,H],'bytes':p.stat().st_size,'sha256':sha(p),'person_text_overlap_pixels':overlap,'minimum_person_text_clearance_px':round(clearance,2),'text_boxes':boxes,'pass':overlap==0 and clearance>=20 and p.stat().st_size<2000000}
 print(json.dumps(result));return result
if __name__=='__main__':
 import sys
 keys=sys.argv[1:] or list('ABCDE');res=[build(k) for k in keys]
 if keys==list('ABCDE'):
  (HERE/'qc.json').write_text(json.dumps(res,indent=2))
  sheet=Image.new('RGB',(1640,1590),'#101923');d=ImageDraw.Draw(sheet);f=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),32)
  d.text((30,20),'Zepbound Even If Ripped: Five Thumbnail Choices',font=f,fill='white')
  label=ImageFont.truetype(str(SUP/'Arial.ttf'),23)
  names={'A':'Pharmacist Double-Take','B':'Doctor Consultation','C':'Real Studio Photo','D':'Poolside Medication','E':'After The Gym'}
  for i,r in enumerate(res):
   x=30+(i%2)*810;y=85+(i//2)*490
   d.text((x,y),r['letter']+'  '+names[r['letter']],font=f,fill='#FFD400')
   sheet.paste(Image.open(OUT/r['file']).resize((770,433),Image.Resampling.LANCZOS),(x,y+43))
  d.text((840,1120),'Pick A, B, C, D Or E.',font=f,fill='white')
  d.text((840,1170),'C uses your real photograph.',font=label,fill='#D4DFEA')
  d.text((840,1210),'The other four are AI concepts of you.',font=label,fill='#D4DFEA')
  sheet.save(OUT/'REVIEW-five-thumbnails.jpg',quality=93)
