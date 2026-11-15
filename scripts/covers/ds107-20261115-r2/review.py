#!/usr/bin/env python3
"""Fresh neutral review publication. Only this new round's key may be read."""
from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parents[3]
R=P/'Short-form video content/covers/review/ds107-20261115-r2'
S=R/'comparison'
if not S.exists():
    for k in 'ABCDE':
        args=['python3',str(P/'.claude/skills/_shared/blind-image/blind.py'),'add',str(S),'--source','codex','--file',str(R/'layouts'/k/'instagram/cover.png'),'--note',json.dumps({'design':k,'instagram':str(R/'layouts'/k/'instagram/cover.png'),'youtube':str(R/'layouts'/k/'youtube/cover.png')})]
        if k=='C':args+=['--not-comparison']
        subprocess.run(args,check=True,capture_output=True)
    subprocess.run(['python3',str(P/'.claude/skills/_shared/blind-image/blind.py'),'build',str(S),'--kind','cover','--video',"Your Metabolism Is Not The Reason You're Fat (DS-107)",'--shot','DS-107 new cover round 2','--comparison-unavailable',str(R/'comparison-unavailable.txt')],check=True)
key=json.loads((S/'.blind-key.json').read_text())['labels']
out=R/'public';out.mkdir(exist_ok=True);cards=[]
sheet=Image.new('RGB',(1400,1040),'#0a1a29');d=ImageDraw.Draw(sheet)
for i,(label,entry) in enumerate(key.items()):
    note=json.loads(entry['note'])
    for j,platform in enumerate(['instagram','youtube']):
        im=Image.open(note[platform]).convert('RGB');im.save(out/f'{label}-{platform}.jpg',quality=93)
        sheet.paste(im.resize((270,480),Image.Resampling.LANCZOS),(i*280,30+j*520));d.text((i*280+5,j*520+8),'Round 2 '+label+' '+platform.title(),fill='white')
    Image.open(out/f'{label}-instagram.jpg').crop((0,240,1080,1680)).save(out/f'{label}-grid.jpg',quality=93)
    cards.append(f'''<article><h2>Round 2 · {label}</h2><div class="pair"><figure><figcaption>Instagram</figcaption><a href="{label}-instagram.jpg"><img src="{label}-instagram.jpg" alt="Round 2 {label}, Instagram" width="1080" height="1920"></a></figure><figure><figcaption>YouTube</figcaption><a href="{label}-youtube.jpg"><img src="{label}-youtube.jpg" alt="Round 2 {label}, YouTube" width="1080" height="1920"></a></figure></div><details><summary>Check Instagram profile crop</summary><img class="grid" src="{label}-grid.jpg" alt="Round 2 {label}, profile crop" width="1080" height="1440"></details></article>''')
sheet.save(out/'all-covers.jpg',quality=94)
(out/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Metabolism Not The Reason: New Cover Round 2</title><style>
*{box-sizing:border-box}body{margin:0;background:#081a2a;color:#eef6ff;font:17px/1.5 system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:24px 16px 60px}header{max-width:850px;margin-bottom:28px}h1{font-size:clamp(29px,4vw,44px);line-height:1.12;margin:12px 0 20px}h2{margin:0 0 14px;font-size:25px;color:#93eaff}a{color:#9aeeff}a:focus,summary:focus{outline:3px solid #ffda37;outline-offset:4px}.status{background:#163045;border-left:4px solid #ffda37;padding:14px 16px;margin:18px 0}.gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}article{padding:14px;border-radius:14px;border:1px solid #38546a;background:#102738}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}figure{margin:0}figcaption{font-size:14px;color:#c4d7e6;margin-bottom:8px}img{width:100%;height:auto;display:block;border-radius:4px}summary{cursor:pointer;color:#b9ecff;margin:16px 0}.grid{max-width:270px;margin:auto}small{color:#b8cbd9}@media(max-width:1050px){.gallery{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.gallery{grid-template-columns:1fr}main{padding-top:16px}h1{font-size:31px}article{padding:12px}}
</style><main><header><small>DS-107 · A Fresh Cover Round · November 15</small><h1>Your Metabolism Is Not The Reason You're Fat</h1><p>Five new designs, each paired for Instagram and YouTube. Reply <strong>Round 2 X1, X2, X3, X4 or X5</strong> with your pick or changes. Tap a picture for full size.</p><div class="status">The previous covers are rejected and preserved as evidence. These are new images and a new review set. The three extra blind alternatives remain unavailable after a fresh subscription-browser retry. No cover is approved or installed. Film and existing metadata are unchanged; nothing has been scheduled.</div><p><a href="all-covers.jpg">See all five together</a></p></header><section class="gallery">'''+''.join(cards)+'''</section></main></html>''')
print(out)
