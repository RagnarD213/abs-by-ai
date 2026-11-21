#!/usr/bin/env python3
"""Measure the exact SL-03 review files: Apple Vision person masks vs the rendered type, plus layout checks."""
from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/sl03-covers-20261008'
m=json.loads((R/'manifest.json').read_text());rows=[];fails=[]
for x in m['outputs']:
 p=Path(x['path']);im=Image.open(p);tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0
 pm=np.array(Image.open(R/'rendered-masks'/x['platform']/(p.stem+'.mask.png')))>127
 ys,xs=np.where(tm);tb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 clearance=round(float(distance_transform_edt(~pm)[tm].min()),1) if pm.any() else 9999.0;overlap=int((tm&pm).sum())
 ig=x['platform']=='instagram';c={'RGB_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'headline_two_lines':len(x['copy']['headline'])==2,
  'text_person_clearance_40px':overlap==0 and clearance>=40,'text_safe_band':(tb[1]>=236 and tb[3]<=1620) if ig else (tb[1]>=48 and tb[3]<=1700)}
 if ig:
  g=np.array(Image.open(R/'grid-crops'/p.name));c['literal_grid_crop']=g.shape==(1440,1080,3) and np.array_equal(g,np.array(im)[240:1680])
 if x['variant']=='A':
  c['hair_not_cropped']=x['source_crop'][1]<x['source_head_y'];c['abs_inside_safe']=x['rendered_abs_bottom']<=(1645 if ig else 1805)
 if x['variant']=='C':
  mp=Path(x['source']).parent/'masks'/(Path(x['source']).stem+'.mask.png');sm=np.array(Image.open(mp))>127;top=np.where(sm[x['crop'][1]:].any(1))[0].min();c['hair_clear_of_crop_top_30px']=int(top)>=30;x['person_top_below_crop']=int(top)
 if not all(c.values()):fails.append((p.name,{k:v for k,v in c.items() if not v},clearance))
 rows.append(dict(short=x['short'],variant=x['variant'],platform=x['platform'],path=str(p),sha256=x['sha256'],text_bbox=tb,min_text_person_clearance_px=clearance,checks=c))
yt=[Path(x['path']) for x in m['outputs'] if x['platform']=='youtube']
jpg_ok=[]
for p in yt:
 import io;b=io.BytesIO();Image.open(p).convert('RGB').save(b,'JPEG',quality=92);jpg_ok.append(b.tell()<2_000_000)
print('YouTube JPEG <2MB at q92:',all(jpg_ok))
qc={'status':'PASS' if not fails and all(jpg_ok) else 'FAIL','files':len(rows),'fails':fails,'rows':rows}
(R/'quality-checks.json').write_text(json.dumps(qc,indent=1,default=str)+'\n');print(qc['status'],len(rows),'files');[print(f) for f in fails]
