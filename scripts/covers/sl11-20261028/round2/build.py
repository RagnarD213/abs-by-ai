"""SL-11 cover R2: three real-screenshot designs per Short, two platform layouts.
Reuse existing touched-up real camera screenshots, no new image generation or film edits.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
import json,hashlib,shutil,subprocess,numpy as np
P=Path(__file__).resolve().parents[4]
BASE=P/'Short-form video content/covers/review/sl11-vacuum-20261028';R=BASE/'round2';S=R/'sources';S.mkdir(parents=True,exist_ok=True)
W,H=1080,1920;SUP=Path('/System/Library/Fonts/Supplemental');PM=Path.home()/'.cache/absbyai/personmask/personmask'
PH=P/'social media graphics/youtube/thumbnails/The Vacuum The Best Ab Exercise For Belly Fat/_build'
SRC={'front':PH/'codex-edit-A-front-smile.png','quarter':PH/'codex-edit-B-three-quarter.png'}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for k,p in SRC.items():
 dest=S/f'{k}-previously-touched-up.png'
 if not dest.exists():shutil.copy2(p,dest)
SRC={k:S/f'{k}-previously-touched-up.png' for k in SRC}
PHOTO={k:Image.open(p).convert('RGB') for k,p in SRC.items()}
CUT={}
for k,p in SRC.items():
 mask=S/f'{k}.mask.png'
 if not mask.exists():subprocess.run([str(PM),str(p),str(mask)],check=True,capture_output=True)
 a=Image.open(mask).convert('L').point(lambda q:255 if q>127 else 0);b=a.getbbox();a=a.filter(ImageFilter.GaussianBlur(.7));raw=PHOTO[k].convert('RGBA');raw.putalpha(a);CUT[k]=(raw.crop(b),b)
COPY={
 'a':{'title':'How To Do A Standing Stomach Vacuum','two':['How To Do A Standing','Stomach Vacuum'],'stack':['How To','Do A','Standing','Stomach','Vacuum'],'bottom':['How To Do A Standing','Stomach','Vacuum']},
 'b':{'title':'Stop Holding Your Breath During Stomach Vacuums','two':['Stop Holding Your Breath','During Stomach Vacuums'],'stack':['Stop Holding','Your Breath','During','Stomach','Vacuums'],'bottom':['Stop Holding Your Breath','During Stomach','Vacuums']},
 'c':{'title':'Start With One 20-Second Vacuum Every Morning','two':['Start With One 20-Second','Vacuum Every Morning'],'stack':['Start With','One 20-Second','Vacuum','Every','Morning'],'bottom':['Start With One','20-Second Vacuum','Every Morning']},
}

def font(name,size):return ImageFont.truetype(str(SUP/name),size)
def fit(txt,name,size,width):
 for n in range(size,25,-1):
  f=font(name,n)
  if f.getbbox(txt)[2]-f.getbbox(txt)[0]<=width:return f
 raise ValueError(txt)
def txt(im,mask,text,xy,f,color,anchor='mt',stroke=0):
 ImageDraw.Draw(im).text(xy,text,font=f,anchor=anchor,fill=color,stroke_width=stroke,stroke_fill='#091827')
 ImageDraw.Draw(mask).text(xy,text,font=f,anchor=anchor,fill=255,stroke_width=stroke)
 return list(ImageDraw.Draw(im).textbbox(xy,text,font=f,anchor=anchor,stroke_width=stroke))
def fill_photo(src,box,crop):
 x,y,x1,y1=box;im=ImageOps.fit(PHOTO[src].crop(crop),(x1-x,y1-y),method=Image.Resampling.LANCZOS,centering=(.5,.2));return im
rows=[]
for key,spec in COPY.items():
 for n in [1,2,3]:
  for plat in ['instagram','youtube']:
   ig=plat=='instagram';mask=Image.new('L',(W,H));im=Image.new('RGB',(W,H),'#0A2038');d=ImageDraw.Draw(im);bounds=[];meta={}
   if n==1:
    # Full-width yellow type above the reused smiling front vacuum, not over it.
    ty=260 if ig else 90;bottom=ty+310
    crop=(680,65,1490,930);box=(0,bottom+30,W,H)
    im.paste(fill_photo('front',box,crop),(box[0],box[1]));d=ImageDraw.Draw(im)
    d.rectangle((0,ty-20,W,bottom),fill='#FFDA20')
    picture=im.copy()
    for i,line in enumerate(spec['two']):
     f=fit(line,'DIN Condensed Bold.ttf',170,970)
     bounds.append(txt(im,mask,line,(540,ty+25+i*142),f,'#0B2033' if i==0 else '#B72B25'))
    meta={'source':'front','source_crop':list(crop),'photo_rect':list(box)}
   elif n==2:
    # Cream left editorial column; real three-quarter camera cutout on navy at right.
    im=Image.new('RGB',(W,H),'#0C2943');d=ImageDraw.Draw(im);d.rectangle((0,0,430,H),fill='#F4F0E5')
    # Real pool detail contains no person, keeping the right backdrop coherent and duplicate-free.
    bg=PHOTO['quarter'].crop((0,20,700,941));bg=ImageOps.fit(bg,(650,H),method=Image.Resampling.LANCZOS);im.paste(bg,(430,0))
    scrim=Image.new('RGBA',(650,H),(3,18,34,90));tmp=im.convert('RGBA');tmp.alpha_composite(scrim,(430,0));im=tmp
    raw,b=CUT['quarter'];height=1420;scale=height/raw.height;sub=raw.resize((round(raw.width*scale),height),Image.Resampling.LANCZOS)
    x=1120-sub.width;y=260 if ig else 250
    im.alpha_composite(sub,(x,y));im=im.convert('RGB');d=ImageDraw.Draw(im)
    top=390 if ig else 250;step=148
    d.rectangle((40,top-45,160,top-35),fill='#BE3029')
    picture=im.copy()
    for i,line in enumerate(spec['stack']):
     f=fit(line,'Impact.ttf',100 if key!='c' else 95,340)
     bounds.append(txt(im,mask,line,(42,top+i*step),f,'#B52C27' if i==len(spec['stack'])-1 else '#0B263F',anchor='lt'))
    band=1610 if ig else 1670
    d.rectangle((0,band,430,H),fill='#F4F0E5');d.rectangle((430,band,W,H),fill='#0C2943')
    d.rectangle((0,band,W,band+32),fill='#B92F29')
    meta={'source':'quarter','cutout_source_bbox':list(b),'person_rect':[x,y,x+sub.width,y+sub.height],'person_scale':scale}
   else:
    # Large real front photo on top, large bottom title in a clean navy/cyan graphic.
    im=Image.new('RGB',(W,H),'#07192D');d=ImageDraw.Draw(im)
    photo_top=240 if ig else 35;photo_bottom=1145 if ig else 1275
    crop=(610,45,1580,900);box=(0,photo_top,W,photo_bottom)
    im.paste(fill_photo('front',box,crop),(box[0],box[1]));d=ImageDraw.Draw(im)
    d.rectangle((0,photo_bottom,W,photo_bottom+10),fill='#4BDEEB')
    start=photo_bottom+35;limit=1610 if ig else 1820;lines=spec['bottom'];maxsizes=[130,180,215]
    fs=[fit(t,'Impact.ttf',sz,990) for t,sz in zip(lines,maxsizes)];heights=[f.getbbox(t,anchor='mt')[3] for t,f in zip(lines,fs)]
    total=sum(heights)+38
    if total>limit-start:
     scale=(limit-start-38)/sum(heights);fs=[fit(t,'Impact.ttf',round(f.size*scale),990) for t,f in zip(lines,fs)];heights=[f.getbbox(t,anchor='mt')[3] for t,f in zip(lines,fs)]
    picture=im.copy()
    yy=start
    for i,(line,f,hh) in enumerate(zip(lines,fs,heights)):
     bounds.append(txt(im,mask,line,(540,yy),f,'#4BDEEB' if i==2 else '#FFFFFF'));yy+=hh+19
    meta={'source':'front','source_crop':list(crop),'photo_rect':list(box)}
   # Save the exact picture layer without glyphs for independent body/face mask checks.
   # Text mask is separate; final crop measurements come from these exact files.
   out=R/key/plat;out.mkdir(parents=True,exist_ok=True);p=out/f'sl11-{key}-real-design-{n}.png'
   picture.convert('RGB').save(p.with_name(p.stem+'-picture.png'))
   im.convert('RGB').save(p);j=p.with_suffix('.jpg');im.convert('RGB').save(j,quality=94);mask.save(p.with_name(p.stem+'-text-mask.png'))
   assert j.stat().st_size<2_000_000
   assert all(25<=b[0]<b[2]<=1055 and (240 if ig else 50)<=b[1]<b[3]<=(1620 if ig else 1850) for b in bounds),bounds
   phone=R/key/'phone'/plat;phone.mkdir(parents=True,exist_ok=True);im.resize((270,480),Image.Resampling.LANCZOS).save(phone/j.name,quality=95)
   gr=R/key/'grid';gr.mkdir(exist_ok=True)
   if ig:im.crop((0,240,W,1680)).resize((270,360),Image.Resampling.LANCZOS).save(gr/f'{n}.jpg',quality=95)
   rows.append(dict(short=key,design=n,platform=plat,path=str(p.relative_to(P)),sha256=sha(p),jpeg_path=str(j.relative_to(P)),jpeg_sha256=sha(j),jpeg_bytes=j.stat().st_size,text_bounds=bounds,title=spec['title'],source_path=str(SRC[meta['source']].relative_to(P)),source_sha256=sha(SRC[meta['source']]),new_image_generation=False,**meta))
(R/'manifest.json').write_text(json.dumps({'round':2,'date':'2026-10-29','status':'awaiting Dan exact picks','source_note':'Reused prior enhanced REAL C1677 screenshots from the RO-02 thumbnail build. Source retouch was already applied in October; no new AI scene or retouch generation in this round.','outputs':rows},indent=2))
for key in COPY:
 sheet=Image.new('RGB',(1200,1490),'#152334');d=ImageDraw.Draw(sheet)
 for row in [q for q in rows if q['short']==key]:
  x=(row['design']-1)*400;y=0 if row['platform']=='instagram' else 745
  d.text((x+15,y+16),f"{row['design']} / {row['platform'].title()}",font=font('Arial Bold.ttf',25),fill='white');sheet.paste(Image.open(P/row['path']).resize((378,672),Image.Resampling.LANCZOS),(x+11,y+60))
 sheet.save(R/key/'three-real-cover-choices.jpg',quality=96)
print('Built',len(rows),'real cover layouts',flush=True)
