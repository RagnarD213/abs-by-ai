"""SL-06: RO-12's full-screen graphics rebuilt for the vertical picture area (1080 x 1610 under the title band). Each
fn(tt, cover, t_abs) returns the 1080 x 1610 RGB picture; everything sits above y 1070 (canvas y 1380) so the burned
captions (from y 1412) land on the plain field, never on the graphic. Same copy and same numbers as the film's graphic."""
import sys
from PIL import Image, ImageDraw
import lib
S = lib.B
W, H, DROP = 1080, 1920, 310
def _wrapc(im, y, s, px, maxw=960, lh=1.16, fill=None):
    f = S.font(px); lines = S.wrap(s, f, maxw)
    for ln in lines: S.text(im, (60, y), ln, px, fill or S.WHITE); y += round(px * lh)
    return y
def _bar(im, box, r=22):
    """a narrow glass column: softblue.glass's tint and edge without its wide specular line (it overhangs a column this narrow)."""
    o = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    d.rounded_rectangle(tuple(round(v) for v in box), r, fill=S.GLASS_TINT + (205,), outline=S.GLASS_LINE + (255,), width=2)
    im.paste(Image.alpha_composite(im.convert("RGBA"), o).convert("RGB"))
def week(tt, c, t):
    """RO-12 S03 'HOW ONE WEEKLY SHOT WORKS' (build.py week): seven glass bars, strongest right after the shot, fading by day 7."""
    im = S.field(t, W, H); u = 2; oy = DROP
    S.text(im, (60, oy + 56), "HOW ONE WEEKLY SHOT WORKS", 34, S.CYAN)
    _wrapc(im, oy + 108, "Strongest Right After Your Shot, Fading By Day 7", 62)
    heights = [0.95, 1.0, 0.9, 0.78, 0.64, 0.5, 0.38]; bw, gap = 118, 22; x00 = (W - (7 * bw + 6 * gap)) // 2; y1 = oy + 970
    for i, hgt in enumerate(heights):
        q = S.ease(tt - 0.35 - i * 0.16, .5)
        if q <= 0: continue
        x0 = x00 + i * (bw + gap); hh = 560 * hgt * q
        if hh < 60: continue
        _bar(im, (x0, y1 - hh, x0 + bw, y1))
        S.rr(im, (x0 + 8, y1 - hh + 8, x0 + bw - 8, y1 - hh + 20), S.CYAN, 6)
        lab = f"Day {i + 1}"; f = S.font(30); S.text(im, (x0 + (bw - S.text_w(lab, f)) / 2, y1 + 18), lab, 30)
    if tt > 0.35: S.text(im, (x00 + 4, y1 - 560 * 0.95 - 58), "SHOT", 32, S.CYAN)
    return im.crop((0, DROP, W, H))
def ramp(tt, c, t):
    """RO-12 S02 'THE STARTING RAMP' (build.py ramp): three glass steps, each landing on its word; same copy and numbers."""
    im = S.field(t, W, H); u = 2; oy = DROP
    S.text(im, (60, oy + 56), "THE STARTING RAMP", 34, S.CYAN)
    _wrapc(im, oy + 108, "Step Up Slowly To Avoid Side Effects", 62)
    bw, gap = 300, 30; x00 = (W - (3 * bw + 2 * gap)) // 2; y1 = oy + 1000
    for i, (lab, d) in enumerate(c["steps"]):
        if tt < d: continue
        q = S.ease(tt - d, .5); x0 = x00 + i * (bw + gap); h = 300 + i * 150; y0 = y1 - h + (1 - q) * 40
        _bar(im, (x0, y0, x0 + bw, y1), 26)
        f = S.font(84); S.text(im, (x0 + (bw - S.text_w(lab, f)) / 2, y0 + 36), lab, 84, S.CYAN)
        sub = ["Start here", "Then", "Then"][i]; f2 = S.font(34, bold=False); S.text(im, (x0 + (bw - S.text_w(sub, f2)) / 2, y0 + 150), sub, 34, bold=False)
        if i: ImageDraw.Draw(im).polygon([(x0 - gap + 4, y1 - 82), (x0 - 4, y1 - 60), (x0 - gap + 4, y1 - 38)], fill=S.CYAN)
    return im.crop((0, DROP, W, H))
SCENES = {"week": week, "ramp": ramp}
