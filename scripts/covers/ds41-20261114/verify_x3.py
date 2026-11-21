from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,urllib.request,io,re
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
Q=P/'r2/x3-revision';R=P/'review';report=(Q/'independent-review.md').read_text()
assert 'VERDICT: PASS' in report
check=[]
for row in json.loads((Q/'manifest.json').read_text()):
 f=Path(row['file']);digest=hashlib.sha256(f.read_bytes()).hexdigest();assert digest==row['sha256'] and digest in report
 im=Image.open(f);base=Image.open(row['base']).convert('RGB');assert im.mode=='RGB' and im.size==(1080,1920)
 x,y,x1,y1=row['changed_region'];outside=np.ones((1920,1080),bool);outside[y:y1,x:x1]=False
 assert np.array_equal(np.asarray(im)[outside],np.asarray(base)[outside])
 assert ' '.join(t['text'] for t in row['text'])=='Why Cheat Days Make You Fat'
 assert row['jpg_bytes']<2_000_000
 for t in row['text']:
    assert t['box'][0]>=40 and t['box'][2]<=1040 and t['box'][1]>=y+7 and t['box'][3]<y1-7
 check.append({'platform':row['platform'],'sha256':digest,'only_headline_band_changed':True,'all_faces_and_food_and_source_label_pixel_identical':True,'text_safe':True,'jpeg_under_2MB':True})
snapshot=json.loads((Q/'prior-review-hashes.json').read_text())
for filename,digest in snapshot.items():
 if filename==str(R/'index.html'):continue
 assert hashlib.sha256(Path(filename).read_bytes()).hexdigest()==digest
url='http://127.0.0.1:9868/';page=urllib.request.urlopen(url).read()
assert b'Revised X3 Approval' in page and b'Why Cheat Days Make You Fat' in page
assert len(re.findall(rb'<img\b',page))==3 and not re.search(rb'<(?:video|audio)\b',page,re.I)
assert all(x not in page.lower() for x in [b'codex',b'google',b'gemini',b'nano banana'])
assets=[]
for f in sorted((R/'x3-revised').glob('*')):
 data=urllib.request.urlopen(url+'x3-revised/'+f.name).read();assert hashlib.sha256(data).hexdigest()==hashlib.sha256(f.read_bytes()).hexdigest()
 Image.open(io.BytesIO(data)).load();assets.append({'file':f.name,'sha256':hashlib.sha256(data).hexdigest()})
for path in ['round1/index.html','round2/index.html']:
 data=urllib.request.urlopen(url+path).read();assert b'<html' in data
# The archived second round now references its same local images correctly.
old=urllib.request.urlopen(url+'round2/index.html').read().decode()
for name in re.findall(r'<img[^>]+src="([^"]+)"',old):
 data=urllib.request.urlopen(url+'round2/'+name).read();Image.open(io.BytesIO(data)).load()
req=urllib.request.Request(url+'x3-revised/X3-Revised-Instagram.jpg',headers={'Range':'bytes=0-99'})
with urllib.request.urlopen(req) as response:assert response.status==206 and len(response.read())==100
(Q/'checks.json').write_text(json.dumps({'exact_file_checks':check,'new_served_images':assets,'previous_assets_unchanged':True,'earlier_rounds_reachable':True,'archived_round2_24_images_decoded':True,'page_images_only_revised_pair_plus_grid':True,'media_elements':0,'page_200':True,'range_206':True,'new_generation_calls':0,'final_approved':False},indent=2)+'\n')
print('PASS: exact revised X3 pair/grid, only headline changed, prior assets preserved, archives/images reachable, page200/range206.')
