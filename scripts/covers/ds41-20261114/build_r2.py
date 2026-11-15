"""Dan's requested four covers: real horizontal podcast above Dan + junk food."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json,hashlib,numpy as np
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup/r2')
O=P/'designed';O.mkdir(exist_ok=True)
F='/System/Library/Fonts/Supplemental/Impact.ttf'
S='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
selection=json.loads((P/'src/selected-top.json').read_text())
source=Image.open(selection['file']).convert('RGB')
assert source.size==(1920,1080)
rows=[]
for key,path,body in [('a',P/'codex/ripped.png','ripped'),('b',P/'codex/fat.png','fat'),('c',P/'google/ripped.jpg','ripped'),('d',P/'google/fat.jpg','fat')]:
 plate=Image.open(path).convert('RGB')
 for platform in ['Instagram','YouTube']:
    im=Image.new('RGB',(1080,1920),'#23131b')
    top_y=240 if platform=='Instagram' else 0
    top_x=156 if platform=='Instagram' else 0
    top_w,top_h=(768,432) if platform=='Instagram' else (1080,608)
    top=source.resize((top_w,top_h),Image.Resampling.LANCZOS)
    band_y=top_y+top_h;photo_y=880 if platform=='Instagram' else 912
    im.paste(top,(top_x,top_y))
    d=ImageDraw.Draw(im);d.rectangle((0,band_y,1080,photo_y),fill='#ffda20')
    boxes=[]
    # Podcast name sits over lower-left curtain/microphone, not a head.
    small=ImageFont.truetype(S,38);name='Kevin James'
    namepos=(top_x+24,top_y+top_h-60)
    b=d.textbbox(namepos,name,font=small,stroke_width=2)
    d.text(namepos,name,font=small,fill='white',stroke_width=2,stroke_fill='#16131a')
    boxes.append({'text':name,'box':list(b),'font_size':38})
    for txt,y,maxsize in [('One Cheat Day',band_y+12 if platform=='Instagram' else band_y+23,100 if platform=='Instagram' else 126),('Wrecked His Diet',band_y+110 if platform=='Instagram' else band_y+165,100 if platform=='Instagram' else 122)]:
      for size in range(maxsize,50,-1):
        f=ImageFont.truetype(F,size)
        if d.textlength(txt,font=f)<=986:break
      bb=d.textbbox((0,0),txt,font=f);x=round((1080-d.textlength(txt,font=f))/2)
      pos=(x,round(y-bb[1]));d.text(pos,txt,font=f,fill='#161616')
      box=d.textbbox(pos,txt,font=f);assert box[3]<photo_y-7
      boxes.append({'text':txt,'box':list(box),'font_size':size})
    # Keep the source's complete height; only modest side scenery/arms crop for YT.
    lower_h=810 if platform=='Instagram' else 1920-photo_y
    lower=ImageOps.fit(plate,(1080,lower_h),Image.Resampling.LANCZOS,centering=(.5,.5))
    im.paste(lower,(0,photo_y))
    f=O/f'{key}-{platform}.png';im.save(f)
    jpg=f.with_suffix('.jpg');im.save(jpg,quality=94,subsampling=0)
    assert jpg.stat().st_size<2_000_000
    assert all(q['box'][1]>=(240 if platform=='Instagram' else 0) and q['box'][3]<1620 for q in boxes)
    # Only the local name caption may differ from the real resized podcast pixels.
    delta=np.any(np.asarray(im.crop((top_x,top_y,top_x+top_w,top_y+top_h)))!=np.asarray(top),axis=2)
    allowed=np.zeros((top_h,top_w),bool)
    nb=boxes[0]['box'];allowed[max(0,nb[1]-top_y):min(top_h,nb[3]-top_y+1),nb[0]-top_x:nb[2]-top_x+1]=True
    assert not np.any(delta & ~allowed)
    mask=Image.new('L',(1080,1920));md=ImageDraw.Draw(mask)
    for q in boxes:md.rectangle(q['box'],fill=255)
    mask.save(O/f'{key}-{platform}-textmask.png')
    if platform=='Instagram':im.crop((0,240,1080,1680)).save(O/f'{key}-Grid.jpg',quality=94)
    rows.append({'concept':key,'platform':platform,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'jpg':str(jpg),'jpg_bytes':jpg.stat().st_size,'body':body,'text':boxes,'podcast_bounds':[top_x,top_y,top_x+top_w,top_y+top_h],'photo_top':photo_y,'photo_bottom':photo_y+lower_h,'plate':str(path),'podcast_real_pixels_resized_only':True,'source_sha256':hashlib.sha256(Path(selection['file']).read_bytes()).hexdigest()})
(P/'layout-manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
sheet=Image.new('RGB',(2160,780),'#152031');d=ImageDraw.Draw(sheet)
for i,k in enumerate('abcd'):
 for j,platform in enumerate(['Instagram','YouTube']):
    im=Image.open(O/f'{k}-{platform}.png').resize((210,373));sheet.paste(im,(i*540+j*218,40));d.text((i*540+j*218,12),k+' '+platform,fill='white')
 im=Image.open(O/f'{k}-Grid.jpg').resize((240,320));sheet.paste(im,(i*540,440))
sheet.save(P/'private-layout-sheet.jpg',quality=96)
print('Built four requested choices in both layouts; real podcast pixels preserved.')
