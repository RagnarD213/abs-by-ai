#!/usr/bin/env python3
"""DS-107 cover packet; adapt the checked SL-08 cover typography helpers.

The approved film is never opened for writing. The real pool choice uses only
crop, resize and local layout; original face/body pixels are not regenerated.
"""
from pathlib import Path
import importlib.util
import json
import hashlib
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

P = Path(__file__).resolve().parents[3]
R = P / 'Short-form video content/covers/review/ds107-20261115'
sys.path.insert(0, str(P / 'scripts/covers/sl08-20261025'))
sp = importlib.util.spec_from_file_location('sl08_cover_helpers', P / 'scripts/covers/sl08-20261025/build.py')
old = importlib.util.module_from_spec(sp)
sp.loader.exec_module(old)
W, H = 1080, 1920
COPY = ["It's Not Your", 'Metabolism']
HEAD = {'A': (320, 515, 700, 870), 'B': (300, 350, 600, 690),
        'C': (390, 745, 665, 1030), 'D': (370, 550, 690, 880),
        'E': (360, 575, 740, 925)}

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def picture(k, ig):
    if k == 'C':
        raw = Image.open(P / 'photos/finalized social media photos/photo-172_FINAL_PRIMARY.jpg').convert('RGB')
        # Stop above either leg opening. Keep all photographed hair, face, torso.
        crop = raw.crop((400, 350, 2600, 2540))
        im = Image.new('RGBA', (W, H), (6, 24, 38, 255))
        crop = crop.resize((1080, 1075), Image.Resampling.LANCZOS)
        im.alpha_composite(crop.convert('RGBA'), (0, 650 if ig else 520))
        return im
    raw = Image.open(R / f'source-{k}.png').convert('RGB').resize((W,H), Image.Resampling.LANCZOS)
    col = tuple(int(v) for v in np.asarray(raw)[:30].reshape(-1,3).mean(axis=0))
    im = Image.new('RGBA', (W,H), col+(255,))
    offset = {'A': 120 if ig else 0, 'B': -300 if ig else -240,
              'D': 100 if ig else 0, 'E': 180 if ig else 20}[k]
    im.alpha_composite(raw.convert('RGBA'), (0,offset))
    if k == 'B':
        old.ramp(im, 1280, 1700, 255, False, (5,22,35))
    return im

def type_on(im, k, ig):
    mask = Image.new('L',(W,H))
    d = ImageDraw.Draw(im)
    top = (250 if ig else 105)
    if k == 'B':
        top = 1300 if ig else 1320
        f=old.common(COPY,old.AVENIR,164,980,2)
        for n,line in enumerate(COPY):
            old.text(im,mask,(540,top+n*150),line,f,'white' if n==0 else (66,223,255),2,anchor='mt')
    elif k == 'A':
        d.rectangle((32,top-18,1048,top+290),fill=(255,216,0))
        f=old.common(COPY,old.DIN,154,930)
        for n,line in enumerate(COPY):
            old.text(im,mask,(540,top+n*140),line,f,(12,17,20) if n==0 else (187,28,30),anchor='mt')
    elif k == 'D':
        old.ramp(im,0,720,180,True,(5,28,43))
        f=old.common(COPY,old.FUTURA,122,970,3)
        for n,line in enumerate(COPY):
            old.text(im,mask,(540,top+n*145),line,f,'white',3,anchor='mt')
        d.rectangle((320,top+283,760,top+292),fill=(255,205,54))
    elif k == 'E':
        d.rectangle((0,top-20,W,top+304),fill=(245,92,69))
        f=old.common(COPY,old.ABLACK,119,980)
        for n,line in enumerate(COPY):
            old.text(im,mask,(540,top+n*140),line,f,(14,26,39) if n==0 else 'white',anchor='mt')
    else:
        f=old.common(COPY,old.IMPACT,154,960)
        for n,line in enumerate(COPY):
            old.text(im,mask,(540,top+n*160),line,f,'white' if n==0 else (74,222,255),anchor='mt')
        d.rectangle((430,top+336,650,top+343),fill=(74,222,255))
    b=mask.getbbox()
    assert b and b[0]>=32 and b[2]<=W-32,b
    assert b[1]>=(240 if ig else 70) and b[3]<= (1740 if not ig and k=='B' else 1620),b
    return mask

def build():
    records=[]
    for k in 'ABCDE':
        for platform in ['instagram','youtube']:
            ig=platform=='instagram'
            out=R/'layouts'/k/platform
            out.mkdir(parents=True,exist_ok=True)
            im=picture(k,ig); pic=im.copy();mask=type_on(im,k,ig)
            p=out/'cover.png';im.convert('RGB').save(p)
            if not ig:
                im.convert('RGB').save(out/'cover.jpg',quality=93)
                assert (out/'cover.jpg').stat().st_size<2_000_000
            mask.save(out/'text-mask.png');pic.convert('RGB').save(out/'picture.jpg',quality=96)
            phone=im.resize((270,480),Image.Resampling.LANCZOS).convert('RGB');phone.save(out/'phone.jpg',quality=95)
            if ig: im.crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS).convert('RGB').save(out/'grid.jpg',quality=95)
            records.append({'design':k,'platform':platform,'path':str(p),'sha256':sha(p),'text_bbox':mask.getbbox(),
                            'source_pixels_preserved':k=='C','source_crop':[400,350,2600,2540] if k=='C' else None})
    (R/'layout-manifest.json').write_text(json.dumps(records,indent=2))
    print('Built ten layouts. Cover approval pending.')

if __name__=='__main__': build()
