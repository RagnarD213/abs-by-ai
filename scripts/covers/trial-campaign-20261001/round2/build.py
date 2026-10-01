"""Round 2 only. Reuse round 1 rendering functions without running its builder."""
from pathlib import Path
import ast,copy,json,hashlib,shutil
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFilter
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
P=ROOT/'social media graphics/youtube/thumbnails/_trial-campaign-20261001'
R=P/'round2'; PH=ROOT/'photos/finalized social media photos'
# Load definitions only. Round 1 output loop and filesystem writes never run.
source=ROOT/'scripts/covers/trial-campaign-20261001/build.py'
tree=ast.parse(source.read_text());tree.body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.Assign)) and not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['ROOT','records'] for t in n.targets))]
ns={'ROOT':ROOT,'__file__':str(source)};exec(compile(tree,str(source),'exec'),ns)
for folder in ['options','phone','qa','references','sources']: (R/folder).mkdir(exist_ok=True)
SIZES={'16x9':(1280,720),'9x16':(1080,1920),'1x1':(1080,1080)}
ADS={a['id']:a for a in ns['ADS']}
choices=[
 dict(id='13-R2A',ad='ad13',photo='photo-10',waist=.713,base='ad13',slot='B',title='Requested pool-photo swap',note='Original B expense scene, now with the real pool portrait.'),
 dict(id='13-R2B',ad='ad13',photo='photo-10',waist=.713,base='ad13',slot='B',plate='ad13-robot',title='Robot trainer',note='A coaching robot takes over the trainer role. Real pool portrait stays unchanged.'),
 dict(id='13-R2C',ad='ad13',photo='photo-10',waist=.713,base='ad13',slot='B',plate='ad13-savings',title='AI coaching saves money',note='A phone and coin-filled piggy bank make the savings message visible.'),
 dict(id='RA-R2A',ad='ra01',photo='studio-blue-53',waist=.80,base='ra01',slot='C',title='C design + E photo',note='Your arms-up E portrait in the original purple C scene.'),
 dict(id='10-R2A',ad='ad10',photo='studio-white-25',waist=.78,base='ad10',slot='B',title='B design + D photo',note='Jeans and glasses in the original orange home-office scene.'),
 dict(id='4-B-original',ad='ad4',photo='studio-white-59',original=True,base='ad4',slot='B',title='Original B, unchanged',note='The exact round-1 JPG, kept for comparison.'),
 dict(id='4-R2A',ad='ad4',photo='studio-gray-55',waist=.70,base='ad4',slot='B',title='Confident smirk',note='A real sideways smirk with hands behind the head. No facial retouching.'),
 dict(id='3-R2A',ad='ad3',photo='studio-blue-173',waist=.79,base='ra01',slot='B',title='RA-01 B design + Ad 3 B copy',note='The exact cyan phone-and-dumbbell design and real RA-01 B portrait.'),
 dict(id='6-B-original',ad='ad6',photo='studio-blue-221',original=True,base='ad6',slot='B',title='Original B, unchanged',note='The exact round-1 JPG, kept for comparison.'),
 dict(id='6-R2A',ad='ad6',photo='studio-blue-171',waist=.78,base='ad6',slot='B',title='Jeans and glasses',note='A different jeans-and-glasses photo from Ad 10, in the original warm gym.'),
 dict(id='6-R2B',ad='ad6',photo='studio-blue-221',waist=.71,base='ad6',slot='B',age=True,title='Older appearance',note='AI age edit: gray hair and older face/neck skin. Original body, hands and clothing retained.')]
recommendations={
'ad13':('13-R2B','The robot makes the AI trainer replacement clear at a glance; the pool portrait carries the result.'),
'ra01':('RA-R2A','Your requested combination makes the abs prominent while keeping the purple visual you liked.'),
'ad10':('10-R2A','Glasses, jeans and the office scene make the busy-dad message feel natural.'),
'ad4':('4-R2A','The sideways smirk supports the provocative headline better than the friendly original smile.'),
'ad3':('3-R2A','The phone stays visible and connects the trainer headline directly to an app.'),
'ad6':('6-R2A','The real jeans-and-glasses photo feels approachable and fits the men-over-40 message.')}
# Blend only generated head and neck pixels into the original cutout.
original=ns['cutout']('studio-blue-221');aged=Image.open(R/'generated/ad6-age.png').convert('RGBA').resize(original.size,Image.Resampling.LANCZOS)
w,h=original.size;mask=Image.new('L',(w,h));d=ImageDraw.Draw(mask)
d.polygon([(int(x*w),int(y*h)) for x,y in [(0.40,.045),(.71,.045),(.71,.24),(.64,.29),(.57,.31),(.46,.30),(.40,.26)]],fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(12));mask=np.array(mask);mask[int(h*.32):]=0;mask=Image.fromarray(mask)
aged_person=Image.composite(aged,original,mask);aged_person.putalpha(original.getchannel('A'));aged_person.save(R/'sources/studio-blue-221-aged-head-original-body.png')
assert np.array_equal(np.array(aged_person)[int(h*.32):],np.array(original)[int(h*.32):])
records=[]
for c in choices:
 a=copy.deepcopy(ADS[c['base']]);slot=c['slot'];i=ord(slot)-65;a['photos'][i]=c['photo'];a['waist'][i]=c.get('waist',a['waist'][i])
 if c['ad']=='ad3':a['lines'][i]=ADS['ad3']['lines'][1]
 c['headline']=a['lines'][i];c['aspects']=ADS[c['ad']]['aspects'];c['reference']=f"{c['base']}-{slot}"
 ref=P/'options'/f"{c['reference']}-16x9.jpg";shutil.copy2(ref,R/'references'/ref.name)
 c['background']=str((R/'generated'/f"{c['plate']}.png") if c.get('plate') else (P/'generated'/f"{c['base']}-{slot}.png"))
 for aspect in c['aspects']:
  size=SIZES[aspect];path=R/'options'/f"{c['id']}-{aspect}.jpg"
  if c.get('original'):
   shutil.copy2(P/'options'/f"{c['base']}-{slot}-{aspect}.jpg",path);im=Image.open(path);info={'unchanged_original':True}
  else:
   im=ImageOps.fit(Image.open(c['background']).convert('RGBA'),size) if c.get('plate') else ns['backdrop'](a,slot,size)
   if c.get('plate')=='ad13-robot':
    shifted=Image.new('RGBA',size,(2,3,4,255));shifted.alpha_composite(im,(0,75));im=shifted
   if c['id']=='3-R2A' and aspect=='1x1':
    im=ns['gradient'](size,(9,11,14),(24,27,31))
    scene=Image.open(c['background']).convert('RGBA');scene=scene.resize((1120,630),Image.Resampling.LANCZOS)
    alpha=Image.new('L',scene.size,255);fade=ImageDraw.Draw(alpha)
    for yy in range(90):fade.line((0,yy,1120,yy),fill=int(255*yy/89))
    scene.putalpha(alpha);im.alpha_composite(scene,(-40,450))
   if c.get('age'):ns['CACHE'][c['photo']]=aged_person
   else:ns['CACHE'].pop(c['photo'],None)
   layer,person,info=ns['place_person'](a,slot,size)
   im.alpha_composite(layer);tm,ti=ns['type_block'](a,slot,im,person);info.update(ti)
   if c.get('plate')=='ad13-robot':info['scene_transform']={'translate_y':75,'fill':'#020304'}
   if c['id']=='3-R2A' and aspect=='1x1':info['scene_transform']={'size':[1120,630],'position':[-40,450],'top_fade_pixels':90}
   assert info['text_person_overlap']==0
   tm.save(R/'qa'/f'{path.stem}-text.png');person.save(R/'qa'/f'{path.stem}-person.png')
   im.convert('RGB').save(path,quality=94,subsampling=0)
  phone=im.convert('RGB');phone.thumbnail((320,600),Image.Resampling.LANCZOS);phone.save(R/'phone'/path.name,quality=94)
  assert path.stat().st_size<2000000
  records.append(dict(info,choice=c['id'],ad=c['ad'],aspect=aspect,path=str(path.relative_to(R)),size=list(size),bytes=path.stat().st_size,sha256=ns['sha'](path),background=c['background'],photo=c['photo'],headline=c['headline']))
ads=[dict(id=k,name=a['name'],recommend=recommendations[k][0],why=recommendations[k][1],choices=[c for c in choices if c['ad']==k]) for k,a in ADS.items()]
manifest=dict(campaign='24316364155',status='review_only_awaiting_Dan_picks',generation_count=3,paid_image_api_calls=0,generation_tokens={'ad13-robot':45629,'ad13-savings':19131,'ad6-age':39670},prompts={p.stem:p.read_text() for p in (R/'prompts').glob('*.txt')},age_edit=dict(source='studio-blue-221',edited_region='hair, face, neck only',original_pixels_unchanged_below_y_fraction=.32),ads=ads,outputs=records)
(R/'manifest.json').write_text(json.dumps(manifest,indent=2))
for ad in ads:
 cs=ad['choices'];s=Image.new('RGB',(max(1,len(cs))*320,215),'#172128');d=ImageDraw.Draw(s)
 for j,c in enumerate(cs):s.paste(Image.open(R/'phone'/f"{c['id']}-16x9.jpg"),(j*320,0));d.text((j*320+8,186),c['id']+('  MY PICK' if c['id']==ad['recommend'] else ''),font=ns['font'](15),fill='white')
 s.save(R/'qa'/f"{ad['id']}-phone.jpg")
print(json.dumps({'choices':len(choices),'layouts':len(records),'max_bytes':max(r['bytes'] for r in records),'overlap_pixels':sum(r.get('text_person_overlap',0) for r in records)}))
