from pathlib import Path
import subprocess,sys,json,re,html,hashlib,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
B=P/'comparison';R=P/'review';R.mkdir(exist_ok=True)
tool=ROOT/'.claude/skills/_shared/blind-image/blind.py'
if not (B/'.blind-key.json').exists():
 for k in ['a','b','c','d','e','g1','g2','g3']:
    args=[sys.executable,str(tool),'add',str(B),'--source','google' if k.startswith('g') else 'codex','--file',str(P/'designed'/f'{k}-Instagram.png'),'--note',k]
    if k=='c':args+=['--not-comparison']
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)
 subprocess.run([sys.executable,str(tool),'build',str(B),'--kind','cover','--video','Kevin James Tried One Cheat Day A Week. It Wrecked His Diet. (DS-41)','--shot','DS-41 covers R1'],check=True)
key=json.loads((B/'.blind-key.json').read_text())
cards=[];mapped={}
for label,item in key['labels'].items():
 k=item['note']; mapped[label]={}
 for platform in ['Instagram','YouTube']:
    src=P/'designed'/f'{k}-{platform}.png'
    im=Image.open(src).convert('RGB')
    # Same output size, encoding and neutral filenames for all review entries.
    im.save(R/f'{label}-{platform}.jpg',quality=94,subsampling=0)
    mapped[label][platform]={'original':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
 im=Image.open(P/'designed'/f'{k}-Instagram.png').crop((0,240,1080,1680))
 im.save(R/f'{label}-Grid.jpg',quality=94,subsampling=0)
 cards.append(f'''<article id="{label}"><h2>{label}</h2><div class="pair">'''+''.join(f'''<figure><figcaption>{pl}</figcaption><a href="{label}-{pl}.jpg" target="_blank"><img loading="lazy" src="{label}-{pl}.jpg" alt="{label} {pl} cover" width="1080" height="1920"></a></figure>''' for pl in ['Instagram','YouTube'])+f'''</div><details><summary>Instagram profile grid</summary><img class="crop" loading="lazy" src="{label}-Grid.jpg" alt="{label} Instagram grid crop"></details></article>''')
(P/'neutral-install-map.json').write_text(json.dumps(mapped,indent=2))
draft=(P/'metadata/draft.txt').read_text()
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kevin James Cheat SFC Setup | Cover Choices</title><style>
*{box-sizing:border-box}body{margin:0;background:#101823;color:#f4f1e8;font:17px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1250px;margin:auto;padding:24px 16px}h1{font-size:clamp(25px,4vw,39px);line-height:1.14;max-width:900px;margin:12px 0}p{max-width:850px}.status{color:#9adcc7;font-weight:650}nav{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0}a{color:#9fd6ff}nav a{padding:8px 14px;border:1px solid #516278;border-radius:7px;text-decoration:none}.gallery{display:grid;grid-template-columns:1fr;gap:20px}article{background:#1b2636;border:1px solid #384a60;border-radius:12px;padding:14px;scroll-margin-top:16px}h2{font-size:25px;margin:0 0 8px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0;min-width:0}figcaption{font-size:14px;margin:0 0 8px;color:#dce2e8}img{display:block;width:100%;height:auto;border-radius:4px}details{margin-top:16px}summary{cursor:pointer;color:#9fd6ff}.crop{max-width:270px;margin-top:12px}pre{white-space:pre-wrap;font:16px/1.6 -apple-system,sans-serif}footer{padding:28px 0;color:#b7c3d0;font-size:14px}@media(min-width:760px){.gallery{grid-template-columns:1fr 1fr}}@media(max-width:430px){main{padding:16px 10px}.pair{gap:8px}article{padding:10px}}
</style><main><div class="status">Film approved November 14 • Cover pick needed</div><h1>Kevin James Tried One Cheat Day A Week. It Wrecked His Diet.</h1><p>Choose one cover from <strong>X1 to X8</strong>. Each choice has an Instagram layout first and a YouTube layout beside it. Tap a cover to inspect the full image. Reply in this chat with your pick, for example <strong>“Use X3 for both.”</strong></p><p>The approved film is unchanged. Backups and metadata are prepared. Nothing has been uploaded to the publishing platforms, queued or scheduled.</p><nav>'''+''.join(f'<a href="#{x}">{x}</a>' for x in mapped)+'''</nav><section class="gallery">'''+''.join(cards)+'''</section><details><summary>Prepared title, description and captions</summary><pre>'''+html.escape(draft)+'''</pre></details><details><summary>Verified backup</summary><p><a href="https://drive.google.com/open?id=1JUV6CjwgPEncwyDIHimFe5uuXsNE5YDj" target="_blank">Approved film and subtitle backup</a>. The video and subtitles match the approved files. Drive sharing was checked without signing in.</p></details><footer>Kevin James Cheat SFC Setup • November 14, 2026<br>Setup pauses here for your cover pick. This page has no video or audio player.</footer></main></html>'''
(R/'index.html').write_text(page)
print('Packaged',len(mapped),'neutral choices in both layouts.')
