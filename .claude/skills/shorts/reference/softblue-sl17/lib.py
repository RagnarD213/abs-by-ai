"""SL-17 shared bits (adapted from SL-15): graded raw-frame grabs of C1768 4K (RO-26 film grade: eq contrast 1.12 gamma 1.15 sat 1.14 bright 0.012, recipe render_r5.py patch()).
SL-15 header follows:  (from softblue-sl07/lib.py): graded raw-frame grabs of C1512 (RO-19 look F, the roll's skin-anchored curve, 16 bit, BT.709), the Soft Blue title band, captions, wordmark.
C1512 is 1920x1080 (the 8/3 shoot), so a 724 window is upscaled 1.49x to the 1080 px picture (the film's own camera frame; no 4K source exists)."""
import json, os, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, ROOT + "/.claude/skills/_shared"); sys.path.insert(0, ROOT + "/.claude/skills/_shared/hyperframes")
import softblue as B
FF = ROOT + "/Media/video_edit/bin/ffmpeg"
RAWD = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop"
GRADE = "eq=contrast=1.12:gamma=1.15:saturation=1.14:brightness=0.012"      # RO-26 R5 film grade (render_r5.py patch(), the approved look)
ROLL = "C1768"
CURVES = json.load(open("/Volumes/Extreme/_edit_work/SL-17/curves.json"))["filter"]      # fitgrade.py: the master's measured look after grade B (held-out frames mae 5.0 -> 1.95 of 255)
TORGB = "scale=flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=rgb24"
W, H, DROP = 1080, 1920, 310
CAP_TOP = 1412
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def grade_vf(w=1920, h=1080):
    """the film's own chain (RO-19 frames.vf): decode BT.709 (tagged) -> 16 bit -> look F curve -> rgb24"""
    return f"scale={w}:{h}:flags=lanczos,{GRADE},{TORGB},{CURVES}"
def raw(roll, t, w=1920, h=1080):
    b = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, t - 2):.3f}", "-i", f"{RAWD}/{roll}.MP4", "-ss", f"{min(2, t):.3f}", "-frames:v", "1", "-vf", grade_vf(w, h), "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (w, h), b)
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
    y = 86      # SL-17 (reviewer B5): 96 let a second line's descenders (g, y) run into the band edge at 309; 86 + 96 leaves about 12 px
    for line in lines: d.text((64, y), line, font=fh, fill=B.WHITE); y += 96
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
