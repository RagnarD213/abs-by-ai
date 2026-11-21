"""RA-04 round 3: does the leg press PLATFORM move with the plates and the feet? usage: platform04.py <tag> <frame> [<frame> ...]
Masked search: the platform rim (r2c_sled.py's platform outline, minus a 14 px band around the shoes) is cut from frame 0 and found in
frame k by brute-force shift over +-70 px (mean abs difference on the rim pixels only). The plates (sled circle) and the near shoe are
found the same way, so all three numbers come from one method. Rigid sled + feet on the platform = the three shifts agree and run along
the 45 degree rails (dx = -dy)."""
import sys, cv2, numpy as np
W = "/Volumes/Extreme/_edit_work/ra04"; tag = sys.argv[1]; ks = [int(x) for x in sys.argv[2:]]
f = lambda i: cv2.cvtColor(cv2.imread(f"{W}/round3/check/{tag}/f/{i:03d}.png"), cv2.COLOR_BGR2GRAY).astype(np.float32)
A = f(0); H, Wd = A.shape
plat = np.zeros((H, Wd), np.uint8); cv2.fillPoly(plat, [np.array([(501, 530), (550, 489), (557, 484), (572, 484), (580, 491), (747, 772), (655, 747), (630, 742)], np.int32)], 1)
plates = np.zeros_like(plat); cv2.circle(plates, (777, 641), 100, 1, -1)
shoes = np.zeros_like(plat); cv2.rectangle(shoes, (520, 520), (700, 715), 1, -1)       # START's shoes on the platform face (r2c_sled fill box)
rim = plat & (1 - cv2.dilate(shoes, np.ones((29, 29), np.uint8))) & (1 - plates)
rim_top = rim.copy(); rim_top[560:] = 0                                                  # the top corner only: the legs never cover it
shoe = np.zeros_like(plat); cv2.rectangle(shoe, (575, 545), (650, 600), 1, -1)
def find(mask, B, R=70):
    ys, xs = np.nonzero(mask); best = (1e9, 0, 0)
    for dy in range(-R, R+1):
        for dx in range(-R, R+1):
            y2, x2 = ys + dy, xs + dx; ok = (y2 >= 0) & (y2 < H) & (x2 >= 0) & (x2 < Wd)
            e = float(np.abs(B[y2[ok], x2[ok]] - A[ys[ok], xs[ok]]).mean())
            if e < best[0]: best = (e, dx, dy)
    return best
print("rim pixels", int(rim.sum()))
for k in ks:
    B = f(k); r = {n: find(m, B) for n, m in (("platform_rim", rim), ("platform_top", rim_top), ("plates", plates), ("near_shoe", shoe))}
    print(k, "  ".join(f"{n}: ({v[1]:+d},{v[2]:+d}) err {v[0]:.1f}" for n, v in r.items()))
