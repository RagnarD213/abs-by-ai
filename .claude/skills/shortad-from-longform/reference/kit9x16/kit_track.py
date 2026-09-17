#!/usr/bin/env python3
"""THE FACE TRACK for the 608-px talk crop: facetrack.json = {n: [frame indices], x: [crop x], crop_w}
in the shape `render.py` interpolates. Measured on base.mp4 (the graded 16:9 conform) at 4 fps with
mediapipe's full-range face detector; smoothed PER PICTURE SEGMENT (never across a cut), zero-phase,
endpoint-anchored and slope-limited -- facetrack4.py's method -- and, per the shared framing rule
(2026-09-16), a segment whose face wanders less than `--fixed-under` source px keeps ONE fixed centre
(its median) instead of a track: the least correction that works.

  python3 kit_track.py --build DIR [--fps 4] [--slope 170] [--fixed-under 40]
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FPS = 30000 / 1001
CROP_W = 608
W, H = 640, 360


def faces(video, fps):
    """(frame index, face centre x in 1920 space) per sample, NaN where no face."""
    import mediapipe as mp
    raw = subprocess.run([FF, "-v", "error", "-i", video, "-vf", f"fps={fps},scale={W}:{H}", "-an",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    fr = np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)
    det = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    xs = np.full(n, np.nan)
    for i in range(n):
        r = det.process(fr[i])
        if r.detections:
            b = max(r.detections, key=lambda d: d.score[0]).location_data.relative_bounding_box
            xs[i] = (b.xmin + b.width / 2) * 1920
    idx = np.array([int(round(i * FPS / fps)) for i in range(n)])
    return idx, xs


def limit_fwd(x, t, lim):
    o = [x[0]]
    for i in range(1, len(x)):
        dt = (t[i] - t[i - 1]) / FPS
        o.append(o[-1] + float(np.clip(x[i] - o[-1], -lim * dt, lim * dt)))
    return np.array(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--fps", type=float, default=4.0)
    ap.add_argument("--slope", type=float, default=170.0, help="source px/s (~300 on the phone), the re-audit's cap")
    ap.add_argument("--fixed-under", type=float, default=40.0, help="a segment whose face x range is under this keeps one fixed centre")
    a = ap.parse_args()
    os.chdir(a.build)
    S = json.load(open("edl_picture.json"))
    n, raw = faces("base.mp4", a.fps)
    ok = ~np.isnan(raw)
    if ok.sum() < 0.5 * len(raw):
        raise SystemExit(f"face found on only {ok.sum()} of {len(raw)} samples -- not a talking-head base")
    r = np.interp(n, n[ok], raw[ok])
    # every picture segment gets a sample on its first and last frame (render.py: "a cut never interpolates across itself")
    n_all, x_all, fixed_segs = [], [], 0
    for s in S:
        m = (n >= s["n0"]) & (n < s["n1"])
        idx = np.where(m)[0]
        seg_n = list(n[idx]); seg_x = list(r[idx])
        if not seg_n or seg_n[0] != s["n0"]:
            seg_n.insert(0, s["n0"]); seg_x.insert(0, float(np.interp(s["n0"], n, r)))
        if seg_n[-1] != s["n1"] - 1:
            seg_n.append(s["n1"] - 1); seg_x.append(float(np.interp(s["n1"] - 1, n, r)))
        seg_n = np.array(seg_n); seg_x = np.array(seg_x, float)
        L = len(seg_x)
        if seg_x.max() - seg_x.min() < a.fixed_under or L < 4:
            out = np.full(L, float(np.median(seg_x)))       # one fixed centre for the shot
            fixed_segs += 1
        else:
            k = 3
            med = np.array([np.median(seg_x[j - min(k, j, L - 1 - j):j + min(k, j, L - 1 - j) + 1]) for j in range(L)])
            f = limit_fwd(med, seg_n, a.slope)
            b = limit_fwd(med[::-1], (-seg_n)[::-1], a.slope)[::-1]
            w = (seg_n - seg_n[0]) / max(1, seg_n[-1] - seg_n[0])
            out = (1 - w) * f + w * b
        n_all += [int(v) for v in seg_n]
        x_all += [float(v) for v in out]
    cx = np.clip(np.array(x_all) - CROP_W / 2, 0, 1920 - CROP_W)
    json.dump(dict(n=n_all, x=[round(float(v), 1) for v in cx], crop_w=CROP_W,
                   method=dict(detector="mediapipe FaceDetection model 1", fps=a.fps, slope_px_s=a.slope,
                               fixed_under_px=a.fixed_under, fixed_segments=fixed_segs, segments=len(S))),
              open("facetrack.json", "w"))
    v = np.abs(np.diff(cx)) / np.maximum(np.diff(np.array(n_all)), 1) * FPS
    print(f"{len(n_all)} samples over {len(S)} picture segments ({fixed_segs} fixed-centre); face x {np.nanmin(raw):.0f}..{np.nanmax(raw):.0f}; "
          f"pan inside segments p90 {np.percentile(v, 90):.0f} max {v.max():.0f} px/s source")


if __name__ == "__main__":
    sys.exit(main())
