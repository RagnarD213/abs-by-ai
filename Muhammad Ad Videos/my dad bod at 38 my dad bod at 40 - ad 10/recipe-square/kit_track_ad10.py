#!/usr/bin/env python3
"""9:16 head track using the shared land-then-hold vertical standard.
20 px dead band, 40 px fixed range, 170 px/s cap for a 608 px crop.
Measure cut-start frames explicitly; never interpolate a renderer across picture cuts.
Run in a new build directory, never an approved video's directory.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

HERE = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shortad-from-longform/reference/kit9x16'   # build-local copy (Ad 10 square): the kit folder, for the shared imports
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "_shared", "cut"))
import landing  # noqa: E402  the 0 px landing smoother, shared
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FPS = 30000 / 1001
CROP_W = 608
W, H = 640, 360


def faces(video, sample_fps, segments, video_fps):
    """Measure regular samples AND actual cut-start frames in the source."""
    import cv2
    import mediapipe as mp
    cap = cv2.VideoCapture(video)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    wanted = set(np.rint(np.arange(0, count / video_fps, 1 / sample_fps) * video_fps).astype(int))
    wanted.update(n0 for n0, _ in landing.seg_bounds(segments, video_fps))
    det = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    idx, xs = [], []
    for frame in sorted(v for v in wanted if v < count):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ok, image = cap.read()
        if not ok:
            raise RuntimeError(f"Cannot read measured frame {frame}")
        result = det.process(cv2.cvtColor(cv2.resize(image, (W, H)), cv2.COLOR_BGR2RGB))
        value = np.nan
        if result.detections:
            box = max(result.detections, key=lambda d: d.score[0]).location_data.relative_bounding_box
            value = (box.xmin + box.width / 2) * image.shape[1]
        idx.append(frame); xs.append(value)
    cap.release(); det.close()
    return np.array(idx), np.array(xs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--fps", type=float, default=4.0)
    ap.add_argument("--crop-width", type=float, default=608.0)
    ap.add_argument("--video-fps", type=float, default=FPS)
    ap.add_argument("--slope", type=float, default=None, help="source px/s (~300 on the phone), the re-audit's cap")
    ap.add_argument("--fixed-under", type=float, default=None, help="a segment whose face x range is under this keeps one fixed centre")
    ap.add_argument("--tolerance", type=float, default=None, help="dead band, source px: the crop holds until he is this far off its centre (0 = the old track)")
    ap.add_argument("--out", default="facetrack.json")
    a = ap.parse_args()
    os.chdir(a.build)
    global CROP_W
    CROP_W = a.crop_width
    a.slope = 170 * CROP_W / 608 if a.slope is None else a.slope
    a.fixed_under = 40 * CROP_W / 608 if a.fixed_under is None else a.fixed_under
    a.tolerance = 20 * CROP_W / 608 if a.tolerance is None else a.tolerance
    S = json.load(open("framing_segments.json" if os.path.exists("framing_segments.json") else "edl_picture.json"))
    # Measure all layout entries/returns and punch boundaries too. The renderer uses these as landing anchors.
    boundaries = set()
    if os.path.exists("beats.json"):
        data = json.load(open("beats.json"))
        for beat in data.get("beats", []):
            if beat.get("kind") in ("window", "stmt", "winmedia", "bleed", "card", "hf", "title", "photo"):
                boundaries.update(round(beat[key] * a.video_fps) for key in ("t0", "t1"))
    if os.path.exists("beats.py"):
        import importlib.util
        spec = importlib.util.spec_from_file_location("vertical_build_beats", "beats.py")
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        timeline, _ = module.timeline()
        boundaries.update(round(b["t0"] * a.video_fps) for b in timeline)
        boundaries.update(round(b["t1"] * a.video_fps) for b in timeline)
        # AD 10 SQUARE BUILD-LOCAL CHANGE (as Ad 6 round 2): zoom times are NOT landing anchors. Re-landing at all four times
        # of every push gave each gradual zoom a one-frame sideways jump at its start and end, and put an instant step's
        # anchor one frame BEFORE its cut at some cuts (camcheck on the first square render: 16 steps of 11 to 57 px).
    split = []
    for start, end in landing.seg_bounds(S, a.video_fps):
        cuts = [start] + sorted(b for b in boundaries if start < b < end) + [end]
        split.extend(dict(n0=x, n1=y) for x, y in zip(cuts[:-1], cuts[1:]))
    S = split
    st = os.stat("base.mp4"); key = [st.st_size, st.st_mtime_ns, a.fps, a.video_fps, S, "cut-frame-head-v1"]
    if os.path.exists("facetrack_raw.json") and json.load(open("facetrack_raw.json"))["key"] == key:
        d = json.load(open("facetrack_raw.json"))
        n, raw = np.array(d["n"]), np.array([np.nan if v is None else v for v in d["x"]])
    else:
        n, raw = faces("base.mp4", a.fps, S, a.video_fps)
        json.dump(dict(key=key, n=[int(v) for v in n], x=[None if np.isnan(v) else round(float(v), 1) for v in raw]), open("facetrack_raw.json", "w"))
    ok = ~np.isnan(raw)
    if ok.sum() < 0.5 * len(raw):
        raise SystemExit(f"face found on only {ok.sum()} of {len(raw)} samples -- not a talking-head base")
    # per picture segment, endpoint-anchored, slope-limited: the shared smoother (_shared/cut/landing.py)
    for start, _ in landing.seg_bounds(S, a.video_fps):
        if start not in n or not np.isfinite(raw[np.where(n == start)[0][0]]):
            raise SystemExit(f"Missing measured head at picture cut {start}")
    n_all, x_all, info = landing.track(n, raw, S, slope_px_s=a.slope, k=3, fixed_under=a.fixed_under, tolerance=a.tolerance or None, fps=a.video_fps)
    info["crop_width"] = CROP_W
    info["policy"] = "vertical-land-then-hold-20261003"
    fixed_segs = info["fixed_segments"]
    if any(abs(x_all[i] - raw[np.where(n == start)[0][0]]) > 1e-6
           for start, _ in landing.seg_bounds(S, a.video_fps)
           for i in np.where(n_all == start)[0]):
        raise SystemExit("Cut landing is not centred")
    cx = np.asarray(x_all) - CROP_W / 2
    if np.any((cx < 0) | (cx > 1920 - CROP_W)):
        raise SystemExit("Centred crop exceeds source width: choose a wider window")
    # how much the camera moves, and how far off centre he gets (measured on the detections, per take)
    na = np.array(n_all); starts = {b[0] for b in landing.seg_bounds(S, a.video_fps)}
    inside = np.array([na[i + 1] not in starts for i in range(len(na) - 1)])
    d = np.abs(np.diff(cx))[inside]; dtf = np.maximum(np.diff(na), 1)[inside]
    v = d / dtf * a.video_fps
    ok_ = ~np.isnan(raw); off = []
    for n0, n1 in landing.seg_bounds(S, a.video_fps):
        m = (n >= n0) & (n < n1) & ok_; t = (na >= n0) & (na < n1)
        if m.any() and t.any():
            off += list(np.abs(raw[m] - (np.interp(n[m], na[t], cx[t]) + CROP_W / 2)))
    off = np.array(off)
    stats = dict(travel_px=round(float(d.sum())), pan_p90_px_s=round(float(np.percentile(v, 90)), 1), pan_max_px_s=round(float(v.max()), 1),
                 moving_frac=round(float((dtf[v > 5 * CROP_W / 608]).sum() / dtf.sum()), 3), off_centre_px=dict(median=round(float(np.median(off)), 1),
                 p95=round(float(np.percentile(off, 95)), 1), max=round(float(off.max()), 1)), fixed_segments=fixed_segs, segments=len(S))
    json.dump(dict(n=[int(v_) for v_ in n_all], x=[round(float(v_), 1) for v_ in cx], crop_w=CROP_W,
                   segments=S, method=dict(policy="vertical-land-then-hold-20261003", detector="mediapipe FaceDetection model 1", fps=a.fps, slope_px_s=a.slope, tolerance_px=a.tolerance,
                               fixed_under_px=a.fixed_under, fixed_segments=fixed_segs, segments=len(S)), stats=stats),
              open(a.out, "w"))
    print(f"{len(n_all)} samples over {len(S)} picture segments ({fixed_segs} fixed-centre); face x {np.nanmin(raw):.0f}..{np.nanmax(raw):.0f}; "
          f"crop travel {stats['travel_px']} px, pan p90 {stats['pan_p90_px_s']} max {stats['pan_max_px_s']} px/s source, moving {100 * stats['moving_frac']:.0f} % of the time; "
          f"he sits {stats['off_centre_px']['median']} px off centre (median), {stats['off_centre_px']['max']} max")


if __name__ == "__main__":
    sys.exit(main())
