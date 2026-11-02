"""Check final cover dimensions, text safety and face/hair clearance."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
import json,hashlib,subprocess
import numpy as np
from build import ROOT,OUT,W,H

PM=Path.home()/'.cache/absbyai/personmask/personmask'
rows=[];faces=[]
manifest=json.loads((OUT/'manifest.json').read_text())
assert len({x['source_sha256'] for x in manifest['outputs']})==4
for row in manifest['outputs']:
    p=Path(row['path']);im=Image.open(p);k=row['design'];pf=row['platform'];m=p.with_name(p.stem+'-person-mask.png')
    run=subprocess.run([str(PM),str(p),str(m)],capture_output=True,text=True,check=True)
    found=json.loads(run.stdout)['faces'];tm=np.array(Image.open(p.with_name(p.stem+'-text-mask.png')))>0
    collisions=[]
    for f in found:
        x0,y0,x1,y1=map(int,f);fw=x1-x0;fh=y1-y0
        a,b,c,d=max(0,x0-fw//4),max(0,y0-fh//2),min(W,x1+fw//4),min(H,y1+fh//5)
        collisions.append(int(tm[b:d,a:c].sum()))
        if pf=='youtube':faces.append((k,ImageOps.contain(im.crop((a,b,c,d)),(260,250))))
    safe=all(25<=b[0]<b[2]<=W-25 and (240 if pf=='instagram' else 50)<=b[1]<b[3]<=(1680 if pf=='instagram' else 1850) for b in row['text_bounds'])
    good=im.size==(W,H) and im.mode=='RGB' and safe and len(found)==1 and not any(collisions)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
    rows.append(dict(design=k,platform=pf,passed=good,faces=found,face_hair_text_pixels=collisions,text_safe=safe,jpeg_bytes=p.with_suffix('.jpg').stat().st_size))
sheet=Image.new('RGB',(4*280,300),'#142532');draw=ImageDraw.Draw(sheet)
for i,(k,im) in enumerate(faces):sheet.paste(im,(i*280+10,32));draw.text((i*280+10,8),k,fill='white')
sheet.save(OUT/'face-check.jpg',quality=96)
grid=Image.new('RGB',(4*270,390),'#142532');draw=ImageDraw.Draw(grid)
for i in range(1,5):grid.paste(Image.open(OUT/'review'/f'R2-{i}-grid.jpg'),((i-1)*270,30));draw.text(((i-1)*270+8,8),str(i),fill='white')
grid.save(OUT/'grid-check.jpg',quality=96)
(OUT/'checks.json').write_text(json.dumps({'all_passed':all(r['passed'] for r in rows),'four_distinct_real_sources':True,'image_generation_used':False,'checks':rows,'visual_review_required':True},indent=2))
print('Real-photo checks:',sum(x['passed'] for x in rows),'of',len(rows))
