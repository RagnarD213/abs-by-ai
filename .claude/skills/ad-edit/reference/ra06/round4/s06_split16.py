#!/usr/bin/env python3
"""RA-06 round 4: the 16:9 opener split screen, from the 9:16 Dan approved (cards_9x16/split.json: same rolls, in-points, looks, labels).
Three stacked 16:9 panels do not fit a 16:9 frame, so the layout follows the subjects' own shapes:
  left   Stomach Vacuum (standing, a tall subject): one 1072x860 panel, the 9:16's crop widened to the panel's shape
  right  Spiderman Plank and Toe Touches (lying, wide subjects): two 744x418 16:9 panels, the 9:16's exact crops
Every panel ends at y 900 so the captions (ink from y 930) sit on the field, never on a panel (RA-06 lesson 8's problem in 9:16).
Writes cards_16x9/split.mp4 (exactly the plan's frame count) and cards_16x9/split.json."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH)
import ra01lib as L, softblue as SB
R = "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera"
S9 = json.load(open("cards_9x16/split.json")); P9 = {p["roll"]: p for p in S9["panels"]}
N = S9["frames"]; B = json.load(open("beats.json"))
assert N == {c["name"]: c for c in B["cards"]}["split"]["frames"]
HOLD = json.load(open("round4/r4_16x9_overrides.json"))["split_hold_frames"]; N += HOLD   # ROUND 4: see that file
W, H, M, GAP, TOP, BOT = 1920, 1080, 40, 24, 40, 900
RW, RH = 744, 418                                   # right column: two 16:9 panels, 418 + 24 + 418 = 860
LW, LH = W - 2*M - GAP - RW, BOT - TOP              # left: 1072 x 860
assert 2*RH + GAP == LH and LW == 1072
# the vacuum panel: the 9:16 crop's height (hair room above, captions never reach it here) at the left panel's shape, centred on him
vw = int(round(P9["C1677"]["crop"][1] * LW / LH)) // 2 * 2; vx = 1262
PANELS = [  # roll, crop (w, h, x, y) in the 3840x2160 frame, panel box, label, anchor
 ("C1677", (vw, P9["C1677"]["crop"][1], vx, P9["C1677"]["crop"][3]), (M, TOP, LW, LH), "Stomach Vacuum", "rt"),
 ("C1683", tuple(P9["C1683"]["crop"]), (M + LW + GAP, TOP, RW, RH), "Spiderman Plank", "rt"),
 ("C1682", tuple(P9["C1682"]["crop"]), (M + LW + GAP, TOP + RH + GAP, RW, RH), "Toe Touches", "lt"),
]
assert vx + vw <= 3840
SLUT = json.load(open("/Volumes/Extreme/_edit_work/ra06/round3/split/split_luts.json"))

def frames(roll, crop, pw, ph):
    w, h, x, y = crop
    vf = f"crop={w}:{h}:{x}:{y},{L.DECODE},{SLUT[roll]['filter']},scale={pw}:{ph}:flags=lanczos,format=rgb24"
    p = subprocess.Popen([L.FF, "-nostdin", "-v", "error", "-ss", f"{P9[roll]['t0']:.3f}", "-i", f"{R}/{roll}.MP4", "-vf", vf,
                          "-frames:v", str(N), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    out = []
    for _ in range(N):
        b = p.stdout.read(pw*ph*3); assert len(b) == pw*ph*3, roll
        out.append(Image.frombytes("RGB", (pw, ph), b))
    p.wait(); return out

src = [frames(r, c, bx[2], bx[3]) for r, c, bx, _l, _a in PANELS]
u = SB.unit(W, H); RAD = round(15*u); ul = 1.7      # label unit: 68 px chips on 418 px panels (the 9:16 had 80 on 580)
masks = []
for _r, _c, (x, y, pw, ph), _l, _a in PANELS:
    m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw-1, ph-1), RAD, fill=255); masks.append(m)
os.makedirs("cards_16x9", exist_ok=True)
enc = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                        "-framerate", "30000/1001", "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-r", "30000/1001", "-colorspace", "bt709",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                        "-x264-params", "keyint=30:min-keyint=1:scenecut=0", "cards_16x9/split.mp4"], stdin=subprocess.PIPE)
boxes = []
os.makedirs("round4/look", exist_ok=True)
for i in range(N):
    t = i*1001/30000
    im = SB.field(t, W, H)
    for k, (r, c, (x, y, pw, ph), lab, anc) in enumerate(PANELS):
        im.paste(src[k][i], (x, y), masks[k])
        SB.rr(im, (x, y, x+pw, y+ph), None, RAD, SB.GLASS_LINE, u/2)
        b = SB.disclosure(im, lab, ((x + 14*ul) if anc == "lt" else (x + pw - 14*ul), y + 14*ul), ul, anchor=anc, size=24)
        if i == 0: boxes.append([round(v) for v in b])
    enc.stdin.write(np.asarray(im).tobytes())
    if i in (0, N//2, N-1): im.save(f"round4/look/split16_f{i:03d}.png")
enc.stdin.close(); assert enc.wait() == 0
json.dump({"panels": [dict(roll=r, t0=P9[r]["t0"], crop=list(c), box=list(bx), label=l, anchor=a) for r, c, bx, l, a in PANELS],
           "label_boxes": boxes, "frames": N, "card_bottom": BOT}, open("cards_16x9/split.json", "w"), indent=1)
print("split16", N, "frames; panels", [p[2] for p in PANELS], "labels", boxes)
