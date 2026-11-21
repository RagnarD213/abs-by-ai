"""Design 1 cover revision: seamless curved callout, two lines, smaller reaction.
Reuses exact round-2 pixels; no new generation and no video changes.
"""
from pathlib import Path
import hashlib,json
import cv2,numpy as np
cv2.setNumThreads(1)
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageOps
P=Path(__file__).resolve().parents[4]
R=P/'Short-form video content/covers/review/ds40-codex-r5-20261025'
O=R/'round3';O.mkdir(exist_ok=True)
W,H=1080,1920
LINES=['Have you ever seen a','fat 90-year-old?']
QUOTE='Have you ever seen a fat 90-year-old?'
FONT='/System/Library/Fonts/Supplemental/Impact.ttf'

def bez(a,b,c,d,n=30):
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],(1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1]) for t in [i/n for i in range(n+1)]]

def build(platform):
    ig=platform=='instagram'
    source=Image.open(R/'round2/assets/maher-0.jpg').convert('RGB')
    cropw=450 if ig else 405;x=403 if ig else 425
    clip=source.crop((x,0,x+cropw,720)).resize((W,round(720*W/cropw)),Image.Resampling.LANCZOS)
    shift=25 # 75 px higher than R2, with the native speaker frame retained.
    im=ImageOps.fit(source,(W,H)).filter(ImageFilter.GaussianBlur(25))
    im.paste(clip.crop((0,0,W,1)).resize((W,shift)),(0,0));im.paste(clip,(0,shift));im=im.convert('RGBA')
    top=815 if ig else 900;bottom=top+230
    # A curved tapered tail and the body are unioned before outlining.
    # There is a single external contour and no line across their junction.
    scale=3
    mask=Image.new('L',(W*scale,H*scale));d=ImageDraw.Draw(mask)
    box=(55,top,1025,bottom)
    d.rounded_rectangle(tuple(round(v*scale) for v in box),radius=51*scale,fill=255)
    tip=(766,top-70)
    curve=bez((788,top+20),(823,top-3),(804,top-43),tip)
    curve+=bez(tip,(828,top-49),(880,top-26),(897,top+20))
    d.polygon([(round(x*scale),round(y*scale)) for x,y in curve],fill=255)
    outside=Image.fromarray(cv2.dilate(np.asarray(mask),np.ones((31,31),np.uint8)))
    border=Image.new('RGBA',mask.size,'#101820');border.putalpha(outside)
    inside=Image.new('RGBA',mask.size,'#fffdf6');inside.putalpha(mask);border.alpha_composite(inside)
    border=border.resize((W,H),Image.Resampling.LANCZOS);im.alpha_composite(border)
    font=ImageFont.truetype(FONT,90)
    d=ImageDraw.Draw(im)
    widths=[]
    for line,y in zip(LINES,[top+22,top+126]):
        width=font.getlength(line);assert width<910
        d.text((540,y),line,font=font,fill='#101820',anchor='mt');widths.append(width)
    fgpath=R/'round2/assets/foreground-1.png';fg=Image.open(fgpath).convert('RGBA');a=fg.getchannel('A');fg=fg.crop(a.getbbox())
    factor=min(895/fg.width,565/fg.height);fg=fg.resize((round(fg.width*factor),round(fg.height*factor)),Image.Resampling.LANCZOS)
    px=(W-fg.width)//2;py=1790-fg.height if ig else H-fg.height
    # Continue the exact wooden table texture to the frame edge, behind the cutout.
    table_y=py+fg.height-48
    table=fg.crop((0,fg.height-24,fg.width,fg.height)).resize((W,H-table_y))
    im.alpha_composite(table,(0,table_y))
    im.alpha_composite(fg,(px,py))
    path=O/platform;path.mkdir(exist_ok=True)
    jpg=path/'design-1-revised.jpg';png=path/'design-1-revised.png'
    im.convert('RGB').save(jpg,quality=95,optimize=True);im.convert('RGB').save(png)
    assert jpg.stat().st_size<2_000_000
    return {'platform':platform,'jpg':str(jpg),'png':str(png),'sha256':hashlib.sha256(jpg.read_bytes()).hexdigest(),'background_shift':shift,'background_shift_delta':-75,'bubble_body':box,'bubble_tail_tip':tip,'bubble_seam':'single union silhouette; external outline only','bubble_body_height':230,'previous_body_height':315 if ig else 320,'quote':QUOTE,'lines':LINES,'font_size':90,'line_widths':widths,'foreground_position':[px,py],'foreground_size':fg.size,'foreground_width_previous':1011,'foreground_size_reduction_approx':0.15,'generated_foreground_source_sha256':hashlib.sha256(fgpath.read_bytes()).hexdigest()}

def main():
    outputs=[build(p) for p in ('instagram','youtube')]
    (O/'manifest.json').write_text(json.dumps({'design':1,'cover_round':3,'approved':False,'outputs':outputs},indent=2)+'\n')
    sheet=Image.new('RGB',(1160,1110),'#101b2b');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',29)
    for i,p in enumerate(('instagram','youtube')):
        x=20+i*575;d.text((x,16),p.title(),font=font,fill='white');thumb=Image.open(O/p/'design-1-revised.jpg');thumb.thumbnail((540,960));sheet.paste(thumb,(x,65))
    d.text((25,1040),'Bill Maher: Design 1 revised | Cover round 3',font=font,fill='#72cdf7');sheet.save(O/'DESIGN-1-REVISED.jpg',quality=95)
    cards=''
    for p in ('instagram','youtube'):
        cards+=f'<figure><h2>{p.title()}</h2><a href="round3/{p}/design-1-revised.png"><img src="round3/{p}/design-1-revised.jpg" alt="Revised design 1 {p}"></a></figure>'
    (R/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bill Maher: Design 1 Revised</title><style>*{box-sizing:border-box}body{margin:0;background:#0c1421;color:#edf3fa;font:17px system-ui;padding:25px}h1{font-size:30px}p{max-width:1050px;color:#bdcce0}main{display:grid;grid-template-columns:repeat(2,minmax(200px,540px));gap:25px;justify-content:center}figure{margin:0;background:#162337;padding:15px;border-radius:14px}h2{font-size:22px;margin:0 0 12px}img{width:100%;display:block;border-radius:5px}a{color:#72cdf7}@media(max-width:500px){body{padding:12px}main{grid-template-columns:1fr}}</style><h1>Bill Maher: Design 1 Revised</h1><p>Seamless curved speech-bubble tail, exact question on two lines, shorter bubble, Bill Maher moved slightly higher with his face clear, and a smaller laptop reaction at the bottom.</p><p><strong>Approved video remains Codex R5, 1:04.86.</strong> This revised cover is ready for your review and has not been installed.</p><p><a href="round3/DESIGN-1-REVISED.jpg">Compare Instagram and YouTube layouts</a></p><main>'''+cards+'</main></html>')
    print('Built revised design 1:',O)

if __name__=='__main__':main()
