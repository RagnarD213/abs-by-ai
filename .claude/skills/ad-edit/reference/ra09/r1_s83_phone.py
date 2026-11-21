#!/usr/bin/env python3
"""RA-14 round 3: the two phone cards MOVING (the round 1 stills were s63_stills.py; same shell, same field, same chips).

  python3 s83_phone.py   -> r1/cards/P1.mp4 (101 f, 14.18-17.55 s)  r1/cards/T1.mp4 (145 f, 33.43-38.27 s)  + cards.json

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
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RA-09")
import ra01lib as L
import s63_stills as S63
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

FPS = L.FPS; W, H = 1080, 1920
OUT = "r1/cards"; os.makedirs(OUT, exist_ok=True)
PL = json.load(open(os.environ.get("PLAN", "beats.json")))
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


B0550 = ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/screen-recordings/"
         "B0550_app-generate-goal-image-heavier-white-man-lake-dock_1320x2868_42s.mp4")
PGOAL = "/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg"   # the prospect's AI goal picture = B0550's result
SRC0 = 22            # B0550 frame (60 fps): the options with "Generate my goal image"; the tap lands about frame 40, the scan runs from 44
WIN = (1320, 2502, 0, 366)   # the phone screen's 0.5275 shape out of the 1320x2868 recording, bottom-aligned: options, button and scan card


def p1():
    # ROUND 2 (Dan, 2026-10-17: "Use one of the white guys that we made instead of me for the generation ... Use it for everything"):
    # the prospect's REAL absbyai.com generation (B0550, RA-04 R5) at 1.0x from "you can generate" until just before "with ripped
    # six-pack abs": the Generate button, the tap, "Analyzing your photo" with the scan over his photo. His before photo is
    # AI-generated: AI-GENERATED under the phone from the frame it appears. Then his AI goal picture, full card, AI-GENERATED, push.
    c = CB["P1"]; n = c["frames"]; a = c["beat"][0]
    e_with = next(w["t"] for w in json.load(open("words_aligned.json"))["words"] if w["t"] > a and w["w"].strip().lower() == "with")
    nph = min(int(round((e_with - 0.20 - a) * FPS)), 33)
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{(SRC0 - 0.5) / 60:.4f}", "-i", B0550, "-vf",
                          "fps=30000/1001,crop=%d:%d:%d:%d,scale=in_color_matrix=bt709:in_range=tv" % WIN,
                          "-frames:v", str(nph), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    scr = np.frombuffer(raw, np.uint8).reshape(-1, WIN[1], WIN[0], 3); assert len(scr) == nph, (len(scr), nph)
    log, out = [], []
    for i in range(nph):
        sf = SRC0 + i * 60 / FPS                                # B0550 frame on screen
        chip = "AI-GENERATED" if sf >= 39 else None              # his (AI-generated) before photo is on screen from B0550 frame 41 (judge: 1 frame unlabelled at 44); one frame early for seek rounding
        im, box = S63.phone_card(a + i / FPS, Image.fromarray(S63.square_corners(scr[i])), chip=chip)
        out.append(im); log.append(dict(f=i, b0550_frame=round(sf, 1), chip=chip))
    for i in range(nph, n):
        im = B.scene_photo(1.0 + 2 * (i - nph) / FPS, W, H, PGOAL, "AI-GENERATED").convert("RGB")
        out.append(im); log.append(dict(f=i, what="result card", chip="AI-GENERATED"))
    L.encode_h264(iter(out), f"{OUT}/P1.mp4", (W, H), crf=15)
    return dict(id="P1", a=a, n=n, phone_frames=nph, phone_box=box, demo=B0550, demo_in=SRC0, demo_fps=60, window=WIN, log=log)


def t1():
    # RA-12: "personalized workout" -> the AI Trainer: tour 5.74 s (frame 172, the tap on AI Trainer) into the Push-Up demo, to 8.04 s;
    # "and nutrition plan" -> the Macro Tracker: tour 1.40 s (frame 42, just before the tap) through the meal photo, Analyze and the
    # 775 cal breakdown, to 4.73 s. Never the Reverse Lunge switch at 8.25 s or the home screen return at 5.0 s.
    c = CB["T1"]; n = c["frames"]; a = c["beat"][0]
    t_nut = next(w["t"] for w in json.load(open("words_aligned.json"))["words"] if w["t"] > a and w["w"].strip().lower().startswith("nutrition"))
    n1 = int(round((t_nut - 0.05 - a) * FPS)); n2 = n - n1
    T0 = min(172, 242 - n1)            # start a few frames earlier on the home screen if the workout part needs them
    assert T0 >= 160, ("workout part too long for the tour", n1)
    assert 42 + n2 <= 142, ("meal part runs past the 775 cal result", n2)
    s1 = frames_of(S63.TOUR, t0=(T0 - 0.5) / FPS, n=n1)
    s2 = frames_of(S63.TOUR, t0=(42 - 0.5) / FPS, n=n2)
    out, log = [], []
    for i in range(n):
        scr = s1[i] if i < n1 else s2[i - n1]
        im, box = S63.phone_card(a + i / FPS, Image.fromarray(scr))
        out.append(im); log.append(dict(f=i, tour_frame=(T0 + i) if i < n1 else (42 + i - n1)))
    L.encode_h264(iter(out), f"{OUT}/T1.mp4", (W, H), crf=15)
    return dict(id="T1", a=a, n=n, cut_at=n1, phone_box=box, tour=S63.TOUR, log=log)


if __name__ == "__main__":
    meta = json.load(open(f"{OUT}/cards.json")) if os.path.exists(f"{OUT}/cards.json") else {}
    for f in ([p1, t1] if "--all" in sys.argv else [p1]):
        m = f(); meta[m["id"]] = m; print("wrote", m["id"], m["n"], "frames")
    json.dump(meta, open(f"{OUT}/cards.json", "w"), indent=1, default=str)
