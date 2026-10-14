#!/usr/bin/env python3
"""RA-14 round 3: the two phone cards MOVING (the round 1 stills were s63_stills.py; same shell, same field, same chips).

  python3 s83_phone.py   -> round3/cards/P1.mp4 (101 f, 14.18-17.55 s)  round3/cards/T1.mp4 (145 f, 33.43-38.27 s)  + cards.json

P1, the approved self-generation demo (Ad 14 R3 g17, approved for reuse 2026-09-17), at 1.0x:
    14.18 "and generate an image..."   demo 2.00-3.57 s: the options screen scrolled to Generate (no photo on it, no chip), the
                                       tap, then "Mapping muscle groups" / "Rendering your goal image" over his photo, with
                                       "Real picture of me. Not AI-generated." for as long as his photo is on the phone
    15.78 just before "dream body"     the result: his AI goal picture full card, AI-GENERATED, slow push, through "It takes seconds"
    The crop screen (demo 0-1.30 s) is never shown (ad-edit lesson 15).
T1, the approved app tour B0544 (approved for reuse 2026-10-10), at 1.0x:
    33.43 "Whatever problem comes up"   tour 2.00-4.73 s: the meal photo, Analyze, the 775 cal breakdown
    36.16 "A home workout"              tour 5.95-8.06 s: the AI Trainer's Push-Up demo (its own AI-GENERATED chip)
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
import s63_stills as S63
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

FPS = L.FPS; W, H = 1080, 1920
OUT = "round3/cards"; os.makedirs(OUT, exist_ok=True)
PL = json.load(open(os.environ.get("PLAN", "beats_r3.json")))
CB = {c["name"]: c for c in PL["cards"]}
REAL = "Real picture of me. Not AI-generated."


def frames_of(path, crop=None, t0=0.0, n=None):
    vf = ("crop=%d:%d:%d:%d," % crop if crop else "") + "scale=in_color_matrix=bt709:in_range=tv"
    w, h = (crop[0], crop[1]) if crop else (432, 920)
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{t0:.4f}", "-i", path, "-frames:v", str(n), "-vf", vf,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    assert len(a) == n, (path, len(a), n)
    return a


def p1():
    c = CB["P1"]; n = c["frames"]; a = c["beat"][0]
    nph = int(round((15.78 - a) * FPS))                         # the phone until just before "dream body"
    D0 = 60                                                      # demo frame 60 (2.00 s): options scrolled to Generate
    dw, dh = S63.DISP[2] // 2 * 2, S63.DISP[3] // 2 * 2         # yuv420 crops come back even-sized (434x941 -> 434x940)
    scr = frames_of(S63.DEMO, (dw, dh, S63.DISP[0], S63.DISP[1]), t0=(D0 - 0.5) / FPS, n=nph)
    log, out = [], []
    for i in range(nph):
        df = D0 + i
        chip = REAL if df >= 78 else None                       # his photo is on screen from demo frame 78 (2.60 s)
        im, box = S63.phone_card(a + i / FPS, Image.fromarray(S63.square_corners(scr[i])), chip=chip)
        out.append(im); log.append(dict(f=i, demo_frame=df, chip=chip))
    for i in range(nph, n):
        t = a + i / FPS
        im = B.scene_photo(1.0 + (i - nph) / FPS, W, H, S63.GOAL, "AI-GENERATED").convert("RGB")
        out.append(im); log.append(dict(f=i, what="result card", chip="AI-GENERATED"))
    L.encode_h264(iter(out), f"{OUT}/P1.mp4", (W, H), crf=15)
    return dict(id="P1", a=a, n=n, phone_frames=nph, phone_box=box, demo=S63.DEMO, demo_in=D0, log=log)


def t1():
    c = CB["T1"]; n = c["frames"]; a = c["beat"][0]
    n1 = int(round((36.16 - 0.03 - a) * FPS))                   # calorie tracking until "A home workout"
    s1 = frames_of(S63.TOUR, t0=(60 - 0.5) / FPS, n=n1)          # tour 2.00 s
    s2 = frames_of(S63.TOUR, t0=(178 - 0.5) / FPS, n=n - n1)     # tour 5.94 s, the Push-Up demo opens at 6.00
    out, log = [], []
    for i in range(n):
        scr = s1[i] if i < n1 else s2[i - n1]
        im, box = S63.phone_card(a + i / FPS, Image.fromarray(scr))
        out.append(im); log.append(dict(f=i, tour_frame=(60 + i) if i < n1 else (178 + i - n1)))
    L.encode_h264(iter(out), f"{OUT}/T1.mp4", (W, H), crf=15)
    return dict(id="T1", a=a, n=n, cut_at=n1, phone_box=box, tour=S63.TOUR, log=log)


if __name__ == "__main__":
    meta = {}
    for f in (p1, t1):
        m = f(); meta[m["id"]] = m; print("wrote", m["id"], m["n"], "frames")
    json.dump(meta, open(f"{OUT}/cards.json", "w"), indent=1, default=str)
