from pathlib import Path
import json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'social media graphics/youtube/thumbnails/_trial-campaign-20261001'
PH=ROOT/'photos/finalized social media photos'
IMPACT='/System/Library/Fonts/Supplemental/Impact.ttf'
MANROPE='/Users/danielrose/Library/Fonts/Manrope.ttf'
ADS=[
 dict(id='ad13',name='Ad 13: The Cost Of Getting Abs',prefix='Ad 13 ',accent='#FFDC32',recommend='B',why='The trainer headline and large expense props connect the objection to the real physique in one glance.',photos=['photo-10','studio-gray-38','studio-white-42','studio-gray-67','studio-blue-38'],waist=[.76,.72,.73,.80,.73],lines=[['FIRE YOUR','PERSONAL','TRAINER'],['HUMAN TRAINERS','HATE THIS AI'],['I FIRED','MY TRAINER'],['ABS WITHOUT','TRAINER BILLS'],['HOW AI','GOT ME ABS']],tests=['Real pool photo makes the result feel attainable.','A provocative trainer headline plus cash and coaching-cost props.','A receipt-filled kettlebell makes the cost of fitness tangible.','A bold outcome-first design connects abs to avoiding trainer bills.','A clean portrait tests personal history against the enemy angle.'],aspects=['16x9'],video='-SuKGXGcbIg'),
 dict(id='ra01',name='RA-01: AI Got Me Abs',prefix='RA-01 ',accent='#50DAFF',recommend='A',why='The real pool photo makes the outcome immediate, and the headline tells the same personal story as the ad.',photos=['photo-125','studio-blue-173','studio-blue-249','studio-blue-100','studio-blue-53'],waist=[.88,.79,.74,.75,.80],lines=[['HOW AI','GOT ME ABS'],['AI GOT','ME ABS'],['HOW AI','GOT ME ABS'],['ABS AT 40','WITH AI'],['AI CHANGED','MY BODY']],tests=['An energetic pool pose carries the first-person AI story.','The phone and weights connect AI to real training.','A luminous portal tests curiosity about imagining a fitness goal.','The age-led treatment qualifies men interested in results at 40.','A clean extended-abs pose tests the personal change angle.'],aspects=['16x9','9x16'],video='OUw788sF1KY'),
 dict(id='ad10',name='Ad 10: Busy Dad Fitness',prefix='Ad 10 ',accent='#FFAF42',recommend='B',why='The headline identifies busy dads immediately; the laptop and weight show the work-and-fitness tension.',photos=['photo-230','studio-blue-127','studio-blue-11','studio-white-25','studio-white-31'],waist=[.96,.79,.78,.78,.80],lines=[['BUSY DADS','GET ABS'],['HOW BUSY DADS','GET ABS'],['BUSY DAD.','REAL ABS.'],['DAD BOD','AT 40'],['HOW DADS','LOSE BELLY FAT']],tests=['A relaxed pool photo sells the outcome without a gym setting.','Work and training props make the busy-dad problem instantly legible.','The giant clock tests the time objection.','A giant age-led headline tests identification before explanation.','A cleaner portrait tests the direct belly-fat outcome.'],aspects=['16x9','9x16'],video='Sg3vcEY2P_8'),
 dict(id='ad4',name='Ad 4: Stop Wasting Money On Supplements',prefix='Ad 4 ',accent='#FF514A',recommend='C',why='The bottle and magnifying glass show the actual reason to watch: using AI to inspect supplements.',photos=['photo-247','studio-white-59','studio-blue-240','studio-white-57','studio-white-4'],waist=[.76,.73,.79,.74,.83],lines=[['THE TRUTH','ABOUT','SUPPLEMENTS'],['SUPPLEMENT','CORPS','HATE HIM'],['AI FIXED','MY SUPPLEMENTS'],['STOP WASTING','SUPPLEMENT','MONEY'],['HOW AI FIXED','MY SUPPLEMENTS']],tests=['A pool portrait tests whether the physique pulls interest into supplements.','Large bottles and the enemy headline test distrust of supplement marketing.','The magnifying glass visualizes inspecting labels with AI.','The direct money-waste angle tests a blunt consumer benefit.','The personal AI story is presented with a restrained studio portrait.'],aspects=['16x9'],video='R08TPEtkjuQ'),
 dict(id='ad3',name='Ad 3: Stop Paying Human Trainers',prefix='Ad 3 ',accent='#6AE5E3',recommend='C',why='The robotic hand and dumbbell make the AI-trainer replacement idea clear before the viewer reads the full headline.',photos=['photo-273','studio-blue-269','studio-gray-4','studio-white-23','studio-blue-76'],waist=[.76,.73,.75,.77,.75],lines=[['FIRE YOUR','PERSONAL','TRAINER'],['TRAINERS','HATE THIS','AI APP'],['AI REPLACED','MY TRAINER'],['HUMAN TRAINERS','HATE HIM'],['MY TRAINER','IS AI']],tests=['A real pool photo pairs with the clearest action headline.','Traditional training props test the direct enemy angle.','The robot dumbbell visual makes the trainer-replacement story concrete.','A loud typographic treatment tests the short personal-enemy headline.','A restrained portrait tests the plain first-person AI-trainer statement.'],aspects=['16x9','9x16','1x1'],video='86jbUhqBTUQ'),
 dict(id='ad6',name="Ad 6: You're Not Too Old",prefix='Ad 6 ',accent='#FFD158',recommend='D',why='The oversized 40 and first-person wording communicate the ad\'s central proof quickly, with no promised timeframe.',photos=['photo-23','studio-blue-221','studio-blue-145','studio-gray-79','studio-white-13'],waist=[.56,.71,.80,.86,.79],lines=[['ABS','AFTER 40'],['HOW MEN 40+','GET ABS'],['NOT TOO OLD','FOR ABS'],['I GOT ABS','AT 40'],['MEN 40+','LOSE BELLY FAT']],tests=['The shortest headline and a poolside physique put age and outcome first.','Warm gym imagery makes fitness after 40 feel relevant and achievable.','The lit steps test an aspirational restart angle.','First-person proof plus a large 40 tests immediate age recognition.','An extended-abs pose tests the audience-and-belly-fat wording.'],aspects=['16x9'],video='Je2yvk00SHE')]
for f in ['options','phone','current','qa','source-portraits']:(P/f).mkdir(exist_ok=True)
def rgb(s):return tuple(bytes.fromhex(s.lstrip('#')))
def font(size,impact=False):
 f=ImageFont.truetype(IMPACT if impact else MANROPE,int(size))
 if not impact:f.set_variation_by_name('ExtraBold')
 return f
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
CACHE={}
def cutout(name):
 if name not in CACHE:
  source=PH/(name+'_FINAL_PRIMARY.jpg')
  if name.startswith('photo-'):
   im=Image.open(source).convert('RGBA');a=Image.open(P/'masks'/(name+'_FINAL_PRIMARY.mask.png')).convert('L');im.putalpha(a)
  else:im=Image.open(PH/'_cutouts'/(name+'_CUTOUT.png')).convert('RGBA')
  CACHE[name]=im
 return CACHE[name].copy()
def scene_pool(name,size):
 im=Image.open(PH/(name+'_FINAL_PRIMARY.jpg')).convert('RGB')
 # Scenery-only strip, selected away from Dan; no duplicate person.
 box=(0,0,int(im.width*.12),im.height)
 bg=ImageOps.fit(im.crop(box),size,method=Image.Resampling.LANCZOS)
 a=np.asarray(bg).astype(float);h,w=a.shape[:2];fade=np.linspace(.19,.52,w)[None,:,None]
 return Image.fromarray((a*fade).astype('uint8')).convert('RGBA')
def gradient(size,base,end):
 w,h=size;y,x=np.mgrid[:h,:w];v=(x/w*.6+y/h*.4)[...,None];a=np.array(base)+(np.array(end)-base)*v
 return Image.fromarray(a.astype('uint8')).convert('RGBA')
def backdrop(ad,slot,size):
 w,h=size;c=rgb(ad['accent'])
 if slot=='A':return scene_pool(ad['photos'][0],size)
 if slot in ['B','C']:
  im=Image.open(P/'generated'/f'{ad["id"]}-{slot}.png').convert('RGBA')
  if w/h>1.3:return ImageOps.fit(im,size)
  # Recompose plate below headline so the prop remains large and in view.
  bg=gradient(size,(9,11,14),(24,27,31))
  crop=im.crop((0,int(im.height*.14),int(im.width*.75),im.height))
  target=ImageOps.fit(crop,(w,int(h*.69)),centering=(.22,.5));bg.alpha_composite(target,(0,int(h*.31)))
  return bg
 if slot=='D':
  bg=gradient(size,tuple(int(v*.93) for v in c),tuple(min(255,int(v*.72+55)) for v in c));d=ImageDraw.Draw(bg)
  d.polygon([(w*.46,0 if w/h>1.3 else h*.32),(w,0 if w/h>1.3 else h*.32),(w,h),(w*.62,h)],fill=(*[int(v*.16) for v in c],255))
  return bg
 return gradient(size,(238,235,224),(189,211,213))
def place_person(ad,slot,size):
 w,h=size;i=ord(slot)-65;name=ad['photos'][i];im=cutout(name);bb=im.getchannel('A').point(lambda x:255 if x>45 else 0).getbbox()
 if name=='photo-23':bb=(int(im.width*.18),bb[1],bb[2],bb[3])
 bottom=int(ad['waist'][i]*im.height);box=(bb[0],max(0,bb[1]-10),bb[2],bottom)
 im=im.crop(box)
 if w/h>1.3:
  top=int(h*.048);targeth=h-top+8;maxw=w*.49;cx=w*(.74 if slot!='E' else .25)
 elif w==h:
  top=int(h*.35);targeth=h-top+8;maxw=w*.72;cx=w*.64
 else:
  top=int(h*.345);targeth=h-top+8;maxw=w*.90;cx=w*.50
 s=min(targeth/im.height,maxw/im.width);nw=int(im.width*s);nh=int(im.height*s)
 # Avoid a waist cut floating above the bottom; keep proportional portrait and fill frame below.
 top=h-nh
 im=im.resize((nw,nh),Image.Resampling.LANCZOS);x=int(cx-nw/2)
 if slot in ['B','C']:outline=im.getchannel('A').filter(ImageFilter.MaxFilter(13));layer=Image.new('RGBA',size);white=Image.new('RGBA',im.size,'white');white.putalpha(outline);layer.alpha_composite(white,(x,top));layer.alpha_composite(im,(x,top))
 else:layer=Image.new('RGBA',size);layer.alpha_composite(im,(x,top))
 person=Image.new('L',size);person.paste(im.getchannel('A'),(x,top))
 return layer,person,dict(source=str(PH/(name+'_FINAL_PRIMARY.jpg')),photo=name,crop=list(box),output_box=[x,top,x+nw,top+nh],scale=s)
def type_block(ad,slot,im,person):
 w,h=im.size;lines=ad['lines'][ord(slot)-65];impact=slot in ['B','C','D'];mask=Image.new('L',im.size);dark=slot in ['D','E'];col=(15,22,28) if dark else (255,255,250);ac=rgb({'ad4':'#8EFF87','ra01':'#C4A3FF','ad3':'#7CBEFF','ad10':'#FFDF45'}.get(ad['id'],ad['accent']) if slot=='C' else ad['accent']);land=w/h>1.3
 if land:
  tx=int(w*(.51 if slot=='E' else .046));maxw=int(w*(.455 if slot=='E' else .45));ty=int(h*(.24 if slot in ['A','D','E'] else .095));maxh=int(h*(.64 if slot in ['A','D','E'] else .45));start=152 if impact else 116
 else:
  tx=int(w*.06);maxw=int(w*.88);ty=int(h*.055);maxh=int(h*.25);start=180 if impact else 127
 # Fit against a genuine person mask; no letters touch face, hair or body.
 dil=person.filter(ImageFilter.MaxFilter(31));dil_array=np.array(dil)>25
 for sz in range(start,35,-2):
  f=font(sz,impact);heights=[f.getbbox(t)[3]-f.getbbox(t)[1] for t in lines];gap=int(sz*.16);total=sum(heights)+gap*(len(lines)-1)
  if max(f.getlength(t) for t in lines)>maxw or total>maxh:continue
  test=Image.new('L',im.size);td=ImageDraw.Draw(test);yy=ty
  for ln,lh in zip(lines,heights):td.text((tx,yy-f.getbbox(ln)[1]),ln,font=f,fill=255,stroke_width=2 if slot in ['B','C'] else 0);yy+=lh+gap
  overlap=np.any((np.array(test)>0)&dil_array)
  if not overlap:break
 else:raise RuntimeError(f'cannot fit {ad["id"]} {slot} {im.size}')
 d=ImageDraw.Draw(im);md=ImageDraw.Draw(mask);yy=ty
 for j,(ln,lh) in enumerate(zip(lines,heights)):
  fill=col
  if slot in ['B','C'] and j==len(lines)-1:fill=ac
  if slot=='D' and j==len(lines)-1:
   width=int(f.getlength(ln));d.rounded_rectangle((tx-12,yy-10,tx+width+14,yy+lh+12),radius=6,fill=(14,24,29));fill=(255,255,250)
  stroke=3 if slot in ['B','C'] else 0
  d.text((tx,yy-f.getbbox(ln)[1]),ln,font=f,fill=fill,stroke_width=stroke,stroke_fill=(7,9,11));md.text((tx,yy-f.getbbox(ln)[1]),ln,font=f,fill=255,stroke_width=stroke);yy+=lh+gap
 if slot=='A':d.rectangle((tx,ty-30,tx+86,ty-20),fill=ac)
 if slot=='E':d.rectangle((tx,ty-28,tx+90,ty-21),fill=(185,55,44))
 return mask,dict(font_size=sz,text_bbox=list(mask.getbbox()),headline=' '.join(lines),text_person_overlap=int(np.count_nonzero((np.array(mask)>0)&(np.array(person)>40))))
records=[]
for ad in ADS:
 folder=next(x for x in P.parent.iterdir() if x.name.startswith(ad['prefix']))
 old=next(x for x in folder.glob('*16x9*FINAL.jpg') if ('O2' if ad['id']=='ad4' else 'O1') in x.name)
 shutil.copy2(old,P/'current'/f'{ad["id"]}.jpg')
 for slot in 'ABCDE':
  for aspect in ad['aspects']:
   size={'16x9':(1280,720),'9x16':(1080,1920),'1x1':(1080,1080)}[aspect]
   if slot in 'BC' and not (P/'generated'/f'{ad["id"]}-{slot}.png').exists():continue
   im=backdrop(ad,slot,size);layer,person,info=place_person(ad,slot,size)
   if slot=='A':
    original=Image.open(info['source']).convert('RGBA');sc=info['scale'];original=original.resize((int(original.width*sc),int(original.height*sc)),Image.Resampling.LANCZOS)
    ox=int(info['output_box'][0]-info['crop'][0]*sc);oy=int(info['output_box'][1]-info['crop'][1]*sc)
    im.alpha_composite(original,(ox,oy));a=np.array(im.convert('RGB')).astype(float);w,h=size
    if w/h>1.3:fade=np.clip(np.linspace(.16,1.3,w),.16,1)[None,:,None]
    else:fade=np.clip(np.linspace(.18,1.15,h),.18,1)[:,None,None]
    im=Image.fromarray((a*fade).astype('uint8')).convert('RGBA')
   im.alpha_composite(layer);tm,ti=type_block(ad,slot,im,person)
   assert ti['text_person_overlap']==0
   path=P/'options'/f'{ad["id"]}-{slot}-{aspect}.jpg';im.convert('RGB').save(path,quality=94,subsampling=0)
   if aspect=='16x9':im.convert('RGB').resize((320,180),Image.Resampling.LANCZOS).save(P/'phone'/path.name,quality=94)
   tm.save(P/'qa'/f'{path.stem}-text.png');person.save(P/'qa'/f'{path.stem}-person.png')
   records.append(dict(ad=ad['id'],option=slot,aspect=aspect,path=str(path),bytes=path.stat().st_size,sha256=sha(path),**info,**ti))
(P/'manifest.json').write_text(json.dumps({'campaign':'24316364155','status':'review_only_awaiting_Dan_picks','ads':ADS,'outputs':records},indent=2))
for ad in ADS:
 sheet=Image.new('RGB',(960,420),'#172128');d=ImageDraw.Draw(sheet)
 items=[('CURRENT',P/'current'/f'{ad["id"]}.jpg')]+[(slot,P/'options'/f'{ad["id"]}-{slot}-16x9.jpg') for slot in 'ABCDE']
 for i,(label,path) in enumerate(items):
  x=i%3*320;y=i//3*210
  if path.exists():sheet.paste(Image.open(path).resize((320,180),Image.Resampling.LANCZOS),(x,y));d.text((x+8,y+185),label+('  RECOMMENDED' if label==ad['recommend'] else ''),font=font(14),fill='white')
 sheet.save(P/'qa'/f'{ad["id"]}-phone.jpg')
print(json.dumps({'layouts':len(records),'max_bytes':max(x['bytes'] for x in records),'overlap_pixels':sum(x['text_person_overlap'] for x in records)}))
