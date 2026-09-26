#!/usr/bin/env python3
"""softblue: the approved Soft Blue Light graphic family for every Abs By AI video.

Standard: `.claude/skills/_shared/GRAPHICS-STANDARDS.md` (Dan, 2026-09-26: all videos, all formats).
Source of truth: WV-01 round 3 option 1 (`style 0` in the private renderer
`/Volumes/Extreme/_edit_work/wv01-edit/round3/recipe/blueglass.py`) and its moving references
`graphics/1-before.mp4`, `1-family.mp4`, `1-cta.mp4`, `G-motivation.mp4`. This module ports ONLY the
approved components (moving field, glass card, photo card, disclosure chip, Motivation lower third,
CTA) with configurable copy, canvas size and placement. It does not carry the rejected three-photo
choices or the rejected round-3 phone shell.

At 16:9 1920x1080 every component reproduces the reference geometry exactly: the reference was
laid out in 960x540 units at 2x, and here `u = min(w, h) / 540` (2.0 on any 1080-based canvas).
Portrait and square canvases reflow the same parts; nothing is a letterboxed 16:9 plate.

Two ways to use it
------------------
1. Full-screen graphic scenes (opaque H.264, cut into the timeline like any insert):
       render_scene(out, dur, lambda t: scene_fact(t, w, h, photo=..., eyebrow=..., ...), w, h)
2. Anything over footage (lower thirds): the glass blurs the real picture beneath it, so it is
   composited per frame onto the decoded footage, never as a pre-baked alpha plate:
       render_over_footage(src, out, dur, lambda im, t: lower_third(im, t, "MOTIVATION", "..."),
                           start=12.0, w=1080, h=1920, vf=<crop+scale>)
   For a long film, `lower_third_patch()` renders only the lower-third band for its window as an
   opaque patch the layout script overlays at (x, y); pixels outside the drawn parts are the
   footage's own, so the overlay is exact on that same graded base.

Conventions follow motionlib: PIL draws all text, 30000/1001 fps, times in seconds relative to the
component's own start, BT.709-tagged H.264. Poppins comes from Media/codex-video-trial/assets/fonts.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np, math, os, subprocess, functools

ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FF = os.environ.get("MOTIONLIB_FFMPEG", ROOT + "/Media/video_edit/bin/ffmpeg")
FONTS = ROOT + "/Media/codex-video-trial/assets/fonts"
FPS = 30000 / 1001

# Renderer anchors from the approved reference (not camera grading values).
BASE = (5, 13, 28)          # deep navy field
CYAN = (104, 197, 255)      # emphasis, eyebrows, lower-third accent
WHITE = (244, 250, 255)     # pale type
GLASS_TINT = (22, 51, 81)
GLASS_LINE = (64, 112, 153)
SPECULAR = (135, 210, 248)
CHIP = (6, 17, 30)
# Teaching colours keep their meaning inside the family (GRAPHICS-STANDARDS.md).
GOOD = (64, 200, 110)
BAD = (235, 64, 64)


def unit(w, h):
    """Reference layout unit in pixels: 2.0 on 1920x1080, 1080x1920 and 1080x1080."""
    return min(w, h) / 540


@functools.lru_cache(None)
def font(px, bold=True):
    return ImageFont.truetype(os.path.join(FONTS, "Poppins-Bold.ttf" if bold else "Poppins-Regular.ttf"),
                              max(1, round(px)))


def ease(t, d=.7):
    q = min(1, max(0, t / d))
    return 1 - (1 - q) ** 3


def text_w(s, f):
    return ImageDraw.Draw(Image.new("RGB", (4, 4))).textlength(s, font=f)


def wrap(s, f, maxw):
    """Greedy word wrap to `maxw` pixels. Explicit newlines are kept."""
    out = []
    for para in s.split("\n"):
        line = ""
        for word in para.split():
            cand = (line + " " + word).strip()
            if line and text_w(cand, f) > maxw:
                out.append(line); line = word
            else:
                line = cand
        out.append(line)
    return out


def rr(im, box, fill=None, r=15, outline=None, width=1):
    ImageDraw.Draw(im).rounded_rectangle(tuple(round(v) for v in box), round(r), fill=fill,
                                         outline=outline, width=max(1, round(width)))


def text(im, xy, s, px, fill=WHITE, bold=True):
    ImageDraw.Draw(im).text((round(xy[0]), round(xy[1])), s, font=font(px, bold), fill=fill)


# ------------------------------------------------------------------ the moving field
@functools.lru_cache(8)
def _grid(w, h):
    gw, gh = max(2, w // 4), max(2, h // 4)
    yy, xx = np.mgrid[:gh, :gw]
    # Blob positions are normalised to the canvas; blob SIZE stays constant in pixels relative to
    # the 1080 short side, so a portrait field has the same soft light as the 16:9 reference.
    s = min(w, h) / 1080
    sx, sy = w / (1920 * s), h / (1080 * s)
    noise = np.random.default_rng(8).normal(0, .42, (gh, gw, 1))
    return xx / gw, yy / gh, sx, sy, noise


def field(t, w=1920, h=1080):
    """Soft Blue Light background (reference `background(t, style=0)`), any canvas size."""
    xx, yy, sx, sy, noise = _grid(w, h)
    a = np.zeros(xx.shape + (3,), float); a[:] = BASE
    gx, gy = .14 + .13 * math.sin(t * .65), .2 + .13 * math.cos(t * .4)
    hx, hy = .83 + .12 * math.cos(t * .6), .88
    g = np.exp(-(((xx - gx) * sx) ** 2 / .18 + ((yy - gy) * sy) ** 2 / .35))
    k = np.exp(-(((xx - hx) * sx) ** 2 / .12 + ((yy - hy) * sy) ** 2 / .18))
    a += g[..., None] * [5, 53, 94] + k[..., None] * [3, 26, 62]
    a = np.clip(a + noise, 0, 255).astype("uint8")
    return Image.fromarray(a).resize((w, h), Image.Resampling.BILINEAR)


# ------------------------------------------------------------------ glass, photos, chips
def glass(im, box, t, u=None, radius=18):
    """Translucent blue glass card: blurs and tints whatever is beneath it, hairline border and a
    short specular line drifting along the top edge. `box` is in pixels."""
    u = u or unit(*im.size)
    x, y, x1, y1 = (round(v) for v in box)
    p = im.crop((x, y, x1, y1)).filter(ImageFilter.GaussianBlur(14 * u / 2))
    p = Image.blend(p, Image.new("RGB", p.size, GLASS_TINT), .54)
    m = Image.new("L", p.size); ImageDraw.Draw(m).rounded_rectangle((0, 0, p.width - 1, p.height - 1),
                                                                    round(radius * u), fill=235)
    im.paste(p, (x, y), m)
    rr(im, (x, y, x1, y1), None, radius * u, GLASS_LINE, u / 2)
    cx = x + 20 * u + (x1 - x - 120 * u) * (.5 + .5 * math.sin(t * .65))
    ImageDraw.Draw(im).line((round(cx), round(y + u), round(cx + 90 * u), round(y + u)),
                            fill=SPECULAR, width=round(2 * u))


@functools.lru_cache(16)
def _src(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def photo_size(path, maxw, maxh):
    """Frame size that fits the photo's own aspect inside maxw x maxh (no letterbox, no stretch)."""
    iw, ih = _src(str(path)).size
    k = min(maxw / iw, maxh / ih)
    return iw * k, ih * k


def photo_card(im, path, box, t, delay=0, fit=False, u=None):
    """Photo in a rounded blue frame with a soft shadow; rises 48 units and fades in, then a very
    slow 1.4 %/s push (photo only, never the presenter). box=(x, y, w, h) in pixels.
    fit=False shows the whole photo (contain); fit=True fills the frame (top-anchored crop)."""
    u = u or unit(*im.size)
    x, y, w, h = box
    q = ease(t - delay)
    if q <= 0: return
    y += (1 - q) * 48 * u
    z = 1 + .014 * max(0, t - delay)
    src = _src(str(path))
    if fit:
        sw, sh = round(w * z), round(h * z)
        p = ImageOps.fit(src, (sw, sh), centering=(.5, 0))
        p = p.crop(((sw - w) / 2, (sh - h) / 2, (sw + w) / 2, (sh + h) / 2))
    else:
        p = ImageOps.contain(src, (round(w), round(h)))
    pad = 15 * u
    L = Image.new("RGBA", (round(w + 2 * pad), round(h + 2 * pad)))
    d = ImageDraw.Draw(L)
    d.rounded_rectangle((10 * u, 13 * u, w + 22 * u, h + 25 * u), round(18 * u), fill=(0, 2, 12, 110))
    L = L.filter(ImageFilter.GaussianBlur(5 * u))
    d = ImageDraw.Draw(L)
    d.rounded_rectangle((7 * u, 7 * u, w + 17 * u, h + 17 * u), round(13 * u), fill=(42, 80, 113, 255),
                        outline=(118, 183, 222, 150), width=round(u))
    L.paste(p, (round((w - p.width) / 2 + 12 * u), round((h - p.height) / 2 + 12 * u)))
    if q < 1:
        L.putalpha(L.getchannel("A").point(lambda a: round(a * q)))
    im.paste(L, (round(x - 12 * u), round(y - 12 * u)), L)


def disclosure(im, s, xy=None, u=None, anchor="lt", size=23):
    """Dark chip for 'Real picture of me. Not AI-generated.' / 'AI-GENERATED'. The caller places
    it clear of face and abs (VIDEO-RULES: measure the rendered frame). Returns the chip box."""
    u = u or unit(*im.size)
    f = font(size * u, False)
    tw = text_w(s, f)
    bw, bh = tw + 40 * u, 40 * u
    x, y = xy
    if "m" in anchor[0]: x -= bw / 2
    if anchor[0] == "r": x -= bw
    rr(im, (x, y, x + bw, y + bh), CHIP, 12 * u)
    ImageDraw.Draw(im).text((x + 20 * u, y + 7 * u), s, font=f, fill=WHITE)
    return (x, y, x + bw, y + bh)


# ------------------------------------------------------------------ Motivation lower third
def lower_third_default_box(w, h, lines=1):
    """Default placement (x0, y_top, x1, height) for a lower third with `lines` main-text lines.
    16:9 matches the approved reference exactly (x 86..1828, bottom 64 px from the frame edge;
    captions lift above it, the 2026-09-02 standing rule). 1:1 keeps the bottom placement.
    9:16 sits with its bottom at 68 % of the height, above the 70-84 % caption band and the
    platform UI; always re-measure against the actual captions and the moving presenter."""
    u = unit(w, h)
    bh = (88 + 36 * (lines - 1)) * u
    if w > h * 1.2:
        x0, x1, bottom = 43 * u, w - 46 * u, h - 32 * u
    elif h > w * 1.2:
        x0, x1, bottom = 34 * u, w - 34 * u, h * .68
    else:
        x0, x1, bottom = 34 * u, w - 34 * u, h - 32 * u
    return x0, bottom - bh, x1, bh


def lower_third(im, t, topic, point, dur=None, box=None, u=None, out_dur=.35):
    """The approved Motivation lower third, composited onto a footage frame (RGB PIL image).

    Slim cyan accent at the left, small uppercase TOPIC pre-header, bold main POINT typed on at
    55 characters/s from 0.15 s, glass strip rising 90 units with a 0.7 s ease. `topic` adapts to
    the narration (MOTIVATION was the gym beat, KEY POINT for a single distilled point, etc.).
    Long points wrap and the strip grows; `box=(x0, y_top, x1)` overrides the placement.
    With `dur`, it eases back out over the last `out_dur` seconds. Returns the image."""
    if t < 0 or (dur is not None and t > dur): return im
    w, h = im.size
    u = u or unit(w, h)
    fmain = font(28 * u)
    x0d, _, x1d, _ = lower_third_default_box(w, h)
    x0, x1 = (box[0], box[2]) if box else (x0d, x1d)
    lines = wrap(point, fmain, x1 - x0 - 31 * u - 24 * u)
    _, ytop, _, bh = lower_third_default_box(w, h, len(lines))
    if box: ytop = box[1]
    base = im.copy() if (dur is not None and t > dur - out_dur) else None
    q = ease(t)
    y = ytop + (1 - q) * 90 * u
    glass(im, (x0, y, x1, y + bh), t, u)
    rr(im, (x0 + u, y + 3 * u, x0 + 9 * u, y + bh - 3 * u), CYAN, 4 * u)
    text(im, (x0 + 31 * u, y + 13 * u), topic.upper(), 14 * u, CYAN)
    n = max(0, int((t - .15) * 55))
    for i, ln in enumerate(lines):
        vis = ln[:max(0, min(len(ln), n))]
        n -= len(ln) + 1
        if vis: text(im, (x0 + 31 * u, y + (38 + 36 * i) * u), vis, 28 * u)
    if base is not None:
        a = ease(dur - t, out_dur)
        im = Image.blend(base, im, a)
    return im


def lower_third_band(w, h, point, box=None):
    """Pixel band (x, y, bw, bh) a lower third can touch during its entrance, for patches/QC."""
    u = unit(w, h)
    x0, ytop, x1, _ = lower_third_default_box(w, h)
    if box: x0, ytop, x1 = box
    lines = wrap(point, font(28 * u), x1 - x0 - 55 * u)
    _, yt, _, bh = lower_third_default_box(w, h, len(lines))
    if box: yt = box[1]
    y0 = max(0, int(yt - 2 * u)); y1 = min(h, int(math.ceil(yt + bh + 92 * u)))
    xa = max(0, int(x0 - 2 * u)); xb = min(w, int(math.ceil(x1 + 2 * u)))
    return xa - xa % 2, y0 - y0 % 2, (xb - xa + xa % 2 + 1) // 2 * 2, (y1 - y0 + y0 % 2 + 1) // 2 * 2


# ------------------------------------------------------------------ full-screen scenes
def scene_fact(t, w, h, photo, eyebrow, headline, detail=None, label=None, fit=False):
    """Photo + glass fact card (reference 1-before). 16:9: photo left, card right. 9:16 and 1:1:
    photo on top, card beneath. `label` is the disclosure string, placed under the photo."""
    im = field(t, w, h); u = unit(w, h)
    land = w > h * 1.2
    if land:
        # the approved reference keeps a fixed 362x405 frame with the photo contained in it
        pw, ph = 362 * u, 405 * u
        px, py = 67 * u, 38 * u
        card = (476 * u, 126 * u, 906 * u, 359 * u)
    else:
        # stacked: photo, disclosure, card; the whole block is centred vertically
        gap = (70 if label else 30) * u
        ch = (215 if detail else 150) * u      # card only as tall as its content
        maxh = h * .46 if h > w * 1.2 else h - 48 * u - gap - ch
        pw, ph = (w - 80 * u, maxh) if fit else photo_size(photo, w - 80 * u, maxh)
        px, py = (w - pw) / 2, (h - (ph + gap + ch)) / 2 + 12 * u
        cy = py + ph + gap
        card = (40 * u, cy, w - 40 * u, cy + ch)
    photo_card(im, photo, (px, py, pw, ph), t, fit=fit, u=u)
    if label:
        if land: disclosure(im, label, (162 * u, 484 * u), u)
        else: disclosure(im, label, (px + pw / 2, py + ph + 20 * u), u, anchor="mt")
    glass(im, card, t, u)
    cx = card[0] + 27 * u
    if t > .2: text(im, (cx, card[1] + 22 * u), eyebrow, 32 * u)
    if t > .7: text(im, (cx, card[1] + 83 * u), headline, 42 * u, CYAN)
    if detail and t > 1.3: text(im, (cx + u, card[1] + 164 * u), detail, 23 * u, bold=False)
    return im


def scene_portraits(t, w, h, photos, label=None):
    """Three vertical portraits with identical frame proportions (the only approved three-photo
    format), staggered 0.22 s, plural disclosure beneath. 16:9 and 1:1: one row. 9:16: two over
    one, so the portraits fill the tall frame instead of a thin strip. Portrait photos only."""
    im = field(t, w, h); u = unit(w, h)
    n = len(photos); land = w > h * 1.2; tall = h > w * 1.2
    lab = 70 * u if label else 0
    if tall and n == 3:
        gap = 20 * u
        pw = min((w - 80 * u - gap) / 2, ((h - 120 * u - lab - gap) / 2) * 263 / 405); ph = pw * 405 / 263
        y0 = (h - (2 * ph + gap + lab)) / 2
        cells = [((w - gap) / 2 - pw, y0), ((w + gap) / 2, y0), ((w - pw) / 2, y0 + ph + gap)]
        bottom = y0 + 2 * ph + gap
    else:
        gap = 44 * u if land else 14 * u
        side = 40 * u if land else 24 * u
        pw = min(263 * u, (w - 2 * side - (n - 1) * gap) / n); ph = pw * 405 / 263
        x0 = (w - (n * pw + (n - 1) * gap)) / 2
        y0 = 33 * u if land else (h - ph - lab) / 2
        cells = [(x0 + i * (pw + gap), y0) for i in range(n)]
        bottom = y0 + ph
    for i, (p, (x, y)) in enumerate(zip(photos, cells)):
        photo_card(im, p, (x, y, pw, ph), t, i * .22, fit=True, u=u)
    if label:
        disclosure(im, label, (w / 2, bottom + 26 * u), u, anchor="mt")
    return im


def scene_photo(t, w, h, photo, label=None, label_xy=None):
    """One large photo on the field (reference 1-family). Horizontal photos in sequence: render
    one scene per photo and cut them consecutively, never a forced portrait triptych."""
    im = field(t, w, h); u = unit(w, h)
    pw, ph = photo_size(photo, w - (210 if w > h * 1.2 else 80) * u, h - (115 if w > h * 1.2 else 160) * u)
    px, py = (w - pw) / 2, (h - ph) / 2 - 10 * u
    photo_card(im, photo, (px, py, pw, ph), t, u=u)
    if label:
        disclosure(im, label, label_xy or (w / 2, py + ph + 22 * u), u, anchor="mt")
    return im


def scene_cta(t, w, h, eyebrow="YOUR NEXT STEP", headline="Try AbsByAI\nfree for 7 days.",
              button="START YOUR FREE TRIAL"):
    """CTA (reference 1-cta): cyan eyebrow, big headline lines staggered 0.35 s with a 22-unit
    rise, then a glass button at 0.7 s. Headline wraps to the canvas."""
    im = field(t, w, h); u = unit(w, h)
    land = w > h * 1.2
    x = (75 if land else 40) * u
    avail = (820 if land else (w / u - 80)) * u
    # keep the author's line breaks: shrink the headline (down to 44 units) before wrapping
    size = 64
    while size > 44 and max(text_w(l, font(size * u)) for l in headline.split("\n")) > avail:
        size -= 2
    lines = wrap(headline, font(size * u), avail)
    lh = 83 * size / 64
    if land:
        y = 79 * u
    else:  # centre eyebrow + headline + button vertically
        y = (h - (61 + len(lines) * lh + 54 + 104) * u) / 2
    text(im, (x + 3 * u, y), eyebrow, 20 * u, CYAN)
    y += 61 * u
    for i, ln in enumerate(lines):
        if t > i * .35:
            text(im, (x, y + i * lh * u + round((1 - ease(t - i * .35)) * 22 * u)), ln, size * u)
    by = y + len(lines) * lh * u + 54 * u
    if t > .7:
        bw = (804 if land else w / u - 80) * u
        glass(im, (x + 3 * u, by, x + 3 * u + bw, by + 104 * u), t, u)
        fb = font(36 * u)
        tx = x + 60 * u if land else x + 3 * u + (bw - text_w(button, fb)) / 2
        text(im, (tx, by + 28 * u), button, 36 * u)
    return im


# ------------------------------------------------------------------ encoding
def _encoder(path, w, h, crf=18):
    return subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                             "-r", "30000/1001", "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", "medium",
                             "-crf", str(crf), "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                             "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", str(path)],
                            stdin=subprocess.PIPE)


def render_scene(out, dur, fn, w=1920, h=1080):
    """Encode fn(t) -> RGB image for `dur` seconds as an opaque BT.709 H.264 insert."""
    p = _encoder(out, w, h)
    for i in range(round(dur * FPS)):
        p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0
    return out


def render_over_footage(src, out, dur, fn, start=0.0, w=1920, h=1080, vf=None):
    """Decode `src` from `start` for `dur` s through `vf` (must yield w x h; scaled if omitted),
    call fn(frame, t) per frame and encode. Decoding is BT.709-accurate (untagged editor
    masters decode wrong otherwise: memory `untagged-video-bt601-trap`)."""
    chain = (vf + "," if vf else "") + f"scale={w}:{h}:in_color_matrix=bt709:out_color_matrix=bt709:flags=accurate_rnd+bicubic"
    dec = subprocess.Popen([FF, "-v", "error", "-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}",
                            "-vf", chain, "-r", "30000/1001", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"],
                           stdout=subprocess.PIPE)
    enc = _encoder(out, w, h)
    n, size = 0, w * h * 3
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size: break
        im = Image.frombytes("RGB", (w, h), buf)
        enc.stdin.write(fn(im, n / FPS).convert("RGB").tobytes()); n += 1
    dec.wait(); enc.stdin.close(); assert enc.wait() == 0 and n > 0, "no frames decoded"
    return out


def lower_third_patch(src, out, start, dur, topic, point, w=1920, h=1080, box=None, vf=None):
    """Render one lower third over `src` (the graded, caption-free base the layout will overlay
    onto) as an opaque patch of its band only. Returns (out, x, y); overlay it with
    `overlay=x:y:enable='between(t,start,start+dur)'` after `-itsoffset start`."""
    bx, by, bw, bh = lower_third_band(w, h, point, box)
    crop = f"crop={bw}:{bh}:{bx}:{by}"
    full_vf = (vf + "," if vf else "") + f"scale={w}:{h}:in_color_matrix=bt709:out_color_matrix=bt709:flags=accurate_rnd+bicubic"

    def fn(frame, t):
        # the band is re-embedded into a full canvas so glass/blur/wrap match a full-frame render
        canvas = Image.new("RGB", (w, h)); canvas.paste(frame, (bx, by))
        canvas = lower_third(canvas, t, topic, point, dur=dur, box=box)
        return canvas.crop((bx, by, bx + bw, by + bh))
    render_over_footage(src, out, dur, fn, start, bw, bh, vf=full_vf + "," + crop)
    return out, bx, by
