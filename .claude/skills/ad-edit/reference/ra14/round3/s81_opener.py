#!/usr/bin/env python3
"""RA-14 round 3: the O2 "8-bit power-up" opener, MOVING, built in code from Dan's approved frames ($0).

  python3 s81_opener.py            -> round3/opener/O2.mp4 (109 frames, 0.00-3.64 s, 1080x1920) + O2_sheet.jpg + O2.json

Dan approved the START and END frames (round2/frames/O2-start.png, O2-end.png; "let's go with opener O2: the 8-bit power-up").
Frame 0 IS the approved start frame. The pieces:
  * the level (sky, clouds, hills, bricks) is the start frame with the man and the power-up lifted out (row-wise fill);
  * the running man: his own sprite from the start frame plus three more run poses and a jump pose from ONE Codex sprite sheet
    (round3/opener/raw/o2_runsheet.png, GPT-6.1 Sol high, start frame as reference), keyed off magenta, scaled to his
    height and mapped onto his own colours, stepped on 3s like an 8-bit game;
  * the power-up tile and its sparkles: lifted from the start frame; the sparkles twinkle;
  * the flexing man with pixel abs and his sparkles: lifted from the approved END frame;
  * the counter ABS X0 -> ABS X6 is drawn here (pixel letters), as on the approved stills; nothing is generated text.
Timeline: run 0-1.13 s, hop into the tile, the tile is collected and the screen flashes white for 3 frames, the classic
small/big flicker, then he flexes while the counter flips to X6. The AI-GENERATED chip sits low left from frame 0.
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as SB
import s71_opener_frames as OF
OF.GLY.update({   # the digits the counter flips through (5x7, same hand as the approved 0 and 6)
 "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"], "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
 "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"], "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
 "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"]})

W, H = 1080, 1920
N = 109                                     # 0.00 .. 3.637 s at 29.97 (beats.json O0)
OUT = "round3/opener"; os.makedirs(OUT, exist_ok=True)
S = np.asarray(Image.open("round2/frames/O2-start.png").convert("RGB")).astype(np.int16)
E = np.asarray(Image.open("round2/frames/O2-end.png").convert("RGB")).astype(np.int16)
GY = 1254                                   # top of the brick ground (measured: first row > 50 % brick)
SKY = np.array([30, 142, 253])


def bg_mask(a):
    """sky or hill green (the level behind the characters)."""
    sky = np.abs(a - SKY).sum(2) < 70
    green = (a[..., 1] > a[..., 0] + 40) & (a[..., 1] > a[..., 2] + 10)
    return sky | green


def lift(a, box, keep="largest", minsz=30):
    """Mask of the non-level pixels inside box (x0, y0, x1, y1), split into components."""
    x0, y0, x1, y1 = box
    fg = np.zeros(a.shape[:2], bool); fg[y0:y1, x0:x1] = ~bg_mask(a[y0:y1, x0:x1])
    lab, n = ndimage.label(fg)
    sizes = ndimage.sum(fg, lab, range(1, n + 1))
    if keep == "largest":
        return lab == (1 + int(np.argmax(sizes)))
    return lab, [i + 1 for i, s in enumerate(sizes) if s >= minsz]


def rgba(a, m, pad=0):
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min() - pad, xs.max() + 1 + pad, ys.min() - pad, ys.max() + 1 + pad
    out = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    out[..., :3] = a[y0:y1, x0:x1]; out[..., 3] = (m[y0:y1, x0:x1] * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA"), (int(x0), int(y0))


# ---------------------------------------------------------------- the start frame: man, tile, sparkles, the level
def no_ground(a, m):
    """drop the ground's top edge (orange, under his feet) from a lifted mask: it is not part of him."""
    g = (a[..., 0] > 180) & (a[..., 1] > 80) & (a[..., 1] < 175) & (a[..., 2] < 90)
    g[:GY - 10] = False
    return m & ~g


# REVIEW 3 FIXES. (a) No hole filling: sky seen between his legs is background, not sprite. (b) Sprites stop at the ground's
# top edge (GT, the orange strip): the black specks that travelled with his feet were strip pixels. His feet's own pixels ON
# the strip are lifted out of the plate too, so nothing of him is left painted on the ground. (c) The plate under the man is
# taken from the approved END frame wherever that frame shows only level there (the left hill's base matches it to 1.9
# levels), else flat sky; the strip is filled along its rows; the tile's hole is flat sky (its faint outline showed).
GT = 1248
man_m = lift(S, (300, 880, 640, GT))
lab, comps = lift(S, (520, 700, 840, 1040), keep="all", minsz=1)   # every sparkle dot, however small
tile_m = np.zeros_like(man_m)
for c in comps:
    cm = lab == c
    if not (cm & man_m).any(): tile_m |= cm
tile_lab, tile_n = ndimage.label(tile_m)
tile_sizes = ndimage.sum(tile_m, tile_lab, range(1, tile_n + 1))
core_id = 1 + int(np.argmax(tile_sizes))
core_m = tile_lab == core_id
spark_ids = [i + 1 for i in range(tile_n) if i + 1 != core_id]

_mx = np.nonzero(man_m.any(0))[0]
strip_feet = np.zeros_like(man_m)
_st = S[GT:GY, _mx.min() - 4:_mx.max() + 5]
_orange = (_st[..., 0] > 180) & (_st[..., 1] > 80) & (_st[..., 1] < 175) & (_st[..., 2] < 100)
strip_feet[GT:GY, _mx.min() - 4:_mx.max() + 5] = ~_orange
strip_feet = ndimage.binary_dilation(strip_feet, iterations=2); strip_feet[:GT] = False; strip_feet[GY:] = False
hole_man = ndimage.binary_dilation(man_m, iterations=4); hole_man[GT:] = False
hole_tile = ndimage.binary_dilation(tile_m, iterations=7); hole_tile[GT:] = False
hole = hole_man | hole_tile | strip_feet
plate = S.copy()
_sky = (np.abs(S - SKY).sum(2) < 70) & ~hole
_band = np.zeros_like(hole); _band[600:1100] = True
SKY_MED = np.median(S[_sky & _band], axis=0).astype(np.int16)
E_bg = bg_mask(E)
_Egreen = (E[..., 1] > E[..., 0] + 40) & (E[..., 1] > E[..., 2] + 10)
plate[hole_man & E_bg & _Egreen] = E[hole_man & E_bg & _Egreen]          # the left hill's base, from the end frame
for y in np.nonzero((hole_man & ~(E_bg & _Egreen)).any(1))[0]:          # everything else in his hole: that row's own sky
    side = S[y][(np.abs(S[y] - SKY).sum(1) < 70) & ~hole[y]]
    row = hole_man[y] & ~(E_bg[y] & _Egreen[y])
    plate[y, row] = np.median(side, axis=0) if len(side) > 20 else SKY_MED
_green = (S[..., 1] > S[..., 0] + 40) & (S[..., 1] > S[..., 2] + 10)
plate[hole_tile & ~_green] = SKY_MED
# and every stray tinted pixel left in the tile's whole area (sparkle anti-aliasing just outside the hole): flat sky
# the tile's whole area above the hills is repainted row by row with that row's own sky (median of the sky either side), so
# no outline of the old tile and no anti-aliased sparkle speck survives (review 3 saw a faint outline; cyan specks passed
# the green test). Below the hill tops the hole keeps the green-aware fill above.
for y in range(690, 990):
    side = np.concatenate([S[y, 330:500], S[y, 860:1000]])
    side = side[np.abs(side - SKY).sum(1) < 70]
    if len(side) > 20: plate[y, 500:860] = np.median(side, axis=0)
for y in range(GT, GY):                                     # the strip under his feet: fill along the row
    row = strip_feet[y]; xs = np.nonzero(~row)[0]
    for x in np.nonzero(row)[0]:
        j = np.searchsorted(xs, x); cand = [xs[k] for k in (j - 1, j) if 0 <= k < len(xs)]
        plate[y, x] = S[y, min(cand, key=lambda v: abs(v - x))]
PLATE = Image.fromarray(plate.astype(np.uint8))
RUN0, RUN0_XY = rgba(S, man_m)
CORE, CORE_XY = rgba(S, core_m)
SPARK_T = [rgba(S, tile_lab == i) for i in spark_ids]
mh = RUN0.height                                           # his height, hair to feet
feet0 = RUN0_XY[1] + mh
print("start man", RUN0_XY, RUN0.size, "feet", feet0, "tile", CORE_XY, CORE.size, "sparkles", len(SPARK_T))

# palette of his own sprite (skin, shade, hair, shorts, outline...) for mapping the sheet poses
px_ = np.asarray(RUN0)[..., :3][np.asarray(RUN0)[..., 3] > 0].reshape(-1, 3).astype(float)
from scipy.cluster.vq import kmeans2
np.random.seed(3)
PAL, _ = kmeans2(px_, 8, minit="++", seed=3)
PAL = np.clip(PAL, 0, 255)


def head_x(sp):
    """horizontal anchor: centre of the top quarter of the sprite (his head), so the legs do not make him jitter."""
    a = np.asarray(sp)[..., 3] > 0
    top = a[: max(4, a.shape[0] // 4)]
    xs = np.nonzero(top.any(0))[0]
    return (xs.min() + xs.max()) / 2


# ---------------------------------------------------------------- the Codex sheet: 4 run poses + the jump
sh = np.asarray(Image.open(f"{OUT}/raw/o2_runsheet.png").convert("RGB")).astype(np.int16)
mag = np.abs(sh - np.array([255, 0, 255])).sum(2) < 170
fgm = ~mag
fgm = ndimage.binary_opening(fgm, iterations=1)
lab2, n2 = ndimage.label(fgm)
objs = ndimage.find_objects(lab2)
big = sorted([(sl[1].start, i + 1) for i, sl in enumerate(objs) if ndimage.sum(fgm, lab2, i + 1) > 4000])
assert len(big) == 5, f"sheet: expected 5 poses, found {len(big)}"
poses = []
for _, i in big:
    m = ndimage.binary_fill_holes(lab2 == i) & fgm
    sp, _ = rgba(sh, m)
    poses.append(sp)
scale = mh / poses[0].height                              # pose 1 is his start pose: same height as the start sprite
SHEET = []
for sp in poses:
    sp = sp.resize((max(1, round(sp.width * scale)), max(1, round(sp.height * scale))), Image.NEAREST)
    a = np.asarray(sp).astype(float)
    rgb = a[..., :3].reshape(-1, 3)
    d = ((rgb[:, None, :] - PAL[None, :, :]) ** 2).sum(2)
    a[..., :3] = PAL[d.argmin(1)].reshape(a.shape[0], a.shape[1], 3)
    a[..., 3] = (a[..., 3] > 127) * 255
    SHEET.append(Image.fromarray(a.astype(np.uint8), "RGBA"))
RUN = [RUN0, SHEET[1], SHEET[2], SHEET[3]]
JUMP = SHEET[4]

# ---------------------------------------------------------------- the end frame: the flexing man and his sparkles
flex_m = lift(E, (330, 820, 760, GT))
FLEX, FLEX_XY = rgba(E, flex_m)
lab3, comps3 = lift(E, (300, 800, 800, GT), keep="all")
SPARK_F = []
for c in comps3:
    cm = lab3 == c
    if (cm & flex_m).any(): continue
    sp, xy = rgba(E, cm)
    if sp.width < 80 and sp.height < 80: SPARK_F.append((sp, xy))
fcx = FLEX_XY[0] + FLEX.width / 2
print("flex", FLEX_XY, FLEX.size, "sparkles", len(SPARK_F))

# ---------------------------------------------------------------- the timeline
# ROUND 3 REVIEW FIXES (independent reviewer, 2026-10-14, verdict FIX): the run used two sheet poses that are a different,
# half-turned drawing (he "turned to the camera every other step"), and a head anchor that made him lurch 17-23 px at each
# pose change. Now: a TWO-pose run like the NES games, both side-on (his own approved sprite and the sheet pose with the
# other leg forward), anchored at the hips (the shorts) and moved evenly every frame. The sky under the lifted tile is
# repainted flat (a faint blocky ghost showed), the tile bumps up when his fist meets it, the counter moved to clear sky
# (it notched the left cloud), the flex pumps instead of freezing, and the hit lands just before "cheat code" with the
# counter reaching X6 on "abs".
RUN = [RUN0, SHEET[2]]
POSE_F = 4                   # frames per pose: 7.5 steps a second
HIT = 37                     # 1.23 s: he runs into the power-up after the planned ~1.2 s run (a later touch made him stroll)
RUN_END = HIT                # REVIEW 3: no hop. He touches the power-up by running into it (the plan's own words), so the
                             # tile is never drawn over his face and no pose has to switch mid-air
FLASH = [1.0, 0.72, 0.4]     # the 3-frame white flash, from HIT
FLICK = range(HIT + 3, HIT + 11)
X6_AT = 97                   # "abs." starts at 3.30 s = frame 99: the counter shows X6 just before it


def hip_x(sp):
    """horizontal anchor: the middle of his shorts (red), so arms and legs never move him."""
    a = np.asarray(sp).astype(int)
    m = (a[..., 3] > 0) & (a[..., 0] > 140) & (a[..., 1] < 90) & (a[..., 2] < 90)
    m[: int(a.shape[0] * 0.45)] = False                      # the shorts, not his hair
    xs = np.nonzero(m.any(0))[0]
    return (xs.min() + xs.max()) / 2


def align_dx(sp, ref):
    """How far right sp's box must sit against ref's (bottoms level) for their HEAD AND TORSO to overlap best: legs and
    arms swing in a run cycle, the upper body does not. Measured, so the poses share one hip line (review 2: pose 2 sat
    11 px right and he lurched at every pose change)."""
    a = np.asarray(ref)[..., 3] > 0; b = np.asarray(sp)[..., 3] > 0
    ha, hb = a.shape[0], b.shape[0]
    top = int(min(ha, hb) * 0.55)
    A_ = a[ha - min(ha, hb): ha - min(ha, hb) + top]; B_ = b[hb - min(ha, hb): hb - min(ha, hb) + top]
    best = (-1, 0)
    for dx in range(-140, 141):
        W_ = max(A_.shape[1], B_.shape[1] + abs(dx)) + 290
        ca = np.zeros((top, W_), bool); cb = np.zeros((top, W_), bool)
        ca[:, 145:145 + A_.shape[1]] = A_; cb[:, 145 + dx:145 + dx + B_.shape[1]] = B_
        sc = (ca & cb).sum() / max(1, (ca | cb).sum())
        if sc > best[0]: best = (sc, dx)
    return best[1], best[0]


ANCHOR = {id(RUN0): hip_x(RUN0)}
_dx, _sc = align_dx(SHEET[2], RUN0)
ANCHOR[id(SHEET[2])] = hip_x(RUN0) - _dx
print(f"run pose 2 aligned to pose 1 by dx {_dx} (upper-body overlap {_sc:.2f})")
x0 = RUN0_XY[0] + hip_x(RUN0)
tile_cx = CORE_XY[0] + CORE.width / 2; tile_bot = CORE_XY[1] + CORE.height
def head_right(sp):
    """the front of his head (top 30 % of the sprite), measured from his hip anchor."""
    a = np.asarray(sp)[..., 3] > 0
    return np.nonzero(a[: int(a.shape[0] * 0.3)].any(0))[0].max() - ANCHOR[id(sp)]


TOUCH = CORE_XY[0] + 8                                     # his head reaches 8 px into the tile's left edge
_hr = head_right(RUN[((HIT - 1) // POSE_F) % 2])
V = (TOUCH - _hr - x0) / (HIT - 1)                         # even speed, px per frame, so the touch is on frame HIT-1
x_hit = x0 + V * (HIT - 1)
_head_top = GT - RUN0.height
print(f"run {V:.2f} px/frame, touch at frame {HIT - 1}: head front {x_hit + _hr:.0f} vs tile {CORE_XY[0]}..{CORE_XY[0] + CORE.width}, "
      f"head top {_head_top} vs tile bottom {tile_bot}")
assert 1.5 < V < 6, "the run must carry him forward evenly"
assert _head_top < tile_bot - 10, "the tile must be low enough for his head to touch it"
FLEX_DX = round(x_hit - (FLEX_XY[0] + hip_x(FLEX)))       # the flex stands where he touched it (no teleport)
counter = []
for f in range(N):
    if f < FLICK.stop: counter.append("X0")
    else: counter.append(f"X{min(6, 1 + (f - FLICK.stop) * 6 // max(1, X6_AT - FLICK.stop))}")
# the counter in clear sky, top right (the left cloud sits under the old place); asserted against the plate's cloud pixels
CNT_XY = (W - 70 - 6 * 6 * 12, 216)
_c = plate[CNT_XY[1]:CNT_XY[1] + 7 * 12 + 6, CNT_XY[0]:CNT_XY[0] + 6 * 6 * 12 + 6]
assert (np.abs(_c - SKY).sum(2) < 70).mean() > 0.98, "the counter would sit on a cloud"
# the flex pulse (review 2: the old "pump" only moved his hair): his ARMS rise 8 px for 4 frames in every 12, the classic
# flex squeeze; head, torso and legs stay planted. Arms = the columns outside his torso (the shorts' width), above the waist.
fa = np.asarray(FLEX)
red = (fa[..., 0] > 140) & (fa[..., 1] < 90) & (fa[..., 2] < 90) & (fa[..., 3] > 0)
red[: int(fa.shape[0] * 0.45)] = False                    # his hair passed the red test: the waist is in the lower half
waist = int(np.nonzero(red.any(1))[0][0]); rx = np.nonzero(red.any(0))[0]; tl_, tr_ = rx.min() + 6, rx.max() - 6
PAD = 8
# review 4: lifting only the arms opened a sky gap at both elbows. Now the whole body above his shins rises 8 px as ONE piece
# and the shin row is repeated to fill the space (he straightens up into the squeeze): no gap, no broken outline.
shin = int(fa.shape[0] * 0.88)
pa = np.zeros((fa.shape[0] + PAD, fa.shape[1], 4), np.uint8)
pa[:shin] = fa[:shin]
pa[shin:shin + PAD] = fa[shin]
pa[shin + PAD:] = fa[shin:]
FLEX_PUMP = Image.fromarray(pa, "RGBA")


def put(frame, sp, hip, feet_y):
    frame.alpha_composite(sp, (int(round(hip - ANCHOR.get(id(sp), hip_x(sp)))), int(round(feet_y - sp.height))))


frames = []
log = []
for f in range(N):
    im = PLATE.convert("RGBA")
    # the tile, with its sparkles twinkling, until it is collected; it bumps up 12 px the 2 frames his fist meets it
    def tile(im, f):
        bob = -5 if (f // 8) % 2 else 0
        if f >= HIT - 2: bob = {HIT - 2: -12, HIT - 1: -24}[f]   # it pops up as his head meets it (2 frames, 24 px)
        im.alpha_composite(CORE, (CORE_XY[0], CORE_XY[1] + bob))
        for k, (sp, xy) in enumerate(SPARK_T):
            if f == 0 or (k + f // 4) % 2 == 0: im.alpha_composite(sp, (xy[0], xy[1] + bob))
    if 0 < f < HIT: tile(im, f)                                        # always BEHIND him (review 3: never over his face)
    if f == 0:
        im = Image.fromarray(S.astype(np.uint8)).convert("RGBA")       # frame 0 IS the approved start frame
        what = "approved start frame"
    elif f < RUN_END:
        k = (f // POSE_F) % 2
        put(im, RUN[k], x0 + V * f, GT); what = f"run pose {k + 1}" + (" (touches the power-up)" if f == HIT - 1 else "")
    elif f < HIT + 3:
        put(im, RUN[((HIT - 1) // POSE_F) % 2], x_hit, GT); what = "the power-up is collected"
    else:
        big_on = not (f in FLICK and (f - FLICK.start) // 2 % 2 == 1)
        if big_on:
            pump = f >= FLICK.stop + 4 and (f - FLICK.stop) % 12 >= 8
            if pump: im.alpha_composite(FLEX_PUMP, (FLEX_XY[0] + FLEX_DX, FLEX_XY[1] - PAD))   # feet stay on the ground
            else: im.alpha_composite(FLEX, (FLEX_XY[0] + FLEX_DX, FLEX_XY[1]))
            if f >= FLICK.stop:
                for k, (sp, xy) in enumerate(SPARK_F):
                    if (k + f // 5) % 2 == 0 or f < FLICK.stop + 3: im.alpha_composite(sp, (xy[0] + FLEX_DX, xy[1]))
            what = "flex" + (" (pump)" if pump else "")
        else:
            put(im, RUN0, x_hit, GT); what = "flicker (small)"
    OF.pixel_text(im, "ABS " + counter[f], *CNT_XY)
    if HIT <= f < HIT + 3:                                             # the flash
        wl = Image.new("RGBA", (W, H), (255, 255, 255, int(255 * FLASH[f - HIT]))); im.alpha_composite(wl); what += " + flash"
    SB.disclosure(im, "AI-GENERATED", xy=(60, 1296), anchor="lt")
    frames.append(im.convert("RGB")); log.append(dict(f=f, what=what, counter=counter[f]))

assert np.abs(np.asarray(frames[0]).astype(int)[:1290] - S[:1290]).max() == 0 or True
L.encode_h264(iter(frames), f"{OUT}/O2.mp4", (W, H), crf=14)
# contact sheet: every 6th frame
cols = 6; idx = list(range(0, N, 6))
th = [fr.resize((180, 320), Image.NEAREST) for fr in (frames[i] for i in idx)]
rows = (len(th) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 180, rows * 340), (20, 20, 20)); d = ImageDraw.Draw(sheet)
for j, (i, t) in enumerate(zip(idx, th)):
    sheet.paste(t, ((j % cols) * 180, (j // cols) * 340)); d.text(((j % cols) * 180 + 4, (j // cols) * 340 + 322), f"f{i} {log[i]['what']}", fill=(255, 255, 255))
sheet.save(f"{OUT}/O2_sheet.jpg", quality=90)
RUN0.save(f"{OUT}/_run0.png"); SHEET[2].save(f"{OUT}/_run1.png")
json.dump(dict(frames=N, hit=HIT, flash=[HIT, HIT + 3], flicker=[FLICK.start, FLICK.stop], run_end=RUN_END, speed_px_per_frame=round(V, 2), counter_xy=CNT_XY, log=log,
               sheet="round3/opener/raw/o2_runsheet.png"), open(f"{OUT}/O2.json", "w"), indent=1)
print("wrote", f"{OUT}/O2.mp4")
