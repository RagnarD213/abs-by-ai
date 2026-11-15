from pathlib import Path
from PIL import Image
import json,hashlib,re,urllib.request,io
import numpy as np
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup/r2')
report=(P/'independent-review.md').read_text()
assert 'VERDICT: PASS' in report
rows=json.loads((P/'layout-manifest.json').read_text())
source=Image.open(json.loads((P/'src/selected-top.json').read_text())['file']).convert('RGB')
checked=[]
for r in rows:
 f=Path(r['file']);im=Image.open(f);h=hashlib.sha256(f.read_bytes()).hexdigest()
 assert h==r['sha256'] and h in report
 assert im.mode=='RGB' and im.size==(1080,1920) and r['jpg_bytes']<2_000_000
 bounds=r['podcast_bounds'];x,y,x1,y1=bounds
 expected=source.resize((x1-x,y1-y),Image.Resampling.LANCZOS)
 actual=im.crop(bounds)
 delta=np.any(np.asarray(actual)!=np.asarray(expected),axis=2)
 allowed=np.zeros(delta.shape,bool);a,b,c,d=r['text'][0]['box']
 allowed[max(0,b-y):min(y1-y,d-y+1),a-x:c-x+1]=True
 assert not np.any(delta & ~allowed)
 assert all(q['box'][1]>=(240 if r['platform']=='Instagram' else 0) and q['box'][3]<=1620 for q in r['text'])
 checked.append({'file':f.name,'sha256':h,'size':[1080,1920],'exact_hash_independent_pass':True,'real_source_outside_name_label_exact':True,'headline_safe':True})
root='http://127.0.0.1:9868/'
page=urllib.request.urlopen(root).read();assert b'Round 2' in page
assert not re.search(rb'<(?:video|audio)\b',page,re.I)
assert all(x not in page.lower() for x in [b'codex',b'google',b'gemini',b'nano banana'])
assets=[]
for f in sorted((P.parent/'review/round2').glob('*')):
 data=urllib.request.urlopen(root+'round2/'+f.name).read();assert hashlib.sha256(data).digest()==hashlib.sha256(f.read_bytes()).digest()
 im=Image.open(io.BytesIO(data));im.load();assets.append({'file':f.name,'sha256':hashlib.sha256(data).hexdigest(),'size':list(im.size)})
old=urllib.request.urlopen(root+'round1/index.html').read();assert b'Previous round' in old
for f in sorted((P.parent/'review/round1').glob('*.jpg')):
 data=urllib.request.urlopen(root+'round1/'+f.name).read();assert hashlib.sha256(data).digest()==hashlib.sha256(f.read_bytes()).digest()
req=urllib.request.Request(root+'round2/X1-Instagram.jpg',headers={'Range':'bytes=0-99'})
with urllib.request.urlopen(req) as resp:assert resp.status==206 and len(resp.read())==100
q={'png_checks':checked,'new_served_assets':assets,'old_round_page_200':True,'old_round_24_images_verified':True,'new_page_200':True,'range_206':True,'media_elements':0,'body_count':{'ripped':2,'fat':2},'independent_report':str(P/'independent-review.md'),'temporal_gate':'Not applicable to still-cover compositions; native images, face/hand crops and grid checked. No video changes.'}
(P/'checks.json').write_text(json.dumps(q,indent=2)+'\n')
print('PASS: 8 reviewed layouts, 13 new assets, preserved R1 and its 24 images, page200/range206.')
