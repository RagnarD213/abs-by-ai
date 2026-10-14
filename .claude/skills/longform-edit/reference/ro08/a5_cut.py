"""RO-08 round 3: the donut clip (A5) as a two-shot cut of the round 2 take, so nothing vanishes (Dan, 2026-10-13: "all the donuts just
disappear, vaporize, and go nowhere... Use a part of the clip only").
Shot one: take frames 0..S1_END, he bites the donut, the box is full, the clock reads nine. HARD CUT (the hour passing).
Shot two: take frames S2_START..end, the box is already empty, the muffin and both hands are at rest, he sinks onto the keyboard.
The fast-forward between them (frames 25..73: hands blur, the donuts fade in the box, a muffin flies, then the keyboard and the muffin
settle) is never shown. Shot two started at frame 68 in the first round 3 render; the independent review found the tail of the old
dissolve there, a translucent wisp on the desk left of the muffin (strong for 6 frames, faint to frame 86), with the muffin still rocking
and the keyboard still sliding. It now starts at 74, where the desk has settled, and what is left of the wisp is painted out with the
same patch of desk from frame 96 (a gradient-domain clone inside a small ellipse, kept off the muffin).
The wall clock is steadied in both shots: Veo runs its minute hand round the dial (an hour in 2.5 s while he sinks at natural speed) and
swaps the 12 for a 10 at the top of the dial. Each shot gets ONE clock, pasted from a clean frame of the same take through a feathered
disc (shot one: frame 0, nine o'clock; shot two: frame 136, ten o'clock). Nothing outside the disc changes (planes are patched in YUV).
24 fps is laid on 29.97 by repeating frames, never retimed.
usage: a5_cut.py OUT.mp4 N_FRAMES   -> prints the output frame the cut falls on (finish08.py needs it)"""
import sys, subprocess, json, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; SRC = "/Volumes/Extreme/_edit_work/ro08/round2/motion/A5-t1.mp4"
out = sys.argv[1]; N = int(sys.argv[2]); FPS = 30000/1001; W, H = 1920, 1080; SZ = W*H*3//2
S1_END = 24; S2_START = 74; REF1 = 0; REF2 = 136; R_IN, R_OUT = 153.0, 166.0
raw = subprocess.run([FF, "-v", "error", "-i", SRC, "-pix_fmt", "yuv420p", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
F = [np.frombuffer(raw[i:i+SZ], np.uint8).copy() for i in range(0, len(raw), SZ)]; assert len(F) == 144, len(F)
def planes(f): return f[:W*H].reshape(H, W), f[W*H:W*H*5//4].reshape(H//2, W//2), f[W*H*5//4:].reshape(H//2, W//2)
CX, CY = 1508.0, 170.5                                   # the clock, measured on the take: dark rim from x 1364 to 1652 and y 23 to 318
def rim(f):                                              # where the rim's outer edge sits: left, right, top, bottom
    y = planes(f)[0]; xs = np.nonzero(y[170, 1300:1720] < 80)[0] + 1300; ys = np.nonzero(y[0:400, 1508] < 80)[0]
    return np.array([xs.min(), xs.max(), ys.min(), ys.max()], np.float32)
used = [i for i in range(len(F)) if i <= S1_END or i >= S2_START]; r0 = rim(F[REF1]); drift = max(float(np.abs(rim(F[i]) - r0).max()) for i in used)
cx, cy = CX, CY
print(f"clock rim edges on frame {REF1}: {r0.tolist()}; most any edge moves over the frames used: {drift:.0f} px (the disc replaces the whole rim, out to {R_IN:.0f} px)")
assert drift <= 4, "the clock moves in the take: a pasted clock would not sit where the wall expects it"
def mask(w, h, s):
    yy, xx = np.mgrid[0:h, 0:w]; r = np.hypot(xx*s + (s-1)/2 - cx, yy*s + (s-1)/2 - cy)
    return np.clip((R_OUT - r)/(R_OUT - R_IN), 0, 1).astype(np.float32)
MY, MC = mask(W, H, 1), mask(W//2, H//2, 2)
def paste(f, ref):
    o = f.copy()
    for p, q, m in zip(planes(o), planes(ref), (MY, MC, MC)): p[:] = np.rint(p*(1-m) + q*m).astype(np.uint8)
    return o
ring = (MY > 0.02) & (MY < 0.98)                         # the feather must sit on wall that is the same in both frames
def wall(f, ref): return float(np.abs(planes(f)[0][ring].astype(np.float32) - planes(ref)[0][ring]).mean())
s1 = list(range(REF1, S1_END+1)); s2 = list(range(S2_START, len(F)))
w1 = max(wall(F[i], F[REF1]) for i in s1); w2 = max(wall(F[i], F[REF2]) for i in s2)
print(f"wall under the feather, worst frame against its clock's frame: shot one {w1:.2f} levels, shot two {w2:.2f} levels")
assert max(w1, w2) < 3.0, "the wall round the clock changes inside a shot: the paste would show"
# ---- one leftover of the old dissolve in shot two's first frames is painted out: a translucent orange smear in the front of the box, the last of
# the glazed donut, fading over take frames 74 to 78, with a dark crumb fading in beside it (second independent review). From frame 84 the box
# holds still, so the patch is frame 84's box.
# The desk left of the muffin is NOT patched. From frame 74 what is left there of the wisp the first review found is a pale speck of 20 to 40 px
# that fades over half a second. Two attempts to paint it out were each worse than the speck: his hand's shadow crosses that exact spot as he
# sinks, so no later frame matches, and the third review measured the patch itself as a pale blob that came and went (12 to 19 levels).
import cv2
# (centre x, y, radius x, y, the later frame the patch comes from). The ellipse is generous: at 176 x 50 a 6 x 12 px end of the smear showed at its
# left edge for three frames (third review).
PATCHES = [(1500, 950, 215, 75, 84)]
# The patch is the later frame's picture plus this frame's own shading: the difference between the two frames is measured only OUTSIDE the ellipse,
# smoothed into it (a normalised blur), and added back, so the desk's shading drift as he leans (up to 11 levels) does not show as a patch.
# Plain numpy on the YUV planes. cv2.seamlessClone was tried first and is NOT used: in this OpenCV build (5.0.0) every second call returned
# the destination untouched, so alternate frames kept the smear (counted per frame below; the second render shipped that way to the reviewer).
def _win(cx, cy, rx, ry): x0 = max(0, (cx - rx - 80)//2*2); y0 = max(0, (cy - ry - 80)//2*2); x1 = min(W, (cx + rx + 80)//2*2); y1 = min(H, (cy + ry + 80)//2*2); return x0, y0, x1, y1
PREP = []
for cx, cy, rx, ry, ref in PATCHES:
    w = _win(cx, cy, rx, ry); x0, y0, x1, y1 = w; yy_, xx_ = np.mgrid[y0:y1, x0:x1]; r_ = np.hypot((xx_-cx)/rx, (yy_-cy)/ry)
    ay = np.clip((1.0 - r_)/0.25, 0, 1).astype(np.float32); wo = (r_ > 1.12).astype(np.float32)                 # the feathered patch, and where the shading is read
    PREP.append((ref, w, ay, cv2.resize(ay, ((x1-x0)//2, (y1-y0)//2), interpolation=cv2.INTER_AREA), wo, cv2.resize(wo, ((x1-x0)//2, (y1-y0)//2), interpolation=cv2.INTER_AREA)))
def dewisp(f, i):
    o = None
    for ref, (x0, y0, x1, y1), ay, ac, wo, woc in PREP:
        if i >= ref: continue
        o = f.copy() if o is None else o
        for p_, q_, m, wt, sg, sl in zip(planes(o), planes(F[ref]), (ay, ac, ac), (wo, woc, woc), (22.0, 11.0, 11.0),
                                         ((slice(y0, y1), slice(x0, x1)), (slice(y0//2, y1//2), slice(x0//2, x1//2)), (slice(y0//2, y1//2), slice(x0//2, x1//2)))):
            d = p_[sl].astype(np.float32) - q_[sl].astype(np.float32)
            shade = cv2.GaussianBlur(d*wt, (0, 0), sg)/np.maximum(cv2.GaussianBlur(wt, (0, 0), sg), 1e-3)
            p_[sl] = np.clip(np.rint(p_[sl]*(1-m) + (q_[sl] + shade)*m), 0, 255).astype(np.uint8)
    return f if o is None else o
def _orange(f, x0, y0, x1, y1):
    b_ = cv2.cvtColor(f.reshape(H*3//2, W), cv2.COLOR_YUV2BGR_I420)[y0:y1, x0:x1].astype(np.int16); return int(((b_[..., 2] - b_[..., 0] > 60) & (b_[..., 2] > 170) & (b_[..., 1] > 110) & (b_[..., 1] < 200)).sum())
shot1 = [paste(F[i], F[REF1]) for i in s1]; shot2 = [dewisp(paste(F[i], F[REF2]), i) for i in s2]
_oc = [_orange(f, 1350, 890, 1670, 1010) for f in shot2[:14]]; _ob = int(np.median([_orange(f, 1350, 890, 1670, 1010) for f in shot2[14:40]]))
print("orange pixels in the front of the box, shot two's first 14 take frames:", _oc, "| the crumbs alone, later:", _ob)
assert max(_oc) < _ob*1.15 + 40, "the glaze smear is still in the box on some frame"
# the check all three renders needed: in shot two's first ten frames, nothing away from the man may change by itself. Each pixel of the shot's
# first frame is compared with the range its neighbourhood takes on the tenth frame (so an edge that drifts a pixel or two is not a change),
# outside a mask of the man (the big connected change) grown by 40 px. The blobs left are printed and a heat map is written beside the clip:
# LOOK AT IT. A moving shadow is fine; a patch of colour that is there on the first frame and gone on the tenth is the fault Dan rejected.
def _rgb(f): return cv2.GaussianBlur(cv2.cvtColor(f.reshape(H*3//2, W), cv2.COLOR_YUV2BGR_I420), (0, 0), 1.5).astype(np.float32)
_a, _b = _rgb(shot2[0]), _rgb(shot2[10]); _k = np.ones((7, 7), np.uint8)
_d = np.maximum(np.maximum(_a - cv2.dilate(_b, _k), cv2.erode(_b, _k) - _a), 0).max(2)
_raw = np.abs(_a - _b).max(2); _n, _lab, _st, _ = cv2.connectedComponentsWithStats((_raw > 14).astype(np.uint8)); _big = 1 + int(np.argmax(_st[1:, cv2.CC_STAT_AREA]))
_man = cv2.dilate((_lab == _big).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81)))
_m = ((_d > 10) & (_man == 0)).astype(np.uint8); _n2, _l2, _s2, _ = cv2.connectedComponentsWithStats(_m)
SELF = sorted(((int(_s2[k, cv2.CC_STAT_AREA]), int(_s2[k, 0]), int(_s2[k, 1]), int(_s2[k, 2]), int(_s2[k, 3])) for k in range(1, _n2)), reverse=True)[:6]
print("shot two, first frame against its tenth, changes away from the man (area px, x, y, w, h):", SELF)
_vis = cv2.cvtColor(np.clip(_d*10, 0, 255).astype(np.uint8), cv2.COLOR_GRAY2BGR); _vis[_man > 0] = (_vis[_man > 0]*0.3 + np.array([60, 0, 0])).astype(np.uint8)
cv2.imwrite(out + ".selfchange.jpg", cv2.resize(_vis, (960, 540)))
n1 = int(round(len(shot1)*FPS/24)); n2 = N - n1
assert int((n2-1)*24/FPS) < len(shot2), f"shot two runs out of source ({n2} frames asked, {len(shot2)} source): never hold a frame"
seq = [shot1[min(len(shot1)-1, int(j*24/FPS))] for j in range(n1)] + [shot2[int(j*24/FPS)] for j in range(n2)]
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", f"{W}x{H}", "-framerate", "30000/1001", "-i", "-", "-an", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                        "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
for f in seq: enc.stdin.write(f.tobytes())
enc.stdin.close(); assert enc.wait() == 0
last = S2_START + int((n2-1)*24/FPS)
json.dump(dict(src=SRC, frames=N, cut_frame=n1, shot1_src=[REF1, S1_END], shot2_src=[S2_START, last], clock_ref=[REF1, REF2], clock_disc=[cx, cy, R_IN, R_OUT],
               rim_drift_px=drift, patches=[list(p_) for p_ in PATCHES], patch_method='later frame + shading read outside the ellipse (numpy)', box_orange_px=_oc, self_change_blobs=SELF, wall_levels=[round(w1, 2), round(w2, 2)]), open(out + ".json", "w"), indent=1)
print(out, N, "frames; the cut is at output frame", n1, f"({n1/FPS:.3f} s); shot two uses take frames {S2_START}..{last} of 143")
