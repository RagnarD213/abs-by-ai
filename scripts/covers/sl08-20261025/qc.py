#!/usr/bin/env python3
"""Measure the exact review files: Apple Vision person mask + face boxes of each cover's picture layer (the rendered cover
 minus its type, saved by build.py as .picture.png, so white type is never mistaken for a person) (personmask.swift, built to
~/.cache/absbyai/personmask/personmask) against the drawn type mask, plus layout and size checks. Writes quality-checks.json."""
from pathlib import Path
import json,io,os,subprocess,numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
import sys;sys.path.insert(0,str(Path(__file__).resolve().parent));from root import R
PM=os.path.expanduser('~/.cache/absbyai/personmask/personmask')
m=json.loads((R/'manifest.json').read_text());keys=sys.argv[1:];prior=json.loads((R/'quality-checks.json').read_text()) if keys and (R/'quality-checks.json').exists() else {'rows':[]}
rows=[x for x in prior['rows'] if x['short'] not in keys] if keys else [];fails=[]
if keys:m['outputs']=[x for x in m['outputs'] if x['short'] in keys]
# Looked at by eye, with the reason. Only the body-clearance row is waived; the face/hair row still runs.
WAIVE={}
for x in m['outputs']:
 p=Path(x['path']);im=Image.open(p);tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0
 md=R/'rendered-masks'/x['platform'];md.mkdir(parents=True,exist_ok=True);mp=md/(p.stem+'.mask.png')
 faces=json.loads(subprocess.run([PM,str(p.with_name(p.stem+'.picture.png')),str(mp)],capture_output=True,text=True,check=True).stdout)['faces']
 pm=np.array(Image.open(mp).convert('L'))>127
 ys,xs=np.where(tm);tb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 clearance=round(float(distance_transform_edt(~pm)[tm].min()),1) if pm.any() else 9999.0;overlap=int((tm&pm).sum())
 face_hit=any(tm[max(0,f[1]-40):f[3],max(0,f[0]):f[2]].any() for f in faces)   # face box grown 40 px up for hair
 ig=x['platform']=='instagram';b=io.BytesIO();im.convert('RGB').save(b,'JPEG',quality=90)
 c={'RGB_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'headline_lines':len(x['copy']['headline']) in (2,3),
  'text_clear_of_person_25px':overlap==0 and clearance>=25,'text_clear_of_face_and_hair':not face_hit,
  'text_safe_band':(tb[1]>=236 and tb[3]<=1620) if ig else (tb[1]>=48 and tb[3]<=1740),'jpeg_under_2MB':b.tell()<2_000_000}
 if x['variant']=='A':c['hair_not_cropped']=x['source_crop'][1]<=x['source_head_y']
 if x['variant'] in 'ABC' or x.get('has_person'):c['person_found']=bool(pm.any()) and len(faces)>=1
 if ig and pm.any():   # abs must sit inside the 3:4 grid tile (y 240-1680): the person's mid-torso row
  yy=np.where(pm.any(axis=1))[0];c['person_inside_grid_tile']=yy.min()<1680
 if (x['short'],x['variant']) in WAIVE and not c['text_clear_of_person_25px'] and not face_hit:c['text_clear_of_person_25px']=True;c['waived']=WAIVE[(x['short'],x['variant'])]
 if not all(v for v in c.values()):fails.append((p.name,x['platform'],{k:v for k,v in c.items() if not v},clearance,overlap))
 c={key:bool(value) for key,value in c.items()}
 rows.append(dict(short=x['short'],variant=x['variant'],platform=x['platform'],path=str(p),text_bbox=tb,faces=faces,min_text_person_clearance_px=clearance,checks=c))
qc={'status':'PASS' if not fails else 'FAIL','files':len(rows),'fails':fails,'rows':rows}
(R/'quality-checks.json').write_text(json.dumps(qc,indent=1,default=str)+'\n');print(qc['status'],len(rows),'files');[print(f) for f in fails]
