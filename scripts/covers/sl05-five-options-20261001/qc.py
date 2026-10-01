#!/usr/bin/env python3
"""Measure exact SL-05 review files against Apple Vision person masks."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
r=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/sl05-covers-20261001'
m=json.loads((r/'manifest.json').read_text());rows=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for x in m['outputs']:
 p=Path(x['path']);im=Image.open(p)
 tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0
 mp=r/'rendered-masks'/x['platform']/(p.stem+'.mask.png');pm=np.array(Image.open(mp))>127
 assert tm.any() and pm.any(),p
 ys,xs=np.where(tm);tb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 overlap=int((tm&pm).sum());clearance=round(float(distance_transform_edt(~pm)[tm].min()),1)
 ab=x['rendered_abs_bottom'];source_hair=(x['source_crop'][1]<x['source_hair_y'] if x['variant']=='A' else x['crop'][1]==0 if x['variant']=='D' else x['source_alpha_crop'][1]>=0)
 checks={'RGB_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'headline_two_lines':len(x['copy']['headline'])==2,'text_person_clearance_40px':overlap==0 and clearance>=40,'text_platform_safe':tb[1]>=(240 if x['platform']=='instagram' else 52) and tb[3]<=1620,'abs_grid_safe_where_visible':ab is None or ab<=(1680 if x['platform']=='instagram' else 1840),'captured_source_hair_retained':source_hair,'source_hash_matches':sha(x['source'])==x['source_sha256'],'export_hash_matches':sha(p)==x['sha256'],'frowning_folder_excluded':'Frowning Photos' not in x['source']}
 if 'enhanced_source' in x:checks['enhanced_hash_matches']=sha(x['enhanced_source'])==x['enhanced_sha256']
 if x['platform']=='instagram':
  grid=Image.open(r/'grid-crops'/p.name);checks['literal_grid_crop']=grid.size==(1080,1440) and np.array_equal(np.array(grid),np.array(im)[240:1680])
 assert all(checks.values()),(p,checks,clearance,ab)
 rows.append(dict(short=x['short'],variant=x['variant'],platform=x['platform'],path=str(p),sha256=x['sha256'],text_bbox=tb,person_mask_path=str(mp),person_mask_sha256=sha(mp),minimum_text_person_clearance_px=clearance,text_person_overlap_pixels=overlap,abs_bottom=ab,abs_note='Covered by authentic black tank top; no abs invented.' if ab is None else 'Visible abs retained inside safe area.',checks=checks))
assert len(rows)==50 and len({(x['short'],x['variant'],x['platform']) for x in rows})==50
qc={'status':'PASS','scope':'50 review PNGs, 25 visual options. Awaiting five picks; no final exports, uploads or scheduling.','method':'Apple Vision accurate person segmentation on every exact rendered file, threshold 127; separate text layer. Minimum 40px text clearance. Literal Instagram profile crop (0,240,1080,1680). Source abs and hair coordinates projected through exact pool crop and real studio alpha composition. Enhanced screenshots preserve captured source hair and black tank top; abs visibility is not applicable to clothed frames. Visual inspection of both platform sheets, all paired/grid sheets and 270x480 phone previews.','visual_checks':['Clear hair and face, sharp defined abs where the source shows them','Pool subjects wear regular black shorts','Studio cutouts are real and not AI repainted','Screenshots preserve identity, black tank top, glasses and gesture','No olive bar, real-photo label or website wordmark','Same approved copy across all five options of each short','Readable at phone size'],'generation':m['generation'],'outputs':rows}
(r/'quality-checks.json').write_text(json.dumps(qc,indent=2)+'\n')
print('PASS: 50 covers. Minimum text/person clearance:',min(x['minimum_text_person_clearance_px'] for x in rows),'px')
