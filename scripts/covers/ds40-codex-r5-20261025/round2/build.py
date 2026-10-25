"""Two Dan-requested reaction covers, real Maher frame plus AI foregrounds.
Only the AI foreground is generated. Speech bubble type is set deterministically.
"""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
P=Path(__file__).resolve().parents[4]
R=P/'Short-form video content/covers/review/ds40-codex-r5-20261025'
OUT=R/'round2'
W,H=1080,1920
FONT='/System/Library/Fonts/Supplemental/Arial Black.ttf'
FONT2='/System/Library/Fonts/Supplemental/Impact.ttf'
QUOTE='Have you ever seen a fat 90-year-old?'

def background(n,ig=False):
    src=Image.open(OUT/'assets'/f'maher-{0 if n==1 else 2}.jpg').convert('RGB')
    # Vertical native crop: speaker fills the entire canvas, no inset frame.
    x=425 if n==1 else 410
    cropw=450 if ig else 405
    if ig: x-=22
    im=src.crop((x,0,x+cropw,720)).resize((W,round(720*W/cropw)),Image.Resampling.LANCZOS)
    # Retain complete hair inside the Instagram grid's crop as well.
    shift=100
    upper=im.crop((0,0,W,1)).resize((W,shift))
    dst=ImageOps.fit(src,(W,H)).filter(ImageFilter.GaussianBlur(25));dst.paste(upper,(0,0));dst.paste(im,(0,shift))
    return dst.convert('RGBA')

def bubble(im,n,ig=False):
    lay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(lay)
    if n==1:
        box=(52,795 if ig else 915,1028,1110 if ig else 1235);tip=(620,750 if ig else 840);fill='#fffdf6';ink='#101820';font=FONT2;size=94;ys=[box[1]+23,box[1]+121,box[1]+219]
        d.polygon([(565,box[1]+20),(tip),(735,box[1]+20)],fill=fill,outline=ink,width=7)
        d.rounded_rectangle(box,radius=68,fill=fill,outline=ink,width=7)
    else:
        box=(54,795 if ig else 915,1026,1110 if ig else 1235);tip=(615,755 if ig else 845);fill='#ffe66e';ink='#101820';font=FONT;size=84;ys=[box[1]+28,box[1]+126,box[1]+224]
        d.polygon([(470,box[1]+25),tip,(705,box[1]+25)],fill=fill,outline=ink,width=9)
        d.rounded_rectangle(box,radius=32,fill=fill,outline=ink,width=9)
    lines=['Have you ever','seen a fat','90-year-old?']
    f=ImageFont.truetype(font,size)
    for text,y in zip(lines,ys):
        assert d.textbbox((0,0),text,font=f)[2]<900
        d.text((540,y),text,font=f,fill=ink,anchor='mt')
    im.alpha_composite(lay)
    return {'box':box,'tip':tip,'text':QUOTE,'lines':lines,'font':font,'size':size}

def foreground(im,n,ig=False):
    src=OUT/'assets'/f'foreground-{n}.png';fg=Image.open(src).convert('RGBA')
    a=fg.getchannel('A');assert a.getextrema()[0]==0,'Generated foreground is not transparent'
    box=a.getbbox();assert box
    fg=fg.crop(box)
    maxh=H-1255
    factor=min(1050/fg.width,maxh/fg.height)
    fg=fg.resize((round(fg.width*factor),round(fg.height*factor)),Image.Resampling.LANCZOS)
    x=(W-fg.width)//2;y=1125 if ig else H-fg.height
    if ig:
        # Continue the wooden tabletop down to the canvas edge, keeping the
        # laptop's upper half visible inside Instagram's center grid crop.
        table=fg.crop((0,fg.height-24,fg.width,fg.height)).resize((W,H-y-fg.height+25))
        im.alpha_composite(table,(0,y+fg.height-1))
    # A subtle dark shadow separates reaction figures from the native clip.
    im.alpha_composite(fg,(x,y))
    return {'source':str(src),'native_alpha_crop':box,'position':[x,y],'size':fg.size,'transparent':True}

def main():
    manifest=[]
    for n in (1,2):
        for platform in ('instagram','youtube'):
            ig=platform=='instagram'
            im=background(n,ig);b=bubble(im,n,ig);f=foreground(im,n,ig)
            out=OUT/platform;out.mkdir(exist_ok=True)
            dest=out/f'design-{n}.jpg';im.convert('RGB').save(dest,quality=95,optimize=True)
            png=out/f'design-{n}.png';im.convert('RGB').save(png)
            assert dest.stat().st_size<2_000_000
            manifest.append({'design':n,'platform':platform,'jpg':str(dest),'png':str(png),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'speech_bubble':b,'foreground':f,'background_source':'Bill Maher original clip, New Rule: Fat Acceptance','size':[W,H]})
    (OUT/'manifest.json').write_text(json.dumps({'quote':QUOTE,'outputs':manifest},indent=2)+'\n')
    sheet=Image.new('RGB',(1160,1110),'#101b2b');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',29)
    for n in (1,2):
        x=20+(n-1)*575;d.text((x,16),f'Design {n}',font=font,fill='white')
        thumb=Image.open(OUT/'youtube'/f'design-{n}.jpg');thumb.thumbnail((540,960));sheet.paste(thumb,(x,65))
    d.text((25,1040),'Bill Maher: Fat 90-Year-Old | Cover round 2',font=font,fill='#72cdf7');sheet.save(OUT/'TWO-DESIGNS.jpg',quality=95)
    cards=''
    for n in (1,2):
        cards+=f'<article><h2>Design {n}</h2><div class="pair">'
        for platform in ('instagram','youtube'):
            cards+=f'<figure><a href="round2/{platform}/design-{n}.png"><img src="round2/{platform}/design-{n}.jpg" alt="Design {n} {platform}: Bill Maher and shocked laptop reaction"></a><figcaption>{platform.title()}</figcaption></figure>'
        cards+='</div></article>'
    (R/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bill Maher: Two New Cover Designs</title><style>*{box-sizing:border-box}body{margin:0;background:#0c1421;color:#edf3fa;font:17px system-ui;padding:25px}h1{font-size:30px}p{max-width:1050px;color:#bdcce0}main{display:grid;grid-template-columns:repeat(2,minmax(250px,540px));gap:25px;justify-content:center}article{background:#162337;padding:15px;border-radius:14px}h2{font-size:22px;margin:0 0 12px}img{width:100%;display:block;border-radius:5px}a{color:#72cdf7}.pair{display:flex;gap:12px}figure{margin:0;width:50%}figcaption{text-align:center;padding-top:8px}@media(max-width:650px){body{padding:12px}main{grid-template-columns:1fr}}</style><h1>Bill Maher: Two New Cover Designs</h1><p>Your requested concept: full-screen Bill Maher behind you, his question in a speech bubble, and AI shirtless Dan beside an overweight older man in a shirt, both shocked while watching the laptop.</p><p><strong>Approved film remains Codex R5, 1:04.86.</strong> These are cover images only. Each design includes Instagram and YouTube layouts; the Instagram reaction is raised to keep both faces and the laptop visible in the grid. Neither design is approved or installed.</p><p><a href="round2/TWO-DESIGNS.jpg">Compare both designs on one sheet</a></p><main>'''+cards+'</main></html>')
    print('Built two cover concepts:',OUT)

if __name__=='__main__':main()
