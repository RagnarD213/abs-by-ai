#!/usr/bin/env python3
"""Grade fit to Muhammad's 2.5-min cut -- SKIN-PIXEL matched.

Rule 27 says fit per-channel percentiles on a face-sized crop of both videos. A fixed
centre crop does not work here: his cut is already punched in, so his centre crop is
almost all skin while ours still contains the dark doorway, and the fit then lifts our
shadows into haze to chase his skin values.

So: select SKIN pixels in both (framing-independent) and fit the mid/high control
points from those, and take the black point from each video's own global p1. Frames that
are graphic cards or cutaways are rejected first.
"""
import subprocess
import numpy as np

FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
REF = "/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/2720d234-b349-49b2-b9ef-e672524403d3/scratchpad/muhammad25.mp4"
OUR = "CUT_v2_graded.mp4"
REF_T = [29.0,30.5,33.0,34.0,36.5,40.5,65.5,67.0,84.0,86.0,105.0,122.5,124.0,133.0,145.0,150.0]
OUR_T = [33.0,36.0,38.0,40.0,44.0,49.0,78.0,80.0,100.0,103.0,126.0,150.0,152.0,163.0,176.0,182.0]

def frames(path, times, vf=""):
    out = []
    for t in times:
        chain = (vf + "," if vf else "") + "scale=320:180"
        raw = subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", path, "-vframes", "1",
                              "-vf", chain, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True).stdout
        f = np.frombuffer(raw, dtype=np.uint8).reshape(180, 320, 3).astype(np.float32)
        if f.reshape(-1, 3).std(0).mean() > 22 and f.mean() < 190:   # not a graphic card
            out.append(f)
    return out

def skin(fs):
    a = np.concatenate([f.reshape(-1, 3) for f in fs])
    r, g, b = a[:, 0], a[:, 1], a[:, 2]
    m = (r > g + 8) & (g > b + 4) & (r > 55) & (r < 250) & (r - b > 18) & (r - b < 130)
    return a[m]

def darkp(fs, p=1):
    a = np.concatenate([f.reshape(-1, 3) for f in fs])
    return np.percentile(a, p, axis=0)

PS = (10, 30, 50, 70, 90)
rf, of = frames(REF, REF_T), frames(OUR, OUR_T)
rs, os_ = skin(rf), skin(of)
print(f"skin pixels: his {len(rs)}  ours {len(os_)}")
rp = {c: np.percentile(rs[:, i], PS) for i, c in enumerate("rgb")}
op = {c: np.percentile(os_[:, i], PS) for i, c in enumerate("rgb")}
rd, od = darkp(rf), darkp(of)
print("skin percentiles (his/ours):")
for j, p in enumerate(PS):
    print(f"  p{p:<3}" + " ".join(f"  {c}:{rp[c][j]:5.0f}/{op[c][j]:<5.0f}" for c in "rgb"))
print("global p1 (black point) his", rd.round(1), " ours", od.round(1))

parts = []
for i, c in enumerate("rgb"):
    xs, ys = [0.0], [round(float(rd[i]) / 255, 4)]
    for j in range(len(PS)):
        x, y = float(op[c][j]) / 255, float(rp[c][j]) / 255
        if x - xs[-1] < 0.05 or y <= ys[-1]: continue
        xs.append(round(x, 3)); ys.append(round(min(0.995, y), 3))
    xs.append(1.0); ys.append(1.0)
    parts.append(f"{c}='" + " ".join(f"{x}/{y}" for x, y in zip(xs, ys)) + "'")
GRADE = "curves=" + ":".join(parts)
print("\n" + GRADE)
open("grade25.txt", "w").write(GRADE)

ck = skin(frames(OUR, OUR_T, GRADE))
cp = {c: np.percentile(ck[:, i], PS) for i, c in enumerate("rgb")}
before = np.mean([abs(rp[c][j] - op[c][j]) for c in "rgb" for j in range(len(PS))])
after  = np.mean([abs(rp[c][j] - cp[c][j]) for c in "rgb" for j in range(len(PS))])
print(f"\nskin mean |err|: {before:.1f} -> {after:.1f} levels")
