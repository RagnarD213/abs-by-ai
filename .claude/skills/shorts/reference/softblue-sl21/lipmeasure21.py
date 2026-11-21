"""How well a clip's mouth follows the voice: per frame, the inner-lip gap (face mesh, over mouth width) against the voice's
loudness envelope at that time. Prints r (correlation), the share of voiced frames with the mouth open (gap > 0.06) and the
share of silent frames with it open.  usage: lipmeasure21.py CLIP.mp4 CLIP.wav"""
import subprocess, sys, json, wave, numpy as np
import mediapipe as mp
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
clip, wav = sys.argv[1], sys.argv[2]; FPSV = float(sys.argv[3]) if len(sys.argv) > 3 else 24.0
raw = subprocess.run([FF, "-v", "error", "-i", clip, "-vf", "scale=540:960:in_color_matrix=bt709,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 960, 540, 3)
w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32).reshape(-1, w.getnchannels()).mean(1) / 32768
gap = []
with mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.3) as FM:
    for f in F:
        r = FM.process(np.ascontiguousarray(f))
        if not r.multi_face_landmarks: gap.append(np.nan); continue
        lm = r.multi_face_landmarks[0].landmark
        gap.append(abs(lm[14].y - lm[13].y) * 960 / max(1.0, abs(lm[291].x - lm[61].x) * 540))
gap = np.array(gap); n = len(gap)
env = np.array([np.sqrt(np.mean(x[int(i / FPSV * sr):int((i + 1) / FPSV * sr)] ** 2) + 1e-12) for i in range(n)])
ok = ~np.isnan(gap); voiced = env > 0.25 * np.percentile(env, 95)
r = float(np.corrcoef(gap[ok], env[ok])[0, 1])
lags = {k: round(float(np.corrcoef(gap[ok][max(0, k):len(gap[ok]) + min(0, k)], env[ok][max(0, -k):len(env[ok]) - max(0, k)])[0, 1]), 2) for k in range(-4, 5)}
print(json.dumps(dict(lag_r=lags, clip=clip, frames=n, face=int(ok.sum()), r=round(r, 2), open_when_voiced=round(float((gap[ok & voiced] > 0.06).mean()), 2),
                      open_when_silent=round(float((gap[ok & ~voiced] > 0.06).mean()), 2) if (ok & ~voiced).any() else None, voiced_frames=int(voiced.sum()))))
