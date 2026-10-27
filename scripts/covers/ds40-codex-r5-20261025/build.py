"""Five distinct DS-40 Codex R5 covers. Real portraits remain unmodified cutout pixels.
Generated plates: built-in Codex subscription imagegen; copy is rendered here.
Adapted from the shared SL-18 cover builder's font, fit, and text-mask methods.
"""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

P=Path(__file__).resolve().parents[3]
R=P/'Short-form video content/covers/review/ds40-codex-r5-20261025'
W,H=1080,1920
SUP='/System/Library/Fonts/Supplemental/'
FONTS={'impact':SUP+'Impact.ttf','din':SUP+'DIN Condensed Bold.ttf',
       'serif':SUP+'Georgia Bold.ttf','arial':SUP+'Arial Bold.ttf',
       'futura':SUP+'Futura.ttc','black':SUP+'Arial Black.ttf'}
COPY=['A Fat','90-Year-Old?']
NAMES=['Sunlit pool','Studio editorial','Dan at 90','Birthday question','Time and strength']

def ft(kind,size):return ImageFont.truetype(FONTS[kind],size)
def fit(kind,text,size,width):
    while ft(kind,size).getlength(text)>width:size-=1
    return ft(kind,size)
def text(im,mask,txt,xy,kind,size,fill,maxw=960,anchor='lt',stroke=0):
    f=fit(kind,txt,size,maxw)
    for target,color in ((im,fill),(mask,255)):
        ImageDraw.Draw(target).text(xy,txt,font=f,fill=color,anchor=anchor,
            stroke_width=stroke,stroke_fill=(8,16,26) if target is im else 255)
def rect(im,mask,box,fill):
    ImageDraw.Draw(im).rectangle(box,fill=fill)
    ImageDraw.Draw(mask).rectangle(box,fill=255)
def ramp(im,start,end,alpha,top=True):
    a=np.zeros((H,W,4),dtype=np.uint8);a[:,:,:3]=(3,9,20)
    t=np.clip((end-np.arange(H))/(end-start) if top else (np.arange(H)-start)/(end-start),0,1)
    a[:,:,3]=(t[:,None]*alpha).astype(np.uint8)
    im.alpha_composite(Image.fromarray(a))
def portrait(im,name,box,xy,height,outline=0):
    p=P/'photos/finalized social media photos/_cutouts'/(name+'_CUTOUT.png')
    photo=Image.open(p).convert('RGBA').crop(box)
    photo=photo.resize((round(photo.width*height/photo.height),height),Image.Resampling.LANCZOS)
    if outline:
        alpha=photo.getchannel('A').filter(ImageFilter.MaxFilter(outline*2+1))
        white=Image.new('RGBA',photo.size,'white');white.putalpha(alpha);im.alpha_composite(white,xy)
    im.alpha_composite(photo,xy)
    return {'path':str(p),'crop':box,'position':xy,'rendered_size':photo.size}

def build():
    outputs=[]
    for n in range(1,6):
        src=R/'assets'/f'plate-{n}.png'
        if not src.exists(): continue
        for platform in ('instagram','youtube'):
            ig=platform=='instagram'
            im=ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
            source=None
            if n==1:
                ramp(im,200,700,200)
                source=portrait(im,'photo-247',(334,492,2060,3400),(285,685 if ig else 525),1100,4)
            if n==2:
                source=portrait(im,'studio-white-23',(162,239,2581,4300),(100,375 if ig else 225),945 if ig else 1095,0)
            if n==3:ramp(im,220,700,160)
            if n==4:ramp(im,1170,1590,185,False)
            if n==5:ramp(im,1150,1550,100,False)
            picture=im.copy().convert('RGB');mask=Image.new('L',(W,H))
            if n==1:
                y=285 if ig else 100
                text(im,mask,'BILL MAHER ASKS',(65,y),'arial',37,'#ecf3e4',920)
                text(im,mask,COPY[0],(60,y+65),'impact',175,'white',950,stroke=2)
                text(im,mask,COPY[1],(60,y+240),'impact',133,'#ffdc6a',950,stroke=2)
            elif n==2:
                y=1330 if ig else 1395
                rect(im,mask,(60,y-25,1020,y-20),'#12283a')
                text(im,mask,COPY[0],(64,y),'din',155,'#12283a',950)
                text(im,mask,COPY[1],(64,y+145),'din',178,'#12283a',950)
                text(im,mask,'BILL MAHER ASKS',(60,275 if ig else 100),'arial',35,'#12283a',900)
            elif n==3:
                y=285 if ig else 110
                text(im,mask,'BILL MAHER ASKS',(540,y),'arial',35,'#7fc7f8',950,'mt')
                text(im,mask,COPY[0],(540,y+65),'serif',145,'#fff8ed',950,'mt')
                text(im,mask,COPY[1],(540,y+220),'serif',128,'#fff8ed',950,'mt')
            elif n==4:
                y=1340 if ig else 1435
                text(im,mask,COPY[0],(540,y),'futura',145,'#ffe2ae',950,'mt')
                text(im,mask,COPY[1],(540,y+140),'futura',122,'#fff6e1',950,'mt')
                text(im,mask,'BILL MAHER ASKS',(540,y-50),'arial',34,'#fff6e1',950,'mt')
            else:
                y=1325 if ig else 1420
                rect(im,mask,(55,y-32,72,y+245),'#ff753c')
                text(im,mask,COPY[0],(106,y),'black',132,'#fffdf6',910)
                text(im,mask,COPY[1],(105,y+143),'black',106,'#fffdf6',910)
                text(im,mask,'BILL MAHER ASKS',(105,y-70),'arial',34,'#fffdf6',900)
            out=R/platform;out.mkdir(exist_ok=True)
            path=out/f'option-{n}.png';im.convert('RGB').save(path)
            picture.save(out/f'option-{n}.picture.jpg',quality=95);mask.save(out/f'option-{n}.text-mask.png')
            jpg=out/f'option-{n}.jpg';im.convert('RGB').save(jpg,quality=94,optimize=True)
            bbox=mask.getbbox();assert bbox[0]>=0 and bbox[2]<=W
            assert (bbox[1]>=240 and bbox[3]<=1660) if ig else bbox[1]>=48 and bbox[3]<=1780
            assert jpg.stat().st_size<2_000_000
            outputs.append({'number':n,'name':NAMES[n-1],'platform':platform,'path':str(path),'jpeg':str(jpg),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_plate':str(src),'real_portrait':source,'text_bbox':bbox})
    (R/'manifest.json').write_text(json.dumps({'copy':COPY,'outputs':outputs},indent=2))
    if len(outputs)!=10:
        print('Built partial set',len(outputs));return
    sheet=Image.new('RGB',(2800,650),'#101b2b');d=ImageDraw.Draw(sheet)
    d.text((30,15),'Bill Maher: Fat 90-Year-Old | Codex R5 | Choose 1 to 5',font=ft('arial',30),fill='white')
    for n in range(1,6):
        x=(n-1)*560;d.text((x+20,65),f'{n}. {NAMES[n-1]}',font=ft('arial',24),fill='#65d7ff')
        for j,platform in enumerate(('instagram','youtube')):
            im=Image.open(R/platform/f'option-{n}.png');im.thumbnail((260,463));sheet.paste(im,(x+10+j*275,130))
            d.text((x+20+j*275,103),'Instagram' if j==0 else 'YouTube',font=ft('arial',17),fill='white')
        d.text((x+20,610),'Real photo' if n<3 else 'AI image',font=ft('arial',18),fill='#acbbce')
    sheet.save(R/'NUMBERED-REVIEW.jpg',quality=95)
    cards=''
    for n in range(1,6):
        cards+=f'<article><h2>{n}. {NAMES[n-1]}</h2><div class="pair">'
        for p in ('instagram','youtube'):
            cards+=f'<figure><a href="{p}/option-{n}.png"><img src="{p}/option-{n}.jpg" alt="Option {n} {p}"></a><figcaption>{p.title()}</figcaption></figure>'
        cards+='</div></article>'
    (R/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fat 90-Year-Old: Cover Choices</title><style>*{box-sizing:border-box}body{margin:0;background:#0c1421;color:#edf3fa;font:17px system-ui;padding:28px}h1{font-size:30px}p{max-width:950px;color:#bdcce0}.sheet{width:100%;border-radius:10px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:24px}article{background:#162337;padding:18px;border-radius:14px}h2{font-size:21px;margin:0 0 15px}.pair{display:flex;gap:12px}figure{width:50%;margin:0}figure img{width:100%;display:block;border-radius:5px}figcaption{text-align:center;padding:8px;color:#b7c9df}a{color:#65d7ff}@media(max-width:500px){body{padding:14px}main{grid-template-columns:1fr}}</style><h1>Bill Maher: Fat 90-Year-Old</h1><p><strong>Selected film: Codex R5, approved by Dan, 1:04.86.</strong> This setup uses the exact Codex master selected in your screenshot.</p><p>Choose one cover number. Both Instagram and YouTube layouts are shown. Options 1 and 2 use real photos; option 3 is an imagined AI version of Dan at 90; options 4 and 5 are AI concepts. The approved video has not changed. Social uploads and scheduling wait for your cover pick.</p><p><a href="NUMBERED-REVIEW.jpg">Open all five on one sheet</a></p><a href="NUMBERED-REVIEW.jpg"><img class="sheet" src="NUMBERED-REVIEW.jpg" alt="All five numbered covers"></a><main>'''+cards+'</main></html>')
    print('Built 10 covers and one sheet:',R)

if __name__=='__main__':build()
