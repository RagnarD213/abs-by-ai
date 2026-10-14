#!/usr/bin/env python3
"""RA-07 round 2: the three phone cards MOVING (round 1 showed them as stills; s63_stills.py / s63_cards07.py drew them).

  python3 s83_phone07.py [P1 K1 W1]   -> round2/cards/<ID>.mp4 + round2/cards/cards.json

P1  14.95 "in seconds. An image of yourself with abs"   the approved self-generation demo (Ad 14 R3 g17) at 1.0x from demo
    2.00 s: the options screen, the tap, "Rendering your goal image" over his photo (chip "Real picture of me. Not
    AI-generated." while his photo is on the phone), then from just before "An image" his goal picture full card, AI-GENERATED,
    slow push. The crop screen (demo 0-1.30 s) is never shown.
K1  17.05 "on your lock screen motivates you."   the goal picture as the phone's lock screen (s63_cards07.lock_screen), with a
    slow supersampled push so it is never a frozen frame.
W1  27.53 "And when you have a program designed to build the body you want,"   the real AI Trainer recording B0034 at 1.0x from
    3.00 s: Monday's list, then the Goblet Squat sheet opens and its demo video plays.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra07")
import ra01lib as L
import s63_stills as S63
import s63_cards07 as C07
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B

FPS = L.FPS; W, H = 1080, 1920
OUT = "round2/cards"; os.makedirs(OUT, exist_ok=True)
PL = json.load(open(os.environ.get("PLAN", "beats_r2.json")))
CB = {c["name"]: c for c in PL["cards"]}
WD = {w["w"]: w for w in []}
REAL = "Real picture of me. Not AI-generated."
WORDS = json.load(open("words_aligned.json"))["words"]


def word_after(word, t0):
    return next(w["t"] for w in WORDS if w["t"] >= t0 - 0.01 and w["w"].strip(".,?!").lower() == word)


def frames_of(path, crop=None, t0=0.0, n=None, size=None):
    vf = ("crop=%d:%d:%d:%d," % crop if crop else "") + "scale=in_color_matrix=bt709:in_range=tv"
    w, h = (crop[0], crop[1]) if crop else size
    raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{t0:.4f}", "-i", path, "-frames:v", str(n), "-vf", vf,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    assert len(a) == n, (path, len(a), n)
    return a


def push(im, k, n, amp=0.025):
    """slow supersampled push-in: scale 1.0 -> 1+amp over the card, float box (no integer jitter)"""
    s = 1.0 + amp * k / max(1, n - 1)
    cw, ch = W / s, H / s
    return im.resize((W, H), Image.LANCZOS, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))


def p1():
    c = CB["P1"]; n = c["frames"]; a = c["beat"][0]
    nph = int(round((word_after("an", a) - 0.06 - a) * FPS))     # the phone until just before "An image of yourself"
    D0 = 60                                                       # demo 2.00 s: options scrolled to Generate
    dw, dh = S63.DISP[2] // 2 * 2, S63.DISP[3] // 2 * 2
    scr = frames_of(S63.DEMO, (dw, dh, S63.DISP[0], S63.DISP[1]), t0=(D0 - 0.5) / FPS, n=nph)
    out, log = [], []
    for i in range(nph):
        df = D0 + i; chip = REAL if df >= 78 else None
        im, box = S63.phone_card(a + i / FPS, Image.fromarray(S63.square_corners(scr[i])), chip=chip)
        out.append(im); log.append(dict(f=i, demo_frame=df, chip=chip))
    for i in range(nph, n):
        out.append(B.scene_photo(1.0 + (i - nph) / FPS, W, H, S63.GOAL, "AI-GENERATED").convert("RGB"))
        log.append(dict(f=i, what="result card", chip="AI-GENERATED"))
    L.encode_h264(iter(out), f"{OUT}/P1.mp4", (W, H), crf=15)
    return dict(id="P1", a=a, n=n, phone_frames=nph, phone_box=box, demo=S63.DEMO, demo_in=D0, log=log)


def k1():
    c = CB["K1"]; n = c["frames"]; a = c["beat"][0]
    base, box = C07.lock_screen(1.0)
    out = [push(base, k, n) for k in range(n)]
    L.encode_h264(iter(out), f"{OUT}/K1.mp4", (W, H), crf=15)
    return dict(id="K1", a=a, n=n, phone_box=box, what="lock screen, 2.5 % push")


def w1():
    c = CB["W1"]; n = c["frames"]; a = c["beat"][0]
    T0 = 3.00
    scr = frames_of(C07.B0034, t0=T0, n=n, size=(780, 1476))
    out = []
    for i in range(n):
        im, box = S63.phone_card(a + i / FPS, Image.fromarray(scr[i]))
        out.append(im)
    L.encode_h264(iter(out), f"{OUT}/W1.mp4", (W, H), crf=15)
    return dict(id="W1", a=a, n=n, phone_box=box, src=C07.B0034, src_in=T0)


if __name__ == "__main__":
    want = set(sys.argv[1:]) or {"P1", "K1", "W1"}
    meta = json.load(open(f"{OUT}/cards.json")) if os.path.exists(f"{OUT}/cards.json") else {}
    for k, f in (("P1", p1), ("K1", k1), ("W1", w1)):
        if k in want:
            m = f(); meta[m["id"]] = m; print("wrote", m["id"], m["n"], "frames", flush=True)
    json.dump(meta, open(f"{OUT}/cards.json", "w"), indent=1, default=str)
