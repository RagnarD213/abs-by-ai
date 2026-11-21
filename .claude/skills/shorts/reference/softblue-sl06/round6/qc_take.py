"""SL-06 R6: measure one Veo intro take for "does it look like a calm real person" (2026-10-21).

  python3 qc_take.py S TAKE.mp4 [--start 0] [--out DIR]

Over the intro window (S's length, from --start seconds):
  - mouth: MediaPipe face mesh lip gap and mouth width, both / eye distance, every frame. Talking or a toothy grin shows as
    lip-gap peaks; a growing grin as mouth-width growth.
  - tremor: jitter.py-style tracks of the vial fist(s) and the pointing fingertip (template match), plus the nose landmark;
    jitter = residual from a 0.33 s moving average, RMS in px at 1080x1920.
  - strips for eyes-on review: 8 full frames, and the mouth every 4th frame.
Bars (calibrated 2026-10-21 on the six R5 intros Dan rejected for shaking: vial jitter RMS 1.8 to 3.6 px):
  vial / finger jitter RMS <= 1.0 px, nose jitter RMS <= 1.0 px, lip gap / eye <= 0.04 on every frame, mouth width growth <= 6 %.
"""
import argparse, json, os, sys
import cv2, numpy as np
import mediapipe as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tremor import hf as _hf

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = {"A": 99, "B": 111, "C": 68, "D": 79, "E": 76, "F": 60}      # intro lengths at 24 fps (R5 fix files)
VIALS = {"A": [(731, 732, 773, 814)], "B": [(794, 577, 838, 657)], "C": [(761, 529, 800, 606)],
         "D": [(246, 670, 288, 739), (805, 670, 846, 739)], "E": [(781, 551, 823, 631)], "F": [(801, 593, 845, 670)]}
FINGER = {"A": (149, 780), "B": (113, 763), "C": (137, 708), "E": (113, 722), "F": (156, 895)}
BARS = {"hand_hf": 0.75, "head_hf": 0.70, "lipgap": 0.04, "width_growth": 0.06, "drift": 45}
# hf = frame-to-frame wobble (tremor.py) of the median optical flow in a box. Calibrated 2026-10-21: rejected R5 hands 0.89-2.18,
# relaxed-pose takes 0.37-0.65, flexed fists 1.6; real footage of Dan's head 0.41-0.65. Template tracks only catch a lost/morphed
# object (match < 0.6) or a hand that leaves its place (drift > 45 px).


def subpix(r, x, y):
    def para(a, b, c):
        d = a - 2 * b + c
        return 0.0 if abs(d) < 1e-9 else 0.5 * (a - c) / d
    h, w = r.shape
    return (x + (para(r[y, x - 1], r[y, x], r[y, x + 1]) if 0 < x < w - 1 else 0),
            y + (para(r[y - 1, x], r[y, x], r[y + 1, x]) if 0 < y < h - 1 else 0))


def track(grays, box, pad=48):
    x, y, w, h = box; tpl = grays[0][y:y + h, x:x + w]; px, py = float(x), float(y); P = []
    for f in grays:
        sx0, sy0 = max(0, int(px) - pad), max(0, int(py) - pad)
        sx1, sy1 = min(1080, int(px) + w + pad), min(1920, int(py) + h + pad)
        r = cv2.matchTemplate(f[sy0:sy1, sx0:sx1], tpl, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(r); bx, by = subpix(r, *ml); px, py = sx0 + bx, sy0 + by; P.append((px, py, mv))
    return np.array(P)


def jitter(xy, fps):
    k = max(3, int(round(0.33 * fps)) | 1); ker = np.ones(k) / k
    sm = np.stack([np.convolve(np.pad(xy[:, j], k // 2, mode="edge"), ker, mode="valid") for j in (0, 1)], 1)
    j = np.linalg.norm(xy - sm, axis=1)[k // 2: -(k // 2)]
    return float(np.sqrt((j ** 2).mean())), float(np.percentile(j, 95))


def flowhf(grays, box):
    x, y, w, h = map(int, box); pos = [np.zeros(2)]; cx, cy = float(x), float(y)
    for p, q in zip(grays, grays[1:]):
        X = min(max(int(round(cx)), 0), 1080 - w); Y = min(max(int(round(cy)), 0), 1920 - h)
        fl = cv2.calcOpticalFlowFarneback(p[Y:Y + h, X:X + w].astype(np.uint8), q[Y:Y + h, X:X + w].astype(np.uint8), None, 0.5, 3, 21, 3, 5, 1.1, 0)
        v = np.median(fl.reshape(-1, 2), 0); pos.append(pos[-1] + v); cx += v[0]; cy += v[1]
    return _hf(pos)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("S"); ap.add_argument("take")
    ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--out"); ap.add_argument("--nofinger", action="store_true"); ap.add_argument("--variant", default="")
    a = ap.parse_args(); S = a.S
    out = a.out or os.path.join(HERE, "qc"); os.makedirs(out, exist_ok=True)
    tag = os.path.splitext(os.path.basename(a.take))[0] + (f"@{a.start:g}" if a.start else "")
    cap = cv2.VideoCapture(a.take); fps = cap.get(cv2.CAP_PROP_FPS) or 24; n = FRAMES[S]
    s0 = int(round(a.start * fps)); bgr = []; i = 0
    while len(bgr) < n:
        ok, f = cap.read()
        if not ok: break
        if i >= s0:
            if f.shape[:2] != (1920, 1080): f = cv2.resize(f, (1080, 1920), interpolation=cv2.INTER_AREA)
            bgr.append(f)
        i += 1
    grays = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in bgr]
    R = {"S": S, "take": a.take, "start": a.start, "frames": len(bgr), "fps": fps, "fails": []}
    # mouth via face mesh
    gaps, widths, nose = [], [], []
    with mp.solutions.face_mesh.FaceMesh(static_image_mode=False, refine_landmarks=True) as fm:
        for f in bgr:
            r = fm.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            if not r.multi_face_landmarks: gaps.append(np.nan); widths.append(np.nan); nose.append((np.nan, np.nan)); continue
            L = r.multi_face_landmarks[0].landmark; X = lambda k: np.array([L[k].x * 1080, L[k].y * 1920])
            eye = np.linalg.norm(X(33) - X(263))
            gaps.append(np.linalg.norm(X(13) - X(14)) / eye); widths.append(np.linalg.norm(X(61) - X(291)) / eye); nose.append(X(1))
    gaps, widths, nose = np.array(gaps), np.array(widths), np.array(nose)
    R["lipgap_max"] = round(float(np.nanmax(gaps)), 4); R["lipgap_mean"] = round(float(np.nanmean(gaps)), 4)
    R["width_growth"] = round(float(np.nanmax(widths) / np.nanmean(widths[:3]) - 1), 4)
    R["face_missing"] = int(np.isnan(gaps).sum())
    R["nose_jitter_rms"], R["nose_jitter_p95"] = map(lambda v: round(v, 3), jitter(nose, fps))
    if R["lipgap_max"] > BARS["lipgap"]: R["fails"].append(f"mouth opens: lip gap {R['lipgap_max']:.3f} > {BARS['lipgap']}")
    if R["width_growth"] > BARS["width_growth"]: R["fails"].append(f"smile grows {R['width_growth']:.0%}")
    if a.variant == "h":   # relaxed pose: one vial at chest height (vials_h.json), no pointing finger
        VIALS[S] = [tuple(json.load(open(os.path.join(HERE, "vials_h.json")))[S])]; a.nofinger = True; BARS["drift"] = 80   # a relaxed hand may settle; the vial stays in view
    parts = {f"vial{k}": (max(0, b[0] - 30), max(0, b[1] - 30), b[2] - b[0] + 60, b[3] - b[1] + 60) for k, b in enumerate(VIALS[S])}
    if S in FINGER and not a.nofinger: parts["finger"] = (FINGER[S][0] - 50, FINGER[S][1] - 55, 100, 110)
    for name, box in parts.items():
        P = track(grays, box); rms, p95 = jitter(P[:, :2], fps)
        R[name] = {"jitter_rms": round(rms, 3), "jitter_p95": round(p95, 3), "travel": round(float(np.linalg.norm(P[-1, :2] - P[0, :2])), 1),
                   "max_drift": round(float(np.linalg.norm(P[:, :2] - P[0, :2], axis=1).max()), 1), "min_match": round(float(P[:, 2].min()), 3)}
        R[name]["hf"] = round(flowhf(grays, box), 3)
        if R[name]["hf"] > BARS["hand_hf"]: R["fails"].append(f"{name} tremor {R[name]['hf']:.2f}")
        if R[name]["max_drift"] > BARS["drift"]: R["fails"].append(f"{name} leaves its place ({R[name]['max_drift']:.0f} px)")
        if R[name]["min_match"] < 0.6: R["fails"].append(f"{name} lost (match {R[name]['min_match']}): changed shape or vanished")
    fb0 = json.load(open(os.path.join(HERE, "face_boxes.json")))[S]["face"]
    R["head_hf"] = round(flowhf(grays, fb0), 3)
    if R["head_hf"] > BARS["head_hf"]: R["fails"].append(f"head tremor {R['head_hf']:.2f}")
    R["verdict"] = "PASS" if not R["fails"] else "FAIL"
    # strips
    idx = np.linspace(0, len(bgr) - 1, 8).astype(int)
    full = np.hstack([cv2.resize(bgr[k][0:1300], (270, 325)) for k in idx])
    fb = json.load(open(os.path.join(HERE, "face_boxes.json")))[S]["face"]; x, y, w, h = fb
    x0, y0 = max(0, x - 20), max(0, y - 20)
    faces = [cv2.resize(bgr[k][y0:y0 + h + 40, x0:x0 + w + 40], (180, int(180 * (h + 40) / (w + 40)))) for k in range(0, len(bgr), 4)]
    rows = [np.hstack(faces[r:r + 10] + [np.zeros_like(faces[0])] * (10 - len(faces[r:r + 10]))) for r in range(0, len(faces), 10)]
    cv2.imwrite(os.path.join(out, f"{tag}_full.jpg"), full); cv2.imwrite(os.path.join(out, f"{tag}_faces.jpg"), np.vstack(rows))
    json.dump(R, open(os.path.join(out, f"{tag}.qc.json"), "w"), indent=1)
    vj = " ".join(f"{k} hf {R[k]['hf']:.2f} drift {R[k]['max_drift']:.0f}" for k in parts) + f"  head hf {R['head_hf']:.2f}"
    print(f"{tag}: {R['verdict']}  lipgap max {R['lipgap_max']:.3f}  smile growth {R['width_growth']:+.0%}  {vj}  {'; '.join(R['fails'])}")


if __name__ == "__main__":
    main()
