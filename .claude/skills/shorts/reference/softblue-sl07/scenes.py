"""SL-07: RO-16's full-screen graphics rebuilt for the vertical picture area (1080 x 1610 under the title band). Each
fn(tt, cover, t_abs) returns the 1080 x 1610 RGB picture; everything sits above y 1070 (canvas y 1380) so the burned
captions (from y 1412) land on the plain field, never on the graphic. Same copy and same numbers as the film's graphic
(recipe gfx.py study_card G18 and chart_card G19), in title case."""
import functools, numpy as np
from PIL import Image, ImageDraw
import lib
S = lib.B
W, H, DROP = 1080, 1920, 310
MUTED = (150, 170, 190); SOFT = (170, 200, 225); DOT = (235, 242, 250)
def _wrapc(im, y, s, px, maxw=960, lh=1.16, fill=None):
    f = S.font(px); lines = s.split("\n") if "\n" in s else S.wrap(s, f, maxw)
    for ln in lines: S.text(im, (60, y), ln, px, fill or S.WHITE); y += round(px * lh)
    return y
def study(tt, c, t):
    """RO-16 G18 'ONE STUDY, 6 MONTHS': two bars, each growing in on its words (c['t1'], c['t2'] = seconds into the scene)."""
    im = S.field(t, W, H); oy = DROP
    S.text(im, (60, oy + 56), "ONE STUDY, 6 MONTHS", 34, S.CYAN)
    y = _wrapc(im, oy + 108, "Daily Weighers Lost\nAbout 13 lb MORE", 72)
    bars = [("Weighed Every Day", 14.4, S.CYAN, "About 14 lb Lost", c.get("t1", 1.0)), ("Didn't Weigh Daily", 0.8, MUTED, "About 1 lb Lost", c.get("t2", 1.4))]
    by = oy + 400; full = 960
    for i, (lab, v, col, vt, d) in enumerate(bars):
        if tt <= d: continue
        q = S.ease(tt - d, .9); yy = by + i * 250
        S.text(im, (60, yy), lab, 44)
        w = max(14, full * v / 14.4 * q)
        S.rr(im, (60, yy + 70, 60 + w, yy + 150), col, 18)
        if q > .6: S.text(im, (60, yy + 166), vt, 40, col)
    if tt > 1.2: S.text(im, (60, oy + 960), "Steinberg et al., J Acad Nutr Diet 2015", 26, SOFT, bold=False)
    return im.crop((0, DROP, W, H))
@functools.lru_cache(1)
def _weights():
    rng = np.random.default_rng(16); days = 28                         # the film's own series (gfx.py _weights)
    trend = 200 - np.arange(days) * (2.4 / 7)
    daily = trend + rng.normal(0, 1.1, days) + np.where(np.arange(days) % 7 == 5, 1.6, 0)
    avg = np.array([daily[max(0, i - 6):i + 1].mean() for i in range(days)])
    return daily, avg
def chart(tt, c, t):
    """RO-16 G19 'WATCH THE 7-DAY AVERAGE': the daily dots arrive as he says the weight bounces; the average line draws on
    'your 7 day moving average' (c['avg_at'] seconds into the scene)."""
    im = S.field(t, W, H); oy = DROP; d = ImageDraw.Draw(im)
    S.text(im, (60, oy + 56), "WATCH THE 7-DAY AVERAGE", 34, S.CYAN)
    _wrapc(im, oy + 108, "Daily Weight Bounces.\nThe Average Tells The Truth.", 58)
    daily, avg = _weights(); n = len(daily); a_at = c.get("avg_at", 1.2)
    px0, px1, py0, py1 = 90, 1000, oy + 400, oy + 900
    lo, hi = daily.min() - 1.5, daily.max() + 1.5
    X = lambda i: px0 + (px1 - px0) * i / (n - 1); Y = lambda v: py1 - (py1 - py0) * (v - lo) / (hi - lo)
    d.line((px0 - 20, py1, px1 + 20, py1), fill=(80, 120, 160), width=3)
    for wk in range(4):
        xx = X(wk * 7); d.line((xx, py1, xx, py1 + 14), fill=(80, 120, 160), width=3)
        S.text(im, (xx + 10, py1 + 22), f"WEEK {wk + 1}", 26, SOFT, bold=False)
    shown = int(min(n, max(0, (tt - .3) * (n / c.get('dots', 3.1)))))            # the 28 dots arrive over c['dots'] seconds
    for i in range(shown):
        r = 11; d.ellipse((X(i) - r, Y(daily[i]) - r, X(i) + r, Y(daily[i]) + r), fill=DOT)
    k = int(min(n, max(0, (tt - a_at) * 12)))
    if k > 1: d.line([(X(i), Y(avg[i])) for i in range(k)], fill=S.CYAN, width=11, joint="curve")
    ly = oy + 300
    d.ellipse((60, ly + 8, 82, ly + 30), fill=DOT); S.text(im, (96, ly), "Daily Weigh-In", 32, bold=False)
    if tt > a_at:
        S.rr(im, (440, ly + 13, 490, ly + 25), S.CYAN, 5); S.text(im, (504, ly), "7-Day Average", 32, S.CYAN)
    return im.crop((0, DROP, W, H))
SCENES = {"study": study, "chart": chart}
if __name__ == "__main__":
    import sys
    for name, tts in (("study", (1.0, 3.0, 6.6)), ("chart", (2.0, 6.0, 12.5))):
        for tt in tts:
            bg = lib.canvas(0); bg.paste(SCENES[name](tt, dict(t1=1.5, t2=5.9, avg_at=8.9), tt), (0, DROP)); lib.band(bg, "LOSE YOUR BELLY FAT", ["Weigh Yourself", "Every Morning"])
            lib.caption(bg, ["sample caption line"]); bg.resize((540, 960)).save(f"probe_scene_{name}_{tt}.jpg", quality=85)
