#!/usr/bin/env python3
"""Round 2 page: Dan's revised covers, every layout, for approval before anything is installed."""
from PIL import Image
from build import OUT as R, BUILT
P = R/'round2-review'; P.mkdir(exist_ok=True)
SETS = [('Stop Drinking 3 Hours Before Bed', 'Fri Dec 25, 6 PM', 's3', [('T1', 'I', 'Living room, wall clock on the right'), ('T2', 'J', 'Home bar, the clock is bigger and your arm is closest to it'), ('T3', 'K', 'Backyard patio at dusk, clock on a brick wall, the man is heavier'), ('T4', 'L', 'Pub at night, the man is heavier')], 'T3'),
        ('What Killed My Urge To Drink', 'Fri Dec 25, 9 AM', 's4', [('U1', 'P', 'Exactly what you asked: X6 with the pen in that hand, in the same spot as the water'), ('U2', 'Q', 'Same picture with that hand raised to your shoulder, so the pen shows at phone size')], 'U2')]
css = '''*{box-sizing:border-box}:root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1;--line:#344156}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1200px;margin:0 auto;padding:28px 16px}h1{font-size:32px;margin:0 0 8px}h2{font-size:27px;margin:40px 0 4px}h3{margin:0 0 4px;font-size:20px}p{color:var(--dim);max-width:820px}section{margin:20px 0;padding:18px;background:var(--card);border:1px solid var(--line);border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr .75fr;gap:16px;margin-top:12px;align-items:start}img{width:100%;height:auto;border-radius:6px;display:block}figure{margin:0;min-width:0}html,body{overflow-x:hidden}figcaption{font-size:14px;color:var(--dim);margin-bottom:6px}@media(max-width:700px){.pair{grid-template-columns:1fr 1fr}.g{grid-column:1/3;max-width:220px}section{padding:14px}}'''
h = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Alcohol Covers Round 2</title><style>{css}</style></head><body><main><h1>Can You Drink Alcohol And Still Have Abs? Shorts covers, round 2</h1><p>Your two revised Shorts. Each choice shows the Instagram layout, the YouTube Shorts layout and the Instagram profile crop. Pick one of each in chat. Nothing with these covers is installed until you approve the exact file.</p>']
for title, when, s, items, rec in SETS:
    h.append(f'<h2>{title}</h2><p>Goes out {when} Central. Recommended: <strong>{rec}</strong>.</p>')
    for x, k, t in items:
        for pf in ['instagram', 'youtube']:
            im = Image.open(BUILT/s/k/f'{pf}.png').convert('RGB'); im.save(P/f'{x}-{pf}.jpg', quality=93)
            if pf == 'instagram': im.crop((0, 240, 1080, 1680)).resize((270, 360), Image.Resampling.LANCZOS).save(P/f'{x}-grid.jpg', quality=93)
        h.append(f'<section><h3>{x}</h3><p>{t}</p><div class="pair"><figure><figcaption>Instagram</figcaption><a href="{x}-instagram.jpg"><img src="{x}-instagram.jpg" alt="{x} Instagram"></a></figure><figure><figcaption>YouTube Shorts</figcaption><a href="{x}-youtube.jpg"><img src="{x}-youtube.jpg" alt="{x} YouTube"></a></figure><figure class="g"><figcaption>Instagram profile crop</figcaption><img src="{x}-grid.jpg" alt="{x} profile crop"></figure></div></section>')
h.append('</main></body></html>'); (P/'index.html').write_text(''.join(h))
