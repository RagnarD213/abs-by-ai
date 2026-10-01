from pathlib import Path
from PIL import Image,ImageCms
import json,hashlib,re,csv,io
R=Path(__file__).resolve().parent
posts=json.loads((R/'posts.json').read_text());checks=[]
assert len(posts)==24 and len({p['source'] for p in posts})==24
assert all(sum(p['style']==s for p in posts)==3 for s in range(1,9))
assert sum(p['slides'] for p in posts)==48
expected={f'{p["id"]}-{i:02}.jpg' for p in posts for i in range(1,p['slides']+1)}
assert {p.name for p in (R/'images').glob('*.jpg')}==expected
for file in sorted((R/'images').glob('*.jpg')):
 im=Image.open(file);assert im.size==(1080,1350) and im.mode=='RGB';assert im.info.get('icc_profile')
 desc=ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(im.info['icc_profile']))).strip()
 assert 'sRGB' in desc
 checks.append(dict(file=file.name,width=im.width,height=im.height,color_profile=desc,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
for file in R.rglob('*'):
 if file.is_file() and file.suffix in ['.py','.cjs','.html','.json','.txt','.csv','.svg']:
  s=file.read_text();assert '\u2014' not in s and '\u2013' not in s,file
bounds=json.loads((R/'qa/text-bounds.json').read_text());assert all(b['right']<=1030 for b in bounds)
html=(R/'index.html').read_text();assert html.count('<article ')==24
assert len(list(csv.DictReader((R/'results-ledger.csv').open())))==24
for p in posts:
 for i in range(1,p['slides']+1):assert f'images/{p["id"]}-{i:02}.jpg' in html
assert all(not r.get(k) for r in csv.DictReader((R/'results-ledger.csv').open()) for k in ['reach','likes','comments','saves','shares','profile_visits','follows'])
report=dict(status='PASS',posts=24,images=48,single_image_posts=18,carousels=6,distinct_shirtless_sources=24,styles=list(range(1,9)),caption_count=24,waistband_crop_ids=[p['id'] for p in posts if p['crop']['waistband_crop']],no_scheduling_or_publishing=True,visual_review='Every final image reviewed at phone size. All six sequences reviewed in order. Both hips checked in three tight crops. Full hair, unobstructed face and abs, text placement, spelling and cutout edges inspected.',browser_review='Style filter and full-size viewer verified. Next-slide navigation opens slide 2 of 5.',font_check='Explicit glyph outlines used for export; all text within horizontal safe bound.',generation=dict(tool='built-in image_gen',calls=3,reported_cost=None),files=checks)
(R/'qa/validation.json').write_text(json.dumps(report,indent=2));print('PASS: 24 posts / 48 sRGB exports / 24 captions / 24 unique sources / 0 text overflows / no em or en dashes.')
