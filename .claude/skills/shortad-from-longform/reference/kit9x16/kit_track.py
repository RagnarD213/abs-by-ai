#!/usr/bin/env python3
"""THE FACE TRACK for the 608-px talk crop: facetrack.json = {n: [frame indices], x: [crop x], crop_w}
in the shape `render.py` interpolates. Measured on base.mp4 (the graded 16:9 conform) at 4 fps with
mediapipe's full-range face detector; smoothed PER PICTURE SEGMENT (never across a cut), zero-phase,
endpoint-anchored and slope-limited -- `_shared/cut/landing.py` -- and, per the shared framing rule
(2026-09-16), a segment whose face wanders less than `--fixed-under` source px keeps ONE fixed centre
(its median) instead of a track: the least correction that works.

THE CALMER CAMERA (Dan, 2026-10-01: "the camera movement to keep me centered... has become a little bit too
aggressive... a little bit more tolerance for going out of center... Maybe reduce camera movement by 30%... while still
keeping me as centered as possible"): `--tolerance` px (source) of dead band. The crop lands on him at every cut,
holds until he is more than that off its centre, then follows. Its ceiling is the gate's own centring bound
(`framing:centering`, a hold's median head centre within 6 % of the frame width = 36 source px). `--tolerance 0` is
the old track. The raw detections are cached in facetrack_raw.json (the base is the key).

Measured on RO-10 (8:38, 25 takes; source px, x1.78 on the phone), old track -> tolerance:
  0 (old)  travel 10,758 px   pan p90 62.9 px/s   moving 50 % of the time   off centre 5.9 median / 73 max
  6        7,194 (-33 %)      36.4 (-42 %)        64 % (slower, spread out)  10.3 / 78       his first ask, "30 %"
  20       3,413 (-68 %)      22.8 (-64 %)        31 %                       17.3 / 92       <- THE STANDARD (Dan, 2026-10-03)
The crop is 608 px wide, so at 92 px off centre his whole head is still far inside the frame.
Dan, 2026-10-03, after watching both first minutes: "I like the calmest one, the two-thirds calmer. That looks the best to me... Let's make this our standard way of centering for verticals going forward. I feel like this is better than what we were doing."
20 px of a 608 px crop is 3.3 % of the crop's width: that fraction is the standard for every vertical (_shared/framing-motion.md).

  python3 kit_track.py --build DIR [--fps 4] [--slope 170] [--fixed-under 40] [--tolerance 20] [--out facetrack.json]
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
    ap.add_argument("--tolerance", type=float, default=20.0, help="dead band, source px: the crop holds until he is this far off its centre (0 = the old track)")
    ap.add_argument("--out", default="facetrack.json")
    a = ap.parse_args()
    os.chdir(a.build)
    S = json.load(open("edl_picture.json"))
    st = os.stat("base.mp4"); key = [st.st_size, st.st_mtime_ns, a.fps]
    if os.path.exists("facetrack_raw.json") and json.load(open("facetrack_raw.json"))["key"] == key:
        d = json.load(open("facetrack_raw.json"))
        n, raw = np.array(d["n"]), np.array([np.nan if v is None else v for v in d["x"]])
    else:
        n, raw = faces("base.mp4", a.fps)
        json.dump(dict(key=key, n=[int(v) for v in n], x=[None if np.isnan(v) else round(float(v), 1) for v in raw]), open("facetrack_raw.json", "w"))
    ok = ~np.isnan(raw)
    if ok.sum() < 0.5 * len(raw):
        raise SystemExit(f"face found on only {ok.sum()} of {len(raw)} samples -- not a talking-head base")
    # per picture segment, endpoint-anchored, slope-limited: the shared smoother (_shared/cut/landing.py)
    n_all, x_all, info = landing.track(n, raw, S, slope_px_s=a.slope, k=3, fixed_under=a.fixed_under, tolerance=a.tolerance or None)
    fixed_segs = info["fixed_segments"]
    cx = np.clip(np.array(x_all) - CROP_W / 2, 0, 1920 - CROP_W)
    # how much the camera moves, and how far off centre he gets (measured on the detections, per take)
    na = np.array(n_all); starts = {b[0] for b in landing.seg_bounds(S)}
    inside = np.array([na[i + 1] not in starts for i in range(len(na) - 1)])
    d = np.abs(np.diff(cx))[inside]; dtf = np.maximum(np.diff(na), 1)[inside]
    v = d / dtf * FPS
    ok_ = ~np.isnan(raw); off = []
    for n0, n1 in landing.seg_bounds(S):
        m = (n >= n0) & (n < n1) & ok_; t = (na >= n0) & (na < n1)
        if m.any() and t.any():
            off += list(np.abs(raw[m] - (np.interp(n[m], na[t], cx[t]) + CROP_W / 2)))
    off = np.array(off)
    stats = dict(travel_px=round(float(d.sum())), pan_p90_px_s=round(float(np.percentile(v, 90)), 1), pan_max_px_s=round(float(v.max()), 1),
                 moving_frac=round(float((dtf[v > 5]).sum() / dtf.sum()), 3), off_centre_px=dict(median=round(float(np.median(off)), 1),
                 p95=round(float(np.percentile(off, 95)), 1), max=round(float(off.max()), 1)), fixed_segments=fixed_segs, segments=len(S))
    json.dump(dict(n=[int(v_) for v_ in n_all], x=[round(float(v_), 1) for v_ in cx], crop_w=CROP_W,
                   method=dict(detector="mediapipe FaceDetection model 1", fps=a.fps, slope_px_s=a.slope, tolerance_px=a.tolerance,
                               fixed_under_px=a.fixed_under, fixed_segments=fixed_segs, segments=len(S)), stats=stats),
              open(a.out, "w"))
    print(f"{len(n_all)} samples over {len(S)} picture segments ({fixed_segs} fixed-centre); face x {np.nanmin(raw):.0f}..{np.nanmax(raw):.0f}; "
          f"crop travel {stats['travel_px']} px, pan p90 {stats['pan_p90_px_s']} max {stats['pan_max_px_s']} px/s source, moving {100 * stats['moving_frac']:.0f} % of the time; "
          f"he sits {stats['off_centre_px']['median']} px off centre (median), {stats['off_centre_px']['max']} max")


if __name__ == "__main__":
    sys.exit(main())
