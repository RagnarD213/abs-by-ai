"""DS-40 R4: the intro clip only (19.4 s), two ways, for Dan to compare.

    python3 comp_r4.py A|B OUT.mp4 [--pink]

A  you in a framed box in the upper left (rounded corners, thin border, soft shadow, moving Soft Blue field inside),
   sized to stay clear of Maher's face (230 x 340: clear of his face box on 93% of frames; bigger covers him often).
B  you in the lower left, larger than R3 (0.40 of full size, was 0.33), laptop visible along the bottom of your footage,
   flush on the left and bottom screen edges, narrow soft right edge (wide only around the shrug, as approved in R3).
--pink: saturated pink instead of the clip (and inside the box), no sound: key check only.
Everything else (clip passage, crop, your real reaction footage, key, grade) is the R3 build that passed review.
"""
import sys, os, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import comp_opening as C
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import softblue as SB

R4 = "/Volumes/Expansion/_edit_work/ds40/r4"
C.SMALL = R4 + "/cache_full"               # full-height key (1920 x 1080 at output scale): the laptop is kept
W, H = C.W, C.H
PINK = np.array([0.95, 0.25, 0.62], np.float32)
# A: the box
BOX = (24, 24, 230, 340)                   # x, y, w, h
CROP_Y0 = 320                              # footage rows above this are empty screen (head top is about row 400)
RADIUS, BORDER = 18, (150, 200, 255, 150)
# B: lower left, larger
S_B = 0.40

def small(k):
    return f"{C.SMALL}/f{k + C.SMALL_OFF:04d}.npy"

def rounded(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return np.asarray(m).astype(np.float32)[..., None] / 255

def frame_A(bg, k, t, pink):
    x, y, w, h = BOX
    inner = np.ones((h, w, 3), np.float32) * PINK if pink else np.asarray(SB.field(t, w, h).convert("RGB")).astype(np.float32) / 255
    G, a = C.dan_layer(small(k))
    s = w / 1080
    inner = C.place(inner, G, a, s, 0, int(round(-CROP_Y0 * s)), wrap=0.10, wrap_sig=6)
    m = rounded(w, h, RADIUS)
    # soft shadow under the box, then the box, then a thin light border
    sh = np.zeros((H, W), np.float32); sh[y + 8:y + 8 + h, x + 4:x + 4 + w] = 0.55
    out = bg * (1 - cv2.GaussianBlur(sh, (0, 0), 14)[..., None])
    out[y:y + h, x:x + w] = inner * m + out[y:y + h, x:x + w] * (1 - m)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((x, y, x + w - 1, y + h - 1), RADIUS, outline=BORDER, width=2)
    L = np.asarray(lay).astype(np.float32) / 255
    return out * (1 - L[..., 3:]) + L[..., :3] * L[..., 3:]

def frame_B(bg, k):
    G, a = C.dan_layer(small(k))
    h = int(round(1920 * S_B))
    return C.place(bg, G, a, S_B, 0, H - h, feather=1.0, fw=C.shrug_fw(k))

def main(which, out_mp4, pink=False):
    n = C.N_CLIP
    assert all(os.path.exists(small(k)) for k in range(n)), "full-height cache incomplete"
    audio = R4 + "/audio/clip_only.wav"
    cmd = [C.FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30000/1001", "-i", "-"]
    if not pink: cmd += ["-i", audio]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    if not pink: cmd += ["-c:a", "aac", "-b:a", "256k", "-shortest"]
    cmd += ["-movflags", "+faststart", out_mp4]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    clips = C.clip_frames()
    for k in range(n):
        fr = next(clips)
        bg = np.ones((H, W, 3), np.float32) * PINK if pink else C.clip_view(fr, W, H)
        out = frame_A(bg, k, k / C.FPS, pink) if which == "A" else frame_B(bg, k)
        enc.stdin.write((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        if (k + 1) % 120 == 0: print(k + 1, "frames", flush=True)
    enc.stdin.close(); enc.wait()
    assert enc.returncode == 0
    print("wrote", out_mp4, n, "frames")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--pink" in sys.argv)
