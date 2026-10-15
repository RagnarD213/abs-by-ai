#!/usr/bin/env python3
"""RA-15 round 3: his BODY extent per talking hold, 10 samples a second, on the graded source (person mask, half scale), written to
framing_body.json. The 9:16 tracker centres on the body's middle (arms included, chest height and up) held within 8 % of the crop width
of his head (s05_plan15.py), because centring the head alone left an arm off one edge with 90-190 px empty on the other (review)."""
import json, os, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15")
import ra01lib as L
CUT = json.load(open("cut.json")); B = json.load(open("beats.json")); FPS = L.FPS; fr = lambda t: int(round(t*FPS)); HALF = 2.0
GRADE = L.grade(); P = CUT["pieces"]
def src_frame(t):
    f = fr(t)
    for p in P:
        if fr(p["t_in"]) <= f < fr(p["t_out"]): return fr(p["src_in"]) + (f - fr(p["t_in"]))
    lp = P[-1]; return fr(lp["src_in"]) + (f - fr(lp["t_in"]))          # the end hold runs on from the last piece
want = {}
for it in [x for x in B["timeline"] if x["kind"] == "dan"]:
    a, b = it["f0"]/FPS, it["f1"]/FPS; t = a
    while t < b - 1e-3:
        want[src_frame(t)] = round(t, 4); t += 0.1
    want[src_frame(b - 1/FPS)] = round(b - 1/FPS, 4)
tmp = tempfile.mkdtemp(prefix="ra15body_"); paths = {}
srcs = sorted(want)
# one decode per contiguous run of source frames (cheap), not one seek per sample
for sf in srcs:
    p = os.path.join(tmp, "%06d.png" % sf)
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{sf/FPS + 0.002:.4f}", "-i", L.ROLL, "-frames:v", "1",
                    "-vf", f"{L.DECODE},{GRADE},scale=1080:1920:flags=bilinear", "-y", p], check=True)
    paths[sf] = p
subprocess.run([L.PERSONMASK, tmp] + list(paths.values()), capture_output=True, text=True)
hair = {round(p["beat"][0], 3): p["hair_min"] for p in B["punch"]}
out, miss = [], 0
for sf in srcs:
    mp_ = paths[sf][:-4] + ".mask.png"
    if not os.path.exists(mp_): miss += 1; continue
    m = np.asarray(Image.open(mp_).convert("L")) > 127
    rows = m[int(1300/HALF):int(2450/HALF)]            # hair (~1400) to the waist (~2400) in source px: arms and hands, not legs
    cols = np.where(rows.any(0))[0]
    if not len(cols): miss += 1; continue
    out.append({"t": want[sf], "src_frame": sf, "l": round(cols[0]*HALF, 1), "r": round(cols[-1]*HALF, 1), "mid": round((cols[0]+cols[-1])/2*HALF, 1)})
shutil.rmtree(tmp, ignore_errors=True)
json.dump({"samples": out, "misses": miss}, open("framing_body.json", "w"), indent=1)
print(f"framing_body.json: {len(out)} samples ({miss} misses)")
