"""DS-40 R6: the whole Short in the locked green screen reaction format.

    python3 comp_r6.py OUT.mp4 [--pink] [--range F0 F1] [--noaudio]

  0 .. 580     the Maher clip full screen (R4 version B: fixed vertical crop on Maher, Dan keyed small lower left at 0.40,
               flush left and bottom, laptop visible, his real reaction), clip sound only; G1 name lower third
  581 .. 595   the R3 move adapted to B: the clip (still playing, silent) shrinks into the card at the top, Dan grows from
               0.40 to full size (full-height key of the scripted take, so his footage always ends on the bottom edge),
               3-frame dissolve from the watching take to the scripted take while still small
  596 ..       the R2 layout: moving Soft Blue field, the card at the top playing SILENT footage from other moments of the
               same episode (plan.json "card"), large Dan (crop row 3490, OY 175); G2 key point; G3 the BMI table full
               screen (it covers the two ad-lib cuts); G4 subscribe
  captions     on every frame (cues.json): top 1040 during the clip, 1412 after
--pink: saturated pink instead of the clip, field and card, no graphics, no captions, no audio (key check only).
"""
import sys, os, json, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); R6 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import comp_opening as C
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import softblue as SB
sys.path.insert(0, "/Users/danielrose/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude/Projects/Abs By AI/"
                   ".claude/worktrees/stoic-cartwright-8bfcc9/.claude/skills/_shared/hyperframes")
from composite import Compositor

P = json.load(open(f"{R6}/plan.json"))
W, H, FPS = C.W, C.H, C.FPS
FF = C.FF
N_CLIP, MOVE = P["n_clip"], P["move"]
F_BMI0, F_BMI1, F_END, REM = P["f_bmi0"], P["f_bmi1"], P["f_end"], P["rem"]
PINK = np.array([0.95, 0.25, 0.62], np.float32)
S_B = 0.40
SMALL = f"{R6}/r4fix/cache_full"            # the R4 corner footage, re-finished with the watch hold-out boxes
SMALL_OFF = C.SMALL_OFF                      # cache frame of clip frame 0 (3)
CARD = C.CARD                                # (60, 36, 1020, 576)
ROLLF0 = P["rollf0"]
CACHES = [  # (first scripted j, last j, cache dir, cache index of j=0)
    (0, 14, f"{R6}/cache_S1F", ROLLF0 - 41963),               # full height, for the move (-ss 1400.15 lands on 41963)
    (15, 278, "/Volumes/Expansion/_edit_work/ds40/r2/cache_r2", 0),  # the approved R2 sample
    (279, 690, f"{R6}/cache_S2w", ROLLF0 - 42240),           # w: re-finished with watch hold-out boxes (R6 review)             # -ss 1409.40 lands on 42240
    (1325, 1500, f"{R6}/cache_S3w", ROLLF0 - 43286),           # -ss 1444.30 lands on 43286
]


def large_npy(j):
    for a, b, d, off in CACHES:
        if a <= j <= b: return f"{d}/f{j + off:04d}.npy", d.endswith("S1F")
    raise KeyError(j)


def dan_j(f):
    if f < N_CLIP or F_BMI0 <= f < F_BMI1: return None
    j = f - N_CLIP
    return j + REM if f >= F_BMI1 else j


def decode(path, ss, n, skip=3):
    """n frames from ss at 29.97 as float RGB 1280x720 (BT.709). Seeks `skip` frames early and drops them (a seek's
    first decoded frame repeats the next one)."""
    p = subprocess.Popen([FF, "-v", "error", "-ss", f"{max(0, ss - skip / FPS):.4f}", "-i", path, "-frames:v", str(n + skip),
                          "-vf", "fps=30000/1001,scale=1280:720:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24",
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    k = 0
    while True:
        b = p.stdout.read(1280 * 720 * 3)
        if len(b) < 1280 * 720 * 3: break
        if k >= skip: yield np.frombuffer(b, np.uint8).reshape(720, 1280, 3).astype(np.float32) / 255
        k += 1
    p.wait()


class Card:
    """The settled card: rounded, soft shadow, hairline border; its picture from the clip (move) or the episode shots."""
    def __init__(self):
        x0, y0, x1, y1 = CARD; self.box = CARD; self.w, self.h = x1 - x0, y1 - y0
        self.m = C.rounded_mask(self.w, self.h, 22)
        sh = np.zeros((H, W), np.float32); sh[y0 + 14:y0 + 14 + self.h, x0 + 6:x0 + 6 + self.w] = 0.59
        self.shadow = cv2.GaussianBlur(sh, (0, 0), 18)[..., None]
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((x0, y0, x1 - 1, y1 - 1), 22, outline=(150, 200, 255, 120), width=2)
        self.L = np.asarray(lay).astype(np.float32) / 255
        self.shots = P["card"]; self.gen = None; self.cur = None

    def frame(self, f):
        for i, s in enumerate(self.shots):
            if s["f0"] <= f < s["f1"]:
                if self.cur != i or self.gen is None:
                    self.cur = i; self.gen = decode(P["episode"], s["ep"] + (f - s["f0"]) / FPS, s["f1"] - f)
                return next(self.gen)
        raise KeyError(f)

    def paint(self, out, pic):
        x0, y0, x1, y1 = self.box
        out = out * (1 - self.shadow)
        v = C.clip_view(pic, self.w, self.h)
        out[y0:y1, x0:x1] = v * self.m + out[y0:y1, x0:x1] * (1 - self.m)
        return out * (1 - self.L[..., 3:]) + self.L[..., :3] * self.L[..., 3:]


ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def cap_rgba(lines, top, size=86):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(ARIAL, size); y = top
    for s in lines:
        w = d.textlength(s, font=f); x = (W - w) / 2
        d.text((x + 3, y + 3), s, font=f, fill=(0, 0, 0, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255))
        d.text((x, y), s, font=f, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255)); y += int(size * 1.12)
    a = np.asarray(im).astype(np.float32) / 255
    ys = np.where(a[..., 3].max(1) > 0)[0]
    return a, (int(ys.min()), int(ys.max()) + 1)


def main(out_mp4, pink=False, rng=None, audio=True):
    f0, f1 = rng or (0, F_END)
    cues = json.load(open(f"{R6}/cues.json"))
    caps = [(int(round(c["a"] * FPS)), int(round(c["b"] * FPS)), *cap_rgba(c["lines"], c["top"])) for c in cues]
    comp = Compositor(json.load(open(f"{R6}/gfx/hf/manifest.json")), wh=(W, H)) if not pink else None
    card = Card()
    # the clip, frames 0 .. N_CLIP + MOVE (it keeps playing, silent, while it shrinks)
    clip = decode(C.CLIP, C.CLIP_IN, N_CLIP + MOVE + 2) if f0 < N_CLIP + MOVE else None
    if clip:
        for _ in range(min(f0, N_CLIP + MOVE)): next(clip)
    cmd = [FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30000/1001", "-i", "-"]
    if audio and not pink: cmd += ["-ss", f"{f0 / FPS:.6f}", "-i", f"{R6}/audio/film.wav"]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    if audio and not pink: cmd += ["-c:a", "aac", "-b:a", "256k", "-shortest"]
    cmd += ["-movflags", "+faststart", out_mp4]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    sx0, sy0 = 0, H - int(round(1920 * S_B))
    for f in range(f0, f1):
        t = f / FPS
        if f < N_CLIP:
            fr = next(clip)
            bg = np.ones((H, W, 3), np.float32) * PINK if pink else C.clip_view(fr, W, H)
            G, a = C.dan_layer(f"{SMALL}/f{f + SMALL_OFF:04d}.npy")
            out = C.place(bg, G, a, S_B, sx0, sy0, feather=1.0, fw=C.shrug_fw(f))
        elif f < N_CLIP + MOVE or F_BMI0 > f >= N_CLIP or f >= F_BMI1:
            if F_BMI0 <= f < F_BMI1: raise AssertionError
            field = np.asarray(SB.field(t, W, H).convert("RGB")).astype(np.float32) / 255
            out = np.ones_like(field) * PINK if pink else field
            j = dan_j(f)
            npy, full = large_npy(j)
            G, a = C.dan_layer(npy)
            if f < N_CLIP + MOVE:
                k = f - N_CLIP; u = C.ease((k + 1) / MOVE)
                fr = next(clip)
                if not pink:   # the clip (still playing) shrinks into the card; shadow and corners grow in with the move
                    x0, y0, x1, y1 = CARD
                    bx0, by0 = x0 * u, y0 * u; bx1, by1 = W + (x1 - W) * u, H + (y1 - H) * u
                    bw, bh = int(round(bx1 - bx0)), int(round(by1 - by0))
                    v = C.clip_view(fr, bw, bh)
                    m = C.rounded_mask(bw, bh, 22 * u)
                    sh = np.zeros((H, W), np.float32)
                    sh[int(by0) + int(14 * u):int(by0) + int(14 * u) + bh, int(bx0) + 6:int(bx0) + 6 + bw] = 0.59 * u
                    out = out * (1 - cv2.GaussianBlur(sh, (0, 0), 18)[..., None])
                    X0, Y0 = int(round(bx0)), int(round(by0)); X1, Y1 = min(W, X0 + bw), min(H, Y0 + bh)
                    out[Y0:Y1, X0:X1] = v[:Y1 - Y0, :X1 - X0] * m[:Y1 - Y0, :X1 - X0] + out[Y0:Y1, X0:X1] * (1 - m[:Y1 - Y0, :X1 - X0])
                if k < C.DISSOLVE:   # the watching take dissolves into the scripted take (both full height here)
                    d = (k + 1) / (C.DISSOLVE + 1)
                    G1, a1 = C.dan_layer(f"{SMALL}/f{f + SMALL_OFF:04d}.npy")
                    an = a1 * (1 - d) + a * d
                    G = (G1 * (a1 * (1 - d))[..., None] + G * (a * d)[..., None]) / np.maximum(an, 1e-4)[..., None]; a = an
                s = S_B + (1 - S_B) * u
                y0d = sy0 * (1 - u) + C.OY * u    # top of his footage: B's position -> the layout's OY; bottom never above H
                assert full and y0d + a.shape[0] * s >= H - 0.5
                out = C.place(out, G, a, s, 0, int(round(y0d)), feather=1 - u, fw=C.EDGE)
            else:
                if not pink: out = card.paint(out, card.frame(f))
                out = C.place(out, G, a, 1.0, 0, C.OY)
        else:
            out = np.ones((H, W, 3), np.float32) * PINK if pink else None
        if pink:
            img = (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)
        else:
            img = None if out is None else (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)
            img = comp.apply(img, f)
            imf = img.astype(np.float32) / 255
            for c0, c1, A, (ya, yb) in caps:
                if c0 <= f < c1:
                    al = A[ya:yb, :, 3:]; imf[ya:yb] = imf[ya:yb] * (1 - al) + A[ya:yb, :, :3] * al
            img = (np.clip(imf, 0, 1) * 255 + 0.5).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(img).tobytes())
        if (f + 1) % 120 == 0: print(f + 1, "frames", flush=True)
    enc.stdin.close(); enc.wait()
    assert enc.returncode == 0
    print("wrote", out_mp4, f1 - f0, "frames")


if __name__ == "__main__":
    a = sys.argv
    rng = (int(a[a.index("--range") + 1]), int(a[a.index("--range") + 2])) if "--range" in a else None
    main(a[1], "--pink" in a, rng, "--noaudio" not in a)
