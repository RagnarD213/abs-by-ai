#!/usr/bin/env python3
"""SL-03: per 0.25 s on a RAW roll: person-mask top row + silhouette x-extent, and the face box (Vision). 960x540 decode, x2.
usage: measure.py NAME ROLL START END ...  -> hair/<NAME>.json"""
import json, os, subprocess, sys, glob, numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
RAWD = '/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera'
PM = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask'
FB = os.path.expanduser('~/.cache/absbyai/facebox')
a = sys.argv[1:]
for i in range(0, len(a), 4):
    name, roll, t0, t1 = a[i], a[i+1], float(a[i+2]), float(a[i+3])
    d = os.path.join(HERE, 'fr', name); os.makedirs(d, exist_ok=True)
    for f in glob.glob(d + '/*.png'): os.remove(f)
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-i', f'{RAWD}/{roll}.MP4', '-t', f'{t1-t0:.3f}',
                    '-vf', 'fps=4,scale=960:540:in_color_matrix=bt709:in_range=tv', f'{d}/f_%04d.png'], check=True)
    fs = sorted(glob.glob(d + '/f_*.png'))
    subprocess.run([PM, d + '/m'] + fs, check=True, capture_output=True)
    fb = dict(l.split('\t') for l in subprocess.run([FB] + fs, capture_output=True, text=True).stdout.strip().split('\n'))
    rows = []
    for k, f in enumerate(fs):
        m = np.array(Image.open(f"{d}/m/{os.path.basename(f)[:-4]}.mask.png")) > 127
        lab, n = ndimage.label(m); r = {'t': round(t0 + k * 0.25, 3)}
        if n:
            sizes = ndimage.sum(m, lab, range(1, n + 1)); b = lab == (int(np.argmax(sizes)) + 1)
            rr = np.where(b.sum(1) >= 20)[0]; c = np.where(b.any(0))[0]
            r.update(top=int(rr[0]) * 2, x0=int(c[0]) * 2, x1=int(c[-1]) * 2)
        v = fb.get(f, 'none')
        if v not in ('none', 'error'):
            x0, y0, x1, y1 = [int(q) * 2 for q in v.split()]; r.update(fx=(x0 + x1) // 2, fy0=y0, fy1=y1, fw=x1 - x0)
        rows.append(r)
    json.dump(rows, open(os.path.join(HERE, name + '.json'), 'w'))
    tops = [r['top'] for r in rows if 'top' in r]; fx = [r['fx'] for r in rows if 'fx' in r]; fy = [r['fy0'] for r in rows if 'fx' in r]
    print(f"{name} {roll} {t0:.2f}-{t1:.2f} n={len(rows)} masktop min={min(tops)} med={np.median(tops):.0f} n<=12:{sum(t<=12 for t in tops)} | "
          f"face n={len(fx)} cx min={min(fx)} med={np.median(fx):.0f} max={max(fx)} | face top min={min(fy)} med={np.median(fy):.0f} | facew med={np.median([r['fw'] for r in rows if 'fw' in r]):.0f}")
