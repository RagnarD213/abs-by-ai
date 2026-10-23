"""SL-09 shared bits (from SL-07 lib.py): frames of Zeeshan's finished Video 4 master (decoded BT.709, his grade carried as is:
Dan finalized the film), the Soft Blue title band, captions, wordmark."""
import json, os, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, ROOT + "/.claude/skills/_shared"); sys.path.insert(0, ROOT + "/.claude/skills/_shared/hyperframes")
import softblue as B
FF = ROOT + "/Media/video_edit/bin/ffmpeg"
MASTER = ROOT + "/Zeeshan Content Videos/my honest oura ring review - video 4/my honest oura ring review | zeeshan | 16x9 | video 4.mp4"
MASTER_MD5 = "5264285762af41f2a6644366e0bae7eb"
ROLL = "MASTER"
W, H, DROP = 1080, 1920, 310
CAP_TOP = 1412
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
DEC = "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb24"      # his master: BT.709, never ffmpeg's 601 default
def raw(roll, t, w=1920, h=1080):
    b = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, t - 2):.3f}", "-i", MASTER, "-ss", f"{min(2, t):.3f}", "-frames:v", "1", "-vf", DEC, "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (1920, 1080), b)
def window(im, cx, cw, ch, y0=0):
    x = int(min(max(cx - cw / 2, 0), 1920 - cw)); return im.crop((x, y0, x + cw, y0 + ch))
def band(bg, eyebrow, lines, t=0):
    """The title band, y 0..310 on the Soft Blue field (SL-03 approved geometry). Eyebrow in title case (VIDEO-RULES 2026-10-16)."""
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
def caption(bg, lines, top=CAP_TOP, size=86):
    d = ImageDraw.Draw(bg); f = ImageFont.truetype(ARIAL, size); y = top
    for s in lines:
        w = d.textlength(s, font=f); x = (W - w) / 2
        d.text((x + 3, y + 3), s, font=f, fill=(0, 0, 0), stroke_width=7, stroke_fill=(0, 0, 0))
        d.text((x, y), s, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0)); y += int(size * 1.12)
    return y
def canvas(t=0): return B.field(t, W, H).convert("RGB")
def save(bg, path):
    bg.save(path + ".jpg", quality=92); bg.resize((540, 960), Image.LANCZOS).save(path + "_sm.jpg", quality=88)
