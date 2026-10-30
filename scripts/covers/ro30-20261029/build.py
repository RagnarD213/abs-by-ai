from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter
from scipy.ndimage import distance_transform_edt
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');S=Path('/Volumes/Extreme/_edit_work/RO-30/setup');O=P/'social media graphics/youtube/thumbnails/The Fastest Way To Lose Stubborn Love Handles';B=O/'_build-2026-10-29';W,H=1280,720
SUP=Path('/System/Library/Fonts/Supplemental');PM=Path.home()/'.cache/absbyai/personmask/personmask'
fonts={'A':SUP/'DIN Condensed Bold.ttf','B':SUP/'Impact.ttf','C':Path.home()/'Library/Fonts/Manrope.ttf','D':SUP/'Arial Bold.ttf','E':SUP/'Arial Bold.ttf'}
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
 pos=(x-b[0],y-b[1]);ImageDraw.Draw(im).text(pos,text,font=f,fill=color,stroke_width=stroke,stroke_fill='#071725');ImageDraw.Draw(mask).text(pos,text,font=f,fill=255,stroke_width=stroke+3)
 return dict(text=text,font_size=size,rect=[x-stroke,y-stroke,x+ww+stroke,y+b[3]-b[1]+stroke])
def fade(im,side,strength):
 a=np.zeros((H,W,4),dtype=np.uint8);a[:,:,:3]=[4,10,18];x=np.arange(W)/W;v=np.clip((.52-x)/.3,0,1) if side=='left' else np.clip((x-.48)/.27,0,1);a[:,:,3]=(strength*v)[None,:].astype(np.uint8);return Image.alpha_composite(im,Image.fromarray(a))
def picture(k):
 if k in 'ABD':return ImageOps.fit(Image.open(B/'assets'/f'ai-{k}.png').convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
 if k=='C':
  im=ImageOps.fit(Image.open(B/'assets/background-C.png').convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA');p=P/'photos/finalized social media photos/_cutouts/studio-blue-222_CUTOUT.png';raw=Image.open(p).convert('RGBA');bb=raw.getchannel('A').getbbox();crop=[bb[0],bb[1],bb[2],round(raw.height*.76)];src=raw.crop(crop);scale=690/src.height;src=src.resize((round(src.width*scale),690),Image.Resampling.LANCZOS);x,y=22,30
  alpha=Image.new('L',(W,H));alpha.paste(src.getchannel('A'),(x,y));outline=alpha.filter(ImageFilter.MaxFilter(7));white=Image.new('RGBA',(W,H),'#F4FCFF');white.putalpha(outline);im=Image.alpha_composite(im,white);im.alpha_composite(src,(x,y))
  (B/'real-photo-provenance.json').write_text(json.dumps(dict(source=str(p),sha256=sha(p),crop=crop,scale=scale,position=[x,y],person_pixels='Original cutout transformed by crop/resize/composite only; no AI redraw or colour/body alteration'),indent=2)+'\n');return im
 im=Image.new('RGBA',(W,H),'white')
 for i,name in enumerate(['opening-heavier.png','opening-lean.png']):
  src=Image.open(S/'sources'/name).convert('RGB').crop((0,0,1920,970));src=ImageOps.fit(src,(636,560),method=Image.Resampling.LANCZOS,centering=(.49,0));im.paste(src,(i*644,160))
 ImageDraw.Draw(im).rectangle((636,160,643,719),fill='#122E43');return im
names={'A':'Choose Water, Cut Liquid Calories','B':'Keep Muscle In The Gym','C':'Real Studio Photograph','D':'Photograph The Meal','E':'The Approved Opening Comparison'}
def build(k):
 im=picture(k);picture_path=B/f'picture-{k}.jpg';im.convert('RGB').save(picture_path,quality=98)
 mask_path=B/f'person-{k}.png';subprocess.run([str(PM),str(picture_path),str(mask_path)],check=True,capture_output=True);person=np.array(Image.open(mask_path).convert('L').resize((W,H)))>100
 tm=Image.new('L',(W,H));boxes=[]
 if k=='A':
  ImageDraw.Draw(im).rectangle((0,0,1279,199),fill='#FFD400')
  boxes+=[put(im,tm,k,'Lose Stubborn',(40,16),118,1200,'#101519',center=True),put(im,tm,k,'Love Handles',(40,107),120,1200,'#AB2119',center=True)]
 elif k=='B':
  im=fade(im,'left',130)
  boxes+=[put(im,tm,k,'Lose',(36,195),114,560,'white'),put(im,tm,k,'Stubborn',(36,303),123,560,'white'),put(im,tm,k,'Love Handles',(36,426),112,560,'#74E7F2')]
  ImageDraw.Draw(im).rectangle((38,563,555,571),fill='#74E7F2')
 elif k=='C':
  boxes+=[put(im,tm,k,'Lose Stubborn',(614,215),91,630,'white'),put(im,tm,k,'Love Handles',(614,337),98,630,'#7FE6EB')]
  ImageDraw.Draw(im).rectangle((614,440,1240,449),fill='#E7433E')
 elif k=='D':
  boxes+=[put(im,tm,k,'Lose',(747,164),88,497,'#193447'),put(im,tm,k,'Stubborn',(747,267),101,497,'#C8392D'),put(im,tm,k,'Love Handles',(747,393),91,497,'#193447')]
  ImageDraw.Draw(im).rectangle((748,500,1230,508),fill='#C8392D')
 else:
  boxes+=[put(im,tm,k,'Lose Stubborn Love Handles',(32,47),87,1216,'#162E40',center=True)]
  ImageDraw.Draw(im).rectangle((0,139,1279,147),fill='#25AEC1')
 out=O/f'RO30-thumbnail-{k}.jpg';im.convert('RGB').save(out,quality=95,subsampling=0);tm.save(B/f'text-{k}.png');text=np.array(tm)>0;overlap=int((text&person).sum());clear=float(distance_transform_edt(~person)[text].min());feed=im.convert('RGB').resize((320,180),Image.Resampling.LANCZOS);feed.save(O/f'RO30-thumbnail-{k}-feed.jpg',quality=94)
 d=dict(letter=k,name=names[k],file=out.name,sha256=sha(out),bytes=out.stat().st_size,size=[W,H],person_text_overlap_pixels=overlap,minimum_person_text_clearance_px=round(clear,2),text_boxes=boxes,pass_checks=overlap==0 and clear>=20 and out.stat().st_size<2000000);print(json.dumps(d),flush=True);return d
if __name__=='__main__':
 import sys
 keys=sys.argv[1:] or list('ABCDE');res=[build(k) for k in keys]
 if keys==list('ABCDE'):
  (B/'qc.json').write_text(json.dumps(res,indent=2)+'\n');sheet=Image.new('RGB',(1640,1590),'#0A1D30');dr=ImageDraw.Draw(sheet);f=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),28);small=ImageFont.truetype(str(SUP/'Arial.ttf'),24);dr.text((30,15),'Love Handles: Five Thumbnail Choices',font=f,fill='white')
  for i,item in enumerate(res):
   x=30+(i%2)*810;y=76+(i//2)*490;dr.text((x,y),item['letter']+'  '+names[item['letter']],font=f,fill='#FFE26A');sheet.paste(Image.open(O/item['file']).resize((770,433),Image.Resampling.LANCZOS),(x,y+40))
  dr.text((842,1120),'Pick A, B, C, D Or E.',font=f,fill='white');dr.text((842,1170),'C is your real studio photograph.',font=small,fill='#D5E7EF');dr.text((842,1220),'E reuses the approved AI opening.',font=small,fill='#D5E7EF');dr.text((842,1270),'A, B and D are new AI scenes of you.',font=small,fill='#D5E7EF');sheet.save(O/'REVIEW-five-thumbnails.jpg',quality=94)
