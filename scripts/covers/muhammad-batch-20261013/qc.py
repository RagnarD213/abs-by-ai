#!/usr/bin/env python3
"""Measure the exact review files: Apple Vision person masks against the rendered type, plus layout and size checks.
Run personmask on every rendered PNG first (rendered-masks/<platform>/)."""
from pathlib import Path
import json,io,numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/muhammad-batch-20261013'
m=json.loads((R/'manifest.json').read_text());rows=[];fails=[]
for x in m['outputs']:
 p=Path(x['path']);im=Image.open(p);tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0
 mp=R/'rendered-masks'/x['platform']/(p.stem+'.mask.png');pm=np.array(Image.open(mp).convert('L'))>127 if mp.exists() else np.zeros((1920,1080),bool)
 ys,xs=np.where(tm);tb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 clearance=round(float(distance_transform_edt(~pm)[tm].min()),1) if pm.any() else 9999.0;overlap=int((tm&pm).sum())
 ig=x['platform']=='instagram';b=io.BytesIO();im.convert('RGB').save(b,'JPEG',quality=92)
 c={'RGB_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'headline_two_lines':len(x['copy']['headline'])==2,'mask_exists':mp.exists(),
  'text_clear_of_person_25px':overlap==0 and clearance>=25,'text_safe_band':(tb[1]>=236 and tb[3]<=1620) if ig else (tb[1]>=48 and tb[3]<=1740),'jpeg_under_2MB':b.tell()<2_000_000}
 if x['variant']=='A':c['hair_not_cropped']=x['source_crop'][1]<x['source_head_y']
 if not all(c.values()):fails.append((p.name,x['platform'],{k:v for k,v in c.items() if not v},clearance,overlap))
 rows.append(dict(short=x['short'],variant=x['variant'],platform=x['platform'],path=str(p),text_bbox=tb,min_text_person_clearance_px=clearance,checks=c))
qc={'status':'PASS' if not fails else 'FAIL','files':len(rows),'fails':fails,'rows':rows}
(R/'quality-checks.json').write_text(json.dumps(qc,indent=1,default=str)+'\n');print(qc['status'],len(rows),'files');[print(f) for f in fails]
