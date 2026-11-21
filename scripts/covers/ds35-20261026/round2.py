#!/usr/bin/env python3
"""Three user-directed beach scenes, adapting DS35's existing cover builder."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
from scipy.ndimage import maximum_filter
from build import ROOT, OUT as BASE, W, H, SUP, PM, sha, fit, COPY

OUT=BASE/'round2'

def title(im, mask, k, platform):
    y=260 if platform=='instagram' else 90
    d=ImageDraw.Draw(im);m=ImageDraw.Draw(mask);bounds=[]
    if k=='1':
        d.rectangle((0,y-20,1080,y+320),fill='#FFD900')
        spec='A';sizes=[190,190];steps=[0,150];colors=['#0C1721','#B81E22']
    elif k=='2':
        spec='B';sizes=[150,166];steps=[0,155];colors=['#FFF8E7','#FFD486']
        a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[4,17,35]
        for row in range(660):a[row,:,3]=int(225*max(0,1-row/660))
        im.alpha_composite(Image.fromarray(a));d=ImageDraw.Draw(im)
        d.line((62,y-24,1018,y-24),fill='#FFD486',width=6)
    else:
        spec='D';sizes=[166,166];steps=[0,145];colors=['#122C4B','#144F89']
        d.polygon([(28,y-22),(1052,y-22),(1052,y+304),(28,y+330)],fill='#FFF5DD')
        d.line((190,y+285,890,y+285),fill='#C72C2C',width=10)
    for i,word in enumerate(COPY):
        f=fit(spec,word,sizes[i],940);yy=y+steps[i];stroke=4 if k=='2' else 0
        d.text((W//2,yy),word,anchor='mt',font=f,fill=colors[i],stroke_width=stroke,stroke_fill='#06152B')
        m.text((W//2,yy),word,anchor='mt',font=f,fill=255,stroke_width=stroke)
        b=f.getbbox(word,anchor='mt');bounds.append([W//2+b[0]-stroke,yy+b[1]-stroke,W//2+b[2]+stroke,yy+b[3]+stroke])
    return bounds

def build():
    rows=[];checks=[];face_tiles=[]
    for k in '123':
        for platform in ['instagram','youtube']:
            folder=OUT/platform;folder.mkdir(exist_ok=True)
            source=OUT/'sources'/f'{k}.png'
            im=ImageOps.fit(Image.open(source).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
            if platform=='youtube':im=im.crop((0,145,W,H)).resize((W,H),Image.Resampling.LANCZOS)
            pic=folder/f'cover-{k}.picture.png';im.convert('RGB').save(pic)
            tm=Image.new('L',(W,H));bounds=title(im,tm,k,platform)
            for b in bounds:
                assert 30<=b[0]<b[2]<=1050
                assert (240 if platform=='instagram' else 60)<=b[1]<b[3]<=1620
            path=folder/f'cover-{k}.png';im.convert('RGB').save(path);tm.save(folder/f'cover-{k}.text-mask.png')
            jpg=path.with_suffix('.jpg');im.convert('RGB').save(jpg,quality=92)
            pm=folder/f'cover-{k}.person-mask.png'
            faces=json.loads(subprocess.run([str(PM),str(pic),str(pm)],capture_output=True,text=True,check=True).stdout)['faces']
            people=np.asarray(Image.open(pm))>127;text=maximum_filter(np.asarray(tm),size=31)>0
            collisions=int((people&text).sum());person_top=int(np.where(people.any(axis=1))[0].min())
            panel_bottom=(y:=260 if platform=='instagram' else 90)+({'1':320,'2':300,'3':330}[k])
            # Panel clearance is checked independently of glyph clearance.
            panel_clear=(person_top>=panel_bottom+15) if k in '13' else True
            checked=dict(choice=k,platform=platform,sha256=sha(path),text_collision_pixels_with_15px_margin=collisions,person_top_y=person_top,panel_bottom=panel_bottom,panel_clear=panel_clear,detected_faces=faces,jpeg_bytes=jpg.stat().st_size,passed=collisions==0 and panel_clear and jpg.stat().st_size<2000000)
            checks.append(checked)
            if platform=='youtube':
                for i,(x0,y0,x1,y1) in enumerate(faces):
                    pad=round((x1-x0)*.35);face=im.crop((max(0,x0-pad),max(0,y0-pad),min(W,x1+pad),min(H,y1+pad)));face.thumbnail((200,220));face_tiles.append((f'{k} / person {i+1}',face.convert('RGB')))
            rows.append(dict(choice=k,platform=platform,path=str(path),sha256=sha(path),jpeg_path=str(jpg),jpeg_sha256=sha(jpg),jpeg_bytes=jpg.stat().st_size,source=str(source),source_sha256=sha(source),text_bounds=bounds))
    (OUT/'manifest.json').write_text(json.dumps({'status':'awaiting Dan pick','copy':COPY,'outputs':rows},indent=2))
    (OUT/'checks.json').write_text(json.dumps({'all_passed':all(x['passed'] for x in checks),'checks':checks},indent=2))
    sheet=Image.new('RGB',(3*420,2*772),'#111C2A');d=ImageDraw.Draw(sheet);label=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),28)
    for r in rows:
        x=(int(r['choice'])-1)*420;y=0 if r['platform']=='instagram' else 772
        d.text((x+15,y+12),r['choice']+' / '+r['platform'].title(),fill='white',font=label)
        cover=Image.open(r['path']);cover.thumbnail((390,700));sheet.paste(cover,(x+15,y+58))
    sheet.save(OUT/'three-new-cover-choices.jpg',quality=95)
    fs=Image.new('RGB',(220*len(face_tiles),270),'#223047');d=ImageDraw.Draw(fs)
    for i,(label,face) in enumerate(face_tiles):d.text((i*220+8,8),label,fill='white');fs.paste(face,(i*220+8,35))
    fs.save(OUT/'face-and-expression-check.jpg',quality=95)
    print(json.dumps({'built':6,'all_checks_passed':all(x['passed'] for x in checks),'checks':checks},indent=2))

if __name__=='__main__':build()
