from pathlib import Path
import json,shutil
w=Path('/Users/danrrose/Projects/_edit_work/sl21-covers');review=w/'review';old=review/'index.html'
if not (w/'round4-index.html').exists():shutil.copy2(old,w/'round4-index.html')
public=json.loads((review/'choices.json').read_text());therapy=next(p for p in public if p['short']==3);vacation=next(e for p in public if p['short']==2 for e in p['choices'] if e['label']=='X7');restaurant=next(e for e in json.loads((w/'r4/review-choices.json').read_text())['choices'] if e['label']=='X2')
head=old.read_text().split('<main>')[0].replace('What To Cut · Cover Choices','What To Cut · Therapy Cover Pick')
html=head+'''<main><div class="status">TWO COVERS APPROVED · ONE PICK LEFT</div><h1>Choose The Therapy Cover</h1><p>Restaurant X2 and Vacation X7 are approved and saved unchanged. Choose one of the original therapy options below, X1–X8. Instagram is on the left, YouTube on the right. Tap any cover to enlarge it.</p><p>All three videos remain approved and unchanged. Backups, media uploads and scheduling will continue after this final cover pick.</p><nav><a href="#short3">Therapy choices</a><a href="#short1">Restaurant X2 approved</a><a href="#short2">Vacation X7 approved</a></nav>'''
def section(k,title,choices,sheet=None):
 h=f'<section id="short{k}"><h2>{title}</h2>'
 if sheet:h+=f'<a class="sheet" href="{sheet}" target="_blank">Open checked sheet</a>'
 h+='<div class="grid">'
 for e in choices:
  h+=f'<article class="card"><h3>{e["label"]}</h3><div class="pair">'
  for platform in ['instagram','youtube']:h+=f'<figure><img loading="lazy" src="{e[platform]}" alt="Short {k}, {e["label"]}, {platform}" onclick="show(this)"><figcaption>{"Instagram" if platform=="instagram" else "YouTube"}</figcaption></figure>'
  h+='</div></article>'
 return h+'</div></section>'
html+=section(3,therapy['title'],therapy['choices'],'short3-sheet.jpg')+section(1,'Restaurant: X2 Approved',[restaurant])+section(2,'Vacation: X7 Approved',[vacation])
html+='''</main><dialog id="zoom"><button onclick="this.parentNode.close()">Close enlarged cover</button><img id="large" alt="Enlarged cover"></dialog><script>function show(i){document.getElementById('large').src=i.src;document.getElementById('large').alt=i.alt;document.getElementById('zoom').showModal()}document.getElementById('zoom').addEventListener('click',e=>{if(e.target.tagName==='DIALOG')e.target.close()});</script></html>''';old.write_text(html);print('Therapy choices first; approved Restaurant X2 and Vacation X7 retained below.')
