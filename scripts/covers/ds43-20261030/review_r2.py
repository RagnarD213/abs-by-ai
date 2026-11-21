#!/usr/bin/env python3
"""Neutral page for cover round 2: X labels only, re-encoded copies, no source named."""
from pathlib import Path
import json, re
from PIL import Image
R = Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/ds43-terry-crews-20261030/r2'
P = R/'blind-review'; P.mkdir(exist_ok=True)
key = json.loads((R/'.blind-key.json').read_text())['labels']
TEXT = {'a': 'Terry by the heavy bag, you jaw-dropped on the left, yellow headline', 'b': 'Terry in side profile, you stunned on the right, black and yellow headline',
        'c': 'Terry front on, you grinning and pointing at the screen, red headline', 'd': 'Terry flexing in the boxing ring, you smiling and pointing, white headline',
        'e': 'Terry in the warehouse gym, you with a hand on your chin, navy headline', 'f': 'Terry pointing at the camera, you with a hand on your chin, cream headline'}
items = []
for x in sorted(key, key=lambda k: int(k[1:])):
    k = re.search(r'design (\w)', key[x]['note']).group(1)
    for pf in ['instagram', 'youtube']:
        im = Image.open(R/f'built/{k}/{pf}.png').convert('RGB'); im.save(P/f'{x}-{pf}.jpg', quality=93)
        if pf == 'instagram': im.crop((0, 240, 1080, 1680)).resize((270, 360), Image.Resampling.LANCZOS).save(P/f'{x}-grid.jpg', quality=93)
    items.append((x, TEXT[k], k))
rec = next(x for x, _, k in items if k == 'a')
css = '''*{box-sizing:border-box}:root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1;--line:#344156}html,body{overflow-x:hidden}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1200px;margin:0 auto;padding:28px 16px}h1{font-size:32px;margin:0 0 8px}p{color:var(--dim);max-width:820px}section{margin:24px 0;padding:20px;background:var(--card);border:1px solid var(--line);border-radius:14px}h2{margin:0 0 4px;font-size:22px}.pair{display:grid;grid-template-columns:1fr 1fr .75fr;gap:18px;margin-top:14px;align-items:start}img{width:100%;height:auto;border-radius:6px;display:block}figure{margin:0;min-width:0}figcaption{font-size:14px;color:var(--dim);margin-bottom:6px}@media(max-width:700px){.pair{grid-template-columns:1fr 1fr}.g{grid-column:1/3;max-width:220px}section{padding:14px}}'''
h = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Terry Crews Covers</title><style>{css}</style></head><body><main><h1>Terry Crews Doesn\'t Eat Until 2 PM: Round 2</h1><p>Six covers: real footage of Terry full screen, you cut out in the corner reacting to your laptop. Each shows the Instagram layout, the YouTube Shorts layout and the Instagram profile crop. Pick a label in chat. My recommendation is {rec}: Terry\'s abs are the clearest and your reaction reads fastest.</p><p>Nothing has been uploaded or scheduled.</p>']
for x, t, k in items:
    h.append(f'<section id="{x}"><h2>{x}</h2><p>{t}</p><div class="pair"><figure><figcaption>Instagram</figcaption><a href="{x}-instagram.jpg"><img loading="lazy" src="{x}-instagram.jpg" alt="{x} Instagram"></a></figure><figure><figcaption>YouTube Shorts</figcaption><a href="{x}-youtube.jpg"><img loading="lazy" src="{x}-youtube.jpg" alt="{x} YouTube"></a></figure><figure class="g"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="{x}-grid.jpg" alt="{x} profile crop"></figure></div></section>')
h.append('</main></body></html>'); (P/'index.html').write_text(''.join(h)); print(rec)
