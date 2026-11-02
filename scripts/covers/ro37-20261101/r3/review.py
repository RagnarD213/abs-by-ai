#!/usr/bin/env python3
"""RO-37 round 3 review page: design C with Dan's new copy, three text treatments."""
from pathlib import Path
from PIL import Image
O = Path(__file__).resolve().parents[4]/'social media graphics/youtube/thumbnails/First Time At The Gym'
D = O/'_build-2026-11-02-r3/designs'
R = O/'_review-r3'; R.mkdir(exist_ok=True)
ITEMS = [('C1', 'V1', 'Huge white headline across the top, then the answer on a tilted yellow tag, like a sticker slapped on.'),
         ('C2', 'V2', 'The question on a small red label, then a giant yellow 3D "Here\'s What To Do" as the main hook.'),
         ('C3', 'V3', 'A glowing neon sign hanging from the gym ceiling: blue-white question, warm yellow answer.')]
for x, k, _ in ITEMS:
    im = Image.open(D/f'RO37-C-{k}.jpg').convert('RGB')
    im.save(R/f'{x}.jpg', quality=93)
    im.resize((320, 180), Image.Resampling.LANCZOS).save(R/f'{x}-phone.jpg', quality=93)
css = ':root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1180px;margin:auto;padding:24px 16px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px}section{background:var(--card);border-radius:12px;padding:14px}img{width:100%;display:block;border-radius:6px}h2{margin:0 0 4px}p{color:var(--dim);margin:0 0 10px}.s{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}.s figure{margin:0;width:160px}.s img{width:160px}.s figcaption{font-size:14px;text-align:center}'
h = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>First Time Gym Thumbnail C</title><style>{css}</style></head><body><main><h1>I&#39;m 41. Here&#39;s What I&#39;d Do If I Walked Into A Gym For The First Time: your pick C, three text versions</h1><p>Your touched-up shoulder press photo with the new words. My recommendation is C2: the answer is the biggest thing on the screen, so it reads first on a phone and promises the payoff. Pick one, or two for a test.</p><div class="g">']
for x, k, t in ITEMS:
    h.append(f'<section id="{x}"><h2>{x}</h2><p>{t}</p><a href="{x}.jpg"><img src="{x}.jpg" alt="{x}"></a></section>')
h.append('</div><h2 style="margin-top:28px">Phone size</h2><div class="s">')
for x, k, t in ITEMS:
    h.append(f'<figure><img src="{x}-phone.jpg" alt="{x} at phone size"><figcaption>{x}</figcaption></figure>')
h.append('</div></main></body></html>')
(R/'index.html').write_text(''.join(h)); print('ok')
