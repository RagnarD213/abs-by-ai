#!/usr/bin/env python3
"""Rev-1 asset additions (J2 style locked):
- shot1/shot2 rebuilt as FIT panels (cover crop cut off head/shorts — Dan's 0:17 note)
- phone mockup: goal image on a phone lockscreen, tagged
Existing assets_v1/* (tag, cta_bar, end_card, p_goal, p_before, p_app_*, p_vidbg,
p_shot3, p_shot4) are reused unchanged.
"""
from PIL import Image, ImageDraw, ImageFont
import importlib.util
spec = importlib.util.spec_from_file_location("pa", "prep_assets.py")
pa = importlib.util.module_from_spec(spec); spec.loader.exec_module(pa)

# 1. shot1 / shot2 as fit panels (J2 bg, whole image visible)
pa.compose_panel(1, pa.SHOTS[0], "assets_v1/p_shot1.jpg")
pa.compose_panel(1, pa.SHOTS[1], "assets_v1/p_shot2.jpg")

# 2. phone mockup — goal image on a phone, J2 bg, lockscreen clock, tag
W, H = 1920, 1080
canvas = pa.panel_bg(1)
goal = Image.open(pa.GOAL).convert("RGB")
ph_h = 960; ph_w = 470          # phone body
scr_pad = 14
sx, sy = (W - ph_w) // 2, (H - ph_h) // 2 + 20
# screen: cover-crop goal to screen aspect
sw, sh = ph_w - 2 * scr_pad, ph_h - 2 * scr_pad
ga = goal.width / goal.height
if ga > sw / sh:
    nw = int(goal.height * sw / sh); goal = goal.crop(((goal.width - nw) // 2, 0, (goal.width - nw) // 2 + nw, goal.height))
else:
    nh = int(goal.width * sh / sw); goal = goal.crop((0, (goal.height - nh) // 2, goal.width, (goal.height - nh) // 2 + nh))
goal = goal.resize((sw, sh), Image.LANCZOS)
d = ImageDraw.Draw(canvas)
d.rounded_rectangle([sx - 6, sy - 6, sx + ph_w + 5, sy + ph_h + 5], radius=64, fill=(24, 25, 22))  # bezel glow edge
d.rounded_rectangle([sx, sy, sx + ph_w, sy + ph_h], radius=56, fill=(5, 5, 5))
mask = Image.new("L", (sw, sh), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=44, fill=255)
canvas.paste(goal, (sx + scr_pad, sy + scr_pad), mask)
d = ImageDraw.Draw(canvas)
# notch + lockscreen clock
d.rounded_rectangle([sx + ph_w // 2 - 60, sy + scr_pad + 8, sx + ph_w // 2 + 60, sy + scr_pad + 30], radius=11, fill=(5, 5, 5))
fclock = ImageFont.truetype(pa.MANROPE, 92)
ftime = ImageFont.truetype(pa.MANROPE, 30)
tw = d.textlength("6:30", font=fclock)
d.text((sx + ph_w / 2 - tw / 2, sy + 70), "6:30", font=fclock, fill=(255, 255, 255))
tw = d.textlength("Monday, June 3", font=ftime)
d.text((sx + ph_w / 2 - tw / 2, sy + 175), "Monday, June 3", font=ftime, fill=(240, 240, 240))
tag = Image.open("assets_v1/tag.png").convert("RGBA")
canvas.paste(tag, (W // 2 - tag.width // 2, 30), tag)
canvas.save("assets_v1/p_phone_mock.jpg", quality=92)
print("rev1 assets done")
