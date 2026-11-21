#!/usr/bin/env python3
"""When and where Zeeshan's burned graphics are on screen inside each shot.
Lower thirds: rows 804-907 (measured on 5 frames), olive fill ~(76,87,48) plus a darker
number box ~(23,34,24). Top-left chips: rows 100-560, x < 800, same olive.
10 fps, BT.709 decode. Output work/gfx.json: per shot, list of [t, lt_x0, lt_x1, chip_x1]."""
import json, subprocess, numpy as np
cfg = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js')))"]))
man = json.load(open('shots/manifest.json'))
W, H = 1920, 1080
def olive(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    m1 = (abs(r - 76) < 16) & (abs(g - 87) < 16) & (abs(b - 48) < 16)
    m2 = (abs(r - 23) < 10) & (abs(g - 34) < 10) & (abs(b - 24) < 10)
    return m1 | m2
out = {}
for m in man:
    raw = subprocess.run([cfg['FF'], '-v', 'error', '-ss', str(m['absStart']), '-i', cfg['SRC'], '-t', str(m['dur']),
                          '-vf', 'fps=10,scale=in_color_matrix=bt709:in_range=tv,format=rgb24', '-f', 'rawvideo', '-'],
                         capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    rows = []
    for i, f in enumerate(fr):
        band = olive(f[820:890])
        cols = np.where(band.sum(0) >= 25)[0]
        lt = (int(cols.min()), int(cols.max())) if len(cols) > 150 else None
        cb = olive(f[100:560, :800])
        ccols = np.where(cb.sum(0) >= 12)[0]
        chip = int(ccols.max()) if len(ccols) > 80 else None
        rows.append([round(m['absStart'] + i / 10, 2), lt, chip])
    out[m['name']] = rows
    on = [r for r in rows if r[1]]; ch = [r for r in rows if r[2]]
    print(m['name'], 'LT', (on[0][0], on[-1][0], min(r[1][0] for r in on), max(r[1][1] for r in on)) if on else '-',
          ' CHIP', (ch[0][0], ch[-1][0], max(r[2] for r in ch)) if ch else '-')
json.dump(out, open('work/gfx.json', 'w'))
