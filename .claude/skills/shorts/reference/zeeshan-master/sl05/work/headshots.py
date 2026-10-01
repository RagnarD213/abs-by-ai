#!/usr/bin/env python3
"""SL-05 round 2: head centre + body extent per talking shot (Vision mask every 0.5 s, 960x540 BT.709, x2 -> source px).
Head = largest mask component, rows top..top+260 source px, columns with >=20 px (source) of mask.
usage: headshots.py S T0 T1 [S T0 T1 ...] -> prints per-shot stats, writes work/hs/<T0>.json"""
import json, os, subprocess, sys, glob, numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(HERE)
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').SRC))"], cwd=B).decode())
PM = os.path.join(B, 'recentre', 'personmask')
a = sys.argv[1:]
for i in range(0, len(a), 3):
    name, t0, t1 = a[i], float(a[i+1]), float(a[i+2])
    d = os.path.join(HERE, 'hs', f'{t0:.3f}'); os.makedirs(d, exist_ok=True)
    for f in glob.glob(d + '/*.png'): os.remove(f)
    dur = t1 - t0 - 0.05
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t0+0.03:.3f}', '-i', SRC, '-t', f'{dur:.3f}',
                    '-vf', 'fps=2,scale=960:540:in_color_matrix=bt709:in_range=tv', f'{d}/f_%04d.png'], check=True)
    fs = sorted(glob.glob(d + '/f_*.png'))
    if not fs: print(name, t0, t1, 'no frames'); continue
    subprocess.run([PM, d + '/m'] + fs, check=True, capture_output=True)
    rows = []
    for k, f in enumerate(fs):
        m = np.array(Image.open(f"{d}/m/{os.path.basename(f)[:-4]}.mask.png").convert('L')) > 127
        lab, n = ndimage.label(m)
        if n == 0: continue
        sizes = ndimage.sum(m, lab, range(1, n + 1)); b = lab == (int(np.argmax(sizes)) + 1)
        r = np.where(b.sum(1) >= 3)[0]; top = r[0]
        band = b[top:top + 130]; c = np.where(band.sum(0) >= 10)[0]
        cb = np.where(b.any(0))[0]
        rows.append({'t': round(t0 + 0.03 + k * 0.5, 2), 'top': int(top) * 2, 'hx0': int(c[0]) * 2, 'hx1': int(c[-1]) * 2,
                     'hc': int(c[0] + c[-1]), 'bx0': int(cb[0]) * 2, 'bx1': int(cb[-1]) * 2})
    json.dump(rows, open(os.path.join(HERE, 'hs', f'{name}_{t0:.3f}.json'), 'w'))
    hc = np.array([r['hc'] for r in rows])
    print(f"{name} {t0:8.3f}-{t1:8.3f} n={len(rows):3d} head c med {np.median(hc):5.0f} min {hc.min():5.0f} max {hc.max():5.0f} "
          f"| head x {min(r['hx0'] for r in rows)}-{max(r['hx1'] for r in rows)} | body {min(r['bx0'] for r in rows)}-{max(r['bx1'] for r in rows)} "
          f"| top min {min(r['top'] for r in rows)} max {max(r['top'] for r in rows)}")
