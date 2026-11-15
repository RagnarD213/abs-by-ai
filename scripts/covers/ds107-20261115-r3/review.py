#!/usr/bin/env python3
"""Round 3 requested Y choices first; existing Round 2 X choices below."""
from pathlib import Path
import json,subprocess,re,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[3]
R=P/'Short-form video content/covers/review/ds107-20261115-r3'
S=R/'comparison';O=R/'public';O.mkdir(exist_ok=True)
if not S.exists():
    for i in range(1,5):
        label=f'Y{i}'
        subprocess.run(['python3',str(P/'.claude/skills/_shared/blind-image/blind.py'),'add',str(S),'--source','codex','--file',str(R/'layouts'/label/'instagram/cover.png'),'--note',json.dumps({'label':label,'instagram':str(R/'layouts'/label/'instagram/cover.png'),'youtube':str(R/'layouts'/label/'youtube/cover.png')})],check=True,capture_output=True)
    subprocess.run(['python3',str(P/'.claude/skills/_shared/blind-image/blind.py'),'build',str(S),'--kind','cover','--video',"Your Metabolism Is Not The Reason You're Fat (DS-107)",'--shot','DS-107 requested conversation covers, Round 3','--comparison-unavailable',str(R/'google-subscription-failure.txt')],check=True,capture_output=True)
    # Adapt only this fresh key to Dan's requested Y labels; no earlier key read.
    p=S/'.blind-key.json';key=json.loads(p.read_text());mapped={};adapter={}
    for x,entry in key['labels'].items():
        y=json.loads(entry['note'])['label'];mapped[y]=entry;adapter[x]=y
    key['labels']={y:mapped[y] for y in sorted(mapped)}
    p.write_text(json.dumps(key,indent=2))
    (S/'label-adapter.json').write_text(json.dumps(adapter,indent=2))
cards=[];sheet=Image.new('RGB',(1120,1040),'#0b1f30');d=ImageDraw.Draw(sheet)
for i in range(1,5):
    k=f'Y{i}';clothing='Shirtless' if i<=2 else 'Tank Top'
    for j,platform in enumerate(['instagram','youtube']):
        im=Image.open(R/'layouts'/k/platform/'cover.png').convert('RGB')
        im.save(O/f'{k}-{platform}.jpg',quality=94)
        sheet.paste(im.resize((270,480),Image.Resampling.LANCZOS),((i-1)*280,30+j*520));d.text(((i-1)*280+5,j*520+8),'Round 3 '+k+' '+platform.title(),fill='white')
    Image.open(O/f'{k}-instagram.jpg').crop((0,240,1080,1680)).save(O/f'{k}-grid.jpg',quality=94)
    cards.append(f'''<article><h2>Round 3 · {k}</h2><p class="variant">{clothing}</p><div class="pair"><figure><figcaption>Instagram</figcaption><a href="{k}-instagram.jpg"><img src="{k}-instagram.jpg" alt="Round 3 {k}, Instagram" width="1080" height="1920"></a></figure><figure><figcaption>YouTube</figcaption><a href="{k}-youtube.jpg"><img src="{k}-youtube.jpg" alt="Round 3 {k}, YouTube" width="1080" height="1920"></a></figure></div><details><summary>Check Instagram Profile Crop</summary><img class="grid" src="{k}-grid.jpg" alt="Round 3 {k}, profile crop" width="1080" height="1440"></details></article>''')
sheet.save(O/'round3-all-covers.jpg',quality=94)
old=P/'Short-form video content/covers/review/ds107-20261115-r2/public';dest=O/'round2';dest.mkdir(exist_ok=True)
for p in [*old.glob('X*-*.jpg'),old/'all-covers.jpg']:
    if p.is_file() and not p.name.startswith('._'):shutil.copy2(p,dest/p.name)
archive=old.parent/'page-before-round3.html'
oldhtml=archive if archive.exists() else old/'index.html'
oldcards=''.join(re.findall(r'<article>.*?</article>',oldhtml.read_text(),re.S))
oldcards=re.sub(r'((?:href|src)=")([^"/]+\.jpg)"',r'\1round2/\2"',oldcards)
(O/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Metabolism Not The Reason: Round 3 Y1-Y4</title><style>
*{box-sizing:border-box}body{margin:0;background:#081a2a;color:#eef6ff;font:17px/1.5 system-ui,sans-serif}main{max-width:1450px;margin:auto;padding:24px 16px 60px}header{max-width:900px;margin-bottom:24px}h1{font-size:clamp(29px,4vw,44px);line-height:1.12;margin:12px 0 20px}h2{margin:0 0 10px;font-size:27px;color:#93eaff}a{color:#9aeeff}a:focus,summary:focus{outline:3px solid #ffda37;outline-offset:4px}.status{background:#163045;border-left:4px solid #ffda37;padding:13px 16px;margin:16px 0}.gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}article{padding:15px;border-radius:14px;border:1px solid #38546a;background:#102738}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}figcaption,.variant{font-size:14px;color:#c4d7e6;margin:0 0 8px}img{width:100%;height:auto;display:block;border-radius:4px}summary{cursor:pointer;color:#b9ecff;margin:16px 0}.grid{max-width:270px;margin:auto}small{color:#b8cbd9}.section-title{font-size:30px;color:#eef6ff;margin:46px 0 12px}nav{display:flex;gap:24px;flex-wrap:wrap;margin:20px 0}@media(max-width:650px){.gallery{grid-template-columns:1fr}main{padding-top:16px}h1{font-size:31px}article{padding:12px}.pair{gap:9px}}
</style><main><header><small>DS-107 · Your Requested Conversation Covers</small><h1>Your Metabolism Is Not The Reason You're Fat</h1><p>The four designs you requested are now first: <strong>Round 3 Y1–Y4</strong>. Two show Dan shirtless and two show him in a tank top. Each includes Instagram and YouTube layouts.</p><p>The man's bubble says <strong>“My metabolism slowed down.”</strong> Dan's says <strong>“No.”</strong></p><div class="status">Reply with Y1, Y2, Y3 or Y4, or request changes. Round 2 X1–X5 remain below as extra options. No cover is approved or installed; film and existing metadata are unchanged. Nothing has been scheduled.</div><nav><a href="#round3">Round 3 Y1–Y4</a><a href="#round2">Round 2 Extra Options</a><a href="round3-all-covers.jpg">All Four New Designs Together</a></nav></header><section id="round3" class="gallery">'''+''.join(cards)+'''</section><h2 id="round2" class="section-title">Round 2: Extra Options</h2><p>The previous five options are kept here unchanged. Specify X1–X5 if choosing one of these.</p><section class="gallery">'''+oldcards+'''</section></main></html>''')
# Keep the service's established source root, which its cache registry pins to
# this port. Preserve the previous HTML before updating the shared owner page.
if not archive.exists():shutil.copy2(old/'index.html',archive)
shutil.copytree(O,old,dirs_exist_ok=True)
print('Canonical Round 3 assets:',O)
print('Refresh the managed service using its established root:',old)
