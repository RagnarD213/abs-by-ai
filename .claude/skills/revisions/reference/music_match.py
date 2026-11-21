#!/usr/bin/env python3
"""Envelope cross-correlation of a candidate music track against windows of a cut."""
import subprocess, sys, numpy as np, os
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SR = 400  # envelope sample rate

def env(path, start=None, dur=None, band=None):
    cmd = [FF, "-v", "error"]
    if start is not None: cmd += ["-ss", str(start)]
    if dur is not None: cmd += ["-t", str(dur)]
    cmd += ["-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    if len(x) == 0: return np.array([])
    n = 16000 // SR
    m = len(x) // n
    e = np.abs(x[:m*n].reshape(m, n)).mean(axis=1)
    e = np.log10(e + 1e-6)
    e -= e.mean()
    return e

def best_corr(a, b, maxlag_s=None):
    """normalised cross-correlation of shorter a against longer b"""
    if len(a) < 10 or len(b) < 10: return 0.0, 0.0
    a = (a - a.mean()) / (a.std() + 1e-9)
    b = (b - b.mean()) / (b.std() + 1e-9)
    if len(a) > len(b): a, b = b, a
    n = len(a)
    # sliding normalised correlation
    c = np.correlate(b, a, mode="valid")
    cs = np.cumsum(np.insert(b, 0, 0))
    cs2 = np.cumsum(np.insert(b*b, 0, 0))
    s = cs[n:] - cs[:-n]
    s2 = cs2[n:] - cs2[:-n]
    var = np.maximum(s2 - s*s/n, 1e-9)
    r = c / np.sqrt(var * n)
    i = int(np.argmax(np.abs(r)))
    return float(r[i]), i / SR

if __name__ == "__main__":
    cut, track = sys.argv[1], sys.argv[2]
    windows = [tuple(float(v) for v in w.split(":")) for w in sys.argv[3:]]
    tr = env(track)
    print(f"track {os.path.basename(track)}  {len(tr)/SR:.1f}s envelope")
    for (st, du) in windows:
        cw = env(cut, st, du)
        r, lag = best_corr(cw, tr)
        print(f"  cut {st:7.1f}-{st+du:7.1f}s  r={r:+.3f}  track offset {lag:7.1f}s")
