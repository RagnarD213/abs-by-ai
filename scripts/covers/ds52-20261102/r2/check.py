#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'Short-form video content/covers/review/ds52-zepbound-free-20261102/r2'
m=json.loads((OUT/'manifest.json').read_text());PM=Path.home()/'.cache/absbyai/personmask/personmask';checks=[]
for row in m['outputs']:
 p=ROOT/row['path'];im=Image.open(p).convert('RGB');mask=p.with_name(p.stem+'-person.png')
 result=subprocess.run([str(PM),str(p),str(mask)],check=True,capture_output=True,text=True);faces=json.loads(result.stdout)['faces']
 tm=np.array(Image.open(p.with_name(p.stem+'-text-mask.png')))>0;counts=[];boxes=[]
 for b in faces:
  x0,y0,x1,y1=map(int,b);fw=x1-x0;fh=y1-y0
  bb=[max(0,x0-fw//5),max(0,y0-fh//2),min(1080,x1+fw//5),min(1920,y1+fh//6)];boxes.append(bb)
  a,b,c,d=bb;counts.append(int(tm[b:d,a:c].sum()))
 check={'design':row['design'],'platform':row['platform'],'dimensions':list(im.size),'faces':faces,'hair_expanded_boxes':boxes,'text_on_face_hair_pixels':counts,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'jpeg_bytes':p.with_suffix('.jpg').stat().st_size}
 check['pass']=len(faces)==1 and not any(counts) and im.size==(1080,1920) and check['sha256']==row['sha256'] and check['jpeg_bytes']<2_000_000
 checks.append(check)
report={'all_exact_file_checks_pass':all(x['pass'] for x in checks),'checks':checks,'source_image_sha256':m['source_sha256'],'source_unchanged':hashlib.sha256((ROOT/m['source_image']).read_bytes()).hexdigest()==m['source_sha256'],'no_generation_calls':True,'visual_review_required':True}
(OUT/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
sheet=Image.new('RGB',(1080,420),'#141C27');d=ImageDraw.Draw(sheet)
for n in range(1,5):
 im=Image.open(OUT/f'Design-{n}-profile.jpg');im.thumbnail((250,370));sheet.paste(im,((n-1)*270+10,40));d.text(((n-1)*270+10,12),str(n),fill='white')
sheet.save(OUT/'profile-crops.jpg',quality=95)
