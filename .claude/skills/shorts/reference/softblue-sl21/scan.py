"""scan.py: verify the film's presenter cut list (silence.json joins, from layout.json) against a frame-difference scan of base.mp4 over
each Short's film ranges (softblue-sl20 README: 192x108 gray, diff > max(8, 6x median))."""
import json, subprocess, sys, numpy as np
sys.path.insert(0, "recipe"); import lib, plans as P
FPS = 30000 / 1001; J = json.load(open("silence.json"))["joins"]
for S, segs in P.SEG.items():
    for a, b in segs:
        a0 = max(0, a - 1.0); n = int((b + 1.0 - a0) * FPS)
        raw = subprocess.run([lib.FF, "-v", "error", "-ss", f"{a0:.3f}", "-i", lib.SRC, "-frames:v", str(n), "-vf", "scale=192:108,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
        fr = np.frombuffer(raw, np.uint8).reshape(-1, 108, 192).astype(np.float32); d = np.abs(fr[1:] - fr[:-1]).mean((1, 2)); thr = max(8, 6 * float(np.median(d)))
        f0 = int(round(a0 * FPS)); cuts = [round((f0 + i + 1) / FPS, 3) for i in np.where(d > thr)[0]]
        want = [j for j in J if a0 < j < b + 1.0]
        miss = [j for j in want if not any(abs(j - c) < 0.02 for c in cuts)]; extra = [c for c in cuts if not any(abs(j - c) < 0.02 for j in want)]
        print(S, f"{a:.2f}-{b:.2f} median diff {np.median(d):.2f} thr {thr:.1f} | scan cuts {cuts} | list {want} | in list, not seen {miss} | seen, not in list {extra}")
        for j in miss:
            k = int(round(j * FPS)) - f0 - 1; print("   ", j, "diff around:", [round(float(x), 1) for x in d[max(0, k - 2):k + 3]])
