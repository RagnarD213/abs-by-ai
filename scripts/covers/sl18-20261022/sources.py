#!/usr/bin/env python3
"""Pool photo person boxes (Apple Vision, personmask) and the real reference photos for the C images. Writes sources/."""
import json,os,subprocess,tempfile
from PIL import Image
import numpy as np
from root import R,PH
PM=os.path.expanduser('~/.cache/absbyai/personmask/personmask')
POOL=['photo-71','photo-289']
REFS={'s1':'studio-gray-30','s2':'studio-blue-137'}
src=R/'sources';src.mkdir(parents=True,exist_ok=True);(src/'masks').mkdir(exist_ok=True)
boxes={}
for s in POOL:
 im=Image.open(PH/f'{s}_FINAL_PRIMARY.jpg').convert('RGB');w,h=im.size;sm=im.resize((w//3,h//3))
 with tempfile.TemporaryDirectory() as t:
  a=os.path.join(t,'i.png');sm.save(a);mp=src/'masks'/f'{s}.png'
  faces=json.loads(subprocess.run([PM,a,str(mp)],capture_output=True,text=True,check=True).stdout)['faces']
 m=np.array(Image.open(mp).convert('L'))>127;ys,xs=np.where(m);sw,sh=sm.size
 boxes[s]=dict(size=[w,h],bbox=[round(xs.min()/sw,4),round(xs.max()/sw,4),round(ys.min()/sh,4),round(ys.max()/sh,4)],
  faces=[[round(f[0]/sw,4),round(f[1]/sh,4),round(f[2]/sw,4),round(f[3]/sh,4)] for f in faces])
 print(s,boxes[s])
(src/'pool_boxes.json').write_text(json.dumps(boxes,indent=1))
refs={}
for k,s in REFS.items():
 im=Image.open(PH/f'{s}_FINAL_PRIMARY.jpg').convert('RGB');im.thumbnail((1400,1400));p=src/f'ref-{k}-{s}.jpg';im.save(p,quality=92);refs[k]=str(p)
(src/'refs.json').write_text(json.dumps(refs,indent=1));print(refs)
