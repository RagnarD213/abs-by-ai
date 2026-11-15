from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
w=Path(__file__).parent;parent=w.parent;review=parent/'review'
root=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI')
b=root/'.claude/skills/_shared/blind-image/blind.py';sd=w/'blind-set'
rs=json.loads((w/'layout-manifest-private.json').read_text());assert len(rs)==8
plan=json.loads((w/'generation-plan.json').read_text())
if not (sd/'.blind-key.json').exists():
 for v in 'ABCD':
  subprocess.run(['python3',str(b),'add',str(sd),'--source',next(j['source'] for j in plan if j['id']==v),'--file',str(w/'layouts/instagram'/(v+'.png')),'--note',v],check=True,capture_output=True)
 subprocess.run(['python3',str(b),'build',str(sd),'--kind','cover','--video','What To Cut Shorts (SL-21)','--shot','Therapy round 2: Dan in middle, two shirtless and two tank top'],check=True,capture_output=True)
key=json.loads((sd/'.blind-key.json').read_text())['labels']
dest=review/'therapy-r2';dest.mkdir(exist_ok=True);entries=[];private=[]
for label,r in sorted(key.items(),key=lambda kv:int(kv[0][1:])):
 v=r['note'];ig=sd/'blind'/(label+'.jpg');(dest/(label+'-instagram.jpg')).write_bytes(ig.read_bytes())
 im=Image.open(w/'layouts/youtube'/(v+'.png')).convert('RGB');im.resize(Image.open(ig).size,Image.Resampling.LANCZOS).save(dest/(label+'-youtube.jpg'),quality=93)
 entries.append({'label':label,'clothing':next(j['clothing'] for j in plan if j['id']==v),'instagram':'therapy-r2/'+label+'-instagram.jpg','youtube':'therapy-r2/'+label+'-youtube.jpg'})
 private.append({'label':label,'id':v,'instagram':str(w/'layouts/instagram'/(v+'.png')),'youtube':str(w/'layouts/youtube'/(v+'.png'))})
(w/'pick-map-private.json').write_text(json.dumps(private,indent=2))
old=review/'index.html';backup=parent/'therapy-round1-index.html'
if not backup.exists():backup.write_bytes(old.read_bytes())
public=json.loads((review/'choices.json').read_text())
vacation=next(e for p in public if p['short']==2 for e in p['choices'] if e['label']=='X7')
restaurant=next(e for e in json.loads((parent/'r4/review-choices.json').read_text())['choices'] if e['label']=='X2')
html=backup.read_text().split('<main>')[0]+'''<main><div class="status">NEW THERAPY COVERS · ROUND 2</div><h1>Choose The Therapy Cover</h1><p>Four new designs: two shirtless and two in a black tank top. All four show you in the middle, with the overweight patient on one side and overweight therapist on the other. Your speech bubble says “You're getting scammed.”</p><p>Instagram is on the left, YouTube on the right. Tap a cover to enlarge it, then choose X1, X2, X3 or X4. Restaurant X2 and Vacation X7 remain approved. All three final videos are unchanged. Setup continues after this last pick.</p><nav><a href="#short3">Four new therapy choices</a><a href="#short1">Restaurant X2 approved</a><a href="#short2">Vacation X7 approved</a></nav>'''
def section(k,title,choices,sheet=None):
 h=f'<section id="short{k}"><h2>{title}</h2>'
 if sheet:h+=f'<a class="sheet" href="{sheet}" target="_blank">Open checked sheet</a>'
 h+='<div class="grid">'
 for e in choices:
  h+=f'<article class="card"><h3>{e["label"]}'+(' · '+e['clothing'].title() if 'clothing' in e else '')+'</h3><div class="pair">'
  for platform in ['instagram','youtube']:h+=f'<figure><img loading="lazy" src="{e[platform]}" alt="Short {k}, {e["label"]}, {platform}" onclick="show(this)"><figcaption>{"Instagram" if platform=="instagram" else "YouTube"}</figcaption></figure>'
  h+='</div></article>'
 return h+'</div></section>'
html+=section(3,"If You Can't Afford A Gym, You Can't Afford Therapy",entries,'therapy-r2-sheet.jpg')
html+=section(1,'Restaurant: X2 Approved',[restaurant])+section(2,'Vacation: X7 Approved',[vacation])
html+='''</main><dialog id="zoom"><button onclick="this.parentNode.close()">Close enlarged cover</button><img id="large" alt="Enlarged cover"></dialog><script>function show(i){document.getElementById('large').src=i.src;document.getElementById('large').alt=i.alt;document.getElementById('zoom').showModal()}document.getElementById('zoom').addEventListener('click',e=>{if(e.target.tagName==='DIALOG')e.target.close()});</script></html>'''
old.write_text(html)
sheet=Image.new('RGB',(1080,1100),'#111b28');d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',23)
for i,e in enumerate(entries):
 for j,p in enumerate(['instagram','youtube']):
  x=i*270;y=j*550;d.text((x+8,y+6),e['label']+' · '+e['clothing'].title(),font=font,fill='white');d.text((x+8,y+31),'Instagram' if j==0 else 'YouTube',font=font,fill='#b9c9dc')
  im=Image.open(review/e[p]).resize((270,480),Image.Resampling.LANCZOS);sheet.paste(im,(x,y+60))
sheet.save(review/'therapy-r2-sheet.jpg',quality=94)
(w/'review-choices.json').write_text(json.dumps({'round':2,'choices':entries},indent=2))
print('Published four new neutral therapy choices. Prior approvals preserved.')
