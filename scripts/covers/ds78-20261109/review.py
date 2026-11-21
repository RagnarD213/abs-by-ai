#!/usr/bin/env python3
"""Shuffle once with the shared blind tool, pair platform files, publish only neutral labels."""
from pathlib import Path
import json,subprocess,sys,shutil,hashlib,socket
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[3];O=R/'Short-form video content/covers/review/ds78-chest-flies-20261109';B=O/'blind-set';P=O/'page';P.mkdir(exist_ok=True);I=P/'img';I.mkdir(exist_ok=True)
rows=json.loads((O/'manifest-private.json').read_text());tool=R/'.claude/skills/_shared/blind-image/blind.py'
if not (B/'.blind-key.json').exists():
 for r in rows:
  if r['platform']!='instagram':continue
  cmd=[sys.executable,str(tool),'add',str(B),'--source',r['source'],'--file',r['path'],'--note',r['design']]
  if not r['comparison_eligible']:cmd.append('--not-comparison')
  subprocess.run(cmd,check=True,capture_output=True)
 subprocess.run([sys.executable,str(tool),'build',str(B),'--kind','cover','--video','How To Do Chest Flies On The Machine (DS-78)','--shot','Initial cover choices'],check=True)
key=json.loads((B/'.blind-key.json').read_text());items=[];sheet=Image.new('RGB',(1080,1020),'#101925');sd=ImageDraw.Draw(sheet)
for i,(label,k) in enumerate(key['labels'].items()):
 design=k['note'];rs={r['platform']:r for r in rows if r['design']==design};obj={'label':label,'files':{}}
 for platform,r in rs.items():
  src=Path(r['path']);dst=I/f'{label}-{platform}.png';shutil.copy2(src,dst)
  # Both full-res files are normalized to RGB PNG with no inherited metadata.
  im=Image.open(src).convert('RGB');im.save(dst)
  obj['files'][platform]={'file':dst.name,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'bytes':dst.stat().st_size,'size':list(im.size)}
  if platform=='youtube':im.save(I/f'{label}-youtube.jpg',quality=93)
 im=Image.open(I/f'{label}-instagram.png');grid=im.crop((0,240,1080,1680));grid.save(I/f'{label}-grid.jpg',quality=94)
 sm=grid.copy();sm.thumbnail((270,360));x=i%4*270;y=i//4*500;sheet.paste(sm,(x,y+40));sd.text((x+8,y+12),label,fill='white')
 items.append(obj)
sheet.crop((0,0,1080,920)).save(I/'all-options.jpg',quality=94)
nav=''.join(f'<a href="#{r["label"]}">{r["label"]}</a>' for r in items)
sections=''
for r in items:
 l=r['label'];sections+=f'<section id="{l}"><h2>{l}</h2><div class="pair"><figure><figcaption>Instagram</figcaption><a href="img/{l}-instagram.png"><img src="img/{l}-instagram.png" alt="{l} Instagram" loading="lazy"></a></figure><figure><figcaption>YouTube Shorts</figcaption><a href="img/{l}-youtube.png"><img src="img/{l}-youtube.png" alt="{l} YouTube Shorts" loading="lazy"></a></figure><figure class="crop"><figcaption>Instagram Profile Grid</figcaption><a href="img/{l}-grid.jpg"><img src="img/{l}-grid.jpg" alt="{l} Instagram profile crop" loading="lazy"></a></figure></div></section>'
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chest Flies Cover Choices</title><style>
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:70px}body{margin:0;background:#0d1521;color:#f3f6fb;font:16px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1220px;margin:auto;padding:18px}h1{font-size:28px;line-height:1.15;margin:12px 0}p{color:#c8d5e4;max-width:850px}.status{color:#9ce8c2}nav{position:sticky;top:0;display:flex;flex-wrap:wrap;gap:6px;padding:10px 0;background:#0d1521;z-index:2}nav a{color:#e7f0ff;border:1px solid #4b6583;border-radius:7px;padding:6px 13px;text-decoration:none}section{scroll-margin-top:20px;margin:22px 0;padding:14px;background:#172334;border:1px solid #33465f;border-radius:12px}h2{margin:0 0 12px;font-size:24px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}figcaption{margin-bottom:7px;font-size:14px;color:#cad6e6}img{display:block;width:100%;height:auto;border-radius:5px}.crop{grid-column:1/3;max-width:220px}.overview{max-width:1000px;margin:20px auto}a{color:#8acaff}@media(min-width:850px){main{padding:28px}h1{font-size:38px}.pair{grid-template-columns:1fr 1fr .72fr;gap:20px}.crop{grid-column:auto;max-width:none}}@media(max-width:430px){main{padding:12px}section{padding:10px}.pair{gap:8px}nav a{padding:5px 10px}figcaption{font-size:12px}}
</style></head><body><main><h1>How To Do Chest Flies</h1><p>Eight cover choices. Each option includes its Instagram layout, YouTube Shorts layout and Instagram profile crop. Tap any picture to inspect the full-size file.</p><p><strong>Reply in chat with your preferred label, X1 to X8.</strong> You can name separate Instagram and YouTube picks.</p><p class="status">The finalized R1 film is preserved exactly. Nothing has been uploaded or scheduled. This review is for the cover only.</p><nav>'''+nav+'''</nav><details class="overview"><summary>See All Eight At Once</summary><a href="img/all-options.jpg"><img src="img/all-options.jpg" alt="All eight cover choices"></a></details>'''+sections+'''</main></body></html>'''
(P/'index.html').write_text(html);(O/'manifest-neutral.json').write_text(json.dumps(items,indent=2))
print('Review built:',P)
