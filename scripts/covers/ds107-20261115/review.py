#!/usr/bin/env python3
"""Publish neutral paired cover previews, without exposing the comparison key."""
from pathlib import Path
import json
import html
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parents[3]
R=P/'Short-form video content/covers/review/ds107-20261115'
out=R/'public';out.mkdir(exist_ok=True)
key=json.loads((R/'comparison/.blind-key.json').read_text())['labels']
cards=[]
sheet=Image.new('RGB',(1400,1040),'#071725');d=ImageDraw.Draw(sheet)
for i,(label,entry) in enumerate(key.items()):
    note=json.loads(entry['note'])
    for j,platform in enumerate(['instagram','youtube']):
        src=P/note[platform]
        im=Image.open(src).convert('RGB')
        im.save(out/f'{label}-{platform}.jpg',quality=93)
        phone=im.resize((270,480),Image.Resampling.LANCZOS)
        sheet.paste(phone,(i*280,j*520+30))
        d.text((i*280+8,j*520+10),label+' '+platform.title(),fill='white')
    ig=Image.open(out/f'{label}-instagram.jpg')
    ig.crop((0,240,1080,1680)).save(out/f'{label}-grid.jpg',quality=93)
    cards.append(f'''<article><h2>{label}</h2><div class="pair">
      <figure><figcaption>Instagram</figcaption><a href="{label}-instagram.jpg"><img src="{label}-instagram.jpg" alt="{label} Instagram cover" width="1080" height="1920"></a></figure>
      <figure><figcaption>YouTube</figcaption><a href="{label}-youtube.jpg"><img src="{label}-youtube.jpg" alt="{label} YouTube cover" width="1080" height="1920"></a></figure></div>
      <details><summary>Check Instagram profile crop</summary><img class="grid" src="{label}-grid.jpg" alt="{label} Instagram profile crop" width="1080" height="1440"></details></article>''')
sheet.save(out/'all-covers.jpg',quality=94)
cfg=json.loads((P/'scripts/blotato/configs/ds107-metabolism-not-the-reason.json').read_text())
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Metabolism Not The Reason: Cover Picks</title><style>
*{box-sizing:border-box}body{margin:0;background:#071725;color:#edf6ff;font:17px/1.5 system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:24px 16px 60px}header{max-width:850px;margin-bottom:28px}h1{font-size:clamp(28px,4vw,43px);line-height:1.12;margin:10px 0 18px}h2{font-size:28px;margin:0 0 14px;color:#7ee6ff}p{margin:12px 0}a{color:#8ae7ff}a:focus,summary:focus{outline:3px solid #ffdb46;outline-offset:4px}.status{border-left:4px solid #ffda4b;background:#152636;padding:12px 16px}.gallery{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}article{background:#112537;padding:14px;border:1px solid #2c495f;border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}figure{margin:0}figcaption{font-size:14px;color:#bad0df;margin-bottom:8px}img{display:block;width:100%;height:auto;border-radius:4px}summary{cursor:pointer;color:#a7e9ff;margin:15px 0}.grid{max-width:270px;margin:auto}details.packaging{margin-top:28px;padding:18px;border:1px solid #2c495f;border-radius:12px}.copy{white-space:pre-wrap;max-width:760px;font-size:16px}small{color:#a5bacb}@media(max-width:1050px){.gallery{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){main{padding-top:16px}.gallery{grid-template-columns:1fr;gap:24px}.pair{gap:9px}article{padding:12px}h1{font-size:31px}}
</style><main><header><small>DS-107 · Approved Film Setup · Cover Review</small><h1>Your Metabolism Is Not The Reason You're Fat</h1><p>Pick the cover you want: reply <strong>X1, X2, X3, X4 or X5</strong>. Each choice includes its Instagram and YouTube layout. Tap an image to inspect the full-size file.</p><div class="status">The film is approved and unchanged. These five covers have not been approved or installed. Three extra blind comparison options remain unavailable because the subscription browser cannot be accessed. Nothing is uploaded or scheduled.</div><p><a href="all-covers.jpg">Open all five together</a></p></header><section class="gallery">'''+''.join(cards)+'''</section><details class="packaging"><summary>Description and pinned question</summary><div class="copy">'''+html.escape(cfg['youtube_description'])+'''</div><h3>Pinned question</h3><p>'''+html.escape(cfg['pinned_comment'])+'''</p><small>The shared routine posts and pins this after release.</small></details></main></html>'''
(out/'index.html').write_text(page)
print(out)
