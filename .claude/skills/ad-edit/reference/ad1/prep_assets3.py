#!/usr/bin/env python3
"""Rev-2 assets:
1. p_phone_mock v2 — image only on the phone (no clock/date/notch text)
2. big_ai_cover.png — large AI-GENERATED box covering the email-capture region of the after screen
3. p_dad1/p_dad2 — the two iCloud dad photos as J2 panels
4. stats_scan.mp4 — sample-after scan line + stats reveal animation (full-frame 1920x1080)
"""
from PIL import Image, ImageDraw, ImageFont
import importlib.util, subprocess, os

spec = importlib.util.spec_from_file_location("pa", "prep_assets.py")
pa = importlib.util.module_from_spec(spec); spec.loader.exec_module(pa)
W, H = 1920, 1080
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"

# ---- 1. phone mock v2: image only ----
canvas = pa.panel_bg(1)
goal = Image.open(pa.GOAL).convert("RGB")
ph_h, ph_w, pad = 960, 470, 14
sx, sy = (W - ph_w) // 2, (H - ph_h) // 2 + 20
sw, sh = ph_w - 2 * pad, ph_h - 2 * pad
ga = goal.width / goal.height
if ga > sw / sh:
    nw = int(goal.height * sw / sh); goal = goal.crop(((goal.width - nw) // 2, 0, (goal.width - nw) // 2 + nw, goal.height))
else:
    nh = int(goal.width * sh / sw); goal = goal.crop((0, (goal.height - nh) // 2, goal.width, (goal.height - nh) // 2 + nh))
goal = goal.resize((sw, sh), Image.LANCZOS)
d = ImageDraw.Draw(canvas)
d.rounded_rectangle([sx - 6, sy - 6, sx + ph_w + 5, sy + ph_h + 5], radius=64, fill=(24, 25, 22))
d.rounded_rectangle([sx, sy, sx + ph_w, sy + ph_h], radius=56, fill=(5, 5, 5))
mask = Image.new("L", (sw, sh), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=44, fill=255)
canvas.paste(goal, (sx + pad, sy + pad), mask)
tag = Image.open("assets_v1/tag.png").convert("RGBA")
canvas.paste(tag, (W // 2 - tag.width // 2, 30), tag)
canvas.save("assets_v1/p_phone_mock.jpg", quality=92)

# ---- 2. big AI-GENERATED cover (over the 570-wide app panel, email region) ----
# panel x 675..1245; email text+field+button occupy roughly y 745..985 in overlay space
cw, ch = 570, 300
cov = Image.new("RGBA", (cw, ch), (0, 0, 0, 255))
d = ImageDraw.Draw(cov)
d.rectangle([0, 0, cw - 1, ch - 1], outline=pa.OLIVE, width=3)
f = ImageFont.truetype(pa.COPPER, 64)
t = "AI-GENERATED"
tw = d.textlength(t, font=f)
d.text(((cw - tw) / 2, (ch - 74) / 2), t, font=f, fill=(255, 255, 255, 255))
cov.save("assets_v1/big_ai_cover.png")

# ---- 3. dad photo panels ----
pa.compose_panel(1, "icloud_photo1.jpg", "assets_v1/p_dad1.jpg")
pa.compose_panel(1, "icloud_photo2.jpg", "assets_v1/p_dad2.jpg")

# ---- 4. stats scan animation (rev-3 layout: tag below image, stats, plan line, teaser body) ----
FPS = 30000 / 1001
DUR = 4.64
N = int(DUR * FPS)
after = Image.open("assets_v1/sample_after.jpg").convert("RGB")
scr_w, scr_h = 570, 1080
img_h = 430
img_w = int(after.width * img_h / after.height)
img_x = (scr_w - img_w) // 2
img_y = 22
after = after.resize((img_w, img_h), Image.LANCZOS)
fL = ImageFont.truetype(pa.MANROPE, 24)
fV = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
fB = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
fT = ImageFont.truetype(pa.MANROPE, 20)
STATS = [
    ("Current Weight", "205 lb"),
    ("Current Body Fat", "29%"),
    ("Goal Weight", "180 lb"),
    ("Goal Body Fat", "15%"),
    ("Goal Fat Loss", "28 lb"),
    ("Goal Muscle Gain", "+3 lb"),
]
BODY = ("Here’s what we saw: you’re starting near 29% body fat with a solid "
"muscle base underneath. To hit your goal you’ll drop 28 lb of fat while adding "
"lean muscle — a high-protein diet plus progressive strength training, 3–4 "
"days a week. Your week-by-week workout program is built for exactly this — "
"every session, every set, mapped to your goal…")
# wrap body text to the screen width
tmp = ImageDraw.Draw(Image.new("RGB",(10,10)))
words_b = BODY.split(); lines_b=[]; cur=""
for wd in words_b:
    t2=(cur+" "+wd).strip()
    if tmp.textlength(t2,font=fT) > scr_w-88: lines_b.append(cur); cur=wd
    else: cur=t2
if cur: lines_b.append(cur)
tagS = Image.open("assets_v1/tag.png").convert("RGBA")
tagS = tagS.resize((int(tagS.width * 0.72), int(tagS.height * 0.72)))
bg_full = pa.panel_bg(1)

os.makedirs("statsframes", exist_ok=True)
SCAN_END = 1.6
ROW_T0, ROW_DT = 1.75, 0.26
BOT_T = 3.45
for i in range(N):
    t = i / FPS
    scr = Image.new("RGB", (scr_w, scr_h), (250, 250, 252))
    scr.paste(after, (img_x, img_y))
    d = ImageDraw.Draw(scr, "RGBA")
    d.rectangle([img_x - 1, img_y - 1, img_x + img_w, img_y + img_h], outline=(210, 210, 215), width=1)
    if t < SCAN_END:
        yy = img_y + int((t / SCAN_END) * img_h)
        d.rectangle([img_x, img_y, img_x + img_w, yy], fill=(120, 180, 255, 46))
        d.rectangle([img_x, yy - 3, img_x + img_w, yy + 3], fill=(70, 140, 255, 230))
        d.rectangle([img_x, yy - 14, img_x + img_w, yy - 3], fill=(120, 180, 255, 90))
    y = 512
    for r, (lab, val) in enumerate(STATS):
        if t >= ROW_T0 + r * ROW_DT:
            a = min(1.0, (t - (ROW_T0 + r * ROW_DT)) / 0.22)
            col = (40, 40, 46, int(255 * a)); colv = (20, 60, 200, int(255 * a))
            d.text((44, y), lab, font=fL, fill=col)
            vw = d.textlength(val, font=fV)
            d.text((scr_w - 44 - vw, y), val, font=fV, fill=colv)
            if a >= 1:
                d.line([44, y + 36, scr_w - 44, y + 36], fill=(228, 228, 232, 255), width=1)
        y += 46
    if t >= BOT_T:
        a = min(1.0, (t - BOT_T) / 0.25)
        bt = "Recommended Workout Plan"
        bw = d.textlength(bt, font=fB)
        d.text(((scr_w - bw) / 2, 800), bt, font=fB, fill=(15, 15, 20, int(255 * a)))
        ty = 852
        for ln in lines_b:
            if ty > 952: break
            d.text((44, ty), ln, font=fT, fill=(96, 96, 104, int(255 * a)))
            ty += 26
    frame = bg_full.copy()
    frame.paste(scr, ((W - scr_w) // 2, 0))
    frame.paste(tagS, (W // 2 - tagS.width // 2, img_y + img_h + 8), tagS)  # tag BELOW the picture
    frame.save("statsframes/f%04d.png" % i)

subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-framerate", "30000/1001",
    "-i", "statsframes/f%04d.png", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-pix_fmt", "yuv420p", "assets_v1/stats_scan.mp4"], check=True)
print("rev3 stats screen done, frames:", N)
