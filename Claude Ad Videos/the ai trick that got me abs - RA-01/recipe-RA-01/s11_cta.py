#!/usr/bin/env python3
"""The CTA pill overlay (alpha MOV) for one aspect: s11_cta.py 9x16|16x9

It appears on "tap the button below" and holds through the line, at both CTA beats.

⚠ THE PILL IS PLACED BY MEASURING HIM ON THE RENDERED FRAME, per beat -- never at a fixed y.

9:16 (accepted in round 1: "960 px, on the chest, clear of the face"): the pill spans the safe
width and sits in the band between his CHIN and the top of his abs, computed from that beat's own
crop and his own head height.

16:9 -- ROUND 2, R4. Round 1 drew a 1800-px-wide solid band across the whole frame; at CTA 2 it lay
across Dan's neck and shoulders and hid the top of the physique, and it read as a letterbox error
(D5). A 16:9 window of this portrait roll is 1888-2144 source px wide and Dan is only ~35 % of it,
so there are ~600 px of clear field on each side of him and NO clear horizontal band anywhere on
him (hair to waistband fills the height). The pill is therefore COMPACT -- sized to its own text --
and placed by person mask in the clear field BESIDE him, as low as it can go while staying clear of
the caption band. That satisfies all of R4: compact, low, and never touching his face, neck or
shoulders.
"""
import json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from ra01lib import Aspect, OLIVE
from PIL import Image, ImageDraw
import motionlib as ml
from motionlib import font, text_size

KEY = sys.argv[1]; A = Aspect(KEY)
B = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
OUT = f"cta_{KEY}"; os.makedirs(OUT, exist_ok=True)

import numpy as np
import mediapipe as mp
GRADE = L.grade()
_fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                      refine_landmarks=False, min_detection_confidence=0.5)

CTA_TEXT, CTA_URL = "Tap the button below", "AbsByAI.com"
fB = font(52 if KEY == "9x16" else 44, "ExtraBold")
fU = font(40 if KEY == "9x16" else 34, "ExtraBold")
# ---- ROUND 3 (plan section 13), D6: the 16:9 pill is measured against the WHOLE beat -----------
# Round 2 probed one frame (the beat's midpoint) and placed a 552x132 pill there. Over the whole
# CTA-2 beat Dan gestures with both arms: the only column clear of him for every frame of that beat
# is the far left, 488 px wide (x 0-487; the narrowest moment is 55.12 s, where his hand reaches
# x 502), and no 552-wide box is clear anywhere between y 306 and y 940. So the round-2 pill could
# only be kept by lifting it to mid-frame (y 322), which is what D6 rejects. The 16:9 pill is
# therefore set in THREE lines -- same type sizes, narrower box -- which fits the clear column, and
# both CTA beats use the one geometry so the two pills match. Both sit bottom-left, 54 px from the
# frame edges, below the height of the round-2 CTA 1.
LINES = ([(CTA_TEXT, fB, "w"), (CTA_URL, fU, "o")] if KEY == "9x16" else
         [("Tap the button", fB, "w"), ("below", fB, "w"), (CTA_URL, fU, "o")])
PADX, PADY = (44, 22) if KEY == "9x16" else (36, 20)
LINE_H = [52, 52, 42] if KEY != "9x16" else None
TW = max(text_size(t, f)[0] for t, f, _ in LINES)
if KEY == "9x16":
    TH = text_size(CTA_TEXT, fB)[1] + 10 + text_size(CTA_URL, fU)[1]
else:
    TH = sum(LINE_H) + 8
PILL_W = TW + 2*PADX; PILL_W -= PILL_W % 2
PILL_H = (132 if KEY == "9x16" else TH + 2*PADY); PILL_H -= PILL_H % 2


def _src_at(t):
    for p in CUT["pieces"]:
        if p["t_in"] - 1e-6 <= t < p["t_out"] + 1e-6:
            return p["src_in"] + (t - p["t_in"])
    p = min(CUT["pieces"], key=lambda p: min(abs(t-p["t_in"]), abs(t-p["t_out"])))
    return p["src_in"] + min(max(t - p["t_in"], 0.0), p["t_out"] - p["t_in"] - 1e-3)


def probe_frame(t):
    """The frame this beat actually delivers, at the delivered size."""
    seg = next((p for p in B["punch"] if p["beat"][0] - 1e-6 <= t < p["beat"][1] + 1e-6), None)
    if seg is None:
        seg = min(B["punch"], key=lambda p: min(abs(t-p["beat"][0]), abs(t-p["beat"][1])))
    cw, ch = A.levels[seg["level"]]
    cy = int(round(seg["hair_min"] - 0.04*ch)); cy = max(0, min(3840-ch, cy - cy % 2))
    # R3 D5: 16:9 shares the FAR centre (see s10_render.py) -- the probe must be the delivered frame
    cxs = seg["cx16"] if (KEY == "16x9" and "cx16" in seg) else seg["cx"]
    cx = int(round(cxs - cw/2));                cx = max(0, min(2160-cw, cx - cx % 2))
    st = _src_at(t)
    p = f"{OUT}/_probe_{t:.2f}.png"
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{st:.3f}", "-i", L.ROLL,
                    "-frames:v", "1", "-vf",
                    f"crop={cw}:{ch}:{cx}:{cy},{L.DECODE},{GRADE},scale={A.VW}:{A.VH}:flags=lanczos",
                    "-y", p], check=True)
    return p, seg


def pill_box(t):
    p, seg = probe_frame(t)
    a = np.asarray(Image.open(p).convert("RGB")); H, W = a.shape[:2]
    if KEY == "9x16":
        r = _fm.process(np.ascontiguousarray(a))
        if not r.multi_face_landmarks:
            raise SystemExit(f"no face on the CTA probe frame at {t:.2f}s -- cannot place by measurement")
        Lm = r.multi_face_landmarks[0].landmark
        fore, chin = Lm[10].y*H, Lm[152].y*H
        head = chin - fore
        top = chin + 0.30*head                      # below the jaw, clear of the face
        bot = chin + 1.05*head                      # above the top of the abs
        yy = int(round((top + bot)/2 - PILL_H/2))
        yy = max(A.SAFE, min(A.CAP_Y - 34 - PILL_H, yy))
        return (A.SAFE, yy, A.VW - A.SAFE, yy + PILL_H), dict(
            chin=round(chin), head=round(head), abs_top=round(bot), level=seg["level"],
            method="chest band between the jaw and the top of the abs")
    raise SystemExit("16:9 uses pill_box16 -- the whole beat, not one frame")


# ---- 16:9 (R3 D6): the pill must be clear of him on EVERY frame of the beat, and as LOW as the
# frame allows. The mask is measured on NPROBE frames spread across the beat and unioned; the pill
# then goes to the lowest position whose box (plus PAD) touches none of them.
NPROBE = 14
PAD = 14


def beat_masks(a, b):
    ms = []
    for k in range(NPROBE):
        t = min(a + (b-a)*k/(NPROBE-1), b - 1e-3)
        p, seg = probe_frame(t)
        m = L.person_mask(Image.open(p))
        if m is None:
            raise SystemExit(f"person mask failed on the CTA probe frame at {t:.2f}s")
        ms.append((round(t, 3), m, seg["level"]))
    return ms


def pill_box16(beats):
    """ONE geometry for both CTA beats, measured against the union of every probe of BOTH: the two
    pills then match, and the position is clear of him in each beat, which picking the lower of two
    separately-solved positions would not guarantee."""
    ms = [m for a, b in beats for m in beat_masks(a, b)]
    H, W = ms[0][1].shape[:2]
    occ = np.zeros((H, W), bool)
    for _, m, _ in ms: occ |= m
    integ = np.cumsum(np.cumsum(occ.astype(np.int32), 0), 1)
    def hits(x, y, w, h):
        x0, y0 = max(0, x-PAD), max(0, y-PAD)
        x1, y1 = min(W, x+w+PAD)-1, min(H, y+h+PAD)-1
        tot = integ[y1, x1]
        if y0: tot -= integ[y0-1, x1]
        if x0: tot -= integ[y1, x0-1]
        if x0 and y0: tot += integ[y0-1, x0-1]
        return int(tot)
    ymax = A.VH - A.SAFE - PILL_H                   # the frame's own bottom safe margin
    for y in range(ymax, A.SAFE-1, -4):
        cands = [x for x in range(A.SAFE, A.VW - A.SAFE - PILL_W + 1, 4) if not hits(x, y, PILL_W, PILL_H)]
        if cands:
            ys, xs = np.where(occ)
            hx = (int(xs.min()) + int(xs.max()))//2 if len(xs) else A.VW//2
            x = max(cands, key=lambda x: abs(x + PILL_W/2 - hx))
            left = [c for c in cands if c + PILL_W/2 < hx]
            if left: x = min(left)                  # bottom-LEFT, like the round-2 CTA 1
            return (x, y, x + PILL_W, y + PILL_H), dict(
                probes=[(t, lv) for t, _, lv in ms], n_probes=len(ms),
                method="compact 3-line pill; person mask unioned over the WHOLE beat; lowest "
                       "position inside the 54 px frame-safe margin that no frame of EITHER beat touches")
    raise SystemExit(f"no clear position for a {PILL_W}x{PILL_H} pill over the CTA beats")


BOXES, WHY = [], []
if KEY == "9x16":
    for a, b in B["cta"]:
        box, why = pill_box((a + b)/2)
        BOXES.append(box); WHY.append(why)
        print(f"  pill {box}  {why}")
else:
    box, why = pill_box16(B["cta"])
    BOXES = [box for _ in B["cta"]]; WHY = [dict(why) for _ in B["cta"]]
    print(f"  16:9 pill, one geometry for both beats: {box}")
if KEY == "16x9":
    # caption clearance: the burned caption is one centred line; it must not touch the pill
    cs = json.load(open(f"cap_{KEY}/caption_states.json"))["states"] if \
        os.path.exists(f"cap_{KEY}/caption_states.json") else []
    worst = None
    for bi, (a, b) in enumerate(B["cta"]):
        for s in cs:
            if s["beat"][1] <= a or s["beat"][0] >= b: continue
            w = text_size(s["line"], font(A.CAP_SIZE, "ExtraBold"))[0]
            gap = (A.VW - w)//2 - BOXES[bi][2]
            if worst is None or gap < worst[0]: worst = (gap, s["line"], round(s["beat"][0], 2))
    print(f"  caption clearance: nearest caption ink starts {worst[0]} px right of the pill "
          f"({worst[1]!r} at {worst[2]}s)" if worst else "  no caption during the CTA beats")
    for w_ in WHY: w_["caption_clearance_px"] = None if not worst else worst[0]
x0, y0, x1, y1 = BOXES[0]


def pill(p, box=None, out_p=1.0):
    """out_p: 1.0 while the pill holds, ramping to 0 over the exit."""
    global x0, y0, x1, y1
    if box: x0, y0, x1, y1 = box
    im = Image.new("RGBA", A.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = ml.ease_out_back(min(p/0.30, 1.0)) if p < 0.30 else 1.0
    h = (y1-y0); w = (x1-x0)
    hh = int(h*(0.90+0.10*k)); ww = int(w*(0.94+0.06*k))
    cx, cy = (x0+x1)//2, (y0+y1)//2
    bx = [cx-ww//2, cy-hh//2, cx+ww//2, cy+hh//2]
    al = int(255*min(p/0.18, 1.0)*max(0.0, min(1.0, out_p)))
    d.rounded_rectangle(bx, radius=20, fill=(13, 14, 11, al))
    d.rounded_rectangle(bx, radius=20, outline=OLIVE + (al,), width=4)
    if KEY == "9x16":
        dy = 22
        d.text((cx, cy-dy), CTA_TEXT, font=fB, fill=(255, 255, 255, al), anchor="mm")
        d.text((cx, cy+dy+4), CTA_URL, font=fU, fill=OLIVE + (al,), anchor="mm")
    else:
        yy = cy - TH/2.0
        for (txt, f, col), lh in zip(LINES, LINE_H):
            if col == "o": yy += 8
            d.text((cx, yy + lh/2.0), txt, font=f, anchor="mm",
                   fill=(OLIVE + (al,)) if col == "o" else (255, 255, 255, al))
            yy += lh
    return im


# ⚠ NEVER REUSE A CACHED FRAME ACROSS A PARAMETER CHANGE: every name carries its own geometry and
# the cache is cleared every run.
import shutil as _sh
_sh.rmtree(f"{OUT}/png", ignore_errors=True)
blank = f"{OUT}/_blank.png"
Image.new("RGBA", A.size, (0, 0, 0, 0)).save(blank)
frames, t, entries = [], 0.0, []
os.makedirs(f"{OUT}/png", exist_ok=True)
for bi, (a, b) in enumerate(B["cta"]):
    x0, y0, x1, y1 = BOXES[bi]
    if a - t > 1e-6: entries.append((blank, a-t)); t = a
    n = L.nf(b-a)
    OUT_F = 6                                   # the exit matches the entry
    for i in range(n):
        p = i/L.FPS
        op = 1.0 if i < n-OUT_F else (n-1-i)/float(OUT_F)
        tag = f"{x0}_{y0}_{x1}_{y1}"
        hold = f"{OUT}/png/hold_{tag}.png"
        if p < 0.34 or op < 1.0:
            pth = f"{OUT}/png/b{bi}_{tag}_{i:04d}.png"
            pill(p, out_p=op).save(pth)
        else:
            if not os.path.exists(hold): pill(1.0).save(hold)
            pth = hold
        entries.append((pth, 1/L.FPS))
    t = b
if B["total"] - t > 1e-6: entries.append((blank, B["total"]-t))
with open(f"{OUT}/list.txt", "w") as f:
    for p, d in entries:
        f.write(f"file '{os.path.abspath(p)}'\nduration {d:.5f}\n")
    f.write(f"file '{os.path.abspath(entries[-1][0])}'\n")
subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", f"{OUT}/list.txt", "-r", "30000/1001", "-c:v", "qtrle", "-pix_fmt", "argb",
                f"{OUT}/cta.mov"], check=True)
# ⚠ ALSO WRITE ONE MOV PER BEAT: the shared watch pass samples a declared graphic's MOV at
# (t - beat_start) INTO THE FILE, so a full-timeline overlay reads as transparent.
beat_movs = []
for bi, (a, b) in enumerate(B["cta"]):
    f0, f1 = int(round(a/L.FD)), int(round(b/L.FD))
    sub = f"{OUT}/cta_b{bi}.mov"
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-i", f"{OUT}/cta.mov",
                    "-vf", f"select='between(n\\,{f0}\\,{f1-1})',setpts=PTS-STARTPTS",
                    "-frames:v", str(f1-f0), "-c:v", "qtrle", "-pix_fmt", "argb", sub], check=True)
    beat_movs.append(os.path.abspath(sub))
    print(f"  beat {bi}: frames {f0}-{f1-1} -> {sub}")
json.dump({"box": list(BOXES[0]), "boxes": [list(b) for b in BOXES], "placement": WHY,
           "pill_size": [PILL_W, PILL_H], "beats": B["cta"],
           "mov": os.path.abspath(f"{OUT}/cta.mov"), "beat_movs": beat_movs},
          open(f"{OUT}/cta.json", "w"), indent=1)
print(f"{KEY}: CTA pill {PILL_W}x{PILL_H} at {B['cta']} -> {OUT}/cta.mov")
