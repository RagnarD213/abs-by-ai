#!/usr/bin/env python3
"""DS-28 cover review. Real pool/studio pixels remain photographic.

Run from any directory. Generated plates and prompts sit beside this recipe.
No modification of the approved film is performed here.
"""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
PROJECT = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
W, H = 1080, 1920
FONTS = Path('/System/Library/Fonts/Supplemental')
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'
WHITE = (255, 253, 246)
records = []


def font(name, size):
    f = ImageFont.truetype(str(FONTS / name) if name != 'Manrope' else MANROPE, size)
    if name == 'Manrope':
        f.set_variation_by_name('ExtraBold')
    return f


def text(im, copy, x, y, name, size, color, maxwidth, align='left', stroke=0):
    d = ImageDraw.Draw(im)
    f = font(name, size)
    while d.textbbox((0, 0), copy, font=f, stroke_width=stroke)[2] > maxwidth:
        size -= 1
        f = font(name, size)
    b = d.textbbox((0, 0), copy, font=f, stroke_width=stroke)
    width = b[2] - b[0]
    if align == 'center':
        x -= width // 2
    d.text((x-b[0], y-b[1]), copy, font=f, fill=color,
           stroke_width=stroke, stroke_fill=(7, 14, 18))
    box = [x, y, x+width, y+b[3]-b[1]]
    assert box[0] >= 24 and box[2] <= W-24, box
    return box


def plate(i):
    path = HERE / f'assets/upscaled-{i}.png'
    if not path.exists():
        path = HERE / f'assets/generated-{i}.png'
    return ImageOps.fit(Image.open(path).convert('RGB'), (W, H), method=Image.Resampling.LANCZOS).convert('RGBA')


def scrim(im, top, bottom, alpha, reverse=False):
    mask = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(mask)
    for y in range(max(0, top), min(H, bottom)):
        t = (y-top) / max(1, bottom-top)
        a = int(alpha*(t if reverse else 1-t))
        d.line((0, y, W, y), fill=a)
    layer = Image.new('RGBA', (W, H), (5, 13, 20, 0))
    layer.putalpha(mask)
    return Image.alpha_composite(im, layer)


def portrait(im, filename, x, y, height, end, outline=0):
    source = PROJECT / 'photos/finalized social media photos/_cutouts' / filename
    raw = Image.open(source).convert('RGBA')
    left, top, right, bottom = raw.getbbox()
    subject = raw.crop((left, top, right, min(bottom, end)))
    subject = subject.resize((round(subject.width*height/subject.height), height), Image.Resampling.LANCZOS)
    if outline:
        alpha = subject.getchannel('A')
        rim = alpha.filter(ImageFilter.MaxFilter(outline*2+1))
        edge = Image.new('RGBA', subject.size, WHITE+(0,))
        edge.putalpha(rim)
        im.alpha_composite(edge, (x, y))
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0))
    shade = Image.new('RGBA', subject.size, (0, 0, 0, 0))
    shade.putalpha(subject.getchannel('A').point(lambda v: int(v*0.35)))
    shadow.alpha_composite(shade, (x+12, y+12))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(14)))
    im.alpha_composite(subject, (x, y))
    return im, {'source':str(source), 'crop':[left,top,right,min(bottom,end)],
                'position':[x,y], 'height':height,
                'hair_face_box':[x+round(subject.width*.25),y,x+round(subject.width*.75),y+round(height*.25)]}


def build(i, layout):
    im = plate(i)
    ig = layout == 'instagram'
    boxes = []
    subject = None
    if i == 1:
        im = scrim(im, 0, 780, 135)
        im, subject = portrait(im, 'photo-247_CUTOUT.png', 320, 645 if ig else 565, 1400, 3730)
        y = 304 if ig else 115
        boxes += [text(im,'Stop Cooking',66,y,'Georgia Bold.ttf',113,WHITE,950)]
        boxes += [text(im,'Your Meals',66,y+145,'Georgia Bold.ttf',118,WHITE,950)]
        ImageDraw.Draw(im).rectangle((69,y+279,375,y+290),fill=(220,58,42))
    elif i == 2:
        im, subject = portrait(im,'studio-blue-222_CUTOUT.png',100,680 if ig else 570,1400,4490,outline=8)
        y = 304 if ig else 120
        boxes += [text(im,'Stop Cooking',540,y,'Impact.ttf',170,(255,218,79),960,'center')]
        boxes += [text(im,'Your Meals',540,y+185,'Impact.ttf',182,WHITE,960,'center')]
    elif i == 3:
        if ig:
            moved = Image.new('RGBA',(W,H),(12,25,38,255))
            moved.alpha_composite(im,(0,195))
            im = moved
        # The lower navy cabinet gives the food and portrait a clear headline band.
        y = 1385 if ig else 1468
        im = scrim(im, y-80, H, 195, reverse=True)
        boxes += [text(im,'Stop Cooking',540,y,'Manrope',119,WHITE,946,'center')]
        boxes += [text(im,'Your Meals',540,y+139,'Manrope',119,(229,184,104),946,'center')]
        subject = {'generated': True,'reference':'studio-white-23_FINAL_PRIMARY.jpg',
                   'hair_face_box':[380,275 if ig else 80,680,590 if ig else 395]}
    elif i == 4:
        d = ImageDraw.Draw(im)
        y = 794 if ig else 736
        # Offset orange strokes frame an overhead food editorial, not a portrait panel.
        d.line((74,y-57,234,y-57),fill=(230,105,36),width=13)
        boxes += [text(im,'Stop Cooking',66,y,'Futura.ttc',132,(20,42,35),952)]
        boxes += [text(im,'Your Meals',66,y+156,'Futura.ttc',146,(20,42,35),952)]
        d.line((840,y+312,999,y+312),fill=(230,105,36),width=13)
    else:
        y = 440 if ig else 325
        # Left-aligned condensed display beside the microwave hero.
        boxes += [text(im,'Stop Cooking',67,y,'Impact.ttf',123,WHITE,650)]
        boxes += [text(im,'Your Meals',67,y+145,'Impact.ttf',144,(80,193,255),650)]
        ImageDraw.Draw(im).rectangle((70,y+316,330,y+325),fill=(80,193,255))
    for b in boxes:
        assert b[1] >= (240 if ig else 80),b
        assert b[3] <= (1620 if ig else 1810),b
        if subject:
            h = subject['hair_face_box']
            assert b[2] < h[0] or b[0] > h[2] or b[3] < h[1]-24 or b[1] > h[3]+24,(b,h)
    path = HERE / layout / f'{i}-meal-prep-cover.jpg'
    im = im.convert('RGB')
    im.save(path, quality=94, subsampling=0)
    assert path.stat().st_size < 2_000_000, path
    records.append({'option':i,'layout':layout,'file':str(path),'dimensions':[W,H],
                    'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'text_boxes':boxes,'subject':subject})
    im.resize((270,480),Image.Resampling.LANCZOS).save(HERE/'checks'/f'{i}-{layout}-phone.jpg',quality=94)
    return im


def main():
    finals = {(i,l):build(i,l) for i in range(1,6) for l in ['youtube','instagram']}
    sw = 1540
    sheet = Image.new('RGB',(sw,1110),(238,237,233))
    d = ImageDraw.Draw(sheet)
    d.text((24,18),'Meal Prep | Cover Choices',font=font('Manrope',33),fill=(14,26,33))
    d.text((24,66),'Top: YouTube full cover    Bottom: Instagram profile crop',font=font('Arial.ttf',22),fill=(65,75,79))
    labels = ['Real Pool Photo','Real Studio Photo','AI Dan','Prepared Meals','Microwave + Clock']
    for i in range(1,6):
        x = 24+(i-1)*303
        d.text((x,112),f'{i}. {labels[i-1]}',font=font('Arial Bold.ttf',20),fill=(14,26,33))
        sheet.paste(finals[i,'youtube'].resize((275,489),Image.Resampling.LANCZOS),(x,153))
        tile = finals[i,'instagram'].crop((0,240,W,1680)).resize((275,367),Image.Resampling.LANCZOS)
        sheet.paste(tile,(x,686))
    d.text((24,1072),'Same headline on all five. Pick 1, 2, 3, 4 or 5.',font=font('Arial.ttf',22),fill=(50,62,66))
    sheet.save(HERE/'REVIEW-meal-prep-five-covers.jpg',quality=95,subsampling=0)
    (HERE/'cover-manifest.json').write_text(json.dumps({'status':'awaiting-dan-pick','headline':'Stop Cooking Your Meals',
        'film_untouched':True,'generation':'Codex subscription, gpt-6.1-sol high',
        'outputs':records},indent=2)+'\n')


if __name__ == '__main__':
    main()
