"""SL-36 R2: the film's real-photo displays rebuilt for the vertical picture area (1080 x 1610 under the title band).
R01 (a side-by-side before/after pair in the film) becomes the before photo full screen, then the after photo full screen
(VIDEO-RULES 2026-11-05: never a before and an after on one screen). R02 (three studio portraits) becomes three single photos in
sequence. Same card language as the film (softblue.photo_card: rounded blue frame, rises in, slow push; glass tab; the dark
disclosure chip above the photo, clear of his face and abs). Label wording per VIDEO-RULES 2026-10-17."""
from PIL import ImageDraw
import lib
S = lib.B
W, H, DROP = 1080, 1920, 310
REAL1 = "Real Photo Of Me, Not AI-Generated"
CHIP_U = 1.6
BOX = (90, DROP + 100, 900, 1200)          # 3:4, canvas y 410-1610; the chip sits above it (y 322-386), his abs at about y 900-1150
def tab(im, cx, y, s, t, delay):
    q = S.ease(t - delay)
    if q <= 0: return
    f = S.font(40); tw = S.text_w(s, f); bw, bh = tw + 48, 68
    S.glass(im, (cx - bw / 2, y, cx + bw / 2, y + bh), t, 2.0, radius=16)
    ImageDraw.Draw(im).text((cx - tw / 2, y + 10), s, font=f, fill=S.WHITE)
def photo1(tt, c, t):
    im = S.field(t, W, H)
    S.photo_card(im, c["photo"], BOX, tt, 0.0, fit=True, u=2.0)
    if c.get("tab"): tab(im, W / 2, DROP + 130, c["tab"], tt, 0.1)
    if tt > 0.15: S.disclosure(im, REAL1, (W / 2, DROP + 12), CHIP_U, anchor="mt")
    return im.crop((0, DROP, W, H))
SCENES = {"photo1": photo1}
