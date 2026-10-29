"""SL-10: measure each cover clip against the graded presenter (VIDEO-RULES 2026-10-11 / 10-23: a real grade, curves with true blacks,
never a gamma lift). Prints p2/p50/p98 of luma, black share (<16), mean saturation, warmth (R-B) at the clip's used mid-point, before
and after its plans eq. python3 grade.py [ids]"""
import subprocess, sys, numpy as np, json, lib, plans as P
FPS = 30000 / 1001
def stats(a):
    a = a.astype(float); y = a @ [0.2126, 0.7152, 0.0722]; mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    return "p2/50/98 %3d/%3d/%3d black %4.1f%% sat %.2f warm %+5.1f" % (*np.percentile(y, [2, 50, 98]), 100 * (y < 16).mean(), sat.mean(), (a[..., 0] - a[..., 2]).mean())
def grab(src, t, eq=None):
    vf = "scale=960:-2:in_color_matrix=bt709:in_range=tv" + ("," + eq if eq else "") + ",format=rgb24"
    p = subprocess.run([lib.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True).stdout
    h = len(p) // (960 * 3); return np.frombuffer(p, np.uint8)[: 960 * 3 * h].reshape(h, 960, 3)
if __name__ == "__main__":
    dan = np.asarray(lib.raw("C1707", 481.5, 1920, 1080))[:, 600:1400]
    print("%-10s %s" % ("DAN", stats(dan)))
    want = sys.argv[1:]
    for S, cs in P.COVERS.items():
        for c in cs:
            if want and c["id"] not in want: continue
            if c["src"].endswith(".mov"): continue
            t = c.get("t", 0) + 1.0
            print("%-10s %s" % (c["id"], stats(grab(c["src"], t))))
            if c.get("eq"): print("%-10s %s" % ("  +eq", stats(grab(c["src"], t, c["eq"]))))
