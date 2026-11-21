"""SL-11 cover R3: #1 photo/composition locked; three top-text treatments only.
Pixel-check every row at/below the photo boundary against R2 Design 1. No generation.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
P=Path(__file__).resolve().parents[4];BASE=P/'Short-form video content/covers/review/sl11-vacuum-20261028';R=BASE/'round3';R.mkdir(exist_ok=True)
W,H=1080,1920;SUP=Path('/System/Library/Fonts/Supplemental')
SPEC={
'a':dict(title='How To Do A Standing Stomach Vacuum',intro='How To Do A Standing',hero='Stomach Vacuum',footer='',split=['How To Do A Standing','Stomach','Vacuum']),
'b':dict(title='Stop Holding Your Breath During Stomach Vacuums',intro='Stop Holding',hero='Your Breath',footer='During Stomach Vacuums',split=['Stop Holding','Your Breath','During Stomach Vacuums']),
'c':dict(title='Start With One 20-Second Vacuum Every Morning',intro='Start With One',hero='20-Second Vacuum',footer='Every Morning',split=['Start With One','20-Second','Vacuum Every Morning']),
}
FONTS={'condensed':('/System/Library/Fonts/Avenir Next Condensed.ttc',8),'manrope':(str(Path.home()/'Library/Fonts/Manrope.ttf'),0),'slab':(str(SUP/'Rockwell.ttc'),2),'medium':('/System/Library/Fonts/Avenir Next.ttc',5)}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(kind,size):
 p,i=FONTS[kind];f=ImageFont.truetype(p,size,index=i)
 if kind=='manrope':f.set_variation_by_name('ExtraBold')
 return f
def fit(txt,kind,start,width):
 for n in range(start,29,-1):
  f=font(kind,n)
  if f.getlength(txt)<=width:return f
 raise ValueError(txt)
def drawtext(im,mask,txt,x,y,kind,size,color,maxw=960,anchor='mt'):
 f=fit(txt,kind,size,maxw);d=ImageDraw.Draw(im);d.text((x,y),txt,font=f,fill=color,anchor=anchor);ImageDraw.Draw(mask).text((x,y),txt,font=f,fill=255,anchor=anchor)
 return dict(text=txt,font=kind,size=f.size,bbox=list(d.textbbox((x,y),txt,font=f,anchor=anchor)))
def gradient(end,c1,c2):
 a=np.zeros((end,W,3),np.uint8)
 for y in range(end):
  v=y/max(end-1,1);a[y,:,:]=[round(c1[i]*(1-v)+c2[i]*v) for i in range(3)]
 return Image.fromarray(a)
prior=json.loads((BASE/'round2/manifest.json').read_text())['outputs'];rows=[]
for key,spec in SPEC.items():
 for plat in ['instagram','youtube']:
  orig=next(x for x in prior if x['short']==key and x['design']==1 and x['platform']==plat);src=P/orig['path'];base=Image.open(src).convert('RGB');start=244 if plat=='instagram' else 58;end=600 if plat=='instagram' else 430
  for variant in [1,2,3]:
   im=base.copy();mask=Image.new('L',(W,H));b=[]
   if variant==1:
    # Midnight editorial: centered geometric hierarchy, champagne detail and generous spacing.
    im.paste(gradient(end,(5,14,29),(14,37,59)),(0,0));d=ImageDraw.Draw(im)
    d.line((68,start+8,238,start+8),fill='#CCAD70',width=3);d.line((842,start+8,1012,start+8),fill='#CCAD70',width=3)
    b.append(drawtext(im,mask,spec['intro'],540,start+29,'manrope',64,'#D8C18B',960))
    main_y=start+118 if spec['footer'] else start+127
    b.append(drawtext(im,mask,spec['hero'],540,main_y,'condensed',174,'#FFFFFF',970))
    if spec['footer']:b.append(drawtext(im,mask,spec['footer'],540,start+286,'medium',52,'#D8C18B',960))
    else:d.line((440,start+312,640,start+312),fill='#CCAD70',width=4)
    d.rectangle((0,end-7,W,end-1),fill='#CCAD70')
   elif variant==2:
    # Cobalt athletic: left aligned, a large key phrase, restrained yellow emphasis.
    im.paste(gradient(end,(15,46,109),(15,76,156)),(0,0));d=ImageDraw.Draw(im)
    d.polygon([(775,0),(985,0),(1080,end-1),(1068,end-1)],fill='#10458D')
    d.rectangle((38,start+24,47,start+322),fill='#F9D74A')
    l=spec['split']
    if key=='a':
     b.append(drawtext(im,mask,l[0],76,start+15,'manrope',56,'#CFDFF4',925,'lt'))
     b.append(drawtext(im,mask,l[1],76,start+92,'manrope',113,'#FFFFFF',925,'lt'))
     b.append(drawtext(im,mask,l[2],76,start+215,'manrope',121,'#FFE058',925,'lt'))
    elif key=='b':
     b.append(drawtext(im,mask,l[0],76,start+21,'manrope',77,'#CFDFF4',925,'lt'))
     b.append(drawtext(im,mask,l[1],76,start+125,'manrope',134,'#FFE058',925,'lt'))
     b.append(drawtext(im,mask,l[2],76,start+286,'medium',53,'#FFFFFF',925,'lt'))
    else:
     b.append(drawtext(im,mask,l[0],76,start+15,'manrope',61,'#CFDFF4',925,'lt'))
     b.append(drawtext(im,mask,l[1],76,start+95,'manrope',121,'#FFE058',925,'lt'))
     b.append(drawtext(im,mask,l[2],76,start+246,'manrope',76,'#FFFFFF',925,'lt'))
    d.rectangle((0,end-7,W,end-1),fill='#FFE058')
   else:
    # Bone & scarlet editorial: bold slab serif, right alignment and a precise inset border.
    im.paste(Image.new('RGB',(W,end),'#EAE5D9'),(0,0));d=ImageDraw.Draw(im)
    d.rectangle((25,start-5,W-26,end-18),outline='#B8AFA0',width=2)
    d.rectangle((51,start+15,59,start+305),fill='#B62E29')
    if key=='a':
     b.append(drawtext(im,mask,spec['intro'],1005,start+23,'medium',57,'#1B2B3A',910,'rt'))
     b.append(drawtext(im,mask,'Stomach',1005,start+107,'slab',125,'#1B2B3A',910,'rt'))
     b.append(drawtext(im,mask,'Vacuum',1005,start+224,'slab',131,'#B62E29',910,'rt'))
    elif key=='b':
     b.append(drawtext(im,mask,spec['intro'],1005,start+23,'medium',65,'#1B2B3A',910,'rt'))
     b.append(drawtext(im,mask,spec['hero'],1005,start+127,'slab',132,'#B62E29',910,'rt'))
     b.append(drawtext(im,mask,spec['footer'],1005,start+283,'medium',51,'#1B2B3A',910,'rt'))
    else:
     b.append(drawtext(im,mask,spec['intro'],1005,start+23,'medium',62,'#1B2B3A',910,'rt'))
     b.append(drawtext(im,mask,'20-Second',1005,start+111,'slab',130,'#B62E29',910,'rt'))
     b.append(drawtext(im,mask,'Vacuum Every Morning',1005,start+270,'medium',64,'#1B2B3A',910,'rt'))
    d.rectangle((0,end-7,W,end-1),fill='#B62E29')
   assert ' '.join(x['text'] for x in b)==spec['title'],b
   # Direction pick locks every photo pixel, not just a source filename or crop.
   assert np.array_equal(np.asarray(im)[end:],np.asarray(base)[end:])
   for x in b:
    x0,y0,x1,y1=x['bbox'];assert 25<=x0<x1<=1055 and (240 if plat=='instagram' else 50)<=y0<y1<=end-15,(key,plat,variant,x)
   p=R/key/plat/f'sl11-{key}-header-{variant}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);j=p.with_suffix('.jpg');im.save(j,quality=94);mask.save(p.with_name(p.stem+'-text-mask.png'));assert j.stat().st_size<2_000_000
   ph=R/key/'phone'/plat;ph.mkdir(parents=True,exist_ok=True);im.resize((270,480),Image.Resampling.LANCZOS).save(ph/j.name,quality=95)
   gr=R/key/'grid';gr.mkdir(exist_ok=True)
   if plat=='instagram':im.crop((0,240,W,1680)).resize((270,360),Image.Resampling.LANCZOS).save(gr/f'{variant}.jpg',quality=95)
   rows.append(dict(short=key,platform=plat,design=variant,path=str(p.relative_to(P)),sha256=sha(p),jpeg_path=str(j.relative_to(P)),jpeg_bytes=j.stat().st_size,jpeg_sha256=sha(j),text=b,base_path=orig['path'],base_sha256=sha(src),photo_start_y=end,all_photo_pixels_identical=True,all_words_preserved=True))
for key in SPEC:
 sh=Image.new('RGB',(1200,1490),'#152334');d=ImageDraw.Draw(sh)
 for row in [r for r in rows if r['short']==key]:
  x=(row['design']-1)*400;y=0 if row['platform']=='instagram' else 745
  d.text((x+15,y+16),f"{row['design']} / {row['platform'].title()}",font=font('manrope',25),fill='white');sh.paste(Image.open(P/row['path']).resize((378,672),Image.Resampling.LANCZOS),(x+11,y+60))
 sh.save(R/key/'three-header-choices.jpg',quality=96)
(R/'manifest.json').write_text(json.dumps({'round':3,'status':'awaiting exact header pick','date':'2026-10-29','scope':'Only the header above R2 Design 1. Photo pixels and original wording preserved.','outputs':rows},indent=2));print('Built',len(rows),'header layouts; exact photo pixels and wording preserved')
