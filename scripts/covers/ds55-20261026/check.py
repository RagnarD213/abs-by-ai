#!/usr/bin/env python3
"""Measure rendered cover clearance, and prepare actual faces for inspection."""
from pathlib import Path
import json, subprocess, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from scipy.ndimage import maximum_filter
from build import OUT, PM

manifest=json.loads((OUT/'manifest.json').read_text())
report=[]; faces_for_sheet=[]
for r in manifest['outputs']:
    p=Path(r['path']);stem=p.stem
    pic=p.with_name(stem+'.picture.png');mask=p.with_name(stem+'.person-mask.png')
    result=subprocess.run([str(PM),str(pic),str(mask)],capture_output=True,text=True,check=True)
    faces=json.loads(result.stdout)['faces']
    person=np.array(Image.open(mask).convert('L'))>127
    text=maximum_filter(np.array(Image.open(p.with_name(stem+'.text-mask.png'))),size=31)>0
    n=int((person & text).sum())
    top=int(np.where(person.any(axis=1))[0].min())
    im=Image.open(p)
    rr={'letter':r['letter'],'platform':r['platform'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':list(im.size),'mode':im.mode,'text_person_collision_pixels_including_15px_margin':n,'person_top_y':top,'text_bounds':r['text_bounds'],'faces':faces,'passed':n==0 and im.size==(1080,1920) and im.mode=='RGB'}
    if r['platform']=='youtube':
        jp=p.with_suffix('.jpg');rr['jpeg_bytes']=jp.stat().st_size;rr['passed'] &= jp.stat().st_size<2000000
        for i,b in enumerate(faces):
            x0,y0,x1,y1=b;pad=round((x1-x0)*.35);b=(max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad))
            face=im.crop(b);face.thumbnail((220,260));faces_for_sheet.append((r['letter']+f' face {i+1}',face))
    report.append(rr)
sheet=Image.new('RGB',(240*(len(faces_for_sheet)+1),320),'#263142');d=ImageDraw.Draw(sheet)
ref=Image.open(OUT/'sources/identity-reference.jpg');ref=ref.crop((465,100,830,480));ref.thumbnail((220,260));sheet.paste(ref,(10,40));d.text((10,10),'Real identity reference',fill='white')
for i,(label,face) in enumerate(faces_for_sheet,1):sheet.paste(face,(i*240+10,40));d.text((i*240+10,10),label,fill='white')
sheet.save(OUT/'face-check.jpg',quality=95)
(OUT/'cover-checks.json').write_text(json.dumps({'all_automated_checks_passed':all(x['passed'] for x in report),'checks':report,'visual_inspection_required':True},indent=2))
print(json.dumps({'all_passed':all(x['passed'] for x in report),'checks':[{'letter':x['letter'],'platform':x['platform'],'collision_pixels':x['text_person_collision_pixels_including_15px_margin'],'passed':x['passed']} for x in report]},indent=2))
