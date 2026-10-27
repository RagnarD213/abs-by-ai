#!/usr/bin/env python3
"""DS55 cover review. Typesetting/compositing adapted from SL08's checked builder.

AI source plates come from codex-image.sh. C preserves the real studio cutout.
The same two-line copy feeds both platforms; only layout placement differs.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import hashlib, json, subprocess, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'Short-form video content/covers/review/ds55-five-minute-exercises-20261026'
W, H = 1080, 1920
SUP = Path('/System/Library/Fonts/Supplemental')
COPY = ['5 Minute', 'Home Workout']
FONTS = {
    'A': (SUP/'DIN Condensed Bold.ttf', 0),
    'B': (SUP/'Impact.ttf', 0),
    'C': (SUP/'Futura.ttc', 4),
    'D': (Path('/System/Library/Fonts/Avenir Next Condensed.ttc'), 8),
    'E': (SUP/'Baskerville.ttc', 2),
}
PM = Path.home()/'.cache/absbyai/personmask/personmask'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def font(k, size):
    p, i = FONTS[k]
    return ImageFont.truetype(str(p), size, index=i)

def fit(k, word, size, width):
    for n in range(size, 39, -1):
        f = font(k, n)
        b = f.getbbox(word)
        if b[2]-b[0] <= width:
            return f
    raise ValueError(word)

def title(im, mask, k, platform):
    ig = platform == 'instagram'
    y = 260 if ig else 90
    draw, md = ImageDraw.Draw(im), ImageDraw.Draw(mask)
    if k == 'A':
        draw.rectangle((0, y-24, W, y+330), fill='#FFD400')
        size, spacing = 190, 152
        colors = ['#111318', '#BB1E1E']
    elif k == 'B':
        size, spacing = 156, 155
        colors = ['#FFFFFF', '#49E4EF']
    elif k == 'C':
        draw.rounded_rectangle((36, y-25, W-36, y+315), radius=12, fill='#0B3171')
        size, spacing = 130, 145
        colors = ['#FFFFFF', '#E3F778']
    elif k == 'D':
        draw.polygon([(0,y-30),(W,y-30),(W,y+295),(0,y+345)], fill='#F6F5EE')
        draw.rectangle((48,y+24,61,y+269), fill='#D52626')
        size, spacing = 156, 140
        colors = ['#171C24', '#C82025']
    else:
        size, spacing = 148, 148
        colors = ['#FFFFFF', '#E9C171']
        draw.line((100,y-20,W-100,y-20), fill='#C8A463', width=4)
        draw.line((100,y+312,W-100,y+312), fill='#C8A463', width=4)
    bounds=[]
    for i,word in enumerate(COPY):
        f=fit(k,word,size,950 if k!='C' else 920)
        box=f.getbbox(word, anchor='mt')
        xx=W//2; yy=y+i*spacing
        stroke=4 if k=='B' else 0
        draw.text((xx,yy),word,font=f,anchor='mt',fill=colors[i],stroke_width=stroke,stroke_fill='#071322')
        md.text((xx,yy),word,font=f,anchor='mt',fill=255,stroke_width=stroke)
        bounds.append([xx+box[0]-stroke,yy+box[1]-stroke,xx+box[2]+stroke,yy+box[3]+stroke])
    return bounds

def picture(k, platform):
    im=ImageOps.fit(Image.open(OUT/'sources'/f'{k}.png').convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
    info={'plate':str(OUT/'sources'/f'{k}.png'),'plate_sha256':sha(OUT/'sources'/f'{k}.png')}
    if k=='B':
        im=im.crop((180,600,900,1880)).resize((W,H),Image.Resampling.LANCZOS);info['source_crop_1080']=[180,600,900,1880]
    if platform=='youtube' and k!='C':
        # Remove the Instagram reserve while keeping the complete lower picture.
        im=im.crop((0,145,W,H)).resize((W,H),Image.Resampling.LANCZOS)
    # A continuous soft scrim gives the two photo-led title treatments legibility.
    if k in 'BE':
        a=np.zeros((H,W,4),np.uint8);a[:,:,:3]=[5,13,26]
        for y in range(850):a[y,:,3]=int(220*max(0,1-y/850)**1.0)
        im.alpha_composite(Image.fromarray(a))
    if k=='C':
        dd=ImageDraw.Draw(im);ff=font('B',84);dd.text((140,1120),'5:00',font=ff,anchor='mm',fill='#103254')
        p=ROOT/'photos/finalized social media photos/_cutouts/studio-blue-169_CUTOUT.png'
        raw=Image.open(p).convert('RGBA');b=raw.getchannel('A').getbbox();sub=raw.crop(b)
        top=650 if platform=='instagram' else 480
        scale=(780 if platform=='instagram' else 860)/sub.width
        sub=sub.resize((round(sub.width*scale),round(sub.height*scale)),Image.Resampling.LANCZOS)
        pad=20;layer=Image.new('RGBA',(sub.width+2*pad,sub.height+2*pad));layer.alpha_composite(sub,(pad,pad))
        x=W-sub.width-30-pad;y=top-pad
        line=Image.new('RGBA',layer.size,'white');line.putalpha(layer.getchannel('A').filter(ImageFilter.MaxFilter(13)))
        im.alpha_composite(line,(x,y));im.alpha_composite(layer,(x,y))
        info.update(real_photo=True,source=str(p),source_sha256=sha(p),source_person_pixels_preserved=True,source_crop=list(b),scale=scale,subject_top=top)
    if k in 'ADE':
        # Keep the whole headline panel clear of actual hair, not just the glyphs.
        with tempfile.TemporaryDirectory(prefix='ds35-cover-') as temp:
            inp=Path(temp)/'picture.png';mp=Path(temp)/'mask.png';im.convert('RGB').save(inp)
            subprocess.run([str(PM),str(inp),str(mp)],capture_output=True,text=True,check=True)
            person=np.array(Image.open(mp))>127
            top=int(np.where(person.any(axis=1))[0].min())
        target=(260 if platform=='instagram' else 90)+({'D':365,'E':340}.get(k,355))
        shift=max(0,target-top)
        if shift:
            color=tuple(int(v) for v in np.array(im.convert('RGB'))[:40].reshape(-1,3).mean(axis=0))
            shifted=Image.new('RGBA',(W,H),color+(255,));shifted.alpha_composite(im.crop((0,0,W,H-shift)),(0,shift));im=shifted
        info.update(source_person_top=top,picture_shift=shift,minimum_subject_top=target)
    return im,info

def build(keys='ABCDE'):
    rows=[]
    for k in keys:
        for platform in ['instagram','youtube']:
            d=OUT/platform;d.mkdir(exist_ok=True)
            im,info=picture(k,platform)
            p=d/f'five-minute-cover-{k}.png';pic=d/f'five-minute-cover-{k}.picture.png'
            im.convert('RGB').save(pic)
            mask=Image.new('L',(W,H));bounds=title(im,mask,k,platform)
            assert all(30<=b[0]<b[2]<=W-30 for b in bounds)
            assert all((240 if platform=='instagram' else 60)<=b[1]<b[3]<1620 for b in bounds)
            if k=='E':ImageDraw.Draw(im).rectangle((22,22,W-23,H-23),outline='#B5975A',width=4)
            im.convert('RGB').save(p)
            if platform=='youtube':
                im.convert('RGB').save(p.with_suffix('.jpg'),quality=92)
                info.update(jpeg_path=str(p.with_suffix('.jpg')),jpeg_sha256=sha(p.with_suffix('.jpg')),jpeg_bytes=p.with_suffix('.jpg').stat().st_size)
            mask.save(d/f'five-minute-cover-{k}.text-mask.png')
            rows.append(dict(letter=k,platform=platform,path=str(p),sha256=sha(p),text_bounds=bounds,**info))
    (OUT/'manifest.json').write_text(json.dumps({'status':'awaiting Dan pick','copy':COPY,'outputs':rows},indent=2))
    sheet=Image.new('RGB',(5*300,2*565),'#101722');dr=ImageDraw.Draw(sheet)
    label=ImageFont.truetype(str(SUP/'Arial Bold.ttf'),24)
    for row in rows:
        x='ABCDE'.index(row['letter'])*300;y=0 if row['platform']=='instagram' else 565
        dr.text((x+12,y+14),row['letter']+' / '+('Instagram' if y==0 else 'YouTube'),font=label,fill='white')
        im=Image.open(row['path']);im.thumbnail((280,500));sheet.paste(im,(x+10,y+52))
    sheet.save(OUT/'five-cover-choices.jpg',quality=95)
    print(f'Built {len(rows)} covers and review sheet')

if __name__=='__main__':build()
