#!/usr/bin/env python3
"""motionlib — animated graphics for Abs By AI video edits (PIL frame sequences -> alpha MOV).

Why this exists
---------------
Our edits used to overlay STATIC PNGs. The Upwork trial edit that beat our rev-4 used a
Premiere MOGRT template pack: cards that scale in, bullet lists that build with the
speech, chips that slide, boxes that draw themselves. Everything in that pack is
reproducible with PIL + ffmpeg, and this module is that pack.

How it is used
--------------
Every component renders an RGBA PNG sequence and encodes it to a QuickTime RLE .mov
(lossless, real alpha channel). The layout script overlays those with ffmpeg:

    [base][gfx]overlay=x:y:enable='between(t,A,B)'

QTRLE is used deliberately: libx264 cannot carry alpha, and pre-multiplying against a
guessed background is how graphics end up with grey fringes.

Conventions
-----------
* 1920x1080, 30000/1001 fps. Components take `dur` in SECONDS.
* Times inside a component are relative to that component's own start.
* Text is drawn with PIL, never ffmpeg drawtext (kerning + emoji + wrapping).
* Nothing here reads or writes global state; every function returns the path it wrote.

Style
-----
The palette below is the Abs By AI CONTENT style: bright paper background, near-black
ink, brand red accent, white cards with soft shadows, Manrope throughout. It is NOT the
dark J2 tactical system used for paid-ad graphics -- see the skill's Step 5.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, shutil, subprocess, tempfile

FF   = os.environ.get("MOTIONLIB_FFMPEG",
                      "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg")
W, H = 1920, 1080
FPS  = 30000 / 1001

# ---------------------------------------------------------------- palette / type
PAPER      = (243, 245, 248)      # page background
PAPER_WARM = (247, 249, 251)      # radial centre -- keep the delta small: a 9-level
                                  # lift shows as a soft blob on a large flat panel
INK        = (17, 21, 28)         # headline / body text
INK_SOFT   = (92, 102, 116)       # secondary text
RED        = (226, 34, 34)        # brand accent
RED_DEEP   = (176, 22, 22)
CARD       = (255, 255, 255)
SHADOW     = (14, 20, 32)

MANROPE = os.path.expanduser("~/Library/Fonts/Manrope.ttf")

_FONT_CACHE = {}
def font(size, weight="Bold"):
    """Manrope at a named weight. Falls back to Arial if Manrope is missing."""
    key = (size, weight)
    if key in _FONT_CACHE: return _FONT_CACHE[key]
    try:
        f = ImageFont.truetype(MANROPE, size)
        f.set_variation_by_name(weight)
    except Exception:
        alt = ("/System/Library/Fonts/Supplemental/Arial Black.ttf"
               if weight in ("ExtraBold", "Bold") else
               "/System/Library/Fonts/Supplemental/Arial.ttf")
        f = ImageFont.truetype(alt, size)
    _FONT_CACHE[key] = f
    return f

# ---------------------------------------------------------------- easing
def clamp01(t):            return 0.0 if t < 0 else (1.0 if t > 1 else t)
def linear(t):             return clamp01(t)
def ease_out_cubic(t):     t = clamp01(t); return 1 - (1 - t) ** 3
def ease_in_cubic(t):      t = clamp01(t); return t ** 3
def ease_in_out(t):
    t = clamp01(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

def ease_out_back(t, overshoot=1.03):
    """Settles just past 1.0 then back -- the 'spring' feel of a MOGRT card."""
    t = clamp01(t)
    c1 = (overshoot - 1.0) * 12.0
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def ease_out_expo(t):
    t = clamp01(t)
    return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)

# ---------------------------------------------------------------- drawing primitives
def paper_bg(w=W, h=H, base=PAPER, centre=PAPER_WARM):
    """Flat brand background with a soft radial lift in the middle.

    Built small and upscaled -- a per-pixel radial at 1920x1080 costs ~2s a frame and
    this is a static layer.
    """
    sm = Image.new("RGB", (96, 54))
    px = sm.load()
    for y in range(54):
        for x in range(96):
            d = math.hypot((x - 48) / 48, (y - 27) / 27)
            k = clamp01(1 - d * 0.85)
            px[x, y] = tuple(int(base[i] + (centre[i] - base[i]) * k) for i in range(3))
    return sm.resize((w, h), Image.BICUBIC)

def drop_shadow(size, box, radius, blur=26, spread=8, opacity=60, offset=(0, 10)):
    """Soft shadow layer for a rounded rect. Returns an RGBA image of `size`."""
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 - spread + offset[0], y0 - spread + offset[1],
                         x1 + spread + offset[0], y1 + spread + offset[1]],
                        radius=radius + spread, fill=SHADOW + (opacity,))
    return lay.filter(ImageFilter.GaussianBlur(blur))

def card(im, box, radius=28, fill=CARD, shadow=True, outline=None, width=0):
    """Draw a rounded card with a soft shadow onto RGBA image `im` (in place)."""
    if shadow:
        im.alpha_composite(drop_shadow(im.size, box, radius))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=radius, fill=fill,
                        outline=outline, width=width if outline else 0)

def fit_cover(img, w, h):
    """Centre-crop `img` to exactly w x h without distortion."""
    ar_src, ar_dst = img.width / img.height, w / h
    if ar_src > ar_dst:
        nw = int(img.height * ar_dst)
        img = img.crop(((img.width - nw) // 2, 0, (img.width - nw) // 2 + nw, img.height))
    else:
        nh = int(img.width / ar_dst)
        img = img.crop((0, (img.height - nh) // 2, img.width, (img.height - nh) // 2 + nh))
    return img.resize((w, h), Image.LANCZOS)

def fit_contain(img, w, h):
    """Scale `img` to fit inside w x h, whole subject preserved. Returns the scaled image.

    Use this for photographs of people: cover-cropping a portrait cuts the top of the
    head or the shorts line, which is a standing rejection (see /coverimage).
    """
    k = min(w / img.width, h / img.height)
    return img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)

def rounded_photo(img, w, h, radius=20, mode="contain", bg=CARD):
    """Photo on a rounded white plate. `contain` never crops the subject."""
    plate = Image.new("RGBA", (w, h), bg + (255,))
    ph = fit_cover(img, w, h) if mode == "cover" else fit_contain(img, w, h)
    plate.paste(ph.convert("RGB"), ((w - ph.width) // 2, (h - ph.height) // 2))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    plate.putalpha(mask)
    return plate

_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def text_bbox(txt, f):
    """Ink bounds relative to a draw at (0,0) with anchor='lt'.

    PIL's 'lt' anchor is the top of the ASCENDER, not the top of the ink, so a rule
    placed at y + text_height lands inside the glyphs. Always position from bbox[3]
    (ink bottom) instead -- that bug shipped a strikethrough headline once.
    """
    return _MEASURE.textbbox((0, 0), txt, font=f)

def text_size(txt, f):
    b = text_bbox(txt, f)
    return b[2] - b[0], b[3] - b[1]

def ink_bottom(txt, f): return text_bbox(txt, f)[3]
def ink_top(txt, f):    return text_bbox(txt, f)[1]

def wrap(txt, f, maxw):
    out, line = [], ""
    for word in txt.split():
        t = (line + " " + word).strip()
        if text_size(t, f)[0] <= maxw or not line: line = t
        else: out.append(line); line = word
    if line: out.append(line)
    return out

def chip(im, xy, txt, f, fill, fg, radius=10, padx=18, pady=10, shadow=False):
    """Small solid label block. Returns (w, h) of the chip drawn at xy."""
    tw, th = text_size(txt, f)
    w, h = tw + padx * 2, th + pady * 2
    box = [xy[0], xy[1], xy[0] + w, xy[1] + h]
    if shadow: im.alpha_composite(drop_shadow(im.size, box, radius, blur=16, spread=4, opacity=48))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=radius, fill=fill)
    d.text((xy[0] + padx, xy[1] + pady), txt, font=f, fill=fg, anchor="lt")
    return w, h

def dashed_arrow(im, p0, p1, progress=1.0, color=INK, width=6, dash=22, gap=16, head=26):
    """Dashed line from p0 to p1, drawn left->right by `progress` (0..1), then a head."""
    d = ImageDraw.Draw(im)
    x0, y0 = p0; x1, y1 = p1
    total = math.hypot(x1 - x0, y1 - y0)
    if total < 1: return
    ux, uy = (x1 - x0) / total, (y1 - y0) / total
    shown = total * clamp01(progress)
    s = 0.0
    while s < shown - 1:
        e = min(s + dash, shown)
        d.line([x0 + ux * s, y0 + uy * s, x0 + ux * e, y0 + uy * e],
               fill=color, width=width)
        s += dash + gap
    if progress > 0.86:                       # head fades/scales in at the end
        k = clamp01((progress - 0.86) / 0.14)
        hx, hy = x0 + ux * total, y0 + uy * total
        L = head * k
        d.polygon([(hx, hy), (hx - L * ux + L * 0.55 * uy, hy - L * uy - L * 0.55 * ux),
                   (hx - L * ux - L * 0.55 * uy, hy - L * uy + L * 0.55 * ux)], fill=color)

def stroke_box(im, box, progress=1.0, color=RED, width=8, radius=16, glow=0.0):
    """Rectangle whose stroke DRAWS ITSELF clockwise from the top-left over `progress`.

    `glow` (0..1) adds a soft outer halo -- use it to pulse after the draw completes.
    """
    x0, y0, x1, y1 = box
    if glow > 0.01:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle(box, radius=radius, outline=color + (int(190 * glow),),
                                            width=width + 10)
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)))
    p = clamp01(progress)
    if p >= 0.999:
        ImageDraw.Draw(im).rounded_rectangle(box, radius=radius, outline=color, width=width)
        return
    w_, h_ = x1 - x0, y1 - y0
    per = 2 * (w_ + h_)
    run = per * p
    d = ImageDraw.Draw(im)
    segs = [((x0, y0), (x1, y0), w_), ((x1, y0), (x1, y1), h_),
            ((x1, y1), (x0, y1), w_), ((x0, y1), (x0, y0), h_)]
    for (a, b, L) in segs:
        if run <= 0: break
        k = min(1.0, run / L)
        d.line([a[0], a[1], a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k],
               fill=color, width=width)
        run -= L

def pop_text(im, t, txt, f, centre, in_dur=0.36, color=INK, accent=RED, rule=True):
    """Letter-by-letter snap-in, drawn onto `im` for local time `t`.

    Each glyph gets its own tile so it can scale about its own centre -- scaling a
    canvas-sized layer about an off-centre anchor translates the whole frame instead.
    """
    txt = txt.upper()
    tw, th = text_size(txt, f)
    b = text_bbox(txt, f)
    top = -(b[1] + b[3]) / 2
    ax, ay = centre
    d = ImageDraw.Draw(im)
    x = ax - tw / 2
    step = in_dur / max(1, len(txt))
    pad = int(f.size * 0.6)
    for ci, ch_ in enumerate(txt):
        adv = d.textlength(ch_, font=f)
        cp = ease_out_back((t - ci * step * 0.55) / (step * 2.2))
        if cp <= 0.02 or ch_ == " ":
            x += adv; continue
        gw, gh = int(adv) + pad * 2, int(f.size * 1.9)
        gl = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
        ImageDraw.Draw(gl).text((pad, gh / 2 + top), ch_, font=f, fill=color, anchor="lt")
        k = 0.72 + 0.28 * cp
        sc = gl.resize((max(1, int(gw * k)), max(1, int(gh * k))), Image.LANCZOS)
        im.alpha_composite(with_alpha(sc, clamp01(cp * 1.4)),
                           (int(x + adv / 2 - sc.width / 2), int(ay - sc.height / 2)))
        x += adv
    if rule:
        up = ease_out_expo((t - in_dur * 0.4) / 0.4)
        if up > 0.01:
            d.rounded_rectangle([ax - tw / 2 - 10, ay + th / 2 + 24,
                                 ax - tw / 2 - 10 + (tw + 20) * up, ay + th / 2 + 38],
                                radius=7, fill=accent)


def panel_plate(box, radius=26, w=W, h=H, base=PAPER, centre=PAPER_WARM, shadow=True):
    """Brand background with a rounded WINDOW punched out of it.

    Composite order is: base video -> the clip (square corners, filling `box`) -> this
    plate. The plate's opaque paper covers everything outside the rounded rect, so the
    clip ends up with real rounded corners and a shadow without needing a per-frame
    mask. Video panels get the same card treatment as photo cards this way.
    """
    plate = paper_bg(w, h, base, centre).convert("RGBA")
    if shadow:
        plate.alpha_composite(drop_shadow((w, h), box, radius, blur=30, spread=10, opacity=64))
    hole = Image.new("L", (w, h), 255)
    ImageDraw.Draw(hole).rounded_rectangle(box, radius=radius, fill=0)
    plate.putalpha(Image.composite(plate.getchannel("A"), Image.new("L", (w, h), 0), hole))
    return plate


def scale_about(layer, k, anchor=None, canvas=(W, H)):
    """Scale an RGBA layer about a point and return a canvas-sized RGBA image."""
    out = Image.new("RGBA", canvas, (0, 0, 0, 0))
    if k <= 0: return out
    nw, nh = max(1, int(layer.width * k)), max(1, int(layer.height * k))
    sc = layer.resize((nw, nh), Image.LANCZOS)
    ax, ay = anchor if anchor else (canvas[0] // 2, canvas[1] // 2)
    out.alpha_composite(sc, (int(ax - nw / 2), int(ay - nh / 2)))
    return out

def with_alpha(layer, a):
    """Multiply a layer's alpha by `a` (0..1)."""
    if a >= 0.999: return layer
    out = layer.copy()
    out.putalpha(out.getchannel("A").point(lambda v: int(v * clamp01(a))))
    return out

# ---------------------------------------------------------------- encode
def encode(frames, out, fps=FPS, alpha=True):
    """Write an iterable of RGBA PIL frames to `out` as QTRLE (alpha) or H.264."""
    tmp = tempfile.mkdtemp(prefix="motionlib_")
    try:
        n = 0
        for im in frames:
            im.save(os.path.join(tmp, "f_%05d.png" % n)); n += 1
        if n == 0: raise ValueError("no frames")
        cmd = [FF, "-nostdin", "-y", "-v", "error", "-framerate", f"{fps:.6f}",
               "-i", os.path.join(tmp, "f_%05d.png")]
        cmd += (["-c:v", "qtrle", "-pix_fmt", "argb"] if alpha else
                ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p"])
        subprocess.run(cmd + [out], check=True)
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def nframes(dur, fps=FPS): return max(1, int(round(dur * fps)))

# ---------------------------------------------------------------- components
def callout_box(out, rect, dur, draw_dur=0.55, delay=0.0, color=RED, width=9,
                radius=14, pad=12, label=None, out_dur=0.28, fps=FPS):
    """An animated highlight drawn around something already in the frame.

    Used for the physical photo taped to the door behind Dan on "THIS picture got me
    abs". The stroke draws itself clockwise, then breathes with a soft halo.
    """
    x0, y0, x1, y1 = rect
    box = [x0 - pad, y0 - pad, x1 + pad, y1 + pad]
    lab_f = font(34, "ExtraBold")
    N = nframes(dur, fps)
    frames = []
    for i in range(N):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if t >= delay:
            u = t - delay
            p = ease_out_cubic(u / draw_dur)
            # after the draw: a slow two-beat halo pulse
            glow = 0.0
            if p >= 1.0:
                glow = 0.45 + 0.35 * math.sin((u - draw_dur) * 3.1)
                glow = max(0.0, glow)
            fade = 1.0
            if t > dur - out_dur:
                fade = 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            stroke_box(lay, box, p, color=color, width=width, radius=radius, glow=glow)
            if label and p >= 1.0:
                chip(lay, (box[0], box[3] + 14), label, lab_f, color, (255, 255, 255, 255),
                     radius=8, shadow=True)
            im.alpha_composite(with_alpha(lay, fade))
        frames.append(im)
    return encode(frames, out, fps)


def card_in(out, dur, build, in_dur=0.42, out_dur=0.30, hold_bg=True,
            anchor=None, fps=FPS, bg=None):
    """Generic full-frame brand scene whose CONTENT scales+fades in with a spring.

    `build(im, t)` draws the scene content onto an RGBA canvas for time t (seconds from
    the component's start). The background (if any) appears instantly; only the content
    animates -- that is what makes a MOGRT card read as "placed" rather than "zoomed".
    """
    N = nframes(dur, fps)
    base = bg if bg is not None else (paper_bg().convert("RGBA") if hold_bg else None)
    frames = []
    for i in range(N):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_in  = ease_out_cubic(t / in_dur) if in_dur > 0 else 1.0
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        if base is not None:
            im.alpha_composite(with_alpha(base, min(a_in * 2.2, 1.0) * a_out))
        content = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        build(content, t)
        k = 0.90 + 0.10 * ease_out_back(t / in_dur) if in_dur > 0 else 1.0
        im.alpha_composite(with_alpha(scale_about(content, k, anchor), a_in * a_out))
        frames.append(im)
    return encode(frames, out, fps)


def title_card(out, headline, subtitle, dur, in_dur=0.55, out_dur=0.35,
               accent=RED, drift=0.035, fps=FPS):
    """Full-screen chapter card: heavy headline on a red rule, subtitle under it.

    The whole group drifts in scale for the full duration so the card is never a
    frozen still (a static full-frame card reads as a stall).
    """
    lines = headline.upper().split("\n")
    fH = font(132, "ExtraBold")
    fS = font(46, "Medium")
    sub = wrap(subtitle, fS, 1180)

    LH_H = int(fH.size * 1.20)          # headline line advance
    LH_S = int(fS.size * 1.32)          # subtitle line advance
    RULE = 15                           # accent rule thickness

    def build(im, t):
        d = ImageDraw.Draw(im)
        block = len(lines) * LH_H + 62 + len(sub) * LH_S
        y = (H - block) / 2 - 30
        for li, l in enumerate(lines):
            tw, _ = text_size(l, fH)
            x = (W - tw) / 2
            bot = ink_bottom(l, fH)
            p = ease_out_cubic((t - li * 0.10) / 0.45)
            # the rule sits under the LAST line only -- one under every line collides
            # with the line beneath it and reads as a strikethrough
            if li == len(lines) - 1:
                d.rounded_rectangle([x - 30, y + bot + 18, x - 30 + (tw + 60) * p,
                                     y + bot + 18 + RULE], radius=RULE // 2, fill=accent)
            if p > 0.05:
                # the headline wipes in left-to-right over its own rule
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((x, y), l, font=fH, fill=INK, anchor="lt")
                cut = x + tw * ease_out_expo((t - li * 0.10) / 0.5)
                mask = Image.new("L", (W, H), 0)
                ImageDraw.Draw(mask).rectangle([0, 0, cut, H], fill=255)
                lay.putalpha(Image.composite(lay.getchannel("A"),
                                             Image.new("L", (W, H), 0), mask))
                im.alpha_composite(lay)
            y += LH_H
        y += 62
        for i, l in enumerate(sub):
            a = ease_out_cubic((t - 0.28 - i * 0.08) / 0.4)
            tw, _ = text_size(l, fS)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text(((W - tw) / 2, y + (1 - a) * 16), l,
                                     font=fS, fill=INK_SOFT, anchor="lt")
            im.alpha_composite(with_alpha(lay, a))
            y += LH_S

    N = nframes(dur, fps)
    base = paper_bg().convert("RGBA")
    frames = []
    for i in range(N):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_in  = ease_out_cubic(t / 0.18)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im.alpha_composite(with_alpha(base, a_in * a_out))
        content = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        build(content, t)
        k = 1.0 + drift * (t / dur)
        im.alpha_composite(with_alpha(scale_about(content, k), a_out))
        frames.append(im)
    return encode(frames, out, fps)


def bullets_build(out, heading, bullets, dur, panel_w=880, in_dur=0.45,
                  out_dur=0.30, accent=RED, fps=FPS):
    """Left-hand list panel whose bullets appear ONE AT A TIME.

    `bullets` is [(t_seconds, "text"), ...] -- sync each t to the word that introduces
    that bullet, not to an even spacing. The panel slides in from the left; each bullet
    fades up and settles from +14px.
    """
    fH = font(48, "ExtraBold")
    fB = font(44, "SemiBold")
    PAD, IND = 78, 38
    LH = int(fB.size * 1.30)
    wrapped = [(t, wrap(txt, fB, panel_w - PAD * 2 - IND)) for t, txt in bullets]
    panel = paper_bg(panel_w, H).convert("RGBA")

    # vertical centring: measure the finished block once, not per frame
    head_h = ink_bottom(heading.upper(), fH) + 58
    block = head_h + sum(len(l) * LH + 34 for _, l in wrapped)
    TOP = max(96, (H - block) / 2)

    N = nframes(dur, fps)
    frames = []
    for i in range(N):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sp = ease_out_cubic(t / in_dur)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        dx = int(-panel_w * (1 - sp))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(panel, (dx, 0))
        d = ImageDraw.Draw(lay)
        y = TOP
        hp = ease_out_cubic((t - 0.16) / 0.4)
        if hp > 0.01:
            hu = heading.upper()
            hw, hb = text_size(hu, fH)[0], ink_bottom(hu, fH)
            d.text((dx + PAD, y), hu, font=fH, fill=INK, anchor="lt")
            d.rounded_rectangle([dx + PAD, y + hb + 14, dx + PAD + hw * hp, y + hb + 24],
                                radius=5, fill=accent)
        y += head_h
        for (bt, lines) in wrapped:
            bp = ease_out_cubic((t - bt) / 0.42)
            if bp > 0.01:
                sub = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                sd = ImageDraw.Draw(sub)
                oy = int((1 - bp) * 16)
                sd.rounded_rectangle([dx + PAD, y + 18 + oy, dx + PAD + 14, y + 32 + oy],
                                     radius=3, fill=accent)
                yy = y + oy
                for l in lines:
                    sd.text((dx + PAD + IND, yy), l, font=fB, fill=INK, anchor="lt")
                    yy += LH
                lay.alpha_composite(with_alpha(sub, bp))
            y += len(lines) * LH + 34
        im.alpha_composite(with_alpha(lay, a_out))
        frames.append(im)
    return encode(frames, out, fps)


def lower_third(out, label, statement, dur, x=90, y=880, in_dur=0.34, out_dur=0.26,
                accent=RED, fps=FPS):
    """Label chip + accent strip, sliding in from the left.

    The white chip carries the CATEGORY ("The Problem"); the red strip carries the
    CLAIM. The strip's text wipes in after the strip lands so the eye reads left-first.
    """
    fL = font(38, "Bold")
    fS = font(38, "ExtraBold")
    lw, lh = text_size(label, fL)
    sw, sh = text_size(statement, fS)
    ch_w, ch_h = lw + 44, max(lh, sh) + 30
    st_w = sw + 44

    N = nframes(dur, fps)
    frames = []
    for i in range(N):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p = ease_out_cubic(t / in_dur)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dx = int(x - (x + ch_w + st_w) * (1 - p))
        lay.alpha_composite(drop_shadow((W, H), [dx, y, dx + ch_w, y + ch_h], 8,
                                        blur=18, spread=4, opacity=70))
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle([dx, y, dx + ch_w, y + ch_h], radius=8, fill=(250, 250, 252))
        d.text((dx + 22, y + ch_h / 2), label, font=fL, fill=INK, anchor="lm")
        # red strip grows out of the chip, then its text wipes in
        gp = ease_out_cubic((t - in_dur * 0.75) / 0.30)
        if gp > 0.01:
            sx = dx + ch_w
            d.rectangle([sx, y, sx + st_w * gp, y + ch_h], fill=accent)
            wp = ease_out_expo((t - in_dur * 0.75 - 0.14) / 0.34)
            if wp > 0.01:
                tl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(tl).text((sx + 22, y + ch_h / 2), statement, font=fS,
                                        fill=(255, 255, 255), anchor="lm")
                m = Image.new("L", (W, H), 0)
                ImageDraw.Draw(m).rectangle([0, 0, sx + 22 + sw * wp, H], fill=255)
                tl.putalpha(Image.composite(tl.getchannel("A"), Image.new("L", (W, H), 0), m))
                lay.alpha_composite(tl)
        im.alpha_composite(with_alpha(lay, a_out))
        frames.append(im)
    return encode(frames, out, fps)


def number_pop(out, text, dur, xy=None, size=150, in_dur=0.36, out_dur=0.26,
               color=INK, accent=RED, fps=FPS):
    """Standalone letter-pop clip. For composing INSIDE another scene use pop_text()."""
    f = font(size, "ExtraBold")
    ax, ay = xy if xy else (W // 2, int(H * 0.80))
    N = nframes(dur, fps)
    frames = []
    for i in range(N):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pop_text(lay, t, text, f, (ax, ay), in_dur, color, accent)
        im.alpha_composite(with_alpha(lay, a_out))
        frames.append(im)
    return encode(frames, out, fps)


def photo_swap(out, items, dur, in_dur=0.45, out_dur=0.30, gap=0.0,
               tag_text=None, fps=FPS):
    """Photo cards shown in SEQUENCE on one brand background -- never side by side.

    `items` is [(t_in, t_out, PIL.Image, caption_or_None), ...]. Sequencing is the
    compliance-safe way to demo a transformation: before -> something else -> after,
    with the after tagged. Two physique photos on screen at once is a banned pattern in
    paid ads and is not worth building into the library at all.
    """
    CW, CH = 760, 860
    fC = font(40, "Bold")
    fT = font(30, "ExtraBold")
    plates = []
    for (a, b, img, cap) in items:
        plates.append((a, b, rounded_photo(img, CW - 36, CH - 36 - (58 if cap else 0),
                                           radius=18, mode="contain"), cap))
    N = nframes(dur, fps)
    base = paper_bg().convert("RGBA")
    frames = []
    for i in range(N):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_in  = ease_out_cubic(t / 0.18)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im.alpha_composite(with_alpha(base, a_in * a_out))
        for (a, b, plate, cap) in plates:
            if t < a - 0.02 or t > b + 0.02: continue
            p = ease_out_cubic((t - a) / in_dur)
            q = 1.0 if t <= b - 0.22 else 1 - ease_in_cubic((t - (b - 0.22)) / 0.22)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            x0, y0 = (W - CW) // 2, (H - CH) // 2
            card(lay, [x0, y0, x0 + CW, y0 + CH], radius=26)
            lay.alpha_composite(plate, (x0 + 18, y0 + 18))
            if cap:
                ImageDraw.Draw(lay).text((W // 2, y0 + CH - 42), cap, font=fC,
                                         fill=INK, anchor="mm")
            if tag_text and t >= a:
                chip(lay, (x0 + 34, y0 + 34), tag_text, fT, (12, 14, 18, 235),
                     (255, 255, 255, 255), radius=8)
            k = 0.92 + 0.08 * ease_out_back(p)
            im.alpha_composite(with_alpha(scale_about(lay, k), min(p, q) * a_out))
        frames.append(im)
    return encode(frames, out, fps)
