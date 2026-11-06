#!/usr/bin/env python3
"""Round 2 review page (Dan, 2026-11-06): four new couple + jealous fat-Dan images, each its own design,
under the Short 1 and Short 2 titles. Served at /round2/ beside round 1. Labels N1-N4 = the same picture in both Shorts."""
from pathlib import Path
import json, shutil, html
from PIL import Image
from build import OUT, ROOT, SHORTS

REV = OUT / 'review' / 'round2'
shutil.rmtree(REV, ignore_errors=True); REV.mkdir(parents=True)
LABEL = {'A': 'N1', 'B': 'N2', 'C': 'N3', 'D': 'N4'}
sections = []
for n, key in ((1, 's1r2'), (2, 's2r2')):
    spec = SHORTS[key]
    m = json.loads((OUT / key / 'manifest.json').read_text())
    rows = {(r['letter'], r['platform']): r for r in m['outputs']}
    d = REV / key; d.mkdir()
    cards = []
    for l in 'ABCD':
        if (l, 'instagram') not in rows:
            continue
        lab = LABEL[l]
        for plat in ('instagram', 'youtube'):
            Image.open(ROOT / rows[(l, plat)]['path']).convert('RGB').save(d / f'{lab}-{plat}.jpg', quality=90)
        Image.open(ROOT / rows[(l, 'instagram')]['path']).convert('RGB').crop((0, 240, 1080, 1680)).resize((540, 720)).save(d / f'{lab}-grid.jpg', quality=90)
        cards.append(f'''<article class="card"><h3>{lab}</h3>
<div class="pair"><figure><img src="{key}/{lab}-instagram.jpg" alt="{lab} Instagram"><figcaption>Instagram</figcaption></figure>
<figure><img src="{key}/{lab}-youtube.jpg" alt="{lab} YouTube"><figcaption>YouTube</figcaption></figure></div>
<figure class="grid"><img src="{key}/{lab}-grid.jpg" alt="{lab} profile tile"><figcaption>Instagram profile tile</figcaption></figure></article>''')
    sections.append(f'<section><h2>Short {n}: {html.escape(spec["title"])}</h2><p class="n">{len(cards)} new choices</p>{"".join(cards)}</section>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Invest Covers Round 2</title><style>
:root{{--bg:#0f141c;--fg:#f3f5f8;--mut:#9aa6b6;--card:#18202b}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.4 -apple-system,system-ui,sans-serif}}
main{{max-width:1500px;margin:auto;padding:16px}} a{{color:#7fd3ff}}
h1{{font-size:22px;margin:4px 0 6px}} h2{{font-size:20px;margin:28px 0 2px}} .n,.lead{{color:var(--mut);margin:0 0 12px}}
section{{display:grid;grid-template-columns:1fr;gap:14px}} section h2,section .n{{grid-column:1/-1}}
.card{{background:var(--card);border-radius:12px;padding:12px}} .card h3{{margin:0 0 8px;font-size:22px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}} figure{{margin:0}} img{{width:100%;display:block;border-radius:6px}}
figcaption{{color:var(--mut);font-size:13px;margin-top:4px}} .grid{{width:50%;margin-top:8px}}
@media(min-width:900px){{section{{grid-template-columns:repeat(4,1fr)}}}}
</style></head><body><main><h1>Invest In Your Health covers: round 2</h1>
<p class="lead">Four new pictures, each its own design: ripped you holding hands with her, fat you watching, jealous. N1 to N4 are the same pictures under each Short's title. Pick one per Short (for example "Short 1 N2"). <a href="../">Round 1 choices</a></p>
{"".join(sections)}</main></body></html>'''
(REV / 'index.html').write_text(page)
print('round 2 page', REV / 'index.html')
