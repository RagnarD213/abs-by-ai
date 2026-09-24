#!/usr/bin/env python3
"""THE 0 px LANDING: the crop-track smoother, shared by every skill that tracks Dan inside a crop.

The defect it fixes (independent audit, Ad 2 vertical, 2026-09-03): a per-segment median with a FULL window
at the segment ends is a median over the future only, so after every cut the crop sat where Dan WOULD be half a
second later. He landed 78-190 px off centre after each cut and the crop panned him back over up to 1 s.

The fix (facetrack3.py, then facetrack4.py and kit_track.py, now here as the only copy):
  * smooth PER PICTURE SEGMENT, never across a cut;
  * the median window SHRINKS to zero at the segment ends (k_eff = min(k, j, L-1-j)), so the first and last
    samples are the raw anchor itself;
  * a forward and a backward slope-limited pass, blended with a weight that trusts the forward pass at the
    segment start and the backward pass at the end, so out[0] == raw[0] and out[-1] == raw[-1] exactly and the
    middle is the zero-phase average;
  * optionally, a segment whose track wanders less than `fixed_under` px keeps ONE fixed centre (the least
    correction that works, the shared framing rule of 2026-09-16).
Measured result: landing error 0 px at every cut, exit error 0, the crop following at <= the slope cap.

  import landing
  x = landing.smooth_segment(n, raw_x, slope_px_s=170)               # one segment's samples
  n_all, x_all, info = landing.track(n, raw_x, segments, slope_px_s=170, fixed_under=40)
  landing.errors(n_all, raw_at(n_all), x_all, segments)              # -> landing / exit error, px
  python3 landing.py selftest

`n` is frame indices (any frame rate); `segments` are picture segments with n0/n1 frame indices
(edl_picture.json from piccuts.py), or cut_in/cut_out seconds.
"""
import json
import sys

import numpy as np

FPS = 30000 / 1001


def limit_fwd(x, t, lim_px_s, fps=FPS):
    """Slope-limited forward pass over samples at frame indices t: moves at most lim_px_s * dt per sample."""
    o = [float(x[0])]
    for i in range(1, len(x)):
        dt = (t[i] - t[i - 1]) / fps
        o.append(o[-1] + float(np.clip(x[i] - o[-1], -lim_px_s * dt, lim_px_s * dt)))
    return np.array(o)


def smooth_segment(n, x, slope_px_s, k=3, fixed_under=None, fps=FPS):
    """One picture segment's track: endpoint-anchored, zero-phase, slope-limited. Returns the smoothed x."""
    n = np.asarray(n, float)
    x = np.asarray(x, float)
    L = len(x)
    if fixed_under is not None and (L < 4 or x.max() - x.min() < fixed_under):
        return np.full(L, float(np.median(x)))
    if L < 4:
        return x.copy()
    med = np.array([np.median(x[j - min(k, j, L - 1 - j):j + min(k, j, L - 1 - j) + 1]) for j in range(L)])
    f = limit_fwd(med, n, slope_px_s, fps)
    b = limit_fwd(med[::-1], (-n)[::-1], slope_px_s, fps)[::-1]
    w = (n - n[0]) / max(1.0, n[-1] - n[0])
    return (1 - w) * f + w * b


def seg_bounds(segments, fps=FPS):
    out = []
    for s in segments:
        if "n0" in s and "n1" in s:
            out.append((int(s["n0"]), int(s["n1"])))
        else:
            out.append((round(s["cut_in"] * fps), round(s["cut_out"] * fps)))
    return out


def track(n, raw, segments, slope_px_s=170.0, k=3, fixed_under=None, fps=FPS):
    """The whole track: per picture segment, with a sample forced onto every segment's first and last frame
    (a renderer interpolating between samples must never interpolate across a cut). raw may hold NaN (no
    detection); it is interpolated first. Returns (frame indices, x, info)."""
    n = np.asarray(n, int)
    raw = np.asarray(raw, float)
    ok = ~np.isnan(raw)
    r = np.interp(n, n[ok], raw[ok])
    n_all, x_all, fixed = [], [], 0
    for n0, n1 in seg_bounds(segments, fps):
        m = (n >= n0) & (n < n1)
        seg_n = list(n[m])
        seg_x = list(r[m])
        # The forced first/last samples take the NEAREST sample of THIS take, never an interpolation across the
        # cut: kit_track.py and facetrack4.py interpolated toward the next take's position (up to 6/7.5 of the
        # jump at 4 fps), so the crop began sliding toward where he will be after the cut before it happened.
        src_n, src_x = (n[m], r[m]) if m.any() else (n, r)
        if not seg_n or seg_n[0] != n0:
            seg_n.insert(0, n0)
            seg_x.insert(0, float(np.interp(n0, src_n, src_x)))
        if seg_n[-1] != n1 - 1 and n1 - 1 > n0:
            seg_n.append(n1 - 1)
            seg_x.append(float(np.interp(n1 - 1, src_n, src_x)))
        seg_x = np.array(seg_x, float)
        out = smooth_segment(seg_n, seg_x, slope_px_s, k, fixed_under, fps)
        if fixed_under is not None and np.ptp(out) == 0 and len(out) > 1:
            fixed += 1
        n_all += [int(v) for v in seg_n]
        x_all += [float(v) for v in out]
    return np.array(n_all), np.array(x_all), dict(segments=len(segments), fixed_segments=fixed, slope_px_s=slope_px_s)


def errors(n, raw, x, segments, fps=FPS):
    """|raw - track| at the first frame after every cut (landing) and the last frame before it (exit), px."""
    n = np.asarray(n)
    raw = np.asarray(raw, float)
    x = np.asarray(x, float)
    land, ex = [], []
    for n0, _ in seg_bounds(segments, fps)[1:]:
        i0 = np.where(n == n0)[0]
        i1 = np.where(n == n0 - 1)[0]
        if len(i0) and not np.isnan(raw[i0[0]]):
            land.append(abs(raw[i0[0]] - x[i0[0]]))
        if len(i1) and not np.isnan(raw[i1[0]]):
            ex.append(abs(raw[i1[0]] - x[i1[0]]))
    st = lambda v: dict(median=round(float(np.median(v)), 1), max=round(float(np.max(v)), 1)) if v else None
    return dict(landing=st(land), exit=st(ex), cuts=len(land))


def selftest():
    """A talking head that steps 150 px at every cut and drifts inside each take: the track must land ON him
    (0 px) at every cut, exit on him, and never exceed the slope cap inside a segment."""
    rng = np.random.default_rng(3)
    segs, n, raw, t = [], [], [], 0
    for j in range(8):
        L = int(rng.integers(40, 160))
        base = 900 + (150 if j % 2 else -150)
        segs.append(dict(n0=t, n1=t + L))
        for q in range(0, L, 7):
            n.append(t + q)
            raw.append(base + 0.4 * q + rng.normal(0, 3))
        t += L
    n, raw = np.array(n), np.array(raw)
    na, xa, _ = track(n, raw, segs, slope_px_s=170)
    ra = np.concatenate([np.interp(na[(na >= s["n0"]) & (na < s["n1"])], n[(n >= s["n0"]) & (n < s["n1"])],
                                   raw[(n >= s["n0"]) & (n < s["n1"])]) for s in segs])   # truth, per take
    e = errors(na, ra, xa, segs)
    v = [abs(xa[i + 1] - xa[i]) / max(1, na[i + 1] - na[i]) * FPS for i in range(len(na) - 1)
         if not any(na[i + 1] == s["n0"] for s in segs)]
    ok = e["landing"]["max"] == 0 and e["exit"]["max"] == 0 and max(v) <= 170 + 1e-6
    print(json.dumps(dict(errors=e, max_pan_px_s=round(max(v), 1), verdict="PASS" if ok else "FAIL")))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        sys.exit(selftest())
    print(__doc__)
