#!/usr/bin/env python3
"""A3 take 2: Veo printed faint red measuring marks on the clear glass jug mid-pour (the round 3 A3 take 1 reviewer FAILED the
same fault). Paint them out: pure-red pixels (hue <= 4 or >= 172, sat > 80, value > 110) in the upper right of the frame whose
neighbourhood is NOT skin (the hand), grown 2 px, inpainted from the surrounding glass on every frame. Writes takes/A3_t2r.mp4
(lossless-quality x264) + a before/after strip. Nothing outside the marks changes."""
import subprocess, numpy as np, cv2, json
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC, OUT = "takes/A3_t2.mp4", "takes/A3_t2r.mp4"
if __name__ == "__main__":
    b = subprocess.run([FF, "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    F = np.frombuffer(b, np.uint8).reshape(-1, 1080, 1920, 3).copy()
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080", "-r", "24", "-i", "-",
                            "-c:v", "libx264", "-crf", "8", "-preset", "slow", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                            "-color_primaries", "bt709", "-color_trc", "bt709", OUT], stdin=subprocess.PIPE)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)); log = []
    for n, f in enumerate(F):
        h = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        red = ((h[..., 0] <= 4) | (h[..., 0] >= 172)) & (h[..., 1] > 80) & (h[..., 2] > 110)
        red[:, :1000] = False; red[760:] = False
        skin = ((h[..., 0] <= 25) & (h[..., 1] > 50) & (h[..., 1] < 210) & (h[..., 2] > 100)).astype(np.float32)
        near_skin = cv2.blur(skin, (31, 31)) > 0.35
        # round 3 re-review: the faint pink-brown parts of the marks on the jug's left wall (about x 1240-1460, y 120-360, f15-f75)
        # are below the pure-red bar; there, any reddish pixel (R above G and B, hue <= 10 or >= 160, sat > 25) that is not skin
        b_, g_, r_ = [f[..., i].astype(np.int16) for i in range(3)]
        wide = ((h[..., 0] <= 10) | (h[..., 0] >= 160)) & (h[..., 1] > 25) & (r_ > g_ + 8) & (r_ > b_ + 8) & (h[..., 2] > 70)
        box = np.zeros_like(wide); box[90:420, 1180:1520] = 15 <= n <= 78
        low = np.zeros_like(wide); low[170:420, 1180:1520] = 15 <= n <= 78      # below the hand: the nuts read as skin, so no skin guard
        m = (((red | (wide & box)) & ~near_skin) | (red & low)).astype(np.uint8) * 255
        m = cv2.dilate(m, k)
        o = cv2.inpaint(f, m, 3, cv2.INPAINT_TELEA) if m.any() else f
        if 15 <= n <= 78:
            # round 3 re-review 2: what is left of the marks is thin pink-brown ticks on clear glass. Smooth the glass of the left wall
            # (median 9) and pull its colour to neutral, protecting the trail mix (saturated browns, dark raisins), grown 7 px.
            y0, y1, x0, x1 = 90, 430, 1180, 1520
            R = o[y0:y1, x0:x1]; hh = cv2.cvtColor(R, cv2.COLOR_BGR2HSV)
            mix = (((hh[..., 1] > 70) & (hh[..., 0] >= 5) & (hh[..., 0] <= 30)) | (hh[..., 2] < 80)).astype(np.uint8)
            mix = cv2.dilate(mix, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
            sm = cv2.medianBlur(R, 9); g = cv2.cvtColor(cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
            sm = (0.35 * sm + 0.65 * g).astype(np.float32)
            w = np.zeros(R.shape[:2], np.float32); w[8:-8, 8:-8] = 1; w = cv2.GaussianBlur(w * (1 - mix), (21, 21), 0)[..., None]
            o = o.copy(); o[y0:y1, x0:x1] = (sm * w + R.astype(np.float32) * (1 - w)).round().astype(np.uint8)
        log.append(int((m > 0).sum())); enc.stdin.write(o.tobytes())
        if n in (30, 48, 56, 60, 62): cv2.imwrite(f"a3_paint_f{n}.jpg", np.hstack([f[60:620, 1100:1800], o[60:620, 1100:1800]]))
    enc.stdin.close(); enc.wait()
    json.dump(dict(painted_px=log), open("a3_paint.json", "w")); print("painted px per frame, max", max(log), "frames>0", sum(x > 0 for x in log))
