#!/usr/bin/env python3
"""Single-frame preview of the rev5 (J2AD) graphic system, composited on a REAL frame.

Rendering a whole ad to find out the type is wrong is the expensive way round -- the
skill's rule is to preview on a real frame first.
"""
import importlib.util, subprocess, sys
from PIL import Image, ImageDraw

SK = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec = importlib.util.spec_from_file_location("ml", f"{SK}/motionlib.py")
ml = importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
PAL = ml.J2AD
FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"

def real_frame(t=36.0):
    grade = open("../grade25.txt").read().strip()
    raw = subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", "../CUT_v2_graded.mp4",
                          "-vframes", "1", "-vf", grade, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (1920, 1080), raw).convert("RGBA")

def grab(fn, *a, **kw):
    """Render one component to a MOV, then pull a frame from ~65% through it."""
    out = "/tmp/_prev.mov"
    fn(out, *a, **kw)
    raw = subprocess.run([FF, "-v", "error", "-i", out, "-vf", "select='eq(n\\,20)'",
                          "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                         capture_output=True).stdout
    return Image.frombytes("RGBA", (1920, 1080), raw[:1920*1080*4])

tiles = []

t = grab(ml.title_card, "Visualizing\nYour Goal",
         "One of the most powerful ways to motivate yourself", 1.0,
         pal=PAL, band=PAL.deep, band_ink=(255, 255, 255))
tiles.append(("title card  (green band, white type, black field)", t))

b = grab(ml.bullets_build, "In today's video",
         [(0.0, "How I got limitless motivation to work out and to eat healthy"),
          (0.15, "What I needed to do to lose my belly fat and get six-pack abs"),
          (0.3, "How you can generate a goal picture of yourself with abs for free")],
         1.2, pal=PAL, head_color=PAL.accent)
base = real_frame()
vid = base.crop((450, 0, 1920, 1080)).resize((940, 1080))
sh = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255)); sh.paste(vid, (980, 0))
sh.alpha_composite(b)
tiles.append(("bullets  (olive caps heading, white body, black panel)", sh))

l = grab(ml.lower_third_bar,
         ["If you saw yourself with abs, you'd be MOTIVATED",
          "to make your dream body a reality."],
         1.0, pal=PAL, size=40, lead_size=44)
f = real_frame(); f.alpha_composite(l)
tiles.append(("lower third  (green bar, white on black)", f))

l2 = grab(ml.lower_third_bar, ["You don't need more knowledge",
                               "You need the motivation to execute what you know"],
          1.0, pal=PAL, size=38, lead_size=46, bar_color=PAL.hot)
f2 = real_frame(100.0); f2.alpha_composite(l2)
tiles.append(("lower third  (red bar variant, for the contrast beat)", f2))

W = 960
sheet = Image.new("RGB", (W * 2, (int(W * 9 / 16) + 28) * 2), (25, 25, 25))
d = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(tiles):
    th = int(W * 9 / 16)
    x, y = (i % 2) * W, (i // 2) * (th + 28)
    sheet.paste(im.convert("RGB").resize((W, th)), (x, y + 28))
    d.text((x + 8, y + 8), name, fill=(255, 230, 120))
sheet.save("style_preview.png")
print("style_preview.png")
