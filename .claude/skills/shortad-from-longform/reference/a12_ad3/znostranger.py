#!/usr/bin/env python3
"""NOBODY ELSE'S BODY IN DAN'S AD -- checked on the DELIVERED file, every frame of the beats that can show one.

The only real app recording uploads a STRANGER's photo, not Dan (coordination 2026-09-10), and it surfaces in two
places that a time-point ban does not cover: the questionnaire SCROLLS past his photo at the card's head, and the
"Creating your future self" progress screen brings it back, entering from the BOTTOM of the screen.

⚠ This was got wrong twice. First a floor fixed the head and left the tail. Then a ceiling was set from a skin
measurement whose "baseline" was sampled at 8.0 s -- inside the range the photo was already on screen at the bottom
of the frame -- so it read the arrival as 8.52 s when it is 7.967 s, and his head still showed. Measure the whole
screen, take the baseline from a range you have proved is clean, and then CHECK THE RENDERED FRAMES.

The questionnaire carries no skin at all, so any skin inside the phone is a photo of somebody.
"""
import subprocess, sys
import numpy as np

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
# the phone hole inside the olive card, in delivered 1080x1920 pixels
BOX = (250, 250, 830, 1300)


def frames(path, n0, n1, w=270, h=480):
    n = n1 - n0
    p = subprocess.run([FF, "-v", "error", "-i", path, "-vf",
                        f"select='between(n\\,{n0}\\,{n1-1})',scale={w}:{h}", "-fps_mode", "passthrough",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.uint8)
    m = len(a)//(w*h*3)
    return a[:m*w*h*3].reshape(m, h, w, 3).astype(np.float32)


def skin_frac(a, box, w=270, h=480):
    x0, y0, x1, y1 = [int(v*w/1080) if i % 2 == 0 else int(v*h/1920) for i, v in enumerate(box)]
    s = a[:, y0:y1, x0:x1]
    r, g, b = s[..., 0], s[..., 1], s[..., 2]
    m = (r > 95) & (r < 235) & (g > 60) & (g < 195) & (b > 45) & (b < 175) & (r > g+10) & (g > b-10)
    return m.mean(axis=(1, 2))


def main():
    f = sys.argv[1] if len(sys.argv) > 1 else 'ad3_vertical_9x16.mp4'
    n0, n1 = 5278, 5362                       # the app-upload card
    a = frames(f, n0, n1)
    fr = skin_frac(a, BOX)
    bad = [(n0+i, v) for i, v in enumerate(fr) if v > 0.010]
    print(f"app-upload card {n0}-{n1} on {f}")
    print(f"  skin inside the phone: max {fr.max():.4f}  mean {fr.mean():.4f}  (the questionnaire alone reads ~0.000)")
    if bad:
        print(f"  FAIL  {len(bad)} frame(s) show a photo: " + ", ".join(f"{n} ({v:.3f})" for n, v in bad[:8]))
        return 1
    print("  PASS  no frame of the card shows anyone's photo")
    return 0


if __name__ == '__main__':
    sys.exit(main())
