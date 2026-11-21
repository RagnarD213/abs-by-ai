#!/usr/bin/env python3
"""SL-06 R5: repair a Veo intro take whose camera is locked. Veo redraws small text (a backwards R on the calendar, scribbled
vial labels); the approved START frame has it right. Per frame: (1) STATIC boxes are copied from START wherever no person covers
them (person mask from MediaPipe, grown), gain-matched to the take on the box's ring; (2) each VIAL label is found by template
matching the START vial (cap + label) near its last position and START's label is pasted there, gain matched, feathered.
Optional frame range and a slight speed-up (VIDEO-RULES 2026-10-08) to land exactly on the slot length.
  fix_take.py TAKE START OUT --frames 0:71 --seconds 3.28 --static x0,y0,x1,y1 ... --vial x0,y0,x1,y1:lx0,ly0,lx1,ly1 ..."""
import argparse, subprocess, json, cv2, numpy as np, mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
ap = argparse.ArgumentParser(); ap.add_argument("take"); ap.add_argument("start"); ap.add_argument("out")
ap.add_argument("--frames", default=None); ap.add_argument("--seconds", type=float, required=True)
ap.add_argument("--static", action="append", default=[]); ap.add_argument("--vial", action="append", default=[])
ap.add_argument("--fps", type=float, default=24.0); ap.add_argument("--log", default=None)
a = ap.parse_args()
W, H = 1080, 1920
raw = subprocess.run([FF, "-v", "error", "-i", a.take, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
f0, f1 = (map(int, a.frames.split(":")) if a.frames else (0, len(fr) - 1))
src = fr[f0:f1 + 1]; n_out = round(a.seconds * a.fps)
idx = np.minimum(np.round(np.arange(n_out) * (len(src) - 1) / max(n_out - 1, 1)).astype(int), len(src) - 1) if len(src) < n_out or True else None
speed = (len(src) - 1) / max(n_out - 1, 1)
S = cv2.imread(a.start); assert S.shape == (H, W, 3)
box = lambda s: tuple(map(int, s.split(",")))
statics = [box(s) for s in a.static]
vials = [(box(v.split(":")[0]), box(v.split(":")[1])) for v in a.vial]
seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
def gain(fa, sa, ring):
    m_f = fa[ring].reshape(-1, 3).mean(0); m_s = sa[ring].reshape(-1, 3).mean(0)
    return np.clip(m_f / np.maximum(m_s, 1), 0.85, 1.15)
pos = [vb[:2] for vb, _ in vials]; log = []
p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", a.out], stdin=subprocess.PIPE)
for k, i in enumerate(idx):
    F = src[i].astype(np.float32).copy()
    person = seg.process(cv2.cvtColor(src[i], cv2.COLOR_BGR2RGB)).segmentation_mask > 0.3
    person = cv2.dilate(person.astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
    for x0, y0, x1, y1 in statics:
        ring = np.zeros((H, W), bool); ring[max(0, y0 - 12):y1 + 12, max(0, x0 - 12):x1 + 12] = True; ring[y0:y1, x0:x1] = False; ring &= ~person
        g = gain(F, S.astype(np.float32), ring) if ring.sum() > 200 else np.ones(3)
        m = np.zeros((H, W), np.float32); m[y0:y1, x0:x1] = 1; m[person] = 0; m = cv2.GaussianBlur(m, (0, 0), 3)[..., None]
        F = F * (1 - m) + S.astype(np.float32) * g * m
    for j, ((vx0, vy0, vx1, vy1), (lx0, ly0, lx1, ly1)) in enumerate(vials):
        tpl = S[vy0:vy1, vx0:vx1]; px, py = pos[j]; R = 40
        sx0, sy0 = max(0, px - R), max(0, py - R); win = src[i][sy0:py + (vy1 - vy0) + R, sx0:px + (vx1 - vx0) + R]
        r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, sc, _, mx = cv2.minMaxLoc(r)
        nx, ny = sx0 + mx[0], sy0 + mx[1]; pos[j] = (nx, ny); dx, dy = nx - vx0, ny - vy0
        lab = S[ly0:ly1, lx0:lx1].astype(np.float32); X0, Y0 = lx0 + dx, ly0 + dy; hh, ww = lab.shape[:2]
        ring = np.zeros((H, W), bool); ring[Y0 - 3:Y0 + hh + 3, X0 - 3:X0 + ww + 3] = True; ring[Y0:Y0 + hh, X0:X0 + ww] = False
        g = np.clip(F[ring].reshape(-1, 3).mean(0) / np.maximum(S.astype(np.float32)[ly0 - 3:ly1 + 3, lx0 - 3:lx1 + 3].reshape(-1, 3).mean(0), 1), 0.8, 1.25)
        m = np.zeros((hh, ww), np.float32); m[2:-2, 2:-2] = 1; m = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None]
        F[Y0:Y0 + hh, X0:X0 + ww] = F[Y0:Y0 + hh, X0:X0 + ww] * (1 - m) + lab * m
        log.append(dict(k=k, vial=j, score=round(float(sc), 3), dx=int(dx), dy=int(dy)))
    p.stdin.write(np.clip(F + 0.5, 0, 255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
if a.log: json.dump(dict(take=a.take, frames=[f0, f1], speed=round(speed, 4), n_out=n_out, statics=statics, vials=vials, track=log), open(a.log, "w"))
print("ok", a.out, "speed", round(speed, 3), "frames", n_out, "min vial score", min([l["score"] for l in log], default=None))
