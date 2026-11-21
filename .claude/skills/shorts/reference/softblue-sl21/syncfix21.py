"""SL-21 round 2: keep the lip-synced pixels only on the lower face (mouth, jaw, cheeks) and the untouched take everywhere else
(RO-06 syncfix / RO-20C beardfix idea). Per frame: MediaPipe face mesh on the synced frame -> hull of the lower face oval
(below the eye line), grown and feathered -> sync over take. Frames with no face found reuse the last mask.
usage: syncfix21.py TAKE_TRIM.mp4 SYNC.mp4 OUT.mp4 [--grow 14] [--feather 10]
Prints: frames, frames with a face, mean abs difference outside the mask between OUT and the take (must be ~0), and the mean
difference inside the mask between sync and take (how much the sync changed the mouth)."""
import subprocess, sys, json, numpy as np, cv2
import mediapipe as mp
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
a = sys.argv[1:]; take, sync, out = a[:3]
grow = int(a[a.index("--grow") + 1]) if "--grow" in a else 14
feather = int(a[a.index("--feather") + 1]) if "--feather" in a else 10
W, H = 1080, 1920
FPSV = float(a[a.index("--fps") + 1]) if "--fps" in a else 24.0
WAV = a[a.index("--wav") + 1] if "--wav" in a else None      # gate by the voice: the synced mouth only while he speaks, the take's own closed mouth in the silences (LatentSync holds the mouth open through silence)


def frames(p):
    raw = subprocess.run([FF, "-v", "error", "-i", p, "-vf", f"scale={W}:{H}:flags=bicubic:in_color_matrix=bt709:out_color_matrix=bt709,format=rgb24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


T, S = frames(take), frames(sync); n = min(len(T), len(S))
gate = np.ones(n, np.float32)
if WAV:
    import wave
    w_ = wave.open(WAV); sr = w_.getframerate(); x = np.frombuffer(w_.readframes(w_.getnframes()), "<i2").astype(np.float32).reshape(-1, w_.getnchannels()).mean(1) / 32768
    env = np.array([np.sqrt(np.mean(x[int(i / FPSV * sr):int((i + 1) / FPSV * sr)] ** 2) + 1e-12) for i in range(n)])
    v = (env > 0.18 * np.percentile(env, 98)).astype(np.float32)
    v = np.array([v[max(0, i - 1):i + 3].max() for i in range(n)])          # open 2 frames before the sound, stay 1 after; only pauses of 3 frames or less stay bridged
    gate = np.convolve(np.pad(v, 1, mode="edge"), np.ones(3) / 3, mode="valid").astype(np.float32)      # a 3-frame ramp in and out
    if "--on-to" in a:      # explicit window: the synced mouth from just before his first word to just after his last, short pauses inside stay synced (a gate that flickers across a 0.3 s pause smears the mouth: SL-21 R, 3.5 to 3.7 s)
        f0_ = max(0, int(round((float(a[a.index("--on-from") + 1]) - 0.08) * FPSV))); f1_ = min(n, int(round((float(a[a.index("--on-to") + 1]) + 0.08) * FPSV)))
        v = np.zeros(n, np.float32); v[f0_:f1_] = 1
        gate = np.convolve(np.pad(v, 1, mode="edge"), np.ones(3) / 3, mode="valid").astype(np.float32)
    elif "--on-from" in a: gate[:max(0, int(round((float(a[a.index("--on-from") + 1]) - 0.08) * FPSV)) - 1)] = 0.0      # nothing before his first word (the lead-in carries Dan's own "like,")
    print("gate", "".join("#" if g > 0.66 else "+" if g > 0.1 else "." for g in gate))
OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234,
        127, 162, 21, 54, 103, 67, 109]
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{FPSV:g}", "-i", "-",
                        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an", out], stdin=subprocess.PIPE)
found = 0; last = None; d_out = []; d_in = []
with mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.4) as FM:
    for i in range(n):
        r = FM.process(S[i])
        if r.multi_face_landmarks:
            lm = r.multi_face_landmarks[0].landmark; P = np.array([[lm[k].x * W, lm[k].y * H] for k in OVAL], np.float32)
            eye_y = (lm[33].y + lm[263].y) / 2 * H; nose_y = lm[1].y * H; cut = eye_y + 0.45 * (nose_y - eye_y)      # keep from just under the eyes down
            m = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(m, cv2.convexHull(P).astype(np.int32), 255)
            # the cut follows the head's tilt: a line through the two eye corners, shifted down
            ex0, ey0, ex1, ey1 = lm[33].x * W, lm[33].y * H, lm[263].x * W, lm[263].y * H
            yy, xx = np.mgrid[0:H, 0:W]; line = ey0 + (ey1 - ey0) * (xx - ex0) / max(1e-3, ex1 - ex0) + (cut - eye_y)
            m[yy < line] = 0
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * grow + 1, 2 * grow + 1)); m = cv2.dilate(m, k)
            last = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), feather); found += 1
        if last is None:
            o = T[i]
        else:
            w = last[..., None] * gate[i]; o = (S[i].astype(np.float32) * w + T[i].astype(np.float32) * (1 - w) + 0.5).astype(np.uint8)
            d_out.append(float(np.abs(o.astype(np.int16) - T[i].astype(np.int16))[last < 0.004].mean()))
            d_in.append(float(np.abs(S[i].astype(np.int16) - T[i].astype(np.int16))[last > 0.9].mean()))
        enc.stdin.write(o.tobytes())
enc.stdin.close(); enc.wait()
print(json.dumps(dict(gate_on=round(float((gate > 0.5).mean()), 2), out=out, frames=n, face_found=found, mean_abs_outside=round(float(np.mean(d_out)), 3) if d_out else None,
                      mean_abs_inside_sync_vs_take=round(float(np.mean(d_in)), 2) if d_in else None)))
