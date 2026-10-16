#!/usr/bin/env python3
"""round 3: AI_B1's needle made one slow 180-degree sweep and stretched (frame-reviewer FAIL). The man, his feet and the room are still
(0 to 1 px), so only the dial is rebuilt: a needle-free dial plate (left half from frame 131, right half from frame 1), pasted on every
original frame, with a drawn needle that swings back and forth around one reading like the approved concept (a metronome). -> clips/AI_B1_fix.mp4"""
import numpy as np, subprocess, os
from PIL import Image, ImageDraw, ImageFilter
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
D = "/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/4e3b94ce-d142-4491-845d-425d2f6ff265/scratchpad/b1"; N = 144; FPS = 24
HX, HY = 539.5, 1213.0                      # hub (measured on frames 1 and 131 at 4x)
RX, RY = 58.0, 36.5                         # inner dial radii (perspective ellipse)
fr = lambda i: np.asarray(Image.open(f"{D}/f{i + 1:03d}.png").convert("RGB")).astype(np.float32)
f1, f131 = fr(0), fr(130)
# red of the AI needle, for the colour of ours
reg = f1[1205:1222, 485:530]; red = reg[(reg[..., 0] > 150) & (reg[..., 1] < 90)]; RED = tuple(int(v) for v in np.median(red, 0)); print("needle red", RED)
yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
left = np.clip((HX - 6 - xx) / 6, 0, 1)                    # soft seam just left of the hub
plate = f1 * (1 - left[..., None]) + f131 * left[..., None]
e = ((xx - HX) / (RX + 9)) ** 2 + ((yy - HY) / (RY + 7)) ** 2        # paste the dial inside its ring (+ the ring's inner edge, where the old tip strayed)
m = np.clip((1.0 - e) / 0.08, 0, 1)[..., None]
def needle(phi, S=4):
    """the needle at angle phi (degrees, 90 = 12 o'clock) in the dial plane, projected, drawn at S x and downsampled; RGBA"""
    W0, H0 = 200 * S, 140 * S; cx, cy = 100 * S, 70 * S
    im = Image.new("RGBA", (W0, H0), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c, s = np.cos(np.radians(phi)), np.sin(np.radians(phi)); L = 0.86 * RX; ry = RY / RX
    def P(u, v):                                             # u along the needle, v across it, in plane units -> image
        x = u * c - v * s; y = u * s + v * c; return (cx + x * S, cy - y * ry * S)
    d.polygon([P(-7, -2.4), P(L - 3, -1.1), P(L, 0), P(L - 3, 1.1), P(-7, 2.4)], fill=RED + (255,))
    d.polygon([P(-7, -2.4), P(L - 3, -1.1), P(L, 0), P(L - 3, 1.1), P(-7, 2.4)], outline=tuple(int(v * 0.6) for v in RED) + (200,))
    r = 5.5; d.ellipse([cx - r * S, cy - r * ry * S * 1.25, cx + r * S, cy + r * ry * S * 1.25], fill=tuple(int(v * 0.85) for v in RED) + (255,))
    r = 2.0; d.ellipse([cx - r * S, cy - r * S * 0.8 - S, cx + r * S, cy + r * S * 0.8 - S], fill=(255, 140, 140, 120))      # a small highlight on the hub
    return np.asarray(im.resize((200, 140), Image.LANCZOS)).astype(np.float32)
sh = Image.new("L", (200, 140), 0)
def phi_at(t): return 100.0 + 24.0 * np.sin(2 * np.pi * (t - 0.15) / 1.3)          # back and forth around one reading, about every 1.3 s
os.makedirs("/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/4e3b94ce-d142-4491-845d-425d2f6ff265/scratchpad/b1fix", exist_ok=True)
for i in range(N):
    base = fr(i); out = base * (1 - m) + plate * m
    acc = np.zeros((140, 200, 4), np.float32)
    for k in range(4): acc += needle(phi_at((i + (k - 1.5) / 4 * 0.5) / FPS))                # a little motion blur (half a frame's shutter)
    acc /= 4
    shadow = np.asarray(Image.fromarray(acc[..., 3].astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32) / 255 * 0.25
    x0, y0 = int(HX) - 100, int(HY) - 70; sub = out[y0:y0 + 140, x0:x0 + 200]
    sub[2:, 2:] *= (1 - shadow[:-2, :-2, None])                                              # soft shadow, down-right
    a = acc[..., 3:4] / 255; sub[:] = sub * (1 - a) + acc[..., :3] * a
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(f"/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/4e3b94ce-d142-4491-845d-425d2f6ff265/scratchpad/b1fix/f{i + 1:03d}.png")
subprocess.run([FF, "-v", "error", "-y", "-framerate", str(FPS), "-i", "/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/4e3b94ce-d142-4491-845d-425d2f6ff265/scratchpad/b1fix/f%03d.png", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "clips/AI_B1_fix.mp4"], check=True)
print("clips/AI_B1_fix.mp4")
