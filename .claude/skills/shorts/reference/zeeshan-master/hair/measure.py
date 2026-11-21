#!/usr/bin/env python3
"""Hair-top per 0.25 s across source ranges (Vision person mask, 960x540 BT.709 decode, x2 -> source px).
usage: measure.py NAME START END [NAME START END ...]  -> hair/<NAME>.json"""
import json, os, subprocess, sys, glob, numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
SRC = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('../config.js').SRC))"], cwd=HERE).decode())
PM = os.path.join(HERE, '..', 'recentre', 'personmask')
a = sys.argv[1:]
for i in range(0, len(a), 3):
    name, t0, t1 = a[i], float(a[i+1]), float(a[i+2])
    d = os.path.join(HERE, 'fr', name); os.makedirs(d, exist_ok=True)
    for f in glob.glob(d + '/*'): os.remove(f)
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-i', SRC, '-t', f'{t1-t0:.3f}',
                    '-vf', 'fps=4,scale=960:540:in_color_matrix=bt709:in_range=tv', f'{d}/f_%04d.png'], check=True)
    fs = sorted(glob.glob(d + '/f_*.png'))
    subprocess.run([PM, d + '/m'] + fs, check=True, capture_output=True)
    rows = []
    for k, f in enumerate(fs):
        m = np.array(Image.open(f"{d}/m/{os.path.basename(f)[:-4]}.mask.png")) > 127
        lab, n = ndimage.label(m)
        if n == 0: rows.append(None); continue
        sizes = ndimage.sum(m, lab, range(1, n + 1)); b = lab == (int(np.argmax(sizes)) + 1)
        r = np.where(b.sum(1) >= 3)[0]
        c = np.where(b.any(0))[0]
        rows.append({'t': round(t0 + k * 0.25, 3), 'top': int(r[0]) * 2, 'x0': int(c[0]) * 2, 'x1': int(c[-1]) * 2})
    json.dump(rows, open(os.path.join(HERE, name + '.json'), 'w'))
    tops = [r['top'] for r in rows if r]
    print(f"{name} {t0:.2f}-{t1:.2f} n={len(tops)} min={min(tops)} p10={np.percentile(tops,10):.0f} med={np.median(tops):.0f} "
          f"n<=12:{sum(t<=12 for t in tops)}  first<=12: {[r['t'] for r in rows if r and r['top']<=12][:6]}")
