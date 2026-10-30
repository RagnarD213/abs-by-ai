#!/usr/bin/env python3
"""Neutral review page for the eight covers: X labels only, re-encoded copies, no source named."""
from pathlib import Path
import json, re
from PIL import Image
R = Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/ds43-terry-crews-20261030'
P = R/'blind-review'; P.mkdir(exist_ok=True)
key = json.loads((R/'.blind-key.json').read_text())['labels']
TEXT = {'A': 'Sitting at a pancake breakfast, looking up at a clock on almost 2, yellow headline',
        'B': 'Dark gym, flexing and holding out an empty plate, clock on 12, white and cyan headline',
        'C': 'Studio photo in front of a steak dinner and a clock on 2, navy headline',
        'D': 'Terry at the stock exchange on top, you shocked at your laptop below, yellow band',
        'E': 'Same man twice: empty plate at 9, steak at 2, large bottom title',
        'F': 'Diner booth, pancakes pushed aside, checking your watch, red headline',
        'G': 'Kitchen at 8 AM, black coffee and an empty plate, white outlined headline',
        'H': 'Restaurant, huge steak at 2 PM, big grin, cream headline'}
items = []
for x in sorted(key, key=lambda k: int(k[1:])):
    k = re.search(r'letter (\w)', key[x]['note']).group(1)
    for pf in ['instagram', 'youtube']:
        im = Image.open(R/f'built/{k}/{pf}/ds-43_terry-crews_cover-{k}.png').convert('RGB')
        im.save(P/f'{x}-{pf}.jpg', quality=93)
        if pf == 'instagram': im.crop((0, 240, 1080, 1680)).resize((270, 360), Image.Resampling.LANCZOS).save(P/f'{x}-grid.jpg', quality=93)
    items.append((x, TEXT[k], k))
rec = next(x for x, _, k in items if k == 'A')
css = '''*{box-sizing:border-box}:root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1;--line:#344156}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1200px;margin:0 auto;padding:28px 16px}h1{font-size:32px;margin:0 0 8px}p{color:var(--dim);max-width:820px}section{margin:24px 0;padding:20px;background:var(--card);border:1px solid var(--line);border-radius:14px}h2{margin:0 0 4px;font-size:22px}.pair{display:grid;grid-template-columns:1fr 1fr .75fr;gap:18px;margin-top:14px;align-items:start}img{width:100%;height:auto;border-radius:6px;display:block}figure{margin:0;min-width:0}html,body{overflow-x:hidden}figcaption{font-size:14px;color:var(--dim);margin-bottom:6px}@media(max-width:700px){.pair{grid-template-columns:1fr 1fr}.g{grid-column:1/3;max-width:220px}section{padding:14px}}'''
h = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Terry Crews Covers</title><style>{css}</style></head><body><main><h1>Terry Crews Doesn\'t Eat Until 2 PM</h1><p>Eight cover choices. Each shows the Instagram layout, the YouTube Shorts layout and the Instagram profile crop. Pick a label in chat. My recommendation is {rec}: it acts the title out at a glance, in the yellow headline you pick most.</p><p>Your approved film is untouched. Nothing has been uploaded or scheduled. After your pick it goes on Tue Dec 22 at 6 PM Central.</p>']
for x, t, k in items:
    h.append(f'<section id="{x}"><h2>{x}</h2><p>{t}</p><div class="pair"><figure><figcaption>Instagram</figcaption><a href="{x}-instagram.jpg"><img loading="lazy" src="{x}-instagram.jpg" alt="{x} Instagram"></a></figure><figure><figcaption>YouTube Shorts</figcaption><a href="{x}-youtube.jpg"><img loading="lazy" src="{x}-youtube.jpg" alt="{x} YouTube"></a></figure><figure class="g"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="{x}-grid.jpg" alt="{x} profile crop"></figure></div></section>')
h.append('</main></body></html>'); (P/'index.html').write_text(''.join(h)); print(rec)
