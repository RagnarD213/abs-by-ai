from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import numpy as np,json,hashlib

P=Path(__file__).resolve().parent;R=P.parent;O=P/'options';O.mkdir(exist_ok=True)
W,H=1080,1920;XY=(270,805)
FONT='/System/Library/Fonts/Supplemental/Impact.ttf'
f=ImageFont.truetype(FONT,205)

def stamp(style):
    im=Image.new('RGBA',(740,270));d=ImageDraw.Draw(im)
    if style=='old':
        d.rounded_rectangle((17,17,723,253),radius=10,fill=(196,23,24,238),outline=(238,38,35,255),width=9);color=(255,255,255,255)
    elif style=='A':
        d.rounded_rectangle((17,17,723,253),radius=10,outline=(202,22,24,224),width=9);color=(202,22,24,224)
    elif style=='B':
        d.rounded_rectangle((17,17,723,253),radius=10,outline=(190,17,22,215),width=9);color=(190,17,22,215)
    else:
        d.rounded_rectangle((17,17,723,253),radius=10,fill=(196,23,24,24),outline=(190,17,22,148),width=9);color=(190,17,22,148)
    b=d.textbbox((0,0),'Fake',font=f);d.text(((740-d.textlength('Fake',font=f))/2,37-b[1]),'Fake',font=f,fill=color)
    if style=='B':
        # Small correlated gaps mimic worn ink, while retaining the same letter shapes.
        arr=np.array(im);rng=np.random.default_rng(4134);texture=Image.fromarray(rng.integers(0,256,(65,180),dtype=np.uint8)).resize(im.size,Image.Resampling.BICUBIC)
        tex=np.asarray(texture);strength=np.ones(tex.shape);strength[tex>175]=.12;strength[(tex>145)&(tex<=175)]=.55
        arr[:,:,3]=np.uint8(arr[:,:,3]*strength);im=Image.fromarray(arr)
    return im.rotate(-12,Image.Resampling.BICUBIC,expand=True)

old=stamp('old');rect=(*XY,XY[0]+old.width,XY[1]+old.height);oldmask=np.zeros((H,W),bool);oldmask[XY[1]:rect[3],XY[0]:rect[2]]=np.asarray(old.getchannel('A'))>0
raw=Image.open(R/'previous-r2/assets/source-12.png').convert('RGB').crop((655,74,1166,631));raw=ImageOps.fit(raw,(W,H),Image.Resampling.LANCZOS,centering=(.52,.5))
noise=np.random.default_rng(1034).normal(0,.65,(H,W,1));records=[]
styles={'A':'Clean Stamp','B':'Worn Ink','C':'Faded Stamp'}
for platform in ['Instagram','YouTube']:
    orig=Image.open(R/'designed'/f'laugh-etched-{platform}.png').convert('RGB');orig_arr=np.asarray(orig)
    # Reconstruct just the covered source-photo area. Every pixel outside the original
    # stamp footprint remains byte-for-byte identical, including the selected person.
    for style,name in styles.items():
        layer=stamp(style);support=np.asarray(layer.getchannel('A'))>0
        changedmask=oldmask.copy();changedmask[XY[1]:rect[3],XY[0]:rect[2]]|=support
        clean=raw.convert('RGBA');clean.alpha_composite(layer,XY)
        patch=np.clip(np.asarray(clean.convert('RGB')).astype(float)+noise,0,255).astype('uint8')
        result=orig_arr.copy();result[changedmask]=patch[changedmask]
        assert np.array_equal(result[~changedmask],orig_arr[~changedmask])
        # The diagonal stamp's support cannot touch the selected person's hair/body.
        fg=Image.open(R/'assets/laugh-keyed.png').filter(ImageFilter.GaussianBlur(.32));fg=fg.resize((520,round(fg.height*520/fg.width)),Image.Resampling.LANCZOS)
        person=np.zeros((H,W),bool);person[H-fg.height:,0:520]=np.asarray(fg.getchannel('A'))>1
        assert not np.any(changedmask & person)
        out=O/f'{style}-{platform}.png';Image.fromarray(result).save(out)
        records.append({'option':style,'name':name,'platform':platform,'file':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'stamp_bounds':rect,'rotation_degrees':-12,'original_stamp_canvas':[740,270],'all_pixels_outside_stamp_unchanged':True,'all_person_pixels_unchanged':True,'new_generation_calls':0})
(P/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
sheet=Image.new('RGB',(1080,690),'#101a28');d=ImageDraw.Draw(sheet);titlefont=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',23)
for i,(style,name) in enumerate(styles.items()):
    d.text((i*360+15,15),style+' · '+name,fill='white',font=titlefont);im=Image.open(O/f'{style}-Instagram.png').resize((350,622));sheet.paste(im,(i*360+5,55))
sheet.save(P/'three-stamps.jpg',quality=96)
print('Built 3 stamp options in both layouts; all person/non-stamp pixels unchanged.')
