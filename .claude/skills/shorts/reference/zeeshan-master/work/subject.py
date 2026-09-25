#!/usr/bin/env python3
"""Per-shot subject geometry from Vision masks (960x540 frames at 4 fps), in SOURCE pixels
(x2): hair top (densely, every 0.25 s), silhouette union, head centre, torso centre."""
import json, glob, os, numpy as np
from PIL import Image
from scipy import ndimage
man = json.load(open('shots/manifest.json'))
res = {}
for m in man:
    fs = sorted(glob.glob(f"masks/out/{m['name']}_*.mask.png"))
    tops, x0s, x1s, bots, heads, torsos = [], [], [], [], [], []
    for f in fs:
        a = np.array(Image.open(f)) > 127
        lab, n = ndimage.label(a)
        if n == 0: continue
        sizes = ndimage.sum(a, lab, range(1, n + 1))
        k = int(np.argmax(sizes)) + 1
        b = lab == k
        rows = np.where(b.sum(1) >= 6)[0]
        cols = np.where(b.any(0))[0]
        if not len(rows): continue
        top = rows[0]; bot = rows[-1]
        tops.append(top); bots.append(bot); x0s.append(cols[0]); x1s.append(cols[-1])
        hh = b[top:top + max(8, (bot - top) // 9)]
        hc = np.where(hh.any(0))[0]; heads.append((hc[0] + hc[-1]) / 2)
        colfill = b.sum(0); full = colfill >= 0.6 * colfill.max()
        tc = np.where(full)[0]; torsos.append((tc[0] + tc[-1]) / 2)
    S = 2.0
    res[m['name']] = {
        'n': len(tops), 'hairTop': float(min(tops) * S), 'hairTopMedian': float(np.median(tops) * S),
        'x0': float(min(x0s) * S), 'x1': float(max(x1s) * S), 'x0p5': float(np.percentile(x0s, 5) * S),
        'x1p95': float(np.percentile(x1s, 95) * S), 'bottom': float(max(bots) * S),
        'headX': float(np.median(heads) * S), 'torsoX': float(np.median(torsos) * S),
        'headXrange': [float(min(heads) * S), float(max(heads) * S)],
    }
    r = res[m['name']]
    print(f"{m['name']} n={r['n']:3d} hair {r['hairTop']:5.0f} (med {r['hairTopMedian']:5.0f})  x {r['x0']:5.0f}-{r['x1']:5.0f} (p {r['x0p5']:5.0f}-{r['x1p95']:5.0f})  bottom {r['bottom']:5.0f}  headX {r['headX']:5.0f} {r['headXrange']}  torsoX {r['torsoX']:5.0f}")
json.dump(res, open('work/subject.json', 'w'), indent=1)
