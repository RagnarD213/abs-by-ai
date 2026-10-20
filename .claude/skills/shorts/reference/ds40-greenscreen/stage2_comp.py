"""Stage 2: grade the cached keyed fg, composite over provisional layout (Soft Blue field + clip card), encode."""
import numpy as np, sys, os, subprocess, json, glob
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import softblue as B
from grade import grade, LOOKS
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
W, H = 1080, 1920
OY = 175                       # output y of source row 0 (scale 0.5, source bottom 3490 -> 1920)
CARD = (60, 36, 1020, 576)     # provisional clip card (960x540)
WRAP, WRAP_SIG = 0.12, 10
MIN_FRAG = 400                 # px at output scale; Dan is one blob of ~600k px

def card_layer(card_img):
    """RGBA layer with the clip still in a rounded card, hairline border and soft shadow."""
    x0, y0, x1, y1 = CARD; cw, ch = x1 - x0, y1 - y0
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y0 + 14, x1 + 6, y1 + 14), 26, fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    lay = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), lay, sh)
    im = card_img.convert("RGB").resize((cw, ch), Image.Resampling.LANCZOS)
    m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, ch - 1), 22, fill=255)
    lay.paste(im, (x0, y0), m)
    ImageDraw.Draw(lay).rounded_rectangle((x0, y0, x1 - 1, y1 - 1), 22, outline=(150, 200, 255, 120), width=2)
    return lay

def background(t, card):
    if card is None:   # key-check backdrop: flat pale grey-blue, no card
        return np.ones((H, W, 3), np.float32) * np.array([0.86, 0.89, 0.93], np.float32)
    f = B.field(t, W, H).convert("RGBA")
    f.alpha_composite(card)
    return np.asarray(f.convert("RGB")).astype(np.float32) / 255

def comp_frame(cache_npy, bg, look):
    d = np.load(cache_npy).astype(np.float32)
    Fp, a = d[..., :3], d[..., 3]
    # despeckle: drop keyed fragments not attached to Dan (grain read as foreground)
    # keep only real body parts (components of alpha > 0.03 over MIN_FRAG px) plus a 3 px edge zone around them;
    # faint haze bridges had kept grain specks attached to the arm edge
    lab, n = ndi.label(a > 0.03)
    if n:
        sizes = ndi.sum(np.ones_like(a), lab, index=np.arange(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= MIN_FRAG
        m = ndi.binary_dilation(keep[lab], iterations=3)
        a = np.where(m, a, 0); Fp = np.where(m[..., None], Fp, 0)
    # haze clip away from the body: the dark left edge of the screen leaves ~3% alpha haze whose peaks twinkle as
    # specks; beyond 3 px from alpha >= 0.25, re-level alpha so anything under 0.15 is background (blur tails stay)
    far = ndi.distance_transform_edt(a < 0.25) > 3
    a_new = np.where(far, np.clip((a - 0.15) / 0.85, 0, 1), a)
    Fp = Fp * np.where(a > 1e-4, a_new / np.maximum(a, 1e-4), 0)[..., None]
    a = a_new
    h, w = a.shape
    F = np.where(a[..., None] > 0.01, Fp / np.maximum(a[..., None], 1e-3), 0)
    G = grade(F, **LOOKS[look]) if look else F
    out = bg.copy()
    reg = out[OY:OY + h, :w]
    A = a[..., None]
    comp = G * A + reg * (1 - A)
    if WRAP:
        inv = 1 - a
        bb = np.stack([ndi.gaussian_filter(reg[..., c] * inv, WRAP_SIG) for c in range(3)], -1)
        cover = ndi.gaussian_filter(inv, WRAP_SIG)[..., None]
        wrapm = WRAP * cover * A
        comp = comp * (1 - wrapm) + bb / np.maximum(cover, 1e-3) * wrapm
    out[OY:OY + h, :w] = comp
    return np.clip(out, 0, 1)

if __name__ == "__main__":
    cache, look, outmp4, card_png = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    audio = sys.argv[5] if len(sys.argv) > 5 else None
    look = None if look == "none" else look
    files = sorted(glob.glob(f"{cache}/f*.npy"))
    assert len(files) > 200, f"cache {cache} has {len(files)} frames: refusing to write an empty or partial sample"
    card = None if card_png == "pale" else card_layer(Image.open(card_png))
    cmd = [FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30000/1001", "-i", "-"]
    if audio: cmd += ["-i", audio]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    if audio: cmd += ["-c:a", "aac", "-b:a", "256k", "-shortest"]
    cmd += ["-movflags", "+faststart", outmp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, f in enumerate(files):
        bg = background(i / 29.97, card)
        fr = comp_frame(f, bg, look)
        p.stdin.write((fr * 255 + 0.5).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); print("wrote", outmp4, len(files), "frames")
