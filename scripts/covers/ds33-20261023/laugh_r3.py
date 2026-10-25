"""Option 3 expression revision; preserve original covers and film."""
from pathlib import Path
import json, hashlib
import build as b
from PIL import Image, ImageOps, ImageDraw

R=b.R
def main():
    out=R/'option-3-laugh-r3';out.mkdir(exist_ok=True)
    outputs=[]
    for platform in ('instagram','youtube'):
        ig=platform=='instagram'
        im=ImageOps.fit(Image.open(R/'assets/plate-3-laugh-r3.png').convert('RGB'),(b.W,b.H),method=Image.Resampling.LANCZOS).convert('RGBA')
        if ig:
            shifted=Image.new('RGBA',(b.W,b.H),im.getpixel((b.W//2,0)))
            shifted.alpha_composite(im.crop((0,0,b.W,b.H-100)),(0,100));im=shifted
        b.ramp(im,100,720,180)
        im.convert('RGB').save(out/f'{platform}.picture.jpg',quality=95)
        mask=Image.new('L',(b.W,b.H));y=280 if ig else 100
        b.text(im,mask,b.COPY[0],(540,y),'serif',105,'#fff8ed',950,'mt')
        b.rect(im,mask,(70,y+116,1010,y+251),'#be302c')
        b.text(im,mask,b.COPY[1],(540,y+134),'serif',109,'#fff8ed',880,'mt')
        p=out/f'{platform}.png';im.convert('RGB').save(p)
        im.convert('RGB').save(out/f'{platform}.jpg',quality=94,optimize=True)
        mask.save(out/f'{platform}.text-mask.png')
        outputs.append({'platform':platform,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text_bbox':mask.getbbox()})
    sheet=Image.new('RGB',(1160,1110),'#101b2b');d=ImageDraw.Draw(sheet)
    d.text((30,20),'Cover 3 revised: harder laugh, eyes open',font=b.ft('arial',35),fill='white')
    for i,platform in enumerate(('instagram','youtube')):
        d.text((30+580*i,80),platform.title(),font=b.ft('arial',27),fill='#65d7ff')
        im=Image.open(out/f'{platform}.png');im.thumbnail((540,960));sheet.paste(im,(20+580*i,130))
    sheet.save(out/'REVIEW.jpg',quality=95)
    (out/'manifest.json').write_text(json.dumps({'picked':3,'revision':3,'request':"Laughing harder, head slightly tilted back, eyes slightly open rather than squinted shut",'state':'awaiting exact revised cover approval','outputs':outputs},indent=2))
    old=R/'index.html'
    if not (R/'original-five.html').exists():(R/'original-five.html').write_bytes(old.read_bytes())
    old.write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ronaldo Ab Belt: Cover 3, Expression R3</title><style>body{background:#0c1421;color:#edf3fa;font:18px system-ui;margin:28px}h1{font-size:30px}p{max-width:1000px;color:#bdcce0}.pair{display:flex;gap:24px;max-width:1160px}figure{width:50%;margin:0}img{width:100%;display:block}figcaption{padding:12px 0;font-weight:600}a{color:#65d7ff}@media(max-width:600px){body{margin:14px}.pair{gap:12px}}</style><h1>Ronaldo Ab Belt: Cover 3, Expression R3</h1><p>Tilted your head slightly back and opened your eyes a little while keeping a harder laugh. The copy, design and approved R5 film are preserved. Review both layouts below and approve this revision before installation or scheduling.</p><div class="pair"><figure><figcaption>Instagram</figcaption><a href="option-3-laugh-r3/instagram.png"><img src="option-3-laugh-r3/instagram.jpg" alt="Revised Instagram cover: Dan laughing harder with eyes slightly open"></a></figure><figure><figcaption>YouTube</figcaption><a href="option-3-laugh-r3/youtube.png"><img src="option-3-laugh-r3/youtube.jpg" alt="Revised YouTube cover: Dan laughing harder with eyes slightly open"></a></figure></div><p><a href="option-3-laugh-r3/REVIEW.jpg">Open both on one sheet</a> · <a href="original-five.html">Original five choices</a></p></html>''')
    print(out)

if __name__=='__main__':main()
