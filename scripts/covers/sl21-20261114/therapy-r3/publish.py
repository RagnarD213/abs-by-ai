from pathlib import Path
from PIL import Image
import json
w=Path(__file__).parent;parent=w.parent;review=parent/'review';dest=review/'therapy-r3'
dest.mkdir(exist_ok=True)
for platform in ['instagram','youtube']:
 im=Image.open(w/'layouts'/platform/'X3-revised.png').convert('RGB')
 im.resize((941,1672),Image.Resampling.LANCZOS).save(dest/('X3-'+platform+'.jpg'),quality=93)
(review/'therapy-r3-sheet.jpg').write_bytes((w/'X3-revised-both-layouts.jpg').read_bytes())
old=review/'index.html';backup=parent/'therapy-round2-index.html'
if not backup.exists():backup.write_bytes(old.read_bytes())
html=backup.read_text().split('<main>')[0]+'''<main><div class="status">X3 SELECTED · SPEECH BUBBLE REVISED</div><h1>Review The Revised X3</h1><p>The speech bubble is smaller and on the right toward the patient, with all-black text on one line. The rectangle and tail form one continuous shape without an internal dividing line. The picture and headline are unchanged.</p><p>Instagram is on the left, YouTube on the right. Tap either cover to enlarge. This revised file needs your approval before installation. Restaurant X2 and Vacation X7 remain approved; all three final videos remain unchanged.</p><nav><a href="#short3">Revised X3</a><a href="#short1">Restaurant X2 approved</a><a href="#short2">Vacation X7 approved</a></nav>'''
def section(k,title,choices,sheet=None):
 h=f'<section id="short{k}"><h2>{title}</h2>'
 if sheet:h+=f'<a class="sheet" href="{sheet}" target="_blank">Open checked sheet</a>'
 h+='<div class="grid">'
 for e in choices:
  h+=f'<article class="card"><h3>{e["label"]}</h3><div class="pair">'
  for pl in ['instagram','youtube']:h+=f'<figure><img src="{e[pl]}" alt="Short {k}, {e["label"]}, {pl}" onclick="show(this)"><figcaption>{pl.title()}</figcaption></figure>'
  h+='</div></article>'
 return h+'</div></section>'
public=json.loads((review/'choices.json').read_text())
vacation=next(e for p in public if p['short']==2 for e in p['choices'] if e['label']=='X7')
restaurant=next(e for e in json.loads((parent/'r4/review-choices.json').read_text())['choices'] if e['label']=='X2')
current={'label':'X3 Revised','instagram':'therapy-r3/X3-instagram.jpg','youtube':'therapy-r3/X3-youtube.jpg'}
html+=section(3,'Therapy: X3 Revised',[current],'therapy-r3-sheet.jpg')
html+=section(1,'Restaurant: X2 Approved',[restaurant])+section(2,'Vacation: X7 Approved',[vacation])
html+='''</main><dialog id="zoom"><button onclick="this.parentNode.close()">Close enlarged cover</button><img id="large" alt="Enlarged cover"></dialog><script>function show(i){document.getElementById('large').src=i.src;document.getElementById('large').alt=i.alt;document.getElementById('zoom').showModal()}document.getElementById('zoom').addEventListener('click',e=>{if(e.target.tagName==='DIALOG')e.target.close()});</script></html>'''
old.write_text(html)
(w/'review-choices.json').write_text(json.dumps({'round':3,'selected_from_round':2,'selected':'X3','status':'awaiting exact revised file approval','choices':[current]},indent=2))
print('Published revised X3 in both layouts; prior approvals preserved.')
