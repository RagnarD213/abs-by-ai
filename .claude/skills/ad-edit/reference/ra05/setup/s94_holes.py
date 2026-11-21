#!/usr/bin/env python3
"""RA-05 setup: the media-card plates' REAL windows (open = B0049 generation, tour = B0544), measured on the locked plate MOVs.

hf9/plates.json gives each plate's configured `hole`. The plate is an opaque Soft Blue field with that window cut out (alpha 0),
so the media under it is what shows. The gate's caption clearance must grade the pixels the window occupies: this measures, on
every plate frame, the bounding box of the transparent pixels (alpha < 128) and writes setup/holes.json {name: {rect, ...}} with
the union over the frames and the configured hole for comparison.
"""
import json, sys
import numpy as np
WD = "/Volumes/Extreme/_edit_work/ra05"; R3 = f"{WD}/round3"
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as CP
W, H = 1080, 1920
PL = json.load(open(f"{R3}/hf9/plates.json")); B = json.load(open(f"{R3}/beats.json"))
CARD = {c["name"]: c for c in B["cards"]}
out = {}
for nm in ("open", "tour"):
    n = CARD[nm]["frames"]; lo = [W, H]; hi = [0, 0]; k = 0
    for fr in CP.reader(PL[nm]["mov"], 0, n, True, (W, H)):
        ys, xs = np.nonzero(fr[..., 3] < 128)
        lo = [min(lo[0], int(xs.min())), min(lo[1], int(ys.min()))]; hi = [max(hi[0], int(xs.max()) + 1), max(hi[1], int(ys.max()) + 1)]
        k += 1
    assert k == n, (nm, k, n)
    out[nm] = dict(rect=lo + hi, frames=k, configured_hole=PL[nm]["hole"])
    print(nm, out[nm])
json.dump(out, open(f"{WD}/setup/holes.json", "w"), indent=1)
