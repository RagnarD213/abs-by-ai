#!/usr/bin/env python3
"""SL-06 R5: hold one smile. Veo opens and closes the lips as if talking under the voiceover (reviewer FAIL on every take).
From frame FROM on, the mouth patch of frame SRC (a clean held smile) is pasted onto each frame, aligned by template-matching
an ANCHOR box (nose and lower glasses) of frame SRC, with a soft elliptical edge. Frames before FROM are untouched.
  mouth_hold.py IN OUT --src 35 --from 40 --mouth x0,y0,x1,y1 --anchor x0,y0,x1,y1 [--log log.json]"""
import argparse, json, subprocess, cv2, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out"); ap.add_argument("--src", type=int, required=True)
ap.add_argument("--from", dest="frm", type=int, required=True); ap.add_argument("--mouth", required=True); ap.add_argument("--anchor", required=True)
ap.add_argument("--fps", type=float, default=24.0); ap.add_argument("--log"); ap.add_argument("--anchor2", default=None); ap.add_argument("--skinclip", action="store_true")
a = ap.parse_args(); W, H = 1080, 1920
fr = np.frombuffer(subprocess.run([FF, "-v", "error", "-i", a.inp, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout, np.uint8).reshape(-1, H, W, 3)
mx0, my0, mx1, my1 = map(int, a.mouth.split(",")); ax0, ay0, ax1, ay1 = map(int, a.anchor.split(","))
S = fr[a.src]; tpl = S[ay0:ay1, ax0:ax1]; patch = S[my0:my1, mx0:mx1].astype(np.float32); h, w = patch.shape[:2]
m = np.zeros((h, w), np.float32); cv2.ellipse(m, (w // 2, h // 2), (w // 2 - 6, h // 2 - 6), 0, 0, 360, 1, -1); m = cv2.GaussianBlur(m, (0, 0), 5)[..., None]
p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-", "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                      "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", a.out], stdin=subprocess.PIPE)
log = []
for i, f in enumerate(fr):
    F = f.astype(np.float32)
    if i >= a.frm:
        R = 30; win = f[ay0 - R:ay1 + R, ax0 - R:ax1 + R]; r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, sc, _, mxl = cv2.minMaxLoc(r)
        dx, dy = mxl[0] - R, mxl[1] - R
        if a.anchor2:                                  # r5 C: average with a chin track so the mouth does not slide against the jaw during a head turn
            bx0, by0, bx1, by1 = map(int, a.anchor2.split(",")); t2 = S[by0:by1, bx0:bx1]; w2 = f[by0 - R:by1 + R, bx0 - R:bx1 + R]
            r2 = cv2.matchTemplate(w2, t2, cv2.TM_CCOEFF_NORMED); _, s2, _, m2 = cv2.minMaxLoc(r2); dx, dy = round((dx + m2[0] - R) / 2), round((dy + m2[1] - R) / 2); sc = min(sc, s2)
        X, Y = mx0 + dx, my0 + dy
        g = np.clip(F[Y:Y + h, X:X + w].reshape(-1, 3).mean(0) / np.maximum(patch.reshape(-1, 3).mean(0), 1), 0.9, 1.1)
        mm = m
        if a.skinclip:                                 # r5 C: never paint past the face: clip to the current frame's face silhouette (skin, holes filled so the mouth stays in)
            P = 40; Y0_, X0_ = max(0, Y - P), max(0, X - P); reg = f[Y0_:Y + h + P, X0_:X + w + P].astype(np.int32)
            sk = ((reg[..., 2] - reg[..., 1] > 10) & (reg[..., 1] > reg[..., 0]) & (reg[..., 2] > 60)).astype(np.uint8)
            sk = cv2.morphologyEx(sk, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)); cs, _ = cv2.findContours(sk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hull = np.zeros_like(sk)
            if cs: cv2.drawContours(hull, [max(cs, key=cv2.contourArea)], -1, 1, -1)
            hull = cv2.GaussianBlur(cv2.erode(hull, np.ones((7, 7), np.uint8)).astype(np.float32), (0, 0), 2)
            mm = m * hull[Y - Y0_:Y - Y0_ + h, X - X0_:X - X0_ + w][..., None]
        F[Y:Y + h, X:X + w] = F[Y:Y + h, X:X + w] * (1 - mm) + patch * g * mm; log.append(dict(i=i, dx=int(dx), dy=int(dy), score=round(float(sc), 3)))
    p.stdin.write(np.clip(F + 0.5, 0, 255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
if a.log: json.dump(dict(inp=a.inp, src=a.src, frm=a.frm, mouth=a.mouth, anchor=a.anchor, track=log), open(a.log, "w"))
print("ok", a.out, "min anchor score", min([l["score"] for l in log], default=None), "max shift", max([abs(l["dx"]) + abs(l["dy"]) for l in log], default=0))
