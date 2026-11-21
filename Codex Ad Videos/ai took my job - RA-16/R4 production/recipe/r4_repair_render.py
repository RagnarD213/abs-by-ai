"""Repair source-hair measurements, rejecting disconnected background silhouettes."""
import importlib.util,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import mediapipe as mp
P=Path(__file__).with_name('r4_render.py');sp=importlib.util.spec_from_file_location('r4',P);B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
B.buildcap.wait('RA16 R4 repair source hair measurements')
model=mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)
def connected_top(mask,v,y0):
 rows=(mask[:,v['b0']:v['b1']]>.65).mean(1)>=.20
 face=min(len(rows)-1,round(v['fore']/4)-y0)
 if not rows[face]:return None
 k=face
 while k>0 and rows[k-1]:k-=1
 if k==0:return None
 return (k+y0)*4
report=[]
for s in B.SEGS:
 d=B.O/'measure'/f"{s['id']}-{s['n0']}";vals=json.load(open(d/'measure.json'))
 for v in vals:
  ar=np.array(Image.open(v['head_crop']).convert('RGB'))
  y0=max(0,int((v['fore']-1.1*v['face_h'])/4))
  tight=ar[y0:];m=model.process(tight).segmentation_mask
  vision=np.array(Image.open(d/'masks'/(Path(v['head_crop']).stem+'.mask.png')).convert('L'))/255
  v['old_unconstrained_hair_mp']=v.get('old_unconstrained_hair_mp',v['hair_mp']);v['old_unconstrained_hair_vision']=v.get('old_unconstrained_hair_vision',v['hair_vision'])
  v['hair_mp']=connected_top(m,v,y0);v['hair_vision']=connected_top(vision[y0:],v,y0)
  assert v['hair_vision'] is not None,('Vision hair needs manual measurement',v['g'])
  for key in ['hair_mp','hair_vision']:
   if v[key] is not None:assert 0 <= v['fore']-v[key] <=1.1*v['face_h'],(v['g'],key,v[key],v['fore'])
  report.append(dict(piece=s['id'],g=v['g'],hair_mp=v['hair_mp'],hair_vision=v['hair_vision'],old_mp=v['old_unconstrained_hair_mp']))
 B.write(d/'measure.json',vals)
model.close();B.write(B.O/'evidence/hair-measurement-repair.json',report)
# All presenter plates used the invalid y geometry. Preserve those rejected candidates, rebuild safely.
reject=B.O/'rejected-framing-candidate';reject.mkdir(exist_ok=True)
for folder in ['plates','masters','review']:
 src=B.O/folder;dst=reject/folder
 if not dst.exists():src.rename(dst);src.mkdir()
B.measure();B.render()
B.write(B.O/'BUILD_STATE.json',{'status':'complete-candidates-awaiting-QC','repair':'Disconnected tree mask removed; native source hair measurements corrected; approved crop windows retained.'})
print('REPAIRED R4 CANDIDATES READY',flush=True)
