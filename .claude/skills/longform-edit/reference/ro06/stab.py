"""Round 5: the camera operator re-aimed inside two presenter shots (kb3.0r6: a pan of about 110 source px over 5 s;
mb2.0r0: a tilt of about 100 source px in the first 4 s). 16:9 rule: the presenter picture does not move inside a shot,
and a source that moves is fixed by stabilising, not by calling it static. This measures the background's travel per
source frame (Lucas-Kanade on background corners, his column masked out), relative to where the camera SETTLES, and
writes round5/stab.json {segment key: [[dx, dy] per frame]}. build.render_seg slides the crop by that much, so the
background holds still and the framing is the settled one from the first frame. usage: stab.py KEY [KEY ...]"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
import build as Bd, frames as F
W = Bd.W; out_p = f"{W}/round5/stab.json"; ST = json.load(open(out_p)) if os.path.exists(out_p) else {}
for key in sys.argv[1:]:
    sg = next(s for s in Bd.all_segments() if s["key"] == key); n = sg["o1"] - sg["o0"]; roll, lf = F.roll_of(sg["src0"]); ts = lf/Bd.FPS; ss = max(0, ts - 1)
    raw = subprocess.run([Bd.FF, "-v", "error", "-ss", f"{ss:.4f}", "-i", F.ROLLS[roll]["path"], "-ss", f"{max(0, ts-ss-0.4/Bd.FPS):.4f}", "-frames:v", str(n),
                          "-vf", "scale=960:540:in_color_matrix=bt709:in_range=tv,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    G = np.frombuffer(raw, np.uint8).reshape(-1, 540, 960); assert len(G) == n, (len(G), n)
    cx = F.SF[sg["shot"]]["cx"]/2; x0, x1 = F.SF[sg["shot"]]["x_extent"]; mask = np.full((540, 960), 255, np.uint8); mask[:, int(max(0, x0/2 - 40)):int(min(960, x1/2 + 40))] = 0
    mask[430:, :] = 0                                     # the water and the equipment at his feet shimmer and move
    d = np.zeros((n, 2)); 
    for i in range(1, n):
        p = cv2.goodFeaturesToTrack(G[i-1], 300, 0.01, 8, mask=mask)
        q, st, _ = cv2.calcOpticalFlowPyrLK(G[i-1], G[i], p, None, winSize=(21, 21), maxLevel=3)
        ok = st.ravel() == 1; d[i] = d[i-1] + np.median((q - p)[ok].reshape(-1, 2), 0)
    d *= 2                                                # back to source px; d[i] = where the background sits against frame 0
    k = np.exp(-0.5*(np.arange(-6, 7)/2.5)**2); k /= k.sum(); sm = np.stack([np.convolve(np.pad(d[:, j], 6, mode="edge"), k, "valid") for j in (0, 1)], 1)
    ref = sm[int(n*0.8):].mean(0); off = sm - ref        # against the settled camera
    last = max([i for i in range(n) if np.abs(off[i]).max() > 1.5] or [0]); ease = np.clip((last + 12 - np.arange(n))/12.0, 0, 1)[:, None]
    off = off*ease                                        # exactly still once the camera has settled
    ST[key] = [[round(float(a), 2), round(float(b), 2)] for a, b in off]
    print(key, roll, n, "frames; travel x", round(float(off[:, 0].min()), 1), "to", round(float(off[:, 0].max()), 1), "y", round(float(off[:, 1].min()), 1), "to", round(float(off[:, 1].max()), 1),
          "| settles at frame", last, f"({last/Bd.FPS:.1f} s in) | crop", sg["crop"], sg["framing"])
json.dump(ST, open(out_p, "w"))
