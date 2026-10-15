#!/usr/bin/env python3
"""RA-04 round 5: A0074 (a phone lying on dark marble, Dan's AI goal picture as its lock screen) with the screen picture replaced by
the white man's AI result from his real generation (round5/after_white_man.jpg), held still on the screen and tracked to the phone.

Built from RA-05's reference/ra05/round3/lockscreen.py (SIFT against frame 0, no chaining; RANSAC homography; corner smoothing), with
what RA-05's `ref` option could not do: a DIFFERENT picture is mapped straight onto frame 0's screen quad instead of being registered
to the old one by SIFT (handoff 2026-10-15, step 3).

  screen   frame 0's screen = the region inside the black bezel, flood-filled from the screen centre (so the notch and the rounded
           corners are excluded by construction); its quad = four lines fitted to the straight middle part of each side
  track    ECC homography against frame 0 on a high-passed band around the phone's edge (bezel, rim, marble), Gaussian-smoothed
           over time; Veo animates the old picture, so nothing inside the screen is tracked (see the track section for what failed)
  picture  cover-fit to the screen quad's shape (what a phone does with a 4:5 photo as wallpaper), centred on his torso
  glare    A0074 has a light sweep across the glass (about 1.7-2.6 s): the low-frequency positive luminance change of the screen
           against frame 0 (Gaussian sigma 35 px, so the old picture's own detail does not come through) is added back as light
  out      round5/lock_src.mp4, 1080x1920 at A0074's 24 fps, from A0074 0.5 s (the card's in-point), N frames

usage: python3 r5_lock.py [N]"""
import json, subprocess, sys
import numpy as np, cv2
from PIL import Image
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
P = json.load(open("/Volumes/Extreme/_edit_work/ra04/clip_paths.json"))
SRC, T0 = P["A0074"], 0.5
N = int(sys.argv[1]) if len(sys.argv) > 1 else 78
W, H = 1080, 1920
OUT = "/Volumes/Extreme/_edit_work/ra04/round5/lock_src.mp4"
PIC = "/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg"

p = subprocess.Popen([FF, "-v", "error", "-ss", f"{T0}", "-i", SRC, "-vf", "scale=in_color_matrix=bt709:out_color_matrix=bt709,format=rgb24",
                      "-frames:v", str(N), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
fr = []
for _ in range(N):
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    fr.append(np.frombuffer(b, np.uint8).reshape(H, W, 3).copy())
p.wait(); N = len(fr); assert N >= 75, N

# ---- the screen in every frame: inside the bezel ---------------------------------------------------------------------------------
def side_line(pts):
    vx, vy, x0, y0 = cv2.fitLine(pts.astype(np.float32), cv2.DIST_HUBER, 0, 0.01, 0.01).ravel(); return np.array([x0, y0]), np.array([vx, vy])
def inter(l1, l2):
    (p1, d1), (p2, d2) = l1, l2; A = np.array([d1, -d2]).T; t = np.linalg.solve(A, p2 - p1); return p1 + t[0] * d1
def outer(pts, axis, side):
    """the outermost contour point per row (axis 0) or column (axis 1): the fit follows the edge, never the picture"""
    d = {}
    for x, y in pts:
        k = int(round(y)) if axis == 0 else int(round(x)); v = x if axis == 0 else y
        if k not in d or (v < d[k] if side < 0 else v > d[k]): d[k] = v
    return np.array([[v, k] if axis == 0 else [k, v] for k, v in d.items()], np.float32)

def screen_of(f):
    """-> (quad TL TR BR BL, hull mask, notch mask). The hull bridges the notch and any dark spot in the old picture."""
    L = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
    dark = (cv2.GaussianBlur(L, (5, 5), 1) < 30).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ff = (1 - dark).copy()
    for sx, sy in ((540, 900), (540, 1150), (600, 700), (450, 1000), (700, 1000), (500, 600)):     # several seeds: one may sit on a dark pixel
        if ff[sy, sx] == 1: cv2.floodFill(ff, np.zeros((H + 2, W + 2), np.uint8), (sx, sy), 2)
    scr = cv2.morphologyEx((ff == 2).astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n_, lab, st, _ = cv2.connectedComponentsWithStats(scr); scr = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    cnts, _ = cv2.findContours(scr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull = cv2.convexHull(max(cnts, key=cv2.contourArea))
    hm = np.zeros((H, W), np.uint8); cv2.fillPoly(hm, [hull[:, 0, :]], 1)
    hc, _ = cv2.findContours(hm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); C = hc[0][:, 0, :].astype(np.float32)
    C = C[(C[:, 0] > 1) & (C[:, 0] < W - 2) & (C[:, 1] > 1) & (C[:, 1] < H - 2)]      # the frame edge is not the screen's edge
    xs, ys = C[:, 0], C[:, 1]; cx, cy = xs.mean(), ys.mean()
    mid = lambda v, lo, hi: (v > lo + 0.22 * (hi - lo)) & (v < lo + 0.78 * (hi - lo))
    y0_, y1_, x0_, x1_ = ys.min(), ys.max(), xs.min(), xs.max()
    Ll = side_line(outer(C[(xs < cx) & mid(ys, y0_, y1_)], 0, -1)); Lr = side_line(outer(C[(xs > cx) & mid(ys, y0_, y1_)], 0, 1))
    Lt = side_line(outer(C[(ys < cy) & mid(xs, x0_, x1_)], 1, -1)); Lb = side_line(outer(C[(ys > cy) & mid(xs, x0_, x1_)], 1, 1))
    quad = np.float32([inter(Lt, Ll), inter(Lt, Lr), inter(Lb, Lr), inter(Lb, Ll)])
    notch = ((dark > 0) & (hm > 0)).astype(np.uint8)
    n_, lab, st, _ = cv2.connectedComponentsWithStats(notch); keep = np.zeros_like(notch)
    for i in range(1, n_):
        x, y, w, h, a = st[i]
        if y < y0_ + 140 and a > 2000 and w > 150: keep[lab == i] = 1          # the notch: a wide dark blob on the top edge
    return quad, hm, keep

f0 = fr[0]
quad, hull0, _ = screen_of(f0)
# the notch, measured on frame 0 at 3x (round5/notch.jpg): x 523-800, bottom edge about y 266-270, rounded bottom corners. It is
# DRAWN BACK in solid notch black over the new picture, and the whole screen (notch area included) is replaced: finding it as "dark
# pixels on the top edge" let the old picture's trees through (first build), and keeping the old notch pixels under a slightly low
# drawn edge left a 4-7 px strip of the old trees along its bottom (independent review, round 5 take 2).
NX0, NX1, NY1, NR = 523, 800, 268, 28
DOT = (546, 580)                           # the front-camera dot's columns in frame 0 (bright in every glare frame)
NC0, NC1 = 230, 260                       # notch rows in frame 0: under the bezel edge, above the old picture's fringe
notch0 = np.zeros((H, W), np.uint8)
cv2.rectangle(notch0, (NX0, 100), (NX1, NY1 - NR), 1, -1); cv2.rectangle(notch0, (NX0 + NR, NY1 - NR), (NX1 - NR, NY1), 1, -1)
cv2.circle(notch0, (NX0 + NR, NY1 - NR), NR, 1, -1); cv2.circle(notch0, (NX1 - NR, NY1 - NR), NR, 1, -1)
notch0 &= hull0
screen0 = (hull0 > 0).astype(np.uint8)                                          # the whole screen, notch area included
NOTCH_RGB = np.median(f0[(cv2.erode(notch0, np.ones((15, 15), np.uint8)) > 0)], 0).astype(np.float32)   # the notch core's own black
print("screen area", int(screen0.sum()), "notch area", int(notch0.sum()), "quad", quad.round(1).tolist())
# ---- the new picture in screen space ---------------------------------------------------------------------------------------------
wq = (np.linalg.norm(quad[1] - quad[0]) + np.linalg.norm(quad[2] - quad[3])) / 2
hq = (np.linalg.norm(quad[3] - quad[0]) + np.linalg.norm(quad[2] - quad[1])) / 2
SW, SH = 1000, int(round(1000 * hq / wq))
pic = Image.open(PIC).convert("RGB"); pw, ph = pic.size
CX = float(sys.argv[2]) if len(sys.argv) > 2 else 0.52                        # horizontal centre of the crop, as a fraction
s = max(SW / pw, SH / ph); cw, ch = SW / s, SH / s
x0 = min(max(0.0, CX * pw - cw / 2), pw - cw); y0 = (ph - ch) / 2
canvas = np.asarray(pic.resize((SW, SH), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))).copy()
print(f"picture {pw}x{ph} -> screen {SW}x{SH}, crop x {x0:.0f}-{x0 + cw:.0f} y {y0:.0f}-{y0 + ch:.0f}")
Hs = cv2.getPerspectiveTransform(np.float32([[0, 0], [SW, 0], [SW, SH], [0, SH]]), quad)   # screen space -> frame 0

# ---- track the phone: ECC against frame 0 on a high-passed band around the phone's edge ---------------------------------------
# Tried first: SIFT outside the screen (inliers fell from 58 to 8 on the dark marble) and the screen quad found in every frame (the
# glass glare from frame 42 brightens the bezel past the marble and the fill leaks). What holds: ECC homography against frame 0 on
# image MINUS its Gaussian blur (the smooth glare is removed, the rim, bezel edge and marble veins stay), in a band from 10 px inside
# the screen edge to 90 px outside it, each frame started from the previous frame's warp.
band = (cv2.dilate(hull0, np.ones((181, 181), np.uint8)) - cv2.erode(hull0, np.ones((21, 21), np.uint8))).astype(np.uint8)
band[notch0 > 0] = 1
hp = lambda f: (lambda g: g - cv2.GaussianBlur(g, (0, 0), 12))(cv2.cvtColor(f, cv2.COLOR_RGB2GRAY).astype(np.float32))
T = hp(f0); Wp = np.eye(3, dtype=np.float32); WPS, INF = [Wp.copy()], [1.0]
crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 150, 1e-6)
for n in range(1, N):
    try:
        cc, Wn = cv2.findTransformECC(T, hp(fr[n]), Wp.copy(), cv2.MOTION_HOMOGRAPHY, crit, band, 5)
        Wp = Wn
    except cv2.error:
        cc = -1.0
    WPS.append(Wp.copy()); INF.append(round(float(cc), 4))
# findTransformECC's warp maps template (frame 0) coordinates -> input (frame n) coordinates with WARP_INVERSE_MAP semantics:
# a point x0 in frame 0 sits at W^-1 x0? No: ECC returns W such that I_n(W x) ~ T(x), i.e. frame-0 point x is at W x in frame n.
corners = np.array([cv2.perspectiveTransform(quad[None], M.astype(np.float64))[0] for M in WPS])
sg = 1.6; kk = np.exp(-0.5 * (np.arange(-4, 5) / sg) ** 2); kk /= kk.sum()
Pd = np.pad(corners, ((4, 4), (0, 0), (0, 0)), mode="edge")
cs = np.stack([np.tensordot(kk, Pd[i:i + 9], axes=(0, 0)) for i in range(N)])
print("ecc min", min(INF[1:]), "| corner travel px", round(float(np.abs(corners - corners[0]).max()), 1),
      "| frame-to-frame jump max px", round(float(np.abs(np.diff(corners, axis=0)).max()), 1),
      "| smoothing moved max px", round(float(np.abs(cs - corners).max()), 2))

# ---- composite ------------------------------------------------------------------------------------------------------------------
# along the top of the notch the screen's soft paste edge blended the new sky into the black: a 1 px light seam (independent review,
# take 3). There the ORIGINAL pixels stay (black notch meeting black bezel, with the clip's own glare): an 8 px band of the notch
# under the hull's top edge is left out of the paste.
notch_top = ((notch0 > 0) & (cv2.erode(hull0, np.ones((17, 17), np.uint8)) == 0)).astype(np.uint8)
paste0 = cv2.GaussianBlur((cv2.erode(screen0, np.ones((3, 3), np.uint8)) & (1 - cv2.dilate(notch_top, np.ones((3, 3), np.uint8)))).astype(np.float32), (5, 5), 1.2)
notchA0 = cv2.GaussianBlur(notch0.astype(np.float32), (5, 5), 1.0)
enc = subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "24",
                        "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "12",
                        "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-color_range", "tv", OUT], stdin=subprocess.PIPE)
log = []
for n, a in enumerate(fr):
    Mn = cv2.getPerspectiveTransform(quad, np.float32(cs[n])).astype(np.float64)          # frame 0 -> frame n (smoothed)
    newpic = cv2.warpPerspective(canvas, Mn @ Hs, (W, H), flags=cv2.INTER_LANCZOS4).astype(np.float32)
    na = cv2.warpPerspective(notchA0, Mn, (W, H), flags=cv2.INTER_LINEAR)[..., None]
    # the notch fill comes from THIS frame's own notch: back in frame-0 space, each column's median over the notch core rows (above the
    # old picture's fringe at its bottom edge), carried down the column. A flat black met the clip's glare-lit notch top in a visible
    # step during the glare (independent review, take 4).
    a0 = cv2.warpPerspective(a, np.linalg.inv(Mn), (W, H), flags=cv2.INTER_LINEAR).astype(np.float32)
    # per column, the 20th percentile over the notch rows: the original's front-camera dot (bright, small, at the notch's left end) is
    # left out; a median took it in and the left end read 18-32 levels lighter than the bezel during the glare (review, take 5)
    inner = np.percentile(a0[NC0:NC1, NX0 + 10:NX1 - 9], 20, axis=0)
    col = np.concatenate([np.repeat(inner[:1], 10, 0), inner, np.repeat(inner[-1:], 10, 0)])
    d0, d1 = DOT[0] - NX0, DOT[1] - NX0                                                  # the dot's columns: bridged from either side
    tt = np.linspace(0, 1, d1 - d0 + 1)[:, None]; col[d0:d1 + 1] = col[d0] * (1 - tt) + col[d1] * tt
    col = cv2.GaussianBlur(col[None].astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.1)[0]   # smooth along the row: no column streaks
    nimg = np.zeros((H, W, 3), np.float32); nimg[:, NX0:NX1 + 1] = col[None]
    nimg = cv2.warpPerspective(nimg, Mn, (W, H), flags=cv2.INTER_LINEAR)
    newpic = newpic * (1 - na) + nimg * na
    m = cv2.warpPerspective(paste0, Mn, (W, H), flags=cv2.INTER_LINEAR)[..., None]
    # glare: what the glass adds over frame 0's screen, at low frequency, light only
    old0 = cv2.warpPerspective(f0, Mn, (W, H), flags=cv2.INTER_LINEAR).astype(np.float32)
    dL = (a.astype(np.float32) - old0).mean(2) * m[..., 0]
    gl = cv2.GaussianBlur(dL, (0, 0), 35) / np.maximum(cv2.GaussianBlur(m[..., 0], (0, 0), 35), 1e-3)
    gl = np.clip(gl - 4.0, 0, None) * m[..., 0]
    lit = newpic + gl[..., None] * (1 - newpic / 300.0) * (1 - na)                   # the notch already carries its own glare                                    # light: lifts darks more than highlights
    o = a.astype(np.float32) * (1 - m) + lit * m
    enc.stdin.write(np.clip(o + 0.5, 0, 255).astype(np.uint8).tobytes())
    log.append(dict(n=n, ecc=INF[n], glare_mean=round(float(gl[m[..., 0] > 0.5].mean()), 2), corners=cs[n].round(1).tolist()))
enc.stdin.close(); assert enc.wait() == 0
json.dump(dict(src=SRC, t0=T0, frames=N, quad0=quad.tolist(), screen_px=[SW, SH], picture=PIC, crop=[x0, y0, cw, ch], log=log),
          open(OUT + ".json", "w"), indent=0)
print("LOCK_DONE", OUT, N, "frames; glare max", max(l["glare_mean"] for l in log))
