from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,shutil,hashlib
w=Path('/Users/danrrose/Projects/_edit_work/sl21-covers/r4');parent=w.parent;review=parent/'review';root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI');b=root/'.claude/skills/_shared/blind-image/blind.py';sd=w/'blind-set';rs=json.loads((w/'layout-manifest-private.json').read_text());assert len(rs)==8
if not (sd/'.blind-key.json').exists():
 for v in 'ABCD':subprocess.run(['python3',str(b),'add',str(sd),'--source',next(j['source'] for j in json.loads((w/'generation-plan.json').read_text()) if j['id']==v),'--file',str(w/'layouts/instagram'/(v+'.png')),'--note',v],check=True,capture_output=True)
 subprocess.run(['python3',str(b),'build',str(sd),'--kind','cover','--video','What To Cut Shorts (SL-21)','--shot','Restaurants round 4: Why Restaurants Make You Fat'],check=True,capture_output=True)
key=json.loads((sd/'.blind-key.json').read_text())['labels'];dest=review/'restaurant-r4';dest.mkdir(exist_ok=True);entries=[];private=[]
for label,r in sorted(key.items(),key=lambda kv:int(kv[0][1:])):
 v=r['note'];concept={'A':'1A','B':'1B','C':'2','D':'3'}[v];ig=sd/'blind'/(label+'.jpg');shutil.copy2(ig,dest/(label+'-instagram.jpg'));im=Image.open(w/'layouts/youtube'/(v+'.png')).convert('RGB');im.resize(Image.open(ig).size,Image.Resampling.LANCZOS).save(dest/(label+'-youtube.jpg'),quality=93)
 entries.append({'label':label,'concept':concept,'instagram':'restaurant-r4/'+label+'-instagram.jpg','youtube':'restaurant-r4/'+label+'-youtube.jpg'})
 private.append({'label':label,'concept':concept,'id':v,'instagram':str(w/'layouts/instagram'/(v+'.png')),'youtube':str(w/'layouts/youtube'/(v+'.png'))})
(w/'pick-map-private.json').write_text(json.dumps(private,indent=2))
# Preserve round one's page before replacing the current review.
old=review/'index.html';backup=parent/'round1-index.html'
if not (parent/'round3-index.html').exists():shutil.copy2(old,parent/'round3-index.html')
if not backup.exists():shutil.copy2(old,backup)
public=json.loads((review/'choices.json').read_text());vacation=next(e for p in public if p['short']==2 for e in p['choices'] if e['label']=='X7');therapy=next(p for p in public if p['short']==3)
html=backup.read_text().split('<main>')[0]+'''<main><div class="status">RESTAURANT COVERS · ROUND 4</div><h1>Why Restaurants Make You Fat</h1><p>Four new designs: two frontal table tips, one slightly elevated view, and one just as the flip starts. You are smiling behind the table, with an ordinary slightly overweight diner on each side and the meal visible. Instagram is on the left, YouTube on the right. Tap a cover to enlarge it, then reply with X1, X2, X3 or X4.</p><p>Vacation X7 is approved and saved unchanged. The therapy cover still needs a pick. The approved videos remain unchanged. Nothing has been uploaded or scheduled in this setup.</p><nav><a href="#short1">New restaurant covers</a><a href="#short2">Vacation X7 approved</a><a href="#short3">Therapy choices</a></nav>'''
def section(k,title,choices,sheet=None):
 h=f'<section id="short{k}"><h2>{title}</h2>'
 if sheet:h+=f'<a class="sheet" href="{sheet}" target="_blank">Open checked sheet</a>'
 h+='<div class="grid">'
 for e in choices:
  h+=f'<article class="card"><h3>{e["label"]}'+(f' · Concept {e["concept"]}' if 'concept' in e else '')+'</h3><div class="pair">'
  for platform in ['instagram','youtube']:h+=f'<figure><img loading="lazy" src="{e[platform]}" alt="Short {k}, {e["label"]}, {platform}" onclick="show(this)"><figcaption>{"Instagram" if platform=="instagram" else "YouTube"}</figcaption></figure>'
  h+='</div></article>'
 return h+'</div></section>'
html+=section(1,'Restaurants: Four New Choices',entries,'restaurant-r4-sheet.jpg');html+=section(2,'Vacation: X7 Approved',[vacation]);html+=section(3,therapy['title']+' (Awaiting Pick)',therapy['choices'],'short3-sheet.jpg')
html+='''</main><dialog id="zoom"><button onclick="this.parentNode.close()">Close enlarged cover</button><img id="large" alt="Enlarged cover"></dialog><script>function show(i){document.getElementById('large').src=i.src;document.getElementById('large').alt=i.alt;document.getElementById('zoom').showModal()}document.getElementById('zoom').addEventListener('click',e=>{if(e.target.tagName==='DIALOG')e.target.close()});</script></html>''';old.write_text(html)
sheet=Image.new('RGB',(1080,1100),'#111b28');d=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',23)
for i,e in enumerate(entries):
 for j,p in enumerate(['instagram','youtube']):
  x=i*270;y=j*550;d.text((x+8,y+6),e['label']+' · Concept '+e['concept'],font=font,fill='white');d.text((x+8,y+31),'Instagram' if j==0 else 'YouTube',font=font,fill='#b9c9dc');im=Image.open(review/e[p]).resize((270,480),Image.Resampling.LANCZOS);sheet.paste(im,(x,y+60))
sheet.save(review/'restaurant-r4-sheet.jpg',quality=94)
(w/'review-choices.json').write_text(json.dumps({'round':4,'cover_title':'Why Restaurants Make You Fat','choices':entries},indent=2));print('Published four new neutral restaurant choices, Vacation X7 approval, unchanged therapy choices.')
