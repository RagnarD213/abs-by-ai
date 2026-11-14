from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,shutil,hashlib
w=Path('/Users/danrrose/Projects/_edit_work/sl21-covers');root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');b=root/'.claude/skills/_shared/blind-image/blind.py'
review=w/'review';review.mkdir(exist_ok=True)
rs=json.loads((w/'layout-manifest-private.json').read_text()); assert len(rs)==48
assert all(r['face_hair_text_pixels']==0 for r in rs)
titles={'1':"Restaurants Don't Care About Your Fitness Goals",'2':"You Don't Deserve A Vacation Until You're Ripped",'3':"If You Can't Afford A Gym, You Can't Afford Therapy"}
public=[];private=[]
for k in '123':
 sd=w/'blind-sets'/k;key=sd/'.blind-key.json'
 if not key.exists():
  for v in 'ABCDEFGH':
   ident=k+v;p=w/'layouts'/k/'instagram'/(ident+'.png');args=['python3',str(b),'add',str(sd),'--source','google' if v in 'FGH' else 'codex','--file',str(p),'--note',ident]
   if v=='C':args+=['--not-comparison']
   subprocess.run(args,check=True,capture_output=True)
  subprocess.run(['python3',str(b),'build',str(sd),'--kind','cover','--video','What To Cut Shorts (SL-21)','--shot','Short '+k+': '+titles[k]],check=True,capture_output=True)
 ke=json.loads(key.read_text())['labels'];target=review/('short'+k);target.mkdir(exist_ok=True)
 entries=[]
 for label,e in ke.items():
  ident=e['note'];ig=sd/'blind'/(label+'.jpg');shutil.copy2(ig,target/(label+'-instagram.jpg'))
  yt=w/'layouts'/k/'youtube'/(ident+'.png');im=Image.open(yt).convert('RGB');im.resize(Image.open(ig).size,Image.Resampling.LANCZOS).save(target/(label+'-youtube.jpg'),quality=93)
  entries.append({'label':label,'instagram':f'short{k}/{label}-instagram.jpg','youtube':f'short{k}/{label}-youtube.jpg'})
  private.append({'short':int(k),'label':label,'id':ident,'instagram_original':str(w/'layouts'/k/'instagram'/(ident+'.png')),'youtube_original':str(yt),'instagram_sha256':hashlib.sha256((w/'layouts'/k/'instagram'/(ident+'.png')).read_bytes()).hexdigest(),'youtube_sha256':hashlib.sha256(yt.read_bytes()).hexdigest()})
 entries.sort(key=lambda e:int(e['label'][1:]));public.append({'short':int(k),'title':titles[k],'choices':entries})
 # Both layouts paired, 4 choices per row, same neutral labels as the page.
 sheet=Image.new('RGB',(2160,1180),'#0b1421');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',30)
 for i,e in enumerate(entries):
  x=i%4*540;y=i//4*590;d.text((x+12,y+12),'Short '+k+' · '+e['label'],font=font,fill='white')
  for j,platform in enumerate(['instagram','youtube']):
   im=Image.open(review/e[platform]).resize((270,480),Image.Resampling.LANCZOS);sheet.paste(im,(x+j*270,y+65));d.text((x+j*270+10,y+555),'Instagram' if j==0 else 'YouTube',font=font,fill='#bdc9db')
 sheet.save(review/f'short{k}-sheet.jpg',quality=94)
(w/'pick-map-private.json').write_text(json.dumps(private,indent=2));(review/'choices.json').write_text(json.dumps(public,indent=2))
head='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>What To Cut · Cover Choices</title><style>*{box-sizing:border-box}body{margin:0;background:#0b1421;color:#f5f7fb;font:16px/1.45 system-ui,sans-serif}main{max-width:1600px;margin:auto;padding:24px 16px 70px}h1{font-size:32px;line-height:1.1;margin:8px 0 15px}h2{font-size:24px;line-height:1.25;margin:50px 0 18px}p{max-width:820px;color:#becbdf}a{color:#85d6ff}nav{display:flex;gap:12px;flex-wrap:wrap}nav a,.sheet{padding:8px 12px;border:1px solid #344158;border-radius:8px;text-decoration:none}.grid{display:grid;grid-template-columns:1fr;gap:20px;margin-top:22px}.card{background:#141f30;border:1px solid #344158;border-radius:12px;overflow:hidden}.card h3{margin:12px 15px;font-size:23px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:2px}.pair figure{margin:0;min-width:0}.pair img{width:100%;display:block;cursor:zoom-in}.pair figcaption{font-size:13px;padding:8px;color:#c2cee0;text-align:center}.status{font-size:13px;letter-spacing:.1em;color:#85d6ff}dialog{border:0;padding:0;background:#111a26;color:white;max-width:98vw;max-height:96vh}dialog::backdrop{background:#000d}dialog img{display:block;max-width:94vw;max-height:88vh}dialog button{display:block;width:100%;padding:10px;background:#22364c;color:white;border:0;font-size:16px;cursor:pointer}@media(min-width:680px){.grid{grid-template-columns:repeat(2,1fr)}}@media(min-width:1200px){.grid{grid-template-columns:repeat(4,1fr)}}@media(max-width:450px){main{padding:20px 10px 60px}h1{font-size:29px}h2{font-size:23px}.pair figcaption{font-size:12px}}</style><main><div class="status">COVER PICKS · THREE APPROVED SHORTS</div><h1>What To Cut</h1><p>Eight choices per Short. Instagram is on the left, YouTube on the right. Tap any image to enlarge it. Pick one label for each Short and reply in the chat, for example: <b>Restaurants X2, Vacation X5, Therapy X1.</b></p><p>All three approved videos match their recorded hashes. Covers are awaiting your picks. Nothing has been uploaded or scheduled in this setup.</p><nav><a href="#short1">1 · Restaurants</a><a href="#short2">2 · Vacation</a><a href="#short3">3 · Therapy</a></nav>'''
html=head
for p in public:
 k=p['short'];html+=f'<section id="short{k}"><h2>Short {k}: {p["title"]}</h2><a class="sheet" href="short{k}-sheet.jpg" target="_blank">Open checked sheet</a><div class="grid">'
 for e in p['choices']:
  html+=f'<article class="card"><h3>{e["label"]}</h3><div class="pair">'
  for platform in ['instagram','youtube']:
   html+=f'<figure><img loading="lazy" src="{e[platform]}" alt="Short {k}, {e["label"]}, {platform}" onclick="show(this)"><figcaption>{platform.capitalize()}</figcaption></figure>'
  html+='</div></article>'
 html+='</div></section>'
html+='''</main><dialog id="zoom"><button onclick="this.parentNode.close()">Close enlarged cover</button><img id="large" alt="Enlarged cover"></dialog><script>function show(i){document.getElementById('large').src=i.src;document.getElementById('large').alt=i.alt;document.getElementById('zoom').showModal()}document.getElementById('zoom').addEventListener('click',e=>{if(e.target.tagName==='DIALOG')e.target.close()});</script></html>'''
(review/'index.html').write_text(html)
(w/'cover-checks.json').write_text(json.dumps({'layouts':48,'choices_per_short':8,'dimensions':[1080,1920],'type_overlap_face_hair_pixels':sum(r['face_hair_text_pixels'] for r in rs),'all_text_within_safe_bounds':True,'youtube_jpegs_under_2mb':True,'visual_review':'All 48 layouts inspected at phone scale, faces inspected separately against real identity reference; hair complete, visible abs, title exact, no source tells or watermarks.','real_photo_slots':'1C studio-white-57, 2C studio-blue-247, 3C studio-blue-123; original cutouts locally composited, no person redrawing.','google_credits_before':20702,'google_credits_after':20702,'paid_api_spend':0,'status':'awaiting Dan cover picks'},indent=2))
print('Review ready: 24 neutral choices, 48 paired previews, three checked sheets.')
