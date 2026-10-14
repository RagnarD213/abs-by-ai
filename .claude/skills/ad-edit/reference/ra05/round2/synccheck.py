"""Lip-sync offset: mouth opening (face mesh, every frame) against the voice's level, cross-correlated over +-10 frames.
  synccheck.py VIDEO T0 T1   -> lag in frames (positive = the voice comes AFTER the mouth)"""
import sys, subprocess, numpy as np, mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
v, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); fps = 30000/1001; W, H = 540, 960
raw = subprocess.run([FF, "-v", "error", "-ss", str(t0), "-t", str(t1-t0), "-i", v, "-vf", f"scale={W}:{H},format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
mo = []
for f in fr:
    r = fm.process(np.ascontiguousarray(f))
    if not r.multi_face_landmarks: mo.append(np.nan); continue
    L = r.multi_face_landmarks[0].landmark
    mo.append(abs(L[14].y - L[13].y) / max(1e-6, abs(L[152].y - L[10].y)))
mo = np.array(mo); n = len(mo)
au = np.frombuffer(subprocess.run([FF, "-v", "error", "-ss", str(t0), "-t", str(t1-t0), "-i", v, "-ac", "1", "-ar", "48000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(float)
hop = 48000/fps; n = min(n, int(len(au)/hop)); mo = mo[:n]; en = np.array([np.sqrt(np.mean(au[int(i*hop):int((i+1)*hop)]**2)+1) for i in range(n)]); en = 20*np.log10(en)
ok = ~np.isnan(mo); m = (mo - np.nanmean(mo)); e = en - en.mean()
print("mouth", np.nanmin(mo), np.nanmax(mo), "env", en.min(), en.max(), file=sys.stderr)
best = []
for lag in range(-10, 11):        # voice at frame i+lag vs mouth at frame i
    idx = np.arange(n); j = idx + lag; s = ok & (j >= 0) & (j < n)
    best.append((np.corrcoef(m[s], e[j[s]])[0, 1], lag))
best.sort(reverse=True)
print(f"{v}  {t0}-{t1}s  best lag {best[0][1]:+d} frames (corr {best[0][0]:.3f}); next {best[1][1]:+d} ({best[1][0]:.3f}), {best[2][1]:+d} ({best[2][0]:.3f})  faces {ok.sum()}/{n}")
