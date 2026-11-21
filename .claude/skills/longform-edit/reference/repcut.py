#!/usr/bin/env python3
"""Find POSE-MATCHED trim points inside the live workout sets.

Why this and not "cut on a rep boundary": the three sets are 178 s of near-silent
rollouts and they are where 158 s of this video's 205 s of dead air actually lives.
Shortening them is the only way to reach the reference cut's runtime -- but a splice
inside a repetitive movement is glaring if the body is in a different position either
side of it. So instead of guessing where a rep starts, search for the PAIR of frames
(i, j) that look most alike and whose distance is close to the amount to remove: cut
i->j and the body is in the same place across the splice.

Frames are compared as 64x36 greyscale, which is coarse enough to ignore compression
noise and fine enough to separate arms-out from arms-in.
"""
import subprocess, sys, json
import numpy as np
FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
SRC = "/Volumes/Extreme/_edit_work/abwheel/roughcuts/CUT_v2_graded.mp4"
FPS = 15

def frames(a, b):
    raw = subprocess.run([FF,"-v","error","-ss",f"{a}","-t",f"{b-a}","-i",SRC,
        "-vf",f"fps={FPS},scale=64:36,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.uint8).reshape(-1,64*36).astype(np.float32)

def cadence(F):
    d = np.abs(np.diff(F,axis=0)).mean(1)
    x = d - d.mean()
    S = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1/FPS)
    ok = (f > 1/8.0) & (f < 1/1.5)          # a rollout rep is 1.5-8 s
    return float(1/f[ok][np.argmax(S[ok])])

def best_pair(F, t0, keep_head, keep_tail, remove, win=2.5):
    """Cut from t0+keep_head to (that + remove); slide both ends +/- win to find the
    pose-matched pair. Returns (cut_in, cut_out, distance, baseline_distance)."""
    n = len(F)
    i0 = int(keep_head*FPS); j0 = int((keep_head+remove)*FPS); w = int(win*FPS)
    best = None
    for i in range(max(1,i0-w), min(n-2, i0+w)):
        for j in range(max(i+FPS, j0-w), min(n-1, j0+w)):
            # match the frame AND its direction of travel, so we don't splice the
            # top of a rollout onto the visually-identical top of a roll-BACK
            d = np.abs(F[i]-F[j]).mean()
            v = np.abs((F[i+1]-F[i]) - (F[j+1]-F[j])).mean()
            s = d + 1.6*v
            if best is None or s < best[0]: best = (s, i, j, d, v)
    s,i,j,d,v = best
    rnd = np.abs(F[np.random.default_rng(0).integers(0,n,400)] -
                 F[np.random.default_rng(1).integers(0,n,400)]).mean()
    return t0+i/FPS, t0+j/FPS, d, v, rnd

if __name__ == "__main__":
    plan = json.load(open("setplan.json"))
    out = []
    for p in plan:
        F = frames(p["a"], p["b"])
        per = cadence(F)
        ci, co, d, v, rnd = best_pair(F, p["a"], p["keep_head"], p["keep_tail"], p["remove"])
        out.append({**p, "period": round(per,2), "cut_in": round(ci,3), "cut_out": round(co,3),
                    "removed": round(co-ci,3), "framedist": round(float(d),2),
                    "veldist": round(float(v),2), "random": round(float(rnd),2)})
        print(f"{p['name']:8s} {p['b']-p['a']:6.2f}s  cadence {per:4.2f}s/rep "
              f"({(p['b']-p['a'])/per:4.1f} reps)   cut {ci:8.2f} -> {co:8.2f}  "
              f"removes {co-ci:6.2f}s   pose distance {d:5.2f} (random pair {rnd:5.2f}), "
              f"motion distance {v:4.2f}")
    json.dump(out, open("setcuts.json","w"), indent=1)
