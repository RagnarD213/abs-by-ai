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

Layout rules (taken from the trial edit, 2026-08-22 — Dan preferred its screens)
-------------------------------------------------------------------------------
A full-screen graphic is a SOLID BRAND FIELD, not a white page with a card on it.
Type is big and heavy, leading is tight (~0.95), the block is TOP-aligned rather than
centred, headings carry a solid accent rule at their own width, list markers are small
filled squares, photographs sit straight on the field, and title-card headlines sit in
an accent BAND in oblique caps. The numbers below were measured off his frames.
"""
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter
import math, os, shutil, subprocess, tempfile

FF   = os.environ.get("MOTIONLIB_FFMPEG",
                      "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg")
W, H = 1920, 1080
FPS  = 30000 / 1001

# ---------------------------------------------------------------- palettes
class Palette:
    """A full-screen graphic style. `hot` is reserved for attention devices (callout
    strokes, the lower-third strip) and stays the brand red in every palette."""
    def __init__(self, field, field_hi, ink, ink_soft, accent, on_accent,
                 hot=(226, 34, 34), deep=None):
        self.field, self.field_hi = field, field_hi
        self.ink, self.ink_soft = ink, ink_soft
        self.accent, self.on_accent = accent, on_accent
        self.hot = hot
        # `deep` is a solid dark-green BLOCK for bars, bands and half-panels. It has to
        # read as green against a near-black field, so it is not the field colour.
        self.deep = deep or accent

# The CONTENT style: J2's dark green, olive accent, off-white type. Dan, 2026-08-22 --
# "copy his graphic screen, but make it dark green".
GREEN = Palette(field=(22, 33, 24), field_hi=(29, 42, 31),
                ink=(233, 238, 222), ink_soft=(158, 171, 142),
                accent=(140, 152, 88), on_accent=(15, 23, 15))

# The PAID-AD style (Dan's ad-1 revisions, 2026-08-23): black background, olive/dark
# green headers, white body copy -- i.e. the YouTube Shorts cover system he pointed at,
# not the dark-green field of the CONTENT style. J2 cover tokens: BG (13,14,11),
# OLIVE (140,152,88).
J2AD = Palette(field=(13, 14, 11), field_hi=(21, 23, 18),
               ink=(255, 255, 255), ink_soft=(176, 184, 158),
               accent=(140, 152, 88), on_accent=(10, 12, 8),
               deep=(28, 52, 33))

# The bright variant, kept because a paid ad may want it.
PAPER = Palette(field=(243, 245, 248), field_hi=(247, 249, 251),
                ink=(17, 21, 28), ink_soft=(92, 102, 116),
                accent=(226, 34, 34), on_accent=(255, 255, 255))

CARD   = (255, 255, 255)
SHADOW = (0, 0, 0)
RED    = (226, 34, 34)

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
def field_bg(pal=GREEN, w=W, h=H):
    """Solid brand field with a soft radial lift.

    Built small and upscaled -- a per-pixel radial at 1920x1080 costs ~2s a frame and
    this is a static layer. Keep the two colours within ~8 levels: a bigger delta shows
    as a distinct blob on a large flat panel.
    """
    sm = Image.new("RGB", (96, 54))
    px = sm.load()
    for y in range(54):
        for x in range(96):
            d = math.hypot((x - 48) / 48, (y - 27) / 27)
            k = clamp01(1 - d * 0.85)
            px[x, y] = tuple(int(pal.field[i] + (pal.field_hi[i] - pal.field[i]) * k)
                             for i in range(3))
    return sm.resize((w, h), Image.BICUBIC)

def drop_shadow(size, box, radius, blur=26, spread=8, opacity=90, offset=(0, 12)):
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
    ImageDraw.Draw(im).rounded_rectangle(box, radius=radius, fill=fill,
                                         outline=outline, width=width if outline else 0)

def oriented(img):
    """Honour EXIF rotation. iPhone photos carry orientation in EXIF and PIL ignores it,
    which silently delivered a sideways portrait into a finished ad graphic once."""
    try:
        return ImageOps.exif_transpose(img)
    except Exception:
        return img


def fit_cover(img, w, h):
    img = oriented(img)
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
    img = oriented(img)
    """Scale `img` to fit inside w x h, whole subject preserved.

    Use this for photographs of people: cover-cropping a portrait cuts the top of the
    head or the shorts line, which is a standing rejection (see /coverimage).
    """
    k = min(w / img.width, h / img.height)
    return img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)

def photo_on_field(img, maxw, maxh, radius=18, shadow=True, size=(W, H), centre=None):
    """A photograph placed straight on the brand field -- no white card behind it.

    Returns (canvas-sized RGBA layer, the photo's box). This is the trial edit's
    treatment: the field IS the card.
    """
    ph = fit_contain(img.convert("RGB"), maxw, maxh)
    cx, cy = centre or (size[0] // 2, size[1] // 2)
    x0, y0 = int(cx - ph.width / 2), int(cy - ph.height / 2)
    box = [x0, y0, x0 + ph.width, y0 + ph.height]
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    if shadow:
        lay.alpha_composite(drop_shadow(size, box, radius, blur=30, spread=6, opacity=115))
    plate = Image.new("RGBA", (ph.width, ph.height), (0, 0, 0, 255))
    plate.paste(ph, (0, 0))
    mask = Image.new("L", (ph.width, ph.height), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, ph.width - 1, ph.height - 1],
                                           radius=radius, fill=255)
    plate.putalpha(mask)
    lay.alpha_composite(plate, (x0, y0))
    return lay, box

def rounded_photo(img, w, h, radius=20, mode="contain", bg=CARD):
    """Photo on a rounded plate of exactly w x h."""
    plate = Image.new("RGBA", (w, h), tuple(bg) + (255,))
    ph = fit_cover(img, w, h) if mode == "cover" else fit_contain(img, w, h)
    plate.paste(ph.convert("RGB"), ((w - ph.width) // 2, (h - ph.height) // 2))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    plate.putalpha(mask)
    return plate

_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def text_bbox(txt, f):
    """Ink bounds for a draw at (0,0) with anchor='lt' -- the anchor everything here uses.

    Measured WITH anchor='lt' on purpose. textbbox() defaults to 'la' (ascender), which
    sits ~0.33em above 'lt' (top of ink): at a 145 px headline that is 48 px, and it put
    a title-card headline right through the top edge of its own accent band. Measure
    with the same anchor you draw with, always. bbox[3] is the ink bottom -- position
    rules from that, never from y + height (that shipped a strikethrough headline once).
    """
    return _MEASURE.textbbox((0, 0), txt, font=f, anchor="lt")

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

def oblique(layer, deg=11.0, pivot_y=None):
    """Shear a layer to fake an italic, pivoting about `pivot_y` (default: layer centre).

    Manrope ships no italic and the trial edit's title-card headline is oblique;
    shearing the rendered glyphs matches it without adding a font dependency. ALWAYS
    pass the pivot when the text is not at the layer's vertical centre -- a shear about
    the canvas centre translates the line sideways by k*(centre - y), which pushed a
    headline clean off the right edge of its band.
    """
    k = math.tan(math.radians(deg))
    py = layer.height / 2 if pivot_y is None else pivot_y
    return layer.transform(layer.size, Image.AFFINE, (1, k, -k * py, 0, 1, 0),
                           resample=Image.BICUBIC)

def chip(im, xy, txt, f, fill, fg, radius=10, padx=18, pady=10, shadow=False):
    """Small solid label block. Returns (w, h) of the chip drawn at xy."""
    tw, th = text_size(txt, f)
    w, h = tw + padx * 2, th + pady * 2
    box = [xy[0], xy[1], xy[0] + w, xy[1] + h]
    if shadow:
        im.alpha_composite(drop_shadow(im.size, box, radius, blur=16, spread=4, opacity=110))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=radius, fill=fill)
    d.text((xy[0] + padx, xy[1] + pady), txt, font=f, fill=fg, anchor="lt")
    return w, h

def dashed_arrow(im, p0, p1, progress=1.0, color=None, width=6, dash=22, gap=16, head=26):
    """Dashed line from p0 to p1, drawn left->right by `progress` (0..1), then a head."""
    color = color or GREEN.ink
    d = ImageDraw.Draw(im)
    x0, y0 = p0; x1, y1 = p1
    total = math.hypot(x1 - x0, y1 - y0)
    if total < 1: return
    ux, uy = (x1 - x0) / total, (y1 - y0) / total
    shown = total * clamp01(progress)
    s = 0.0
    while s < shown - 1:
        e = min(s + dash, shown)
        d.line([x0 + ux * s, y0 + uy * s, x0 + ux * e, y0 + uy * e], fill=color, width=width)
        s += dash + gap
    if progress > 0.86:
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
        ImageDraw.Draw(g).rounded_rectangle(box, radius=radius,
                                            outline=tuple(color) + (int(190 * glow),),
                                            width=width + 10)
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)))
    p = clamp01(progress)
    d = ImageDraw.Draw(im)
    if p >= 0.999:
        d.rounded_rectangle(box, radius=radius, outline=color, width=width); return
    w_, h_ = x1 - x0, y1 - y0
    run = 2 * (w_ + h_) * p
    for (a, b, L) in [((x0, y0), (x1, y0), w_), ((x1, y0), (x1, y1), h_),
                      ((x1, y1), (x0, y1), w_), ((x0, y1), (x0, y0), h_)]:
        if run <= 0: break
        k = min(1.0, run / L)
        d.line([a[0], a[1], a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k],
               fill=color, width=width)
        run -= L

def scale_about(layer, k, anchor=None, canvas=(W, H)):
    """Scale a canvas-sized RGBA layer about a point.

    Pass an anchor only for a layer that really is canvas-sized -- scaling a small tile
    this way translates it to the anchor instead of scaling it in place.
    """
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

def pop_text(im, t, txt, f, centre, in_dur=0.36, color=None, accent=RED, rule=True):
    """Letter-by-letter snap-in, drawn onto `im` for local time `t`."""
    color = color or GREEN.ink
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

def panel_plate(box, radius=26, pal=GREEN, w=W, h=H, shadow=True):
    """Brand field with a rounded WINDOW punched out of it.

    Composite order is: base video -> the clip (square corners, filling `box`) -> this
    plate. The plate's opaque field covers everything outside the rounded rect, so the
    clip ends up with real rounded corners and a shadow without a per-frame mask.
    """
    plate = field_bg(pal, w, h).convert("RGBA")
    if shadow:
        plate.alpha_composite(drop_shadow((w, h), box, radius, blur=30, spread=10, opacity=130))
    hole = Image.new("L", (w, h), 255)
    ImageDraw.Draw(hole).rounded_rectangle(box, radius=radius, fill=0)
    plate.putalpha(Image.composite(plate.getchannel("A"), Image.new("L", (w, h), 0), hole))
    return plate

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
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if t >= delay:
            u = t - delay
            p = ease_out_cubic(u / draw_dur)
            glow = max(0.0, 0.45 + 0.35 * math.sin((u - draw_dur) * 3.1)) if p >= 1.0 else 0.0
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


def card_in(out, dur, build, in_dur=0.42, out_dur=0.30, anchor=None, fps=FPS, pal=GREEN):
    """Full-frame brand scene whose CONTENT scales+fades in with a spring.

    `build(im, t)` draws the scene content onto an RGBA canvas for time t (seconds from
    the component's start). The field appears instantly; only the content animates --
    that is what makes a MOGRT card read as "placed" rather than "zoomed".
    """
    base = field_bg(pal).convert("RGBA")
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_in  = ease_out_cubic(t / in_dur) if in_dur > 0 else 1.0
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im.alpha_composite(with_alpha(base, min(a_in * 2.2, 1.0) * a_out))
        content = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        build(content, t)
        k = 0.90 + 0.10 * ease_out_back(t / in_dur) if in_dur > 0 else 1.0
        im.alpha_composite(with_alpha(scale_about(content, k, anchor), a_in * a_out))
        frames.append(im)
    return encode(frames, out, fps)


def title_card(out, headline, subtitle, dur, in_dur=0.55, out_dur=0.35, pal=GREEN,
               size=145, sub_size=66, drift=0.030, fps=FPS, band=None, band_ink=None):
    """Full-screen chapter card: oblique caps headline inside an accent BAND.

    The trial edit's version, recoloured: a solid accent block spans the whole headline
    block and the headline sits on it in `on_accent`; the subtitle sits below on the
    field. The group drifts in scale for the full duration so it is never a frozen still.
    """
    lines = [l.upper() for l in headline.split("\n")]
    fH = font(size, "ExtraBold")
    fS = font(sub_size, "Medium")
    sub = wrap(subtitle, fS, 1320)
    # measured off his card: cap height 111 px (=> ~145 px Manrope ExtraBold), line
    # advance 127 px (0.88 of the size -- much tighter than a default 1.2 leading),
    # band padding ~50 x 22, and 76 px down to the subtitle.
    LH_H = int(size * 0.88)
    LH_S = int(sub_size * 1.18)
    PADX, PADY_T, PADY_B = 54, 24, 36     # PADX carries the shear overhang too

    widths = [text_size(l, fH)[0] for l in lines]
    cap    = max(ink_bottom(l, fH) for l in lines)
    band_w = max(widths) + PADX * 2
    band_h = (len(lines) - 1) * LH_H + cap + PADY_T + PADY_B
    block_h = band_h + 76 + len(sub) * LH_S
    band_y = int((H - block_h) / 2)

    def build(im, t):
        d = ImageDraw.Draw(im)
        bp = ease_out_cubic(t / 0.34)            # the band wipes open from the centre
        bw = band_w * bp
        d.rectangle([W / 2 - bw / 2, band_y, W / 2 + bw / 2, band_y + band_h],
                    fill=band or pal.accent)
        for li, l in enumerate(lines):
            p = ease_out_cubic((t - 0.16 - li * 0.09) / 0.42)
            if p <= 0.02: continue
            tw = widths[li]
            x = (W - tw) / 2
            y = band_y + PADY_T + li * LH_H
            gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(gl).text((x, y), l, font=fH, fill=band_ink or pal.on_accent,
                                     anchor="lt")
            gl = oblique(gl, 11.0, pivot_y=y + cap / 2)
            cut = x + tw * ease_out_expo((t - 0.16 - li * 0.09) / 0.5) + size * 0.3
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).rectangle([0, 0, cut, H], fill=255)
            gl.putalpha(Image.composite(gl.getchannel("A"), Image.new("L", (W, H), 0), m))
            im.alpha_composite(gl)
        y = band_y + band_h + 76
        for i, l in enumerate(sub):
            a = ease_out_cubic((t - 0.40 - i * 0.08) / 0.4)
            if a <= 0.01:
                y += LH_S; continue
            tw, _ = text_size(l, fS)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text(((W - tw) / 2, y + (1 - a) * 16), l,
                                     font=fS, fill=pal.ink, anchor="lt")
            im.alpha_composite(with_alpha(lay, a))
            y += LH_S

    base = field_bg(pal).convert("RGBA")
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_in  = ease_out_cubic(t / 0.16)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im.alpha_composite(with_alpha(base, a_in * a_out))
        content = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        build(content, t)
        im.alpha_composite(with_alpha(scale_about(content, 1.0 + drift * (t / dur)), a_out))
        frames.append(im)
    return encode(frames, out, fps)


def bullets_build(out, heading, bullets, dur, panel_w=980, in_dur=0.45, out_dur=0.30,
                  pal=GREEN, head_size=76, body_size=68, fps=FPS, head_color=None):
    """Left-hand list panel whose bullets appear ONE AT A TIME.

    `bullets` is [(t_seconds, "text"), ...] -- sync each t to the word that introduces
    that bullet, not to an even spacing.

    Type sizes and spacing are the trial edit's, measured off his frames: a heavy
    heading with a solid accent rule at its own width, small SQUARE markers, tight 0.95
    leading, and the whole block TOP-aligned. A vertically centred block reads as a
    slide; his reads as part of the video.
    """
    fH = font(head_size, "ExtraBold")
    fB = font(body_size, "SemiBold")
    PAD  = int(panel_w * 0.095)
    IND  = int(body_size * 0.86)
    LH   = int(body_size * 0.95)
    TOP  = 96
    RULE = 9
    wrapped = [(t, wrap(txt, fB, panel_w - PAD - IND - 40)) for t, txt in bullets]
    panel = field_bg(pal, panel_w, H).convert("RGBA")
    hu = heading.upper()
    head_w, head_bot = text_size(hu, fH)[0], ink_bottom(hu, fH)

    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sp = ease_out_cubic(t / in_dur)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        dx = int(-panel_w * (1 - sp))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(panel, (dx, 0))
        d = ImageDraw.Draw(lay)
        y = TOP
        hp = ease_out_cubic((t - 0.14) / 0.38)
        if hp > 0.01:
            d.text((dx + PAD, y), hu, font=fH, fill=head_color or pal.ink, anchor="lt")
            d.rectangle([dx + PAD, y + head_bot + 18,
                         dx + PAD + head_w * hp, y + head_bot + 18 + RULE], fill=pal.accent)
        y += head_bot + 18 + RULE + 52
        for (bt, lines) in wrapped:
            bp = ease_out_cubic((t - bt) / 0.42)
            if bp > 0.01:
                sub = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                sd = ImageDraw.Draw(sub)
                oy = int((1 - bp) * 16)
                m = int(body_size * 0.29)
                sd.rectangle([dx + PAD, y + oy + int(body_size * 0.30),
                              dx + PAD + m, y + oy + int(body_size * 0.30) + m], fill=pal.accent)
                yy = y + oy - ink_top(lines[0], fB)
                for l in lines:
                    sd.text((dx + PAD + IND, yy), l, font=fB, fill=pal.ink, anchor="lt")
                    yy += LH
                lay.alpha_composite(with_alpha(sub, bp))
            y += len(lines) * LH + int(body_size * 0.52)
        im.alpha_composite(with_alpha(lay, a_out))
        frames.append(im)
    return encode(frames, out, fps)


def lower_third(out, label, statement, dur, x=90, y=880, in_dur=0.34, out_dur=0.26,
                pal=GREEN, fps=FPS):
    """Label chip + accent strip, sliding in from the left.

    The light chip carries the CATEGORY ("The Problem"); the red strip carries the
    CLAIM. The strip's text wipes in after the strip lands so the eye reads left-first.
    This one sits over FOOTAGE, so it keeps the brand red rather than the field accent.
    """
    fL = font(38, "Bold")
    fS = font(38, "ExtraBold")
    lw, lh = text_size(label, fL)
    sw, sh = text_size(statement, fS)
    ch_w, ch_h = lw + 44, max(lh, sh) + 30
    st_w = sw + 44

    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p = ease_out_cubic(t / in_dur)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dx = int(x - (x + ch_w + st_w) * (1 - p))
        lay.alpha_composite(drop_shadow((W, H), [dx, y, dx + ch_w, y + ch_h], 8,
                                        blur=18, spread=4, opacity=120))
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle([dx, y, dx + ch_w, y + ch_h], radius=8, fill=pal.ink)
        d.text((dx + 22, y + ch_h / 2), label, font=fL, fill=(18, 26, 18), anchor="lm")
        gp = ease_out_cubic((t - in_dur * 0.75) / 0.30)
        if gp > 0.01:
            sx = dx + ch_w
            d.rectangle([sx, y, sx + st_w * gp, y + ch_h], fill=pal.hot)
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


def lower_third_bar(out, lines, dur, x=90, y=None, in_dur=0.34, out_dur=0.26,
                    pal=GREEN, size=42, lead_size=None, fps=FPS, bar_w=26,
                    bar_color=None, plate=None, text_color=None):
    """Solid accent BAR on the left + a plate carrying one or two lines of statement.

    Dan's ad-1 revision (2026-08-23) restyles every lower third this way: "green bar on
    left, white text on black background". It replaces the chip+red-strip form for paid
    ads -- that one puts a light category chip first, which reads as a label; this one
    reads as the claim itself, which is what a lower third in an ad is for.

    `lines` is a list of strings. The first line is set heavier (and larger, if
    `lead_size` is given) so a two-line chip has a headline and a qualifier.
    """
    # olive, not the deep green: a (28,52,33) block on a near-black field is almost
    # invisible at lower-third size -- measured 12 levels of separation.
    bar_color = bar_color or pal.accent
    plate     = plate or (10, 11, 9)
    text_color = text_color or (255, 255, 255)
    fonts = [font(lead_size or size, "ExtraBold")] + [font(size, "Bold")] * (len(lines) - 1)
    sizes = [text_size(l, f) for l, f in zip(lines, fonts)]
    PADX, PADY, GAP = 26, 16, 8
    tw = max(w for w, _ in sizes)
    line_h = [max(h, f.size) for (_, h), f in zip(sizes, fonts)]
    ch_h = sum(line_h) + GAP * (len(lines) - 1) + PADY * 2
    pl_w = tw + PADX * 2
    if y is None: y = H - 200 - ch_h

    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p_in  = ease_out_cubic(t / in_dur)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        # the bar drops in first, then the plate grows out of it to the right
        bh = ch_h * ease_out_back(t / (in_dur * 0.8))
        d = ImageDraw.Draw(lay)
        by = y + (ch_h - bh) / 2
        d.rectangle([x, by, x + bar_w, by + bh], fill=bar_color)
        gp = ease_out_cubic((t - in_dur * 0.55) / 0.30)
        if gp > 0.01:
            px = x + bar_w
            lay.alpha_composite(drop_shadow((W, H), [px, y, px + pl_w * gp, y + ch_h], 4,
                                            blur=18, spread=4, opacity=130))
            d = ImageDraw.Draw(lay)
            d.rectangle([px, y, px + pl_w * gp, y + ch_h], fill=plate)
            yy = y + PADY
            for li, (l, f) in enumerate(zip(lines, fonts)):
                wp = ease_out_expo((t - in_dur * 0.55 - 0.12 - li * 0.10) / 0.34)
                if wp > 0.01:
                    tl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    ImageDraw.Draw(tl).text((px + PADX, yy), l, font=f,
                                            fill=text_color,
                                            anchor="lt")
                    m = Image.new("L", (W, H), 0)
                    ImageDraw.Draw(m).rectangle([0, 0, px + PADX + sizes[li][0] * wp, H], fill=255)
                    tl.putalpha(Image.composite(tl.getchannel("A"), Image.new("L", (W, H), 0), m))
                    lay.alpha_composite(tl)
                yy += line_h[li] + GAP
        im.alpha_composite(with_alpha(lay, a_out * min(1.0, p_in * 3)))
        frames.append(im)
    return encode(frames, out, fps)


def number_pop(out, text, dur, xy=None, size=150, in_dur=0.36, out_dur=0.26,
               pal=GREEN, fps=FPS):
    """Standalone letter-pop clip. To compose INSIDE another scene use pop_text()."""
    f = font(size, "ExtraBold")
    ax, ay = xy if xy else (W // 2, int(H * 0.80))
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pop_text(lay, t, text, f, (ax, ay), in_dur, pal.ink, pal.hot)
        im.alpha_composite(with_alpha(lay, a_out))
        frames.append(im)
    return encode(frames, out, fps)


def photo_sequence(out, items, dur, in_dur=0.40, out_dur=0.28, pal=GREEN,
                   maxw=1560, maxh=880, caption_size=44, fps=FPS):
    """Photographs shown in SEQUENCE on one brand field -- never side by side.

    `items` is [(t_in, t_out, PIL.Image, caption_or_None, tag_or_None), ...].
    Sequencing is the compliance-safe way to demo a transformation: before -> something
    else -> after, with the after tagged. Two physique photos on screen at once is a
    banned pattern in paid ads and is not worth building into the library at all.
    """
    fC = font(caption_size, "Bold")
    fT = font(30, "ExtraBold")
    prepared = []
    for (a, b, img, cap, tag) in items:
        cy = H // 2 - (34 if cap else 0)
        lay, box = photo_on_field(img, maxw, maxh, centre=(W // 2, cy))
        if cap:
            ImageDraw.Draw(lay).text((W // 2, box[3] + 46), cap, font=fC,
                                     fill=pal.ink, anchor="mm")
        if tag:
            chip(lay, (box[0] + 26, box[1] + 26), tag, fT, (12, 16, 12, 235),
                 (255, 255, 255, 255), radius=8)
        prepared.append((a, b, lay))

    base = field_bg(pal).convert("RGBA")
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a_in  = ease_out_cubic(t / 0.16)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im.alpha_composite(with_alpha(base, a_in * a_out))
        for (a, b, lay) in prepared:
            if t < a - 0.02 or t > b + 0.02: continue
            p = ease_out_cubic((t - a) / in_dur)
            q = 1.0 if t <= b - 0.20 else 1 - ease_in_cubic((t - (b - 0.20)) / 0.20)
            k = 0.94 + 0.06 * ease_out_back(p)
            im.alpha_composite(with_alpha(scale_about(lay, k), min(p, q) * a_out))
        frames.append(im)
    return encode(frames, out, fps)


# ============================================================================
# LONGFORM CONTENT PACK  (added 2026-08-24 for the ab-wheel rebuild)
#
# Measured off the reference edit of the same footage, then recoloured to Dan's
# revision note: "make green used in graphics slightly darker, military green".
# His card gradient measures (84,93,55) -> (141,152,97) -- the light end is almost
# exactly our brand OLIVE (140,152,88) -- so MIL below sits a stop under it and
# desaturates toward olive drab, which is what "military green" means.
# ============================================================================

MIL = Palette(field=(13, 14, 11), field_hi=(21, 23, 18),
              ink=(255, 255, 255), ink_soft=(171, 180, 148),
              accent=(104, 118, 66), on_accent=(255, 255, 255),
              deep=(46, 54, 32))
MIL.mid = (78, 89, 50)          # plate/bar green, between deep and accent
# No red in this palette. `hot` is the brand red everywhere else, but Dan's ab-wheel
# revision asks for the graphics to sit in the military-green family, and a red rule
# under a "$17" callout on an olive/black card reads as a different brand.
MIL.hot = MIL.accent
OLIVE   = (140, 152, 88)        # brand olive: hairlines and eyebrows only


def bracket_frame(im, pal=MIL, inset=30, color=None, width=3, tick=26, alpha=255):
    """J2 corner brackets with tick marks along the border.

    The reference edit puts this frame around every full-screen graphic and every
    inset, and it is the single cheapest thing that makes a card look designed rather
    than typed. Corners only -- a continuous rectangle reads as a border, brackets read
    as a viewfinder.
    """
    d = ImageDraw.Draw(im)
    c = (color or OLIVE) + (alpha,)
    w, h = im.size
    x0, y0, x1, y1 = inset, inset, w - inset - 1, h - inset - 1
    L = int(min(w, h) * 0.085)
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(cx, cy), (cx + sx * L, cy)], fill=c, width=width)
        d.line([(cx, cy), (cx, cy + sy * L)], fill=c, width=width)
    for i in range(1, 9):                       # tick marks along top and bottom
        x = x0 + (x1 - x0) * i / 9
        n = tick if i % 3 == 0 else tick // 2
        d.line([(x, y0 + 4), (x, y0 + 4 + n)], fill=c, width=2)
        d.line([(x, y1 - 4), (x, y1 - 4 - n)], fill=c, width=2)
    return im


def _grad_plate(size, box, radius, c0, c1, angle="v"):
    """Rounded plate filled with a two-stop gradient (the reference edit's card fill)."""
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = max(1, x1 - x0), max(1, y1 - y0)
    sm = Image.new("RGB", (2, 2))
    px = sm.load()
    for j in range(2):
        for i in range(2):
            k = (j if angle == "v" else i)
            px[i, j] = tuple(int(c0[n] + (c1[n] - c0[n]) * k) for n in range(3))
    grad = sm.resize((w, h), Image.BICUBIC)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    lay.paste(grad, (x0, y0), m)
    return lay


def title_plate(out, headline, subtitle=None, dur=3.4, pal=MIL, size=104, sub_size=46,
                in_dur=0.5, out_dur=0.32, fps=FPS, plate_w=1420, ink=None):
    """Full-screen chapter card in the reference edit's form.

    A near-black bracketed field, a rounded plate filled with a military-green gradient,
    and the headline in white oblique caps wiping on line by line. The subtitle lands
    afterwards on its own light strip under the plate, which is how his second line
    ("EQUIPMENT FOR AB TRAINING") arrives.
    """
    lines = [l.upper() for l in headline.split("\n")]
    fH = font(size, "ExtraBold")
    fS = font(sub_size, "Bold")
    LH = int(size * 0.98)
    widths = [text_size(l, fH)[0] for l in lines]
    cap = max(ink_bottom(l, fH) for l in lines)
    plate_w = max(plate_w, max(widths) + 150)
    plate_h = (len(lines) - 1) * LH + cap + 130
    px0 = (W - plate_w) / 2
    total_h = plate_h + (96 if subtitle else 0)
    py0 = (H - total_h) / 2

    base = Image.new("RGBA", (W, H), pal.field + (255,))
    bracket_frame(base, pal)

    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        a_in = ease_out_cubic(t / 0.18)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        im.alpha_composite(with_alpha(base, a_in * a_out))
        con = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p = ease_out_cubic(t / (in_dur * 0.7))                 # plate grows from centre
        if p > 0.01:
            ph = plate_h * p
            con.alpha_composite(_grad_plate((W, H),
                [px0, py0 + (plate_h - ph) / 2, px0 + plate_w, py0 + (plate_h + ph) / 2],
                26, pal.deep, pal.accent))
        y = py0 + 66
        for li, l in enumerate(lines):
            q = ease_out_cubic((t - 0.22 - li * 0.10) / 0.40)
            if q <= 0.02: y += LH; continue
            tw = widths[li]; x = (W - tw) / 2
            gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(gl).text((x, y), l, font=fH, fill=(ink or pal.on_accent), anchor="lt")
            gl = oblique(gl, 10.0, pivot_y=y + cap / 2)
            cut = x + tw * ease_out_expo((t - 0.22 - li * 0.10) / 0.5) + size * 0.3
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).rectangle([0, 0, cut, H], fill=255)
            gl.putalpha(Image.composite(gl.getchannel("A"), Image.new("L", (W, H), 0), m))
            con.alpha_composite(gl)
            y += LH
        if subtitle:
            q = ease_out_cubic((t - 0.52) / 0.36)
            if q > 0.01:
                su = subtitle.upper()
                tw, th = text_size(su, fS)
                bx0, by0 = (W - tw) / 2 - 34, py0 + plate_h + 26
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).rectangle(
                    [bx0, by0, bx0 + (tw + 68) * q, by0 + th + 26], fill=(238, 240, 232, 255))
                if q > 0.5:
                    ImageDraw.Draw(lay).text((W / 2, by0 + (th + 26) / 2), su, font=fS,
                                             fill=(16, 20, 14), anchor="mm")
                con.alpha_composite(lay)
        im.alpha_composite(with_alpha(scale_about(con, 1.0 + 0.022 * (t / dur)), a_in * a_out))
        frames.append(im)
    return encode(frames, out, fps)


def section_label(out, number, text, dur=3.6, pal=MIL, x=110, y=None, size=54,
                  in_dur=0.36, out_dur=0.28, fps=FPS):
    """Numbered section chip + light plate, sliding in from the left.

    The reference edit's "02 | It Has A Built In Progression". The number sits in a
    solid military-green square; the title sits on a near-white plate so it stays
    readable over bright outdoor footage, which a dark plate does not.
    """
    fN = font(int(size * 1.05), "ExtraBold")
    fT = font(size, "Bold")
    tw, th = text_size(text, fT)
    ch_h = max(th, size) + 34
    nw = max(ch_h, text_size(number, fN)[0] + 34)
    pl_w = tw + 60
    if y is None: y = H - 196 - ch_h
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        p = ease_out_back(t / in_dur)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dx = int(x - (x + nw + pl_w) * (1 - clamp01(t / in_dur)))
        lay.alpha_composite(drop_shadow((W, H), [dx, y, dx + nw, y + ch_h], 6,
                                        blur=20, spread=5, opacity=140))
        d = ImageDraw.Draw(lay)
        d.rectangle([dx, y, dx + nw, y + ch_h], fill=pal.mid)
        d.text((dx + nw / 2, y + ch_h / 2), number, font=fN, fill=(255, 255, 255), anchor="mm")
        gp = ease_out_cubic((t - in_dur * 0.6) / 0.30)
        if gp > 0.01:
            sx = dx + nw
            d.rectangle([sx, y, sx + pl_w * gp, y + ch_h], fill=(240, 242, 234))
            wp = ease_out_expo((t - in_dur * 0.6 - 0.10) / 0.34)
            if wp > 0.01:
                tl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(tl).text((sx + 30, y + ch_h / 2), text, font=fT,
                                        fill=(17, 21, 14), anchor="lm")
                m = Image.new("L", (W, H), 0)
                ImageDraw.Draw(m).rectangle([0, 0, sx + 30 + tw * wp, H], fill=255)
                tl.putalpha(Image.composite(tl.getchannel("A"), Image.new("L", (W, H), 0), m))
                lay.alpha_composite(tl)
        im.alpha_composite(with_alpha(lay, a_out * min(1.0, p * 3)))
        frames.append(im)
    return encode(frames, out, fps)


def stack_build(out, items, dur, pal=MIL, x=110, y=250, size=62, head=None,
                out_dur=0.34, fps=FPS):
    """A list of names that appear ONE AT A TIME, synced to when they are spoken.

    `items` is [(t_seconds, "text"), ...]. Used for the three ab muscles as Dan names
    them -- the reference edit does exactly this and it is the one graphic in the video
    that carries information the viewer cannot get from the audio alone.
    """
    fH = font(38, "ExtraBold")
    fB = font(size, "Bold")
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        yy = y
        if head:
            hp = ease_out_cubic(t / 0.4)
            if hp > 0.01:
                hu = head.upper()
                tw, th = text_size(hu, fH)
                d = ImageDraw.Draw(lay)
                d.rectangle([x, yy, x + (tw + 44) * hp, yy + th + 24], fill=pal.mid)
                if hp > 0.5:
                    d.text((x + 22, yy + (th + 24) / 2), hu, font=fH,
                           fill=(255, 255, 255), anchor="lm")
            yy += 92
        for (bt, txt) in items:
            p = ease_out_cubic((t - bt) / 0.40)
            if p > 0.01:
                sub = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                sd = ImageDraw.Draw(sub)
                ox = int((1 - p) * 26)
                tw, th = text_size(txt, fB)
                sd.rectangle([x - ox, yy, x - ox + tw + 56, yy + th + 26], fill=(12, 14, 10, 232))
                sd.rectangle([x - ox, yy, x - ox + 9, yy + th + 26], fill=pal.accent)
                sd.text((x - ox + 30, yy + (th + 26) / 2), txt, font=fB,
                        fill=(255, 255, 255), anchor="lm")
                lay.alpha_composite(with_alpha(sub, p))
            yy += size + 46
        im.alpha_composite(with_alpha(lay, a_out))
        frames.append(im)
    return encode(frames, out, fps)


def inset_frame(out, dur, box, pal=MIL, radius=26, in_dur=0.42, out_dur=0.30, fps=FPS,
                label=None):
    """Bracketed field with a rounded WINDOW punched through it.

    Composite order is [programme][stock clip][this] -- the stock clip shows through the
    window and everything outside it becomes the brand field, which is how the reference
    edit presents its gym B-roll instead of cutting to it full-frame.
    """
    fL = font(34, "ExtraBold")
    base = Image.new("RGBA", (W, H), pal.field + (255,))
    bracket_frame(base, pal)
    hole = Image.new("L", (W, H), 255)
    ImageDraw.Draw(hole).rounded_rectangle(box, radius=radius, fill=0)
    base.putalpha(Image.composite(base.getchannel("A"), Image.new("L", (W, H), 0), hole))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, outline=pal.accent + (255,), width=3)
    if label:
        chip(base, (box[0], box[1] - 56), label, fL, pal.mid + (255,), (255, 255, 255, 255),
             radius=6)
    frames = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        a_in = ease_out_cubic(t / in_dur)
        a_out = 1.0 if t <= dur - out_dur else 1 - ease_in_cubic((t - (dur - out_dur)) / out_dur)
        frames.append(with_alpha(base, a_in * a_out))
    return encode(frames, out, fps)
