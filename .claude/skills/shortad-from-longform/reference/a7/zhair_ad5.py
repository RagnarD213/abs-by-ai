#!/usr/bin/env python3
"""Hair top, refined RELATIVE to what is above the head. The head band's per-row 30th-percentile luma is bright wall
/ fridge above the hair and near-black in it; the hair top is where that profile first drops below the midpoint of the
two levels, walking down from the top of the frame to the Vision mask's top (+30). Fixed 70-level threshold failed:
the dim wall above his head reads < 70 in places and the walk climbed to y=0 (2026-09-10)."""
import json, glob, os, numpy as np
from PIL import Image
R = json.load(open('measure.json'))
fs = sorted(glob.glob('rc/fr/?????.png'))
out = []
for r, f in zip(R, fs):
    if not r.get('ok') or r.get('hair_mask') is None: out.append(r); continue
    im = np.asarray(Image.open(f).convert('RGB'), dtype=np.float32)
    Y = 0.299*im[..., 0] + 0.587*im[..., 1] + 0.114*im[..., 2]
    c0, c1 = int(r['head'] - 60), int(r['head'] + 60)
    prof = np.percentile(Y[:, max(0, c0):c1], 30, axis=1)
    ym = r['hair_mask']
    hair_lvl = float(np.median(prof[ym+6:ym+26])) if ym + 26 < 1080 else float(prof[ym])
    above = prof[:max(1, ym-8)]
    wall_lvl = float(np.percentile(above, 70)) if len(above) >= 4 else None
    # walk UP from inside the hair while the rows stay hair-dark (hair level + 14). The earlier top-down midpoint
    # search read y = 0 wherever a dim wall sat above the bright fridge above his head (frame 1373, 2026-09-10).
    thr = hair_lvl + 14; y = min(ym + 12, 1079)
    while y > 0 and y > ym - 80 and prof[y-1] < thr: y -= 1
    r['hair'] = int(y); r['hair_src'] = 'luma'; r['wall'] = None if wall_lvl is None else round(wall_lvl); r['hlvl'] = round(hair_lvl)
    out.append(r)
json.dump(out, open('measure.json', 'w'))
ok = [r for r in out if r.get('ok') and r.get('hair') is not None]
h = np.array([r['hair'] for r in ok]); d = np.array([r['hair'] - r['hair_mask'] for r in ok])
print(f"hair top (1080 px): min {h.min()} p5 {np.percentile(h,5):.0f} median {np.median(h):.0f} max {h.max()}   "
      f"vs mask: median {np.median(d):+.0f} p5 {np.percentile(d,5):+.0f} p95 {np.percentile(d,95):+.0f}   "
      f"sources {dict(zip(*np.unique([r['hair_src'] for r in ok], return_counts=True)))}")
# proof sheet: the 10 tallest instants at native scale, line at the detected hair top and at the mask top
tall = sorted(ok, key=lambda r: r['hair'])[:10]
sheet = Image.new('RGB', (10*260, 300), (0, 0, 0))
from PIL import ImageDraw
for i, r in enumerate(tall):
    f = fs[[q['n'] for q in R].index(r['n'])]
    im = Image.open(f).convert('RGB'); x0 = int(r['head']) - 130
    c = im.crop((x0, 0, x0 + 260, 300)); d = ImageDraw.Draw(c)
    d.line([(0, r['hair']), (259, r['hair'])], fill=(255, 0, 0), width=1)
    d.line([(0, r['hair_mask']), (40, r['hair_mask'])], fill=(0, 255, 255), width=1)
    d.text((4, 280), f"n{r['n']} y{r['hair']}", fill=(255, 255, 0))
    sheet.paste(c, (i*260, 0))
sheet.save('/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/abcaa32a-9420-4f02-8ed3-b5b041b09a14/scratchpad/hairproof.png')
