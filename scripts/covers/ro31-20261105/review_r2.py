#!/usr/bin/env python3
"""RO-31 Man Boobs: neutral review page for the round 2, four thumbnails (X labels only, no source named), phone sizes first."""
from pathlib import Path
import json, re
from PIL import Image
T = Path(__file__).resolve().parents[3]/'social media graphics/youtube/thumbnails/Man Boobs Or Chest Fat'
D = T/'_build-2026-11-05-r2/designs'
P = T/'round2-review'; P.mkdir(exist_ok=True)
ORDER = ['P1', 'P2', 'P3', 'P5']  # all four are Codex (Dan asked for exactly four); X labels map in this order
TEXT = {'P1': 'Heavier you hunched on a pool lounger, arms crossed over your chest, while fit people in bikinis and ripped guys play with a beach ball behind you. Big one-line title in the yellow band.',
        'P2': 'Heavier you at the pool edge at golden hour, clutching a towel over your chest and looking down at it, while the party cheers and cannonballs behind you. Large white and yellow title in a black bottom band.',
        'P3': 'Heavier you waist-deep in the pool, arms crossed, glancing sideways at a ripped guy laughing with two women in bikinis. White and yellow title on the water.',
        'P5': 'Heavier you on the pool steps hugging a pink flamingo float over your chest, while ripped guys and women in bikinis play chicken fights behind you. Stacked yellow, white and red boxes on the left.'}
items = []
for i, k in enumerate(ORDER):
    x = f'X{i + 1}'
    im = Image.open(D/f'RO31r2-{k}.jpg').convert('RGB').resize((1280, 720), Image.Resampling.LANCZOS)
    im.save(P/f'{x}.jpg', quality=93)
    im.resize((320, 180), Image.Resampling.LANCZOS).save(P/f'{x}-phone.jpg', quality=93)
    items.append((x, TEXT[k], k))
rec = next(x for x, _, k in items if k == 'P1')
css = ':root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1180px;margin:auto;padding:24px 16px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}section{background:var(--card);border-radius:12px;padding:14px}img{width:100%;display:block;border-radius:6px}h2{margin:0 0 4px}p{color:var(--dim);margin:0 0 10px}.s{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin:10px 0 28px}.s figure{margin:0}.s figcaption{font-size:14px;text-align:center}'
h = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Man Boobs Thumbnails</title><style>{css}</style></head><body><main><h1>How To Get Rid Of Man Boobs (RO-31): round 2, four thumbnails</h1><p>Same words on all four: "Man Boobs Or Chest Fat?" My pick is {rec}: you read as embarrassed at a glance, the fun crowd behind you tells the story, and the yellow band is your most-picked layout. Pick one, or two for a test.</p><h2>Phone size (how most people will see it)</h2><div class="s">']
for x, t, k in items:
    h.append(f'<figure><a href="#{x}"><img src="{x}-phone.jpg" alt="{x} at phone size"></a><figcaption>{x}</figcaption></figure>')
h.append('</div><div class="g">')
for x, t, k in items:
    h.append(f'<section id="{x}"><h2>{x}</h2><p>{t}</p><a href="{x}.jpg"><img src="{x}.jpg" alt="{x}"></a></section>')
h.append('</div></main></body></html>')
(P/'index.html').write_text(''.join(h))
# review sheet
sheet = Image.new('RGB', (2 * 640 + 30, 2 * 400 + 10), (16, 24, 35))
from PIL import ImageDraw, ImageFont
d = ImageDraw.Draw(sheet); f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
for i, (x, t, k) in enumerate(items):
    px, py = 10 + (i % 2) * 650, 10 + (i // 2) * 400
    sheet.paste(Image.open(P/f'{x}.jpg').resize((640, 360)), (px, py + 36)); d.text((px, py), x, font=f, fill=(255, 214, 0))
sheet.save(T/'REVIEW_CHOICES_R2.jpg', quality=88)
print('recommend', rec)
