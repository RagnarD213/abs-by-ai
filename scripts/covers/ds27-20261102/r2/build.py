"""Four requested real exercise photographs, with paired platform layouts.

Uses original finalized photo pixels, cropping/resizing and graphic overlays only.
No image generation or repainting of Dan. Prior choices stay preserved.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib, json
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT/'Short-form video content/covers/review/ds27-20261102/r2'
PHOTO = ROOT/'photos/finalized social media photos'
PLAN = json.loads((Path(__file__).parent/'design-plan.json').read_text())
SUP = Path('/System/Library/Fonts/Supplemental')
W,H=1080,1920

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(name,size):return ImageFont.truetype(str(SUP/name),size)
def fit(text,name,size,width):
    while size>30:
        f=font(name,size)
        if f.getbbox(text)[2]-f.getbbox(text)[0]<=width:return f
        size-=1
    raise ValueError(text)

def text(im,mask,txt,xy,size,color,name='Impact.ttf',anchor='lt',width=960,stroke=0):
    f=fit(txt,name,size,width);d=ImageDraw.Draw(im);m=ImageDraw.Draw(mask)
    d.text(xy,txt,font=f,fill=color,anchor=anchor,stroke_width=stroke,stroke_fill='#07172C')
    m.text(xy,txt,font=f,fill=255,anchor=anchor,stroke_width=stroke)
    return list(d.textbbox(xy,txt,font=f,anchor=anchor,stroke_width=stroke))

def photo(im,src,box,crop=None):
    pic=Image.open(src).convert('RGB')
    if crop:pic=pic.crop(crop)
    x0,y0,x1,y1=box
    # Contain the measured crop so the complete selected action stays visible.
    pic=ImageOps.contain(pic,(x1-x0,y1-y0),Image.Resampling.LANCZOS)
    x=x0+(x1-x0-pic.width)//2;y=y0+(y1-y0-pic.height)//2
    im.paste(pic,(x,y))
    return {'source_crop':crop or [0,0,*Image.open(src).size], 'photo_bounds':[x,y,x+pic.width,y+pic.height]}

def build(k,pf):
    ig=pf=='instagram';spec=PLAN['designs'][k];src=PHOTO/spec['photo']
    mask=Image.new('L',(W,H));bounds=[];ink='#0A2034';im=Image.new('RGB',(W,H),'#F8F5EE')
    if k=='1':
        # Airy editorial white, a red rule and a tall, uncropped action photograph.
        y=258 if ig else 85
        bounds.append(text(im,mask,'Home', (62,y),182,ink,width=950))
        bounds.append(text(im,mask,'Workouts',(62,y+155),182,ink,width=950))
        ImageDraw.Draw(im).rectangle((64,y+328,1016,y+342),fill='#E34536')
        bounds.append(text(im,mask,'Skip The Commute',(64,y+372),78,ink,'Arial Bold.ttf',width=950))
        top=760 if ig else 585
        info=photo(im,src,(25,top,1055,1910),[180,380,2580,3600])
    elif k=='2':
        # Original jump rope photo, an orange slab and left aligned bold typography.
        im=Image.new('RGB',(W,H),'#12202B')
        info=photo(im,src,(0,230 if ig else 80,W,2150 if ig else 2000),[120,130,2620,4060])
        y=252 if ig else 78
        ImageDraw.Draw(im).rectangle((0,y-20,890,y+330),fill='#F47532')
        bounds.append(text(im,mask,'Home',(55,y+12),162,'#102430',width=810))
        bounds.append(text(im,mask,'Workouts',(55,y+158),162,'#102430',width=810))
        # The subtitle has its own small footer ribbon, clear of the torso.
        sy=1514 if ig else 1730
        ImageDraw.Draw(im).rectangle((38,sy-20,1042,sy+106),fill='#102430')
        bounds.append(text(im,mask,'Skip The Commute',(65,sy),87,'#FFFFFF','Arial Bold.ttf',width=950))
    elif k=='3':
        # Landscape action is intentionally wide. No head, hands or shoes are sacrificed.
        im=Image.new('RGB',(W,H),'#092B42');y=255 if ig else 95
        bounds.append(text(im,mask,'Home Workouts',(58,y),136,'#FFFFFF',width=960))
        ImageDraw.Draw(im).rectangle((58,y+157,365,y+171),fill='#43D9E6')
        top=610 if ig else 480
        info=photo(im,src,(26,top,1054,top+760),[0,0,4096,2747])
        ImageDraw.Draw(im).rectangle((26,top-8,1054,top),fill='#43D9E6')
        sy=1390
        bounds.append(text(im,mask,'Skip The',(58,sy),133,'#FFFFFF',width=960))
        bounds.append(text(im,mask,'Commute',(58,sy+140),162,'#43D9E6',width=960))
    else:
        # Overhead ball and hands remain in the real photograph below the yellow title.
        im=Image.new('RGB',(W,H),'#FBCB22');y=257 if ig else 82
        bounds.append(text(im,mask,'Home Workouts',(W//2,y),139,'#142C3B',anchor='mt',width=970))
        ImageDraw.Draw(im).rectangle((52,y+180,1028,y+310),fill='#FFFFFF')
        bounds.append(text(im,mask,'Skip The Commute',(W//2,y+200),81,'#142C3B','Arial Bold.ttf',anchor='mt',width=940))
        top=660 if ig else 490
        info=photo(im,src,(0,top,W,H),[40,0,2707,3550])
    for b in bounds:
        assert 25<=b[0]<b[2]<=W-25,b
        assert (240 if ig else 50)<=b[1]<b[3]<=(1680 if ig else 1850),b
    d=OUT/'review';d.mkdir(exist_ok=True)
    path=d/f'R2-{k}-{pf}.png';im.save(path);mask.save(d/f'R2-{k}-{pf}-text-mask.png')
    im.save(path.with_suffix('.jpg'),quality=94)
    assert path.with_suffix('.jpg').stat().st_size<2_000_000
    if ig:im.crop((0,240,W,1680)).resize((270,360),Image.Resampling.LANCZOS).save(d/f'R2-{k}-grid.jpg',quality=95)
    return {'design':k,'platform':pf,'path':str(path),'sha256':sha(path),'jpeg_sha256':sha(path.with_suffix('.jpg')),'source':str(src),'source_sha256':sha(src),'original_person_pixels':True,'image_generation':False,'text_bounds':bounds,**info}

if __name__=='__main__':
    OUT.mkdir(exist_ok=True);rows=[]
    for k in PLAN['designs']:
        for pf in ['instagram','youtube']:rows.append(build(k,pf))
    (OUT/'manifest.json').write_text(json.dumps({'status':'awaiting Dan cover pick','request':'four unique designs, four real workout photographs','outputs':rows},indent=2))
    font_label=font('Arial Bold.ttf',24)
    sheet=Image.new('RGB',(1200,1140),'#112331');d=ImageDraw.Draw(sheet)
    for i,k in enumerate(PLAN['designs']):
        for n,pf in enumerate(['instagram','youtube']):
            x=i*300;y=n*570;d.text((x+10,y+10),f'{k} / {pf.title()}',font=font_label,fill='white')
            im=Image.open(OUT/'review'/f'R2-{k}-{pf}.png');im.thumbnail((280,500));sheet.paste(im,(x+10,y+52))
    sheet.save(OUT/'review/four-cover-choices.jpg',quality=95)
    print('Built four real-photo designs, eight platform layouts')
