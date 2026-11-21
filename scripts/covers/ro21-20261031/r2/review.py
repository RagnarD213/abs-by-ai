#!/usr/bin/env python3
"""Neutral round 2 page: X labels only, re-encoded copies, no source named."""
from pathlib import Path
import json, re
from PIL import Image
R = Path(__file__).resolve().parents[4]/'social media graphics/youtube/thumbnails/What Every Body Fat Percentage Looks Like/_blind-set/r2'
P = R/'blind-review'; P.mkdir(exist_ok=True)
key = json.loads((R/'.blind-key.json').read_text())['labels']
TEXT = {'R1': 'Plain grey backdrop, yellow band: your pick with the new title and four figures',
        'R2': 'Dark navy studio like the film, black band with white and yellow type',
        'R3': 'Bright gym, red band',
        'R4': 'Sunny pool deck, white band with black and red type',
        'R5': 'Beach at sunset, no band, outlined type on the sky',
        'R6': 'Dark gym with blue neon, no band, white and blue type'}
items = []
for x in sorted(key, key=lambda k: int(k[1:])):
    k = re.search(r'design (\w+)', key[x]['note']).group(1)
    im = Image.open(R/'blind'/f'{x}.jpg').convert('RGB').resize((1280, 720), Image.Resampling.LANCZOS)
    im.save(P/f'{x}.jpg', quality=93)
    im.resize((320, 180), Image.Resampling.LANCZOS).save(P/f'{x}-phone.jpg', quality=93)
    items.append((x, TEXT[k], k))
rec = next(x for x, _, k in items if k == 'R2')
css = ':root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1180px;margin:auto;padding:24px 16px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px}section{background:var(--card);border-radius:12px;padding:14px}img{width:100%;display:block;border-radius:6px}h2{margin:0 0 4px}p{color:var(--dim);margin:0 0 10px}.s{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}.s figure{margin:0;width:160px}.s img{width:160px}.s figcaption{font-size:14px;text-align:center}'
h = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Body Fat Thumbnails R2</title><style>{css}</style></head><body><main><h1>Body Fat Percentage thumbnails: round 2</h1><p>All six use your title and the four figures: 35%, 25%, 15% and 8%. My recommendation is {rec}: the dark set matches the film and the bodies pop most at phone size. You can also mix: name one picture with another\'s title style.</p><div class="g">']
for x, t, k in items:
    h.append(f'<section id="{x}"><h2>{x}</h2><p>{t}</p><a href="{x}.jpg"><img src="{x}.jpg" alt="{x}"></a></section>')
h.append('</div><h2 style="margin-top:28px">Phone size</h2><div class="s">')
for x, t, k in items:
    h.append(f'<figure><img src="{x}-phone.jpg" alt="{x} at phone size"><figcaption>{x}</figcaption></figure>')
h.append('</div></main></body></html>')
(P/'index.html').write_text(''.join(h)); print('recommend', rec)
