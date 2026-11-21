#!/usr/bin/env python3
"""Where is Dan in the frame, second by second?

The camera is a locked wide shot for the whole nine minutes, so a per-pixel MEDIAN over
the programme is a clean plate of the empty patio. Anything that differs from the plate
is Dan -- except the pool, which ripples all day, and the trees, which move in the wind.
Both of those are handled by scoring COLUMNS rather than pixels and taking the single
strongest contiguous run: ripple is low-amplitude and spread across the pool's width,
Dan is high-amplitude and narrow.

Used to place every punch-in crop. A crop centred on the frame instead of on Dan would
put him at the edge of the punched-in shot, or lose him entirely -- he works at the far
left in the intro and at the far right during the sets.
"""
import subprocess, json, sys
import numpy as np
FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
SRC = "/Volumes/Extreme/_edit_work/abwheel/roughcuts/CUT_v2_graded.mp4"
GW, GH = 192, 108           # grid the analysis runs on
FPS = 2                      # 2 samples/s is plenty for a crop that moves slowly

def grab(fps=FPS, ss=None, t=None):
    cmd = [FF, "-v", "error"]
    if ss is not None: cmd += ["-ss", f"{ss}"]
    if t is not None:  cmd += ["-t", f"{t}"]
    cmd += ["-i", SRC, "-vf", f"fps={fps},scale={GW}:{GH},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, GH, GW).astype(np.float32)

def build():
    F = grab()
    plate = np.median(F[::3], axis=0)                  # clean plate of the empty patio
    boxes = []
    for i, f in enumerate(F):
        d = np.abs(f - plate)
        d[d < 16] = 0                                  # ripple and leaf shimmer live here
        col = d.sum(0); row = d.sum(1)
        if col.max() < 200:                            # nobody in frame
            boxes.append(None); continue
        # peak column, then grow outwards while the column still carries 12% of the
        # peak -- a hard 22% run cut his extended arms and legs off during rollouts and
        # left the box sitting to the right of him.
        pk = int(np.argmax(col)); thr = col.max() * 0.12
        x0 = pk
        while x0 > 0 and col[x0-1] > thr: x0 -= 1
        x1 = pk
        while x1 < GW-1 and col[x1+1] > thr: x1 += 1
        # rows are scored ONLY inside those columns, otherwise the roofline and the
        # trees behind him stretch every box to the top of frame
        row = d[:, x0:x1+1].sum(1)
        thr_r = row.max() * 0.16
        ys = np.where(row > thr_r)[0]
        y0, y1 = (int(ys[0]), int(ys[-1])) if len(ys) else (0, GH-1)
        boxes.append([x0/GW, y0/GH, (x1+1)/GW, (y1+1)/GH])
    # fill gaps, then smooth so a crop never jitters
    last = next((b for b in boxes if b), [0.35,0.2,0.65,0.95])
    filled = []
    for b in boxes:
        if b: last = b
        filled.append(last)
    A = np.array(filled)
    k = 9
    pad = np.pad(A, ((k//2, k//2), (0,0)), mode="edge")
    S = np.stack([np.convolve(pad[:, j], np.ones(k)/k, "valid") for j in range(4)], 1)
    return S

def centre_at(S, t):
    i = min(len(S)-1, max(0, int(round(t*FPS))))
    x0,y0,x1,y1 = S[i]
    return (x0+x1)/2, (y0+y1)/2, x1-x0, y1-y0

if __name__ == "__main__":
    S = build()
    np.save("subject.npy", S)
    print(f"{len(S)} samples at {FPS}/s over {len(S)/FPS:.1f}s")
    for t in (8,30,55,80,110,130,160,200,240,265,290,300,340,380,430,450,505,530):
        cx,cy,w,h = centre_at(S,t)
        print(f"  {t//60}:{t%60:02d}  centre ({cx:.2f},{cy:.2f})  size ({w:.2f}x{h:.2f})")
