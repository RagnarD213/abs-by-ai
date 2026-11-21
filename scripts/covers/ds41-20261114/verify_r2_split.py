from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np,urllib.request,io,re
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup/r2')
Q=P/'split';R=P.parent/'review';report=(Q/'independent-review.md').read_text()
assert 'VERDICT: PASS' in report
hashfile=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
snapshot=json.loads((Q/'pre-extension-hashes.json').read_text())
for filename,digest in snapshot.items():
 if filename==str(P/'neutral-install-map.json'):continue
 assert hashfile(filename)==digest,filename
combined=json.loads((P/'neutral-install-map.json').read_text())
old={k:v for k,v in combined.items() if int(k[1:])<=4}
oldbytes=(json.dumps(old,indent=2)+'\n').encode()
assert hashlib.sha256(oldbytes).hexdigest()==snapshot[str(P/'neutral-install-map.json')]
key=json.loads((P/'comparison/.blind-key.json').read_text())
expanded=json.loads((P/'comparison-expanded/.blind-key.json').read_text())
assert all(expanded['labels'][k]==v for k,v in key['labels'].items())
manifest=json.loads((Q/'layout-manifest.json').read_text());result=[]
sources={'Joe Rogan':Image.open(P/'src/joe-83.9.png').convert('RGB'),'Kevin James':Image.open(P/'src/kevin-59.2.png').convert('RGB')}
for r in manifest:
 im=Image.open(r['file']);base=Image.open(r['base_original']).convert('RGB')
 digest=hashfile(r['file']);assert digest==r['sha256'] and digest in report
 assert im.size==(1080,1920) and im.mode=='RGB' and r['jpg_bytes']<2_000_000
 x,y,x1,y1=r['podcast_bounds'];w=x1-x;h=y1-y;half=w//2
 panel=Image.new('RGB',(w,h))
 panel.paste(sources['Joe Rogan'].crop(r['source_crops']['Joe Rogan']).resize((half,h),Image.Resampling.LANCZOS),(0,0))
 panel.paste(sources['Kevin James'].crop(r['source_crops']['Kevin James']).resize((w-half,h),Image.Resampling.LANCZOS),(half,0))
 actual=np.asarray(im.crop((x,y,x1,y1)));expect=np.asarray(panel)
 allowed=np.zeros((h,w),bool);a,b,c,d=r['name_bounds'];allowed[b-y:d-y+1,a-x:c-x+1]=True;allowed[:,half:half+2]=True
 assert not np.any(np.any(actual!=expect,axis=2)&~allowed)
 outside=np.ones((1920,1080),bool);outside[y:y1,x:x1]=False
 assert np.array_equal(np.asarray(im)[outside],np.asarray(base)[outside])
 prior=r['same_lower_image_as'];assert int(r['label'][1:])==int(prior[1:])+4
 assert all(q['box'][1]>=(240 if r['platform']=='Instagram' else 0) and q['box'][3]<1620 for q in r['headline'])
 # The public JPEGs also preserve the lower photo pixel for pixel after decoding.
 newjpeg=np.asarray(Image.open(R/'round2'/f"{r['label']}-{r['platform']}.jpg").convert('RGB'))
 oldjpeg=np.asarray(Image.open(R/'round2'/f"{prior}-{r['platform']}.jpg").convert('RGB'))
 assert np.array_equal(newjpeg[r['photo_top']:],oldjpeg[r['photo_top']:])
 result.append({'label':r['label'],'platform':r['platform'],'sha256':digest,'same_lower_as':prior,'outside_top_pixel_identical':True,'real_source_exact_outside_caption_and_seam':True,'public_jpeg_lower_identical':True})
url='http://127.0.0.1:9868/';page=urllib.request.urlopen(url).read()
assert b'id="X8"' in page and b'two separate real frames side by side' in page
assert not re.search(rb'<(?:audio|video)\b',page,re.I)
assert not any(x in page.lower() for x in [b'codex',b'google',b'gemini',b'nano banana'])
served=[]
for f in sorted((R/'round2').glob('*')):
 data=urllib.request.urlopen(url+'round2/'+f.name).read();assert hashlib.sha256(data).hexdigest()==hashfile(f)
 Image.open(io.BytesIO(data)).load();served.append(f.name)
oldpage=urllib.request.urlopen(url+'round1/index.html').read();assert b'Previous round' in oldpage
req=urllib.request.Request(url+'round2/X5-Instagram.jpg',headers={'Range':'bytes=0-99'})
with urllib.request.urlopen(req) as resp:assert resp.status==206 and len(resp.read())==100
(Q/'checks.json').write_text(json.dumps({'checks':result,'existing_files_unchanged':True,'existing_map_entries_unchanged':True,'original_blind_key_unchanged':True,'no_reshuffle':True,'new_generation_calls':0,'all_round2_assets_served_and_decoded':served,'previous_round_reachable':True,'page_200':True,'range_206':True,'media_elements':0},indent=2)+'\n')
print('PASS: new8 layouts, oldfiles/key unchanged, exact lower pixels/order, real split sources, page200/range206.')
