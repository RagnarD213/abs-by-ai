#!/usr/bin/env python3
"""Draw the measured subject extremes back onto the frame they came from.

A min/max over a Vision mask is only as good as the mask; a reflection in the pool or a
speck would widen it and quietly force a wider crop than the shot needs. Look before trusting.
"""
import glob, json, os, subprocess, sys
import numpy as np, cv2
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'recentre'))
from anchor import anchors
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./config.js')))"], cwd=HERE).decode())['SRC']
man = {m['name']: m for m in json.load(open(os.path.join(HERE, 'shots', 'manifest.json')))}
rows = []
for shot in sys.argv[1:]:
    fr = []
    for f in sorted(glob.glob(os.path.join(HERE, 'recentre', 'mk', shot, '*.mask.png'))):
        if os.path.basename(f).startswith('._'): continue
        m = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        if m is None: continue
        a = anchors(m > 127)
        if a: fr.append((int(os.path.basename(f)[:3]), a, m > 127))
    if not fr: continue
    wide = min(fr, key=lambda x: x[1]['l'])
    idx, a, mask = wide
    t = man[shot]['absStart'] + (idx - 0.5) / 2.0     # collect2 sampled at 2 fps
    o = f'/tmp/_vs_{shot}.png'
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', SRC,
                    '-frames:v', '1', o], check=True)
    im = cv2.imread(o)
    # overlay the mask that produced the measurement
    mk = cv2.resize(mask.astype(np.uint8) * 255, (im.shape[1], im.shape[0]))
    im[mk > 127] = (0.62 * im[mk > 127] + 0.38 * np.array([0, 0, 255])).astype(np.uint8)
    for v, col in ((a['l'], (0, 255, 255)), (a['r'], (0, 255, 255))):
        x = int(v * im.shape[1]); cv2.line(im, (x, 0), (x, im.shape[0]), col, 6)
    cv2.putText(im, f"{shot}  l={a['l']:.3f} r={a['r']:.3f}  t={t:.2f}s",
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 255), 4)
    rows.append(cv2.resize(im, (860, 484)))
if rows:
    n = len(rows); g = np.vstack([np.hstack(rows[i:i+2]) if len(rows[i:i+2]) == 2
        else np.hstack([rows[i], np.zeros_like(rows[i])]) for i in range(0, n, 2)])
    cv2.imwrite(os.path.join(HERE, 'shots', 'span_check.jpg'), g)
    print('shots/span_check.jpg', g.shape)
