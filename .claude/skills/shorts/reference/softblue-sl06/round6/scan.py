"""Window scan (SL-06 R6, 2026-10-21): find the most natural stretch of an 8 s Veo take for an intro of N frames.

Reviewers failed takes that my per-take checks passed: a slow ~1 Hz body rock (112 px), a head snap and sharpness pop in the
first 0.4 s (the uploaded still turning into Veo's render), eyes closing on the last frame, a smile fading by 14 %. So per frame:
  lip gap, mouth width, eye openness (face mesh, / eye distance), nose, face sharpness (Laplacian variance),
  torso and hand positions (median optical flow, integrated).
Calibrated on reviewer verdicts (C passed: waist 18, head 31, hand 30; A/D failed: waist 138/112, head 78/69).
A window passes when, inside it: lips closed (gap <= 0.04); mouth width within 10 % (max/min); eyes open on the first and last
3 frames, at most 1 blink; sharpness max/min <= 3.2; waist silhouette range <= 30 px; head range <= 35 px; hand range <= 40 px; tremor (tremor.py hf) on
hand <= 0.75 and head <= 0.70. Windows start at >= 0.5 s (skips the still-to-render pop). Score = sum of normalised margins.
  python3 scan.py S TAKE.mp4 [--variant h] [--json out.json]
"""
import argparse, json, os, sys
import cv2, numpy as np, mediapipe as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tremor import hf
N_FR = {"A": 99, "B": 111, "C": 68, "D": 79, "E": 76, "F": 60}


def flowtrack(G, box):
    x, y, w, h = map(int, box); pos = [np.zeros(2)]; cx, cy = float(x), float(y)
    for p, q in zip(G, G[1:]):
        X = min(max(int(round(cx)), 0), 1080 - w); Y = min(max(int(round(cy)), 0), 1920 - h)
        fl = cv2.calcOpticalFlowFarneback(p[Y:Y + h, X:X + w], q[Y:Y + h, X:X + w], None, 0.5, 3, 21, 3, 5, 1.1, 0)
        v = np.median(fl.reshape(-1, 2), 0); pos.append(pos[-1] + v); cx += v[0]; cy += v[1]
    return np.array(pos)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("S"); ap.add_argument("take"); ap.add_argument("--variant", default="h")
    ap.add_argument("--json"); ap.add_argument("--whole", action="store_true", help="one window: the whole clip from frame 0")
    a = ap.parse_args(); S = a.S; n = N_FR[S]
    cap = cv2.VideoCapture(a.take); F = []
    while True:
        ok, f = cap.read()
        if not ok: break
        F.append(cv2.resize(f, (1080, 1920), interpolation=cv2.INTER_AREA))
    G = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in F]
    gap, wid, eye, nose, sharp = [], [], [], [], []
    with mp.solutions.face_mesh.FaceMesh(refine_landmarks=True) as fm:
        for f in F:
            r = fm.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            if not r.multi_face_landmarks:
                gap.append(np.nan); wid.append(np.nan); eye.append(np.nan); nose.append((np.nan, np.nan)); sharp.append(np.nan); continue
            L = r.multi_face_landmarks[0].landmark; X = lambda k: np.array([L[k].x * 1080, L[k].y * 1920])
            ed = np.linalg.norm(X(33) - X(263))
            gap.append(np.linalg.norm(X(13) - X(14)) / ed); wid.append(np.linalg.norm(X(61) - X(291)) / ed)
            eye.append((np.linalg.norm(X(159) - X(145)) + np.linalg.norm(X(386) - X(374))) / 2 / ed); nose.append(X(1))
            xs = [p.x * 1080 for p in L]; ys = [p.y * 1920 for p in L]
            g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)[int(min(ys)):int(max(ys)), int(min(xs)):int(max(xs))]
            sharp.append(cv2.Laplacian(g, cv2.CV_64F).var())
    gap, wid, eye, sharp, nose = map(np.array, (gap, wid, eye, sharp, nose))
    fb = json.load(open(os.path.join(HERE, "face_boxes.json")))[S]["face"]; x, y, w, h = fb
    cx = x + w // 2
    torso = (cx - 90, min(y + h + 620, 1920 - 170), 180, 160)      # the abs/navel: always skin, below the vial hand
    head = flowtrack(G, fb)
    band = (min(y + h + 600, 1700), min(y + h + 760, 1860))           # waist rows: the silhouette's centre and edges
    seg = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0); T = []
    for f in F:
        m = seg.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).segmentation_mask[band[0]:band[1]] > 0.5
        cols = np.where(m.any(0))[0]
        xs = np.where(m)[1]
        T.append((xs.mean() if xs.size else np.nan, cols.min() if cols.size else np.nan))
    tor = np.array(T)
    vb = json.load(open(os.path.join(HERE, "vials_h.json")))[S] if a.variant == "h" else None
    hand = flowtrack(G, (vb[0] - 30, vb[1] - 30, vb[2] - vb[0] + 60, vb[3] - vb[1] + 60)) if vb else None
    eye_open = np.nanmedian(eye)
    res = []
    closed = eye < 0.6 * eye_open
    starts = [0] if a.whole else range(12, len(F) - n + 1, 3)       # start >= 0.5 s (skips the still-to-render pop), step 3
    if a.whole: n = len(F)
    for s in starts:
        e = s + n; sl = slice(s, e); fails = []
        if np.isnan(gap[sl]).any(): fails.append("face lost")
        gmax = np.nanmax(gap[sl]); wr = np.nanmax(wid[sl]) / np.nanmin(wid[sl]); sr = np.nanmax(sharp[sl]) / np.nanmin(sharp[sl])
        ends = np.r_[eye[s:s + 3], eye[e - 3:e]]
        tr = np.ptp(tor[sl], 0).max(); hr = np.ptp(head[sl], 0).max(); har = np.ptp(hand[sl], 0).max() if hand is not None else 0
        thf = hf(hand[sl]) if hand is not None else 0; hhf = hf(head[sl])
        if gmax > 0.04: fails.append(f"lips {gmax:.3f}")
        if wr > 1.10: fails.append(f"mouth width {100 * (wr - 1):.0f}%")
        if np.nanmin(ends) < 0.6 * eye_open: fails.append("eyes closed at an end")
        if sr > 3.2: fails.append(f"sharpness x{sr:.2f}")
        if tr > 30: fails.append(f"torso sway {tr:.0f}px")
        if hr > 30: fails.append(f"head travel {hr:.0f}px")
        cl = np.nan_to_num(closed[sl]).astype(int)                 # a blink = a run of >= 2 closed frames (one-frame dips are noise)
        runs, k = [], 0
        for i, v in enumerate(list(cl) + [0]):
            if v: k += 1
            elif k: runs.append((i - k, k)); k = 0
        bl = [st for st, r in runs if r >= 2]; blinks = len(bl)
        if blinks > 2 or (blinks == 2 and bl[1] - bl[0] < 36): fails.append(f"{blinks} blinks")   # 2 allowed if >= 1.5 s apart
        if any(r > 6 for st, r in runs): fails.append(f"slow eye closure ({max(r for st, r in runs)} frames)")   # a real blink is 3-5
        if har > 40: fails.append(f"hand travel {har:.0f}px")
        if thf > 0.75: fails.append(f"hand tremor {thf:.2f}")
        if hhf > 0.70: fails.append(f"head tremor {hhf:.2f}")
        score = (0.04 - gmax) / 0.04 + (1.10 - wr) / 0.10 + (30 - tr) / 30 + (30 - hr) / 30 + (40 - har) / 40 + (0.75 - thf) / 0.75 + (0.7 - hhf) / 0.7 + (3.2 - sr) / 1.6
        res.append(dict(start=s, t=round(s / 24, 3), ok=not fails, fails=fails, score=round(float(score), 2),
                        torso=round(float(tr), 1), head=round(float(hr), 1), hand=round(float(har), 1), hand_hf=round(thf, 2),
                        head_hf=round(hhf, 2), lips=round(float(gmax), 3), blinks=blinks, width=round(float(wr), 3), sharp=round(float(sr), 2)))
    good = sorted([r for r in res if r["ok"]], key=lambda r: -r["score"])
    best = good[0] if good else sorted(res, key=lambda r: (len(r["fails"]), -r["score"]))[0]
    tag = os.path.basename(a.take)[:-4]
    print(f"{tag}: {len(good)}/{len(res)} windows pass; best start {best['t']}s ok={best['ok']} score {best['score']} "
          f"torso {best['torso']} head {best['head']} hand {best['hand']} hf {best['hand_hf']}/{best['head_hf']} lips {best['lips']} "
          f"width {best['width']} sharp {best['sharp']} blinks {best['blinks']} {'; '.join(best['fails'])}")
    if a.json: json.dump(dict(take=a.take, S=S, n=n, windows=res, best=best), open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
