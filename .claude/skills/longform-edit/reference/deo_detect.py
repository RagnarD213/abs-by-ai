#!/usr/bin/env python3
"""Find the ARMS-SPREAD shots - the only ones where the underarm is on screen,
and therefore the only ones where the deodorant residue is visible at all.

Why not use the handoff's weight function as the locator: it is the FILTER, and
it only discriminates INSIDE a tight armpit box. Measured over any wider region
it fires on the doorway wood (sat 0.19) and the wall (sat 0.42) too, and scoring
its mass inside a tight box does not separate arms-up from arms-down either
(arms-down 300.0s scored L 2444 / R 3680 against arms-spread 14.0s L 2925 /
R 2933). What DOES separate them is bare forearm skin reaching the outer thirds
of the frame: 0.199-0.223 arms-spread vs 0.010-0.011 arms-down, a 20x gap.
usage: deo_detect.py <video.mp4> <fps> [sheet]
"""
import subprocess, sys, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont

VID, FPS = sys.argv[1], float(sys.argv[2])
SHEET = len(sys.argv) > 3
X0, X1, Y0, Y1 = 120, 1810, 420, 700
Wd, Ht = X1 - X0, Y1 - Y0
THRESH = 0.06
cmd = ["ffmpeg","-nostdin","-v","error","-i",VID,"-vf",
       f"fps={FPS},crop={Wd}:{Ht}:{X0}:{Y0}","-f","rawvideo","-pix_fmt","rgb24","-"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)
fsz = Wd * Ht * 3
rows, t = [], 0.0
def skin(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(2); mn = a.min(2)
    sat = (mx - mn) / np.maximum(mx, 1.0); val = mx / 255.0
    return ((sat > 0.52) & (sat < 0.88) & (val > 0.35) & (r > g) & (g > b)).mean()
while True:
    buf = p.stdout.read(fsz)
    if len(buf) < fsz: break
    a = np.frombuffer(buf, np.uint8).reshape(Ht, Wd, 3).astype(np.float32)
    L = skin(a[:, :310])            # x  120- 430
    R = skin(a[:, 1380:])           # x 1500-1810
    rows.append((round(t, 2), float(L), float(R)))
    t += 1.0 / FPS
p.wait()
def mmss(x): return f"{int(x//60)}:{x%60:05.2f}"
hits = [r for r in rows if max(r[1], r[2]) > THRESH]
runs = []
for r in hits:
    if runs and r[0] - runs[-1][-1][0] <= 1.5: runs[-1].append(r)
    else: runs.append([r])
runs = [r for r in runs if r[-1][0] - r[0][0] >= 0.4]
print(f"scanned {len(rows)} frames at {FPS} fps; {len(hits)} arms-spread frames in {len(runs)} runs\n")
tot = 0
for run in runs:
    a, b = run[0][0], run[-1][0] + 1.0/FPS
    tot += b - a
    print(f"  {mmss(a):>9s} - {mmss(b):>9s}  ({b-a:5.2f}s)  peak {max(max(x[1],x[2]) for x in run):.3f}")
print(f"\n{tot:.1f}s of arms-spread footage out of {rows[-1][0]:.0f}s ({100*tot/rows[-1][0]:.1f}%)")
if SHEET and runs:
    picks = [run[len(run)//2][0] for run in runs][:24]
    ims = []
    for tt in picks:
        o = subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",f"{tt:.2f}","-i",VID,
            "-frames:v","1","-vf","crop=900:260:520:600,scale=450:130","-f","image2pipe",
            "-vcodec","png","-"], capture_output=True)
        ims.append((tt, Image.open(io.BytesIO(o.stdout)).convert("RGB")))
    cols = 3; rowsn = (len(ims)+cols-1)//cols
    sh = Image.new("RGB", (450*cols, 130*rowsn), (20,20,20))
    f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 15)
    for i,(tt,m) in enumerate(ims):
        sh.paste(m, (450*(i%cols), 130*(i//cols)))
        ImageDraw.Draw(sh).text((450*(i%cols)+4, 130*(i//cols)+4), mmss(tt), font=f, fill=(255,230,0))
    sh.save("/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/dae62b2c-e3c9-48e6-8e67-6badf48f7e80/scratchpad/DEO_SHEET.png")
    print("wrote DEO_SHEET.png")
