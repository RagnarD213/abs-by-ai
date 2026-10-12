"""How well does a lip-synced clip follow its audio? MediaPipe face mesh gives the mouth opening per frame (inner-lip gap over face
height); it is correlated with the speech envelope of the slot's audio at lags of -6..+6 frames, whole clip and per window.
A good sync peaks near lag 0 with r well above the unsynced take. usage: lipmeasure20.py CLIP.mp4 AUDIO.wav [fps=24] [win=2.0]"""
import sys, subprocess, wave, numpy as np, cv2, mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def aperture(clip):
    cap = cv2.VideoCapture(clip); fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.3, min_tracking_confidence=0.3); out = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        r = fm.process(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
        if not r.multi_face_landmarks: out.append(np.nan); continue
        L = r.multi_face_landmarks[0].landmark; p = lambda i: np.array([L[i].x*fr.shape[1], L[i].y*fr.shape[0]])
        out.append(np.linalg.norm(p(13) - p(14))/max(1e-6, np.linalg.norm(p(10) - p(152))))
    a = np.array(out); n = np.isnan(a)
    if n.any() and not n.all(): a[n] = np.interp(np.flatnonzero(n), np.flatnonzero(~n), a[~n])
    return a, int(n.sum())
def envelope(wav, n, fps):
    w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
    hop = sr/fps; e = np.array([np.sqrt(np.mean(x[int(i*hop):int((i+1)*hop)]**2) + 1e-12) for i in range(n)]); return 20*np.log10(e + 1e-6)
def corr(a, e, lag):
    if lag > 0: x, y = a[lag:], e[:-lag]
    elif lag < 0: x, y = a[:lag], e[-lag:]
    else: x, y = a, e
    return float(np.corrcoef(x, y)[0, 1]) if len(x) > 8 and x.std() > 1e-6 and y.std() > 1e-6 else 0.0
def report(clip, wav, fps=24.0, win=2.0, quiet=False):
    a, miss = aperture(clip); e = envelope(wav, len(a), fps); e = np.clip(e, -55, 0)
    best = max(range(-6, 7), key=lambda l: corr(a, e, l)); res = dict(frames=len(a), no_face=miss, r0=round(corr(a, e, 0), 2), best_lag=best, r_best=round(corr(a, e, best), 2), windows=[])
    k = int(win*fps)
    for s in range(0, len(a) - k//2, k//2):
        aa, ee = a[s:s+k], e[s:s+k]; b = max(range(-5, 6), key=lambda l: corr(aa, ee, l)); res["windows"].append((round(s/fps, 1), round(corr(aa, ee, 0), 2), b, round(corr(aa, ee, b), 2)))
    if not quiet:
        print(clip.split("/")[-1], res["frames"], "frames, no face on", miss, "| r at lag 0:", res["r0"], "| best lag", best, "frames, r", res["r_best"])
        print("   window start s: (r at 0, best lag, r best)", " ".join(f"{w[0]}:({w[1]},{w[2]},{w[3]})" for w in res["windows"]))
    return res, a, e
if __name__ == "__main__":
    report(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 24.0, float(sys.argv[4]) if len(sys.argv) > 4 else 2.0)
