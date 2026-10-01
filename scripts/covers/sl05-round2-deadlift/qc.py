#!/usr/bin/env python3
"""Verify the exact 20 SL-05 R2 rendered files and literal Instagram crops."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import distance_transform_edt
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/sl05-covers-20261001/round2-deadlift'
m=json.loads((R/'manifest.json').read_text());rows=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for x in m['outputs']:
 p=Path(x['path']);im=Image.open(p);tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0
 mp=R/'rendered-masks'/x['platform']/(p.stem+'.mask.png');pm=np.array(Image.open(mp))>127
 assert tm.any() and pm.any(),p
 ys,xs=np.where(tm);tb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 overlap=int((tm&pm).sum());clearance=round(float(distance_transform_edt(~pm)[tm].min()),1)
 src=Image.open(x['source']);crop=x['source_crop'];box=x['subject_photo_box']
 warning=np.array(Image.open(p.with_name(p.stem+'.warning-mask.png')))>0
 wy,wx=np.where(warning)
 checks={'RGB_1080x1920':im.mode=='RGB' and im.size==(1080,1920),'headline_two_lines':len(x['copy']['headline'])==2,'text_person_clearance_40px':overlap==0 and clearance>=40,'text_platform_safe':tb[1]>=(240 if x['platform']=='instagram' else 52) and tb[3]<=1620,'source_hair_retained':crop[1]<x['source_hair_y'],'entire_source_width_and_lower_action_retained':crop[0]==0 and crop[2:]==[src.width,src.height],'photo_inside_platform_safe_area':box[3]<=(1680 if x['platform']=='instagram' else 1840),'warning_below_face':int(wy.min())>x['rendered_hair_y']+220*x['scale'],'source_hash_matches':sha(x['source'])==x['source_sha256'],'export_hash_matches':sha(p)==x['sha256']}
 if x['platform']=='instagram':
  grid=Image.open(R/'grid-crops'/p.name);checks['literal_grid_crop']=grid.size==(1080,1440) and np.array_equal(np.array(grid),np.array(im)[240:1680])
 assert all(checks.values()),(p,checks,clearance)
 rows.append(dict(short=x['short'],variant=x['variant'],platform=x['platform'],path=str(p),sha256=x['sha256'],text_bbox=tb,person_mask_path=str(mp),person_mask_sha256=sha(mp),minimum_text_person_clearance_px=clearance,text_person_overlap_pixels=overlap,warning_top_y=int(wy.min()),checks=checks))
assert len(rows)==20 and len({(x['short'],x['variant'],x['platform']) for x in rows})==20
q={'status':'PASS','scope':'Five new generated powerlifter images, two designs each, separate Instagram and YouTube layouts. Twenty review PNGs. Awaiting five picks; no finals, uploads or scheduling.','method':'Apple Vision accurate person segmentation on every exact rendered file, threshold127; separate text and warning layers. Minimum40px text clearance. Literal Instagram crop (0,240,1080,1680). Source crop preserves full width and everything below the head. Warning top is below hair plus220 scaled source pixels; faces and bars were also visually inspected.','visual_checks':['All five paired sheets and both platform sheets inspected','Straining faces, hands and heavily loaded bars read as deadlifting','Hair and faces visible above warning marks','Bar and plates remain visible below warning marks','No invented visible abs on clothed lifters','Headline readable in phone-size previews and literal Instagram crops','Approved copy unchanged; Dan explicitly requested this replacement visual direction'],'generation':m['generation'],'outputs':rows}
(R/'quality-checks.json').write_text(json.dumps(q,indent=2)+'\n')
print('PASS:20 covers. Minimum text/person clearance:',min(x['minimum_text_person_clearance_px'] for x in rows),'px')
