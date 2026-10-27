#!/usr/bin/env python3
"""DS-06 A-r2 (Dan, 2026-10-27): "move the poster ... up slightly". Codex redrew the body types (ds06-A-r2.png) but
left the poster in place, so this moves it locally. Dan's pixels are kept exactly (person mask on top); the vacated
wall is refilled from a smooth fit of the surrounding wall. Writes ds06-A-r2-moved.png."""
from pathlib import Path
from PIL import Image
import numpy as np, subprocess, tempfile
ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT/'Short-form video content/covers/review/muhammad-batch-b-20261026/sources'
PM = Path.home()/'.cache/absbyai/personmask/personmask'
UP = 100                        # 6% of the 1672 px plate
X0, X1, Y0, Y1 = 468, 936, 612, 1012   # poster with its left and bottom edge shadows
PX0, PX1, PY0, PY1 = 482, 929, 621, 990  # the paper itself (measured from brightness profiles)
im = np.array(Image.open(SRC/'ds06-A-r2.png').convert('RGB')).astype(float)
H, W, _ = im.shape
with tempfile.TemporaryDirectory() as t:
    Image.fromarray(im.astype(np.uint8)).save(f'{t}/i.png')
    subprocess.run([str(PM), f'{t}/i.png', f'{t}/m.png'], check=True, capture_output=True)
    person = np.array(Image.open(f'{t}/m.png').convert('L').resize((W, H))).astype(float)/255
from scipy.ndimage import binary_dilation
hard = binary_dilation(person > 0.2, iterations=6)
yy, xx = np.mgrid[0:H, 0:W]
def feats(x, y):
    x = x/W; y = y/H; return np.stack([np.ones_like(x), x, y, x*x, x*y, y*y], -1)
def surface(sample, where):
    """Quadratic colour surface fitted on `sample` pixels, evaluated on `where`."""
    A = feats(xx[sample], yy[sample]); F = feats(xx[where], yy[where])
    return np.stack([F @ np.linalg.lstsq(A, im[sample][:, c], rcond=None)[0] for c in range(3)], -1)
# wall: a ring around old and new poster positions, never the person or the poster
ring = np.zeros((H, W), bool); ring[Y0-UP-60:Y1+40, X0-40:W] = True; ring[Y0-UP:Y1, X0:X1] = False; ring &= ~hard
area = np.zeros((H, W), bool); area[Y0-UP:Y1, X0:X1] = True
out = im.copy(); out[area] = surface(ring, area) + np.random.default_rng(0).normal(0, 1.0, (area.sum(), 3))
wall = out.copy()
# paper: plain paper pixels (not silhouettes, not Dan)
paper = np.zeros((H, W), bool); paper[PY0+4:PY1-4, PX0+4:PX1-4] = True
plain = paper & ~hard & (im.mean(-1) > 200)
inpaper = np.zeros((H, W), bool); inpaper[PY0:PY1, PX0:PX1] = True
paperfit = np.zeros_like(im); paperfit[inpaper] = surface(plain, inpaper)
# the moved poster: original pixels, and behind Dan rebuilt paper (inside the paper) or wall (outside it)
patch = im[Y0:Y1, X0:X1].copy(); occ = hard[Y0:Y1, X0:X1]
rebuilt_paper = paperfit[Y0:Y1, X0:X1]; ip = inpaper[Y0:Y1, X0:X1]
patch[occ & ip] = rebuilt_paper[occ & ip]
dest_wall = wall[Y0-UP:Y1-UP, X0:X1]
patch[occ & ~ip] = dest_wall[occ & ~ip]
out[Y0-UP:Y1-UP, X0:X1] = patch
a = person[..., None]
out = out*(1-a) + im*a
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(SRC/'ds06-A-r2-moved.png')
print('occluded patch px', int(occ.sum()), 'saved')
