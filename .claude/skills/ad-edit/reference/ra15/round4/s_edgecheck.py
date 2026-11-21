#!/usr/bin/env python3
"""RA-15 round 3: per talking hold of a delivered master, how often his body touches a side edge (person mask, 10 fps), and on those
frames how much room the other side had (a crop that could have fitted him).  s_edgecheck.py <master> 9x16|16x9"""
import glob, json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra15")
import ra01lib as L
M, K = sys.argv[1], sys.argv[2]
B = json.load(open("beats.json")); FPS = L.FPS
W, H = (270, 480) if K == "9x16" else (480, 270)
out = []
for it in [x for x in B["timeline"] if x["kind"] == "dan"]:
    a, b = it["f0"] / FPS, it["f1"] / FPS
    tmp = tempfile.mkdtemp(prefix="edge_")
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{a + 0.05:.3f}", "-t", f"{b - a - 0.1:.3f}", "-i", M, "-vf", f"fps=10,scale={W}:{H}", f"{tmp}/f%04d.png"], check=True)
    fs = sorted(glob.glob(f"{tmp}/f*.png")); subprocess.run([L.PERSONMASK, tmp] + fs, capture_output=True)
    touch, room = 0, []
    for f in fs:
        m = f[:-4] + ".mask.png"
        if not os.path.exists(m): continue
        k = np.asarray(Image.open(m).convert("L")) > 127
        rows = k[: int(H * 0.75)]                      # above the bottom quarter (legs/shorts run off the bottom by design)
        lt, rt = rows[:, :2].any(), rows[:, -2:].any()
        if lt != rt:
            touch += 1
            cols = np.where(rows.any(0))[0]
            room.append(int((W - 1 - cols.max()) if lt else cols.min()) * (1080 if K == "9x16" else 1920) // W)
    out.append(dict(hold=it["name"], a=round(a, 2), b=round(b, 2), frames=len(fs), one_side_touch=touch,
                    worst_room_other_side_px=max(room) if room else 0))
    print(out[-1], flush=True)
json.dump(out, open(f"round4/edgecheck_{K}.json", "w"), indent=1)
