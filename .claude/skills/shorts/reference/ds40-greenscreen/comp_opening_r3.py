"""DS-40 R3 opening: the Maher clip full screen (vertical crop), Dan keyed small in the bottom-left corner while it
plays (his real reaction, watched live on the laptop), then a 0.5 s move: the clip shrinks into its card at the top,
Dan grows to full size and speaks ("Bill Maher is right...", the approved R2 sample).

    python3 comp_opening.py OUT.mp4 [--pink]     (--pink: no clip, saturated pink, key check only, no audio)
"""
import numpy as np, sys, os, subprocess, cv2
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import softblue as B
from grade import grade, LOOKS

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
W, H, FPS = 1080, 1920, 30000 / 1001
R3 = os.environ.get("R3DIR", "/Volumes/Expansion/_edit_work/ds40/r3")
CLIP = os.environ.get("CLIP", "/Volumes/Extreme/_edit_work/ds40/r1/src/maher_yfiWjnStE3w_210-238.mp4")
CLIP_IN, CLIP_OUT = 4.40, 23.78          # "let me ask you this" .. "an unchallenged lie" (doc: 2:15 to 2:33)
# R3 review: 4.30 let a stray "But" in; 23.55 clipped the end of "lie" (it runs to 23.72; "that" starts 24.36)
N_CLIP = int(round((CLIP_OUT - CLIP_IN) * FPS))     # 581 frames
SMALL_OFF = int(round((CLIP_IN - 4.30) * FPS))      # cache_small frame 0 = roll 1354.70 = clip 4.30 (laptop playback)
DISSOLVE = 3                             # move frames over which the watching take dissolves into the scripted take
FEATHER = 120                            # px: soft right edge of his footage around the shrug (the hand leaves the camera)
EDGE = 36                                # px (12 px at the small size): narrow soft edge on every other frame, so a shoulder
                                         # that runs past the camera's own picture edge reads soft, not sliced (R3 re-check 3)
SHRUG = (100, 130, 6)                    # small-phase frames given the wide fade, with ramp frames (R3 re-check 2: a fade on
                                         # all the time ate into his shoulder, which normally sits 8-20 px from that edge)
SMALL = R3 + "/cache_small"
LARGE = os.environ.get("LARGE", "/Volumes/Expansion/_edit_work/ds40/r2/cache_r2")   # approved R2 sample, roll 1400.25
AUDIO_DAN = "/Volumes/Extreme/_edit_work/ds40/r1/audio/s10_E_bass15.wav"
CROP_CX = 620                            # Maher's head centre in the 1280x720 clip (one shot, steady crop)
OY = 175                                 # large Dan: output y of source row 0 (as R1/R2)
S_SMALL, SMALL_BODY_X = 0.33, 178        # small Dan: scale; his footage sits flush on the left and bottom screen edges
                                         # (R3 re-check: 14 px in from the edge, his arm ended in a straight line)
BODY_CX = 540                            # body centre in Dan's own 1080-wide frame
MOVE = 15                                # frames for the shrink/grow move (0.5 s)
CARD = (60, 36, 1020, 576)               # the clip card of the R1/R2 placeholder layout
LOOK = LOOKS["B_warmvivid"]
MIN_FRAG = 400

def shrug_fw(k):
    """Right-edge fade width for small-phase frame k: wide around the shrug, narrow (EDGE) elsewhere."""
    a, b, r = SHRUG
    w = min(1.0, max(0.0, (k - (a - r)) / r), max(0.0, ((b + r) - k) / r))
    return EDGE + (FEATHER - EDGE) * w

def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)

def dan_layer(npy):
    """Graded straight colour G and alpha a at 1745x1080 (same despeckle and haze clip as the R2 sample)."""
    d = np.load(npy).astype(np.float32); Fp, a = d[..., :3], d[..., 3]
    lab, n = ndi.label(a > 0.03)
    if n:
        sizes = ndi.sum(np.ones_like(a), lab, index=np.arange(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= MIN_FRAG
        m = ndi.binary_dilation(keep[lab], iterations=3)
        a = np.where(m, a, 0); Fp = np.where(m[..., None], Fp, 0)
    far = ndi.distance_transform_edt(a < 0.25) > 3
    a_new = np.where(far, np.clip((a - 0.15) / 0.85, 0, 1), a)
    Fp = Fp * np.where(a > 1e-4, a_new / np.maximum(a, 1e-4), 0)[..., None]; a = a_new
    F = np.where(a[..., None] > 0.01, Fp / np.maximum(a[..., None], 1e-3), 0)
    return grade(F, **LOOK), a

def place(out, G, a, s, x0, y0, wrap=0.12, wrap_sig=10, feather=0.0, fw=FEATHER):
    """Composite Dan (straight G, alpha a) scaled by s with top-left at (x0, y0); premultiplied area resize.
    feather (0..1): fade his footage out toward its left, right and top edges, for when those edges sit inside the
    screen (small Dan): a hand that leaves the camera fades instead of stopping on a straight line."""
    h, w = a.shape
    if feather > 0:
        xs = np.arange(w).astype(np.float32)
        rl = np.ones(w, np.float32) if x0 <= 0 else xs / FEATHER          # no fade on an edge that sits on the screen edge
        rx = np.minimum(rl, (w - 1 - xs) / max(fw, 1.0)); ry = np.arange(h) / FEATHER
        ramp = np.clip(rx[None, :], 0, 1) * np.clip(ry[:, None], 0, 1)
        a = a * (1 - feather + feather * ramp)
    if s != 1.0:
        sw, sh = max(1, int(round(w * s))), max(1, int(round(h * s)))
        P = cv2.resize(G * a[..., None], (sw, sh), interpolation=cv2.INTER_AREA)
        a = cv2.resize(a, (sw, sh), interpolation=cv2.INTER_AREA)
        G = np.where(a[..., None] > 1e-3, P / np.maximum(a[..., None], 1e-3), 0)
    h, w = a.shape
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if X1 <= X0 or Y1 <= Y0: return out
    ga = G[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]; aa = a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    reg = out[Y0:Y1, X0:X1]
    A = aa[..., None]; comp = ga * A + reg * (1 - A)
    if wrap:
        sg = max(2.0, wrap_sig * s); inv = 1 - aa
        bb = np.stack([ndi.gaussian_filter(reg[..., c] * inv, sg) for c in range(3)], -1)
        cover = ndi.gaussian_filter(inv, sg)[..., None]; wm = wrap * cover * A
        comp = comp * (1 - wm) + bb / np.maximum(cover, 1e-3) * wm
    out[Y0:Y1, X0:X1] = comp
    return out

def clip_frames():
    p = subprocess.Popen([FF, "-v", "error", "-ss", f"{CLIP_IN:.3f}", "-i", CLIP, "-t", f"{CLIP_OUT - CLIP_IN + 0.2:.3f}",
                          "-vf", "fps=30000/1001,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24",
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(1280 * 720 * 3)
        if len(b) < 1280 * 720 * 3: break
        yield np.frombuffer(b, np.uint8).reshape(720, 1280, 3).astype(np.float32) / 255
    p.wait()

def clip_view(fr, w, h):
    """The part of the clip that fills a w x h box: largest window of that aspect, centred on Maher, sharpened up."""
    asp = w / h
    ch = 720 if 1280 / 720 >= asp else 1280 / asp
    cw = ch * asp
    cx = min(max(CROP_CX, cw / 2), 1280 - cw / 2); cy = 360
    M = np.array([[w / cw, 0, -(cx - cw / 2) * w / cw], [0, h / ch, -(cy - ch / 2) * h / ch]], np.float32)
    v = cv2.warpAffine(fr, M, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    if w / cw > 1.5:   # upscaled: gentle unsharp so the 720p clip does not look mushy on a phone
        bl = cv2.GaussianBlur(v, (0, 0), 1.6); v = np.clip(v + 0.45 * (v - bl), 0, 1)
    return v

def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), int(r), fill=255)
    return np.asarray(m).astype(np.float32)[..., None] / 255

def main(out_mp4, pink=False):
    small = lambda i: f"{SMALL}/f{i:04d}.npy"   # by frame number (a copy may hold only the frames used)
    large = [f"{LARGE}/f{i:04d}.npy" for i in range(279)]
    need = range(SMALL_OFF, SMALL_OFF + N_CLIP + DISSOLVE)
    assert all(os.path.exists(small(i)) for i in need), f"small cache is missing frames in {need}"
    assert all(os.path.exists(f) for f in large)
    sw = int(round(1080 * S_SMALL)); sh_ = int(round(1745 * S_SMALL))
    sx0, sy0 = int(round(SMALL_BODY_X - BODY_CX * S_SMALL)), H - sh_
    cmd = [FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30000/1001", "-i", "-"]
    if not pink:
        cmd += ["-i", R3 + "/audio/opening.wav"]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    if not pink:
        cmd += ["-c:a", "aac", "-b:a", "256k", "-shortest"]
    cmd += ["-movflags", "+faststart", out_mp4]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    clips = clip_frames(); last = None; n = 0
    total = N_CLIP + len(large)
    for k in range(total):
        t = k / FPS
        if k < N_CLIP:
            fr = next(clips); last = fr
        else:
            fr = last
        if k < N_CLIP:
            # the clip full screen, Dan small in the corner
            bg = np.ones((H, W, 3), np.float32) * np.array([0.95, 0.25, 0.62], np.float32) if pink else clip_view(fr, W, H)
            G, a = dan_layer(small(k + SMALL_OFF))
            out = place(bg, G, a, S_SMALL, sx0, sy0, feather=1.0, fw=shrug_fw(k))
        else:
            j = k - N_CLIP; u = ease((j + 1) / MOVE)
            field = np.asarray(B.field(t, W, H).convert("RGB")).astype(np.float32) / 255
            out = np.ones_like(field) * np.array([0.95, 0.25, 0.62], np.float32) if pink else field.copy()
            if not pink:
                x0, y0, x1, y1 = CARD
                bx0 = 0 + (x0 - 0) * u; by0 = 0 + (y0 - 0) * u; bx1 = W + (x1 - W) * u; by1 = H + (y1 - H) * u
                bw, bh = int(round(bx1 - bx0)), int(round(by1 - by0))
                v = clip_view(last, bw, bh)
                if u > 0:   # soft shadow and rounded corners grow in with the move
                    m = rounded_mask(bw, bh, 22 * u)
                    sh = np.zeros((H, W), np.float32)
                    sh[int(by0) + int(14 * u):int(by0) + int(14 * u) + bh, int(bx0) + 6:int(bx0) + 6 + bw] = 0.59 * u
                    sh = cv2.GaussianBlur(sh, (0, 0), 18)[..., None]
                    out = out * (1 - sh)
                else:
                    m = np.ones((bh, bw, 1), np.float32)
                X0, Y0 = int(round(bx0)), int(round(by0))
                X1, Y1 = min(W, X0 + bw), min(H, Y0 + bh)
                out[Y0:Y1, X0:X1] = v[:Y1 - Y0, :X1 - X0] * m[:Y1 - Y0, :X1 - X0] + out[Y0:Y1, X0:X1] * (1 - m[:Y1 - Y0, :X1 - X0])
                if u >= 1:   # hairline border of the settled card
                    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    ImageDraw.Draw(lay).rounded_rectangle((x0, y0, x1 - 1, y1 - 1), 22, outline=(150, 200, 255, 120), width=2)
                    L = np.asarray(lay).astype(np.float32) / 255
                    out = out * (1 - L[..., 3:]) + L[..., :3] * L[..., 3:]
            G, a = dan_layer(large[j])
            if j < DISSOLVE:   # the watching take dissolves into the scripted take (they are 26 s apart on the roll)
                d = (j + 1) / (DISSOLVE + 1)
                G1, a1 = dan_layer(small(N_CLIP + SMALL_OFF + j))
                an = a1 * (1 - d) + a * d
                G = (G1 * (a1 * (1 - d))[..., None] + G * (a * d)[..., None]) / np.maximum(an, 1e-4)[..., None]; a = an
            s = S_SMALL + (1 - S_SMALL) * u
            x0d = sx0 + (0 - sx0) * u
            y0d = H - int(round(1745 * s))   # his footage always ends on the bottom edge (no stray field row)
            out = place(out, G, a, s, int(round(x0d)), int(y0d), feather=1 - u, fw=EDGE)
        enc.stdin.write((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes()); n += 1
        if n % 120 == 0: print(n, "frames", flush=True)
    enc.stdin.close(); enc.wait()
    assert n == total and enc.returncode == 0, (n, total, enc.returncode)
    print("wrote", out_mp4, n, "frames")

if __name__ == "__main__":
    main(sys.argv[1], "--pink" in sys.argv)
