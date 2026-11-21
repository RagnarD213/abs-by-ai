#!/usr/bin/env python3
"""Every talk-to-talk picture cut, scored by the ONLY thing that decides whether it reads as a jump:
the difference between the two RAW SOURCE frames the cut joins.

A cut at his frame n joins raw[n-1+offA] to raw[n+offB]. That is computable exactly from the roll, with no
render -- so every candidate position in a +-15 frame window can be scored before committing a 25-minute render.
Muhammad's own technique (memory: muhammad-trial-edit-analysis) is to place the picture cut 1-15 frames off the
audio splice on a POSE-MATCHED frame; this finds that frame.

Prints, per cut: the offset step, the jump as built, the best jump in the window, and his own frame-diff there
(a big one means he covered the cut with a flash or a graphic, so ours can hide in it too).
"""
import json, subprocess, sys
import numpy as np

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
W, H = 240, 135
WIN = 15


def read_gray(path, n0, n1, w=W, h=H):
    n = n1 - n0
    p = subprocess.run([FF, "-v", "error", "-ss", f"{n0/FPS:.6f}", "-i", path, "-frames:v", str(n),
                        "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    if len(a) < n*w*h: n = len(a)//(w*h)
    return a[:n*w*h].reshape(n, h, w).astype(np.float32), n0


class Roll:
    """random access to the raw roll, by frame index, with a small cache of decoded windows"""
    def __init__(self, path): self.path = path; self.win = {}
    def get(self, k):
        base = (k // 64) * 64
        if base not in self.win:
            if len(self.win) > 24: self.win.clear()
            a, _ = read_gray(self.path, base, base + 64)
            self.win[base] = a
        a = self.win[base]
        i = k - base
        return a[i] if 0 <= i < len(a) else None


def main():
    E = json.load(open('edl_picture.json'))
    roll = Roll('raw.mp4')
    his, h0 = None, None
    # his own frame diff, whole file, at 240x135
    hz, _ = read_gray('ref/ad3_v6hd.mp4', 0, 7948)
    hd = np.abs(np.diff(hz, axis=0)).mean(axis=(1, 2))     # hd[i] = diff between his frame i and i+1
    del hz
    segs = {s['n0']: s for s in E}
    order = sorted(segs)
    print(f"{'cut n':>6} {'step':>5} {'built':>7} {'best n':>7} {'best':>7} {'gain':>6} {'hisdiff':>8}  note")
    rows = []
    for i in range(1, len(order)):
        a, b = segs[order[i-1]], segs[order[i]]
        if a['n1'] != b['n0']:
            continue                                        # a gap = a media beat sits between them, not a talk cut
        n = b['n0']
        offA, offB = round(a['off']*FPS), round(b['off']*FPS)
        step = offB - offA
        def jump(m):
            f1, f2 = roll.get(m-1+offA), roll.get(m+offB)
            if f1 is None or f2 is None: return None
            return float(np.abs(f1-f2).mean())
        built = jump(n)
        lo = max(a['n0']+4, n-WIN); hi = min(b['n1']-4, n+WIN)
        cand = [(jump(m), m) for m in range(lo, hi+1)]
        cand = [(v, m) for v, m in cand if v is not None]
        best, bn = min(cand) if cand else (None, n)
        hisd = float(hd[n-1]) if 0 < n < len(hd)+1 else float('nan')
        note = ''
        if built is not None:
            if abs(step) <= 3: note = 'MERGE (step<=3fr, <=100ms sync cost)'
            elif best < built - 1.5: note = f'MOVE {n}->{bn}'
        rows.append((n, step, built, bn, best, hisd, note))
        print(f"{n:6d} {step:5d} {built:7.2f} {bn:7d} {best:7.2f} {built-best:6.2f} {hisd:8.1f}  {note}")
    json.dump([{'n': r[0], 'step': r[1], 'built': r[2], 'best_n': r[3], 'best': r[4], 'his': r[5]} for r in rows],
              open('picjoin.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
