"""SL-06 shared bits (from softblue-sl03/lib.py): graded raw-frame grabs of C1706 (RO-12 grade-C lut, BT.709), the Soft Blue title band, captions, wordmark."""
import json, os, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, ROOT + "/.claude/skills/_shared"); sys.path.insert(0, ROOT + "/.claude/skills/_shared/hyperframes")
import softblue as B
FF = ROOT + "/Media/video_edit/bin/ffmpeg"
RAWD = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content"
LUT = "/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube"      # RO-12's locked 9/23 look (notes-RO12.md)
ROLL = "C1706"
W, H, DROP = 1080, 1920, 310
CAP_TOP = 1412
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def grade_vf(w=1920, h=1080):
    """the film's own chain (build.py presenter): decode BT.709 -> float -> grade-C lut -> full-range rgb24, at w x h of the whole 4K frame"""
    return (f"scale={w}:{h}:flags=accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le,"
            f"lut3d=file='{LUT}':interp=tetrahedral,scale=out_color_matrix=bt709:out_range=pc,format=rgb24")
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
    y = 86      # 2026-10-22 (SL-17 reviewer B5): 96/100 let a second line's descenders (g, j, p, q, y) at 88 px run to row 312, cut by the glass line at 309; 86/96 ends them at 298 (softblue_titlecheck.py enforces < 299)
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
