#!/usr/bin/env python3
"""Propose a centred window per shot, then render SHIPPED vs PROPOSED, five frames across
each shot. The metric is a shortlist; nothing changes until this sheet has been looked at."""
import glob, json, os, subprocess, sys
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anchor import anchors
HERE = os.path.dirname(os.path.abspath(__file__)); BD = os.path.dirname(HERE)
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = json.loads(subprocess.check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./config.js')))"], cwd=BD).decode())['SRC']
L = json.load(open(os.path.join(BD, 'layout.json')))
CW, CH = L['canvas']; SRC_W, SRC_H = 1920, 1080
meta = {s['shot']: s for s in json.load(open(os.path.join(HERE, 'fr.json')))['shots']}
crops = json.load(open(os.path.join(BD, 'shots', 'crops.json')))
audit = {r['shot']: r for r in json.load(open(os.path.join(HERE, 'audit.json')))}

def torso(shot):
    A = []
    for f in sorted(glob.glob(os.path.join(HERE, 'mk', shot, '*.mask.png'))):
        m = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        if m is None: continue
        a = anchors(m > 127)
        if a: A.append(a['torso'])
    return float(np.median(A))

def propose(shot):
    sh = meta[shot]; T = torso(shot)
    if sh['t'] in ('talk', 'broll'):
        cw = L['talk']['zoomW'] if sh['zoom'] else L['talk']['cropW']
        half = cw / 2 / SRC_W
        return ('x', round(float(np.clip(T, half, 1 - half)), 4))
    cc = list(sh['cardCrop'] or [0, 1, 0, 1])
    w = cc[1] - cc[0]
    x0 = float(np.clip(T - w / 2, 0, 1 - w))
    return ('cardCrop', [round(x0, 4), round(x0 + w, 4), cc[2], cc[3]])

def render(shot, mode, val, t):
    o = f"/tmp/_pab_{shot}_{t:.2f}.png"
    if not os.path.exists(o):
        subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', SRC,
                        '-frames:v', '1', o], check=True)
    im = cv2.imread(o); sh = meta[shot]
    if mode == 'x':
        cw = L['talk']['zoomW'] if sh['zoom'] else L['talk']['cropW']
        ch = L['talk']['zoomH'] if sh['zoom'] else SRC_H
        x0 = int(round(min(max(val * SRC_W - cw / 2, 0), SRC_W - cw)))
        if sh['minX0'] is not None: x0 = max(x0, sh['minX0'])
        return cv2.resize(im[0:ch, x0:x0 + cw], (200, 356), interpolation=cv2.INTER_AREA)
    x0, x1, y0, y1 = val
    sub = im[int(y0 * SRC_H):int(y1 * SRC_H), int(x0 * SRC_W):int(x1 * SRC_W)]
    k = min(L['card']['w'] / sub.shape[1], L['card']['h'] / sub.shape[0])
    fit = cv2.resize(sub, (int(sub.shape[1] * k), int(sub.shape[0] * k)), interpolation=cv2.INTER_AREA)
    canvas = np.zeros((CH, CW, 3), np.uint8)
    cx = L['card']['x'] + (L['card']['w'] - fit.shape[1]) // 2
    cy = L['card']['y'] + (L['card']['h'] - fit.shape[0]) // 2
    canvas[cy:cy + fit.shape[0], cx:cx + fit.shape[1]] = fit
    return cv2.resize(canvas, (200, 356), interpolation=cv2.INTER_AREA)

shots = sys.argv[1:]
out_props = {}
rows = []
for n in shots:
    sh = meta[n]; mode, new = propose(n)
    old = crops[n] if mode == 'x' else (sh['cardCrop'] or [0, 1, 0, 1])
    out_props[n] = {'mode': mode, 'old': old, 'new': new}
    strip = []
    for i in range(5):
        t = sh['start'] + sh['dur'] * (i + 0.5) / 5
        a = render(n, mode, old, t); b = render(n, mode, new, t)
        strip += [np.hstack([a, np.zeros((356, 4, 3), np.uint8), b]), np.zeros((356, 14, 3), np.uint8)]
    body = np.hstack(strip)
    lab = np.zeros((26, body.shape[1], 3), np.uint8)
    o = audit[n]
    cv2.putText(lab, f"{n} [{sh['t']}]  SHIPPED {old} | PROPOSED {new}   off {o['off']:+.0f}px  cut-off {o['cutoff']:.0f}px",
                (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1)
    rows.append(np.vstack([lab, body]))
w = max(r.shape[1] for r in rows)
rows = [np.hstack([r, np.zeros((r.shape[0], w - r.shape[1], 3), np.uint8)]) for r in rows]
cv2.imwrite(os.path.join(HERE, 'ab.jpg'), np.vstack(rows))
json.dump(out_props, open(os.path.join(HERE, 'proposals.json'), 'w'), indent=1)
print('ab.jpg', len(rows), 'shots')
