#!/usr/bin/env python3
"""Blind review page for the SL-20 covers: register each option with blind.py (Instagram layout is the logged image),
shuffle to neutral X labels, and write a phone-first page with both layouts per label. Sources never shown."""
from pathlib import Path
import json, hashlib, subprocess, shutil, html
from PIL import Image
from build import OUT, ROOT, SHORTS

BLIND = ROOT / '.claude/skills/_shared/blind-image/blind.py'
REV = OUT / 'review'
shutil.rmtree(REV, ignore_errors=True); REV.mkdir(parents=True)
sections = []
for n, key in enumerate(SHORTS, 1):
    spec = SHORTS[key]
    m = json.loads((OUT / key / 'manifest.json').read_text())
    rows = {(r['letter'], r['platform']): r for r in m['outputs']}
    setdir = OUT / key / 'blind-set'
    shutil.rmtree(setdir, ignore_errors=True)
    letters = sorted({l for l, _ in rows})
    for l in letters:
        src = 'google' if l in 'FGH' else 'codex'
        subprocess.run(['python3', str(BLIND), 'add', str(setdir), '--source', src, '--file', str(ROOT / rows[(l, 'instagram')]['path'])], check=True, capture_output=True)
    subprocess.run(['python3', str(BLIND), 'build', str(setdir), '--kind', 'cover', '--video', f"{spec['title']} (SL-20 Short {n})", '--shot', f'sl20-short{n}-cover'], check=True, capture_output=True)
    key_json = json.loads((setdir / '.blind-key.json').read_text())
    by_sha = {hashlib.sha256((ROOT / rows[(l, 'instagram')]['path']).read_bytes()).hexdigest()[:12]: l for l in letters}
    mapping = {lab: by_sha[v['sha']] for lab, v in key_json['labels'].items()}
    (setdir / '.letter-map.json').write_text(json.dumps(mapping, indent=1))   # internal: X label -> build letter
    d = REV / key; d.mkdir()
    cards = []
    for lab in sorted(mapping, key=lambda s: int(s[1:])):
        l = mapping[lab]
        for plat in ('instagram', 'youtube'):
            Image.open(ROOT / rows[(l, plat)]['path']).convert('RGB').save(d / f'{lab}-{plat}.jpg', quality=90)
        Image.open(ROOT / rows[(l, 'instagram')]['path']).convert('RGB').crop((0, 240, 1080, 1680)).resize((540, 720)).save(d / f'{lab}-grid.jpg', quality=90)
        cards.append(f'''<article class="card"><h3>{lab}</h3>
<div class="pair"><figure><img src="{key}/{lab}-instagram.jpg" alt="{lab} Instagram"><figcaption>Instagram</figcaption></figure>
<figure><img src="{key}/{lab}-youtube.jpg" alt="{lab} YouTube"><figcaption>YouTube</figcaption></figure></div>
<figure class="grid"><img src="{key}/{lab}-grid.jpg" alt="{lab} profile tile"><figcaption>Instagram profile tile</figcaption></figure></article>''')
    sections.append(f'<section><h2>Short {n}: {html.escape(spec["title"])}</h2><p class="n">{len(cards)} choices</p>{"".join(cards)}</section>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Invest In Your Health Covers</title><style>
:root{{--bg:#0f141c;--fg:#f3f5f8;--mut:#9aa6b6;--card:#18202b}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.4 -apple-system,system-ui,sans-serif}}
main{{max-width:1500px;margin:auto;padding:16px}}
h1{{font-size:22px;margin:4px 0 6px}} h2{{font-size:20px;margin:28px 0 2px}} .n,.lead{{color:var(--mut);margin:0 0 12px}}
section{{display:grid;grid-template-columns:1fr;gap:14px}} section h2,section .n{{grid-column:1/-1}}
.card{{background:var(--card);border-radius:12px;padding:12px}} .card h3{{margin:0 0 8px;font-size:22px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}} figure{{margin:0}} img{{width:100%;display:block;border-radius:6px}}
figcaption{{color:var(--mut);font-size:13px;margin-top:4px}} .grid{{width:50%;margin-top:8px}}
@media(min-width:900px){{section{{grid-template-columns:repeat(4,1fr)}}}}
</style></head><body><main><h1>Invest In Your Health Shorts: cover choices</h1>
<p class="lead"><a href="round2/" style="color:#FFD400;font-weight:700">New: round 2 covers (four new pictures) &rarr;</a></p><p class="lead">Pick one label per Short (for example "Short 1 X3"). Each choice shows the Instagram cover, the YouTube cover and how the Instagram profile tile crops it.</p>
{"".join(sections)}</main></body></html>'''
(REV / 'index.html').write_text(page)
print('review page', REV / 'index.html')
