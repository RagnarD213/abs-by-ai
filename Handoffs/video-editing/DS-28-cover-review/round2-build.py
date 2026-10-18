#!/usr/bin/env python3
"""Option 3 typography revisions. Reuse the exact generated photograph."""
from pathlib import Path
import json
import hashlib
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
SOURCE = HERE.parent/'round1/assets/upscaled-3.png'
W,H=1080,1920
WHITE=(255,253,246)
GOLD=(255,205,91)
NAVY=(7,19,31)
FONT='/Users/danielrose/Library/Fonts/Manrope.ttf'
IMPACT='/System/Library/Fonts/Supplemental/Impact.ttf'
records=[]


def face(size,kind='manrope'):
    f=ImageFont.truetype(FONT if kind=='manrope' else IMPACT,size)
    if kind=='manrope':f.set_variation_by_name('ExtraBold')
    return f


def line(im,copy,y,width,color,kind='manrope',shadow=False):
    # Both lines fill the same width, including the shorter second line.
    size=300
    f=face(size,kind);b=f.getbbox(copy)
    while b[2]-b[0]>width:
        size-=1;f=face(size,kind);b=f.getbbox(copy)
    x=(W-(b[2]-b[0]))//2
    d=ImageDraw.Draw(im)
    if shadow:d.text((x-b[0]+4,y-b[1]+6),copy,font=f,fill=(0,0,0),stroke_width=5,stroke_fill=(0,0,0))
    d.text((x-b[0],y-b[1]),copy,font=f,fill=color)
    box=[x,y,x+b[2]-b[0],y+b[3]-b[1]]
    assert box[0]>=24 and box[2]<=1056
    return {'copy':copy,'font':kind,'size':size,'bounds':box}


def image(ig=False):
    im=ImageOps.fit(Image.open(SOURCE).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
    if ig:
        canvas=Image.new('RGB',(W,H),(12,25,38));canvas.paste(im,(0,195));im=canvas
    return im


def fade(im,start,full,color=NAVY):
    overlay=Image.new('RGB',im.size,color);mask=Image.new('L',im.size,0);d=ImageDraw.Draw(mask)
    for y in range(start,H):
        a=round(255*min(1,(y-start)/max(1,full-start)))
        d.line((0,y,W,y),fill=a)
    return Image.composite(overlay,im,mask)


def save(im,name,layout,lines):
    p=HERE/(name+'.jpg');im.save(p,quality=95,subsampling=0)
    assert p.stat().st_size<2_000_000
    for row in lines:
        b=row['bounds'];assert b[1]>=240 and b[3]<=(1620 if layout=='instagram' else 1810),b
        assert b[1]>1200 # Face, hair and abdomen are above all typography.
    records.append({'name':name,'layout':layout,'path':str(p),'dimensions':[W,H],
                    'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':lines})
    return im


def main():
    # Tall: original photograph, same white/gold identity, much wider two-line type.
    tall=fade(image(),1360,1460)
    boxes=[line(tall,'Stop Cooking',1440,1010,WHITE),line(tall,'Your Meals',1622,1010,(236,191,106))]
    tall=save(tall,'3-tall-larger-text','youtube',boxes)

    # A: same typography family, clean navy field removes countertop interference.
    a=fade(image(True),1190,1300)
    boxes=[line(a,'Stop Cooking',1305,1000,WHITE),line(a,'Your Meals',1476,1000,GOLD)]
    a=save(a,'3-short-A-clean-navy','instagram',boxes)

    # B: high-contrast gold panel with black, condensed display type.
    b=fade(image(True),1185,1270)
    d=ImageDraw.Draw(b);d.rectangle((22,1230,1058,1630),fill=GOLD)
    boxes=[line(b,'Stop Cooking',1250,984,NAVY,'impact'),line(b,'Your Meals',1432,984,NAVY,'impact')]
    b=save(b,'3-short-B-gold-panel','instagram',boxes)

    # C: oversized condensed white lettering with one gold line and a strong outline.
    c=fade(image(True),1170,1250)
    boxes=[line(c,'Stop Cooking',1250,1010,WHITE,'impact',True),line(c,'Your Meals',1438,1010,GOLD,'impact',True)]
    c=save(c,'3-short-C-bold-display','instagram',boxes)

    sheet=Image.new('RGB',(1540,1000),(237,237,233));d=ImageDraw.Draw(sheet)
    d.text((28,20),'Option 3 | Larger, Clearer Text',font=face(33),fill=NAVY)
    d.text((28,76),'Tall cover updated. Pick A, B or C for the shorter profile thumbnail.',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',25),fill=NAVY)
    labels=['Tall: Larger Text','A. Clean Navy','B. Gold Panel','C. Bold Display']
    for i,(label,im) in enumerate(zip(labels,[tall,a,b,c])):
        x=28+i*380
        d.text((x,137),label,font=face(24),fill=NAVY)
        crop=im if i==0 else im.crop((0,240,1080,1680))
        h=640 if i==0 else 480
        sheet.paste(crop.resize((360,h),Image.Resampling.LANCZOS),(x,194))
        if i>0:
            small=crop.resize((135,180),Image.Resampling.LANCZOS)
            sheet.paste(small,(x+112,729))
    d.text((410,937),'Small previews show how the text reads on a phone.',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22),fill=NAVY)
    sheet.save(HERE/'REVIEW-option-3-text-variations.jpg',quality=95,subsampling=0)
    (HERE/'manifest.json').write_text(json.dumps({'status':'awaiting-final-text-pick','image_option':3,'photo_unchanged':True,'new_generations':0,'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'outputs':records},indent=2)+'\n')


if __name__=='__main__':main()
