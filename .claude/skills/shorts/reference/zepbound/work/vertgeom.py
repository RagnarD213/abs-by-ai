#!/usr/bin/env python3
"""Choose the vertical crop: how much dead ceiling to remove.

⚠ The naive "mask top" is NOT the head. Vision leaves a faint low-confidence sliver along
the top frame edge on some frames, which put three beats' head at source row 15-24 against
~180 everywhere else - a 160px error that would have set the whole batch's geometry. Head
top is therefore the first row carrying a real RUN of mask (>=20px at 640, ~60px at 1920),
inside the largest connected component only.

The full-height 724x1080 window puts his head at delivered y=574, a quarter of the Short
being kitchen ceiling. Cropping rows off the TOP narrows the window (fixed 2:3 aspect) -
the trap the skill records - but here that is the right direction: it also makes Dan bigger,
which a talking-head Short wants. Constraint: his head clears dropTop=310 by >=60px on every
beat at his highest (the ab-wheel batch shipped at 62px).
"""
import glob, json
import numpy as np, cv2

def head_top(path):
    m = (cv2.imread(path, cv2.IMREAD_GRAYSCALE) > 127).astype(np.uint8)
    nl, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if nl < 2: return None
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    big = lab == k
    rows = np.nonzero(big.sum(1) >= 20)[0]
    return None if not len(rows) else rows[0] / m.shape[0] * 1080

tops = {}
for d in sorted(glob.glob('work/mk/*/')):
    name = d.strip('/').split('/')[-1]
    t = [h for h in (head_top(f) for f in sorted(glob.glob(d + '*.mask.png'))) if h is not None]
    tops[name] = (min(t), max(t))
gmin = min(v[0] for v in tops.values())
worst = min(tops, key=lambda k: tops[k][0])
print(f"head top per beat (source rows): global min {gmin:.0f} ({worst}), "
      f"per-beat min range {min(v[0] for v in tops.values()):.0f}..{max(v[0] for v in tops.values()):.0f}")
for k in sorted(tops): print(f"   {k:10s} {tops[k][0]:6.0f} .. {tops[k][1]:6.0f}")
print(f"\n{'cropTop':>8s} {'cropH':>6s} {'cropW':>6s} {'upscale':>8s} {'head y':>7s} {'clear':>6s}")
pick = None
for T in (0, 60, 100, 120, 140, 150, 160, 180):
    Hc = 1080 - T; Wc = int(round(Hc * 1080 / 1610)) // 2 * 2
    hy = 310 + (gmin - T) * (1610 / Hc)
    ok = hy - 310 >= 60
    if ok: pick = (T, Hc, Wc, hy)
    print(f"{T:8d} {Hc:6d} {Wc:6d} {1080/Wc:7.2f}x {hy:7.0f} {hy-310:6.0f} {'' if ok else '  <- head enters the title band'}")
T, Hc, Wc, hy = pick
print(f"\nCHOSEN cropTop={T} cropH={Hc} cropW={Wc} ({1080/Wc:.2f}x upscale), "
      f"head at y={hy:.0f}, {hy-310:.0f}px clear of the title band")
json.dump({'cropTop': T, 'cropH': Hc, 'cropW': Wc, 'headY': round(hy, 1),
           'headTopSrc': round(gmin, 1),
           'tops': {k: [round(a, 1), round(b, 1)] for k, (a, b) in tops.items()}},
          open('work/vertgeom.json', 'w'), indent=1)
