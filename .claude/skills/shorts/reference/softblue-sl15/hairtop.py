#!/usr/bin/env python3
"""SL-15: is Dan's hair cut by the CAMERA on the talking shots? For every talking output frame every 0.25 s: the raw C1512 frame,
his head columns (Vision mask at ear level, track.json), the top 8 source rows: share of hair-dark pixels (luma < 60 on the graded
frame). Hair reaching row 0 means the camera frame itself cut it, so no vertical crop can show the top of his hair."""
import json, subprocess, sys, numpy as np
sys.path.insert(0, "."); import lib
FPS = 30000 / 1001
def frame(t):
    b = subprocess.run([lib.FF, "-v", "error", "-ss", f"{max(0, t - 1):.3f}", "-i", f"{lib.RAWD}/C1512.MP4", "-ss", f"{min(1, t):.3f}", "-frames:v", "1",
                        "-vf", "crop=1920:24:0:0,scale=in_color_matrix=bt709:in_range=tv,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(24, 1920)
out = {}
for S in sys.argv[1:]:
    shots = json.load(open(f"build/{S}/shots.json")); trk = json.load(open(f"build/{S}/track.json")); rows = []
    for sh in shots:
        if sh["kind"] != "talk": continue
        tr = trk.get(f"{sh['roll']}:{sh['raw0']:.2f}:{sh['raw1']:.2f}", [])
        for j in range(0, len(sh["raw"]), 8):
            t = sh["raw"][j]; r = min((r for r in tr if "hx0" in r), key=lambda r: abs(r["t"] - t), default=None)
            if not r: continue
            f = frame(t); x0, x1 = r["hx0"] + 20, r["hx1"] - 20
            d0 = float((f[0:2, x0:x1] < 60).mean()); rows.append(dict(t_out=round((sh["f0"] + j) / FPS, 2), src=round(t, 2), row0_hair=round(d0, 2)))
    touch = [r for r in rows if r["row0_hair"] > 0.25]
    out[S] = dict(samples=len(rows), hair_at_top_row=len(touch), share=round(len(touch) / max(1, len(rows)), 3), worst=sorted(rows, key=lambda r: -r["row0_hair"])[:5])
    print(S, out[S]["samples"], "samples;", out[S]["hair_at_top_row"], "with his hair in the camera frame's top row", out[S]["worst"][:3])
json.dump(out, open("hairtop.json", "w"), indent=1)
