#!/usr/bin/env python3
"""Check the exact five-option exports against Vision masks and source provenance."""
from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
from scipy.ndimage import distance_transform_edt
r=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/sl04-covers-20260930/round2-five-options';m=json.loads((r/'manifest.json').read_text());previous=json.loads((r.parent/'quality-checks.json').read_text());rows=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for x in m['outputs']:
 p=Path(x['path']);im=Image.open(p);tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0;mp=r/'rendered-masks'/x['platform']/(p.stem+'.mask.png');pm=np.array(Image.open(mp))>127
 assert pm.any() and tm.any(),p
 ys,xs=np.where(tm);tb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];overlap=int((tm&pm).sum());clearance=round(float(distance_transform_edt(~pm)[tm].min()),1)
 if x['variant']=='A':
  old=next(z for z in previous['outputs'] if z['short']==x['short'] and z['variant']=='A' and z['platform']==x['platform']);abs_bottom=old['rendered_abs_region'][3];source_hair=True;assert x['sha256']==old['sha256']
 else:
  abs_bottom=x['rendered_abs_bottom'];source_hair=(x.get('source_alpha_crop',[0,0])[1]>=0 if x['variant']!='D' else x['crop'][1]==0)
 checks={'RGB_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'text_max_two_lines':len(x['copy']['headline'])<=2,'text_person_clearance_40px':overlap==0 and clearance>=40,'text_platform_safe':tb[1]>=(240 if x['platform']=='instagram' else 52) and tb[3]<=1620,'abs_bottom_grid_safe':abs_bottom<=(1680 if x['platform']=='instagram' else 1840),'source_hair_retained':source_hair,'source_hash_matches':sha(x['source'])==x['source_sha256'],'export_hash_matches':sha(p)==x['sha256'],'frowning_folder_excluded':'Frowning Photos' not in x['source']}
 assert all(checks.values()),(p,checks,clearance,abs_bottom)
 if x['platform']=='instagram':
  grid=Image.open(r/'grid-crops'/p.name);assert grid.size==(1080,1440) and np.array_equal(np.array(grid),np.array(im)[240:1680])
 rows.append(dict(short=x['short'],variant=x['variant'],platform=x['platform'],path=str(p),sha256=x['sha256'],text_bbox=tb,person_mask_path=str(mp),person_mask_sha256=sha(mp),minimum_text_person_clearance_px=clearance,text_person_overlap_pixels=overlap,abs_bottom=abs_bottom,checks=checks))
for ref in previous['reference_unchanged']:assert sha(ref['path'])==ref['unchanged_sha256']
qc={'status':'PASS','scope':'40 review PNGs, 20 visual options. No selections or final exports yet.','method':'Apple Vision accurate person segmentation on each exact rendered file, mask threshold 127, separate text layer. Minimum 40px text clearance. Literal Instagram profile crop (0,240,1080,1680). Studio source abs-bottom measurements projected through native alpha composition; screenshot source coordinates projected through exact crop. Unchanged pool images reuse prior source-region checks. Visual review at 270x480 of both platform sheets, and paired full-frame/grid sheets.','visual_checks':['Hair, face and arms retained in the source crop','Abs visible in each Instagram grid crop','Studio portraits composited without AI repainting','Authentic exercise screenshots, enhanced for clarity','No real-picture label or website wordmark','Headlines readable at phone size'],'reference_unchanged':previous['reference_unchanged'],'outputs':rows}
(r/'quality-checks.json').write_text(json.dumps(qc,indent=2)+'\n');print('PASS: 40 files. Minimum text/person clearance:',min(x['minimum_text_person_clearance_px'] for x in rows),'px')
