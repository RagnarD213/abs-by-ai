"""Trace each stub's centre line from its own pixels (median over frames 0..118 of the card), x by x."""
import json, sys, numpy as np, cv2
sys.argv = ["x"]; import importlib.util
spec = importlib.util.spec_from_file_location("S", "s06_scan3.py"); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
acc = {k: {} for k in S.STUBS}
for g, a in enumerate(S.frames()):
    if g % 6: continue
    cm = S.core(a)
    for k, pts in S.STUBS.items():
        for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                if x < 0 or x >= 608: continue
                yr = y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 != x0 else y0
                lo, hi = int(yr) - 9, int(yr) + 10
                col = cm[lo:hi, x]
                if col.sum() >= 1:
                    ys = np.arange(lo, hi)[col]; acc[k].setdefault(x, []).append(float(ys.mean()))
out = {}
for k, d in acc.items():
    xs = sorted(d); out[k] = [[x, round(float(np.median(d[x])), 1)] for x in xs if len(d[x]) >= 5]
    print(k, len(out[k]), out[k][:3], out[k][-3:])
json.dump(out, open("scan3/stub_paths.json", "w"))
