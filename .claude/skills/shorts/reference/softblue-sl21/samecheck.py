"""Prove a round 2 Short is the approved round 1 Short everywhere except the new clip: per frame, mean abs difference of the
decoded pictures (540x960 luma), and the audio sample for sample.  usage: samecheck.py NEW.mp4 OLD.mp4 CHANGED_T0 CHANGED_T1"""
import subprocess, sys, numpy as np
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
new, old, t0, t1 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]); FPS = 30000 / 1001
def luma(p):
    raw = subprocess.run([FF, "-v", "error", "-i", p, "-vf", "scale=540:960:flags=area,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 960, 540)
def pcm(p):
    return np.frombuffer(subprocess.run([FF, "-v", "error", "-i", p, "-vn", "-ac", "2", "-ar", "48000", "-f", "s16le", "-"], capture_output=True).stdout, "<i2")
A, B = luma(new), luma(old); n = min(len(A), len(B))
d = np.array([np.abs(A[i].astype(np.int16) - B[i].astype(np.int16)).mean() for i in range(n)])
f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS)); out = np.r_[d[:f0], d[f1:]]
bad = [i for i in range(n) if not (f0 <= i < f1) and d[i] > 1.0]
a, b = pcm(new), pcm(old); m = min(len(a), len(b))
print(dict(frames_new=len(A), frames_old=len(B), changed_window=[f0, f1], outside_mean=round(float(out.mean()), 3), outside_max=round(float(out.max()), 3),
           outside_frames_over_1=bad[:12], n_over=len(bad), inside_mean=round(float(d[f0:f1].mean()), 1),
           audio_samples=[len(a), len(b)], audio_max_abs_diff=int(np.abs(a[:m].astype(np.int32) - b[:m].astype(np.int32)).max())))
