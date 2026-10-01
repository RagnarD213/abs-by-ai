"""RO-16 graphics, all Soft Blue Light (pinned copy of _shared/softblue.py beside this file).
paint(frame, t, items) composites every active item onto the graded presenter frame at output time t.
Full-screen items (scene/title/clip/ai) replace the frame; l3 shifts the presenter; lt overlays."""
import sys, os, math, json, glob, subprocess, functools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import softblue as B
from PIL import Image, ImageDraw, ImageOps
import numpy as np
FF = B.FF; FPS = B.FPS; U = 2.0      # unit at 1920x1080
PHOTOS = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/photos/finalized social media photos"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
SHIFT = {"W2": dict(dx=346, c0=560, wall_w=560), "W3": dict(dx=342, c0=520, wall_w=520)}

def rise(t, d=.55): return B.ease(t, d)
# ------------------------------------------------------------------ full-screen scenes
def title_card(t, step, headline):
    im = B.field(t); d = ImageDraw.Draw(im)
    x = 150; lines = headline.split("\n"); size = 76
    while size > 56 and max(B.text_w(l, B.font(size)) for l in lines) > 1600: size -= 2
    blockh = 64 + 34 + len(lines) * size * 1.22
    y = (1080 - blockh) / 2
    if t > .05:
        a = rise(t); B.rr(im, (x, y + 8, x + 8 + 70 * a, y + 16), B.CYAN, 3)
        B.text(im, (x, y + 30), f"STEP {step} OF 8", 30, B.CYAN)
    for i, ln in enumerate(lines):
        tt = t - .18 - i * .22
        if tt > 0: B.text(im, (x - 4, y + 98 + i * size * 1.22 + (1 - rise(tt)) * 26), ln, size)
    return im

def study_card(t, eyebrow, headline, detail, bars):
    """Glass card, headline, then bars [(label, value, color)] growing in; citation line under."""
    im = B.field(t); x0, y0, x1, y1 = 180, 150, 1740, 930
    B.glass(im, (x0, y0, x1, y1), t, U, 22)
    if t > .1: B.text(im, (x0 + 70, y0 + 60), eyebrow, 28, B.CYAN)
    for i, ln in enumerate(headline.split("\n")):
        tt = t - .3 - i * .2
        if tt > 0: B.text(im, (x0 + 66, y0 + 120 + i * 78 + (1 - rise(tt)) * 20), ln, 62)
    by = y0 + 330; vmax = max(v for _, v, _, _ in bars)
    for i, (lab, v, col, vt) in enumerate(bars):
        tt = t - 1.0 - i * .35
        if tt <= 0: continue
        q = rise(tt, .9); y = by + i * 120
        B.text(im, (x0 + 70, y), lab, 30, B.WHITE)
        w = (x1 - x0 - 480) * v / vmax * q
        B.rr(im, (x0 + 70, y + 46, x0 + 70 + max(6, w), y + 92), col, 12)
        if q > .6: B.text(im, (x0 + 90 + w, y + 50), vt, 32, col)
    if t > 1.6: B.text(im, (x0 + 70, y1 - 70), detail, 22, (170, 200, 225), bold=False)
    return im

def split_bar_card(t, eyebrow, headline, detail, parts):
    """One 100 % bar split into parts [(label, share, color)]."""
    im = B.field(t); x0, y0, x1, y1 = 180, 150, 1740, 930
    B.glass(im, (x0, y0, x1, y1), t, U, 22)
    if t > .1: B.text(im, (x0 + 70, y0 + 60), eyebrow, 28, B.CYAN)
    for i, ln in enumerate(headline.split("\n")):
        tt = t - .3 - i * .2
        if tt > 0: B.text(im, (x0 + 66, y0 + 120 + i * 78 + (1 - rise(tt)) * 20), ln, 62)
    bx0, bx1, by = x0 + 70, x1 - 70, y0 + 400; q = rise(t - 1.0, 1.0) if t > 1.0 else 0
    x = bx0
    for lab, share, col in parts:
        w = (bx1 - bx0) * share * q
        if w > 2:
            B.rr(im, (x, by, x + w, by + 110), col, 16)
            if q > .8: B.text(im, (x + 26, by + 128), lab, 30, col)
        x += w
    if t > 1.6: B.text(im, (x0 + 70, y1 - 70), detail, 22, (170, 200, 225), bold=False)
    return im

@functools.lru_cache(1)
def _weights():
    rng = np.random.default_rng(16); days = 28
    trend = 200 - np.arange(days) * (2.4 / 7)
    daily = trend + rng.normal(0, 1.1, days) + np.where(np.arange(days) % 7 == 5, 1.6, 0)
    avg = np.array([daily[max(0, i - 6):i + 1].mean() for i in range(days)])
    return daily, avg

def chart_card(t, eyebrow, headline):
    im = B.field(t); x0, y0, x1, y1 = 150, 120, 1770, 960
    B.glass(im, (x0, y0, x1, y1), t, U, 22)
    B.text(im, (x0 + 60, y0 + 50), eyebrow, 28, B.CYAN)
    B.text(im, (x0 + 56, y0 + 100), headline, 46)
    daily, avg = _weights(); n = len(daily)
    px0, px1, py0, py1 = x0 + 110, x1 - 90, y0 + 230, y1 - 120
    lo, hi = daily.min() - 1.5, daily.max() + 1.5
    X = lambda i: px0 + (px1 - px0) * i / (n - 1); Y = lambda v: py1 - (py1 - py0) * (v - lo) / (hi - lo)
    d = ImageDraw.Draw(im)
    d.line((px0, py1, px1, py1), fill=(80, 120, 160), width=2)
    for wk in range(5):
        xx = X(min(n - 1, wk * 7)); d.line((xx, py1, xx, py1 + 10), fill=(80, 120, 160), width=2)
        if wk < 4: B.text(im, (xx + 8, py1 + 16), f"WEEK {wk + 1}", 20, (150, 185, 215), bold=False)
    shown = int(min(n, max(0, (t - .4) * 14)))
    for i in range(shown):
        r = 9; d.ellipse((X(i) - r, Y(daily[i]) - r, X(i) + r, Y(daily[i]) + r), fill=(235, 242, 250))
    k = int(min(n, max(0, (t - 1.2) * 12)))
    if k > 1: d.line([(X(i), Y(avg[i])) for i in range(k)], fill=B.CYAN, width=9, joint="curve")
    B.rr(im, (px1 - 520, y0 + 190, px1 - 500, y0 + 210), (235, 242, 250), 10)
    B.text(im, (px1 - 488, y0 + 184), "Daily weigh-in", 24, bold=False)
    if t > 1.2:
        B.rr(im, (px1 - 270, y0 + 196, px1 - 230, y0 + 205), B.CYAN, 4)
        B.text(im, (px1 - 220, y0 + 184), "7-day average", 24, B.CYAN)
    return im

def recap_card(t, eyebrow, items):
    im = B.field(t); B.text(im, (150, 110), eyebrow, 30, B.CYAN)
    B.text(im, (146, 160), "What I'd do if I had belly fat", 58)
    for i, s in enumerate(items):
        tt = t - .35 - i * .16
        if tt <= 0: continue
        col, row = divmod(i, 4); x = 150 + col * 830; y = 330 + row * 150 + (1 - rise(tt)) * 18
        B.glass(im, (x, y, x + 780, y + 118), t, U, 18)
        B.text(im, (x + 34, y + 34), f"{i + 1}", 44, B.CYAN)
        B.text(im, (x + 100, y + 38), s, 38)
    return im

def scene(it, t):
    k = it["scene"]
    # labels arrive with their photos (review r1: a chip on screen before any photo, or a plural chip over one photo)
    if k == "fact":
        im = B.scene_fact(t, 1920, 1080, it["photo"], it["eyebrow"], it["headline"], it.get("detail"), None, fit=True)
        if it.get("label") and t > .05: B.disclosure(im, it["label"], (162 * U, 484 * U), U)
        return im
    if k == "portraits":
        ps = [f"{PHOTOS}/{p}_FINAL_PRIMARY.jpg" for p in it["photos"]]
        im = B.scene_portraits(t, 1920, 1080, ps, None)
        if it.get("label") and t > .05: B.disclosure(im, it["label"], (960, 876 + 26 * U), U, anchor="mt")
        return im
    if k == "portraits_codex":
        # Codex's WV-01 three-photo slate mechanics (round9/10 components): cutout on the blue-gray gradient panel,
        # 526x730 panels, natural smiling photos; staggered rise; plural real-photo chip with the photos
        im = B.field(t)
        pw, ph = 526, 730; gap = 50; x0 = (1920 - (3 * pw + 2 * gap)) / 2; y0 = 110
        for i, n in enumerate(it["photos"]):
            B.photo_card(im, f"/Volumes/Extreme/_edit_work/ro16/assets/g03/{n}_panel.png", (x0 + i * (pw + gap), y0, pw, ph), t, i * .22, fit=True, u=U)
        if it.get("label") and t > .05: B.disclosure(im, it["label"], (960, y0 + ph + 34), U, anchor="mt")
        return im
    if k == "photo":
        im = B.scene_photo(t, 1920, 1080, f"{PHOTOS}/{it['photo']}_FINAL_PRIMARY.jpg", None)
        if it.get("label") and t > .05:
            pw, ph = B.photo_size(f"{PHOTOS}/{it['photo']}_FINAL_PRIMARY.jpg", 1920 - 210 * U, 1080 - 115 * U)
            B.disclosure(im, it["label"], (960, (1080 - ph) / 2 - 10 * U + ph + 22 * U), U, anchor="mt")
        return im
    if k == "study" and it["id"] == "G16":
        return split_bar_card(t, it["eyebrow"], it["headline"], it["detail"], [("Fat: about 3 in 4", .75, B.GOOD), ("Lean mass: about 1 in 4", .25, B.BAD)])   # Dan 09-30: fat green, lean mass red
    if k == "study":
        return study_card(t, it["eyebrow"], it["headline"], it["detail"],
                          [("Weighed every day", 14.4, B.CYAN, "about 14 lb lost"), ("Didn't weigh daily", 0.8, (150, 170, 190), "about 1 lb lost")])
    if k == "chart": return chart_card(t, it["eyebrow"], it["headline"])
    if k == "recap": return recap_card(t, it["eyebrow"], it["items"])
    raise KeyError(k)

# ------------------------------------------------------------------ phone (approved RO-05 round-3 iPhone shell)
_SH = {}
def iphone(im, content, ox=0):
    from PIL import ImageFilter
    if ox not in _SH:
        sh = Image.new('RGBA', im.size); ImageDraw.Draw(sh).rounded_rectangle((91+ox, 34, 573+ox, 1062), 68, fill=(0, 0, 0, 120))
        _SH[ox] = sh.filter(ImageFilter.GaussianBlur(14))
    im = Image.alpha_composite(im.convert('RGBA'), _SH[ox]).convert('RGB')
    def rr(box, fill, r, outline=None, width=1): ImageDraw.Draw(im).rounded_rectangle(tuple(v + (ox if i % 2 == 0 else 0) for i, v in enumerate(box)), r, fill=fill, outline=outline, width=width)
    rr((90, 28, 562, 1052), (95, 107, 119), 66, (166, 179, 190), 2); rr((95, 33, 557, 1047), (5, 8, 12), 62)
    scr = Image.new('RGB', (448, 1000), (248, 250, 252)); p = ImageOps.contain(content, (432, 920), Image.Resampling.LANCZOS)
    scr.paste(p, ((448 - p.width)//2, 65)); d = ImageDraw.Draw(scr); d.text((30, 14), '9:41', font=B.font(17), fill=(23, 43, 59))
    for i in range(4): d.rounded_rectangle((352+i*6, 30-i*3, 355+i*6, 35), 1, fill=(25, 32, 40))
    d.rounded_rectangle((391, 22, 418, 34), 3, outline=(25, 32, 40), width=2); d.rectangle((419, 26, 422, 30), fill=(25, 32, 40)); d.rectangle((394, 25, 413, 31), fill=(25, 32, 40))
    d.rounded_rectangle((146, 15, 302, 51), 18, fill=(0, 0, 0)); d.ellipse((276, 26, 288, 38), fill=(18, 26, 36)); d.ellipse((280, 29, 284, 33), fill=(34, 60, 82)); d.rounded_rectangle((153, 984, 295, 989), 3, fill=(24, 28, 32))
    m = Image.new('L', (448, 1000)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 447, 999), 54, fill=255); im.paste(scr, (102+ox, 40), m)
    rr((86, 202, 90, 258), (69, 81, 94), 2); rr((86, 283, 90, 354), (69, 81, 94), 2); rr((562, 253, 566, 352), (86, 96, 110), 2)
    return im

# ------------------------------------------------------------------ clip sources
def lib_path(cid):
    hits = glob.glob(f"{LIB}/*/*/{cid}_*") + glob.glob(f"{LIB}/*/*/*/{cid}_*")
    assert hits, cid; return sorted(hits)[0]
def src_path(s): return s.split("@")[0] if s.startswith("/") else lib_path(s.split("@")[0])
def src_start(s): return float(s.split("@")[1]) if "@" in s else 0.0
def clip_vf(zoom=1.0):
    """scale-to-fill, centre crop (16:9 sources), BT.709 decode; zoom>1 pushes in anchored bottom-right."""
    z = f",scale=iw*{zoom}:ih*{zoom},crop=1920:1080:iw-1920:ih-1080" if zoom != 1.0 else ""
    return "scale=1920:1080:force_original_aspect_ratio=increase:in_color_matrix=bt709:in_range=tv,crop=1920:1080" + z + ",format=rgb24"
def clip_frame(path, ts, zoom=1.0):
    vf = clip_vf(zoom)
    p = subprocess.run([FF, "-v", "error", "-ss", f"{ts:.3f}", "-i", path, "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)

def ai_chip(im, xy=(1866, 54), anchor="rt"):
    B.disclosure(im, "AI-GENERATED", xy, U, anchor=anchor); return im

# ------------------------------------------------------------------ compositing one frame
def paint(frame, t, items, framing="W2", clip_img=None):
    """frame: graded presenter frame at t. Returns the composed frame."""
    act = [it for it in items if it["t0"] <= t < (it["t1"] or it["t0"])]
    full = [it for it in act if it["kind"] in ("scene", "title", "clip", "ai")]
    if full:
        it = full[-1]; tl = t - it["t0"]
        if it["kind"] == "scene": return scene(it, tl)
        if it["kind"] == "title": return title_card(tl, it["step"], it["headline"])
        im = clip_img.copy() if clip_img is not None else Image.new("RGB", (1920, 1080))
        if it.get("label"): ai_chip(im, *(it.get("chip", ((1866, 54), "rt"))))
        return im
    im = frame
    for it in act:
        tl = t - it["t0"]; dur = it["t1"] - it["t0"]
        if it["kind"] == "l3":
            assert framing in ("W2", "W3"), "side cards sit on the wide framing only (T2 + shift pushes his arm off frame)"
            im = B.shift_presenter(im, **SHIFT[framing])
            # the locked 3A reveal: card, heading and divider at 0, items whole at 0, 0.25, 0.50 s (review r1)
            im = B.left_third(im, tl, it["heading"], it["points"], dur=None)
        elif it["kind"] == "phone":
            im = B.shift_presenter(im, **SHIFT[framing])
            im = iphone(im, clip_img if clip_img is not None else Image.new("RGB", (574, 1080), "white"))
            B.disclosure(im, "AbsByAI.com", (600, 54), U, anchor="lt")   # clear of his hair (review r1)
    for it in act:
        if it["kind"] == "lt":
            im = B.lower_third(im, t - it["t0"], it["topic"], it["point"], dur=it["t1"] - it["t0"])
    return im
