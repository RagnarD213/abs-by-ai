"""RO-03 graphics that are not HyperFrames templates (from RO-02; the title chip and the set / rest chip are new), all Soft Blue Light (pinned softblue.py beside this file).
paint(frame, t, items, clip) composites every active item onto the graded presenter frame at output time t.
Full-screen: opener (two AI panels + red X on the heard words), title (PART n OF 6), scene/recap, clip.
Over the presenter: anat (the 3A card holding the two-muscle diagram, stages land on words), count (20-second hold
countdown), url (AbsByAI.com chip). lt / l3 / fact come from hyperframes/from_plan.py through composite.py."""
import sys, os, math, glob, subprocess, functools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import softblue as B
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
FF = B.FF; FPS = B.FPS; U = 2.0
W = "/Volumes/Extreme/_edit_work/ro03"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
TEAL = (45, 212, 191)

def rise(t, d=.55): return B.ease(t, d)

# ------------------------------------------------------------------ section title + recap (RO-10 approved styles)
def title_card(t, step, headline):
    im = B.field(t); x = 150; lines = headline.split("\n"); size = 76
    while size > 56 and max(B.text_w(l, B.font(size)) for l in lines) > 1600: size -= 2
    blockh = 64 + 34 + len(lines) * size * 1.22; y = (1080 - blockh) / 2
    if t > .05:
        a = rise(t); B.rr(im, (x, y + 8, x + 8 + 70 * a, y + 16), B.CYAN, 3)
        B.text(im, (x, y + 30), f"PART {step} OF 6", 30, B.CYAN)
    for i, ln in enumerate(lines):
        tt = t - .18 - i * .22
        if tt > 0: B.text(im, (x - 4, y + 98 + i * size * 1.22 + (1 - rise(tt)) * 26), ln, size)
    return im

def recap_card(t, eyebrow, items, headline):
    im = B.field(t); B.text(im, (150, 110), eyebrow, 30, B.CYAN); B.text(im, (146, 160), headline, 58)
    for i, s in enumerate(items):
        tt = t - .35 - i * .16
        if tt <= 0: continue
        row, col = divmod(i, 2); x = 150 + col * 830; y = 360 + row * 170 + (1 - rise(tt)) * 18
        B.glass(im, (x, y, x + 780, y + 118), t, U, 18)
        B.text(im, (x + 34, y + 34), f"{i + 1}", 44, B.CYAN); B.text(im, (x + 100, y + 38), s, 38)
    return im

# ------------------------------------------------------------------ the opener: title, two AI panels, a red X on each
PANEL = dict(A=(90, 372, 850, 478), B=(980, 372, 850, 478))          # x, y, w, h (16:9, the whole AI clip, nothing cropped)
@functools.lru_cache(8)
def _panel_img(path):
    return Image.open(path).convert("RGB").resize((850, 478), Image.Resampling.LANCZOS)
@functools.lru_cache(1)
def _panel_mask():
    m = Image.new("L", (850, 478)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 849, 477), 26, fill=255); return m
def red_x(im, box, q):
    """A hand-drawn-speed X: stroke 1 over the first 55 %, stroke 2 over the last 55 %. It sits in the middle of the
    panel (arms stop short of the corners, so the AI chip and the label stay clear)."""
    x, y, w, h = box; cx, cy = x + w / 2, y + h / 2 + 14; r = 132
    ss = 2; L = Image.new("RGBA", (im.width * ss, im.height * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    def stroke(p0, p1, k, width, col):
        if k <= 0: return
        k = min(1, k); e = (p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k)
        d.line([(p0[0] * ss, p0[1] * ss), (e[0] * ss, e[1] * ss)], fill=col, width=width * ss)
        for p in (p0, e): d.ellipse(((p[0] - width / 2) * ss, (p[1] - width / 2) * ss, (p[0] + width / 2) * ss, (p[1] + width / 2) * ss), fill=col)
    k1 = 1 - (1 - min(1, q / .55)) ** 3; k2 = 0 if q < .45 else 1 - (1 - min(1, (q - .45) / .55)) ** 3
    for width, col in ((40, (5, 13, 28, 150)), (26, B.BAD + (255,))):
        stroke((cx - r, cy - r), (cx + r, cy + r), k1, width, col); stroke((cx + r, cy - r), (cx - r, cy + r), k2, width, col)
    L = L.resize(im.size, Image.Resampling.LANCZOS); im.paste(L, (0, 0), L)

def opener(t, it, frames, note=None):
    """t = seconds from 0:00. frames = {'A': PIL, 'B': PIL} (the AI clip frames for this instant, 16:9)."""
    im = B.field(t)
    B.rr(im, (90, 96, 168, 104), B.CYAN, 3)
    for i, ln in enumerate(it["title"]): B.text(im, (86, 122 + i * 96), ln, 78)
    for k in ("A", "B"):
        x, y, w, h = PANEL[k]; p = frames[k].copy(); xt = it["x"][k]; on = t >= xt
        if on:                                                   # the crossed-out clip dims under its X
            q = min(1, (t - xt) / .25); p = Image.blend(p, Image.new("RGB", p.size, (5, 13, 28)), .42 * q)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x - 2, y + 10, x + w + 2, y + h + 18), 30, fill=(0, 0, 0, 130))
        sh = sh.filter(ImageFilter.GaussianBlur(16)); im.paste(sh, (0, 0), sh)
        im.paste(p, (x, y), _panel_mask()); B.rr(im, (x, y, x + w, y + h), None, 26, B.GLASS_LINE, 2)
        B.disclosure(im, "AI-GENERATED", (x + 18, y + 18), 1.5)                   # top-left corner of its panel: clear of the X, the man and the title
        lab = it["labels"][k]; f = B.font(34); tw = B.text_w(lab, f)
        B.text(im, (x + w / 2 - tw / 2, y + h + 26), lab, 34, B.BAD if on else B.CYAN)
        if on: red_x(im, PANEL[k], min(1, (t - xt) / .30))
    if note: B.disclosure(im, note, (960, 988), 2.0, anchor="mt")
    return im

# ------------------------------------------------------------------ the two-muscle diagram in the 3A left card
CARD = (36, 70, 752, 1010)
def _chaikin(P, n=3):
    for _ in range(n):
        Q = []
        for a, b in zip(P, P[1:] + P[:1]): Q += [(.75 * a[0] + .25 * b[0], .75 * a[1] + .25 * b[1]), (.25 * a[0] + .75 * b[0], .25 * a[1] + .75 * b[1])]
        P = Q
    return P
def _torso(cx, y0, h):
    """Front-view torso outline (neck and shoulders to the waistband), drawn and smoothed: a diagram, not a body render."""
    half = [(-.10, -.06), (-.13, .02), (-.36, .05), (-.52, .12), (-.50, .30), (-.44, .46), (-.37, .62), (-.365, .76), (-.42, .92), (-.45, 1.0)]
    L = [(cx + x * h, y0 + y * h) for x, y in half]
    P = L + [(2 * cx - x, y) for x, y in reversed(L)]
    return _chaikin(P[:-1] + [P[-1]], 2)
def anat_card(im, t, it):
    """it['stage'] = [t_sixpack, t_deep] (film seconds, relative times are computed by the caller as t - it['t0'])."""
    x0, y0, x1, y1 = CARD; a = rise(t, .40)
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((x0, y0, x1, y1), 32, fill=B.LT_FILL, outline=B.LT_EDGE, width=2)
    f = B.font(56); d.text((x0 + 37, y0 + 30), it["heading"], font=f, fill=B.LT_CYAN)
    d.rectangle((x0 + 37, y0 + 122, x1 - 37, y0 + 125), fill=B.LT_WHITE)
    s1 = t - (it["stage_t"][0] - it["t0"]); s2 = t - (it["stage_t"][1] - it["t0"])
    q1 = rise(s1, .5) if s1 > 0 else 0; q2 = rise(s2, .5) if s2 > 0 else 0
    cx = (x0 + x1) / 2; ty = y0 + 178; th = 452
    T = _torso(cx, ty, th)
    d.polygon(T, fill=(6, 20, 40, 255)); d.line(T + [T[0]], fill=(99, 176, 224, 255), width=4, joint="curve")
    # chest line + navel hint, so it reads as a torso
    d.arc((cx - 150, ty + 60, cx - 6, ty + 170), 20, 160, fill=(99, 176, 224, 150), width=3); d.arc((cx + 6, ty + 60, cx + 150, ty + 170), 20, 160, fill=(99, 176, 224, 150), width=3)
    # deep muscle: a wide belt across the whole waist, horizontal fibres, behind the six pack
    M = Image.new("L", im.size, 0); ImageDraw.Draw(M).polygon(T, fill=255)
    belt = Image.new("RGBA", im.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(belt); by0, by1 = ty + th * .44, ty + th * .95
    bd.rectangle((x0, by0, x1, by1), fill=TEAL + (int(40 + 150 * q2),))
    for k in range(13):
        yy = by0 + 10 + k * (by1 - by0 - 20) / 12; bd.line((x0, yy, x1, yy), fill=(210, 255, 248, int(40 + 150 * q2)), width=2)
    belt.putalpha(Image.composite(belt.getchannel("A"), Image.new("L", im.size, 0), M)); L.alpha_composite(belt)
    d = ImageDraw.Draw(L)
    if q2 > 0: d.line(T + [T[0]], fill=(99, 176, 224, 255), width=4, joint="curve")
    # six pack: 2 x 4 blocks down the middle, in front
    bw, bh, gap = 58, 52, 9; sy = ty + th * .41
    for r in range(4):
        for c in (-1, 0):
            bx = cx + c * (bw + gap) + gap / 2; byy = sy + r * (bh + gap); w_ = bw - (4 if r == 3 else 0)
            col = tuple(int(u + (v - u) * q1) for u, v in zip((22, 51, 81), B.LT_CYAN))
            d.rounded_rectangle((bx + (0 if c == 0 else bw - w_), byy, bx + (w_ if c == 0 else bw), byy + bh), 14, fill=col + (255,), outline=(5, 13, 28, 255), width=2)
    # legend: each row lands with its muscle
    ly = ty + th + 40
    for q, col, head, sub in ((q1, B.LT_CYAN, it["rows"][0][0], it["rows"][0][1]), (q2, TEAL, it["rows"][1][0], it["rows"][1][1])):
        if q > 0:
            o = int((1 - q) * 16); al = int(255 * q)
            d.rounded_rectangle((x0 + 37, ly + 8 + o, x0 + 37 + 36, ly + 44 + o), 9, fill=col + (al,))
            d.text((x0 + 92, ly - 4 + o), head, font=B.font(38), fill=B.LT_WHITE + (al,))
            d.text((x0 + 92, ly + 46 + o), sub, font=B.font(29, False), fill=(205, 226, 244, al))
        ly += 112
    if a < 1:
        L.putalpha(L.getchannel("A").point(lambda v: int(v * a))); L = Image.fromarray(np.roll(np.asarray(L), int((1 - a) * 24), 0))
    out = im.convert("RGBA"); out.alpha_composite(L); return out.convert("RGB")

# ------------------------------------------------------------------ 20-second hold countdown + URL chip
def countdown(im, t, it):
    """Glass chip, top left: HOLD + the seconds left, a bar that empties. it['hold_t'] = film time the hold starts."""
    s = t - (it["hold_t"] - it["t0"]); left = it["secs"] - s
    x, y, w, h = 70, 64, 330, 150
    B.glass(im, (x, y, x + w, y + h), t, U, 18)
    B.rr(im, (x + 28, y + 30, x + 34, y + 62), B.CYAN, 3); B.text(im, (x + 48, y + 26), "HOLD" if s >= 0 else "GET READY", 28, B.CYAN)
    n = it["secs"] if s < 0 else max(0, math.ceil(left - 1e-6))
    B.text(im, (x + 28, y + 62), f"{n}", 62); B.text(im, (x + 28 + B.text_w(f"{n}", B.font(62)) + 12, y + 92), "seconds", 28, (205, 226, 244), bold=False)
    k = 1.0 if s < 0 else max(0, min(1, left / it["secs"]))
    B.rr(im, (x + 200, y + 44, x + w - 28, y + 54), (22, 51, 81), 5)
    if k > 0.02: B.rr(im, (x + 200, y + 44, x + 200 + (w - 228) * k, y + 54), B.CYAN, 5)
    return im

# ------------------------------------------------------------------ RO-03: title chip + the set / rest chip (RO-02's countdown chip, one line added)
CHIP_XY = (70, 64)
def title_chip(im, t, it):
    """Glass chip, top left: eyebrow, the video's name, one line of what the workout is."""
    x, y = CHIP_XY; w = 78 + max(B.text_w(it["headline"], B.font(54)), B.text_w(it["detail"], B.font(28, False))); h = 196
    B.glass(im, (x, y, x + w, y + h), t, U, 18)
    B.rr(im, (x + 28, y + 30, x + 34, y + 62), B.CYAN, 3); B.text(im, (x + 48, y + 26), it["eyebrow"], 28, B.CYAN)
    B.text(im, (x + 28, y + 70), it["headline"], 54); B.text(im, (x + 28, y + 142), it["detail"], 28, (205, 226, 244), bold=False)
    return im
def work_state(tf, it):
    """Film time -> (line, seconds shown, bar 0..1). Hold n runs holds[n] to beeps[n]; a rest runs beeps[n] to holds[n+1]."""
    H, Bp, secs = it["holds"], it["beeps"], it["secs"]; n = len(H)
    for i in range(n):
        if tf < H[i] and (i == 0 or tf >= Bp[i-1]):
            if i == 0: return "SET 1 OF 3: GET READY", secs, 1.0
            left = H[i] - tf; tot = H[i] - Bp[i-1]
            return f"REST. SET {i+1} OF 3 IS NEXT", min(int(round(tot)), max(1, math.ceil(left - 1e-6))), max(0, min(1, left / tot))   # capped at the rest's length: rest 2 measures 30.016 s and read 31 for one frame (round 2 review)
        if H[i] <= tf < Bp[i]:
            left = Bp[i] - tf; return f"SET {i+1} OF 3: HOLD", max(1, math.ceil(left - 1e-6)), max(0, min(1, left / secs))
    return "WORKOUT COMPLETE", 3, 0.0
def work_chip(im, tf, it):
    """Glass chip, top left: which set, HOLD or REST, the seconds left, a bar that empties."""
    line, n, k = work_state(tf, it); x, y = CHIP_XY; w, h = 470, 176
    B.glass(im, (x, y, x + w, y + h), tf, U, 18)
    B.rr(im, (x + 28, y + 30, x + 34, y + 62), B.CYAN, 3); B.text(im, (x + 48, y + 26), line, 28, B.CYAN)
    B.text(im, (x + 28, y + 62), f"{n}", 62); B.text(im, (x + 28 + B.text_w(f"{n}", B.font(62)) + 12, y + 92), "sets done" if line == "WORKOUT COMPLETE" else ("seconds" if n != 1 else "second"), 28, (205, 226, 244), bold=False)
    B.rr(im, (x + 28, y + 142, x + w - 28, y + 152), (22, 51, 81), 5)
    if k > 0.01: B.rr(im, (x + 28, y + 142, x + 28 + (w - 56) * k, y + 152), B.CYAN, 5)
    return im

# ------------------------------------------------------------------ clip sources
def lib_path(cid):
    hits = glob.glob(f"{LIB}/*/*/{cid}_*") + glob.glob(f"{LIB}/*/*/*/{cid}_*"); assert hits, cid; return sorted(hits)[0]
def src_path(s): return s.split("@")[0] if s.startswith("/") else lib_path(s.split("@")[0])
def src_start(s): return float(s.split("@")[1]) if "@" in s else 0.0
def clip_vf(zoom=1.0):
    z = f",scale=iw*{zoom}:ih*{zoom},crop=1920:1080:(iw-1920)/2:(ih-1080)/2" if zoom != 1.0 else ""
    return "scale=1920:1080:force_original_aspect_ratio=increase:in_color_matrix=bt709:in_range=tv,crop=1920:1080" + z + ",format=rgb24"
def clip_frame(path, ts, zoom=1.0):
    p = subprocess.run([FF, "-v", "error", "-ss", f"{ts:.3f}", "-i", path, "-frames:v", "1", "-vf", clip_vf(zoom), "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)

# ------------------------------------------------------------------ compositing one frame
FULL = ("scene", "title", "clip", "opener")
def paint(frame, t, items, clip_img=None, opener_frames=None, note=None):
    act = [it for it in items if it["t0"] <= t < (it["t1"] or it["t0"])]
    full = [it for it in act if it["kind"] in FULL]
    im = frame
    if full: im = clip_img.copy() if clip_img is not None else Image.new("RGB", (1920, 1080))      # RO-03's only full-frame kind is a clip
    for it in act:
        if it["kind"] == "wtitle": im = title_chip(im.copy(), t - it["t0"], it)
        elif it["kind"] == "work": im = work_chip(im.copy(), t, it)
    return im
