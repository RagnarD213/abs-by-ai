#!/usr/bin/env python3
"""RA-05 round 3: the body scan (A0044, the /start VSL version A) rebuilt VERTICAL (Dan, 2026-10-14: "reproduce this in a vertical
format so that his body occupies the full vertical frame. You can put the notes maybe on the top or the bottom").

  picture  a fixed full-height 608 x 1080 window of SCAN-readable.mp4 at x 653 (land-then-hold, no pan), Lanczos to 1080 x 1920 + a
           light unsharp (Real-ESRGAN is not installed; RA-07 round 2 precedent)
  stubs    the clip's own leader lines run from its four glowing dots to boxes that sit outside the window. The dots stay; the line
           pixels are found per frame inside a band around each measured path and painted out (OpenCV Telea), so nothing dangles
  notes    the same four texts as Soft Blue glass callouts, two at the top (beside his head) and two at the bottom (over the shorts,
           ending above the caption band at 1385), each with a thin cyan line to its dot; each lands on a spoken word
usage: s06_scan3.py            -> cards_9x16/scan.mp4 (exactly the timeline's frames)
       s06_scan3.py still T    -> scan3/still_<T>.png at film time T (seconds into the card)"""
import json, math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH)
import softblue as SB
FF = SB.FF; FPSS = "30000/1001"; W, H = 1080, 1920
SRC = "/Volumes/Extreme/_edit_work/wv01-edit/round4/motion/SCAN-readable.mp4"
SRC_SHA = "68ef87d8c63ac0b6c1a357ec5f6748bb2e2d231f4403896abeec559fc2f4ba31"
X0, WW, T0 = 653, 608, 40 * 1001 / 30000                   # window; source frame 40: the clip's own lines and their glow have finished growing (re-review, round 3)
K = W / WW                                    # 1.7763
B = json.load(open("beats.json")); card = next(c for c in B["cards"] if c["name"] == "scan")
N = card["frames"]; A0 = card["beat"][0]
WD = json.load(open("words_aligned.json"))["words"]
def word(w, after):
    return next(x["t"] for x in WD if x["t"] >= after and x["w"].strip(" ,.").lower() == w)
# reference geometry in WINDOW pixels, measured on the 2.0 s frame (scan3/core_mask.png): dot centre, then the stub path to the edge
STUBS = {"head":     [(367, 112), (515, 157), (608, 157)],
         "shoulder": [(147, 333), (38, 267), (0, 267)],
         "abs":      [(245, 593), (75, 553), (0, 550)],
         "waist":    [(395, 573), (608, 545)]}
# callouts: dot, text, box (OUTPUT px; y of None = sized to the text and pinned by the other edge), start (card s).
# abs + waist: their stubs cross his arms, so they are KEPT and the new line is drawn exactly over them, then turns down to the
# bottom card at TURN (window x); only the bit past the turn is painted out. head + shoulder: over plain background, painted out
# kept up to the card edge too. Only the parts hidden under the cards are painted. All four land in the first 0.6 s, with the
# source's own line growth (0 to 0.3 s), so no line ends in the air for more than a few frames.
NOTES = [
 ("abs",      "Deploy Fasting for More Fat Loss",              (20, None, 520, 1352),  0.10),
 ("waist",    "Train Transverse Abdominis to Tighten Waist",   (560, None, 1062, 1352), 0.20),
 ("shoulder", "Add Deltoid Volume to Make Waist Look Smaller", (20, None, 372, 486),   0.00),
 ("head",     "Deploy Sleep Coaching for Better Recovery",     (704, 150, 1044, None), 0.05),
]
TURN = {"abs": 28, "waist": 582, "head": 396, "shoulder": 49}   # window x where each kept line ends (head, shoulder: the card edge)
DOWN = {"abs", "waist"}                                          # these turn straight down to their card
PAINT_WHOLE = set()
PX = int(os.environ.get("NOTE_PX", "36"))
CHIP_XY = tuple(json.loads(os.environ.get("CHIP_XY", "[20, 160]")))
LINE_IN, BOX_IN = 0.30, 0.28
TH = int(os.environ.get('STUB_TH', '9'))                 # the line draws from the dot, then the card fades and settles in

def frames():
    import hashlib
    assert hashlib.sha256(open(SRC, "rb").read()).hexdigest() == SRC_SHA, "A0044 changed"
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-ss", f"{T0 - 0.5/29.97:.4f}", "-i", SRC, "-vf",
                          f"crop={WW}:1080:{X0}:0,scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709,format=rgb24",
                          "-frames:v", str(N), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    for g in range(N):
        b = p.stdout.read(WW * 1080 * 3); assert len(b) == WW * 1080 * 3, g
        yield np.frombuffer(b, np.uint8).reshape(1080, WW, 3).copy()
    p.stdout.close(); p.wait()

RING = np.zeros((31, 31), np.float32); cv2.circle(RING, (15, 15), 11, 1, 3)
def core(a):
    a = a.astype(int)
    return ((a[..., 2] > 150) & (a[..., 1] > 110) & ((a[..., 2] - a[..., 0]) > 20))

def track(cm, ref):
    x, y = ref; sub = cm[y-30:y+31, x-30:x+31].astype(np.float32)
    r = cv2.matchTemplate(sub, RING, cv2.TM_CCORR_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
    dx, dy = ml[0] - 15, ml[1] - 15
    return (x + dx, y + dy, mv) if (mv > 0.45 and abs(dx) <= 8 and abs(dy) <= 8) else (x, y, mv)

PATHS = {}
if os.path.exists("scan3/stub_paths.json"):           # traced from the stubs' own pixels (scan3/fit_paths.py), smoothed
    for k, pts in json.load(open("scan3/stub_paths.json")).items():
        xs = np.array([p[0] for p in pts], float); ys = np.array([p[1] for p in pts], float)
        # straight segments between the measured bends (the old lines are straight; a median trace jogged where it crossed the
        # forearm outline, final check note N2): least squares per segment of the reference polyline
        ref = STUBS[k]; fy = ys.copy()
        for (xa, _), (xb, _) in zip(ref[:-1], ref[1:]):
            lo, hi = min(xa, xb), max(xa, xb); sel = (xs >= lo) & (xs <= hi)
            if sel.sum() >= 5:
                a_, b_ = np.polyfit(xs[sel], ys[sel], 1); fy[sel] = a_ * xs[sel] + b_
        PATHS[k] = (xs, fy)
BAND, KEEP_R = int(os.environ.get("STUB_BAND", "25")), int(os.environ.get("KEEP_R", "13"))
SHIFT = int(os.environ.get("SHIFT", "18"))

def paint(a, dots):
    """Remove the stub pixels (line + glow) inside a narrow band along each traced path; keep a disc around each dot."""
    cm = core(a); band = np.zeros(cm.shape, np.uint8); keep = np.zeros(cm.shape, np.uint8)
    for k in STUBS:
        d = dots[k]; r0 = STUBS[k][0]; xs, ys = PATHS[k]
        ex = xs[-1] if abs(xs[-1] - r0[0]) > abs(xs[0] - r0[0]) else xs[0]       # the edge end
        w = np.clip(np.abs(xs - ex) / max(1.0, abs(r0[0] - ex)), 0, 1)        # 1 at the dot, 0 at the edge
        pts = np.stack([xs + w * (d[0] - r0[0]), ys + w * (d[1] - r0[1])], 1)
        if k not in PAINT_WHOLE:                                   # only the part past the turn, toward the frame edge
            tx = TURN[k]; pts = pts[(pts[:, 0] <= tx + 3) if ex < r0[0] else (pts[:, 0] >= tx - 3)]   # from just inside the turn: the new line covers the overlap
        if len(pts) > 1: cv2.polylines(band, [np.int32(np.round(pts))], False, 1, BAND)
        cv2.circle(keep, (int(d[0]), int(d[1])), KEEP_R, 1, -1)
    bl = a[..., 2]; th = cv2.subtract(bl, cv2.morphologyEx(bl, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))))
    m = ((band > 0) & (keep == 0)).astype(np.uint8)          # the WHOLE band: a thresholded mask leaves ragged glow edges
    # Fill by copying texture from SHIFT px above and below (the arms and the scanner pillars run vertically, so a vertical
    # copy keeps their edges and skin grain); Telea only where both copies are themselves masked. Feathered 2 px.
    # every painted part now lies on plain background (the kept lines cover everything over his arms): a smooth inpaint, no copy
    fill = cv2.inpaint(a, m * 255, 7, cv2.INPAINT_TELEA).astype(np.float32)
    al = cv2.GaussianBlur(m.astype(np.float32), (5, 5), 1.0); al = np.maximum(al, m.astype(np.float32))[..., None]
    out = a * (1 - al) + fill * al
    return np.clip(out + 0.5, 0, 255).astype(np.uint8), m

def upscale(a):
    im = Image.fromarray(a).resize((W, H), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2.0, percent=55, threshold=2))

F = SB.font(PX)
def box_of(txt, box):
    x0, y0, x1, y1 = box; lines = SB.wrap(txt, F, x1 - x0 - 56); lh = round(PX * 1.22)
    pair = [n for n in NOTES if (n[2][3] == y1 if y0 is None else n[2][1] == y0)]     # cards in the same row share a height
    h = max(len(SB.wrap(n[1], F, n[2][2] - n[2][0] - 56)) for n in pair) * lh + 44
    if y0 is None: y0 = y1 - h
    if y1 is None: y1 = y0 + h
    return (x0, y0, x1, y1), lines, lh

def leader(key, dot, box):
    """The new line in OUTPUT px: [dot, ..., point on the card edge]."""
    dx, dy = dot[0] * K, dot[1] * K; x0, y0, x1, y1 = box
    if key in TURN:                                    # follow the kept stub to its turn (abs, waist: then down to the card top)
        xs, ys = PATHS[key]; r0 = STUBS[key][0]; tx = TURN[key]
        sel = (xs <= r0[0]) & (xs >= tx) if tx < r0[0] else (xs >= r0[0]) & (xs <= tx)
        px, py = xs[sel], ys[sel]; o = np.argsort(np.abs(px - r0[0])); px, py = px[o], py[o]
        w = np.clip(1 - np.abs(px - r0[0]) / abs(tx - r0[0]), 0, 1)
        pts = [((x + w_ * (dot[0] - r0[0])) * K, (y + w_ * (dot[1] - r0[1])) * K) for x, y, w_ in zip(px, py, w)]
        pts = [(dx, dy)] + pts[::4] + [pts[-1]]
        return pts + [(pts[-1][0], y0)] if key in DOWN else pts
    # head + shoulder: leave the dot in the old line's own direction (it covers the old line's last stub at the ring) and run
    # straight on until the line meets the card's edge
    xs, ys = PATHS[key]; r0 = STUBS[key][0]
    far = 40 if key == "head" else 60                  # window px along the old path that set the direction
    i = int(np.argmin(np.abs(xs - (r0[0] + (far if key == "head" else -far)))))
    ux, uy = (xs[i] - r0[0]) * K, (ys[i] - r0[1]) * K; n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
    tt = [((x0 - dx) / ux) if ux > 0 else ((x1 - dx) / ux)]
    if key == "shoulder": tt = [(y1 - dy) / uy]
    t_ = min(v for v in tt if v > 0); return [(dx, dy), (dx + ux * t_, dy + uy * t_)]

def partial(pts, q):
    seg = [math.dist(a, b) for a, b in zip(pts[:-1], pts[1:])]; L = sum(seg) * q; out = [pts[0]]
    for (a, b), s_ in zip(zip(pts[:-1], pts[1:]), seg):
        if L <= 0: break
        f = min(1.0, L / s_) if s_ else 1.0; out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)); L -= s_
    return out

def note_layer(im, t, dots):
    """Draw the four callouts onto the 1080x1920 RGB frame at card time t (s)."""
    glow = Image.new("RGBA", im.size); gd = ImageDraw.Draw(glow); sharp = Image.new("RGBA", im.size); sd = ImageDraw.Draw(sharp)
    cards = []
    for key, txt, box, ta in NOTES:
        bx, lines, lh = box_of(txt, box)
        pts = leader(key, dots[key], bx)
        seg = pts                      # the clip's own lines exist from frame 0, so the new ones do too (nothing points at nothing)
        if len(seg) > 1:
            gd.line(seg, fill=SB.LT_CYAN + (110,), width=12, joint="curve"); sd.line(seg, fill=SB.LT_CYAN + (255,), width=5, joint="curve")
        qb = SB.ease(t + 0.06, BOX_IN) # all four cards fade in together, already half up on frame 0, with their lines (final check N1)
        if qb > 0: cards.append((bx, lines, lh, qb, t))
    im = Image.alpha_composite(im.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(5)))
    im = Image.alpha_composite(im, sharp).convert("RGB")
    for (x0, y0, x1, y1), lines, lh, qb, tt in cards:
        lay = im.copy(); SB.glass(lay, (x0, y0, x1, y1), tt)
        ov = Image.new("RGBA", im.size); od = ImageDraw.Draw(ov)
        od.rounded_rectangle((x0, y0, x1, y1), 20, fill=SB.LT_FILL, outline=SB.LT_EDGE, width=3)
        ty = y0 + (y1 - y0 - lh * len(lines)) / 2 - PX * 0.14
        for j, ln in enumerate(lines):
            od.text((x0 + 28, ty + j * lh), ln, font=F, fill=SB.LT_WHITE)
        lay = Image.alpha_composite(lay.convert("RGBA"), ov).convert("RGB")
        im = Image.blend(im, lay, qb)
    return im

G_CLEAN = 0  # was 16 with the old start; at source frame 40 no clean plate is needed
                                 # card frame by which the clip's own lines have finished growing (measured: by 9)
def zones():
    """window-px mask: each kept line's part past its turn, thick, feathered wide. In the first G_CLEAN frames the
    clip's growing glow passes through here and the narrow paint band left edges and patches (independent review, frames 5 to 9)."""
    z = np.zeros((1080, WW), np.uint8)
    for k in STUBS:
        xs, ys = PATHS[k]; r0 = STUBS[k][0]; tx = TURN[k]
        sel = (xs <= tx) if tx < r0[0] else (xs >= tx)
        pts = np.stack([xs[sel], ys[sel]], 1)
        if len(pts) > 1: cv2.polylines(z, [np.int32(np.round(pts))], False, 1, 41)
    # no disc on the turn point: the plate (no glow) read as a dark disc where the growing glow lights the wall (frames 6-7)
    z = cv2.GaussianBlur(z.astype(np.float32), (31, 31), 8)
    return z[..., None]

def render(only_t=None):
    dots = {k: v[0] for k, v in STUBS.items()}
    FR = list(frames()); Z = zones(); plate = None
    e = None
    if only_t is None:
        e = subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", FPSS,
                              "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                              "-crf", "15", "-pix_fmt", "yuv420p", "-r", FPSS, "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc",
                              "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0", "cards_9x16/scan.mp4"],
                             stdin=subprocess.PIPE)
    # the clean plate: frame G_CLEAN painted, its lines complete (dots fixed at their measured places there)
    cmp_ = core(FR[G_CLEAN]); dp = {k: track(cmp_, STUBS[k][0])[:2] for k in STUBS}
    plate = paint(FR[G_CLEAN], dp)[0].astype(np.float32)
    log = []
    for g, a in enumerate(FR):
        t = g * 1001 / 30000
        if only_t is not None and abs(t - only_t) > 0.5 / 29.97: continue
        cm = core(a)
        for k in dots: x, y, mv = track(cm, dots[k] if g else STUBS[k][0]); dots[k] = (x, y)
        pa, m = paint(a, dots)
        if g < G_CLEAN:
            pa = np.clip(pa * (1 - Z) + plate * Z + 0.5, 0, 255).astype(np.uint8)
        im = upscale(pa); im = note_layer(im, t, dots)
        box = SB.disclosure(im, "AI-GENERATED", CHIP_XY, size=20)
        log.append({"g": g, "dots": {k: list(map(int, v)) for k, v in dots.items()}, "painted_px": int(m.sum()), "plate": g < G_CLEAN})
        if e: e.stdin.write(np.ascontiguousarray(np.asarray(im)).tobytes())
        else:
            im.save(f"scan3/still_{only_t:.2f}.png"); Image.fromarray(pa).save(f"scan3/painted_{only_t:.2f}.png")
            Image.fromarray(a).save(f"scan3/raw_{only_t:.2f}.png")
            print("still", only_t, "chip", box, log[-1]); return
    e.stdin.close(); assert e.wait() == 0
    meta = json.load(open("cards_9x16/meta.json")) if os.path.exists("cards_9x16/meta.json") else {}
    meta["scan"] = {"source": SRC, "sha256": SRC_SHA, "window": [X0, 0, WW, 1080], "src_t0": round(T0, 4), "scale": K, "frames": N,
                    "chip": "AI-GENERATED", "chip_box": [round(v) for v in box],
                    "notes": [{"dot": k, "text": s_, "box": list(box_of(s_, b)[0]), "lands_card_t": ta} for k, s_, b, ta in NOTES]}
    json.dump(meta, open("cards_9x16/meta.json", "w"), indent=1)
    json.dump(log, open("scan3/scan_track.json", "w"))
    print("scan", N, "frames -> cards_9x16/scan.mp4")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "still": render(float(sys.argv[2]))
    else: render()
