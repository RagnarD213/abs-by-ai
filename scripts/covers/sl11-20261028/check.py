from pathlib import Path
import json,subprocess,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageOps,ImageFont
from build import OUT,ROOT,PM,W,H,SHORTS
allrows=[]
for key in (sys.argv[1:] or list(SHORTS)):
 r=OUT/key;m=json.loads((r/'manifest.json').read_text());rows=[];faceimages=[]
 for row in m['outputs']:
  p=ROOT/row['path'];pic=p.with_name(p.stem+'.picture.png');mp=p.with_name(p.stem+'.person-mask.png');res=subprocess.run([str(PM),str(pic),str(mp)],capture_output=True,text=True,check=True);faces=json.loads(res.stdout)['faces'];tm=np.array(Image.open(p.with_name(p.stem+'.text-mask.png')))>0;pm=np.array(Image.open(mp).convert('L'))>127;im=Image.open(p);collisions=[]
  for f in faces:
   x0,y0,x1,y1=map(int,f);fw=x1-x0;fh=y1-y0;b=(max(0,x0-fw//5),max(0,y0-fh//2),min(W,x1+fw//5),min(H,y1+fh//5));a,c,d,e=b;collisions.append(int(tm[c:e,a:d].sum()))
   if row['platform']=='youtube':faceimages.append((row['letter'],ImageOps.contain(im.crop(b),(210,250))))
  miny=240 if row['platform']=='instagram' else 50;maxy=1620 if row['platform']=='instagram' else 1850;safe=all(25<=b[0]<b[2]<=W-25 and miny<=b[1]<b[3]<=maxy for b in row['text_bounds']);actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==row['sha256'];d=dict(short=key,letter=row['letter'],platform=row['platform'],sha256=actual,size=list(im.size),mode=im.mode,text_bounds_safe=safe,faces=faces,text_on_face_and_hair_pixels=collisions,text_person_pixels=int((pm&tm).sum()),person_top=int(np.where(pm.any(axis=1))[0].min()) if pm.any() else None)
  d['passed']=safe and im.size==(1080,1920) and im.mode=='RGB' and len(faces)>=1 and not any(collisions)
  if row['platform']=='youtube':d['jpeg_bytes']=p.with_suffix('.jpg').stat().st_size;d['passed'] &= d['jpeg_bytes']<2_000_000
  ph=r/'phone'/row['platform'];ph.mkdir(parents=True,exist_ok=True);im.resize((270,480),Image.Resampling.LANCZOS).save(ph/p.with_suffix('.jpg').name,quality=95)
  gr=r/'grid';gr.mkdir(exist_ok=True)
  if row['platform']=='instagram':im.crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS).save(gr/f"{row['letter']}.jpg",quality=95)
  rows.append(d);print(key,row['letter'],row['platform'],d['passed'],d['text_person_pixels'],flush=True)
 sheet=Image.new('RGB',(230*(1+len(faceimages)),310),'#253044');dr=ImageDraw.Draw(sheet);ref=Image.open(OUT/'sources/identity-reference.jpg').crop((465,70,860,500));ref.thumbnail((210,250));sheet.paste(ref,(10,40));dr.text((10,10),'Real identity reference',fill='white')
 for i,(letter,face) in enumerate(faceimages,1):sheet.paste(face,(i*230+10,40));dr.text((i*230+10,10),letter,fill='white')
 sheet.save(r/'face-check.jpg',quality=95)
 (r/'cover-checks.json').write_text(json.dumps({'all_automated_checks_passed':all(d['passed'] for d in rows),'checks':rows,'visual_inspection_required':True},indent=2));allrows+=rows
allrows=[d for key in SHORTS if (OUT/key/'cover-checks.json').exists() for d in json.loads((OUT/key/'cover-checks.json').read_text())['checks']]
(OUT/'cover-checks.json').write_text(json.dumps({'all_automated_checks_passed':len(allrows)==30 and all(d['passed'] for d in allrows),'files':len(allrows),'checks':allrows},indent=2));print('ALL',len(allrows),all(d['passed'] for d in allrows))
