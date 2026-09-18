#!/usr/bin/env python3
"""adkit.cardlib -- the card toolkit Dan approved on RA-01 (2026-09-18), promoted out of that ad's recipe.

Geometry, the ONE label-chip style, measured chip placement, the J2AD field, fitted photo layers, the
continuing Ken Burns drift, hard-cut card entries and the h264 card encoder -- for 9:16 and 16:9.
Origin: `Claude Ad Videos/the ai trick that got me abs - RA-01/recipe-RA-01/ra01lib.py` (three review rounds).
Rules baked in (do not undo them here -- change the rule in AGENTS.md first):
  * a label chip is placed by MEASURING the person mask on the rendered frame, never at a fixed y, never on
    his face, hair or abs; it shrinks, then wraps, before it may overflow;
  * 9:16 chips live in the platform-safe band (y >= 200, x <= 940, above the caption band);
  * a card leaves the caption band clear (captions run under it on the field);
  * cards enter and leave on HARD CUTS (no alpha fade: a fade put a luma-13 frame between two pictures and
    is the one way two physique pictures could share a frame); every still keeps drifting.
"""
import json, math, os, subprocess, sys, tempfile, shutil
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))            # .claude/skills/_shared  (motionlib lives there)
from PIL import Image, ImageDraw, ImageFilter
import motionlib as ml
from motionlib import font, text_size, J2AD

REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
FF   = f"{REPO}/Media/video_edit/bin/ffmpeg"
FPS  = 30000/1001
PERSONMASK = f"{REPO}/.claude/skills/shorts/reference/recentre/personmask"

LIME  = (167, 186, 90)          # the approved verticals' caption highlight
OLIVE = (140, 152, 88)
PLAN_GREEN = (28, 52, 33)
FIELD = J2AD.field              # (13,14,11)
CHIP_AI   = "AI-GENERATED"
CHIP_REAL = "Real picture of me \u2014 not AI-generated"


class Aspect:
    """Output geometry for one aspect: safe margins, caption line, the chip band and the card rectangle.
    Numbers are the ones measured and gated on RA-01 (GATE_VERSION 2.1.0): 9:16 caption ink top y 1400,
    16:9 y 930; a card that ends at CARD_RECT's bottom clears the captions by >= 30 px."""
    def __init__(self, key):
        self.key = key
        if key == "9x16":
            self.VW, self.VH = 1080, 1920
            self.CAP_Y, self.CAP_SIZE, self.SAFE = 1400, 64, 60
            self.CHIP_BOX  = (60, 200, 940, 1366)
            self.CARD_RECT = (60, 290, 1020, 1352)
        elif key == "16x9":
            self.VW, self.VH = 1920, 1080
            self.CAP_Y, self.CAP_SIZE, self.SAFE = 930, 64, 54
            self.CHIP_BOX  = (54, 54, 1866, 900)
            self.CARD_RECT = (60, 40, 1860, 900)
        else:
            raise ValueError("aspect must be 9x16 or 16x9 (add 1x1 here, measured, when a square needs it)")
    @property
    def size(self): return (self.VW, self.VH)

def person_mask(im):
    """Boolean person silhouette of a RENDERED frame (Apple Vision, .accurate)."""
    import numpy as np
    tmp = tempfile.mkdtemp(prefix="pm_")
    try:
        p = os.path.join(tmp, "f.png"); im.convert("RGB").save(p)
        subprocess.run([PERSONMASK, tmp, p], capture_output=True, text=True)
        mp_ = os.path.join(tmp, "f.mask.png")
        if not os.path.exists(mp_):
            return None
        return np.asarray(Image.open(mp_).convert("L"), dtype=np.float32)/255.0 > 0.5
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def person_bbox(im):
    import numpy as np
    m = person_mask(im)
    if m is None or not m.any(): return None
    rows, cols = np.where(m.any(1))[0], np.where(m.any(0))[0]
    return (int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1]))


def _chip_lines(text, f, two_line):
    if not two_line:
        return [text]
    # split on the em dash if there is one, else at the middle space
    if "—" in text:
        a, b = text.split("—", 1)
        return [a.strip() + " —", b.strip()]
    ws = text.split()
    k = len(ws)//2
    return [" ".join(ws[:k]), " ".join(ws[k:])]


def chip_png(text, path, size=None, pal=J2AD, max_w=None, min_size=22):
    """The one chip style for BOTH labels: a solid rounded block, olive rule, white type.

    R6 (round 2) puts the 9:16 chips inside a platform-safe band and the 16:9 chips fully inside
    the card, so the chip has to FIT a width it is given. It shrinks, and then wraps to two lines,
    before it is ever allowed to overflow -- the same order AGENTS.md asks for when nothing is
    clear enough: "shrink the chip or move it to a corner before you put it on him".
    """
    padx, pady, gap = 26, 16, 6
    start = size or 40
    chosen = None
    # Largest type that fits, single line preferred AT THAT SIZE: wrapping to two lines at 38 px
    # beats shrinking to 24 px to stay on one line, which is what a narrow 16:9 card forces.
    for s in range(start, min_size-1, -2):
        f = font(s, "ExtraBold")
        for two_line in (False, True):
            lines = _chip_lines(text, f, two_line)
            tw = max(text_size(l, f)[0] for l in lines)
            if max_w is None or tw + padx*2 <= max_w:
                chosen = (s, f, lines, tw)
                break
        if chosen:
            break
    if chosen is None:                       # even two lines at min_size do not fit -- say so
        f = font(min_size, "ExtraBold")
        lines = _chip_lines(text, f, True)
        chosen = (min_size, f, lines, max(text_size(l, f)[0] for l in lines))
    s, f, lines, tw = chosen
    lh = max(text_size(l, f)[1] for l in lines)
    w = tw + padx*2
    h = lh*len(lines) + gap*(len(lines)-1) + pady*2
    w -= w % 2; h -= h % 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w-1, h-1], radius=12, fill=pal.field + (255,))
    d.rounded_rectangle([0, 0, w-1, h-1], radius=12, outline=OLIVE + (255,), width=3)
    for i, l in enumerate(lines):
        d.text((w//2, pady + i*(lh+gap)), l, font=f, fill=(255, 255, 255, 255), anchor="mt")
    im.save(path)
    return im.size


def place_chip(masks, chip_wh, A, prefer_top=True, pad=10, box=None):
    """Place the label by MEASURING him on the RENDERED frame — never at a fixed y.

    AGENTS.md, Dan 2026-09-12: "the label will not block my face or my abs... put it above my head,
    to the side, or somewhere that it doesn't block my face and my abs". So: union the person mask
    over the card's whole drift, then take the position, inside the safe area and clear of the
    caption band, whose chip rectangle touches NO person pixel and sits furthest from his head-and-
    torso box. If nothing is clear, the chip shrinks before it ever goes on him.
    """
    import numpy as np
    cw, ch = chip_wh
    M = None
    for m in masks:
        M = m.copy() if M is None else (M | m)
    # R6: the search box is the platform-safe band (9:16) or the card itself (16:9), never the
    # whole frame. `box` is (x0, y0, x1, y1) inclusive of where the chip's rectangle may live.
    bx0, by0, bx1, by1 = box if box else (A.SAFE, A.SAFE, A.VW - A.SAFE, A.CAP_Y - 34)
    S = A.SAFE
    cap_top = by1
    ys, xs = np.where(M)
    if len(ys) == 0:
        return (S, S), "no person found on the card"
    hy0, hy1 = int(ys.min()), int(ys.max())
    hx0, hx1 = int(xs.min()), int(xs.max())
    # head + torso: the top 55 % of the silhouette is where the face and the abs are
    torso_y1 = hy0 + int(0.55*(hy1-hy0))
    integ = np.cumsum(np.cumsum(M.astype(np.int32), 0), 1)
    def occupied(x, y, w, h):
        x0, y0, x1, y1 = x-pad, y-pad, min(A.VW, x+w+pad)-1, min(A.VH, y+h+pad)-1
        x0, y0 = max(0, x0), max(0, y0)
        tot = integ[y1, x1]
        if y0: tot -= integ[y0-1, x1]
        if x0: tot -= integ[y1, x0-1]
        if x0 and y0: tot += integ[y0-1, x0-1]
        return int(tot)
    best, bestscore, why = None, -1e18, ""
    for y in range(by0, max(by0+1, cap_top-ch), 8):
        for x in range(bx0, max(bx0+1, bx1-cw), 12):
            if occupied(x, y, cw, ch): continue
            cx = x+cw/2
            above = y+ch <= hy0
            # the sideways-distance term only means something for a chip BESIDE him; scoring it for
            # a chip that already clears his head drove every label into a corner for no reason.
            d = max(0.0, hy0-(y+ch)) + max(0.0, y-torso_y1)*0.6
            if not above:
                d += max(0.0, hx0-(x+cw))*0.5 + max(0.0, x-hx1)*0.5
            score = d - 0.22*abs(cx - (bx0+bx1)/2) + (400.0 if above else 0.0)
            if score > bestscore:
                bestscore, best = score, (x, y)
                why = ("above his head" if above else
                       "beside him" if (x+cw <= hx0 or x >= hx1) else "in a clear band")
    if best is None:
        return (bx0, by0), "NO CLEAR BAND — chip placed at the box corner; shrink it or move the photo"
    return best, why


def field(A):
    im = Image.new("RGBA", A.size, FIELD + (255,))
    d = ImageDraw.Draw(im)
    for i in range(0, A.VH, 4):                                 # a faint tonal wash, not flat black
        k = i / A.VH
        d.line([(0, i), (A.VW, i)], fill=(int(13+9*k), int(14+9*k), int(11+7*k), 255), width=4)
    return im


def photo_layer(path, A, margin_frac=0.055, radius=22, rect=None):
    """The photograph, fitted whole into `rect` on the field. NEVER cover-cropped: a crop that cuts
    the top of his head or the shorts line is the /coverimage rule and ad-edit lesson 6.

    R1 (round 2): `rect` is A.CARD_RECT, which stops above the caption band, so the captions run
    under the card on the J2AD field instead of being switched off beneath it.
    """
    img = ml.oriented(Image.open(path).convert("RGB"))
    if rect is None:
        m = int(A.VW * margin_frac)
        rect = (m, m, A.VW - m, A.VH - m)
    rx0, ry0, rx1, ry1 = rect
    maxw, maxh = rx1-rx0, ry1-ry0
    k = min(maxw/img.width, maxh/img.height)
    nw, nh = int(img.width*k), int(img.height*k)
    nw -= nw % 2; nh -= nh % 2
    img = img.resize((nw, nh), Image.LANCZOS)
    layer = Image.new("RGBA", A.size, (0, 0, 0, 0))
    x, y = rx0 + (maxw-nw)//2, ry0 + (maxh-nh)//2
    mask = Image.new("L", (nw, nh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, nw-1, nh-1], radius=radius, fill=255)
    layer.paste(img, (x, y), mask)
    return layer, (x, y, x+nw-1, y+nh-1)


def kb(layer, t, dur, direction=1, amp=0.035, canvas=None):
    """Continuing Ken Burns drift. ad-edit lesson 52: a card that animates in and then HOLDS is
    what Dan called out; every still keeps moving. Lesson 7: supersample by scaling the layer."""
    p = 0.0 if dur <= 0 else min(max(t/dur, 0.0), 1.0)
    k = (1.0 + amp*p) if direction > 0 else (1.0 + amp*(1.0-p))
    return ml.scale_about(layer, k, canvas=canvas or layer.size)


def entry(t, in_dur=0.30):
    """Card entry: a small scale spring and NOTHING ELSE.

    ⚠ NO ALPHA FADE. The first build faded every card up from the near-black field, which put a
    luma-13 frame between the third after picture and the AI image at 9.31 s — under the delivery
    gate's black-frame bound (6.0) and therefore invisible to it, and found only by looking at
    consecutive frames. A fade between two physique pictures is also the one thing that could ever
    make them share a frame. Every card in and out is a hard cut.
    """
    if t >= in_dur:
        return 1.0, 1.0
    return 0.94 + 0.06*ml.ease_out_back(t/in_dur), 1.0


def encode_h264(frames, out, size, crf=16):
    """Write RGB frames to an h264 mp4 at the delivered size and frame rate."""
    tmp = tempfile.mkdtemp(prefix="ra01card_")
    try:
        n = 0
        for im in frames:
            im.convert("RGB").save(os.path.join(tmp, "f_%05d.png" % n), compress_level=1); n += 1
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-framerate", "30000/1001",
                        "-i", os.path.join(tmp, "f_%05d.png"),
                        "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
                        "-pix_fmt", "yuv420p", "-r", "30000/1001",
                        "-colorspace", "bt709", "-color_primaries", "bt709",
                        "-color_trc", "bt709", "-color_range", "tv",
                        "-x264-params", "keyint=30:min-keyint=1:scenecut=0", out], check=True)
        return n
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def nf(dur): return max(1, int(round(dur*FPS)))
