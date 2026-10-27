#!/usr/bin/env python3
"""Dan's picked beach image 2, revised title-case headline and bottom teaser."""
from pathlib import Path
import json, shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy.ndimage import maximum_filter
from build import ROOT, OUT as BASE, W, H, SUP, fit, sha

OUT=BASE/'round3'
HEADLINE=['Do Women Like','The Dad Bod?']
TEASER='Surprising Answer Revealed!'

def build():
    OUT.mkdir(exist_ok=True)
    rows=[]
    for platform in ['instagram','youtube']:
        ig=platform=='instagram';previous=BASE/'round2'/platform
        source=previous/'cover-2.picture.png'
        im=Image.open(source).convert('RGBA')
        # Reuse the exact picked photograph and the original top scrim.
        old=Image.open(previous/'cover-2.png').convert('RGBA')
        yy=np.arange(H);alpha=np.clip((660-yy)/660,0,1)*225
        overlay=np.zeros((H,W,4),np.uint8);overlay[:,:,:3]=[4,17,35];overlay[:,:,3]=alpha.astype('uint8')[:,None]
        im.alpha_composite(Image.fromarray(overlay))
        d=ImageDraw.Draw(im);mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask)
        y=260 if ig else 90
        d.line((62,y-24,1018,y-24),fill='#FFD486',width=6)
        bounds=[]
        for i,word in enumerate(HEADLINE):
            f=fit('B',word,146 if i==0 else 158,940);ty=y+i*155
            d.text((W//2,ty),word,anchor='mt',font=f,fill='#FFF8E7' if i==0 else '#FFD486',stroke_width=4,stroke_fill='#06152B')
            md.text((W//2,ty),word,anchor='mt',font=f,fill=255,stroke_width=4)
            b=f.getbbox(word,anchor='mt');bounds.append([W//2+b[0]-4,ty+b[1]-4,W//2+b[2]+4,ty+b[3]+4])
        # Instagram retains this teaser in its central 3:4 profile tile.
        sy=1572 if ig else 1780
        f=fit('D',TEASER,68,930);b=f.getbbox(TEASER,anchor='mm')
        pill=(W//2+b[0]-26,sy+b[1]-19,W//2+b[2]+26,sy+b[3]+19)
        d.rounded_rectangle(pill,radius=15,fill='#071A31',outline='#FFD486',width=3)
        d.text((W//2,sy),TEASER,anchor='mm',font=f,fill='#FFF8E7')
        teaser_bounds=[W//2+b[0],sy+b[1],W//2+b[2],sy+b[3]]
        target=OUT/platform;target.mkdir(exist_ok=True)
        path=target/'dad-bod-cover-2-r3.png';im.convert('RGB').save(path)
        jpeg=path.with_suffix('.jpg');im.convert('RGB').save(jpeg,quality=92)
        mask.save(target/'headline-mask.png')
        person=np.asarray(Image.open(previous/'cover-2.person-mask.png'))>127
        collision=int((person & (maximum_filter(np.asarray(mask),size=31)>0)).sum())
        assert collision==0
        assert jpeg.stat().st_size<2000000
        assert all(30<=b[0]<b[2]<=1050 for b in bounds+[teaser_bounds])
        if ig:assert 240<=bounds[0][1] and teaser_bounds[3]<=1620
        # The teaser is below all torsos; the top headline is clear of all people.
        rows.append(dict(platform=platform,path=str(path),sha256=sha(path),jpeg_path=str(jpeg),jpeg_sha256=sha(jpeg),jpeg_bytes=jpeg.stat().st_size,picked_picture=str(source),picked_picture_sha256=sha(source),headline=HEADLINE,headline_bounds=bounds,headline_collision_pixels_with_15px_margin=collision,teaser=TEASER,teaser_bounds=teaser_bounds,teaser_pill=list(pill),teaser_font_size=f.size,passed=True))
    sheet=Image.new('RGB',(900,850),'#142031');d=ImageDraw.Draw(sheet);label=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),28)
    for i,r in enumerate(rows):
        d.text((i*450+18,16),r['platform'].title(),font=label,fill='white')
        im=Image.open(r['path']);im.thumbnail((420,760));sheet.paste(im,(i*450+15,62))
    sheet.save(OUT/'revised-design-2-both-layouts.jpg',quality=95)
    crop=Image.open(rows[0]['path']).crop((0,240,1080,1680));crop.save(OUT/'instagram-profile-crop.jpg',quality=95)
    (OUT/'manifest.json').write_text(json.dumps({'status':'revised exact files awaiting Dan approval','selected_design':'Round 2 design 2, image approved; wording revision requested','copy':{'headline':'Do Women Like The Dad Bod?','teaser':TEASER},'outputs':rows},indent=2))
    print(json.dumps({'built':2,'passed':True,'outputs':rows},indent=2))

if __name__=='__main__':build()
