"""Change only the selected X3 headline; preserve every picture pixel."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
R=P/'r2';Q=R/'x3-revision';O=Q/'designed';O.mkdir(parents=True,exist_ok=True)
words='Let\'s go with X3. Let\'s change the text to "Why cheat days make you fat."'
pickfile=Q/'selection.json'
if not pickfile.exists():
 subprocess.run([sys.executable,str(ROOT/'.claude/skills/_shared/blind-image/blind.py'),'pick',str(R/'comparison-expanded'),'--chose','X3','--words',words],check=True)
 pickfile.write_text(json.dumps({'date':'2026-11-15','round':2,'selected':'X3','exact_words':words,'requested_headline':'Why cheat days make you fat.','rendered_headline':'Why Cheat Days Make You Fat','final_files_approved':False,'state':'REVISION_AWAITING_FINAL_OK'},indent=2)+'\n')
mapping=json.loads((R/'neutral-install-map.json').read_text())['X3']
manifest=json.loads((R/'layout-manifest.json').read_text());out=[]
for platform,selected in mapping.items():
 source=Path(selected['original']);assert hashlib.sha256(source.read_bytes()).hexdigest()==selected['sha256']
 base=Image.open(source).convert('RGB');im=base.copy();d=ImageDraw.Draw(im)
 old=next(r for r in manifest if r['file']==str(source));band_y=old['podcast_bounds'][3];photo_y=old['photo_top']
 d.rectangle((0,band_y,1079,photo_y-1),fill='#ffda20')
 text=[]
 for phrase,oldrow in zip(['Why Cheat Days','Make You Fat'],old['text'][1:]):
    maxsize=oldrow['font_size'];y=oldrow['box'][1]
    for size in range(maxsize,50,-1):
      f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Impact.ttf',size)
      if d.textlength(phrase,font=f)<=986:break
    bb=d.textbbox((0,0),phrase,font=f);x=round((1080-d.textlength(phrase,font=f))/2)
    pos=(x,y-bb[1]);d.text(pos,phrase,font=f,fill='#161616')
    bounds=list(d.textbbox(pos,phrase,font=f));assert bounds[0]>=40 and bounds[2]<=1040 and bounds[1]>=band_y+7 and bounds[3]<photo_y-7
    text.append({'text':phrase,'box':bounds,'font_size':size})
 outside=np.ones((1920,1080),bool);outside[band_y:photo_y]=False
 assert np.array_equal(np.asarray(im)[outside],np.asarray(base)[outside])
 f=O/f'X3-Revised-{platform}.png';im.save(f)
 jpg=f.with_suffix('.jpg');im.save(jpg,quality=94,subsampling=0);assert jpg.stat().st_size<2_000_000
 if platform=='Instagram':im.crop((0,240,1080,1680)).save(O/'X3-Revised-Grid.jpg',quality=94,subsampling=0)
 out.append({'platform':platform,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'jpg':str(jpg),'jpg_bytes':jpg.stat().st_size,'base':str(source),'base_sha256':selected['sha256'],'changed_region':[0,band_y,1080,photo_y],'all_pixels_outside_headline_band_unchanged':True,'text':text,'source_name_caption_unchanged':True,'podcast_bounds':old['podcast_bounds'],'photo_top':photo_y,'final_approved':False})
(Q/'manifest.json').write_text(json.dumps(out,indent=2)+'\n')
sheet=Image.new('RGB',(1080,730),'#152031');d=ImageDraw.Draw(sheet)
for i,platform in enumerate(['Instagram','YouTube']):
 im=Image.open(O/f'X3-Revised-{platform}.png').resize((350,622));sheet.paste(im,(i*360,44));d.text((i*360+8,12),platform,fill='white')
im=Image.open(O/'X3-Revised-Grid.jpg').resize((350,467));sheet.paste(im,(720,44));d.text((728,12),'Instagram grid',fill='white')
sheet.save(Q/'contact.jpg',quality=96)
print('Built revised X3 pair and grid; only headline band changed. Await final approval.')
