#!/usr/bin/env python3
"""What does the proposed full-bleed window actually contain, and does it slice a product?

Two things a talking-head crop can get wrong here:
  1. The window edge cutting THROUGH the AG1 bag's big printed logo - a sliced word at the
     frame edge reads as a mistake in a way a partly-visible bottle does not.
  2. His head sitting too high once the picture is dropped to y=310 for the title band.

Both measured off a real frame rather than estimated. The AG1 bag is found as the large
saturated GREEN region on the counter; its printed logo is the white ink inside it.
"""
import json, subprocess
import numpy as np, cv2
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/claude edited long form content/02 - My Honest Zepbound Update/CUT_v1_graded_NO-GRAPHICS.mp4"

p = subprocess.run([FF, '-nostdin', '-v', 'error', '-ss', '1060', '-i', SRC,
                    '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                   capture_output=True)
im = np.frombuffer(p.stdout, np.uint8).reshape(1080, 1920, 3).astype(np.int16)
r, g, b = im[..., 0], im[..., 1], im[..., 2]

green = (g > r + 18) & (g > b + 12) & (g > 55)
ys, xs = np.nonzero(green)
# keep the biggest connected blob
nl, lab, stats, _ = cv2.connectedComponentsWithStats(green.astype(np.uint8), 8)
k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
x0, y0, w, h, area = stats[k]
print(f"AG1 bag  x {x0/1920:.3f}-{(x0+w)/1920:.3f}  y {y0/1080:.3f}-{(y0+h)/1080:.3f}  area {area}")
# white ink inside the bag = the printed logo
sub = im[y0:y0+h, x0:x0+w]
ink = (sub[..., 0] > 175) & (sub[..., 1] > 185) & (sub[..., 2] > 175)
iy, ix = np.nonzero(ink)
if len(ix):
    print(f"AG1 logo x {(x0+ix.min())/1920:.3f}-{(x0+ix.max())/1920:.3f}")

# head top, from the Vision masks already collected for the two tightest beats
import glob
for beat in ('B-b46', 'E-b45'):
    tops = []
    for f in sorted(glob.glob(f'work/mk/{beat}/*.mask.png')):
        m = cv2.imread(f, cv2.IMREAD_GRAYSCALE) > 127
        yy = np.nonzero(m.any(1))[0]
        if len(yy): tops.append(yy.min() / m.shape[0])
    print(f"{beat} head top: source row {min(tops)*1080:.0f} "
          f"-> delivered y {310 + min(tops)*1610:.0f}  (title band ends at 310)")

for cen in (0.6676, 0.687, 0.6969):
    L = cen - (724/1920)/2; R = cen + (724/1920)/2
    print(f"window centre {cen:.4f}: x {L:.3f}-{R:.3f}")
