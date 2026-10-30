from pathlib import Path
import json,hashlib,subprocess,importlib.util
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont
from scipy.ndimage import distance_transform_edt
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');O=P/'social media graphics/youtube/thumbnails/The Fastest Way To Lose Stubborn Love Handles';B=O/'_build-2026-10-30-r2';W,H=1280,720
spec=importlib.util.spec_from_file_location('base',P/'scripts/covers/ro30-20261029/build.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
PM=Path.home()/'.cache/absbyai/personmask/personmask';SUP=Path('/System/Library/Fonts/Supplemental')
names={'1':'Poolside: The Fat-Gain Version','2':'Gym: The Fat-Gain Version','3':'Studio: The Fat-Gain Version'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build(k):
 src=B/'assets'/f'AI-Dan-fat-gain-{k}.png';assert src.exists(),src
 im=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA');pic=B/f'picture-{k}.jpg';im.convert('RGB').save(pic,quality=98)
 mp=B/f'person-{k}.png';subprocess.run([str(PM),str(pic),str(mp)],check=True,capture_output=True);person=np.array(Image.open(mp).convert('L').resize((W,H)))>100
 tm=Image.new('L',(W,H));boxes=[]
 if k=='1':
  ImageDraw.Draw(im).rectangle((0,0,1279,189),fill='#FFD400')
  boxes+=[base.put(im,tm,'A','Lose Stubborn',(40,16),110,1200,'#101519',center=True),base.put(im,tm,'A','Love Handles',(40,103),110,1200,'#AB2119',center=True)]
 elif k=='2':
  im=base.fade(im,'right',100)
  for txt,y,fs,col in [('Lose',178,120,'white'),('Stubborn',297,121,'white'),('Love Handles',432,109,'#78E2F1')]:boxes.append(base.put(im,tm,'B',txt,(720,y),fs,525,col))
  ImageDraw.Draw(im).rectangle((720,563,1237,571),fill='#78E2F1')
 else:
  for txt,y,fs,col in [('Lose',175,100,'#193447'),('Stubborn',293,116,'#B5332A'),('Love Handles',434,95,'#193447')]:boxes.append(base.put(im,tm,'D',txt,(38,y),fs,545,col))
  ImageDraw.Draw(im).rectangle((40,543,564,551),fill='#B5332A')
 out=O/f'RO30-thumbnail-R2-{k}.jpg';im.convert('RGB').save(out,quality=95,subsampling=0);tm.save(B/f'text-{k}.png');text=np.array(tm)>0;overlap=int((text&person).sum());clear=float(distance_transform_edt(~person)[text].min());im.convert('RGB').resize((320,180),Image.Resampling.LANCZOS).save(O/f'RO30-thumbnail-R2-{k}-feed.jpg',quality=95)
 result=dict(design=k,name=names[k],file=out.name,sha256=sha(out),bytes=out.stat().st_size,size=[W,H],text='Lose Stubborn Love Handles',person_text_overlap_pixels=overlap,minimum_person_text_clearance_px=round(clear,2),text_boxes=boxes,pass_checks=overlap==0 and clear>=20 and out.stat().st_size<2000000);print(json.dumps(result),flush=True);return result
if __name__=='__main__':
 import sys
 keys=sys.argv[1:] or ['1','2','3'];res=[build(k) for k in keys]
 if keys==['1','2','3']:
  (B/'qc.json').write_text(json.dumps(res,indent=2)+'\n');sheet=Image.new('RGB',(1320,2410),'#0B2133');d=ImageDraw.Draw(sheet);f=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),30);d.text((25,18),'Love Handles: Three New Designs',font=f,fill='white')
  for i,r in enumerate(res):
   y=72+i*775;d.text((25,y),r['design']+'  '+r['name'],font=f,fill='#FFE068');sheet.paste(Image.open(O/r['file']),(20,y+42))
  sheet.save(O/'REVIEW-R2-three-fat-gain-designs.jpg',quality=94)
  feed=Image.new('RGB',(960,212),'#11263A');d=ImageDraw.Draw(feed)
  for i,k in enumerate(keys):d.text((i*320+4,2),k,fill='white');feed.paste(Image.open(O/f'RO30-thumbnail-R2-{k}-feed.jpg'),(i*320,25))
  feed.save(O/'REVIEW-R2-phone-size.jpg',quality=95)
