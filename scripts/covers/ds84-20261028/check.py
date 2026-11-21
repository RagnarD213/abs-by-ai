#!/usr/bin/env python3
"""Check exact rendered covers and prepare faces and phone/grid previews for visual review."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageOps
from build import OUT,ROOT,PM,W,H
R=OUT/'ds84';m=json.loads((R/'manifest.json').read_text());rows=[];faces_out=[]
for row in m['outputs']:
 p=ROOT/row['path'];pic=p.with_name(p.stem+'.picture.png');mask=p.with_name(p.stem+'.person-mask.png')
 r=subprocess.run([str(PM),str(pic),str(mask)],capture_output=True,text=True,check=True);data=json.loads(r.stdout);faces=data['faces']
 tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0
 im=Image.open(p);person=np.array(Image.open(mask))>127;face_collisions=[]
 for f in faces:
  x0,y0,x1,y1=map(int,f);fw=x1-x0;fh=y1-y0
  # Expand the detected face to include hair and a margin.
  box=(max(0,x0-fw//4),max(0,y0-fh//2),min(W,x1+fw//4),min(H,y1+fh//5))
  a,b,c,d=box;face_collisions.append(int(tm[b:d,a:c].sum()))
  if row['platform']=='youtube':
   crop=ImageOps.contain(im.crop(box),(220,250));faces_out.append((row['letter'],crop))
 bounds=row['text_bounds'];miny=240 if row['platform']=='instagram' else 50;maxy=1680 if row['platform']=='instagram' else 1850
 safe=all(25<=b[0]<b[2]<=W-25 and miny<=b[1]<b[3]<=maxy for b in bounds)
 actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==row['sha256']
 d=dict(letter=row['letter'],platform=row['platform'],sha256=actual,size=list(im.size),mode=im.mode,text_bounds_safe=safe,detected_faces=faces,text_on_expanded_face_pixels=face_collisions,person_top=int(np.where(person.any(axis=1))[0].min()),text_person_pixels=int((person&tm).sum()))
 d['passed']=safe and im.size==(1080,1920) and im.mode=='RGB' and len(faces)==1 and not any(face_collisions)
 if row['platform']=='youtube':
  jp=p.with_suffix('.jpg');d['jpeg_bytes']=jp.stat().st_size;d['passed'] &= d['jpeg_bytes']<2_000_000
 ph=R/'phone'/row['platform'];ph.mkdir(parents=True,exist_ok=True);im.resize((270,480),Image.Resampling.LANCZOS).save(ph/p.with_suffix('.jpg').name,quality=95)
 gr=R/'grid';gr.mkdir(exist_ok=True)
 if row['platform']=='instagram':im.crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS).save(gr/f"{row['letter']}.jpg",quality=95)
 rows.append(d)
sheet=Image.new('RGB',(240*6,310),'#253044');dr=ImageDraw.Draw(sheet)
ref=Image.open(OUT/'sources/identity-reference.jpg');ref=ref.crop((465,100,830,480));ref.thumbnail((220,250));sheet.paste(ref,(10,40));dr.text((10,10),'Real identity reference',fill='white')
for i,(letter,face) in enumerate(faces_out,1):sheet.paste(face,(i*240+10,40));dr.text((i*240+10,10),letter,fill='white')
sheet.save(R/'face-check.jpg',quality=95)
report=dict(all_automated_checks_passed=all(r['passed'] for r in rows),checks=rows,visual_inspection_required=True)
(R/'cover-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
