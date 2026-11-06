#!/usr/bin/env python3
"""DS-77 blind cover review page: eight unlabeled choices X1..X8, Instagram + YouTube + profile crop each.
Copies are re-saved without metadata under neutral names; the source key stays in blind/.blind-key.json."""
from pathlib import Path
import json, os
from PIL import Image
ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/'Short-form video content/covers/review/ds77-t-bar-rows-20261105'
KEY = json.loads((BASE/'blind/.blind-key.json').read_text())['labels']
PAGE = BASE/'page'; (PAGE/'img').mkdir(parents=True, exist_ok=True)
labels = sorted(KEY, key=lambda x: int(x[1:]))
for x in labels:
    letter = KEY[x]['note'].split()[-1]   # internal plate letter, never shown
    ig = BASE/'ds77/instagram'/f'ds-77_t-bar-rows_cover-{letter}.png'
    yt = BASE/'ds77/youtube'/f'ds-77_t-bar-rows_cover-{letter}.png'
    Image.open(ig).convert('RGB').save(PAGE/'img'/f'{x}-instagram.jpg', quality=93)
    Image.open(yt).convert('RGB').save(PAGE/'img'/f'{x}-youtube.jpg', quality=93)
    Image.open(BASE/'ds77/grid'/f'{letter}.jpg').convert('RGB').save(PAGE/'img'/f'{x}-grid.jpg', quality=93)
cards = ''.join(f'''<section id="{x}"><h2>{x}</h2><div class="pair">
<figure><figcaption>Instagram</figcaption><a href="img/{x}-instagram.jpg"><img loading="lazy" src="img/{x}-instagram.jpg" alt="{x} Instagram"></a></figure>
<figure><figcaption>YouTube Shorts</figcaption><a href="img/{x}-youtube.jpg"><img loading="lazy" src="img/{x}-youtube.jpg" alt="{x} YouTube"></a></figure>
<figure class="grid"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="img/{x}-grid.jpg" alt="{x} profile crop"></figure></div></section>''' for x in labels)
# Round 2 (Dan, 2026-11-06): four new touched-up real frames, labelled N1..N4 (all from the same maker; not part of the blind set).
R2 = {'N1': 'I', 'N2': 'J', 'N3': 'K', 'N4': 'L'}
for n, letter in R2.items():
    Image.open(BASE/'ds77/instagram'/f'ds-77_t-bar-rows_cover-{letter}.png').convert('RGB').save(PAGE/'img'/f'{n}-instagram.jpg', quality=93)
    Image.open(BASE/'ds77/youtube'/f'ds-77_t-bar-rows_cover-{letter}.png').convert('RGB').save(PAGE/'img'/f'{n}-youtube.jpg', quality=93)
    Image.open(BASE/'ds77/grid'/f'{letter}.jpg').convert('RGB').save(PAGE/'img'/f'{n}-grid.jpg', quality=93)
def card(x):
    return f'''<section id="{x}"><h2>{x}</h2><div class="pair">
<figure><figcaption>Instagram</figcaption><a href="img/{x}-instagram.jpg"><img loading="lazy" src="img/{x}-instagram.jpg" alt="{x} Instagram"></a></figure>
<figure><figcaption>YouTube Shorts</figcaption><a href="img/{x}-youtube.jpg"><img loading="lazy" src="img/{x}-youtube.jpg" alt="{x} YouTube"></a></figure>
<figure class="grid"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="img/{x}-grid.jpg" alt="{x} profile crop"></figure></div></section>'''
r2cards = ''.join(card(n) for n in R2)
nav = ''.join(f'<a href="#{x}">{x}</a>' for x in list(R2)+labels)
html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>T-Bar Rows Covers</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#101823;color:#f1f5f9;font:16px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}}main{{max-width:1200px;margin:0 auto;padding:16px}}h1{{font-size:26px;margin:4px 0 8px}}p{{color:#cbd5e1;margin:6px 0}}
.nav{{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0;position:sticky;top:0;background:#101823;padding:8px 0;z-index:2}}.nav a{{padding:6px 14px;background:#233147;border-radius:8px;color:#64e4f3;text-decoration:none}}
section{{margin:18px 0;padding:14px;background:#182230;border:1px solid #344156;border-radius:12px}}h2{{margin:0 0 10px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.grid{{grid-column:1/3;max-width:220px}}img{{width:100%;height:auto;border-radius:6px;display:block}}figure{{margin:0}}figcaption{{font-size:14px;color:#cbd5e1;margin-bottom:6px}}
@media(min-width:900px){{main{{padding:28px}}h1{{font-size:34px}}.pair{{grid-template-columns:1fr 1fr .7fr;gap:20px}}.grid{{grid-column:auto;max-width:none}}}}
</style></head><body><main><h1>How To Do T-Bar Rows</h1><p>Eight cover choices, shown in random order. Each has its Instagram layout, its YouTube Shorts layout and how it looks on your Instagram profile grid. Tap any picture for the full-size file.</p><p><strong>New: N1 to N4.</strong> Four new touched-up screenshots from your real T-bar row footage, each a different moment and a different design. Your favorite from the first set, X4, is right below them for comparison.</p><p><strong>Reply in chat with one label</strong> (N1 to N4, or any X), or two for a YouTube A/B test.</p><p>Your finalized film is untouched and backed up. Nothing is uploaded or scheduled until you pick.</p><div class="nav">{nav}</div>{r2cards}<h2 style="margin-top:28px">Your favorite from the first set</h2>{card('X4')}<h2 style="margin-top:28px">First set: all eight</h2>{cards}</main></body></html>'''
(PAGE/'index.html').write_text(html); print(PAGE/'index.html')
