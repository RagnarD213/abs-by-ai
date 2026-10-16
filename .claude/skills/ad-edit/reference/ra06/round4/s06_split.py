#!/usr/bin/env python3
"""RA-06 opener: the script's cue "[SHOW SPLIT SCREEN OF DAN DOING THREE EXERCISES: TOE TOUCH, VACUUM, SPIDERMAN PLANK]".
Three 16:9 panels of Dan's own 8/28 pool B-roll stacked on the Soft Blue field, each with its exercise name, from frame 0.
  toe touches  C1682 (medicine-ball toe touches, the same pool and light as the talking roll)
  vacuum       C1677 (front-on stomach vacuum, library B0429's source range)
  spiderman    C1683 (Dan's spiderman plank: forearm plank up to a push-up and back, as he teaches it in short4_spiderman-planks)
Graded with the presenter's look (grade.json) plus a per-roll exposure trim, judged by eye beside the presenter
(look/split_panels.jpg). Writes cards_9x16/split.mp4, exactly the plan's frame count."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra06")
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH)
import ra01lib as L, softblue as SB
R = "/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera"
G = json.load(open("grade.json"))["filter"]
B = json.load(open("beats.json")); N = {c["name"]: c for c in B["cards"]}["split"]["frames"]
W, H, M, GAP = 1080, 1920, 24, 24
PW = W - 2*M; PH = round(PW*9/16); PH -= PH % 2
Y0 = (H - 3*PH - 2*GAP)//2
PANELS = [  # roll, in-point s, crop (w, h, x, y) in the 3840x2160 frame, exposure trim, label, label anchor
 # round 1 re-audit: the caption band (ink ~1420-1470) falls on the BOTTOM panel. Toe touches there put the words on the top of
 # his rep, so the order is spiderman / toe touches / vacuum: the words cross the vacuum panel's chest and pool, under his face; the vacuum crop puts Dan in the left third so the top-right label clears his hair; trims from body luma
 # measured on the panel (reviewer: toe 0.23 / plank 0.20 / vacuum 0.48 against 0.33 on the talking shots)
 ("C1683", float(os.environ.get("T3", "135.5")), (1920, 1080, 1066, 1000), "null", "Spiderman Plank", "rt"),
 ("C1682", float(os.environ.get("T1", "16.0")),  (2560, 1440, 1000, 560),  "null", "Toe Touches", "lt"),
 # ROUND 3: Dan, "make sure I'm actively doing the vacuum when you show, not just standing around": B0419's approved range
 # (C1677 @136.6 s). From 138.95 (reviews: from 137.75 the first 1.2 s was the exhale, from 138.35 0.6 s of standing) it opens on the draw-in and holds;
 # crop 2304x1296 gives his hair room (hair src 330-340, chin 550-575 across the window) under the panel edge while the captions stay below his chin.
 ("C1677", float(os.environ.get("T2", "138.95")), (2304, 1296, 1263, 279),  "null", "Stomach Vacuum", "rt"),
]
# ROUND 3: Dan, "This footage looks very dark": each roll gets its own C2 LUT at a higher exposure (round3/s06c_split_luts.py),
# replacing round 1's presenter LUT + gamma trims. Measured: his body skin 112 / 112 / 150 against 107-113 on the talking shots.
LABEL_DY = {"C1677": -6}   # ROUND 4: the gate measured the Stomach Vacuum label 19 px above the caption ink (needs 20)
SLUT = json.load(open("/Volumes/Extreme/_edit_work/ra06/round3/split/split_luts.json"))
def frames(roll, t0, crop, trim):
    w, h, x, y = crop
    vf = f"crop={w}:{h}:{x}:{y},{L.DECODE},{SLUT[roll]['filter']},{trim},scale={PW}:{PH}:flags=lanczos,format=rgb24"
    p = subprocess.Popen([L.FF, "-nostdin", "-v", "error", "-ss", f"{t0:.3f}", "-i", f"{R}/{roll}.MP4", "-vf", vf,
                          "-frames:v", str(N), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    out = []
    for _ in range(N):
        b = p.stdout.read(PW*PH*3); assert len(b) == PW*PH*3, roll
        out.append(Image.frombytes("RGB", (PW, PH), b))
    p.wait(); return out
src = [frames(r, t, c, g) for r, t, c, g, _, _a in PANELS]
u = SB.unit(W, H); RAD = round(15*u)
mask = Image.new("L", (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, PW-1, PH-1), RAD, fill=255)
os.makedirs("cards_9x16", exist_ok=True)
enc = subprocess.Popen([L.FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                        "-framerate", "30000/1001", "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-r", "30000/1001", "-colorspace", "bt709",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                        "-x264-params", "keyint=30:min-keyint=1:scenecut=0", "cards_9x16/split.mp4"], stdin=subprocess.PIPE)
boxes = []
for i in range(N):
    t = i*1001/30000
    im = SB.field(t, W, H)
    for k, (r, t0, c, g, lab, anc) in enumerate(PANELS):
        y = Y0 + k*(PH + GAP)
        im.paste(src[k][i], (M, y), mask)
        SB.rr(im, (M, y, M+PW, y+PH), None, RAD, SB.GLASS_LINE, u/2)
        b = SB.disclosure(im, lab, ((M + 14*u) if anc == "lt" else (M + PW - 14*u), y + 14*u + LABEL_DY.get(r, 0)), u, anchor=anc, size=24)
        if i == 0: boxes.append([round(v) for v in b])
    enc.stdin.write(np.asarray(im).tobytes())
    if i in (0, N//2, N-1): im.save(f"look/split_f{i:03d}.png")
enc.stdin.close(); assert enc.wait() == 0
json.dump({"panels": [dict(roll=r, t0=t, crop=c, trim=g, label=l, anchor=a) for r, t, c, g, l, a in PANELS], "panel_wh": [PW, PH],
           "y0": Y0, "label_boxes": boxes, "frames": N}, open("cards_9x16/split.json", "w"), indent=1)
print("split", N, "frames", PW, "x", PH, "panels at y", [Y0 + k*(PH+GAP) for k in range(3)])
