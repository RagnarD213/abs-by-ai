#!/usr/bin/env python3
"""RO-05 five review options. Existing real photos only; no generation or upload.
Adapts the Ab Wheel Workout recipe and Ad 5 studio layouts.
Run python3 build.py. Outputs stay in this build until Dan picks.
"""
from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
TH=ROOT/'social media graphics/youtube/thumbnails'
spec=importlib.util.spec_from_file_location('ab',TH/'Ab Wheel Workout/_build-2026-09-13/build.py')
ab=importlib.util.module_from_spec(spec);spec.loader.exec_module(ab)
ab.HERE=str(HERE);ab.LINES=['MY DAILY','SALAD'];ab.clean.LINES=ab.LINES
(HERE/'mask').mkdir(exist_ok=True)
W,H=1280,720

def studio(name,waist,ground):
    fn=ab.clean.o1 if ground=='dark' else ab.clean.o2
    canvas,mask=fn(name,W,H,.74,24,waist)
    # White headline and logo on both studio options.
    if ground=='light': canvas=ab.side_scrim(canvas,rw_frac=.65,strength=235,top_strength=200)
    return decorate(canvas,name)

def decorate(canvas,tag):
    mask=ab.person_mask(canvas,tag+'_before')
    size,_,_=ab.clean.set_type(canvas,mask,W,H,ab.WHITE,None)
    # Repeat the fitted geometry to validate all text and branding on the saved JPEG.
    f=ab.font(size);hs=[f.getbbox(t)[3]-f.getbbox(t)[1] for t in ab.LINES]
    lead=int(size*.4);total=sum(hs)+lead
    top=max(44+ab.logo_img(298).height+40,(44+ab.logo_img(298).height+40+H-60)//2-total//2)
    boxes=[];y=top
    for t,h in zip(ab.LINES,hs):
        b=f.getbbox(t);boxes.append((96,y,96+b[2]-b[0],y+h));y+=h+lead
    return canvas,size,boxes

def pool(name,keep):
    im=Image.open(TH/f'_finished-ads-build-2026-09-10/final/{name}-photo.jpg').convert('RGB')
    ch=int(im.height*keep);cw=int(ch*W/H)
    cx=int(json.loads((TH/f'_finished-ads-build-2026-09-10/final/{name}-comp.json').read_text())['subject_cx']*im.width)
    l=min(max(0,cx-int(cw*.69)),im.width-cw)
    canvas=ab.side_scrim(im.crop((l,0,l+cw,ch)).resize((W,H),Image.Resampling.LANCZOS))
    return decorate(canvas,name)

def food():
    # Crop away the finished master's lower third, preserving the finished bowl.
    im=Image.open(HERE/'salad-t005.jpg').convert('RGB').crop((0,0,1920,835))
    # Edge-to-edge real scene. No blur or generated food.
    im=im.crop((110,0,1594,835)).resize((W,H),Image.Resampling.LANCZOS)
    canvas=ab.side_scrim(im,rw_frac=.65,strength=238,top_strength=165)
    cut,_=ab.clean.place('studio-white-23',ab.clean.src('studio-white-23')['cut'],W,H,.76,24,.695)
    canvas.paste(cut,(0,0),cut)
    return decorate(canvas,'food')

variants=[(1,'Pool, relaxed smile','photo-221',lambda:pool('p221',1.0)),
          (2,'Pool, front-facing smile','photo-247',lambda:pool('p247',1.0)),
          (3,'Dark studio','studio-blue-192',lambda:studio('studio-blue-192',.65,'dark')),
          (4,'Light studio','studio-white-84',lambda:studio('studio-white-84',.715,'light')),
          (5,'Finished salad + real studio portrait','studio-white-23 + approved master 00:05.000',food)]
results=[]
for n,label,source,fn in variants:
    canvas,size,boxes=fn();path=HERE/f'ro05-option-{n}.jpg';canvas.save(path,quality=94,subsampling=0)
    rendered=Image.open(path).convert('RGB');pm=ab.person_mask(rendered,f'option{n}_rendered')
    clear=ab.clearance(pm,boxes)
    logo_box=(60,44,358,44+ab.logo_img(298).height)
    logo_overlap=int(pm[logo_box[1]:logo_box[3],logo_box[0]:logo_box[2]].sum())
    assert clear>=25,(n,clear)
    assert logo_overlap==0,(n,'logo overlap')
    assert path.stat().st_size<2000000
    rendered.resize((320,180),Image.Resampling.LANCZOS).save(HERE/f'ro05-option-{n}-feed.jpg',quality=94)
    row=dict(option=n,label=label,source=source,font_px=size,clearance_px=clear,logo_overlap_px=logo_overlap,
             dimensions=[W,H],bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),file=path.name)
    results.append(row);print(row)
(HERE/'qc.json').write_text(json.dumps(results,indent=2)+'\n')
# Two columns, with numbered labels outside the thumbnail.
sh=Image.new('RGB',(1372,1410),(242,242,244));d=ImageDraw.Draw(sh)
d.text((30,20),'RO-05: MY DAILY SALAD',font=ab.font(34),fill=ab.CHAR)
d.text((30,65),'Five thumbnail options | same headline | pick one or two',font=ab.font(20),fill=ab.CHAR)
for i,r in enumerate(results):
    x=30+(i%2)*686;y=118+(i//2)*425
    d.text((x,y),f"{r['option']}. {r['label']}",font=ab.font(22),fill=ab.CHAR)
    im=Image.open(HERE/r['file']);sh.paste(im.resize((640,360),Image.Resampling.LANCZOS),(x,y+35))
# Include an actual 320px check for the food option in the unused sixth cell.
x,y=716,968
d.text((x,y),'Phone-feed check (320px wide)',font=ab.font(22),fill=ab.CHAR)
sh.paste(Image.open(HERE/'ro05-option-5-feed.jpg'),(x,y+42))
sh.save(HERE/'REVIEW_ro05_thumbnails.jpg',quality=94,subsampling=0)
print('PASS: all five rendered JPEGs clear text and logo; review sheet ready.')
