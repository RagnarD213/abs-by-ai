#!/usr/bin/env python3
"""RO-37 round 2 review page: two coaching scenes and four touched-up real gym screenshots."""
from pathlib import Path
from PIL import Image
O = Path(__file__).resolve().parents[4]/'social media graphics/youtube/thumbnails/First Time At The Gym'
D = O/'_build-2026-11-02-r2/designs'
R = O/'_review-r2'; R.mkdir(exist_ok=True)
ITEMS = [('A', 'T1', 'You in a tank top coaching a slightly overweight beginner on the chest press, guiding his elbow. Yellow band.'),
         ('B', 'T2', 'You crouched beside the beginner on the seated cable row, hand on his back. Stacked color blocks.'),
         ('C', 'R1', 'Real screenshot, touched up: you on the shoulder press, arms loaded, smiling. Navy top with white and blue type.'),
         ('D', 'R2', 'Real screenshot, touched up: you on the chest fly, arms spread wide. Words either side of your head.'),
         ('E', 'R3', 'Real screenshot, touched up: you on the chest press from the side, arm and shoulder up close. White and gold type.'),
         ('F', 'R4', 'Real screenshot, touched up: you on the lat pulldown, arms overhead. Red and white label strips.')]
for x, k, _ in ITEMS:
    im = Image.open(D/f'RO37-{k}.jpg').convert('RGB')
    im.save(R/f'{x}.jpg', quality=93)
    im.resize((320, 180), Image.Resampling.LANCZOS).save(R/f'{x}-phone.jpg', quality=93)
css = ':root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1180px;margin:auto;padding:24px 16px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px}section{background:var(--card);border-radius:12px;padding:14px}img{width:100%;display:block;border-radius:6px}h2{margin:0 0 4px}p{color:var(--dim);margin:0 0 10px}.s{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}.s figure{margin:0;width:160px}.s img{width:160px}.s figcaption{font-size:14px;text-align:center}'
h = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>First Time Gym Thumbnails R2</title><style>{css}</style></head><body><main><h1>I&#39;m 41. Here&#39;s What I&#39;d Do If I Walked Into A Gym For The First Time: six new thumbnails</h1><p>A and B are new AI scenes of you coaching a beginner. C to F are real screenshots from your October 23 gym footage, touched up to make you look as ripped as possible. Same words on all six. My recommendation is A: you coaching a regular guy tells a beginner this video is for him, and the yellow band is the look you pick most. Pick one, or two for a test.</p><div class="g">']
for x, k, t in ITEMS:
    h.append(f'<section id="{x}"><h2>{x}</h2><p>{t}</p><a href="{x}.jpg"><img src="{x}.jpg" alt="{x}"></a></section>')
h.append('</div><h2 style="margin-top:28px">Phone size</h2><div class="s">')
for x, k, t in ITEMS:
    h.append(f'<figure><img src="{x}-phone.jpg" alt="{x} at phone size"><figcaption>{x}</figcaption></figure>')
h.append('</div></main></body></html>')
(R/'index.html').write_text(''.join(h)); print('ok')
