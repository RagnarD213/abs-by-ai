"""Append X5-X8 without changing or reshuffling existing R2 choices."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np,copy,shutil
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup/r2')
O=P/'split/designed';O.mkdir(parents=True,exist_ok=True)
oldmap=json.loads((P/'neutral-install-map.json').read_text())
base={k:v for k,v in oldmap.items() if k in ['X1','X2','X3','X4']}
key=json.loads((P/'comparison/.blind-key.json').read_text())
rows=json.loads((P/'layout-manifest.json').read_text())
joe=Image.open(P/'src/joe-83.9.png').convert('RGB')
kevin=Image.open(P/'src/kevin-59.2.png').convert('RGB')
# Only side scenery is cropped. Both sources keep all1080 native rows; no mirror.
crops={'Joe Rogan':[540,0,1500,1080],'Kevin James':[450,0,1410,1080]}
sources={'Joe Rogan':joe,'Kevin James':kevin}
S='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
manifest=[];extra={};expanded=copy.deepcopy(key)
E=P/'comparison-expanded';(E/'originals').mkdir(parents=True,exist_ok=True)
for n in range(1,5):
 prior=f'X{n}';label=f'X{n+4}';extra[label]={}
 for platform in ['Instagram','YouTube']:
    source_path=Path(base[prior][platform]['original'])
    original=Image.open(source_path).convert('RGB');im=original.copy()
    r=next(q for q in rows if q['file']==str(source_path))
    x,y,x1,y1=r['podcast_bounds'];w,h=x1-x,y1-y;half=w//2
    panel=Image.new('RGB',(w,h))
    panel.paste(joe.crop(crops['Joe Rogan']).resize((half,h),Image.Resampling.LANCZOS),(0,0))
    panel.paste(kevin.crop(crops['Kevin James']).resize((w-half,h),Image.Resampling.LANCZOS),(half,0))
    d=ImageDraw.Draw(panel);d.line((half,0,half,h),fill='#fff0cb',width=2)
    font=ImageFont.truetype(S,38);name='Joe Rogan | Kevin James'
    tx=round((w-d.textlength(name,font=font))/2);ty=h-59
    box=d.textbbox((tx,ty),name,font=font,stroke_width=2)
    assert box[0]>=8 and box[2]<=w-8
    d.text((tx,ty),name,font=font,fill='white',stroke_width=2,stroke_fill='#17141a')
    im.paste(panel,(x,y))
    mask=np.zeros((1920,1080),bool);mask[y:y1,x:x1]=True
    assert np.array_equal(np.asarray(im)[~mask],np.asarray(original)[~mask])
    f=O/f'{label}-{platform}.png';im.save(f)
    jpg=f.with_suffix('.jpg');im.save(jpg,quality=94,subsampling=0)
    assert jpg.stat().st_size<2_000_000
    if platform=='Instagram':im.crop((0,240,1080,1680)).save(O/f'{label}-Grid.jpg',quality=94)
    digest=hashlib.sha256(f.read_bytes()).hexdigest()
    extra[label][platform]={'original':str(f),'sha256':digest,'same_lower_image_as':prior}
    manifest.append({'label':label,'platform':platform,'same_lower_image_as':prior,'file':str(f),'sha256':digest,'base_original':str(source_path),'base_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),'unchanged_outside_top_panel':True,'podcast_bounds':[x,y,x1,y1],'source_crops':crops,'source_order':['Joe Rogan','Kevin James'],'mirrored':False,'source_label':name,'name_bounds':[x+box[0],y+box[1],x+box[2],y+box[3]],'divider_x':x+half,'jpg_bytes':jpg.stat().st_size,'headline':r['text'][1:],'photo_top':r['photo_top']})
 # New label inherits the blind lower-image source without changing the old key.
 original=E/'originals'/f'{label}.png';shutil.copy2(Path(extra[label]['Instagram']['original']),original)
 entry=copy.deepcopy(key['labels'][prior]);entry.update({'original':str(original),'sha':hashlib.sha256(original.read_bytes()).hexdigest()[:12],'note':f'Split two-real-frame variant of {prior}','same_lower_image_as':prior})
 expanded['labels'][label]=entry
(E/'.blind-key.json').write_text(json.dumps(expanded,indent=1)+'\n')
(P/'split/neutral-install-map.json').write_text(json.dumps(extra,indent=2)+'\n')
(P/'split/layout-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Existing entries stay byte-equivalent in meaning; files remain untouched.
combined=copy.deepcopy(base);combined.update(extra)
(P/'neutral-install-map.json').write_text(json.dumps(combined,indent=2)+'\n')
proof={'Joe Rogan':{'file':str(P/'src/joe-83.9.png'),'time':83.9,'crop':crops['Joe Rogan']},'Kevin James':{'file':str(P/'src/kevin-59.2.png'),'time':59.2,'crop':crops['Kevin James']},'two_separate_real_frames':True,'no_generated_pixels':True,'no_mirroring':True,'layout':'Joe left facing right, Kevin right facing left','old_key_unchanged':True,'new_pick_key':str(E/'.blind-key.json')}
for v in [proof['Joe Rogan'],proof['Kevin James']]:v['sha256']=hashlib.sha256(Path(v['file']).read_bytes()).hexdigest()
(P/'split/source-provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
sheet=Image.new('RGB',(1440,710),'#142031');d=ImageDraw.Draw(sheet)
for i,label in enumerate(['X5','X6','X7','X8']):
 for j,platform in enumerate(['Instagram','YouTube']):
    im=Image.open(O/f'{label}-{platform}.png').resize((170,302));sheet.paste(im,(i*360+j*178,34));d.text((i*360+j*178+2,6),label+' '+platform,fill='white')
 im=Image.open(O/f'{label}-Grid.jpg').resize((240,320));sheet.paste(im,(i*360,365))
sheet.save(P/'split/contact.jpg',quality=96)
print('Appended X5-X8, same lower images as X1-X4. No generation or reshuffle.')
