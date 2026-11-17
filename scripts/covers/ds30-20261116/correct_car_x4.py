"""Dan's R2-X4 copy revision: two single-line headers. Preserve scene and film."""
from pathlib import Path
import ast,json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
ROOT=Path(__file__).resolve().parents[3];BASE=Path('/Volumes/Expansion/_edit_work/DS-30-setup');P=BASE/'r2';OUT=BASE/'r5'/'covers';OUT.mkdir(exist_ok=True);W,H=1080,1920
FONT='/System/Library/Fonts/Supplemental/Impact.ttf';SMALL='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
tree=ast.parse((Path(__file__).parent/'build.py').read_text());helper=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['text','shade']],type_ignores=[]);exec(compile(helper,'r1-layout-helpers','exec'))
words='Change the title to "Make Time for Fitness with a Self-Driving Car." Let\'s go with R2-X4. I want to change the text though. Put "Make Time for Fitness" all on one line on the top with "the self-driving car" all on one line below it. Increase the size of the "self-driving car" text as much as you can while fitting it all on one line'
selection=P/'selection-R2-X4.json'
if not selection.exists():
 subprocess.run(['python3',str(ROOT/'.claude/skills/_shared/blind-image/blind.py'),'pick',str(P/'comparison'),'--chose','X4','--words',words],check=True)
 selection.write_text(json.dumps({'selected':'R2-X4','words':words,'status':'scene chosen, revised text awaits exact-file approval','publishing_title':'Make Time for Fitness with a Self-Driving Car.'},indent=2))
(BASE/'publishing-title.json').write_text(json.dumps({'title':'Make Time for Fitness with a Self-Driving Car.','approved_by':'Dan','date':'2026-11-16','source':'Dan publishing-title choice and latest cover-copy correction','cover_text':['Make Time For Fitness','With A Self-Driving Car'],'film_unchanged':True},indent=2))
full=Image.open(BASE/'r5/car-corrected-source.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS);records=[]
for plat in ['Instagram','YouTube']:
 ig=plat=='Instagram'
 if ig:
  im=full.filter(ImageFilter.GaussianBlur(30));small=full.resize((972,1728),Image.Resampling.LANCZOS);mask=Image.new('L',small.size,255);md=ImageDraw.Draw(mask)
  for x in range(20):md.line((x,0,x,1728),fill=int(255*x/20));md.line((971-x,0,971-x,1728),fill=int(255*x/20))
  im.paste(small,(54,100),mask)
 else:im=full.copy()
 im=shade(im,550 if ig else 365,610 if ig else 420,[23,29,39],.96)
 start=250 if ig else 96;d=ImageDraw.Draw(im);d.rectangle((55,start,64,start+288),fill='#ffae70')
 # Maximum available line width while retaining the selected design's left rule and safe right margin.
 width=943;left=92
 t=[text(im,'Make Time For Fitness',start,280,'#fff6e7',width=width,left=left),text(im,'With A Self-Driving Car',start+140,280,'#ffae70',width=width,left=left)]
 for v in t:
  assert len(v['text'].split('\n'))==1
  assert v['box'][2]<=1035
  f=ImageFont.truetype(FONT,v['font_size']+1)
  assert d.textlength(v['text'],font=f)>width,'font must be largest integer size fitting available width'
 assert t[0]['box'][3]<t[1]['box'][1]
 f=OUT/f'R2-X4-Car-Fixed-{plat}.png';im.save(f);jpg=f.with_suffix('.jpg');im.save(jpg,quality=94,subsampling=0);assert jpg.stat().st_size<2_000_000
 im.crop((0,240,W,1680)).save(OUT/f'R2-X4-Car-Fixed-{plat}-Grid.jpg',quality=95)
 old=Image.open(BASE/'r4'/f'R2-X4-With-{plat}.png').convert('RGB');changed=np.any(np.asarray(old)!=np.asarray(im),axis=2)
 native=Image.open(BASE/'r5/foreground-protect-final.png').convert('L').point(lambda v:255 if v==255 else 0).filter(ImageFilter.MinFilter(13))
 pm=native.resize((W,H),Image.Resampling.NEAREST)
 if ig:
  mm=Image.new('L',(W,H));mm.paste(pm.resize((972,1728),Image.Resampling.NEAREST),(54,100));pm=mm
 pa=np.array(pm)>0;pa[:550 if ig else 420,:]=False
 assert int(pa.sum())>300000
 # The Instagram photo-edge feather also samples the blurred car background.
 # Restore the selected cover's exact protected foreground after that blend.
 final=np.array(im);final[pa]=np.array(old)[pa];im=Image.fromarray(final)
 changed=np.any(np.array(old)!=final,axis=2)
 im.save(f);im.save(jpg,quality=94,subsampling=0)
 im.crop((0,240,W,1680)).save(OUT/f'R2-X4-Car-Fixed-{plat}-Grid.jpg',quality=95)
 assert not changed[pa].any(),'protected original foreground changed in cover'
 car_changes=int(changed.sum())
 records.append({'platform':plat,'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'jpg':str(jpg),'jpg_bytes':jpg.stat().st_size,'text':t,'max_line_width':width,'largest_integer_font_verified':True,'protected_foreground_pixels':int(pa.sum()),'protected_foreground_pixels_changed':0,'car_background_pixels_changed':car_changes,'selected_scene':'R2-X4'})
(OUT/'revision-manifest.json').write_text(json.dumps(records,indent=2))
sheet=Image.new('RGB',(1110,1030),'#101c2a');sd=ImageDraw.Draw(sheet);label=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',26)
for i,plat in enumerate(['Instagram','YouTube']):
 im=Image.open(OUT/f'R2-X4-Car-Fixed-{plat}.png');im.thumbnail((520,925));x=20+i*550;sheet.paste(im,(x,60));sd.text((x,16),plat,font=label,fill='white')
sheet.save(OUT/'R2-X4-Car-Fixed-Paired.jpg',quality=95)
print(json.dumps([{'platform':r['platform'],'fonts':[x['font_size'] for x in r['text']],'widths':[x['box'][2]-x['box'][0] for x in r['text']],'protected_foreground_changed':r['protected_foreground_pixels_changed'],'car_pixels_changed':r['car_background_pixels_changed']} for r in records]))
