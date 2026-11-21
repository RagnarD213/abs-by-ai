#!/usr/bin/env python3
"""SL-06 R7: the edit's slow push-in, sub-pixel smooth (cv2.warpAffine, cubic), about a focus point, on a clip or a still;
optional B light-dim: the left lamp's pool (over the pen) fades to about 30 % with a soft falloff while the vial's pool
stays, as a real light dimming would (no hard edge, ambient kept). Optional overlay (C's step badges, RGBA ProRes) before
the push so it zooms with the scene.
  python3 push.py S SRC(.mp4|.jpg) OUT.mp4 --frames N --push 0.07 --focus x,y [--dim] [--overlay badges.mov]"""
import argparse, subprocess
import cv2, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
ap = argparse.ArgumentParser(); ap.add_argument("S"); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--frames", type=int, required=True); ap.add_argument("--push", type=float, default=0.07)
ap.add_argument("--focus", required=True); ap.add_argument("--dim", action="store_true"); ap.add_argument("--overlay")
a = ap.parse_args(); n = a.frames; cx, cy = map(float, a.focus.split(","))
if a.src.lower().endswith((".jpg", ".png")):
    still = cv2.resize(cv2.imread(a.src), (1080, 1920), interpolation=cv2.INTER_AREA); frames = (still for _ in range(n))
else:
    cap = cv2.VideoCapture(a.src)
    def gen():
        for _ in range(n):
            ok, f = cap.read()
            if not ok: break
            yield cv2.resize(f, (1080, 1920), interpolation=cv2.INTER_AREA)
    frames = gen()
ov = None
if a.overlay:
    raw = subprocess.run([FF.replace("/ffmpeg", "/ffmpeg.real"), "-v", "error", "-i", a.overlay, "-pix_fmt", "bgra", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    ov = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 4)
if a.dim:
    yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
    w = np.exp(-(((xx - 400) / 420) ** 2 + ((yy - 700) / 820) ** 2))        # the left lamp's pool, wall down to the pen
    w *= 1 / (1 + np.exp((xx - 640) / 45))                                    # fades out before the vial's pool
    lift = 0.07 * np.exp(-(((xx - 790) / 220) ** 2 + ((yy - 980) / 300) ** 2))   # the vial's light a touch warmer/brighter
def ease(t): return 0.5 - 0.5 * np.cos(np.pi * t)
p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "24", "-i", "-",
                      "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p",
                      "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", a.out], stdin=subprocess.PIPE)
for k, f in enumerate(frames):
    img = f.astype(np.float32)
    if a.dim:
        d = ease(np.clip((k - 10) / 30, 0, 1))                               # dims over 1.25 s from 0.4 s
        img *= (1 - 0.7 * d * w)[..., None]; img *= (1 + d * lift)[..., None]
    if ov is not None and k * 30000 / 1001 / 24 < len(ov):
        o = ov[min(len(ov) - 1, int(round(k / 24 * 30000 / 1001)))].astype(np.float32); al = o[..., 3:4] / 255
        img = img * (1 - al) + o[..., :3] * al
    z = 1 + a.push * (k / max(n - 1, 1))
    M = np.float32([[z, 0, cx - z * cx], [0, z, cy - z * cy]])
    out = cv2.warpAffine(np.clip(img, 0, 255).astype(np.uint8), M, (1080, 1920), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    p.stdin.write(out.tobytes())
p.stdin.close(); p.wait(); print("push", a.S, a.out, n)
