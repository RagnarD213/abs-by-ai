"""SL-15: RO-19's real-photo displays rebuilt for the vertical picture area (1080 x 1610 under the title band). Each
fn(tt, cover, t_abs) returns the 1080 x 1610 RGB picture. Same photos, same card language as the film (softblue.photo_card:
rounded blue frame, rises in, a slow 1.4 %/s push; glass caption tabs; the dark disclosure chip), laid out to fill the tall frame.
Real-photo label wording per VIDEO-RULES 2026-10-17, title case in the graphic. Chip boxes are placed clear of his face and abs
(measured with the person mask on the rendered frame: chipcheck in the build notes)."""
import numpy as np
from PIL import Image, ImageDraw
import lib
S = lib.B
W, H, DROP = 1080, 1920, 310
PH = "/Volumes/Extreme/_edit_work/SL-17/clips"
REAL1 = "Real Photo Of Me, Not AI-Generated"
REAL2 = "Real Photos Of Me, Not AI-Generated"
CHIP_U = 1.6
PHOTO1_BOX = (66, DROP + 90, 947, 1184)                        # 4:5, the film's own crop of the photo; canvas y 400 to 1584, the chip above it (inside the card it touched his hair)
PAIR_W, PAIR_H, PAIR_Y = 500, 900, DROP + 100                  # two tall cards side by side, canvas y 410 to 1310
PAIR_X = (27, 553)
def chip_xy(c, default):
    return tuple(c.get("chip", default))
def tab(im, cx, y, s, t, delay):
    """caption tab under a photo (the film's pairs.tab, sized for the vertical): glass pill, white title-case text"""
    q = S.ease(t - delay)
    if q <= 0: return
    f = S.font(36); tw = S.text_w(s, f); bw, bh = tw + 44, 62
    box = (cx - bw / 2, y, cx + bw / 2, y + bh)
    S.glass(im, box, t, 2.0, radius=16)
    ImageDraw.Draw(im).text((cx - tw / 2, y + 9), s, font=f, fill=S.WHITE)
def photo1(tt, c, t):
    """the film's P02: one real photo, as large as the picture area allows with the chip above it (chip box y 322-386, his hair from y 409)."""
    im = S.field(t, W, H)
    S.photo_card(im, f"{PH}/{c['photo']}.jpg", PHOTO1_BOX, tt, 0.0, fit=True, u=2.0)
    if tt > 0.25: S.disclosure(im, REAL1, chip_xy(c, (W / 2, DROP + 12)), CHIP_U, anchor="mt")
    return im.crop((0, DROP, W, H))
def pair(tt, c, t):
    """the film's P05: before and after, the same side pose, two tall cards; the after card comes up on c['reveal'] (s)."""
    im = S.field(t, W, H)
    for i, (p, d, cap) in enumerate(((c["before"], 0.0, "Before The Tan"), (c["after"], c.get("reveal", 0.6), "After The Tan"))):
        x = PAIR_X[i]
        S.photo_card(im, f"{PH}/{p}.jpg", (x, PAIR_Y, PAIR_W, PAIR_H), tt, d, fit=True, u=2.0)
        tab(im, x + PAIR_W / 2, PAIR_Y + PAIR_H - 92, cap, tt, d + 0.15)
    if tt > 0.25: S.disclosure(im, REAL2, chip_xy(c, (W / 2, DROP + 12)), CHIP_U, anchor="mt")
    return im.crop((0, DROP, W, H))
GROUP_BOX = (40, DROP + 260, 1000, 667)                         # the 1440x960 group photo at its own 3:2, as wide as the frame allows; canvas y 570 to 1237, clear of the captions (1412)
def group(tt, c, t):
    """RO-26's P14: Dan's supplied black-belt group photo, original aspect (a row of people across the width: a crop would cut them).
    No real-photo chip: the film showed it without one (not a physique picture, VIDEO-RULES 2026-09-11 applies to result photos)."""
    im = S.field(t, W, H)
    S.photo_card(im, f"{PH}/{c['photo']}", GROUP_BOX, tt, 0.0, fit=True, u=2.0)
    return im.crop((0, DROP, W, H))
SCENES = {"photo1": photo1, "pair": pair, "group": group}
