"""SL-03 shared bits: graded raw-frame grabs (RO-05 grade B luts, BT.709), the Soft Blue title band, captions, wordmark."""
import json, os, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, ROOT + "/.claude/skills/_shared"); sys.path.insert(0, ROOT + "/.claude/skills/_shared/hyperframes")
import softblue as B
FF = ROOT + "/Media/video_edit/bin/ffmpeg"
RAWD = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera"
LUTS = "/Volumes/Extreme/_edit_work/ro05-fable/round2/grade/luts_B"
SCREEN = ROOT + "/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4"
SYNC = [(33.70,8.0),(48.96,24.0),(60.42,36.0),(66.32,41.0),(71.36,47.5),(74.60,53.0),(81.76,57.0),(86.94,63.0),(88.82,66.0),
        (100.86,78.0),(117.04,93.0),(146.50,121.0),(160.64,134.5),(172.58,138.0),(201.98,183.0),(237.96,214.5),(288.08,256.3),(299.58,270.0)]
BANNED_SCREEN = [(8.0, 23.0), (286.0, 293.0), (254.8, 256.0)]
W, H, DROP = 1080, 1920, 310
CAP_TOP = 1412
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def screen_t(c):
    e = [s for s in SYNC if s[0] <= c + 1e-6][-1]; st = e[1] + (c - e[0])
    for a, b in BANNED_SCREEN: assert not (a - 0.05 <= st <= b + 0.05), f"banned screen {st}"
    return st
def raw(roll, t):
    """1920x1080 graded RGB frame of a raw roll (the long-form's own chain: decode BT.709 -> rgb48 -> grade-B lut)."""
    vf = (f"scale=1920:1080:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb48le,lut3d=file='{LUTS}/{roll}.cube':interp=tetrahedral,format=rgb24")
    b = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", f"{RAWD}/{roll}.MP4", "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (1920, 1080), b)
def screen(cam_t):
    b = subprocess.run([FF, "-v", "error", "-ss", f"{screen_t(cam_t):.3f}", "-i", SCREEN, "-frames:v", "1", "-vf", "crop=1320:2500:0:175,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (1320, 2500), b)
def window(im, cx, cw, ch, y0=0):
    x = int(min(max(cx - cw / 2, 0), 1920 - cw)); return im.crop((x, y0, x + cw, y0 + ch))
def band(bg, eyebrow, lines, t=0):
    """The title band, y 0..310 on the Soft Blue field (SL-04/05 geometry, the SL-05 round-1 Soft Blue option)."""
    d = ImageDraw.Draw(bg); fe = B.font(34)
    size = 88
    while max(B.text_w(l, B.font(size)) for l in lines) > 1080 - 2 * 64: size -= 2
    fh = B.font(size)
    d.rounded_rectangle((64, 50, 71, 86), 3, fill=B.CYAN); x = 88
    for ch in eyebrow: d.text((x, 44), ch, font=fe, fill=B.CYAN); x += B.text_w(ch, fe) + 4
    assert x < 1040, eyebrow
    y = 96
    for line in lines: d.text((64, y), line, font=fh, fill=B.WHITE); y += 100
    assert y <= DROP + 2, (lines, y)
    d.line((0, DROP - 1, W, DROP - 1), fill=B.GLASS_LINE, width=2)
    return size
def wordmark(bg, xy=(64, 1800)):
    o = Image.new("RGBA", bg.size); d = ImageDraw.Draw(o); f = B.font(30)
    d.text((xy[0] + 2, xy[1] + 2), "AbsByAI.com", font=f, fill=(0, 0, 0, 140)); d.text(xy, "AbsByAI.com", font=f, fill=(244, 250, 255, 170))
    bg.paste(Image.alpha_composite(bg.convert("RGBA"), o).convert("RGB"))
def caption(bg, lines, top=CAP_TOP, size=86):
    """Approximation of the burned caption (Arial Bold 86, white, 7 px black outline, soft shadow), top line at `top`."""
    d = ImageDraw.Draw(bg); f = ImageFont.truetype(ARIAL, size); y = top
    for s in lines:
        w = d.textlength(s, font=f); x = (W - w) / 2
        d.text((x + 3, y + 3), s, font=f, fill=(0, 0, 0), stroke_width=7, stroke_fill=(0, 0, 0))
        d.text((x, y), s, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0)); y += int(size * 1.12)
    return y
def canvas(t=0): return B.field(t, W, H).convert("RGB")
def talk(bg, roll, t, cx, cw=724, ch=1080):
    im = window(raw(roll, t), cx, cw, ch).resize((W, H - DROP), Image.LANCZOS); bg.paste(im, (0, DROP)); return bg
def square(bg, roll, t, x0, y=DROP):
    im = raw(roll, t).crop((x0, 0, x0 + 1080, 1080)); bg.paste(im, (0, y)); return bg
def save(bg, path):
    bg.save(path + ".jpg", quality=92); bg.resize((540, 960), Image.LANCZOS).save(path + "_sm.jpg", quality=88)
