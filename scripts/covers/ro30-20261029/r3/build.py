from pathlib import Path
import json,hashlib,subprocess,importlib.util
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFilter,ImageFont
from scipy.ndimage import distance_transform_edt
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');O=P/'social media graphics/youtube/thumbnails/The Fastest Way To Lose Stubborn Love Handles';B=O/'_build-2026-10-30-r3';W,H=1280,720
spec=importlib.util.spec_from_file_location('base',P/'scripts/covers/ro30-20261029/build.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
PM=Path.home()/'.cache/absbyai/personmask/personmask';SUP=Path('/System/Library/Fonts/Supplemental');source=Image.open(O/'_build-2026-10-30-r2/assets/AI-Dan-fat-gain-2.png').convert('RGB');original=Image.open(O/'RO30-thumbnail-R2-2.jpg').convert('RGB')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
names={'1':'Lightest','2':'Middle','3':'Fullest Of These Three'}
def build(k):
 edit=Image.open(B/'assets'/f'less-fat-{k}.png').convert('RGB').resize(source.size,Image.Resampling.LANCZOS)
 mask=Image.new('L',source.size,0);d=ImageDraw.Draw(mask);sx,sy=source.width/W,source.height/H;rect=[round(x*sx) if i%2==0 else round(x*sy) for i,x in enumerate([205,275,568,680])];d.rectangle(rect,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(12*sx));mask.save(B/f'body-edit-mask-{k}.png')
 # Keep original face/hair/arms/background outside the torso edit, preventing unintended redraws.
 blended=Image.composite(edit,source,mask);im=ImageOps.fit(blended,(W,H),method=Image.Resampling.LANCZOS).convert('RGBA');pic=B/f'picture-{k}.jpg';im.convert('RGB').save(pic,quality=98)
 mp=B/f'person-{k}.png';subprocess.run([str(PM),str(pic),str(mp)],check=True,capture_output=True);person=np.array(Image.open(mp).convert('L').resize((W,H)))>100
 im=base.fade(im,'right',100);tm=Image.new('L',(W,H));boxes=[]
 for txt,y,fs,col in [('Lose',178,120,'white'),('Stubborn',297,121,'white'),('Love Handles',432,109,'#78E2F1')]:boxes.append(base.put(im,tm,'B',txt,(720,y),fs,525,col))
 ImageDraw.Draw(im).rectangle((720,563,1237,571),fill='#78E2F1')
 out=O/f'RO30-thumbnail-R3-{k}.jpg';im.convert('RGB').save(out,quality=95,subsampling=0);tm.save(B/f'text-{k}.png');a=np.array(Image.open(out).convert('RGB'));old=np.array(original);text=np.array(tm)>0;overlap=int((text&person).sum());clear=float(distance_transform_edt(~person)[text].min());rightmax=int(np.abs(a[:,704:].astype(int)-old[:,704:].astype(int)).max());facemax=int(np.abs(a[:220,:650].astype(int)-old[:220,:650].astype(int)).max())
 im.convert('RGB').resize((320,180),Image.Resampling.LANCZOS).save(O/f'RO30-thumbnail-R3-{k}-feed.jpg',quality=95)
 r=dict(variation=k,label=names[k],file=out.name,sha256=sha(out),size=[W,H],bytes=out.stat().st_size,text='Lose Stubborn Love Handles',person_text_overlap_pixels=overlap,minimum_person_text_clearance_px=round(clear,2),headline_region_max_pixel_difference_vs_R2=rightmax,face_region_max_pixel_difference_vs_R2=facemax,pass_checks=overlap==0 and clear>=20 and out.stat().st_size<2000000 and rightmax==0);print(json.dumps(r),flush=True);return r
if __name__=='__main__':
 import sys
 keys=sys.argv[1:] or ['1','2','3'];res=[build(k) for k in keys]
 if keys==['1','2','3']:
  (B/'qc.json').write_text(json.dumps(res,indent=2)+'\n');sheet=Image.new('RGB',(1320,2410),'#0B2133');d=ImageDraw.Draw(sheet);f=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),30);d.text((25,18),'Love Handles: Three Slimmer Variations',font=f,fill='white')
  for i,r in enumerate(res):
   y=72+i*775;d.text((25,y),r['variation']+'  '+r['label'],font=f,fill='#FFE068');sheet.paste(Image.open(O/r['file']),(20,y+42))
  sheet.save(O/'REVIEW-R3-three-slimmer-variations.jpg',quality=94)
  feed=Image.new('RGB',(1280,212),'#11263A');d=ImageDraw.Draw(feed)
  for i,k in enumerate(keys):d.text((i*320+4,2),k+' '+names[k],fill='white');feed.paste(Image.open(O/f'RO30-thumbnail-R3-{k}-feed.jpg'),(i*320,25))
  d.text((964,2),'Previous, reference only',fill='white');feed.paste(original.resize((320,180),Image.Resampling.LANCZOS),(960,25));feed.save(O/'REVIEW-R3-comparison-phone-size.jpg',quality=95)
