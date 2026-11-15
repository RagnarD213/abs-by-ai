"""DS-41 cover layouts. Final image/type geometry, provenance and QA live in setup."""
from pathlib import Path
import json, hashlib, subprocess
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[3]
P = Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
OUT=P/'designed'; OUT.mkdir(exist_ok=True)
W,H=1080,1920
FONT='/System/Library/Fonts/Supplemental/Impact.ttf'
SMALL='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
styles={
 'a':('#ffd51a','#141414','#141414','band'),
 'b':('#102d47','#ffffff','#66ddff','gradient'),
 'c':('#f9f0dd','#171e25','#b05422','card'),
 'd':('#fff7ed','#143246','#db5925','divider'),
 'e':('#39151e','#fff5e1','#ff8b70','split'),
 'g1':('#a63b20','#fff7e8','#ffd86a','rule'),
 'g2':('#f9f5df','#074d3a','#074d3a','pill'),
 'g3':('#173d68','#ffffff','#ffad6b','outline'),
}

def text(im, phrase, y, maxsize, color, font=FONT, width=960, left=None):
    d=ImageDraw.Draw(im)
    for size in range(maxsize,29,-1):
        f=ImageFont.truetype(font,size)
        if d.textlength(phrase,font=f)<=width: break
    b=d.textbbox((0,0),phrase,font=f); x=(W-d.textlength(phrase,font=f))/2
    xy=(round(x if left is None else left),round(y-b[1]));d.text(xy,phrase,font=f,fill=color)
    box=d.textbbox(xy,phrase,font=f)
    assert box[0]>=45 and box[2]<=1035
    return {'text':phrase,'box':list(box),'font_size':size}

def lower(im, src, top):
    # Remove only empty upper scenery. Anchor the crop to its top, preserving hair.
    src=src.crop((0,round(src.height*.20),src.width,src.height))
    scale=max(W/src.width,(H-top)/src.height)
    src=src.resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS)
    left=(src.width-W)//2
    im.paste(src.crop((left,0,left+W,H-top)),(0,top))

records=[]
for k,(bg,fg,accent,kind) in styles.items():
 for platform in ['Instagram','YouTube']:
    top=660 if platform=='Instagram' else 540
    im=Image.new('RGB',(W,H),bg)
    if k=='c':
        back=Image.open(P/'plates/c.png').convert('RGB').resize((1080,608),Image.Resampling.LANCZOS)
        ImageDraw.Draw(im).rectangle((0,top,W,H),fill='#102033')
        im.paste(back,(0,1312))
        real=Image.open(ROOT/'photos/finalized social media photos/_cutouts/studio-white-23_CUTOUT.png').convert('RGBA')
        real=real.crop(real.getbbox()); real.thumbnail((860,1230),Image.Resampling.LANCZOS)
        im.paste(real,((W-real.width)//2,top+30),real)
    elif k=='e':
        # Whole real source head fills the scene; small natural reaction foreground.
        kevin=Image.open(P/'kevin-source.jpg').convert('RGB').crop((0,60,1080,1160))
        im.paste(kevin,(0,top))
        ImageDraw.Draw(im).rectangle((0,top+1100,W,H),fill='#111014')
        dan=Image.open(P/'plates/e.png').convert('RGB')
        import mediapipe as mp
        with mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0) as seg:
            m=seg.process(np.array(dan)).segmentation_mask
        # Soft, natural photographic edge; no white keyline or sticker treatment.
        alpha=np.uint8(np.clip((m-.24)/.55,0,1)*255)
        dan=dan.convert('RGBA');dan.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.5)))
        dan=dan.crop((0,440,900,1672));dan.thumbnail((660,1000),Image.Resampling.LANCZOS)
        im.paste(dan,(0,H-dan.height),dan)
    elif k in ['b','d']:
        # Full photograph, including the sky/wall behind the type: no header box.
        im=Image.open(P/'plates'/f'{k}.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
        if k=='b':
            arr=np.asarray(im).copy().astype(float)
            a=np.maximum(0,1-np.arange(H)/710)*.88
            arr=arr*(1-a[:,None,None])+np.array([16,45,71])*a[:,None,None]
            im=Image.fromarray(np.uint8(arr))
    else:
        src=P/('google/'+k+'.jpg' if k.startswith('g') else 'plates/'+k+'.png')
        lower(im,Image.open(src).convert('RGB'),top)
    d=ImageDraw.Draw(im)
    start=268 if platform=='Instagram' else 108
    # Upper photo/scenery retains a full-bleed color field; every headline has two lines.
    if kind=='card':
        d.rounded_rectangle((38,start-24,1042,top-20),radius=22,fill='#fff8e9')
    if kind in ['rule','split']:
        d.line((70,start+66,1010,start+66),fill=accent,width=5)
    if kind=='pill':
        d.rounded_rectangle((354,start-9,726,start+55),radius=28,fill='#074d3a')
    t=[]
    if kind=='divider':
        d.rectangle((46,start-6,59,start+325),fill=accent)
        t.append(text(im,'Kevin James',start,42,accent,SMALL,width=900,left=86))
        t.append(text(im,'One Cheat Day',start+85,111,fg,SMALL,width=900,left=86))
        t.append(text(im,'Wrecked His Diet',start+225,103,accent,SMALL,width=900,left=86))
    elif kind=='card':
        t.append(text(im,'Kevin James',start,43,accent,SMALL))
        t.append(text(im,'One Cheat Day',start+100,105,fg,SMALL))
        t.append(text(im,'Wrecked His Diet',start+240,101,fg,SMALL))
    else:
        t.append(text(im,'Kevin James',start,43,'#f9f5df' if kind=='pill' else accent,SMALL))
        t.append(text(im,'One Cheat Day',start+100,126,fg))
        t.append(text(im,'Wrecked His Diet',start+255,122,accent if k in ['b','d','e','g1','g3'] else fg))
    assert min(x['box'][1] for x in t)>=(240 if platform=='Instagram' else 90)
    assert max(x['box'][3] for x in t)<top-18
    f=OUT/f'{k}-{platform}.png';im.save(f)
    jpg=f.with_suffix('.jpg');im.save(jpg,quality=94,subsampling=0)
    assert jpg.stat().st_size<2_000_000
    # Exact typography ink mask for face/hair/torso clearance QA.
    mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask)
    for r in t:md.rectangle(r['box'],fill=255)
    mask.save(OUT/f'{k}-{platform}-textmask.png')
    crop=im.crop((0,240,W,1680));crop.resize((270,360)).save(OUT/f'{k}-{platform}-grid.jpg',quality=94)
    records.append({'concept':k,'platform':platform,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'jpg':str(jpg),'jpg_bytes':jpg.stat().st_size,'text':t,'image_top':top,'original_real_person_pixels':k=='c','celebrity_real_source':str(P/'kevin-source.jpg') if k=='e' else None})
(P/'layout-manifest.json').write_text(json.dumps(records,indent=2))
sheet=Image.new('RGB',(2160,1100),'#101b29');d=ImageDraw.Draw(sheet)
for i,k in enumerate(styles):
    for j,platform in enumerate(['Instagram','YouTube']):
        im=Image.open(OUT/f'{k}-{platform}.png').resize((128,228))
        x=(i%4)*540+j*135;y=(i//4)*550+38
        sheet.paste(im,(x,y));d.text((x,y-24),k+' '+platform,fill='white')
    crop=Image.open(OUT/f'{k}-Instagram-grid.jpg');sheet.paste(crop,((i%4)*540+270,(i//4)*550+38))
sheet.save(P/'layout-sheet.jpg',quality=96)
print('Built 16 1080x1920 covers, 16 JPEGs under 2MB, and grid crops.')
