#!/usr/bin/env python3
"""Neutral review page for the eight thumbnails: X labels only, re-encoded copies, no source named."""
from pathlib import Path
import json, re
from PIL import Image
R = Path(__file__).resolve().parents[3]/'social media graphics/youtube/thumbnails/What Every Body Fat Percentage Looks Like/_blind-set'
P = R/'blind-review'; P.mkdir(exist_ok=True)
key = json.loads((R/'.blind-key.json').read_text())['labels']
TEXT = {'A': 'Three of you side by side at 35%, 20% and 8%, yellow band',
        'B': 'Ripped you looking in the mirror at a much heavier you, stacked color blocks',
        'C': 'Your studio photo in a dark blue room with the level numbers, clean white type',
        'D': 'One body, half heavy and half ripped, white and blue type',
        'E': 'You on a body scanner machine, delighted at the result, tall dark and gold type',
        'G1': 'Three of you climbing a stairway from heavy to ripped, blue light',
        'G2': 'You in a gallery with a row of framed levels, white title bar',
        'G3': 'You holding a life-size cardboard cutout of heavier you, red title band'}
items = []
for x in sorted(key, key=lambda k: int(k[1:])):
    k = re.search(r'design (\w+)', key[x]['note']).group(1)
    im = Image.open(R/'blind'/f'{x}.jpg').convert('RGB').resize((1280, 720), Image.Resampling.LANCZOS)
    im.save(P/f'{x}.jpg', quality=93)
    im.resize((320, 180), Image.Resampling.LANCZOS).save(P/f'{x}-phone.jpg', quality=93)
    items.append((x, TEXT[k], k))
rec = next(x for x, _, k in items if k == 'A')
css = ':root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1180px;margin:auto;padding:24px 16px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px}section{background:var(--card);border-radius:12px;padding:14px}img{width:100%;display:block;border-radius:6px}h2{margin:0 0 4px}p{color:var(--dim);margin:0 0 10px}.s{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}.s figure{margin:0;width:160px}.s img{width:160px}.s figcaption{font-size:14px;text-align:center}'
h = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Body Fat Thumbnails</title><style>{css}</style></head><body><main><h1>What Every Body Fat Percentage Looks Like (On Me): eight thumbnails</h1><p>Same words on all eight. My recommendation is {rec}: three of you side by side reads instantly on a phone and repeats the same-person idea you picked for the Ozempic film. Pick one, or two for a test.</p><div class="g">']
for x, t, k in items:
    h.append(f'<section id="{x}"><h2>{x}</h2><p>{t}</p><a href="{x}.jpg"><img src="{x}.jpg" alt="{x}"></a></section>')
h.append('</div><h2 style="margin-top:28px">Phone size</h2><div class="s">')
for x, t, k in items:
    h.append(f'<figure><img src="{x}-phone.jpg" alt="{x} at phone size"><figcaption>{x}</figcaption></figure>')
h.append('</div></main></body></html>')
(P/'index.html').write_text(''.join(h)); print('recommend', rec)
