#!/usr/bin/env python3
"""SQUARE (1080x1080) rebuild of Muhammad's design system for Ad 1.

This is `vlib.py` (the approved 9:16 build) re-laid-out for 1:1. Every COLOUR, grid pitch,
type weight, reveal and easing is unchanged -- they were measured off his 16:9 render and
Dan approved them in the vertical. Only the GEOMETRY changes, per the square rules in
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md`:

  * the talking head is a 1080x1080 crop of the 1080p source at 1.00x -- NO upscale at all
    (the vertical is forced into 1.78x). This is the square's one free advantage.
  * TWO beat families, not one:
      STACKED     -- his text-left / Dan-right bullet screens. A 1:1 text column is only
                     ~620 px if Dan sits beside it, which puts his 48 px type at 27 px.
                     So Dan goes in a window at the TOP and the text runs full width below.
      SIDE-BY-SIDE -- portrait media (the app recording). A 1:1 frame HAS the width for
                     his own left/right split, so it keeps it.
  * 16:9 media never goes full bleed: it goes in his olive card at the media's own aspect,
    which is a downscale.
  * safe area: nothing that must be READ below y=980 or above y=80, and nothing readable
    in the right-hand 100 px (in-feed UI). Captions centred at y=880.
"""
import sys, os, math
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import motionlib as M
from PIL import Image, ImageDraw, ImageFilter
from motionlib import font, wrap, text_size, text_bbox, oblique, drop_shadow, nframes, encode
from motionlib import ease_out_cubic, ease_out_expo, ease_out_back, ease_in_out, clamp01

VW, VH = 1080, 1080
FPS = 30000/1001
SRC_W, SRC_H = 1920, 1080          # the graded conform this build crops from

FIELD    = (13, 14, 11)
FIELD_HI = (23, 25, 19)
OLIVE    = (140, 153, 91)
CARD_OL  = (90, 100, 58)
INK      = (255, 255, 255)
INK_SOFT = (176, 184, 158)
BAR      = (0, 0, 0)

# --- square safe area ---------------------------------------------------------
# A Demand Gen in-feed / Discover / Gmail slot puts its own UI along the bottom and the
# right-hand edge, and Reels/feed crops nibble the top. Nothing that must be read goes
# outside 80..980, and nothing readable sits in the right-hand 100 px.
TOP_SAFE, BOT_SAFE = 80, 980
RIGHT_SAFE = 100
CAP_Y  = 880                # caption band: 64 px ExtraBold ends ~958, clear of 980
MARGIN = 64

# ------------------------------------------------------------------ background
_FIELD_CACHE = {}
def field(w=VW, h=VH, grid=True):
    """Dark field + radial lift + the fine grid he uses on every graphic screen."""
    key = (w, h, grid)
    if key in _FIELD_CACHE: return _FIELD_CACHE[key].copy()
    sm = Image.new("RGB", (54, 54)); px = sm.load()
    for y in range(54):
        for x in range(54):
            d = math.hypot((x-27)/27, (y-27)/27)
            k = clamp01(1 - d*0.8)
            px[x, y] = tuple(int(FIELD[i] + (FIELD_HI[i]-FIELD[i])*k) for i in range(3))
    im = sm.resize((w, h), Image.BICUBIC)
    if grid:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        P = 46                                   # same pitch as the vertical: his 73px at 1920
        for x in range(0, w, P): d.line([(x, 0), (x, h)], fill=(255, 255, 255, 9))
        for y in range(0, h, P): d.line([(0, y), (w, y)], fill=(255, 255, 255, 9))
        im = Image.alpha_composite(im.convert("RGBA"), g).convert("RGB")
    _FIELD_CACHE[key] = im
    return im.copy()

def vignette_mask(w=VW, h=VH):
    """His radial falloff, re-derived in the SQUARE frame's own coordinates (never the
    9:16 mask carried over -- the radius means a different thing in a different frame)."""
    from grade import VIGNETTE
    import numpy as np
    ys, xs = np.mgrid[0:h, 0:w]
    r = np.hypot((xs-w/2)/(w/2), (ys-h/2)/(h/2))
    rr = np.array([p[0] for p in VIGNETTE]); gg = np.array([p[1] for p in VIGNETTE])
    return np.interp(r, rr, gg).astype("float32")

# ------------------------------------------------------------------ helpers
def rrect(im, box, radius, fill=None, outline=None, width=0, glow=0):
    if glow:
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(gl).rounded_rectangle(
            [box[0]-glow, box[1]-glow, box[2]+glow, box[3]+glow],
            radius=radius+glow, fill=OLIVE+(70,))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(glow*0.9)))
    ImageDraw.Draw(im).rounded_rectangle(box, radius=radius, fill=fill,
                                         outline=outline, width=width)

def draw_lines(d, lines, f, x, y, fill, lead=1.12, align="l", w=None):
    lh = int(f.size*lead)
    for i, ln in enumerate(lines):
        xx = x
        if align == "c": xx = x + (w - text_size(ln, f)[0])//2
        d.text((xx, y + i*lh), ln, font=f, fill=fill, anchor="lt")
    return y + lh*len(lines)

def cover(img, w, h, ox=0.5, oy=0.5):
    img = M.oriented(img).convert("RGB")
    s = max(w/img.width, h/img.height)
    im = img.resize((max(1,int(img.width*s)), max(1,int(img.height*s))), Image.LANCZOS)
    x = int((im.width-w)*ox); y = int((im.height-h)*oy)
    return im.crop((x, y, x+w, y+h))

# ==============================================================================
#  TYPE-ON REVEAL (unchanged from the approved vertical)
# ==============================================================================
def draw_type(d, txt, f, x, y, fill, k, tail=5, spread=0.75, anchor_w=None):
    """Type-on reveal. ⚠ EVERY CHARACTER IS DRAWN ON THE BASELINE (anchor='ls'): PIL's 't'
    anchor is the ascender line OF THE STRING IT IS GIVEN, so per-glyph 'lt' rides periods
    up to cap height and drops every ascender-less letter."""
    n = len(txt)
    if n == 0: return 0
    y = y + f.getmetrics()[0]
    shown = k * (n + tail)
    ax = x
    for i, ch in enumerate(txt):
        lead = shown - i
        if lead <= 0: break
        w = text_size(ch, f)[0]
        if lead >= tail: a, extra = 1.0, 0
        else:
            a = clamp01(lead / tail); extra = int(w * spread * (1 - a))
        col = tuple(int(v * a) for v in fill[:3]) + ((int(fill[3]*a),) if len(fill) > 3 else ())
        d.text((ax, y), ch, font=f, fill=col, anchor="ls")
        ax += w + extra
    return ax - x

def type_lines(d, lines, f, x, y, fill, k, lead=1.14, align="l", w=None, stagger=0.55):
    lh = int(f.size * lead)
    for i, ln in enumerate(lines):
        kk = clamp01((k - i * stagger * (1.0 / max(1, len(lines)))) * (1 + stagger))
        xx = x
        if align == "c": xx = x + (w - text_size(ln, f)[0]) // 2
        draw_type(d, ln, f, xx, y + i * lh, fill, kk)
    return y + lh * len(lines)

# ==============================================================================
#  WINDOW SIZING -- the square's core geometry decision
# ==============================================================================
#  A window of (w, h) is filled by a crop of the 1920x1080 conform. The crop is chosen by
#  MAGNIFICATION, never by "fit the whole room in": fitting the room made Dan a third of the
#  size he is in Muhammad's own frame, and left him off to one side with an empty doorway
#  beside him, because a 1920-wide crop leaves the face track nothing to centre.
MAX_WIN_H, MIN_WIN_H = 700, 380
WIN_TOP = 34
GAP     = 40
# HIS magnification. In his 16:9 frame Dan's panel is source pixels at 1:1 inside a 1920-wide
# picture, and a phone shows that picture about 1080 wide -- so on the viewer's screen his
# Dan is the source scaled by 1080/1920 = 0.5625. The square reproduces that number rather
# than "fit the whole room into the window": fitting the room made Dan a third of his size.
MAG = 1080/1920
CROP_W_MAX = 1400

def window_rect(text_h):
    """Dan's window for a STACKED beat: FULL WIDTH, as tall as the beat's text leaves room
    for. Full width because the crop is chosen by magnification (below), so a wide window
    shows more ROOM at the same size of Dan -- never a smaller Dan."""
    h = BOT_SAFE - WIN_TOP - GAP - text_h - 10
    h = max(MIN_WIN_H, min(MAX_WIN_H, h))
    h -= h % 2
    return (0, WIN_TOP, VW, WIN_TOP+h)

def window_crop(win_w, win_h, cx=None):
    """Source crop (in the 1920x1080 conform) that fills a win_w x win_h window AT HIS
    MAGNIFICATION, clamped so the window is never an upscale. `cx` is the beat's measured
    face centre -- Dan leans, and a fixed x leaves him off-centre."""
    if cx is None:
        from grade import SUBJECT_CX
        cx = SUBJECT_CX
    ar = win_w / win_h
    w = win_w / MAG; h = w / ar
    # ⚠ CAP THE CROP WIDTH. At the full 1920 the crop cannot be centred on him at all (the
    # track's x clamps to 0), so a short window became a letterbox strip of the room with
    # Dan at one edge. 1400 px leaves the track ~260 px of travel and still never upscales
    # (win_w is 1080). The resulting magnification, 0.77, sits between his 0.56 and the
    # approved vertical's 1.78.
    w = min(w, CROP_W_MAX)
    h = w / ar
    if h > SRC_H: h = SRC_H; w = h * ar          # limited by the source height
    if w > SRC_W: w = SRC_W; h = w / ar          # limited by the source width
    w = max(w, win_w)                            # never an upscale
    w = int(min(w, SRC_W)); h = int(min(max(h, win_h), SRC_H))
    w -= w % 2; h -= h % 2
    x = int(round(cx - w/2)); x = max(0, min(x, SRC_W - w))
    # Anchor on the HAIR, not on the centre (memory `framing-standard-hair-anchored`): a
    # centred crop of a shot with this little headroom takes the top of his head.
    y = 0 if h >= SRC_H else 0
    return (w, h, x, y)

# ==============================================================================
#  BEAT PLATES -- one opaque RGBA plate per beat with a rounded "media hole"
# ==============================================================================
def _hole_at(rect, t, in_dur=0.42, grow=0.055):
    k = ease_out_back(clamp01(t/in_dur)) if in_dur > 0 else 1.0
    x0, y0, x1, y1 = rect
    cx, cy = (x0+x1)/2, (y0+y1)/2
    s = (1-grow) + grow*k
    hw, hh = (x1-x0)/2*s, (y1-y0)/2*s
    return (cx-hw, cy-hh, cx+hw, cy+hh)

def _punch(plate, hole, radius):
    m = Image.new("L", plate.size, 255)
    ImageDraw.Draw(m).rounded_rectangle([int(v) for v in hole], radius=radius, fill=0)
    a = plate.getchannel("A").point(lambda v: v)
    plate.putalpha(Image.composite(a, Image.new("L", plate.size, 0), m))
    return plate

# ---- STACKED: Dan above, his text below -------------------------------------
BUL_SIZES = [(46, 42), (42, 38), (38, 34), (34, 31)]   # (bullet, header) ladder

def _bullet_layout(header, bullets):
    """Pick the largest type ladder rung whose wrapped block still leaves Dan a window of
    at least MIN_WIN_H. Never one fixed compromise size (square rule 2)."""
    # ⚠ THE WRAP MUST CLEAR THE RIGHT-HAND SAFE STRIP. Without RIGHT_SAFE the bullets
    # wrapped to x = 1007, i.e. 27 px inside the 100 px an in-feed placement covers with
    # its own UI (audit finding F6). The lower thirds already subtracted it; this did not.
    maxw = VW - MARGIN*2 - 38 - RIGHT_SAFE
    for bs, hs in BUL_SIZES:
        fb, fh = font(bs, "SemiBold"), font(hs, "ExtraBold")
        items = [wrap(b, fb, maxw) for b in bullets]
        lh = int(fb.size*1.14)
        text_h = ((hs+30) if header else 0) + sum(len(it)*lh + 30 for it in items)
        if BOT_SAFE - WIN_TOP - GAP - text_h - 10 >= MIN_WIN_H or (bs, hs) == BUL_SIZES[-1]:
            bottom = WIN_TOP + max(MIN_WIN_H, min(MAX_WIN_H,
                     BOT_SAFE - WIN_TOP - GAP - text_h - 10)) + GAP + text_h
            assert bottom <= BOT_SAFE, f'bullet block ends at y={bottom}, past the {BOT_SAFE} safe line'
            return fb, fh, items, lh, text_h
    raise AssertionError

def _win_plate(dur, body, fps=FPS, text_h=0, radius=0, grow=0.045, in_dur=0.42):
    rect = window_rect(text_h)
    out = []
    for i in range(nframes(dur, fps)):
        t = i / fps
        im = field().convert("RGBA")
        d = ImageDraw.Draw(im)
        body(d, im, t, rect[3] + GAP)
        out.append(_punch(im, _hole_at(rect, t, in_dur, grow), radius))
    return out, rect

def plate_window(header, bullets, dur, fps=FPS, radius=0, stagger=0.62, reveal=1.05):
    """His 'IN TODAY'S EPISODE' screen: olive eyebrow + white bullets, Dan above."""
    fb, fh, items, lh, text_h = _bullet_layout(header, bullets)
    def body(d, im, t, ty):
        if header:
            k = clamp01((t-0.08)/0.42)
            wdt = draw_type(d, header.upper(), fh, MARGIN, ty, OLIVE+(255,), k)
            d.rectangle([MARGIN, ty+fh.size+13, MARGIN+int(wdt*clamp01(k*1.2)), ty+fh.size+18],
                        fill=OLIVE)
            ty += fh.size + 48
        for n, lines in enumerate(items):
            k = clamp01((t - (0.30 + n*stagger)) / reveal)
            if k <= 0: break
            d.rectangle([MARGIN, ty+16, MARGIN+13, ty+29],
                        fill=tuple(int(v*clamp01(k*4)) for v in OLIVE))
            type_lines(d, lines, fb, MARGIN+36, ty, INK+(255,), k, lead=1.14)
            ty += len(lines)*lh + 30
    return _win_plate(dur, body, fps, text_h, radius)

def plate_stmt_window(parts, dur, fps=FPS, radius=0, reveal=1.15):
    """His 'Chat GPT / General Purpose AI' screen -- the same split as the bullets."""
    for big, mid in ((62, 50), (56, 45), (50, 40)):
        fbig, fmid = font(big, "ExtraBold"), font(mid, "SemiBold")
        lines = []
        for txt, kind in parts:
            f = fbig if kind in ("big", "olive") else fmid
            col = OLIVE if kind == "olive" else INK
            for ln in wrap(txt, f, VW-2*MARGIN-RIGHT_SAFE): lines.append((ln, f, col))
        text_h = sum(int(f.size*1.16) for _, f, _ in lines)
        if BOT_SAFE - WIN_TOP - GAP - text_h - 10 >= MIN_WIN_H or big == 50: break
    bottom = WIN_TOP + max(MIN_WIN_H, min(MAX_WIN_H,
             BOT_SAFE - WIN_TOP - GAP - text_h - 10)) + GAP + text_h
    assert bottom <= BOT_SAFE, f'statement block ends at y={bottom}, past the {BOT_SAFE} safe line'
    def body(d, im, t, ty):
        for n, (ln, f, col) in enumerate(lines):
            k = clamp01((t - 0.25 - n*0.22) / reveal)
            draw_type(d, ln, f, MARGIN, ty, col+(255,), k)
            ty += int(f.size*1.16)
    return _win_plate(dur, body, fps, text_h, radius)

# ---- SIDE-BY-SIDE: his own left/right split, kept ---------------------------
def plate_window_media(dur, media_ar, fps=FPS, radius=0, gap=26, dan_left=True):
    """His 'phone left / Dan right' product screen. A 1:1 frame HAS the width for his own
    arrangement, so the square keeps it instead of stacking (square rule 2).

    Returns (frames, dan_rect, media_hole)."""
    top, bot = 40, VH - 40
    h = bot - top                                     # 1000
    # media first: it is the subject on this beat
    mh = h; mw = int(round(mh * media_ar))
    dan_w = VW - mw - gap - 2*20
    if dan_w < 360:                                   # a very narrow phone still leaves room
        mh = int(h*0.96); mw = int(round(mh*media_ar)); dan_w = VW - mw - gap - 2*20
    dan_w -= dan_w % 2; mw -= mw % 2; mh -= mh % 2
    x = 20
    if dan_left:
        dan = (x, top, x+dan_w, top+h)
        hx = x + dan_w + gap
        hole = (hx, top + (h-mh)//2, hx+mw, top + (h-mh)//2 + mh)
    else:
        hole = (x, top + (h-mh)//2, x+mw, top + (h-mh)//2 + mh)
        dx = x + mw + gap
        dan = (dx, top, dx+dan_w, top+h)
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        hh = _hole_at(hole, t, 0.42, 0.06)
        rrect(im, [hh[0]-11, hh[1]-11, hh[2]+11, hh[3]+11], 22, fill=CARD_OL+(255,), glow=20)
        im = _punch(im, hh, 16)
        im = _punch(im, _hole_at(dan, t, 0.30, 0.03), radius)
        out.append(im)
    return out, dan, hole

# ---- CARD -------------------------------------------------------------------
def card_hole(media_ar, has_text, full_height=False):
    """Biggest card that fits the media's OWN aspect ratio. A fixed 16:9 hole cover-crops a
    portrait photo, and what it crops off a photo of a person is their head."""
    maxw = VW - 2*40
    top = TOP_SAFE - 20
    bot = (CAP_Y - 30) if not has_text else (CAP_Y - 110)
    if full_height: top, bot = 0, VH
    maxh = bot - top
    w, h = maxw, maxw/media_ar
    if h > maxh: h, w = maxh, maxh*media_ar
    cx, cy = VW//2, top + maxh/2
    return (int(cx-w/2), int(cy-h/2), int(cx+w/2), int(cy+h/2))

def plate_card(dur, caption=None, label=None, portrait=False, fps=FPS,
               top_kicker=None, hole=None, media_ar=None):
    if hole is None:
        if media_ar is None: media_ar = 0.62 if portrait else 16/9
        hole = card_hole(media_ar, bool(caption or top_kicker))
    fc = font(40, "SemiBold"); fl = font(28, "SemiBold")
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        d  = ImageDraw.Draw(im)
        h  = _hole_at(hole, t)
        rrect(im, [h[0]-12, h[1]-12, h[2]+12, h[3]+12], 26, fill=CARD_OL+(255,), glow=22)
        ty = hole[3] + 40
        if top_kicker:
            k = ease_out_expo(clamp01((t-0.10)/0.42))
            kf = font(64, "ExtraBold")
            lay = Image.new("RGBA", (VW, VH), (0,0,0,0))
            lines = wrap(top_kicker.upper(), kf, VW-2*MARGIN)
            draw_lines(ImageDraw.Draw(lay), lines, kf, MARGIN, ty,
                       tuple(int(v*k) for v in OLIVE), lead=1.06, align="c", w=VW-2*MARGIN)
            hgt = len(lines)*int(kf.size*1.06)
            im.alpha_composite(oblique(lay, 9.0, pivot_y=ty+hgt/2))
            wdt = max(text_size(x, kf)[0] for x in lines)
            d.rectangle([(VW-wdt)//2, ty+hgt+8, (VW-wdt)//2+int(wdt*k), ty+hgt+14], fill=OLIVE)
            ty += hgt + 34
        if caption:
            k = ease_out_cubic(clamp01((t-0.30)/0.42))
            lines = wrap(caption, fc, VW-2*MARGIN)
            draw_lines(d, lines, fc, MARGIN, ty+int((1-k)*16),
                       tuple(int(v*k) for v in INK), lead=1.14, align="c", w=VW-2*MARGIN)
        out.append(_punch(im, h, 18))
        if label:
            out[-1].alpha_composite(chip_layer(label, int(h[3]) - 34, fl))
    return out, hole

# ---- LABEL CHIPS ------------------------------------------------------------
#  Two mutually exclusive labels (AGENTS.md, Dan 2026-09-11):
#    'AI-GENERATED'                        on every AI image / clip
#    'Real picture of me — not AI-generated'  on every real after picture of Dan
#  Both sit LOW on the frame, above the caption band, NEVER over his face.
REAL_LABEL = "Real picture of me — not AI-generated"
AI_LABEL   = "AI-GENERATED"

def chip_layer(label, y_bottom, f=None, max_w=None):
    """One chip, centred, its BOTTOM edge at y_bottom."""
    f = f or font(34, "SemiBold")
    max_w = max_w or (VW - 2*40)
    while f.size > 22 and text_size(label, f)[0] + 34 > max_w:
        f = font(f.size-2, "SemiBold")
    lw, lh = text_size(label, f)
    lay = Image.new("RGBA", (VW, VH), (0,0,0,0))
    bx = (VW-(lw+34))//2
    by = int(y_bottom) - (lh+22)
    ImageDraw.Draw(lay).rounded_rectangle([bx, by, bx+lw+34, by+lh+22], radius=9,
                                          fill=(0,0,0,215))
    ImageDraw.Draw(lay).text((bx+17, by+11), label, font=f, fill=INK, anchor="lt")
    return lay

def bleed_chip(label, y_bottom=None):
    """Chip for a full-bleed shot: low on the frame, at the shorts/waist line, above the
    caption band -- never over his face (Dan, 2026-08-27)."""
    return chip_layer(label, y_bottom if y_bottom is not None else CAP_Y - 26)

# ---- TITLE ------------------------------------------------------------------
def plate_title_card(headline, sub, dur, fps=FPS):
    """His 'VISUALIZING YOUR GOAL' beat: an olive card on the bare field, heavy oblique
    caps typing on, subtitle under. No Dan."""
    fh, fs = font(82, "ExtraBold"), font(40, "SemiBold")
    hl = wrap(headline.upper(), fh, VW-2*130)
    sl = wrap(sub, fs, VW-2*130) if sub else []
    lh, ls = int(fh.size*1.06), int(fs.size*1.20)
    inner = len(hl)*lh + (34+len(sl)*ls if sl else 0)
    ch = inner + 120
    box = (60, (VH-ch)//2, VW-60, (VH-ch)//2 + ch)
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = field().convert("RGBA")
        k0 = ease_out_back(clamp01(t/0.40))
        cx, cy = (box[0]+box[2])/2, (box[1]+box[3])/2
        hw, hh = (box[2]-box[0])/2*(0.94+0.06*k0), (box[3]-box[1])/2*(0.94+0.06*k0)
        rrect(im, [cx-hw, cy-hh, cx+hw, cy+hh], 26, fill=CARD_OL+(255,), glow=22)
        lay = Image.new("RGBA", (VW, VH), (0,0,0,0)); d = ImageDraw.Draw(lay)
        y = box[1] + 60
        for n, ln in enumerate(hl):
            k = clamp01((t - 0.18 - n*0.26)/0.62)
            draw_type(d, ln, fh, (VW - text_size(ln, fh)[0])//2, y, INK+(255,), k)
            y += lh
        lay = oblique(lay, 9.0, pivot_y=box[1]+60+len(hl)*lh/2)
        im.alpha_composite(lay)
        if sl:
            y += 34
            d2 = ImageDraw.Draw(im)
            for n, ln in enumerate(sl):
                k = clamp01((t - 0.55 - n*0.18)/0.55)
                draw_type(d2, ln, fs, (VW - text_size(ln, fs)[0])//2, y, INK+(255,), k)
                y += ls
        out.append(im)
    return out, None

# ------------------------------------------------------------------ overlays
def overlay_lower_third(lines, dur, fps=FPS, y_bottom=None, in_dur=0.55):
    """Olive tab + black bar + white type, revealed letter by letter. Seven of these carry
    his cut; captions are suppressed for their duration."""
    y_bottom = y_bottom if y_bottom is not None else BOT_SAFE - 10
    AVAIL = VW - 2*36 - 86 - RIGHT_SAFE//2
    fs = []
    for n, t in enumerate(lines):
        sz = 44 if n == 0 else 34
        w8 = "ExtraBold" if n == 0 else "SemiBold"
        while sz > 22 and text_size(t, font(sz, w8))[0] > AVAIL: sz -= 2
        fs.append(font(sz, w8))
    ws  = [text_size(t, f)[0] for t, f in zip(lines, fs)]
    lhs = [int(f.size*1.30) for f in fs]
    bw = min(max(ws) + 86, VW - 2*36)
    bh = sum(lhs) + 28
    bx, by = (VW-bw)//2 + 18, y_bottom - bh
    TAB = 22
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        im = Image.new("RGBA", (VW, VH), (0,0,0,0))
        o  = 1.0 - ease_in_out(clamp01((t-(dur-0.32))/0.32))
        gw = ease_out_cubic(clamp01(t/0.34))
        d  = ImageDraw.Draw(im)
        d.rounded_rectangle([bx-TAB-12, by, bx-12, by+bh], radius=7, fill=OLIVE+(int(235*o*gw),))
        d.rounded_rectangle([bx, by, bx+int(bw*gw), by+bh], radius=7, fill=(0,0,0,int(232*o)))
        yy = by + 14
        for n, (txt, f, lh) in enumerate(zip(lines, fs, lhs)):
            k = clamp01((t - 0.20 - n*0.55)/0.80)
            draw_type(d, txt, f, bx + (bw - text_size(txt, f)[0])//2, yy, INK+(int(255*o),), k)
            yy += lh
        out.append(im)
    return out, None

def overlay_cta(top, big, dur, fps=FPS, y=None):
    """His sage CTA pill. RGBA overlay -- it sits ON Dan, it does not replace him."""
    ft, fb = font(34, "SemiBold"), font(58, "ExtraBold")
    tl = wrap(top, ft, VW-2*MARGIN-70); bl = wrap(big, fb, VW-2*MARGIN-70)
    w = max([text_size(x, ft)[0] for x in tl] + [text_size(x, fb)[0] for x in bl]) + 84
    w = min(w, VW-2*44)
    h = len(tl)*int(ft.size*1.2) + len(bl)*int(fb.size*1.12) + 52
    y = y if y is not None else CAP_Y - h//2 - 10
    x = (VW-w)//2
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        k = ease_out_back(clamp01(t/0.40))
        o = 1.0 - ease_in_out(clamp01((t-(dur-0.30))/0.30))
        im = Image.new("RGBA", (VW, VH), (0,0,0,0))
        ww, hh = int(w*(0.94+0.06*k)), int(h*(0.94+0.06*k))
        bx, by = (VW-ww)//2, y+(h-hh)//2
        rrect(im, [bx, by, bx+ww, by+hh], 22, fill=OLIVE+(int(255*o),), glow=14)
        d = ImageDraw.Draw(im)
        yy = by+24
        yy = draw_lines(d, tl, ft, bx, yy, (255,255,255,int(255*o)), lead=1.2, align="c", w=ww)
        draw_lines(d, bl, fb, bx, yy+4, (255,255,255,int(255*o)), lead=1.12, align="c", w=ww)
        out.append(im)
    return out, None

def overlay_inset_photo(img_path, dur, fps=FPS, rect=(28, 300, 250, 610)):
    x0, y0, x1, y1 = rect
    w, h = x1-x0, y1-y0
    img = Image.open(img_path).convert("RGB")
    s = min(w/img.width, h/img.height)
    iw, ih = int(img.width*s), int(img.height*s)
    img = img.resize((iw, ih), Image.LANCZOS)
    x1, y1 = x0+iw, y0+ih
    out = []
    for i in range(nframes(dur, fps)):
        t = i/fps
        k = ease_out_back(clamp01((t-0.06)/0.42))
        o = 1.0 - ease_in_out(clamp01((t-(dur-0.30))/0.30))
        im = Image.new("RGBA", (VW, VH), (0,0,0,0))
        if k <= 0 or o <= 0: out.append(im); continue
        ww, hh = max(2,int(iw*(0.86+0.14*k))), max(2,int(ih*(0.86+0.14*k)))
        cx, cy = (x0+x1)//2, (y0+y1)//2
        bx, by = cx-ww//2, cy-hh//2
        a = int(255*o*clamp01(t/0.20))
        sh = Image.new("RGBA", (VW, VH), (0,0,0,0))
        ImageDraw.Draw(sh).rounded_rectangle([bx, by, bx+ww, by+hh], radius=16, fill=(0,0,0,int(160*o)))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
        ph = img.resize((ww, hh), Image.LANCZOS).convert("RGBA")
        m = Image.new("L", (ww, hh), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, ww, hh], radius=16, fill=a)
        ph.putalpha(m)
        im.alpha_composite(ph, (bx, by))
        p = ease_out_cubic(clamp01((t-0.30)/0.45))
        if p > 0:
            hw2, hh2 = ww/2*(1.10-0.10*p)+8, hh/2*(1.10-0.10*p)+8
            ImageDraw.Draw(im).rounded_rectangle([cx-hw2, cy-hh2, cx+hw2, cy+hh2], radius=12,
                                                 outline=(214, 236, 244, int(255*o*p)), width=4)
        out.append(im)
    return out, None
