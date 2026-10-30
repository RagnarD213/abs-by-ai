"""RO-11 graphics, all Soft Blue Light (pinned copy of _shared/softblue.py beside this file).
paint(frame, t, items) composites every active item onto the graded presenter frame at output time t.
Full-screen items (scene/title/clip/ai) replace the frame; l3 shifts the presenter; lt overlays."""
import sys, os, math, json, glob, subprocess, functools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import softblue as B
from PIL import Image, ImageDraw, ImageOps
import numpy as np
FF = B.FF; FPS = B.FPS; U = 2.0      # unit at 1920x1080
PHOTOS = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/photos/finalized social media photos"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
SHIFT = {"W2": dict(dx=346, c0=560, wall_w=560), "W3": dict(dx=342, c0=520, wall_w=520), "W4": dict(dx=330, c0=450, wall_w=450)}

def rise(t, d=.55): return B.ease(t, d)
# ------------------------------------------------------------------ full-screen scenes
TITLE_FRAME = dict(x=890, w=905, h=900, h_label=820, gap=26)      # round 3: picture on the right of a section card
TITLE_BLEED = dict(x=800, w=1120, ramp=340)
def _chip_in(im, q, label, xy, anchor, size=23):
    """Disclosure chip that fades in with its picture (labels arrive with their photos)."""
    if q <= 0: return im
    if q >= 1: B.disclosure(im, label, xy, U, anchor=anchor, size=size); return im
    c = im.copy(); B.disclosure(c, label, xy, U, anchor=anchor, size=size)
    return Image.blend(im, c, q)

def title_picture(im, t, photo, label=None, layout="frame", chip=None):
    """Round 3 (Dan 2026-10-08: the section cards "look a little empty... add an image to the right"). photo is the stem of a
    prepared crop (titles.py writes <stem>_frame.jpg / <stem>_bleed.jpg at the exact aspect, graded).
    frame: the fact card's photo frame (rounded, hairline border, soft shadow), filling the right side; the label sits
    under the frame, off the picture. bleed: the picture runs off the top, right and bottom edges and fades into the field
    on its left; the label goes at `chip` = ((x, y), anchor), measured clear of his face and abs."""
    if layout == "frame":
        F_ = TITLE_FRAME; fh = F_["h_label"] if label else F_["h"]
        fy = (1080 - fh - ((F_["gap"] + 40 * U) if label else 0)) / 2
        B.photo_card(im, f"{photo}_frame.jpg", (F_["x"], fy, F_["w"], fh), t, 0, fit=True, u=U)
        q = B.ease(t)                                  # the label rises and fades with its picture (photo_card: 48 units)
        if label: im = _chip_in(im, q, label, (F_["x"] + F_["w"] / 2, fy + fh + F_["gap"] + (1 - q) * 48 * U), "mt")
        return im
    D = TITLE_BLEED; q = B.ease(t, .5)
    if q <= 0: return im
    w, h = D["w"], 1080; z = 1.02 + .014 * t
    p = B._src(f"{photo}_bleed.jpg").resize((round(w * z), round(h * z)), Image.Resampling.LANCZOS)
    p = p.crop(((p.width - w) // 2, (p.height - h) // 2, (p.width - w) // 2 + w, (p.height - h) // 2 + h))
    r = np.clip(np.arange(w) / D["ramp"], 0, 1); r = r * r * (3 - 2 * r)
    m = Image.fromarray(np.tile((r * 255 * q).astype("uint8"), (h, 1)))
    im.paste(p, (D["x"], 0), m)
    if label and chip: im = _chip_in(im, q, label, tuple(chip[0]), chip[1])
    return im

def title_card(t, step, headline, photo=None, label=None, layout="frame", chip=None):
    im = B.field(t)
    if photo: im = title_picture(im, t, photo, label, layout, chip)
    d = ImageDraw.Draw(im)
    x = 150; lines = headline.split("\n"); size = 76
    while size > 56 and max(B.text_w(l, B.font(size)) for l in lines) > (700 if photo else 1600): size -= 2
    blockh = 64 + 34 + len(lines) * size * 1.22
    y = (1080 - blockh) / 2
    if t > .05:
        a = rise(t); B.rr(im, (x, y + 8, x + 8 + 70 * a, y + 16), B.CYAN, 3)
        B.text(im, (x, y + 30), step if isinstance(step, str) else f"FOOD {step} OF 3", 30, B.CYAN)
    for i, ln in enumerate(lines):
        tt = t - .18 - i * .22
        if tt > 0: B.text(im, (x - 4, y + 98 + i * size * 1.22 + (1 - rise(tt)) * 26), ln, size)
    return im

def study_card(t, eyebrow, headline, detail, bars, rts=None):
    """Glass card, headline, then bars [(label, value, color)] growing in; citation line under."""
    im = B.field(t); x0, y0, x1, y1 = 180, 150, 1740, 930
    B.glass(im, (x0, y0, x1, y1), t, U, 22)
    if t > .1: B.text(im, (x0 + 70, y0 + 60), eyebrow, 28, B.CYAN)
    for i, ln in enumerate(headline.split("\n")):
        tt = t - .3 - i * .2
        if tt > 0: B.text(im, (x0 + 66, y0 + 120 + i * 78 + (1 - rise(tt)) * 20), ln, 62)
    by = y0 + 330; vmax = max(v for _, v, _, _ in bars)
    lw = max(B.text_w(vt, B.font(32, True)) for _, _, _, vt in bars)   # RO-18 re-check: the longest value label stays inside the card
    wmax = min(x1 - x0 - 480, x1 - 60 - (x0 + 90) - lw)
    for i, (lab, v, col, vt) in enumerate(bars):
        tt = t - (rts[i] if rts else 1.0 + i * .35)          # RO-18: each row on its word when the plan gives reveal times
        if tt <= 0: continue
        q = rise(tt, .9); y = by + i * 120
        B.text(im, (x0 + 70, y), lab, 30, B.WHITE)
        w = wmax * v / vmax * q
        B.rr(im, (x0 + 70, y + 46, x0 + 70 + max(6, w), y + 92), col, 12)
        if q > .6: B.text(im, (x0 + 90 + w, y + 50), vt, 32, col)
    # the detail line: on its own word when the plan gives one more reveal than bars, else just after the last row lands
    dt = rts[len(bars)] if rts and len(rts) > len(bars) else (max(rts[:len(bars)]) + .6 if rts else 1.6)
    if t > dt: B.text(im, (x0 + 70, y1 - 70), detail, 22, (170, 200, 225), bold=False)
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

def recap_card(t, eyebrow, items, headline="What I'd do if I had belly fat", rts=None, photo=None, label=None, chip=None):
    """RO-14: items land on their words (rts); with a photo, one column on the left and the picture bled in on the right
    (the section card's 'bleed' layout); five items without a photo go 3 + 2 over the full width."""
    im = B.field(t)
    if photo: im = title_picture(im, t, photo, label, "bleed", chip)
    B.text(im, (150, 110), eyebrow, 30, B.CYAN)
    B.text(im, (146, 160), headline, 58)
    per = 4 if (photo or len(items) != 5) else 3; dy = 150 if per == 4 else 170; y0 = 330 if per == 4 else 360
    for i, s in enumerate(items):
        tt = t - (rts[i] if rts else .35 + i * .16)
        if tt <= 0: continue
        col, row = divmod(i, per); x = 150 + col * 830; y = y0 + row * dy + (1 - rise(tt)) * 18
        B.glass(im, (x, y, x + (620 if photo else 780), y + 118), t, U, 18)
        B.text(im, (x + 34, y + 34), f"{i + 1}", 44, B.CYAN)
        sz = 38; room = (620 if photo else 780) - 130
        while sz > 28 and B.text_w(s, B.font(sz)) > room: sz -= 1          # RO-14: a long item shrinks to fit its box
        B.text(im, (x + 100, y + 38 + (38 - sz) * .5), s, sz)
    return im

def swap_card(t, it):
    """RO-17 closing card: THROW OUT (left, red cross) / REPLACE WITH (right, green tick), two glass columns on the field;
    each row rises on the word that names it (it["reveal_left_t"] / it["reveal_right_t"], seconds from the item's start)."""
    im = B.field(t)
    cols = [("THROW OUT", it["left"], it["reveal_left_t"], B.BAD, "x"), ("REPLACE WITH", it["right"], it["reveal_right_t"], B.GOOD, "v")]
    for c, (head, rows, rts, col, mark) in enumerate(cols):
        x0 = 200 + c * 800; y0 = 235                         # block centred: header 235, rows to about 855
        if t > .05 + c * .1:
            a = rise(t - .05 - c * .1); B.rr(im, (x0, y0 + 8, x0 + 8 + 70 * a, y0 + 16), col, 3)
            B.text(im, (x0, y0 + 30), head, 34, col)
        for i, (s, rt) in enumerate(zip(rows, rts)):
            tt = t - rt
            if tt <= 0: continue
            y = y0 + 110 + i * 170 + (1 - rise(tt)) * 22
            B.glass(im, (x0, y, x0 + 720, y + 136), t, U, 20)
            d = ImageDraw.Draw(im); cx, cy = x0 + 70, y + 68
            if mark == "x":
                d.line((cx - 22, cy - 22, cx + 22, cy + 22), fill=col, width=9); d.line((cx - 22, cy + 22, cx + 22, cy - 22), fill=col, width=9)
            else:
                d.line((cx - 24, cy + 2, cx - 6, cy + 20), fill=col, width=9); d.line((cx - 6, cy + 20, cx + 26, cy - 20), fill=col, width=9)
            B.text(im, (x0 + 130, y + 40), s, 50)
    return im


def week_card(t, it):
    """RO-14: one dieting week. Five weekday bars go DOWN (the deficit, green, -500 each) as he says them, a running total
    counts with them; then Friday night and Saturday go UP (red) and the total climbs back to zero. Each bar lands on its
    word (it["reveal_days_t"], seconds from the item's start)."""
    im = B.field(t); d = ImageDraw.Draw(im)
    days = it["days"]; rts = it["reveal_days_t"]
    B.text(im, (150, 96), it["eyebrow"], 30, B.CYAN)
    B.text(im, (146, 146), it["headline"], 56)
    x0, x1, zy = 190, 1730, 620; sc = 0.22                     # px per calorie
    d.line((x0 - 20, zy, x1 + 20, zy), fill=(120, 165, 205), width=3)
    B.text(im, (x0 - 20, zy - 44), "0", 26, (150, 185, 215), bold=False)
    n = len(days); cw = (x1 - x0) / n; tot = 0.0
    for i, ((lab, val), rt) in enumerate(zip(days, rts)):
        cx = x0 + cw * i + cw / 2; bw = cw * 0.56
        B.text(im, (cx - B.text_w(lab, B.font(24, True)) / 2, 880), lab, 24, (170, 200, 225))
        tt = t - rt
        if tt <= 0: continue
        q = rise(tt, .45); h = abs(val) * sc * q; col = B.GOOD if val < 0 else B.BAD
        box = (cx - bw / 2, zy, cx + bw / 2, zy + h) if val < 0 else (cx - bw / 2, zy - h, cx + bw / 2, zy)
        B.rr(im, box, col, 10)
        if q > .5:
            vt = f"{'+' if val > 0 else '-'}{abs(val):,}"
            ty = zy + h + 10 if val < 0 else zy - h - 46
            B.text(im, (cx - B.text_w(vt, B.font(30, True)) / 2, ty), vt, 30, col)
        tot += val * q
    # running total, bottom right
    shown = int(round(tot / 10.0)) * 10
    lab = "WEEK TOTAL"; vt = f"{shown:+,}" if shown else "0"
    B.glass(im, (1330, 930, 1770, 1040), t, U, 18)
    B.text(im, (1360, 950), lab, 24, B.CYAN)
    B.text(im, (1360, 982), vt + " cal", 40, B.GOOD if shown < 0 else (B.WHITE if shown == 0 else B.BAD))
    return im


def tiles_card(t, it):
    """RO-18: six equipment pictures in a 3 x 2 grid, each rising on the word that names it (it["reveal_items_t"]), its name
    under it. Pictures are cover-cropped into rounded frames on the field."""
    im = B.field(t)
    B.text(im, (150, 92), it["eyebrow"], 30, B.CYAN)
    B.text(im, (146, 140), it["headline"], 58)
    rts = it.get("reveal_items_t") or [.3 + i * .25 for i in range(len(it["tiles"]))]
    tw, th, gx, gy = 500, 300, 60, 70; x0 = (1920 - (3 * tw + 2 * gx)) / 2; y0 = 290
    for i, ((lab, path, _), rt) in enumerate(zip(it["tiles"], rts)):
        tt = t - rt
        if tt <= 0: continue
        c, r = i % 3, i // 3; x = x0 + c * (tw + gx); y = y0 + r * (th + gy + 40) + (1 - rise(tt)) * 20
        B.photo_card(im, path, (x, y, tw, th), tt, 0, fit=True, u=U)
        if tt > .15: B.text(im, (x + 4, y + th + 16), lab, 32)
    if it.get("footer") and it.get("reveal_t") and t > it["reveal_t"][0]:
        q = rise(t - it["reveal_t"][0]); f = it["footer"]
        B.text(im, (1770 - B.text_w(f, B.font(48, True)), 150 + (1 - q) * 14), f, 48, B.CYAN)   # right-aligned on the headline row
    return im

def dictate_card(t, it):
    """RO-18: what you say (an example with ums and a change of mind) against what Wispr Flow types. Rows land on their
    words: [0] what you say, [1] the ums struck out, [2] the typed version."""
    im = B.field(t); d = ImageDraw.Draw(im)
    rts = it.get("reveal_t") or [.3, 1.5, 3.0]
    x0, x1 = 200, 1720
    B.glass(im, (x0, 170, x1, 470), t, U, 22)
    B.text(im, (x0 + 60, 205), "WHAT YOU SAY", 28, (170, 200, 225))
    if t > rts[0]:
        q = rise(t - rts[0]); say = it["say"]
        B.text(im, (x0 + 56, 270 + (1 - q) * 16), "\u201c" + say + "\u201d", 46, (225, 233, 242), bold=False)
        if t > rts[1]:
            # strike the filler and the first, abandoned time: "Um, so," and "at five, no wait,"
            f = B.font(46, False); pre = "\u201c"
            for frag in ("Um, so, ", "at five, no wait, "):
                a = say.index(frag); xs = x0 + 56 + B.text_w(pre + say[:a], f); xe = xs + B.text_w(frag.rstrip(), f)
                k = min(1, (t - rts[1]) / .35); d.line((xs, 300, xs + (xe - xs) * k, 300), fill=B.BAD, width=6)
    B.glass(im, (x0, 540, x1, 860), t, U, 22)
    B.text(im, (x0 + 60, 575), "WHAT WISPR FLOW TYPES", 28, B.CYAN)
    if t > rts[2]:
        q = rise(t - rts[2]); B.text(im, (x0 + 56, 650 + (1 - q) * 16), it["typed"], 62)
    return im

def split_card(t, it):
    """RO-18: one bar in parts, each part growing in on its word (it["reveal_t"]), its label under it."""
    im = B.field(t); x0, y0, x1, y1 = 180, 150, 1740, 930
    B.glass(im, (x0, y0, x1, y1), t, U, 22)
    if t > .1: B.text(im, (x0 + 70, y0 + 60), it["eyebrow"], 28, B.CYAN)
    for i, ln in enumerate(it["headline"].split("\n")):
        tt = t - .3 - i * .2
        if tt > 0: B.text(im, (x0 + 66, y0 + 120 + i * 78 + (1 - rise(tt)) * 20), ln, 62)
    rts = it.get("reveal_t") or [1.0 + i * .5 for i in range(len(it["parts"]))]
    bx0, bx1, by = x0 + 70, x1 - 70, y0 + 400; x = bx0
    for (lab, share, col), rt in zip(it["parts"], rts):
        q = rise(t - rt, .8) if t > rt else 0; w = (bx1 - bx0) * share * q
        if w > 2:
            B.rr(im, (x, by, x + w, by + 110), tuple(col), 16)
            if q > .8: B.text(im, (x + 26, by + 128), lab, 30, tuple(col))
        x += (bx1 - bx0) * share
    if t > 1.6 and it.get("detail"): B.text(im, (x0 + 70, y1 - 70), it["detail"], 22, (170, 200, 225), bold=False)
    return im

def scene(it, t):
    k = it["scene"]
    # labels arrive with their photos (review r1: a chip on screen before any photo, or a plural chip over one photo)
    if k == "fact":
        im = B.scene_fact(t, 1920, 1080, it["photo"], it["eyebrow"], it["headline"], it.get("detail"), None, fit=True)
        if it.get("label") and t > 0: B.disclosure(im, it["label"], (162 * U, 484 * U), U)
        return im
    if k == "portraits":
        ps = [f"{PHOTOS}/{p}_FINAL_PRIMARY.jpg" for p in it["photos"]]
        im = B.scene_portraits(t, 1920, 1080, ps, None)
        if it.get("label") and t > 0: B.disclosure(im, it["label"], (960, 876 + 26 * U), U, anchor="mt")
        return im
    if k == "portraits_codex":
        # Codex's WV-01 three-photo slate mechanics (round9/10 components): cutout on the blue-gray gradient panel,
        # 526x730 panels, natural smiling photos; staggered rise; plural real-photo chip with the photos
        im = B.field(t)
        pw, ph = 526, 730; gap = 50; x0 = (1920 - (3 * pw + 2 * gap)) / 2; y0 = 110
        for i, n in enumerate(it["photos"]):
            B.photo_card(im, f"/Volumes/Expansion/_edit_work/RO-29/round2/assets/g03/{n}_panel.png", (x0 + i * (pw + gap), y0, pw, ph), t, i * .22, fit=True, u=U)
        if it.get("label") and t > 0: B.disclosure(im, it["label"], (960, y0 + ph + 34), U, anchor="mt")
        return im
    if k == "photo":
        pp = it["photo"] if it["photo"].startswith("/") else f"{PHOTOS}/{it['photo']}_FINAL_PRIMARY.jpg"
        im = B.scene_photo(t, 1920, 1080, pp, None)
        if it.get("label") and t > 0:
            pw, ph = B.photo_size(pp, 1920 - 210 * U, 1080 - 115 * U)
            B.disclosure(im, it["label"], (960, (1080 - ph) / 2 - 10 * U + ph + 22 * U), U, anchor="mt")
        return im
    if k == "study" and it.get("bars"):
        return study_card(t, it["eyebrow"], it["headline"], it["detail"], [(b[0], b[1], tuple(b[2]), b[3]) for b in it["bars"]], it.get("reveal_t"))
    if k == "week": return week_card(t, it)
    if k == "tiles": return tiles_card(t, it)
    if k == "dictate": return dictate_card(t, it)
    if k == "split": return split_card(t, it)
    if k == "study":
        return study_card(t, it["eyebrow"], it["headline"], it["detail"],
                          [("Weighed every day", 14.4, B.CYAN, "about 14 lb lost"), ("Didn't weigh daily", 0.8, (150, 170, 190), "about 1 lb lost")])
    if k == "chart": return chart_card(t, it["eyebrow"], it["headline"])
    if k == "swap": return swap_card(t, it)
    if k == "recap": return recap_card(t, it["eyebrow"], it["items"], it.get("headline", "What I'd do if I had belly fat"), it.get("reveal_items_t"), it.get("photo"), it.get("label"), it.get("chip"))
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
def clip_vf(zoom=1.0, grade=None, crop=None):
    """scale-to-fill, centre crop (16:9 sources), BT.709 decode; zoom>1 pushes in anchored bottom-right; grade = an optional
    per-clip ffmpeg eq (RO-17: flat, washed stock lifted to sit with the film, VIDEO-RULES 2026-10-11 "All B-roll is colour corrected")."""
    z = f",scale=iw*{zoom}:ih*{zoom},crop=1920:1080:iw-1920:ih-1080" if zoom != 1.0 else ""
    g = f",{grade}" if grade else ""
    c = f"crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}," if crop else ""      # RO-28: a source window (w, h, x, y) before the fill, e.g. Dan larger in a wide pool shot
    return c + "scale=1920:1080:force_original_aspect_ratio=increase:in_color_matrix=bt709:in_range=tv,crop=1920:1080" + z + g + ",format=rgb24"
def clip_frame(path, ts, zoom=1.0, grade=None, crop=None):
    vf = clip_vf(zoom, grade, crop)
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
        if it["kind"] == "title": return title_card(tl, it["step"], it["headline"], it.get("photo"), it.get("label"), it.get("layout", "frame"), it.get("chip"))
        im = clip_img.copy() if clip_img is not None else Image.new("RGB", (1920, 1080))
        lab = it.get("label")
        if it.get("labels"):                     # per-source labels on a multi-source clip (same split as build.ClipReader)
            FPS = 30000/1001; n = int(round(it["t1"]*FPS)) - int(round(it["t0"]*FPS)); per = n // len(it["labels"])
            lab = it["labels"][min(int(round(tl*FPS)) // per, len(it["labels"]) - 1)]
        if lab: ai_chip(im, *(it.get("chip", ((1866, 54), "rt"))))
        return im
    im = frame
    for it in act:
        tl = t - it["t0"]; dur = it["t1"] - it["t0"]
        if it["kind"] == "l3":
            assert framing in ("W2", "W3", "W4"), "side cards sit on the wide framing only (T2 + shift pushes his arm off frame)"
            im = B.shift_presenter(im, **SHIFT[framing])
            # the locked 3A reveal: card, heading and divider at 0, items whole at 0, 0.25, 0.50 s (review r1)
            im = B.left_third(im, tl, it["heading"], it["points"], dur=None)
        elif it["kind"] == "phone":
            im = B.shift_presenter(im, **SHIFT[framing])
            im = iphone(im, clip_img if clip_img is not None else Image.new("RGB", (574, 1080), "white"))
            B.disclosure(im, it.get("credit", "AbsByAI.com"), (326, 930), U, anchor="mt", size=11)   # RO-29: the TikTok creator's credit, in the phone's empty band under the video (top-left chip touched his hair)
    for it in act:
        if it["kind"] == "lt":
            im = B.lower_third(im, t - it["t0"], it["topic"], it["point"], dur=it["t1"] - it["t0"])
    return im
