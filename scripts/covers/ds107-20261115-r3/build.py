#!/usr/bin/env python3
"""Four requested conversation covers; exact speech added locally."""
from pathlib import Path
import importlib.util,json,hashlib,sys,subprocess
from PIL import Image,ImageDraw,ImageOps
import numpy as np
P=Path(__file__).resolve().parents[3]
R=P/'Short-form video content/covers/review/ds107-20261115-r3'
sys.path.insert(0,str(P/'scripts/covers/sl08-20261025'))
s=importlib.util.spec_from_file_location('cover_helpers',P/'scripts/covers/sl08-20261025/build.py')
h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
W,H=1080,1920
PM=str(Path.home()/'.cache/absbyai/personmask/personmask')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def faces_for(im,k):
    a=Path('/tmp')/f'ds107-r3-{k}-picture.png';b=a.with_name(a.stem+'-mask.png')
    im.convert('RGB').save(a)
    det=json.loads(subprocess.check_output([PM,str(a),str(b)],text=True))
    faces=sorted(det['faces'],key=lambda b:(b[0]+b[2])/2)
    assert len(faces)==2,(k,faces)
    return faces

def headbox(face):
    x0,y0,x1,y1=face;fh=y1-y0
    return [max(0,x0-int(fh*.25)),max(0,y0-int(fh*.65)),min(W,x1+int(fh*.25)),y1]

def bubble(im,mask,box,face,lines,font_size,fill=(255,255,248),response=False):
    x0,y0,x1,y1=box;d=ImageDraw.Draw(im)
    head=headbox(face);cx=(face[0]+face[2])//2
    tip=(cx,head[1]-24);base=max(x0+90,min(x1-90,cx+(-35 if response else 40)))
    tail=[(base-40,y1-15),(base+40,y1-15),tip]
    d.polygon(tail,fill=fill,outline=(12,23,31));d.line(tail+[tail[0]],fill=(12,23,31),width=8,joint='curve')
    d.rounded_rectangle(box,radius=40,fill=fill,outline=(12,23,31),width=8)
    font=h.common(lines,h.AVENIR,font_size,x1-x0-65)
    step=round(font.size*1.10)
    height=len(lines)*step
    y=y0+(y1-y0-height)//2+5
    for i,line in enumerate(lines):
        color=(9,29,45) if response or i==0 else (166,33,30)
        h.text(im,mask,((x0+x1)//2,y+i*step),line,font,color,anchor='mt')
    return {'box':box,'tail':tail,'font_size':font.size,'text': ' '.join(lines)}

def build():
    rows=[]
    for n in range(1,5):
        k=f'Y{n}';src=R/f'source-{k}.png'
        raw=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
        raw_faces=faces_for(raw,k)
        for platform in ['instagram','youtube']:
            ig=platform=='instagram';top=250 if ig else 100
            my_box=[34,top,708,top+300];no_box=[780,top+55,1048,top+270]
            min_head=min(headbox(f)[1] for f in raw_faces)
            shift=max(0,top+355-min_head)
            col=tuple(int(x) for x in np.asarray(raw.convert('RGB'))[:30].reshape(-1,3).mean(axis=0))
            im=Image.new('RGBA',(W,H),col+(255,));im.alpha_composite(raw,(0,shift));picture=im.copy()
            faces=[[f[0],f[1]+shift,f[2],f[3]+shift] for f in raw_faces]
            tm=Image.new('L',(W,H))
            old=bubble(im,tm,my_box,faces[0],['My metabolism','slowed down.'],101)
            dan=bubble(im,tm,no_box,faces[1],['No.'],160,fill=(255,222,69),response=True)
            mask=np.asarray(tm);assert tm.getbbox()[1]>=(240 if ig else 70)
            for f in faces:
                x0,y0,x1,y1=headbox(f);assert not np.count_nonzero(mask[y0:y1,x0:x1]),(k,platform,f)
            out=R/'layouts'/k/platform;out.mkdir(parents=True,exist_ok=True)
            im.convert('RGB').save(out/'cover.png');im.convert('RGB').save(out/'cover.jpg',quality=94)
            assert (out/'cover.jpg').stat().st_size<2_000_000
            picture.convert('RGB').save(out/'picture.jpg',quality=96);tm.save(out/'text-mask.png')
            im.resize((270,480),Image.Resampling.LANCZOS).convert('RGB').save(out/'phone.jpg',quality=95)
            rows.append({'round':3,'label':k,'platform':platform,'Dan_clothing':'shirtless' if n<3 else 'tank top','source':str(src),'source_sha256':sha(src),'path':str(out/'cover.png'),'sha256':sha(out/'cover.png'),'jpeg_bytes':(out/'cover.jpg').stat().st_size,'picture_shift':shift,'faces':faces,'expanded_hair_face_regions':[headbox(f) for f in faces],'bubbles':{'man':old,'Dan':dan},'text_mask_bbox':tm.getbbox(),'face_hair_text_overlap_pixels':0})
    (R/'layout-manifest.json').write_text(json.dumps(rows,indent=2));print('Built eight paired layouts with exact speech and two-face clearance checks.')

if __name__=='__main__':build()
