from pathlib import Path
from PIL import Image
import sys,subprocess,json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[3]
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
R=P/'review';N=P/'r2';B=N/'comparison';D=R/'round2';D.mkdir(exist_ok=True)
tool=ROOT/'.claude/skills/_shared/blind-image/blind.py'
if not (B/'.blind-key.json').exists():
 for k in 'abcd':
    subprocess.run([sys.executable,str(tool),'add',str(B),'--source','codex' if k in 'ab' else 'google','--file',str(N/'designed'/f'{k}-Instagram.png'),'--note',k],check=True,stdout=subprocess.DEVNULL)
 subprocess.run([sys.executable,str(tool),'build',str(B),'--kind','cover','--video','Kevin James Tried One Cheat Day A Week. It Wrecked His Diet. (DS-41)','--shot','DS-41 covers R2, four requested choices'],check=True)
old=R/'round1'
if not (old/'index.html').exists():
 old.mkdir(exist_ok=True)
 for f in R.glob('*.jpg'):shutil.copy2(f,old/f.name)
 page=(R/'index.html').read_text()
 page=page.replace('<main>','<main><p style="padding:18px;background:#682f25">Previous round. None of these eight covers was approved. <a href="../">Open the four new choices</a>.</p>',1)
 (old/'index.html').write_text(page)
key=json.loads((B/'.blind-key.json').read_text());mapped={};cards=[]
for label,item in key['labels'].items():
 k=item['note'];mapped[label]={}
 for pl in ['Instagram','YouTube']:
    src=N/'designed'/f'{k}-{pl}.png';im=Image.open(src).convert('RGB')
    im.save(D/f'{label}-{pl}.jpg',quality=94,subsampling=0)
    mapped[label][pl]={'original':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
 Image.open(N/'designed'/f'{k}-Grid.jpg').convert('RGB').save(D/f'{label}-Grid.jpg',quality=94,subsampling=0)
 cards.append(f'<article id="{label}"><h2>{label}</h2><div class="pair">'+''.join(f'<figure><figcaption>{pl}</figcaption><a href="round2/{label}-{pl}.jpg" target="_blank"><img src="round2/{label}-{pl}.jpg" alt="Round 2 {label} {pl} cover" width="1080" height="1920"></a></figure>' for pl in ['Instagram','YouTube'])+f'</div><details><summary>Instagram profile grid</summary><img class="gridcrop" src="round2/{label}-Grid.jpg" alt="{label} profile grid"></details></article>')
(N/'neutral-install-map.json').write_text(json.dumps(mapped,indent=2)+'\n')
shutil.copy2(N/'src/kevin-59.2.png',D/'podcast-frame.png')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kevin James Cheat SFC Setup | Round 2 Covers</title><style>
*{box-sizing:border-box}body{margin:0;background:#101823;color:#f5f2e9;font:17px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1250px;margin:auto;padding:24px 16px}h1{font-size:clamp(26px,4vw,40px);line-height:1.15;margin:12px 0}p{max-width:870px}a{color:#a4d9ff}.status{font-weight:700;color:#9fe1be}nav{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}nav a{padding:8px 15px;border:1px solid #50617a;border-radius:7px;text-decoration:none}.gallery{display:grid;grid-template-columns:1fr;gap:20px}article{background:#1b2636;border:1px solid #384a60;border-radius:12px;padding:14px;scroll-margin-top:15px}h2{font-size:25px;margin:0 0 10px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0;min-width:0}figcaption{font-size:14px;margin:0 0 8px}img{display:block;width:100%;height:auto;border-radius:4px}details{margin:16px 0}summary{cursor:pointer;color:#a4d9ff}.gridcrop{max-width:300px;margin-top:12px}footer{font-size:14px;color:#b8c4d1;margin:28px 0}@media(min-width:760px){.gallery{grid-template-columns:1fr 1fr}}@media(max-width:430px){main{padding:16px 10px}article{padding:10px}.pair{gap:8px}}
</style><main><div class="status">Round 2 • Four new choices • Waiting for your pick</div><h1>Kevin James Cheat Day</h1><p>Four new covers in your requested layout: the real podcast frame above, you with a huge mound of junk food below. Two images show you ripped and two show you fat.</p><p><strong>The top frame shows Kevin James only.</strong> I scanned the full 714-second source and inspected the shot changes. It alternates between Kevin and Joe; I found no frame with both together. Kevin's image uses real source pixels.</p><p>Choose <strong>one of X1 through X4</strong> for both layouts, for example <strong>“Round 2, use X2 for both.”</strong> Instagram appears first, YouTube beside it. Open the profile-grid preview to see the crop. Tap any cover to inspect the full image.</p><p>The film is unchanged. No cover is approved or installed. Nothing has been uploaded to publishing platforms, queued or scheduled.</p><nav>'''+''.join(f'<a href="#{k}">{k}</a>' for k in mapped)+'''<a href="round1/index.html">Previous round, not approved</a></nav><section class="gallery">'''+''.join(cards)+'''</section><details><summary>Real podcast source frame</summary><p>Kevin James at 59.2 seconds in the supplied JRE Clips source. <a href="round2/podcast-frame.png" target="_blank">Open original 1920 × 1080 frame</a>.</p></details><footer>Kevin James Tried One Cheat Day A Week. It Wrecked His Diet.<br>Cover round 2 • November 15, 2026. Setup stops here for your pick. This page contains no video or audio player.</footer></main></html>'''
(R/'index.html').write_text(page)
print('Packaged four neutral R2 choices in both layouts; R1 preserved at /round1/index.html.')
