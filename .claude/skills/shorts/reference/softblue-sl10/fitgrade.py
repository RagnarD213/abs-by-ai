"""SL-10: the RO-13 master's look, measured. The film's own chain (grade-C.cube via lib.GRADE) on the raw C1707 read about
+5.6 R / +6 G / +4 B levels brighter than the delivered master on aligned talking frames (mae 5.5-5.7 of 255). Fit one tone
curve per channel (binned medians of aligned pixel pairs, top 600 rows: no lower thirds), test on held-out frames, write curves.json."""
import json, subprocess, numpy as np, lib
from PIL import Image
FPS = 30000 / 1001
C = json.load(open("ro13_cut_map.json"))["cuts"]
CROP = {"W2": (3552, 1998, 144, 162), "T2": (2608, 1466, 616, 184), "W4S": (2800, 1575, 0, 183), "W4": (2800, 1575, 520, 183)}
segs = json.load(open("/Volumes/Extreme/_edit_work/ro13/round2/RO13_MASTER.mp4.build.json"))["segments"]
def pair(t, curves="null"):
    c = next(c for c in C if c["out_in"] <= t < c["out_out"]); src = c["src_in"] + t - c["out_in"]
    m = subprocess.run([lib.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", "/Volumes/Extreme/_edit_work/ro13/round2/RO13_MASTER.mp4", "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    M = np.frombuffer(m, np.uint8).reshape(1080, 1920, 3)
    seg = next(x for x in segs if x["o0"] <= round(t * FPS) < x["o1"]); cw, ch, x, y = CROP[seg["framing"]]
    r = subprocess.run([lib.FF, "-v", "error", "-ss", f"{max(0, src - 2):.3f}", "-i", f"{lib.RAWD}/C1707.MP4", "-ss", f"{min(2, src):.3f}", "-frames:v", "1", "-vf",
                        f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le,lut3d=file='{lib.LUT}':interp=tetrahedral,format=rgb24,{curves}", "-f", "rawvideo", "-"], capture_output=True).stdout
    R = np.frombuffer(r, np.uint8).reshape(1080, 1920, 3)
    return M[:600].astype(float), R[:600].astype(float)
TRAIN = [64.0, 280.0, 344.0, 408.0, 30.0, 200.0, 263.5, 355.0]; TEST = [66.0, 285.0, 395.0]
if __name__ == "__main__":
    pts = {k: [] for k in range(3)}
    for t in TRAIN:
        M, R = pair(t)
        if np.abs(M - R).mean() > 15: print("skip", t, "(cover in the master)"); continue
        for k in range(3): pts[k].append(np.stack([R[..., k].ravel(), M[..., k].ravel()], 1))
    out = []
    for k, nm in enumerate("rgb"):
        p = np.concatenate(pts[k]); xs, ys = [0.0], [0.0]
        for a in range(0, 256, 8):
            s = p[(p[:, 0] >= a) & (p[:, 0] < a + 8)]
            if len(s) > 400: xs.append((a + 4) / 255); ys.append(float(np.median(s[:, 1])) / 255)
        xs.append(1.0); ys.append(max(ys[-1], 1.0) if False else min(1.0, ys[-1] + (1 - xs[-2]) * (ys[-1] - ys[-2]) / max(1e-6, xs[-2] - xs[-3])))
        ys = list(np.maximum.accumulate(np.convolve(np.pad(ys, 1, mode="edge"), [0.25, 0.5, 0.25], mode="valid")))
        out.append(f"{nm}='" + " ".join(f"{x:.4f}/{y:.4f}" for x, y in zip(xs, ys)) + "'")
    flt = "curves=" + ":".join(out)
    for t in TEST:
        M, R = pair(t); M2, R2 = pair(t, flt); print("held-out", t, "mae", round(np.abs(M - R).mean(), 2), "->", round(np.abs(M2 - R2).mean(), 2))
    json.dump({"filter": flt}, open("curves.json", "w")); print(flt[:200])
