#!/usr/bin/env python3
"""Neutral review page for the four Shorts: eight covers each, X labels only, re-encoded copies, no source named."""
from pathlib import Path
import json, re, html
from PIL import Image
from build import OUT as R, BUILT, SHORTS
P = R/'blind-review'; P.mkdir(exist_ok=True)
TEXT = {
 's1': dict(A='Wincing after a sip at a poolside bar, yellow headline', B='Black tank top at a home bar, disgusted look at the glass, white and cyan headline', C='Studio photo in front of a vodka soda, navy headline', D='Pushing away a pink margarita, holding soda water, large bottom title', E='Eating a margarita with a spoon like a sundae, white and gold headline', F='Biting a lime at a beach bar, sour face, yellow headline', G='Six empty margarita glasses, sheepish grin, white and cyan headline', H='Pouring soda into vodka, skeptical look, large bottom title'),
 's2': dict(A='Fourteen glasses of wine on the table, shocked, yellow headline', B='On the couch at night, caught with a glass, white and cyan headline', C='Studio photo in front of a wine bottle, navy headline', D='Pouring a glass down the sink, thumbs up, large bottom title', E='Same man twice: ripped with water, heavier with wine, white and gold headline', F='Pouring a glass until it overflows, shocked, yellow headline', G='Wine cellar, worried look at the glass, white and gold headline', H='Wagging a finger at a glass of wine, white and cyan headline'),
 's3': dict(A='Wide awake and wrecked at 3 AM by the bed, yellow headline', B='Covering his glass and tapping his watch, white and cyan headline', C='Studio photo in a dark bedroom with a clock and whiskey, navy headline', D='Shocked at his ring on the edge of the bed, large bottom title', E='Last toast with a big clock under his arm, white and gold headline', F='Lying in bed staring up, wide awake, white and cyan headline', G='Pointing at the bedside clock with a glass of water, yellow headline', H='Huge yawn with a coffee in the morning, white and gold headline'),
 's4': dict(A='Pool party, palm up to a beer, sparkling water in hand, yellow headline', B='Bar stool, bored shrug by a full beer, white and cyan headline', C='Studio photo in front of beers and shots, navy headline', D='Holding up an injector pen, sliding the beer away, large bottom title', E='Fresh and sipping water the morning after the party, white and gold headline', F='Bored chin-on-hand look at a full beer, yellow headline', G='Cookout toast with a can of sparkling water, white and cyan headline', H='Pool party, empty hands, calm shrug, white and gold headline'),
}
REC = dict(s1='A', s2='A', s3='A', s4='A')
PLAN = dict(s2='Thu Dec 24, 9 AM', s1='Thu Dec 24, 6 PM', s4='Fri Dec 25, 9 AM', s3='Fri Dec 25, 6 PM')
ORDER = ['s2', 's1', 's4', 's3']
css = '''*{box-sizing:border-box}:root{--bg:#101823;--card:#182230;--ink:#f1f5f9;--dim:#cbd5e1;--line:#344156}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1200px;margin:0 auto;padding:28px 16px}h1{font-size:32px;margin:0 0 8px}h2{font-size:27px;margin:44px 0 4px}h3{margin:0 0 4px;font-size:20px}p{color:var(--dim);max-width:820px}nav{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}nav a{color:#64e4f3;padding:6px 14px;background:#233147;border-radius:8px;text-decoration:none}section{margin:20px 0;padding:18px;background:var(--card);border:1px solid var(--line);border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr .75fr;gap:16px;margin-top:12px;align-items:start}img{width:100%;height:auto;border-radius:6px;display:block}figure{margin:0;min-width:0}html,body{overflow-x:hidden}figcaption{font-size:14px;color:var(--dim);margin-bottom:6px}@media(max-width:700px){.pair{grid-template-columns:1fr 1fr}.g{grid-column:1/3;max-width:220px}section{padding:14px}}'''
h = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Alcohol Shorts Covers</title><style>{css}</style></head><body><main><h1>Can You Drink Alcohol And Still Have Abs? Shorts covers</h1><p>Eight cover choices for each of the four Shorts. Each choice shows the Instagram layout, the YouTube Shorts layout and the Instagram profile crop. Pick one label per Short in chat, for example "Wine X3, Taste Bad X5, Urge X1, 3 Hours X8". My recommendation is marked on each Short.</p><p>Your approved films are untouched. Nothing has been uploaded or scheduled. All four Shorts follow the full video, which goes out Sun Dec 20.</p><nav>']
pages = []
for s in ORDER:
    spec = SHORTS[s]; key = json.loads((R/s/'.blind-key.json').read_text())['labels']; (P/s).mkdir(exist_ok=True)
    items = []
    for x in sorted(key, key=lambda k: int(k[1:])):
        k = re.search(r'letter (\w)', key[x]['note']).group(1)
        for pf in ['instagram', 'youtube']:
            im = Image.open(BUILT/s/k/f'{pf}.png').convert('RGB'); im.save(P/s/f'{x}-{pf}.jpg', quality=93)
            if pf == 'instagram': im.crop((0, 240, 1080, 1680)).resize((270, 360), Image.Resampling.LANCZOS).save(P/s/f'{x}-grid.jpg', quality=93)
        items.append((x, TEXT[s][k], k))
    rec = next(x for x, _, k in items if k == REC[s])
    h.append(f'<a href="#{s}">{html.escape(spec["title"])}</a>')
    b = [f'<h2 id="{s}">{html.escape(spec["title"])}</h2><p>Goes out {PLAN[s]} Central. Recommended: <strong>{rec}</strong>.</p>']
    for x, t, k in items:
        b.append(f'<section id="{s}-{x}"><h3>{x}</h3><p>{html.escape(t)}</p><div class="pair"><figure><figcaption>Instagram</figcaption><a href="{s}/{x}-instagram.jpg"><img loading="lazy" src="{s}/{x}-instagram.jpg" alt="{x} Instagram"></a></figure><figure><figcaption>YouTube Shorts</figcaption><a href="{s}/{x}-youtube.jpg"><img loading="lazy" src="{s}/{x}-youtube.jpg" alt="{x} YouTube"></a></figure><figure class="g"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="{s}/{x}-grid.jpg" alt="{x} profile crop"></figure></div></section>')
    pages.append(''.join(b)); print(spec['title'], 'recommended', rec)
h.append('</nav>'); h += pages; h.append('</main></body></html>'); (P/'index.html').write_text(''.join(h))
