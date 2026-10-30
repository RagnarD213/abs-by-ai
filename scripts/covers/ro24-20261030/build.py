from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter
from scipy.ndimage import distance_transform_edt
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');O=P/'social media graphics/youtube/thumbnails/Reacting To Celebrity Ozempic Transformations';B=O/'_build-2026-10-30';W,H=1280,720
SUP=Path('/System/Library/Fonts/Supplemental');PM=Path.home()/'.cache/absbyai/personmask/personmask'
REAL=P/'photos/finalized social media photos/_cutouts/studio-blue-249_CUTOUT.png'
fonts={'A':SUP/'Impact.ttf','B':SUP/'Impact.ttf','C':Path.home()/'Library/Fonts/Manrope.ttf','D':SUP/'Impact.ttf','E':SUP/'DIN Condensed Bold.ttf'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(k,n):
 f=ImageFont.truetype(str(fonts[k]),n)
 if k=='C':f.set_variation_by_name('ExtraBold')
 return f
def put(im,mask,k,text,xy,size,maxw,color,stroke=0,center=False):
 x,y=xy
 while True:
  f=font(k,size);b=f.getbbox(text);ww=b[2]-b[0]
  if ww+2*stroke<=maxw:break
  size-=1
 if center:x+=round((maxw-ww)/2)
 pos=(x-b[0],y-b[1]);ImageDraw.Draw(im).text(pos,text,font=f,fill=color,stroke_width=stroke,stroke_fill='#050505');ImageDraw.Draw(mask).text(pos,text,font=f,fill=255,stroke_width=stroke+3)
 return dict(text=text,font_size=size,rect=[x-stroke,y-stroke,x+ww+stroke,y+b[3]-b[1]+stroke])
def block(im,mask,k,text,y,h,x0,x1,bg,fg):
 d=ImageDraw.Draw(im);d.rectangle((x0+9,y+9,x1+9,y+h+9),fill='#000000');d.rectangle((x0,y,x1,y+h),fill=bg)
 return put(im,mask,k,text,(x0+22,y+14),h,x1-x0-44,fg,center=True)
def fade(im,side,strength):
 a=np.zeros((H,W,4),dtype=np.uint8);a[:,:,:3]=[6,6,8];x=np.arange(W)/W;v=np.clip((.52-x)/.3,0,1) if side=='left' else np.clip((x-.48)/.27,0,1);a[:,:,3]=(strength*v)[None,:].astype(np.uint8);return Image.alpha_composite(im,Image.fromarray(a))
def picture(k):
 if k!='C':return ImageOps.fit(Image.open(B/'assets'/f'ai-{k}.png').convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
 im=ImageOps.fit(Image.open(B/'assets/background-C.png').convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA');raw=Image.open(REAL).convert('RGBA');bb=raw.getchannel('A').getbbox();crop=[bb[0],bb[1],bb[2],round(bb[1]+(bb[3]-bb[1])*.70)];src=raw.crop(crop);scale=694/src.height;src=src.resize((round(src.width*scale),694),Image.Resampling.LANCZOS);x,y=6,26
 alpha=Image.new('L',(W,H));alpha.paste(src.getchannel('A'),(x,y));white=Image.new('RGBA',(W,H),'#FFFFFF');white.putalpha(alpha.filter(ImageFilter.MaxFilter(7)));im=Image.alpha_composite(im,white);im.alpha_composite(src,(x,y))
 (B/'real-photo-provenance.json').write_text(json.dumps(dict(source=str(REAL),sha256=sha(REAL),crop=crop,scale=scale,position=[x,y],person_pixels='Original cutout transformed by crop/resize/composite only; no AI redraw or colour/body alteration'),indent=2)+'\n');return im
names={'A':'Same Drug, Same You, Two Outcomes','B':'You Reacting In Disbelief','C':'Real Studio Photograph','D':'Lifting Alongside The Pen','E':'Red Carpet Secret'}
def build(k):
 im=picture(k);pp=B/f'picture-{k}.jpg';im.convert('RGB').save(pp,quality=98)
 mp=B/f'person-{k}.png';subprocess.run([str(PM),str(pp),str(mp)],check=True,capture_output=True);person=np.array(Image.open(mp).convert('L').resize((W,H)))>100
 tm=Image.new('L',(W,H));boxes=[];d=ImageDraw.Draw(im)
 if k=='A':
  d.rectangle((0,0,1279,199),fill='#FFD400');d.rectangle((0,199,1279,206),fill='#101010')
  boxes+=[put(im,tm,k,'Ozempic:',(30,10),92,1220,'#101519',center=True),put(im,tm,k,'Ripped Or Ruined?',(30,100),100,1220,'#C21A12',center=True)]
 elif k=='B':
  boxes+=[block(im,tm,k,'Ozempic:',96,140,680,1236,'#FFD400','#0A0A0A'),block(im,tm,k,'Ripped Or',276,140,680,1236,'#E01B1B','#FFFFFF'),block(im,tm,k,'Ruined?',456,170,680,1236,'#0A0A0A','#FFD400')]
 elif k=='C':
  boxes+=[put(im,tm,k,'Ozempic:',(650,128),96,590,'#FFFFFF'),put(im,tm,k,'Ripped Or',(650,242),104,590,'#FFFFFF'),put(im,tm,k,'Ruined?',(650,366),112,590,'#FF4B3E')]
 elif k=='D':
  im=fade(im,'left',150)
  boxes+=[put(im,tm,k,'Ozempic:',(40,158),112,520,'#FFFFFF'),put(im,tm,k,'Ripped',(40,288),134,520,'#6FE3F0'),put(im,tm,k,'Or Ruined?',(40,436),112,520,'#FFFFFF')]
 else:
  im=fade(im,'right',185)
  boxes+=[put(im,tm,k,'Ozempic:',(700,150),120,530,'#FFFFFF',stroke=2),put(im,tm,k,'Ripped Or',(700,284),150,530,'#F4C95D',stroke=2),put(im,tm,k,'Ruined?',(700,430),150,530,'#FFFFFF',stroke=2)]
 out=O/f'RO24-thumbnail-{k}.jpg';im.convert('RGB').save(out,quality=95,subsampling=0);tm.save(B/f'text-{k}.png');text=np.array(tm)>0;overlap=int((text&person).sum());clear=float(distance_transform_edt(~person)[text].min());im.convert('RGB').resize((320,180),Image.Resampling.LANCZOS).save(O/f'RO24-thumbnail-{k}-feed.jpg',quality=94)
 r=dict(letter=k,name=names[k],file=out.name,sha256=sha(out),bytes=out.stat().st_size,size=[W,H],person_text_overlap_pixels=overlap,minimum_person_text_clearance_px=round(clear,2),text_boxes=boxes,pass_checks=overlap==0 and clear>=20 and out.stat().st_size<2000000);print(json.dumps({x:r[x] for x in ('letter','bytes','person_text_overlap_pixels','minimum_person_text_clearance_px','pass_checks')}),flush=True);return r
if __name__=='__main__':
 keys=sys.argv[1:] or list('ABCDE');res=[build(k) for k in keys]
 if keys==list('ABCDE'):
  (B/'qc.json').write_text(json.dumps(res,indent=2)+'\n');sheet=Image.new('RGB',(1640,1590),'#0A1D30');dr=ImageDraw.Draw(sheet);f=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),28);small=ImageFont.truetype(str(SUP/'Arial.ttf'),24);dr.text((30,15),'Celebrity Ozempic: Five Thumbnail Choices',font=f,fill='white')
  for i,item in enumerate(res):
   x=30+(i%2)*810;y=76+(i//2)*490;dr.text((x,y),item['letter']+'  '+names[item['letter']],font=f,fill='#FFE26A');sheet.paste(Image.open(O/item['file']).resize((770,433),Image.Resampling.LANCZOS),(x,y+40))
  dr.text((842,1120),'Pick A, B, C, D Or E.',font=f,fill='white');dr.text((842,1170),'C is your real studio photograph.',font=small,fill='#D5E7EF');dr.text((842,1220),'A, B, D and E are new AI scenes of you.',font=small,fill='#D5E7EF');sheet.save(O/'REVIEW-five-thumbnails.jpg',quality=94)
  ph=Image.new('RGB',(1720,240),'#0F0F0F')
  for i,item in enumerate(res):ph.paste(Image.open(O/f"RO24-thumbnail-{item['letter']}-feed.jpg"),(20+i*340,30))
  ph.save(O/'REVIEW-phone-size.jpg',quality=94)
