#!/usr/bin/env python3
"""Generate a vertical track in a new build directory from measured head centres.
raw_torso.npy is a legacy filename: samples MUST represent head centre, not body centroid.
Supply raw_torso_n.npy with exact frame indices including every picture cut start.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_shared", "cut"))
import landing
raw = np.load("raw_torso.npy")
n = np.load("raw_torso_n.npy").astype(int)
segments = json.load(open("edl_picture.json"))
fps = 30000 / 1001
crop_width = 608
for start, end in landing.seg_bounds(segments, fps):
    if start not in n or not np.isfinite(raw[np.where(n == start)[0][0]]):
        raise SystemExit(f"Missing measured head centre at cut frame {start}")
na, centres, heads, info = landing.vertical_dense(n, raw, segments, crop_width, fps)
x = centres - crop_width / 2
if np.any((x < 0) | (x > 1920 - crop_width)):
    raise SystemExit("Centred crop leaves source bounds: use a wider window")
stats = landing.motion_stats(na, heads, centres, segments, crop_width, fps)
info['policy'] = 'vertical-land-then-hold-20261003'
json.dump(dict(n=na.tolist(), x=x.tolist(), crop_w=crop_width, segments=segments, method=info, stats=stats), open("facetrack.json", "w"))
print(json.dumps(stats))
