#!/usr/bin/env python3
"""A fresh DS-107 cover round. Reuses SL-08 type helpers, no rejected key/assets."""
from pathlib import Path
import importlib.util, json, hashlib, sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

P=Path(__file__).resolve().parents[3]
R=P/'Short-form video content/covers/review/ds107-20261115-r2'
sys.path.insert(0,str(P/'scripts/covers/sl08-20261025'))
spec=importlib.util.spec_from_file_location('sl08_helpers',P/'scripts/covers/sl08-20261025/build.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
W,H=1080,1920
COPY=["It's Not Your",'Metabolism']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def real(ig):
    im=Image.new('RGBA',(W,H),(244,239,229,255))
    d=ImageDraw.Draw(im)
    d.ellipse((-180,150,1280,1520),fill=(224,231,233))
    src=P/'photos/finalized social media photos/_cutouts/studio-white-49_CUTOUT.png'
    raw=Image.open(src).convert('RGBA');b=raw.getchannel('A').getbbox()
    b=(b[0],b[1],b[2],4200)
    sub=raw.crop(b);height=970 if ig else 1110
    sub=sub.resize((round(sub.width*height/sub.height),height),Image.Resampling.LANCZOS)
    x=(W-sub.width)//2;y=240 if ig else 100
    shadow=Image.new('RGBA',sub.size,(17,47,65,255));shadow.putalpha(sub.getchannel('A').filter(ImageFilter.GaussianBlur(15)).point(lambda v:int(v*.25)))
    im.alpha_composite(shadow,(x+15,y+12));im.alpha_composite(sub,(x,y))
    return im,{'source':str(src),'source_sha256':sha(src),'source_crop':list(b),'person_top':y,'person_bottom':y+height,'source_pixels_preserved':True}

def photo(k,ig,end):
    source=R/f'source-{k}.png'
    raw=Image.open(source).convert('RGB').resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
    # Shift only enough to keep the full top of the person clear of the headline.
    person,_=h.person_mask(raw)
    ys=np.where(person.any(axis=1))[0]
    assert len(ys)
    shift=max(0,round(end+48-int(ys.min())))
    col=tuple(int(x) for x in np.asarray(raw.convert('RGB'))[:30].reshape(-1,3).mean(axis=0))
    im=Image.new('RGBA',(W,H),col+(255,));im.alpha_composite(raw,(0,shift))
    return im,{'source':str(source),'source_sha256':sha(source),'person_top':int(ys.min())+shift,'picture_shift':shift,'source_pixels_preserved':False}

def typography(im,k,ig):
    mask=Image.new('L',(W,H));d=ImageDraw.Draw(im)
    top=250 if ig else 100
    if k=='C':
        lines=["It's Not",'Your','Metabolism'];top=1240
        f=h.common(lines,h.FUTURA,135,980)
        for i,line in enumerate(lines):h.text(im,mask,(540,top+120*i),line,f,(9,39,58) if i<2 else (0,100,158),anchor='mt')
        d.rectangle((28,260 if ig else 110,38,1150),fill=(0,100,158))
    elif k=='A':
        d.rectangle((26,top-15,1054,top+296),fill=(255,215,24))
        f=h.common(COPY,h.DIN,160,950)
        for i,line in enumerate(COPY):h.text(im,mask,(540,top+144*i),line,f,(10,20,30) if i==0 else (187,25,28),anchor='mt')
    elif k=='B':
        d.rounded_rectangle((28,top-18,1052,top+307),radius=28,fill=(248,246,238))
        f=h.common(COPY,h.AVENIR,154,950)
        for i,line in enumerate(COPY):h.text(im,mask,(540,top+146*i),line,f,(16,39,63),anchor='mt')
        d.rectangle((270,top+281,810,top+290),fill=(20,132,170))
    elif k=='D':
        h.ramp(im,0,780,220,True,(5,9,22))
        f=h.common(COPY,h.IMPACT,154,960,5)
        for i,line in enumerate(COPY):h.text(im,mask,(540,top+150*i),line,f,'white' if i==0 else (90,221,255),5,anchor='mt')
        d.rectangle((28,top-20,39,top+305),fill=(222,62,47))
    else:
        h.ramp(im,0,740,195,True,(3,31,43))
        f=h.common(COPY,h.FUTURA,126,950,2)
        for i,line in enumerate(COPY):h.text(im,mask,(55,top+150*i),line,f,'white' if i==0 else (112,247,219),2,anchor='lt')
        d.rectangle((55,top+302,250,top+309),fill=(112,247,219))
    b=mask.getbbox();assert b and b[0]>=24 and b[2]<=1056,b
    assert b[1]>=(240 if ig else 70) and b[3]<=1620,b
    return mask,max(top+325,b[3]) if k!='C' else b[3]

def build():
    records=[]
    for k in 'ABCDE':
        for platform in ['instagram','youtube']:
            ig=platform=='instagram';out=R/'layouts'/k/platform;out.mkdir(parents=True,exist_ok=True)
            test=Image.new('RGBA',(W,H));_,bottom=typography(test,k,ig)
            im,info=real(ig) if k=='C' else photo(k,ig,bottom)
            picture=im.copy();mask,_=typography(im,k,ig)
            p=out/'cover.png';im.convert('RGB').save(p)
            im.convert('RGB').save(out/'cover.jpg',quality=93)
            assert (out/'cover.jpg').stat().st_size<2_000_000
            mask.save(out/'text-mask.png');picture.convert('RGB').save(out/'picture.jpg',quality=96)
            im.resize((270,480),Image.Resampling.LANCZOS).convert('RGB').save(out/'phone.jpg',quality=95)
            records.append({'round':2,'design':k,'platform':platform,'file':str(p),'sha256':sha(p),'text_bbox':mask.getbbox(),**info})
    (R/'layout-manifest.json').write_text(json.dumps(records,indent=2));print('Built 10 new layouts')

if __name__=='__main__':build()
