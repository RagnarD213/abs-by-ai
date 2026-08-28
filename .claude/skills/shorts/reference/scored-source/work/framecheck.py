#!/usr/bin/env python3
"""Two standing rules, checked against the PLAN before a single frame is encoded.

  1. NOTHING IMPORTANT LEAVES THE FRAME. The subject's measured silhouette union must sit
     inside the crop window. Dan: "make sure I'm not going off screen when I do the ab wheel
     rollout."
  2. NO GRAPHIC IS SLICED. Muhammad's burned overlays must be either entirely inside the
     window or entirely outside it. Dan: "double-check for graphics that are cropped out or
     which don't make any sense in the video."
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(HERE, 'layout.json')))
geom = json.load(open(os.path.join(HERE, 'shots', 'geom.json')))
crops = json.load(open(os.path.join(HERE, 'shots', 'crops.json')))
plan = json.loads(subprocess.check_output(
    ['node', '-e', "const p=require('./plan.js');console.log(JSON.stringify({SHOTS:p.SHOTS,TALK_X:p.TALK_X}))"],
    cwd=HERE, stderr=subprocess.DEVNULL).decode())
SRC_W = 1920.0
bad = 0

def window(n, spec):
    """The crop window in source-x fractions, plus the y range it keeps."""
    if spec['t'] in ('talk', 'broll'):
        cw = L['talk']['dropZoomW'] if spec.get('zoom') else L['talk']['dropW']
        x0 = min(max(crops[n] * SRC_W - cw / 2, 0), SRC_W - cw)
        if spec.get('minX0') is not None: x0 = max(x0, spec['minX0'])
        y1 = (L['talk']['zoomH'] / 1080.0) if spec.get('zoom') else 1.0
        return x0 / SRC_W, (x0 + cw) / SRC_W, 0.0, y1
    if spec['t'] == 'extern':
        return None
    c = spec.get('cardCrop') or [0, 1, 0, 1]
    return c[0], c[1], c[2], c[3]

for n, spec in plan['SHOTS'].items():
    w = window(n, spec)
    if w is None:
        print(f"  {n:12s} extern clip - checked separately"); continue
    x0, x1, y0, y1 = w
    g = geom[n]
    # rule 1: subject inside
    s = g['subject']
    if s:
        cl = max(0.0, x0 - s[0]); cr = max(0.0, s[1] - x1)
        if cl > 0.004 or cr > 0.004:
            print(f"  {n:12s} SUBJECT CLIPPED  left {cl*SRC_W:5.0f}px  right {cr*SRC_W:5.0f}px "
                  f"(subject {s[0]:.3f}-{s[1]:.3f}, window {x0:.3f}-{x1:.3f})"); bad += 1
    # rule 2: every graphic whole, or absent from the window entirely
    for tag in ('graphic_top', 'graphic_bot'):
        gr = g.get(tag)
        if not gr: continue
        gy_out = gr[3] <= y0 + 0.004 or gr[2] >= y1 - 0.004   # cropped off vertically (zoom)
        inside = gr[0] >= x0 - 0.004 and gr[1] <= x1 + 0.004
        outside = gr[1] <= x0 + 0.004 or gr[0] >= x1 - 0.004
        if not (gy_out or inside or outside):
            print(f"  {n:12s} GRAPHIC SLICED [{tag[8:]}] x {gr[0]:.3f}-{gr[1]:.3f} "
                  f"y {gr[2]:.2f}-{gr[3]:.2f}  window x {x0:.3f}-{x1:.3f} y {y0:.2f}-{y1:.2f}")
            bad += 1
print(f"\nframe check: {'PASS - subject contained and no graphic sliced, on all shots' if bad == 0 else f'{bad} violation(s)'}")
sys.exit(0 if bad == 0 else 1)
