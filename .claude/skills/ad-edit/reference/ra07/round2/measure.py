#!/usr/bin/env python3
"""Measure every pause splice and the take seam of cut.json on the graded source, at the round 2 FAR crop.
For each join: the difference between the last kept frame before it and the first after it, against the median
difference of the two frame pairs either side (the roll's own motion). ratio >= 2 reads as a visible jump."""
import json, subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
W7 = "/Volumes/Extreme/_edit_work/ra07"
CUT = json.load(open(f"{W7}/cut.json")); TRK = json.load(open(f"{W7}/framing.json"))["samples"]
FPS = L.FPS; cw, ch = L.Aspect("9x16").levels["FAR"]


def frames(src_f0, n, cx, hair):
    y = int(round(hair - 0.04*ch)); y -= y % 2; x = int(round(cx - cw/2)); x -= x % 2
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{(src_f0-0.5)/FPS:.5f}", "-i", L.ROLL, "-frames:v", str(n),
                          "-vf", f"crop={cw}:{ch}:{x}:{y},{L.DECODE},{L.grade()},scale=180:320", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 320, 180).astype(float)


out = []
P = CUT["pieces"]
for k in range(len(P) - 1):
    a, b = P[k], P[k+1]
    t = b["t_in"]
    s = min(TRK, key=lambda x: abs(x["t"] - t)); hair = min(x["hair"] for x in TRK if abs(x["t"] - t) < 2)
    fa = int(round(a["src_out"]*FPS)); fb = int(round(b["src_in"]*FPS))
    A = frames(fa - 3, 3, s["cx"], hair); B = frames(fb, 3, s["cx"], hair)
    d = lambda u, v: float(np.abs(u - v).mean())
    join = d(A[-1], B[0]); ctrl = np.median([d(A[0], A[1]), d(A[1], A[2]), d(B[0], B[1]), d(B[1], B[2])])
    out.append(dict(t=round(t, 3), join=round(join, 2), ctrl=round(float(ctrl), 2), ratio=round(join/max(ctrl, 0.3), 1),
                    seam=a["range"] != b["range"]))
    print(out[-1], flush=True)
json.dump(out, open(f"{W7}/round2/splices/splices.json", "w"), indent=1)
