import os
import numpy as np
from PIL import Image

SC = os.path.dirname(os.path.abspath(__file__))
SHOT = os.path.join(SC, "shots", "01-pool-raw.png")   # real pool-guy reveal (honest 20-24%->9%)
AFTER = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/example pictures/dan by pool.png"
OUT = os.path.join(SC, "shots", "01-the-reveal-final.png")

X0, Y0, X1, Y1 = 695, 774, 1231, 1464   # AFTER panel (known-good bounds)
W, H = X1 - X0, Y1 - Y0

base = Image.open(SHOT).convert("RGB")
arr = np.asarray(base).astype(int)
bg = np.array([244, 243, 239])
panel = arr[Y0:Y1, X0:X1]
is_bg = (np.abs(panel - bg).sum(axis=2) < 24)
radius = next((y for y in range(H) if not is_bg[y, 0]), 1) or 1

yy, xx = np.mgrid[0:H, 0:W]
outside = np.zeros((H, W), dtype=bool)
for cy, cx in ((radius, radius), (radius, W - 1 - radius),
               (H - 1 - radius, radius), (H - 1 - radius, W - 1 - radius)):
    in_box = ((yy < radius) | (yy > H - 1 - radius)) & ((xx < radius) | (xx > W - 1 - radius))
    near = ((yy - cy) ** 2 + (xx - cx) ** 2) > radius ** 2
    quad = (np.abs(yy - cy) <= radius) & (np.abs(xx - cx) <= radius)
    outside |= in_box & near & quad

new = Image.open(AFTER).convert("RGB")
sa = W / H
ia = new.width / new.height
if ia > sa:
    nw = int(new.height * sa); left = (new.width - nw) // 2
    new = new.crop((left, 0, left + nw, new.height))
else:
    nh = int(new.width / sa); new = new.crop((0, 0, new.width, nh))
new = new.resize((W, H), Image.LANCZOS)

arr[Y0:Y1, X0:X1] = np.where(outside[:, :, None], panel, np.asarray(new).astype(int))
Image.fromarray(arr.astype(np.uint8)).save(OUT, "PNG")
print("wrote", OUT, "radius", radius)
