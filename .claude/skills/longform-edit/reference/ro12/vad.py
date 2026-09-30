#!/usr/bin/env python3
"""Energy map of the C1706 lav: speech islands and silences, used to place cuts in measured silence.
import vad; vad.silences(a, b) -> [(s0, s1), ...] gaps >= min_gap inside [a, b]; vad.quiet_point(t0, t1) -> quietest 10 ms in window."""
import numpy as np, wave, os, sys
LAV = "/Volumes/Extreme/_edit_work/ro12/audio/lav.wav"
CACHE = "/Volumes/Extreme/_edit_work/ro12/audio/rms10ms.npy"
HOP = 0.01
def _load():
    if os.path.exists(CACHE): return np.load(CACHE)
    import subprocess
    FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
    b = subprocess.run([FF, "-v", "error", "-i", LAV, "-f", "f32le", "-ac", "1", "-ar", "48000", "-"], capture_output=True).stdout
    x = np.frombuffer(b, np.float32); n = len(x)//480
    r = 20*np.log10(np.sqrt((x[:n*480].reshape(n, 480)**2).mean(1)) + 1e-9)
    np.save(CACHE, r); return r
R = _load()
THR = -52.0   # dBFS: roll floor -68, speech -20..-35; breaths sit around -50..-58
def silences(a, b, min_gap=0.18, thr=THR):
    i0, i1 = int(a/HOP), int(b/HOP); q = R[i0:i1] < thr; out = []; s = None
    for k, v in enumerate(q):
        if v and s is None: s = k
        if (not v or k == len(q)-1) and s is not None:
            e = k if not v else k+1
            if (e - s)*HOP >= min_gap: out.append((round(a + s*HOP, 2), round(a + e*HOP, 2)))
            s = None
    return out
def islands(a, b, min_gap=0.18):
    sl = silences(a, b, min_gap); out = []; t = a
    for s0, s1 in sl:
        if s0 > t: out.append((round(t, 2), s0))
        t = s1
    if t < b: out.append((round(t, 2), round(b, 2)))
    return out
def quiet_point(t0, t1):
    i0, i1 = int(t0/HOP), max(int(t0/HOP)+1, int(t1/HOP)); k = int(np.argmin(R[i0:i1])); return round((i0 + k)*HOP + HOP/2, 3)
if __name__ == "__main__":
    a, b = float(sys.argv[1]), float(sys.argv[2])
    for s0, s1 in islands(a, b): print(f"speech {s0:8.2f}-{s1:8.2f}  ({s1-s0:.2f})")
