#!/usr/bin/env python3
"""Publish only the four revised cover choices; preserve the rejected prior set."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,os,shutil,subprocess
ROOT=Path(os.environ.get('ABS_PROJECT_ROOT') or Path(__file__).resolve().parents[3])
BASE=ROOT/'Short-form video content/covers/review/ds36-20261105';R=BASE/'round2';P=BASE/'blind-review';P.mkdir(exist_ok=True)
check=json.loads((R/'cover-checks.json').read_text());assert check['all_passed'] and len(check['checks'])==8
archive=BASE/'round1-review-preserved'
if not archive.exists():shutil.copytree(P,archive,ignore=shutil.ignore_patterns('._*'))
for k in '1234':
 label=f'M{k}'
 shutil.copy2(R/'instagram'/f'{label}.png',P/f'{label}-instagram.png');shutil.copy2(R/'youtube'/f'{label}.jpg',P/f'{label}-youtube.jpg')
 im=Image.open(R/'instagram'/f'{label}.png');im.crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS).save(P/f'{label}-grid.jpg',quality=95)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',25);sheet=Image.new('RGB',(1200,1140),'#111A27');draw=ImageDraw.Draw(sheet)
for i,k in enumerate('1234'):
 for j,pf in enumerate(['instagram','youtube']):
  im=Image.open(R/pf/f'M{k}.png');im.thumbnail((280,500));x=i*300;y=j*570;sheet.paste(im,(x+10,y+55));draw.text((x+12,y+14),f'M{k} / '+('Instagram' if j==0 else 'YouTube'),font=font,fill='white')
sheet.save(R/'four-cover-choices.jpg',quality=95);shutil.copy2(R/'four-cover-choices.jpg',P/'new-four-mirror-choices.jpg')
key=R/'.blind-key.json'
if not key.exists():
 helper=ROOT/'.claude/skills/_shared/blind-image/blind.py'
 for k in '1234':subprocess.run(['python3',str(helper),'add',str(R),'--source','codex','--file',str(R/'instagram'/f'M{k}.png'),'--note',f'revision M{k}; explicit four AI heavier mirror designs'],check=True,capture_output=True)
 reg=json.loads((R/'.blind-registry.json').read_text());assert len(reg)==4
 labels={f'M{i}':{'source':v['source'],'original':v['file'],'sha':v['sha'],'note':v['note']} for i,v in enumerate(reg,1)}
 key.write_text(json.dumps({'video':'Why Fat Shaming Is Good (DS-36)','shot':'Four Heavier Mirror Cover Revisions','kind':'cover-revision','comparison':False,'requested_count':4,'labels':labels},indent=2))
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#101823;color:#f2f5fa;font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1240px;margin:auto;padding:24px 18px}h1{margin:0;font-size:32px}p{color:#c8d5e5;max-width:900px}a{color:#91d9ff}.overview{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:22px 0}.overview a{display:block;text-decoration:none;background:#1c2a3d;padding:10px;border-radius:10px}.overview strong{display:block;margin-bottom:8px}img{display:block;width:100%;height:auto;border-radius:5px}section{background:#1a2637;border:1px solid #34475f;border-radius:12px;padding:22px;margin:24px 0}h2{margin:0 0 12px}.pair{display:grid;grid-template-columns:1fr 1fr .7fr;gap:18px;align-items:start}figure{margin:0;min-width:0}figcaption{font-size:14px;color:#cad4e4;margin-bottom:8px}small{color:#b9c8db}@media(max-width:700px){main{padding:20px 12px}h1{font-size:27px}.overview{grid-template-columns:1fr 1fr;gap:12px}.pair{grid-template-columns:1fr 1fr;gap:12px}section{padding:14px}.grid{grid-column:1/3;max-width:230px}}'''
headings={'1':'Warm Bathroom Mirror','2':'Dark Side View','3':'Black And White Mirror','4':'Oak-Framed Reflection'}
h=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Why Fat Shaming Is Good: New Mirror Covers</title><style>{css}</style></head><body><main><h1>Why Fat Shaming Is Good</h1><p>Four new mirror designs showing the heavier version of you with the ashamed expression you requested. Choose M1, M2, M3 or M4. Each has separate Instagram and YouTube layouts.</p><nav class="overview">']
for k in '1234':h.append(f'<a href="#M{k}"><strong>M{k}</strong><img src="M{k}-grid.jpg" alt="M{k} profile crop"></a>')
h.append('</nav>')
for k in '1234':
 h.append(f'<section id="M{k}"><h2>M{k}: {headings[k]}</h2><div class="pair">')
 for pf,title,ext in [('instagram','Instagram','png'),('youtube','YouTube Shorts','jpg'),('grid','Instagram Profile Crop','jpg')]:h.append(f'<figure class="{"grid" if pf=="grid" else ""}"><figcaption>{title}</figcaption><a href="M{k}-{pf}.{ext}"><img loading="lazy" src="M{k}-{pf}.{ext}" alt="M{k} {title}"></a></figure>')
 h.append('</div></section>')
h.append('<p><a href="new-four-mirror-choices.jpg">Open the full comparison sheet</a></p><p>Reply with M1 to M4, or name a change. The video remains approved and unchanged. Publishing setup is waiting for your cover approval.</p></main></body></html>')
(P/'index.html').write_text(''.join(h));rows=[]
for k in '1234':
 for pf,ext in [('instagram','png'),('youtube','jpg')]:
  p=P/f'M{k}-{pf}.{ext}';rows.append({'label':f'M{k}','platform':pf,'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(R/'neutral-delivery-manifest.json').write_text(json.dumps({'title':'Why Fat Shaming Is Good','status':'awaiting Dan revised cover pick','review_url':'http://127.0.0.1:10336/','outputs':rows},indent=2));print('Four revised mirror choices ready at existing review URL')
