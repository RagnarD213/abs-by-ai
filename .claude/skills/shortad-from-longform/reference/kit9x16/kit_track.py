#!/usr/bin/env python3
"""THE FACE TRACK for the 608-px talk crop: facetrack.json = {n: [frame indices], x: [crop x], crop_w}
in the shape `render.py` interpolates. Measured on base.mp4 (the graded 16:9 conform) at 4 fps with
mediapipe's full-range face detector; smoothed PER PICTURE SEGMENT (never across a cut), zero-phase,
endpoint-anchored and slope-limited -- `_shared/cut/landing.py` -- and, per the shared framing rule
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
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "_shared", "cut"))
import landing  # noqa: E402  the 0 px landing smoother, shared
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
    # per picture segment, endpoint-anchored, slope-limited: the shared smoother (_shared/cut/landing.py)
    n_all, x_all, info = landing.track(n, raw, S, slope_px_s=a.slope, k=3, fixed_under=a.fixed_under)
    fixed_segs = info["fixed_segments"]
    cx = np.clip(np.array(x_all) - CROP_W / 2, 0, 1920 - CROP_W)
    json.dump(dict(n=[int(v) for v in n_all], x=[round(float(v), 1) for v in cx], crop_w=CROP_W,
                   method=dict(detector="mediapipe FaceDetection model 1", fps=a.fps, slope_px_s=a.slope,
                               fixed_under_px=a.fixed_under, fixed_segments=fixed_segs, segments=len(S))),
              open("facetrack.json", "w"))
    v = np.abs(np.diff(cx)) / np.maximum(np.diff(np.array(n_all)), 1) * FPS
    print(f"{len(n_all)} samples over {len(S)} picture segments ({fixed_segs} fixed-centre); face x {np.nanmin(raw):.0f}..{np.nanmax(raw):.0f}; "
          f"pan inside segments p90 {np.percentile(v, 90):.0f} max {v.max():.0f} px/s source")


if __name__ == "__main__":
    sys.exit(main())
