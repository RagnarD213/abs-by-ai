#!/usr/bin/env python3
"""Framing rows -- Dan's hair-anchored standard, measured on the DELIVERED picture of ANY set.

THE STANDARD (LOCKED 2026-09-08, memory `framing-standard-hair-anchored`; do not renegotiate it).
Dan, approving website rev 4: "The framing and the cropping are all looking good. You nailed it
with this one. Let's lock that in and crop all the videos like this going forward."
  * every talking-head crop is anchored to the MEASURED TOP OF THE HAIR -- never the frame edge,
    never a skin/hairline detector;
  * per hold, the crop puts that hold's tallest hair instant ~4 % of the crop height below the top
    edge (~43 px at 1080p): hair >= 20 px from the edge on every frame, the per-hold minimum in
    30-70 px, the median over the video <= 75 px;
  * two levels only, NEAR (hair -> belly button) and FAR (hair -> shorts line). No wide level;
  * centred on his head band; a push schedule, never one fixed crop for a whole talk.

WHY THIS FILE REPLACES website-video/reference/recipe/hairdet.py + hairgate.py. That detector
climbed from the skin through the hair band until it reached the luma of the DOOR PANEL behind Dan
in the 8/28 kitchen (hairtrack.json `hdr_col`, hair ~20-30 vs panel 36-37). It could not run on a
pool shoot, a gym, or an editor's master, so the standard was enforced on one set in one skill --
while /shortad-from-longform re-cropped Dan into vertical for every ad with no framing rule at all.
Framing is 4 of Dan's 11 recorded rejections.

ONE TRACKER, FIVE ROWS. Every row here is arithmetic on one per-sample signal
        (t, head_top_y, head_height, head_centre_x, valid)      in DELIVERED pixels
measured at TRACK_FPS with NO set-specific reference:
  1 mediapipe FaceMesh (legacy solutions API: bundled model, CPU, no download) anchors the face --
    centre x from the cheek edges, face height forehead (10) -> chin (152), and a head band
    +-0.4 face widths wide. A face FaceMesh's short-range finder misses (a wide shot) is located
    by the full-range FaceDetection model and meshed on a crop -- see _facefinder. ⚠ It reads any
    face, so a legacy/full-frame build keeps only samples on the MAIN SCENE (palette distance <=
    the coverage threshold, the same definition style:coverage uses). Evidence-contract v2 builds
    instead crop to each renderer-declared talking-head window, then prove a face and silhouette
    exist inside those declared pixels.
  2 Apple Vision person segmentation (shorts/reference/recentre/personmask, .accurate) on a head
    crop gives the silhouette; the hair top is the first row of the head band that is >= 20 %
    person. Measured 2026-09-12 on the corpus frames: crop and full-frame tops agree within 2 px.
  3 THE INDEPENDENT TEST KEPT FROM hairgate.py (its test B): the top TOP_ROWS rows of the head
    band must not be head. It ran against the door panel's luma; here it runs on a SECOND, unrelated
    segmenter (mediapipe selfie segmentation on the same crop, a different model with different
    failure modes). Rev 3 passed its own gate at 21-95 px of "headroom" because gate and plan used
    one detector; a hair top read by one model is only trusted where the other does not see head
    against the edge. Both are recorded on every sample, and the row fails on EITHER.

VALIDITY, so a wrong detection can never read as "fine":
  * a sample with no face, or no silhouette in the head band, is INVALID and reported;
  * a sample whose hair band (forehead landmark - hair top) is outside CLIMB x face height is
    INVALID -- the silhouette started on something that was not his head. Measured 2026-09-12 on
    the corpus frames: 0.23-0.36 of the face height (rev 2, rev 4 x2, the outdoor ad 1 cutdown,
    the off-centre Short);
  * EXCEPT when the silhouette touches the edge (top <= EDGE_PX): that is the defect itself,
    whatever the climb reads. A cut-off head shortens the climb; discarding it would hide rev 3;
  * a track with fewer than MIN_VALID_FRAC of its on-scene samples valid FAILS every row that
    needs it. Nobody looked is not it is fine.

Bounds live in formats.py in 1080p pixels; headroom is normalized to a 1080-high talking-head
window so full-screen, stacked and side-by-side composites use the same physical standard.
"""
import os
import subprocess
import tempfile

import numpy as np

from .. import common as C
from .. import contract as CONTRACT
from ..common import Row, unmeasured

TRACK_FPS = 4                 # hairgate.py sampled the delivered frames at 4 fps; kept
BAND_HALF = 0.40              # head band = centre +- 0.40 face widths (hairdet BAND=80 of a ~200 px face)
TOP_ROWS = 12                 # hairgate.py TOP_ROWS, unchanged (12 rows at 1080p; scaled by H)
CLIMB = (0.10, 0.60)          # hair band as a fraction of face height; measured 0.23-0.36
EDGE_PX = 2                   # a silhouette starting this close to the top edge IS at the edge
MASK_THR, BAND_FRAC = 0.5, 0.20
MIN_VALID_FRAC = 0.60         # hairgate.py: ">= 60 % of samples valid", unchanged
SCENE_D = 0.12                # picture.coverage's off-scene threshold, same number, same histogram
SCENE_GUARD = 0.5             # s either side of a sample that must also be on-scene (dissolves)
PERSIST = 2                   # consecutive samples (0.5 s at 4 fps) a hair-at-the-edge reading must
                              # hold before it is a defect: one sample is a blend or a blink of the
                              # segmenter, a hold is >= 1 s. Rev 3 reads 661 consecutive.

TALK_MO_SD = 0.012            # a hold is TALK when the mouth opening (inner lips / face height)
                              # varies by at least this much over the hold. A photo card with his
                              # face on it holds still by construction (only detector jitter);
                              # a mute b-roll shot of Dan walking mostly does. Measured 2026-09-12:
                              # every talking hold in the corpus reads sd 0.019-0.054 (rev 4,
                              # Muhammad Ad 2, the Ad 1 vertical, v2-short3, rev 1). ⚠ Mute b-roll
                              # of Dan TALKING (ad1-vertical-attempt1 used some) reads as talk.

PERSONMASK = os.path.join(C.REPO, ".claude/skills/shorts/reference/recentre/personmask")


class Track:
    """The per-sample framing signal of one delivered file. Built once, shared by every row."""

    def __init__(self, samples, H, W, fps, on_scene_n, why=None):
        self.samples, self.H, self.W, self.fps = samples, H, W, fps
        self.on_scene_n, self.why = on_scene_n, why

    @property
    def k(self):
        return self.H / 1080.0

    def valid(self):
        return [s for s in self.samples if s["valid"]]

    def valid_frac(self):
        return len(self.valid()) / max(1, self.on_scene_n)


def _facemesh():
    import mediapipe as mp
    return mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                           refine_landmarks=False, min_detection_confidence=0.5)


def _facefinder():
    """The full-range detector (model_selection=1, faces out to ~5 m). FaceMesh's own short-range
    finder misses a face that is small in the frame -- measured 2026-09-12 on website rev 1's
    banned WIDE shot (a 150 px face in 1080p): FaceMesh alone found nothing on 107 of 112 on-scene
    samples, which would have made the one row that must FAIL that file read NOT MEASURED instead.
    A wide shot is exactly where the face is small, so the wide-shot row needs the long-range finder."""
    import mediapipe as mp
    return mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)


def _find_face(fm, fd, fr, W, H):
    """FaceMesh on the full frame; if it finds nothing, the full-range detector locates the face
    and FaceMesh runs on a crop around it. Returns landmark (x, y) in frame pixels for the four
    points the tracker uses, or None."""
    r = fm.process(fr)
    if r.multi_face_landmarks:
        L = r.multi_face_landmarks[0].landmark
        return {i: (L[i].x * W, L[i].y * H) for i in (10, 152, 234, 454, 13, 14)}
    d = fd.process(fr)
    if not d.detections:
        return None
    b = d.detections[0].location_data.relative_bounding_box
    cx, cy = (b.xmin + b.width / 2) * W, (b.ymin + b.height / 2) * H
    s = max(b.width * W, b.height * H) * 2.2
    x0, y0 = int(max(0, cx - s / 2)), int(max(0, cy - s / 2))
    x1, y1 = int(min(W, cx + s / 2)), int(min(H, cy + s / 2))
    if x1 - x0 < 16 or y1 - y0 < 16:
        return None
    crop = np.ascontiguousarray(fr[y0:y1, x0:x1])
    r = fm.process(crop)
    if not r.multi_face_landmarks:
        return None
    L = r.multi_face_landmarks[0].landmark
    cw, ch = x1 - x0, y1 - y0
    return {i: (L[i].x * cw + x0, L[i].y * ch + y0) for i in (10, 152, 234, 454, 13, 14)}


def _selfieseg():
    import mediapipe as mp
    return mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)


def _band_top(mask, b0, b1):
    fr = (mask[:, b0:b1] > MASK_THR).mean(1)
    idx = np.where(fr >= BAND_FRAC)[0]
    return int(idx[0]) if len(idx) else None


def build_track(pic, plan):
    """Decode at TRACK_FPS, native size; face -> head crop -> two silhouettes -> one sample each."""
    if not os.path.exists(PERSONMASK):
        return Track([], 0, 0, TRACK_FPS, 0,
                     why=f"Apple Vision segmenter not built: {PERSONMASK} (swiftc -O -o personmask "
                         f"personmask.swift in shorts/reference/recentre)")
    pr = C.probe(pic.v)
    W, H = pr["width"], pr["height"]
    windows = plan.get("talking_head_windows")
    if windows is not None:
        err = CONTRACT.contract_error(plan, "framing")
        if err:
            return Track([], H, W, TRACK_FPS, 0, why=err)
    _, pal_d = pic.palette()                       # 2 fps palette distance from the programme median
    declared = []
    for key in ("ai_inserts", "real_photos", "graphics"):
        for g in (plan.get(key) or []):
            declared.append(tuple(g["beat"]))
    for ab in (plan.get("cards") or []):
        declared.append(tuple(ab))

    def on_scene(t):
        """On the main scene, AND not inside a dissolve into or out of something else: every
        palette sample within +-SCENE_GUARD s must be on-scene too. Measured on website rev 4
        (2026-09-12): a 0.5 s cross-dissolve into an AI insert blends a second person's head over
        Dan's, and the mid-dissolve frame read a hair top of 6 px on an approved file."""
        if windows is not None:
            # A composite can have no stable full-frame palette at all. The renderer's window
            # schedule names exactly where Dan is; the face and two silhouette models still prove
            # the declared pixels contain him.
            return any(float(x["beat"][0]) <= t < float(x["beat"][1]) for x in windows)
        if any(a - 0.3 <= t <= b + 0.3 for a, b in declared):
            return False
        if not len(pal_d):
            return True
        i0 = max(0, int((t - SCENE_GUARD) * 2))
        i1 = min(len(pal_d), int((t + SCENE_GUARD) * 2) + 1)
        return bool((pal_d[i0:i1] <= SCENE_D).all())

    fm, fd, seg = _facemesh(), _facefinder(), _selfieseg()
    tmp = tempfile.mkdtemp(prefix="framing_")
    from PIL import Image
    p = subprocess.Popen([C.FF, "-v", "error", "-i", pic.v, "-vf", f"fps={TRACK_FPS}", "-an",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE,
                         bufsize=W * H * 3 * 2)
    samples, crops, k, n_scene = [], [], 0, 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = k / TRACK_FPS
        k += 1
        if not on_scene(t):
            continue
        n_scene += 1
        full = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        win = CONTRACT.rect_at(windows, t, W, H)
        if win is None:
            samples.append(dict(t=round(t, 3), valid=False, why="invalid talking-head window"))
            continue
        ox, oy, w, h, wi = win
        fr = np.ascontiguousarray(full[oy:oy + h, ox:ox + w])
        top_rows = max(4, int(round(TOP_ROWS * h / 1080.0)))
        P = _find_face(fm, fd, fr, w, h)
        s = dict(t=round(t, 3), valid=False, top=None, top_m=None, edge_m=None, hh=None, cx=None,
                 fh=None, fw=None, why=None, ox=ox, oy=oy, win_w=w, win_h=h,
                 motion=wi.get("motion", "tracking"), window=wi.get("name", "window"))
        if P is None:
            s["why"] = "no face"
            samples.append(s)
            continue
        cx = (P[234][0] + P[454][0]) / 2
        fw = abs(P[454][0] - P[234][0])
        fore, chin = P[10][1], P[152][1]
        fh = chin - fore
        if fh < 0.04 * h or fw < 0.02 * w:
            s["why"] = f"face too small ({fh:.0f} px)"
            samples.append(s)
            continue
        cw = min(w, int(2.2 * fh))
        x0 = int(max(0, min(w - cw, cx - cw / 2)))
        y1 = int(min(h, chin + 0.25 * fh))
        crop = np.ascontiguousarray(fr[0:y1, x0:x0 + cw])
        b0, b1 = int(max(0, cx - BAND_HALF * fw - x0)), int(min(cw, cx + BAND_HALF * fw - x0))
        # the independent segmenter, now
        m = seg.process(crop).segmentation_mask
        s["top_m"] = _band_top(m, b0, b1)
        s["edge_m"] = round(float((m[:top_rows, b0:b1] > MASK_THR).mean()), 3)
        s.update(cx=round(float(cx), 1), fw=round(float(fw), 1), fh=round(float(fh), 1),
                 chin=round(float(chin), 1), fore=round(float(fore), 1), x0=x0, b0=b0, b1=b1,
                 mo=round(float(abs(P[14][1] - P[13][1]) / fh), 4))
        path = os.path.join(tmp, f"{len(samples):06d}.png")
        Image.fromarray(crop).save(path, compress_level=1)
        crops.append((len(samples), path))
        samples.append(s)
    p.stdout.close()
    p.wait()
    fm.close()
    fd.close()
    seg.close()

    # Apple Vision on every head crop, in batches
    mdir = os.path.join(tmp, "m")
    for i in range(0, len(crops), 200):
        subprocess.run([PERSONMASK, mdir] + [pth for _, pth in crops[i:i + 200]],
                       capture_output=True, text=True)
    for idx, pth in crops:
        s = samples[idx]
        mp_ = os.path.join(mdir, os.path.basename(pth)[:-4] + ".mask.png")
        if not os.path.exists(mp_):
            s["why"] = "vision returned no mask"
            continue
        m = np.asarray(Image.open(mp_).convert("L"), dtype=np.float32) / 255.0
        top = _band_top(m, s["b0"], s["b1"])
        s["edge_v"] = round(float((m[:top_rows, s["b0"]:s["b1"]] > MASK_THR).mean()), 3)
        if top is None:
            s["why"] = "no silhouette in the head band"
            continue
        climb = (s["fore"] - top) / s["fh"]
        s["top"], s["climb"] = top, round(float(climb), 3)
        s["hh"] = round(float(s["chin"] - top), 1)
        s["top1080"] = round(float(top * 1080.0 / s["win_h"]), 2)
        s["hh_frac"] = round(float(s["hh"] / s["win_h"]), 5)
        s["cx_off_frac"] = round(float((s["cx"] - s["win_w"] / 2) / s["win_w"]), 5)
        if top > EDGE_PX and not (CLIMB[0] <= climb <= CLIMB[1]):
            s["why"] = f"hair band {climb:.2f} of face height, outside {CLIMB}"
            continue
        s["valid"] = True
        try:
            os.unlink(mp_)
            os.unlink(pth)
        except OSError:
            pass
    try:
        os.rmdir(mdir)
        os.rmdir(tmp)
    except OSError:
        pass
    return Track(samples, H, W, TRACK_FPS, n_scene)


def track_of(pic, plan):
    """Cached on the Picture: five rows, one track."""
    if getattr(pic, "_framing", None) is None:
        pic._framing = build_track(pic, plan)
    return pic._framing


def holds(pic, tr):
    """Contiguous runs of valid samples between picture-change events, >= 1 s long."""
    ev = pic.change_events()
    out, cur = [], []
    for s in tr.samples:
        if not s["valid"]:
            if cur:
                out.append(cur)
                cur = []
            continue
        if cur and any(cur[-1]["t"] < e <= s["t"] for e in ev):
            out.append(cur)
            cur = []
        cur.append(s)
    if cur:
        out.append(cur)
    return [h for h in out if h[-1]["t"] - h[0]["t"] >= 1.0 - 1.0 / TRACK_FPS]


def talk_holds(pic, tr):
    """The holds where Dan is TALKING to camera: the mouth moves. Framing levels are a rule about
    the talking head; a mute outdoor b-roll shot or a still photo card with his face in it is
    framed by other rules (shortad-from-longform rule 12) and would otherwise read as a "wide
    level" (ad1-vertical-attempt1's and the approved Ad 1 vertical's cards both read 22 % of H)."""
    out = []
    for h in holds(pic, tr):
        mo = [s["mo"] for s in h if s.get("mo") is not None]
        if len(mo) >= 3 and float(np.std(mo)) >= TALK_MO_SD:
            out.append(h)
    return out


def _robust_min(vals):
    """The tightest reading that PERSISTS: the minimum over adjacent pairs of the pair's maximum,
    so one blink of the segmenter is not a hold's number (a hold is >= 1 s = 4 samples)."""
    v = list(vals)
    if len(v) < 2:
        return min(v)
    return min(max(v[i], v[i + 1]) for i in range(len(v) - 1))


def _need(key, tr, min_valid=MIN_VALID_FRAC):
    if tr.why:
        return unmeasured(key, tr.why)
    if tr.on_scene_n == 0:
        return unmeasured(key, "no on-scene frame at all: the palette never settles on a main "
                               "scene, or every frame is a declared insert")
    v = tr.valid()
    if not v:
        return unmeasured(key, f"0 of {tr.on_scene_n} on-scene samples valid -- no face, or "
                               f"the silhouette never lands on his head band")
    if tr.valid_frac() < min_valid:
        return Row(key, False, f"detector agreement: only {len(v)}/{tr.on_scene_n} on-scene samples "
                               f"valid (min {min_valid*100:.0f} %); first reasons "
                               f"{sorted({s['why'] for s in tr.samples if not s['valid'] and s['why']})[:3]}")
    return None


def _runs(hits, fps):
    """Keep only readings that persist PERSIST consecutive samples; returns (t, value) of each."""
    out, run = [], []
    for h in hits:
        if run and abs(h[0] - run[-1][0] - 1.0 / fps) < 1e-3:
            run.append(h)
        else:
            if len(run) >= PERSIST:
                out.extend(run)
            run = [h]
    if len(run) >= PERSIST:
        out.extend(run)
    return out


# ---------------------------------------------------------------------------- rows
def hair_top(key, pic, cfg, plan):
    """framing:hair_top -- the hair never touches the top edge, on either segmenter."""
    tr = track_of(pic, plan)
    bad = _need(key, tr)
    if bad is not None:
        return bad
    lo = cfg["min_px"]
    v = tr.valid()
    tops = np.array([s["top1080"] for s in v], dtype=float)
    cut = _runs([(s["t"], s["top1080"]) for s in v if s["top1080"] < lo], tr.fps)
    # the independent test: the second segmenter sees head in the top rows of the band
    edge = _runs([(s["t"], s["edge_m"]) for s in tr.samples
                  if s.get("edge_m") is not None and s["edge_m"] >= cfg["edge_frac"]], tr.fps)
    ok = not cut and not edge
    return Row(key, ok,
               f"hair top below the edge: min {tops.min():.0f} px, median {np.median(tops):.0f} "
               f"(min {lo:.0f} px, normalized to each 1080-high talking-head window); {len(cut)} "
               f"sample(s) under it for >= {PERSIST} in a row "
               f"{cut[:5]}; independent top-rows test: {len(edge)} sample(s) with head in the top "
               f"{TOP_ROWS} rows (>= {cfg['edge_frac']}) {edge[:5]}; {len(v)}/{tr.on_scene_n} valid",
               dict(min=float(tops.min()), median=float(np.median(tops)), cut=cut[:40],
                    edge=edge[:40], valid=len(v), on_scene=tr.on_scene_n, min_px=lo))


def headroom(key, pic, cfg, plan):
    """framing:headroom -- each hold anchors the hair inside [seg_min, seg_max]; median <= max."""
    tr = track_of(pic, plan)
    bad = _need(key, tr)
    if bad is not None:
        return bad
    lo, hi, med_max = cfg["seg_min_px"], cfg["seg_max_px"], cfg["median_max_px"]
    all_hs = talk_holds(pic, tr)
    hs = [h for h in all_hs if not all(s.get("motion") == "fixed-wide" for s in h)]
    if not all_hs:
        return unmeasured(key, "no TALKING hold of >= 1 s with valid samples (mouth never moves "
                               "on a hold: b-roll only, or the face finder is on the wrong face)")
    if not hs:
        tops = [s["top1080"] for h in all_hs for s in h]
        return Row(key, True,
                   f"{len(all_hs)} talking hold(s) are intentional fixed-wide shots; tracking "
                   f"headroom bounds do not apply, while hair safety remains measured on every "
                   f"sample by framing:hair_top (median {np.median(tops):.0f} normalized px)",
                   dict(fixed_wide=len(all_hs), tracked=0, median=float(np.median(tops))))
    mins = [(round(h[0]["t"], 2), round(_robust_min(s["top1080"] for s in h))) for h in hs]
    loose = [m for m in mins if m[1] > hi]
    tight = [m for m in mins if m[1] < lo]
    med = float(np.median([s["top1080"] for h in hs for s in h]))
    ok = not loose and not tight and med <= med_max
    return Row(key, ok,
               f"{len(hs)} tracked talking holds + {len(all_hs)-len(hs)} intentional fixed-wide; "
               f"per-hold min hair top {[m[1] for m in mins[:12]]}{'...' if len(mins) > 12 else ''} "
               f"(must sit in {lo:.0f}-{hi:.0f} normalized px inside its own window): "
               f"{len(loose)} loose {loose[:4]}, "
               f"{len(tight)} tight {tight[:4]}; median over the video {med:.0f} (max {med_max:.0f})",
               dict(holds=len(hs), fixed_wide=len(all_hs)-len(hs), mins=mins[:60],
                    loose=loose[:30], tight=tight[:30],
                    median=med, seg_min=lo, seg_max=hi, median_max=med_max))


def centering(key, pic, cfg, plan):
    """framing:centering -- his head band sits on the frame's centre line, per hold."""
    tr = track_of(pic, plan)
    bad = _need(key, tr)
    if bad is not None:
        return bad
    all_hs = holds(pic, tr)
    hs = [h for h in all_hs if not all(s.get("motion") == "fixed-wide" for s in h)]
    if not hs:
        if all_hs:
            return Row(key, True, f"{len(all_hs)} hold(s) are intentional fixed-wide shots; "
                                  "face and hair were still detected inside every declared window",
                       dict(fixed_wide=len(all_hs), tracked=0))
        return unmeasured(key, "no hold of >= 1 s with valid samples")
    tol = cfg["max_off_frac"]
    offs = [(round(h[0]["t"], 2), float(np.median([s["cx_off_frac"] for s in h]))) for h in hs]
    off = [o for o in offs if abs(o[1]) > tol]
    worst = max(offs, key=lambda o: abs(o[1]))
    return Row(key, not off,
               f"{len(hs)} tracked hold(s) + {len(all_hs)-len(hs)} intentional fixed-wide; head "
               f"centre vs its window centre: worst {worst[1]*100:+.1f}% at {worst[0]}s "
               f"(max +-{tol*100:.0f}%); {len(off)} hold(s) "
               f"off {off[:5]}",
               dict(worst=worst, off=off[:30], max_px=tol))


def no_wide_level(key, pic, cfg, plan):
    """framing:no_wide_level -- the head never drops below the FAR level's size."""
    tr = track_of(pic, plan)
    bad = _need(key, tr)
    if bad is not None:
        return bad
    hs = talk_holds(pic, tr)
    if not hs:
        return unmeasured(key, "no TALKING hold of >= 1 s with valid samples")
    lo = cfg["min_head_frac"]
    meds = [(round(h[0]["t"], 2), float(np.median([s["hh_frac"] for s in h]))) for h in hs]
    wide = [m for m in meds if m[1] < lo]
    smallest = min(meds, key=lambda m: m[1])
    return Row(key, not wide,
               f"{len(hs)} talking holds; head height (hair -> chin) per hold: smallest "
               f"{smallest[1]*100:.1f}% of its window at {smallest[0]}s "
               f"(min {cfg['min_head_frac']*100:.1f}%); "
               f"{len(wide)} wide hold(s) {wide[:5]}",
               dict(smallest=smallest, wide=wide[:30], min_frac=lo))


def push_coverage(key, pic, cfg, plan):
    """framing:push_coverage -- the talk is not ONE fixed crop: its framing levels spread.

    ad1-vertical-attempt1 ran 100 % of its talk at one locked-off crop (Dan: "truly awful");
    Muhammad's Ad 2 spends 39 % of talk inside 14 pushes. Measured as the SPREAD of the per-hold
    median head heights across the talking holds -- largest over smallest, inside the `push_ratio`
    window of the dominant level (a hold outside it is a different shot: outdoor b-roll, a photo
    card with a face on it). Per-hold medians, because a locked-off crop still reads +-10 % of head
    height as Dan leans toward and away from the camera (ad1-vertical-attempt1: 425-479 px inside
    one hold), and a push is a change BETWEEN holds. Measured 2026-09-12:
        ad1-vertical-attempt1  (rejected)   434 / 436          spread x1.005
        muhammad ad 2 16x9     (reference)  379 .. 448         x1.18
        website rev 4          (approved)   328 .. 413         x1.26   (NEAR / FAR alternate)
        ad 1 | claude | 9x16   (approved)   674 .. 825         x1.22
        ad 2 | claude | 9x16   (approved)   665 .. 834         x1.25
    """
    tr = track_of(pic, plan)
    bad = _need(key, tr)
    if bad is not None:
        return bad
    hs = talk_holds(pic, tr)
    if not hs:
        return unmeasured(key, "no TALKING hold of >= 1 s with valid samples")
    meds = np.array([float(np.median([s["hh_frac"] for s in h])) for h in hs])
    n = np.array([len(h) for h in hs])
    step = cfg["level_step"]
    q = np.round(meds / step).astype(int)
    vals, counts = np.unique(q, return_counts=True)
    dom = float(np.median(np.repeat(meds, n)[np.repeat(q, n) == vals[int(np.argmax(counts))]]))
    lo_r, hi_r = cfg["push_ratio"]
    same = (meds / dom >= lo_r) & (meds / dom <= hi_r)
    if same.sum() < 2:
        return Row(key, False, f"only {int(same.sum())} talking hold(s) at the dominant shot "
                               f"(head {dom*100:.1f}% of its window): a single hold is one fixed "
                               "crop by definition", dict(holds=int(same.sum()), dominant_frac=dom))
    spread = float(meds[same].max() / meds[same].min())
    lo = cfg["min_spread"]
    off = float(n[same & (np.abs(meds / dom - 1.0) >= 0.06)].sum() / max(1, n[same].sum()))
    return Row(key, spread >= lo,
               f"{int(same.sum())} talking holds on the dominant shot (head {dom*100:.1f}% of its "
               f"window): per-hold median head height {meds[same].min()*100:.1f}-"
               f"{meds[same].max()*100:.1f}% = spread x{spread:.3f} (min x{lo}); {off*100:.0f}% of that "
               f"talk sits >= 6 % off the dominant level; {int((~same).sum())} hold(s) on other shots ignored",
               dict(spread=round(spread, 4), min_spread=lo, dominant_frac=dom, off_frac=round(off, 3),
                    holds=int(same.sum()), other_shots=int((~same).sum())))


# ---------------------------------------------------------------------------- proof sheet
def proof_sheet(pic, tr, out, n_tight=6, n_loose=3):
    """Native-scale, contrast-stretched crops of the tightest and loosest valid samples, with the
    measured hair line. Every earlier sheet lied at 480 px tiles ("a line at the hairline and a
    line at the hair top are two pixels apart"); this one is 1:1."""
    from PIL import Image, ImageDraw, ImageFont
    v = tr.valid()
    if not v:
        return None
    picks = [("tight", s) for s in sorted(v, key=lambda s: s["top"])[:n_tight]]
    picks += [("loose", s) for s in sorted(v, key=lambda s: -s["top"])[:n_loose]]
    med = float(np.median([s["top"] for s in v]))
    picks += [("median", min(v, key=lambda s: abs(s["top"] - med)))]
    TW, TH = 640, 360
    cols = 5
    rows = (len(picks) + cols - 1) // cols
    sheet = Image.new("RGB", (TW * cols, (TH + 26) * rows), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    try:
        fnt = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except Exception:
        fnt = ImageFont.load_default()
    for n, (kind, s) in enumerate(picks):
        raw = subprocess.run([C.FF, "-v", "error", "-ss", f"{s['t']:.3f}", "-i", pic.v, "-frames:v",
                              "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True).stdout
        if len(raw) < tr.W * tr.H * 3:
            continue
        full = np.frombuffer(raw[:tr.W * tr.H * 3], np.uint8).reshape(tr.H, tr.W, 3)
        ox, oy, ww, wh = s.get("ox", 0), s.get("oy", 0), s.get("win_w", tr.W), s.get("win_h", tr.H)
        win = full[oy:oy + wh, ox:ox + ww]
        cx = int(s["cx"])
        xs = max(0, min(max(0, ww - TW), cx - TW // 2))
        crop = win[0:min(TH, wh), xs:min(ww, xs + TW)].astype(float)
        if crop.shape[:2] != (TH, TW):
            crop = np.asarray(Image.fromarray(crop.astype(np.uint8)).resize((TW, TH)))
        lo_, hi_ = np.percentile(crop, 1), np.percentile(crop, 99)
        crop = np.clip((crop - lo_) / (hi_ - lo_ + 1e-6) * 255, 0, 255).astype(np.uint8)
        tile = Image.fromarray(crop)
        td = ImageDraw.Draw(tile)
        sy = TH / max(1, wh)
        td.line([(0, s["top"] * sy), (TW, s["top"] * sy)], fill=(0, 255, 0), width=2)
        if s.get("top_m") is not None:
            td.line([(0, s["top_m"] * sy), (TW, s["top_m"] * sy)], fill=(255, 0, 255), width=1)
        for gy in range(0, TH, 50):
            td.line([(0, gy), (14, gy)], fill=(255, 0, 0), width=1)
            td.text((16, gy - 8), str(gy), fill=(255, 255, 0), font=fnt)
        X, Y = (n % cols) * TW, (n // cols) * (TH + 26)
        sheet.paste(tile, (X, Y + 26))
        d.text((X + 4, Y + 2), f"{kind} {s['t']:.2f}s hair top {s['top']} px (vision; magenta = "
                               f"selfie-seg {s.get('top_m')})", fill=(255, 255, 0), font=fnt)
    sheet.save(out, quality=90)
    return out


if __name__ == "__main__":                     # measurement CLI: dump the track + row readings
    import argparse
    import json
    import sys
    sys.path.insert(0, os.path.join(C.REPO, ".claude/skills"))
    from _shared.deliver.checks import picture as PIC
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--plan")
    ap.add_argument("--json")
    ap.add_argument("--sheet")
    a = ap.parse_args()
    plan = json.load(open(a.plan)) if a.plan else {}
    pr = C.probe(a.video)
    pic = PIC.Picture(a.video, pr["vdur"])
    tr = track_of(pic, plan)
    v = tr.valid()
    print(f"{os.path.basename(a.video)}: {len(tr.samples)} on-scene samples, {len(v)} valid "
          f"({tr.valid_frac()*100:.0f} %), {tr.W}x{tr.H}")
    if v:
        tops = np.array([s["top"] for s in v]); hh = np.array([s["hh"] for s in v])
        cxs = np.array([s["cx"] for s in v]) - tr.W / 2
        print(f"  hair top  min {tops.min():.0f} p5 {np.percentile(tops,5):.0f} med {np.median(tops):.0f} "
              f"p95 {np.percentile(tops,95):.0f} max {tops.max():.0f}")
        print(f"  head hh   min {hh.min():.0f} med {np.median(hh):.0f} max {hh.max():.0f}  "
              f"({hh.min()/tr.H*100:.1f}-{hh.max()/tr.H*100:.1f} % of H)")
        print(f"  centre    min {cxs.min():+.0f} med {np.median(cxs):+.0f} max {cxs.max():+.0f}")
        em = [s["edge_m"] for s in tr.samples if s.get("edge_m") is not None]
        print(f"  edge_m    max {max(em):.3f}  n>=0.2 {sum(1 for e in em if e >= 0.2)}")
        hs = holds(pic, tr)
        print(f"  holds {len(hs)}: mins {[round(min(s['top'] for s in h)) for h in hs][:40]}")
        print(f"  robust mins: {[round(_robust_min(s['top'] for s in h)) for h in hs][:40]}")
        print(f"  hold mo sd: {[round(float(np.std([s['mo'] for s in h])), 3) for h in hs][:40]}")
        print(f"  talk holds: {len(talk_holds(pic, tr))}")
        print(f"  hold hh: {[round(float(np.median([s['hh'] for s in h]))) for h in hs][:40]}")
        print(f"  hold cx: {[round(float(np.median([s['cx'] for s in h])) - tr.W/2) for h in hs][:40]}")
        whys = {}
        for s in tr.samples:
            if not s["valid"]:
                whys[s["why"]] = whys.get(s["why"], 0) + 1
        print(f"  invalid: {whys}")
    if a.json:
        json.dump(dict(W=tr.W, H=tr.H, on_scene=tr.on_scene_n, samples=tr.samples,
                       events=pic.change_events()), open(a.json, "w"))
    if a.sheet:
        proof_sheet(pic, tr, a.sheet)
