#!/usr/bin/env python3
"""ROUND 2, R5 -- choose the grade by MEASURING Dan's skin, exposure AND saturation.

Plan section 12, R5, replaces round 1's exposure-only rule (which produced D6, "he looks grey-brown
and flat beside the saturated AI image and the studio photos he is intercut with"):

  * exposure in 1.00-1.30, chosen by FACE LUMA against the approved website video (target 73 +- 5);
  * then `eq=saturation` raised from 0.88 until Dan's FACE CHROMA reaches >= 85 % of the approved
    Ad 1 vertical's, capped at 1.25;
  * no white-balance and no hue change -- `eq=saturation` scales chroma only;
  * prove it on a sheet of four graded frames beside Ad 1 frames and check the trees, the pool and
    the shorts have not gone neon.

Every number is measured through ONE routine (`skin_stats`) on both sides, so the 85 % ratio is a
ratio of like for like. Writes grade.json and r2/grade/proof.jpg.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
import mediapipe as mp

REPO = L.REPO
AD1 = (f"{REPO}/Zeeshan Ad Videos/this picture got me abs - ad 1/"
       "this picture got me abs | claude | 9x16 | ad 1.mp4")
WEB = (f"{REPO}/Website Videos/Website Conversion Video (post-generation)/website_video_16x9.mp4")
OUT = "r2/grade"
os.makedirs(OUT, exist_ok=True)

# talking-head instants picked by eye off r2/grade/ad1_sheet.png (a 3 s contact sheet): every one
# is Dan on camera in the approved vertical, never a card, a phone or an AI insert.
AD1_T = [21, 24, 33, 36, 42, 48, 90, 96, 108, 132, 135, 138]
# ours: instants inside the kept take where Dan is talking to camera
OUR_T = [33, 41, 50, 58, 66, 74, 80, 88]
WEB_T = [30, 60, 95]

fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)
fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)


def _rgb2lab(px):
    """sRGB (0-255 float, N x 3) -> CIELAB D65. Plain, explicit, no colour library."""
    c = px/255.0
    c = np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787*xyz + 16/116)
    Lv = 116*f[:, 1] - 16
    a = 500*(f[:, 0] - f[:, 1])
    b = 200*(f[:, 1] - f[:, 2])
    return Lv, a, b


def skin_stats(path):
    """Median skin luma / L* / a* / b* / chroma over the FACE, located by mediapipe.

    The face is found by landmarks (full-range detector first for a small face in a 4K portrait
    frame), the skin inside the face box is selected by the same R>G>B test s17_expo.py used, and
    every statistic is a MEDIAN so a specular highlight or a glasses frame cannot move it.
    """
    a = np.asarray(Image.open(path).convert("RGB")); H, W = a.shape[:2]
    r = fm.process(np.ascontiguousarray(a))
    if r.multi_face_landmarks:
        Lm = r.multi_face_landmarks[0].landmark
        xs = [p.x*W for p in Lm]; ys = [p.y*H for p in Lm]
    else:
        d = fd.process(np.ascontiguousarray(a))
        if not d.detections: return None
        b = d.detections[0].location_data.relative_bounding_box
        cx, cy = (b.xmin+b.width/2)*W, (b.ymin+b.height/2)*H
        s_ = max(b.width*W, b.height*H)*2.2
        cx0, cy0 = int(max(0, cx-s_/2)), int(max(0, cy-s_/2))
        cx1, cy1 = int(min(W, cx+s_/2)), int(min(H, cy+s_/2))
        rr = fm.process(np.ascontiguousarray(a[cy0:cy1, cx0:cx1]))
        if not rr.multi_face_landmarks: return None
        Lm = rr.multi_face_landmarks[0].landmark
        cw, ch = cx1-cx0, cy1-cy0
        xs = [p.x*cw+cx0 for p in Lm]; ys = [p.y*ch+cy0 for p in Lm]
    x0, x1 = int(max(0, min(xs))), int(min(W, max(xs)))
    y0, y1 = int(max(0, min(ys))), int(min(H, max(ys)))
    c = a[y0:y1, x0:x1].astype(np.float32)
    if c.size < 300: return None
    R, G, B = c[..., 0], c[..., 1], c[..., 2]
    skin = (R > G+8) & (G > B) & (R > 55)
    if skin.sum() < 200: return None
    px = c[skin]
    luma = 0.2126*px[:, 0] + 0.7152*px[:, 1] + 0.0722*px[:, 2]
    Lv, av, bv = _rgb2lab(px)
    return {"face_luma": float(np.median(luma)), "L": float(np.median(Lv)),
            "a": float(np.median(av)), "b": float(np.median(bv)),
            "chroma": float(np.median(np.hypot(av, bv))), "n": int(skin.sum()),
            "face_box": [x0, y0, x1, y1]}


def frame_chroma(path, mask_face=True):
    """Whole-frame chroma percentiles -- the 'have the trees and the pool gone neon' test."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    px = a.reshape(-1, 3)[::37]
    _, av, bv = _rgb2lab(px)
    ch = np.hypot(av, bv)
    return {"p50": float(np.percentile(ch, 50)), "p95": float(np.percentile(ch, 95)),
            "p99": float(np.percentile(ch, 99)), "max": float(ch.max())}


def grab(src, t, out, vf=None):
    cmd = [L.FF, "-nostdin", "-v", "error", "-ss", f"{t}", "-i", src, "-frames:v", "1"]
    if vf: cmd += ["-vf", vf]
    cmd += ["-y", out]
    subprocess.run(cmd, check=True)
    return out


def agg(rows, keys=("face_luma", "L", "a", "b", "chroma")):
    return {k: round(float(np.median([r[k] for r in rows])), 2) for k in keys} | {"frames": len(rows)}


# ---------------------------------------------------------------- 1. the two references
ref = {}
for name, src, ts in (("ad1_vertical", AD1, AD1_T), ("website_video", WEB, WEB_T)):
    rows = []
    for t in ts:
        p = grab(src, t, f"{OUT}/ref_{name}_{t}.png")
        s = skin_stats(p)
        if s: rows.append(s)
        else: print(f"  no face on {name} @{t}s")
    ref[name] = agg(rows)
    print(f"{name:14s} {ref[name]}")

TARGET_LUMA = ref["website_video"]["face_luma"]        # plan: "target 73 +- 5, the approved website video"
CHROMA_FLOOR = 0.85*ref["ad1_vertical"]["chroma"]
print(f"\nface-luma target {TARGET_LUMA:.1f} +- 5   chroma floor {CHROMA_FLOOR:.2f} "
      f"(85 % of Ad 1's {ref['ad1_vertical']['chroma']:.2f})")

# ---------------------------------------------------------------- 2. exposure, by face luma
MAKE_LUT = (f"{REPO}/claude edited long form content/06 - Website Conversion Video "
            f"(post-generation)/recipe_REV5/make_lut.py")
EXPOS = ["1.00", "1.15", "1.30"]
for e in EXPOS:
    if not os.path.exists(L.LUT % e):
        print(f"  building LUT e{e}")
        subprocess.run([sys.executable, MAKE_LUT, e], check=True,
                       cwd=os.path.dirname(MAKE_LUT))
        built = os.path.join(os.path.dirname(MAKE_LUT), f"slog3_709_e{e}.cube")
        if os.path.exists(built) and not os.path.exists(L.LUT % e):
            import shutil; shutil.copy2(built, L.LUT % e)
EXPOS = [e for e in EXPOS if os.path.exists(L.LUT % e)]

expo_rows = {}
for e in EXPOS:
    rows = []
    for t in OUR_T:
        vf = f"{L.DECODE},lut3d=file={L.LUT % e}:interp=tetrahedral,eq=saturation=0.88"
        p = grab(L.ROLL, t, f"{OUT}/our_e{e}_{t}.png", vf)
        s = skin_stats(p)
        if s: rows.append(s)
    expo_rows[e] = agg(rows)
    expo_rows[e]["luma_err"] = round(abs(expo_rows[e]["face_luma"] - TARGET_LUMA), 2)
    print(f"  e{e}: face luma {expo_rows[e]['face_luma']:6.1f} (err {expo_rows[e]['luma_err']:5.2f})"
          f"  L*{expo_rows[e]['L']:6.1f}  a*{expo_rows[e]['a']:5.1f} b*{expo_rows[e]['b']:5.1f}"
          f"  chroma {expo_rows[e]['chroma']:5.2f}")
inband = [e for e in EXPOS if expo_rows[e]["luma_err"] <= 5.0] or EXPOS
print(f"exposures inside the 73 +- 5 band: {inband}")

# ---------------------------------------------------------------- 3. saturation, by face chroma
# Every candidate exposure in the luma band is taken all the way to its own chosen saturation and
# judged THERE, because `eq=saturation` moves face luma a little as well: at sat 1.25 e1.00 reads
# luma 70.1 (err 3.25) and e1.15 reads 76.2 (err 2.85), i.e. the exposure that looked best at
# sat 0.88 is not the one that is best at the saturation actually delivered.
SATS = ["0.88", "0.95", "1.00", "1.05", "1.10", "1.15", "1.20", "1.25"]
grid, best = {}, None
for e in inband:
    sat_rows = {}
    for s_ in SATS:
        rows, fr = [], []
        for t in OUR_T[:5]:
            vf = f"{L.DECODE},lut3d=file={L.LUT % e}:interp=tetrahedral,eq=saturation={s_}"
            p = grab(L.ROLL, t, f"{OUT}/our_e{e}_s{s_}_{t}.png", vf)
            st = skin_stats(p)
            if st: rows.append(st)
            fr.append(frame_chroma(p))
        sat_rows[s_] = agg(rows) | {
            "frame_chroma_p95": round(float(np.median([f["p95"] for f in fr])), 2),
            "frame_chroma_p99": round(float(np.median([f["p99"] for f in fr])), 2)}
        print(f"  e{e} sat {s_}: face chroma {sat_rows[s_]['chroma']:5.2f} "
              f"(floor {CHROMA_FLOOR:.2f})  luma {sat_rows[s_]['face_luma']:6.1f}  "
              f"frame chroma p95 {sat_rows[s_]['frame_chroma_p95']:5.1f} "
              f"p99 {sat_rows[s_]['frame_chroma_p99']:5.1f}")
    ok = [s_ for s_ in SATS if sat_rows[s_]["chroma"] >= CHROMA_FLOOR]
    s_pick = ok[0] if ok else "1.25"            # the LOWEST saturation that clears the floor; else the cap
    grid[e] = {"sat": s_pick, "rows": sat_rows, "reached": sat_rows[s_pick]["chroma"] >= CHROMA_FLOOR,
               "luma_err_at_sat": round(abs(sat_rows[s_pick]["face_luma"] - TARGET_LUMA), 2)}
    print(f"  e{e} -> sat {s_pick}  chroma {sat_rows[s_pick]['chroma']:.2f}  "
          f"luma err {grid[e]['luma_err_at_sat']:.2f}  "
          f"floor {'reached' if grid[e]['reached'] else 'NOT reached'}")

# Pick: any exposure that REACHES the floor wins (lowest saturation first, then luma error). If
# none reaches it -- which is the finding here -- take the pair that is closest to the floor while
# still inside the luma band; a chroma shortfall is the defect D6 is about.
reached_any = [e for e in inband if grid[e]["reached"]]
if reached_any:
    EXPO = min(reached_any, key=lambda e: (float(grid[e]["sat"]), grid[e]["luma_err_at_sat"]))
else:
    EXPO = max(inband, key=lambda e: (grid[e]["rows"][grid[e]["sat"]]["chroma"],
                                      -grid[e]["luma_err_at_sat"]))
SAT = grid[EXPO]["sat"]
sat_rows = grid[EXPO]["rows"]
reached = grid[EXPO]["reached"]
print(f"GRADE -> exposure {EXPO}, saturation {SAT}  "
      f"(chroma floor {'reached' if reached else 'NOT reached at the 1.25 cap'})")

out = {
 "_rule": "plan section 12 R5: exposure 1.00-1.30 by face luma (target 73 +- 5, the approved "
          "website video); saturation raised from 0.88 until face chroma >= 85 % of the approved "
          "Ad 1 vertical's, capped at 1.25; no white-balance or hue change.",
 "exposure": EXPO, "saturation": SAT,
 "lut": L.LUT % EXPO,
 "filter": f"lut3d=file={L.LUT % EXPO}:interp=tetrahedral,eq=saturation={SAT}",
 "reference": ref, "target_face_luma": round(TARGET_LUMA, 2),
 "chroma_floor_85pct_of_ad1": round(CHROMA_FLOOR, 2),
 "chroma_floor_reached": bool(reached),
 "exposure_tests": expo_rows, "saturation_tests": sat_rows,
 "grid": {e: {"sat": g["sat"], "reached": g["reached"], "luma_err_at_sat": g["luma_err_at_sat"],
              "chroma_at_sat": g["rows"][g["sat"]]["chroma"]} for e, g in grid.items()},
 "face_chroma_pct_of_ad1": round(100*sat_rows[SAT]["chroma"]/ref["ad1_vertical"]["chroma"], 1),
 "round1_was": {"exposure": "1.30", "saturation": "0.88",
                "face_chroma_measured_here": expo_rows["1.30"]["chroma"]},
}
json.dump(out, open("grade.json", "w"), indent=1)
print("\ngrade.json written ->", out["filter"])

# ---------------------------------------------------------------- 4. the proof sheet
from PIL import ImageDraw
from motionlib import font
tiles, labels = [], []
for t in OUR_T[:4]:
    p = f"{OUT}/our_e{EXPO}_s{SAT}_{t}.png"
    if not os.path.exists(p):
        vf = f"{L.DECODE},lut3d=file={L.LUT % EXPO}:interp=tetrahedral,eq=saturation={SAT}"
        grab(L.ROLL, t, p, vf)
    tiles.append(p)
    labels.append(f"RA-01 e{EXPO} sat{SAT}  t={t}s")
for t in AD1_T[:4]:
    tiles.append(f"{OUT}/ref_ad1_vertical_{t}.png"); labels.append(f"Ad 1 vertical (approved) t={t}s")
TH = 620
ims = []
for p, lab in zip(tiles, labels):
    im = Image.open(p).convert("RGB")
    k = TH/im.height
    im = im.resize((int(im.width*k), TH), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = font(20, "ExtraBold")
    d.rectangle([0, 0, im.width, 30], fill=(0, 0, 0))
    d.text((6, 4), lab, font=f, fill=(255, 220, 90))
    ims.append(im)
rows = [ims[:4], ims[4:]]
W = max(sum(i.width for i in r) for r in rows)
sheet = Image.new("RGB", (W, TH*2), (20, 20, 20))
for ri, r in enumerate(rows):
    x = 0
    for im in r:
        sheet.paste(im, (x, ri*TH)); x += im.width
sheet.save(f"{OUT}/proof.jpg", quality=92)
print(f"{OUT}/proof.jpg  (top: ours graded, bottom: the approved Ad 1 vertical)")
