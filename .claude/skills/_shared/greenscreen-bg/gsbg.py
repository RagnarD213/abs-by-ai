"""Green-screen background template: the moving backgrounds Dan approved for green-screen reaction and commentary
videos (Dan, 2026-10-24, RO-24 round 2 mockups; README.md beside this file), drawn per frame behind a keyed presenter.

Everything here works in OUTPUT space (1920x1080, float32 RGB 0..1). The keyed presenter comes from a plate (FFV1
gbrap16le, unpremultiplied colour + alpha, the house key's output) and is cropped, premultiplied and scaled by ffmpeg
straight to its screen size, so a film is composed at 1080p and the 4K plate is decoded once per render (no re-key).

Types (Dan's numbers from the mockups; 5, the built TV wall, was rejected):
  1 soft     their clip or photo behind Dan, blurred, darkened, navy-tinted          Dan centre
  2 corner   their clip full screen (muted), Dan talking from the lower-right corner  Dan corner
  2b side    their clip full screen behind (muted), Dan full size to the side         Dan right
  3 wall     a wall of photos scrolling slowly behind Dan                             Dan centre
  4 panel    their before/after pair with weight lost and medication (HyperFrames)    Dan right
  6 cards    tilted photo cards drifting slowly on the Soft Blue field                Dan centre
  7 bigtype  the number and the drug, huge and faint on the field (HyperFrames)       Dan right
  8 set      a realistic studio set (one Codex plate per film); its TV plays their clip or a pair   Dan right

  bg = make_background(seg, ctx)          # seg: one bg_plan.json segment (README "Plan format")
  img = bg.frame(i, cam)                  # i: frame index from the segment start; cam: (s, tx, ty) camera affine
"""
import functools, json, math, os, pathlib, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageOps, ImageDraw, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import softblue as SB                                  # noqa: E402  (the Soft Blue field and palette)

ROOT = pathlib.Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI")
FF = str(ROOT / "Media/video_edit/bin/ffmpeg")         # the render-queue wrapper (passes through inside a held slot)
FFPROBE = str(ROOT / "Media/video_edit/bin/ffprobe")
FACEBOX = pathlib.Path.home() / ".cache/absbyai/facebox"
FPS = 30000 / 1001
OW, OH = 1920, 1080

# ------------------------------------------------------------------ presenter placement
PW, PH = 2880, 1620                                     # plate size (house key output, 16:9 port)
TW = int(round(PW * 0.74)) // 2 * 2; TH = int(round(TW * 9 / 16))   # the tight framing window (round 2)
RIGHT_W_DX = 346                                       # Dan to the side, wide: round 2's S framing (+519 plate px)
RIGHT_T_HX = 1330                                      # Dan to the side, tight: head centre x on screen
CORNER = {"W": dict(k=0.48, hx=1580, hy=490), "T": dict(k=0.65, hx=1505, hy=400)}   # 1.35x apart, like W/T (a 1.14x step read as a jump cut)
FEATHER = 22                                           # px: soft edge where the camera's own frame edge is on screen
PLACEMENT = {"soft": "center", "corner": "corner", "side": "right", "wall": "center", "panel": "right",
             "cards": "center", "bigtype": "right", "set": "right", "plain": "center"}
NUMBER = {"soft": "1", "corner": "2", "side": "2b", "wall": "3", "panel": "4", "cards": "6", "bigtype": "7", "set": "8"}
CAMERA_LOCKED = {"soft", "set", "plain"}               # these zoom with a tight cut, as a real camera would


def shot_head(geo, k0, k1):
    """(top of hair, median head centre x) over plate frames k0..k1 (key16 geo rows: [k, top, cx, x0, x1])."""
    g = [geo[k] for k in range(k0, k1) if k in geo and geo[k][1] >= 0]
    assert g, "no head geometry in this shot"
    return min(x[1] for x in g), float(np.median([x[2] for x in g]))


def affine(mode, framing, top, cx):
    """screen = plate * k + (ox, oy) for a placement mode and framing (W wide / T tight). Hair clearance: T puts the
    hair top 4 % of the window height below the frame top (round 2); W keeps the camera's own headroom."""
    if mode == "center":
        if framing == "W":
            return 2 / 3, 0.0, 0.0
        k = OW / TW; x0 = float(np.clip(cx - TW / 2, 0, PW - TW)); y0 = max(0.0, top - 0.04 * TH)
        return k, -x0 * k, -y0 * k
    if mode == "right":
        if framing == "W":
            return 2 / 3, float(RIGHT_W_DX), 0.0
        k = OW / TW; y0 = max(0.0, top - 0.04 * TH)
        return k, RIGHT_T_HX - cx * k, -y0 * k
    if mode == "corner":
        c = CORNER[framing]; k = c["k"]
        return k, c["hx"] - cx * k, c["hy"] - top * k
    raise ValueError(mode)


def camera(mode, framing, top, cx):
    """The background's camera for camera-locked types: the move from this placement's W mapping to the shot's
    mapping, applied to the W background (identity for W). Returns (s, tx, ty): out = in * s + t."""
    kw, oxw, oyw = affine(mode, "W", top, cx)
    k, ox, oy = affine(mode, framing, top, cx)
    s = k / kw
    return s, ox - oxw * s, oy - oyw * s


def visible(k, ox, oy):
    """Integer plate crop (x, y, w, h) and its screen rect (x, y, w, h) for the part of the plate on screen, plus which
    plate edges lie inside the screen (they get a feather)."""
    sx0, sy0 = max(0.0, ox), max(0.0, oy)
    sx1, sy1 = min(float(OW), ox + PW * k), min(float(OH), oy + PH * k)
    px0 = max(0, int(math.floor((sx0 - ox) / k))); py0 = max(0, int(math.floor((sy0 - oy) / k)))
    px1 = min(PW, int(math.ceil((sx1 - ox) / k))); py1 = min(PH, int(math.ceil((sy1 - oy) / k)))
    px0 -= px0 % 2; py0 -= py0 % 2; px1 += px1 % 2; py1 += py1 % 2          # even crops for the scaler
    px1 = min(PW, px1); py1 = min(PH, py1)
    x = int(round(px0 * k + ox)); y = int(round(py0 * k + oy))
    w = int(round((px1 - px0) * k)); h = int(round((py1 - py0) * k))
    edges = dict(l=ox > 0.5, t=oy > 0.5, r=ox + PW * k < OW - 0.5, b=oy + PH * k < OH - 0.5)
    return (px0, py0, px1 - px0, py1 - py0), (x, y, w, h), edges


class Presenter:
    """Reads one shot of a plate, already cropped and scaled to its screen rect (premultiplied scaling, then
    unpremultiplied here so the grade sees true colour). Frames are plate frames k0, k0+1, ..."""

    def __init__(self, plate, k0, n, k, ox, oy):
        self.crop, self.rect, self.edges = visible(k, ox, oy)
        cx, cy, cw, ch = self.crop; x, y, w, h = self.rect
        self.w, self.h, self.n, self.k = w, h, n, k
        vf = f"crop={cw}:{ch}:{cx}:{cy},premultiply=inplace=1,scale={w}:{h}:flags=area"
        self.p = subprocess.Popen([FF, "-v", "error", "-ss", f"{(k0 - 0.5) / FPS:.6f}", "-i", plate, "-frames:v", str(n),
                                   "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgba64le", "-"], stdout=subprocess.PIPE)
        self.ramp = self._ramp()

    def _ramp(self):
        r = np.ones((self.h, self.w), np.float32); f = FEATHER
        x, y, w, h = self.rect
        if self.edges["l"]: r[:, :f] *= np.linspace(0, 1, f, dtype=np.float32)[None]
        if self.edges["r"]: r[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32)[None]
        if self.edges["t"]: r[:f, :] *= np.linspace(0, 1, f, dtype=np.float32)[:, None]
        if self.edges["b"]: r[-f:, :] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]
        return r

    def read(self):
        nb = self.w * self.h * 8
        raw = self.p.stdout.read(nb)
        assert len(raw) == nb, "plate ended early"
        a = np.frombuffer(raw, "<u2").reshape(self.h, self.w, 4).astype(np.float32) * (1 / 65535)
        A = a[..., 3]
        F = a[..., :3] / np.maximum(A, 1e-4)[..., None]
        F[A < 2e-3] = 0
        return np.clip(F, 0, 1), A * self.ramp

    def close(self):
        self.p.stdout.close(); self.p.wait()


# ------------------------------------------------------------------ grade and compose (house key standard)
def grade(x, mode="warm"):
    """The locked DS-40 grade (comp16.grade, verbatim maths), applied once to the presenter only."""
    if mode == "rich": gains = [1.015, 1, 1.01]; sat = 1.12; exposure = 1.03; con = 1.07
    elif mode == "natural": gains = [.985, 1, 1.035]; sat = .94; exposure = 1.035; con = 1.035
    elif mode == "warm": gains = [1.01, 1, 1.015]; sat = 1.04; exposure = 1.035; con = 1.045
    else: gains = [.985, 1.005, 1.035]; sat = .98; exposure = 1.075; con = 1.055
    x = x * np.array(gains, np.float32); y = np.sum(x * np.array([.2126, .7152, .0722], np.float32), -1, keepdims=True)
    x = y + sat * (x - y); x = np.maximum(x, 0) ** .97 * exposure; x = (x - .18) * con + .18
    return np.clip(x, 0, 1)


WRAP = 0.12; WRAP_SIG_PLATE = 11.0                     # the approved light wrap (house key stage 2), in plate px


def compose(bg, F, A, rect, k, mode="warm", light=None):
    """Lay the graded presenter over bg (in place, returns bg). light(G, A, region) may adjust his light to the set."""
    x, y, w, h = rect
    X0, Y0, X1, Y1 = max(0, x), max(0, y), min(OW, x + w), min(OH, y + h)
    if X1 <= X0 or Y1 <= Y0: return bg
    F = F[Y0 - y:Y1 - y, X0 - x:X1 - x]; A = A[Y0 - y:Y1 - y, X0 - x:X1 - x]
    reg = bg[Y0:Y1, X0:X1]
    G = grade(F, mode)
    if light is not None: G = light(G, A, reg)
    aa = A[..., None]
    out = G * aa + reg * (1 - aa)
    sig = max(1.5, WRAP_SIG_PLATE * k)
    inv = (1 - A).astype(np.float32)
    bb = cv2.GaussianBlur(np.ascontiguousarray(reg * inv[..., None]), (0, 0), sig)
    cover = cv2.GaussianBlur(inv, (0, 0), sig)[..., None]
    wm = WRAP * cover * aa
    out = out * (1 - wm) + bb / np.maximum(cover, 1e-3) * wm
    bg[Y0:Y1, X0:X1] = np.clip(out, 0, 1)
    return bg


# ------------------------------------------------------------------ shared pieces
@functools.lru_cache(4)
def _field_base():
    return None


def field(t):
    """The moving Soft Blue Light field (softblue.field), float32."""
    return np.asarray(SB.field(t, OW, OH), np.float32) * (1 / 255)


def warp(img, cam, size=(OW, OH)):
    """Apply a camera (s, tx, ty) to an output-space image (zoom in for a tight cut)."""
    s, tx, ty = cam
    if abs(s - 1) < 1e-6 and abs(tx) < 0.01 and abs(ty) < 0.01: return img
    M = np.float32([[s, 0, tx], [0, s, ty]])
    return cv2.warpAffine(img, M, size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def tint(img, amount, color=(5 / 255, 13 / 255, 28 / 255)):
    return img * (1 - amount) + np.array(color, np.float32) * amount


def radial(w=OW, h=OH, cx=0.5, cy=0.45, rx=0.55, ry=0.75):
    y, x = np.mgrid[:h, :w].astype(np.float32); x /= w; y /= h
    return np.clip(np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2), 0, 1.5)


@functools.lru_cache(64)
def facebox(path):
    """Largest Vision face box (x0, y0, x1, y1) in a photo, or None (hyperframes/facebox.swift)."""
    if not FACEBOX.exists():
        subprocess.run(["swiftc", "-O", str(HERE.parent / "hyperframes/facebox.swift"), "-o", str(FACEBOX)], check=True)
    r = subprocess.run([str(FACEBOX), str(path)], capture_output=True, text=True).stdout.strip().split("\t")
    if len(r) < 2 or r[1] in ("none", "error"): return None
    return tuple(int(v) for v in r[1].split())


@functools.lru_cache(64)
def load_photo(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def person_crop(path, aspect, k=5.0, top=0.6, box=None):
    """Crop a photo of a person to `aspect` (w/h): about k face heights tall, the face `top` face heights below the
    crop top, centred on the face across (or an explicit box). Returns a PIL image."""
    im = load_photo(str(path)); iw, ih = im.size
    if box: return im.crop(tuple(box))
    fb = facebox(str(path))
    if fb is None:
        h = min(ih, iw / aspect); w = h * aspect
        return im.crop((round((iw - w) / 2), 0, round((iw + w) / 2), round(h)))
    fx0, fy0, fx1, fy1 = fb; fh = fy1 - fy0; cx = (fx0 + fx1) / 2
    h = min(ih, k * fh, iw / aspect); w = h * aspect
    y0 = max(0, min(ih - h, fy0 - top * fh)); x0 = max(0, min(iw - w, cx - w / 2))
    return im.crop((round(x0), round(y0), round(x0 + w), round(y0 + h)))


def to_f32(im):
    return np.asarray(im, np.float32) * (1 / 255)


class ClipSource:
    """Muted footage from a clip: plays `windows` [(a, b), ...] (clip seconds) one after another at 29.97 fps, cover-
    scaled to `size`, starting again from the first window if the segment outlasts them. A cut between windows is the
    clip's own kind of edit, so it reads naturally."""

    def __init__(self, path, windows, size=(OW, OH), zoom=1.0, focus=(0.5, 0.45), out_focus=None):
        self.path, self.windows, self.size = str(path), [tuple(w) for w in windows], size
        self.zoom, self.focus, self.out_focus = zoom, focus, out_focus
        self.wi, self.p, self.left, self.last = -1, None, 0, None

    def _vf(self):
        W, H = self.size; z = self.zoom
        if z <= 1.0001 and self.out_focus is None:
            return f"fps=30000/1001,scale={W}:{H}:force_original_aspect_ratio=increase:flags=bicubic,crop={W}:{H}"
        # zoomed: scale up by z, then crop a W x H window placing the clip's focus point at out_focus on screen
        fx, fy = self.focus; ox, oy = self.out_focus or (0.5, 0.5)
        sw, sh = int(round(W * z / 2)) * 2, int(round(H * z / 2)) * 2
        cx = int(np.clip(fx * sw - ox * W, 0, sw - W)); cy = int(np.clip(fy * sh - oy * H, 0, sh - H))
        return f"fps=30000/1001,scale={sw}:{sh}:force_original_aspect_ratio=increase:flags=bicubic,crop={W}:{H}:{cx}:{cy}"

    def _next(self):
        if self.p: self.p.stdout.close(); self.p.wait()
        self.wi = (self.wi + 1) % len(self.windows)
        a, b = self.windows[self.wi]
        self.left = int(round((b - a) * FPS))
        self.p = subprocess.Popen([FF, "-v", "error", "-ss", f"{a:.3f}", "-i", self.path, "-t", f"{b - a + 0.2:.3f}", "-an",
                                   "-vf", self._vf(), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)

    def read(self):
        W, H = self.size
        if self.left <= 0: self._next()
        raw = self.p.stdout.read(W * H * 3)
        if len(raw) < W * H * 3:                          # window ended a frame early: move on
            self.left = 0; self._next(); raw = self.p.stdout.read(W * H * 3)
        self.left -= 1
        self.last = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32) * (1 / 255)
        return self.last

    def close(self):
        if self.p: self.p.stdout.close(); self.p.wait()


class MovFrames:
    """Sequential frames of a rendered background movie (HyperFrames renders are UNTAGGED BT.601 limited range)."""

    def __init__(self, path, bt601=True):
        vf = "scale=in_color_matrix=bt601:in_range=tv:out_range=pc,format=rgb24" if bt601 else "format=rgb24"
        self.p = subprocess.Popen([FF, "-v", "error", "-i", str(path), "-an", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        self.last = None

    def read(self):
        raw = self.p.stdout.read(OW * OH * 3)
        if len(raw) == OW * OH * 3:
            self.last = np.frombuffer(raw, np.uint8).reshape(OH, OW, 3).astype(np.float32) * (1 / 255)
        assert self.last is not None, "background render is empty"
        return self.last

    def close(self):
        self.p.stdout.close(); self.p.wait()


# ------------------------------------------------------------------ the types
class Background:
    placement = "center"
    light = None

    def __init__(self, seg, ctx):
        self.seg, self.ctx = seg, ctx

    def frame(self, i, cam):
        raise NotImplementedError

    def close(self):
        pass


class Plain(Background):
    """The moving Soft Blue field alone (a fallback, not one of Dan's types)."""

    def frame(self, i, cam):
        return warp(field(self.seg.get("t_field", 0) + i / FPS), cam)


class Soft(Background):
    """1: their clip (muted) or a photo behind Dan, softened: blurred, darkened and navy-tinted, so he reads first."""

    def __init__(self, seg, ctx):
        super().__init__(seg, ctx)
        self.small = (480, 270)
        c = seg.get("clip")
        self.src = ClipSource(ctx.path(c["src"]), c["windows"], self.small) if c else None
        if not self.src:
            im = person_crop(ctx.path(seg["photos"][0]), 16 / 9, k=seg.get("k", 7.0), top=1.2)
            self.photo = to_f32(im.resize((960, 540), Image.Resampling.LANCZOS))
        self.vig = radial(*self.small, cx=0.5, cy=0.42, rx=0.7, ry=0.9)

    def frame(self, i, cam):
        if self.src:
            img = self.src.read()
        else:                                            # slow push on the photo for its whole time on screen
            z = 1.0 + 0.06 * i / max(1, self.seg["frames"])
            img = warp(cv2.resize(self.photo, self.small, interpolation=cv2.INTER_AREA), (z, (1 - z) * 240, (1 - z) * 120), self.small)
        img = cv2.GaussianBlur(img, (0, 0), 3.2)
        img = img * 0.50
        img = tint(img, 0.32)
        img = img * (1 - 0.35 * np.clip(self.vig - 0.45, 0, 1)[..., None])
        big = cv2.resize(img, (OW, OH), interpolation=cv2.INTER_LINEAR)
        big = np.clip(big + (np.random.default_rng(i).random((OH, OW, 1), np.float32) - .5) / 255 * 1.5, 0, 1)
        return warp(big, cam)

    def close(self):
        if self.src: self.src.close()


class ClipFull(Background):
    """2 corner / 2b side: their clip full screen (muted, it keeps rolling after it played with sound), Dan talking
    in the corner or full size to one side. A soft shade behind him keeps his edges readable."""

    def __init__(self, seg, ctx):
        super().__init__(seg, ctx)
        c = seg["clip"]; self.side = seg["type"] == "side"
        self.placement = "right" if self.side else "corner"
        self.src = ClipSource(ctx.path(c["src"]), c["windows"], (OW, OH), zoom=c.get("zoom", 1.0),
                              focus=tuple(c.get("focus", (0.5, 0.45))), out_focus=tuple(c["out_focus"]) if c.get("out_focus") else None)
        y, x = np.mgrid[:OH, :OW].astype(np.float32); x /= OW; y /= OH
        if self.side:      # behind Dan (right) a little darker and softer, so he and the person both read
            g = np.clip((x - 0.45) / 0.35, 0, 1)
            self.shade = (1 - 0.38 * g)[..., None] * 0.92
        else:              # a soft pool of shade in the lower right where Dan stands
            d = np.sqrt(((x - 0.80) / 0.32) ** 2 + ((y - 0.80) / 0.45) ** 2)
            self.shade = (1 - 0.30 * np.clip(1.15 - d, 0, 1))[..., None]

    def frame(self, i, cam):
        img = self.src.read()
        if self.side: img = cv2.GaussianBlur(img, (0, 0), 1.6)
        return img * self.shade

    def close(self):
        self.src.close()


class Wall(Background):
    """3: a wall of photos scrolling slowly behind Dan, alternate columns up and down, darkened a little."""

    def __init__(self, seg, ctx):
        super().__init__(seg, ctx)
        cols = seg.get("cols", 6); gap = 12
        self.tw = (OW - (cols - 1) * gap) // cols; self.th = int(round(self.tw * 4 / 3)); self.gap = gap; self.cols = cols
        photos = [ctx.path(p) for p in seg["photos"]]
        tiles = [to_f32(person_crop(p, 3 / 4, k=seg.get("k", 5.5), top=0.7).resize((self.tw, self.th), Image.Resampling.LANCZOS)) for p in photos]
        self.speed = seg.get("speed", 26.0)          # px per second
        travel = self.speed * seg.get("frames", 600) / FPS
        rows = int(math.ceil((OH + travel) / (self.th + gap))) + 1   # only the tiles that come on screen during the segment
        # deal the photos column by column so each tile is unique while the pool lasts; a repeat lands in a far column,
        # scrolling the other way, at another height (RO-24 R3 review: two copies of one photo on screen at once)
        order = [(r, c) for r in range(rows) for c in (0, 3, 1, 4, 2, 5)[:cols] if c < cols]
        deal = {rc: tiles[i % len(tiles)] for i, rc in enumerate(order)}
        self.strips = []
        for c in range(cols):
            strip = np.zeros((rows * (self.th + gap), self.tw, 3), np.float32) + np.array(SB.BASE, np.float32) / 255
            for r in range(rows): strip[r * (self.th + gap): r * (self.th + gap) + self.th] = deal[(r, c)]
            self.strips.append(strip)
        self.period = rows * (self.th + gap)
        self.unique = len(tiles) >= rows * cols
        self.vig = radial(cx=0.5, cy=0.45, rx=0.38, ry=0.75)[..., None]

    def frame(self, i, cam):
        t = i / FPS; out = np.zeros((OH, OW, 3), np.float32) + np.array(SB.BASE, np.float32) / 255
        span = self.period - OH - 1
        for c, strip in enumerate(self.strips):
            st = (c * 97) % max(1, span - int(self.speed * self.seg.get("frames", 600) / FPS)) if span > 0 else 0
            d = min(span, st + self.speed * t)
            off = d if c % 2 == 0 else span - d                # alternate columns scroll the other way, no wrap
            o = int(off); fr = off - o
            a = strip[o:o + OH + 1]
            col = a[:-1] * (1 - fr) + a[1:] * fr               # sub-pixel scroll: smooth at 26 px/s
            x = c * (self.tw + self.gap); out[:, x:x + self.tw] = col[:OH]
        out = tint(out * 0.74, 0.16)
        out = out * (1 - 0.30 * np.clip(1 - self.vig, 0, 1))  # a little darker right behind Dan
        return out


class Cards(Background):
    """6: tilted photo cards with white borders, drifting slowly on the moving Soft Blue field, around Dan."""

    SLOTS = [  # centre x, centre y, width, angle (deg): two each side, two high behind his shoulders
        (300, 330, 380, -7), (330, 800, 400, 5), (1625, 320, 380, 6), (1590, 790, 400, -5),
        (650, 175, 300, 4), (1270, 185, 300, -4)]

    def __init__(self, seg, ctx):
        super().__init__(seg, ctx)
        self.cards = []
        rng = np.random.default_rng(seg.get("seed", 3))
        for n, p in enumerate(seg["photos"][:len(self.SLOTS)]):
            cx, cy, w, ang = self.SLOTS[n]
            im = person_crop(ctx.path(p), 4 / 5, k=seg.get("k", 5.5), top=0.7)
            h = int(round(w * 5 / 4)); b = max(8, w // 34)
            im = im.resize((w, h), Image.Resampling.LANCZOS)
            card = Image.new("RGBA", (w + 2 * b, h + 2 * b), (246, 247, 250, 255)); card.paste(im, (b, b))
            pad = 60; big = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
            sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((pad + 8, pad + 14, pad + card.width + 8, pad + card.height + 14), fill=(0, 3, 12, 150))
            sh = sh.filter(ImageFilter.GaussianBlur(16)); big.alpha_composite(sh); big.alpha_composite(card, (pad, pad))
            arr = np.asarray(big, np.float32) * (1 / 255)
            self.cards.append(dict(img=arr, cx=cx, cy=cy, ang=ang, ph=rng.random() * 6.28, per=rng.uniform(9, 14),
                                   amp=rng.uniform(10, 18), rot=rng.uniform(0.6, 1.4), dx=rng.uniform(-14, 14)))

    def frame(self, i, cam):
        t = i / FPS; out = field(self.seg.get("t_field", 0) + t)
        for c in self.cards:
            ph = c["ph"] + 2 * math.pi * t / c["per"]
            cx = c["cx"] + c["dx"] * t / 10 + 0.6 * c["amp"] * math.cos(ph); cy = c["cy"] + c["amp"] * math.sin(ph)
            ang = c["ang"] + c["rot"] * math.sin(ph * 0.8)
            settle = 1.0 + 0.03 * max(0.0, 1 - t / 0.6) ** 2        # cards settle in over the first 0.6 s
            img = c["img"]; h, w = img.shape[:2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, settle)
            M[0, 2] += cx - w / 2; M[1, 2] += cy - h / 2
            lay = cv2.warpAffine(img, M, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
            a = lay[..., 3:4]; out = out * (1 - a) + lay[..., :3] * a
        return out


class Set(Background):
    """8: the studio set (one Codex plate for the whole film), its TV playing their clip (muted) or a photo pair.
    Light match: Dan a touch dimmer, warmer at the edges, a soft shadow on the set around him; shallow depth of field
    on the set."""
    placement = "right"

    def __init__(self, seg, ctx):
        super().__init__(seg, ctx)
        st = ctx.set_plate()
        self.plate, self.tv = st["img"], st["tv"]          # output-space plate (float32 1920x1080) and TV rect
        x, y, w, h = self.tv
        c = seg.get("clip")
        self.src = ClipSource(ctx.path(c["src"]), c["windows"], (w, h)) if c else None
        if not self.src:
            self.tvimg = pair_image(ctx, seg["photos"][:2], (w, h))
        yy, xx = np.mgrid[:h, :w].astype(np.float32)
        self.glare = (0.06 * np.clip(1 - np.abs((xx / w - 0.25) - (yy / h) * 0.5) * 4, 0, 1))[..., None]
        self.chip = None
        if seg.get("ai_label", True):                    # every AI image carries AI-GENERATED (00-RULES); top left, clear of Dan
            im = Image.new("RGBA", (OW, OH), (0, 0, 0, 0)); SB.disclosure(im, "AI-GENERATED", xy=(56, 48))
            a = np.asarray(im, np.float32) * (1 / 255); self.chip = (a[..., :3], a[..., 3:4])

    def frame(self, i, cam):
        out = self.plate.copy(); x, y, w, h = self.tv
        tvc = self.src.read() if self.src else self.tvimg
        tvc = np.clip(tvc * 0.86 + self.glare, 0, 1)
        out[y:y + h, x:x + w] = tvc
        out = cv2.GaussianBlur(out, (0, 0), 1.3)            # depth of field: the set sits behind him
        out = warp(out, cam)
        if self.chip is not None: out = out * (1 - self.chip[1]) + self.chip[0] * self.chip[1]
        return out

    @staticmethod
    def light(G, A, reg):
        """Dan in the set's light (dark room, blue practicals left, warm lamp right): 12 % dimmer and a touch cooler, a blue
        rim on the edges facing left and a warm rim on the edges facing right."""
        h, w = A.shape
        edge = np.clip(A - cv2.GaussianBlur(A, (0, 0), 4), 0, 1) * 2.4
        gx = cv2.Sobel(cv2.GaussianBlur(A, (0, 0), 3), cv2.CV_32F, 1, 0, ksize=5)
        left = np.clip(gx, 0, None); right = np.clip(-gx, 0, None); tot = left + right + 1e-6
        G = G * 0.88 * np.array([0.98, 1.0, 1.03], np.float32)
        blue, warm = np.array([0.80, 0.95, 1.30], np.float32), np.array([1.12, 1.0, 0.84], np.float32)
        rim = (left / tot)[..., None] * blue + (right / tot)[..., None] * warm
        e = (0.35 * edge)[..., None]
        return np.clip(G * (1 - e) + G * rim * e, 0, 1)

    def close(self):
        if self.src: self.src.close()


class HFLayer(Background):
    """4 panel / 7 bigtype: a HyperFrames render of the whole background (field + the graphic), read frame by frame."""

    def __init__(self, seg, ctx):
        super().__init__(seg, ctx)
        self.m = MovFrames(ctx.path(seg["mov"]))

    def frame(self, i, cam):
        return self.m.read()

    def close(self):
        self.m.close()


def pair_image(ctx, photos, size, gap=None):
    """A before/after pair laid side by side to fill `size` (for the set's TV)."""
    W, H = size; gap = gap if gap is not None else max(4, W // 60)
    pw = (W - gap) // 2
    out = np.zeros((H, W, 3), np.float32) + np.array([8, 14, 24], np.float32) / 255
    for n, p in enumerate(photos):
        im = person_crop(ctx.path(p), pw / H, k=6.0, top=0.6).resize((pw, H), Image.Resampling.LANCZOS)
        out[:, n * (pw + gap): n * (pw + gap) + pw] = to_f32(im)
    return out


TYPES = {"soft": Soft, "corner": ClipFull, "side": ClipFull, "wall": Wall, "cards": Cards, "set": Set,
         "panel": HFLayer, "bigtype": HFLayer, "plain": Plain}


def make_background(seg, ctx):
    bg = TYPES[seg["type"]](seg, ctx)
    bg.placement = seg.get("placement", PLACEMENT[seg["type"]])
    return bg


class Context:
    """Paths and the film's studio-set plate. root: the film's work folder (relative paths in a plan resolve here)."""

    def __init__(self, root, set_plate=None, set_tv=None):
        self.root = pathlib.Path(root); self.set_path = set_plate; self.set_tv = set_tv; self._set = None

    def path(self, p):
        p = pathlib.Path(p)
        return str(p if p.is_absolute() else self.root / p)

    def set_plate(self):
        """The set plate cover-scaled to 1920x1080 and the TV screen's rect in output space. set_tv: the screen's
        (x, y, w, h) in the plate's own pixels (measure it once: the largest near-black rectangle)."""
        if self._set is None:
            im = load_photo(self.path(self.set_path)); iw, ih = im.size
            s = max(OW / iw, OH / ih)
            big = im.resize((int(round(iw * s)), int(round(ih * s))), Image.Resampling.LANCZOS)
            ox, oy = (big.width - OW) // 2, (big.height - OH) // 2
            img = to_f32(big.crop((ox, oy, ox + OW, oy + OH)))
            x, y, w, h = self.set_tv
            tv = (int(round(x * s - ox)) + 2, int(round(y * s - oy)) + 2, int(round(w * s)) - 4, int(round(h * s)) - 4)
            self._set = dict(img=img, tv=tv)
        return self._set
