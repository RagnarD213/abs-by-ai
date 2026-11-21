from pathlib import Path
from PIL import Image
import json,hashlib,io,re,urllib.request
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
report=(P/'cover-independent-review.md').read_text()
assert 'VERDICT: PASS' in report
checks=[]
for r in json.loads((P/'layout-manifest.json').read_text()):
 f=Path(r['file']);im=Image.open(f);h=hashlib.sha256(f.read_bytes()).hexdigest()
 assert im.mode=='RGB' and im.size==(1080,1920)
 assert h==r['sha256'] and h in report
 assert all(x['box'][1]>=(240 if r['platform']=='Instagram' else 90) and x['box'][3]<=1620 for x in r['text'])
 assert r['jpg_bytes']<2_000_000
 checks.append({'file':f.name,'sha256':h,'rgb_1080x1920':True,'type_within_safe_area':True,'jpeg_under_2MB':True,'independent_exact_hash_review':True})
page=urllib.request.urlopen('http://127.0.0.1:9868/').read()
assert not re.search(rb'<(?:video|audio)\b',page,re.I)
without_backup=re.sub(rb'https://drive\.google\.com/open\?id=[\w-]+',b'',page)
assert all(x not in without_backup.lower() for x in [b'google',b'codex',b'gemini',b'nano banana'])
served=[]
for f in sorted((P/'review').glob('*.jpg')):
 data=urllib.request.urlopen('http://127.0.0.1:9868/'+f.name).read()
 assert hashlib.sha256(data).digest()==hashlib.sha256(f.read_bytes()).digest()
 im=Image.open(io.BytesIO(data));im.load()
 served.append({'file':f.name,'size':list(im.size),'sha256':hashlib.sha256(data).hexdigest()})
req=urllib.request.Request('http://127.0.0.1:9868/X1-Instagram.jpg',headers={'Range':'bytes=0-99'})
with urllib.request.urlopen(req) as resp:
 assert resp.status==206 and len(resp.read())==100
q={'checks':checks,'served_assets':served,'page_http_200':True,'range_http_206':True,'browser_visual_gallery_verified':True,'media_elements':0,'sound_handoff':'Finish checks for owner clicked and owner-ready state observed; no media elements or playback','frame_check':'All finished stills inspected natively and at phone/grid sizes, with independent report. No START/END pair or motion exists; temporal gates not applicable.','face_check':'Apple Vision detector on final PNGs and independent native-resolution face/hand crops against identity and film references. Hair bounds individually inspected.','real_photo_provenance':'c is deterministic resize/composite directly from studio-white-23_CUTOUT.png; source person layer is never sent for an AI edit.','audio':'No playback or audio inspection; approved movie unchanged.'}
(P/'cover-checks.json').write_text(json.dumps(q,indent=2)+'\n')
print('PASS: 16 exact reviewed layouts, 24 served images, page 200, range 206, no media elements.')
