#!/usr/bin/env python3
"""Full-frame-rate cut finder: mean abs diff between consecutive 160x90 frames; a cut is a
spike well above the local median. Replaces the 320x180 `scene` detector, which missed
Zeeshan's wide<->medium punch-ins on this master."""
import json, subprocess, sys, numpy as np
sys.path.insert(0, '.')
cfg = json.loads(subprocess.check_output(['node', '-e', "const c=require('./config.js');const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify({c,S:SEGMENTS}))"]))
FF, SRC = cfg['c']['FF'], cfg['c']['SRC']
FPS = 30000/1001
res = {}
for seg in cfg['S']:
    for pi, p in enumerate(seg['pieces']):
        a0 = max(0, p['start'] - 0.5); dur = p['end'] - a0 + 0.5
        raw = subprocess.run([FF, '-v', 'error', '-ss', f'{a0:.3f}', '-i', SRC, '-t', f'{dur:.3f}',
                              '-vf', 'scale=160:90', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                             capture_output=True).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(np.float32)
        d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
        med = np.median(d) + 0.3
        cuts = []
        for i in range(1, len(d) - 1):
            if d[i] > 6 * med and d[i] > 4 and d[i] >= d[i-1] and d[i] >= d[i+1]:
                t = a0 + (i + 1) / FPS   # first frame of the new shot
                cuts.append(round(t, 3))
        res[f"{seg['id']}-p{pi}"] = {'start': p['start'], 'end': p['end'], 'cuts': cuts,
                                     'score': [round(float(x), 1) for x in d[[int(round((c - a0) * FPS)) - 1 for c in cuts]]] if cuts else []}
        print(seg['id'], pi, p['start'], p['end'], cuts)
json.dump(res, open('work/cuts.json', 'w'), indent=1)
