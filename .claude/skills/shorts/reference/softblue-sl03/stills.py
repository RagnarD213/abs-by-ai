#!/usr/bin/env python3
"""SL-03 round 1 stills: short 1's opener, crops, title, key points, cutaway, captions; the six title bands; short 5's phone layouts."""
import sys, json; sys.path.insert(0, '.')
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import lib, lt
B = lib.B; O = "round1/stills"
T1 = ("INTERMITTENT FASTING", ["BREAK YOUR FAST", "WITH THIS"])
TITLES = {1: T1, 2: ("MEAL PREP", ["THE $20 SALAD YOU", "CAN MAKE FOR $4"]), 3: ("MEAL PREP", ["KEEP YOUR SALADS", "FRESH FOR 7 DAYS"]),
          4: ("DAILY SALAD", ["STOP BUYING", "SALAD DRESSING"]), 5: ("AI MACRO TRACKING", ["TRACK A WEEK OF", "MEALS FROM 1 PHOTO"]),
          6: ("AI CALORIE TRACKING", ["THE ONE LINE THAT", "MAKES IT ACCURATE"])}
def base(fn):
    bg = lib.canvas(); fn(bg); lib.band(bg, *T1); return bg
def fin(im, cap, name, top=None):
    if cap: lib.caption(im, cap, **({'top': top} if top else {}))
    lib.wordmark(im); lib.save(im, f"{O}/{name}")
which = sys.argv[1:] or ['O1', 'L1', 'L2', 'L3', 'G1', 'C2', 'G2', 'T', 'HAIR']
# O1 opener: the finished salad, centre square (bowl is 1,120 px wide at this moment; a 724 px fill window cuts it)
if 'O1' in which:
    fin(base(lambda bg: lib.square(bg, "C1550", 116.3, 150)), ["let's talk about why"], "O1")
    bg = lib.canvas(); lib.talk(bg, "C1550", 116.3, 660); lib.band(bg, *T1); fin(bg, ["let's talk about why"], "O1_fill")
if 'L1' in which: fin(base(lambda bg: lib.talk(bg, "C1536", 6.28, 980)), ["my most important", "fitness habit."], "L1")
if 'L2' in which: fin(base(lambda bg: lib.talk(bg, "C1536", 13.44, 1000, 604, 900)), ["fasting until", "about 2pm"], "L2")
if 'L3' in which: fin(base(lambda bg: lib.talk(bg, "C1536", 138.10, 1075)), ["start doing what", "I'm doing"], "L3", top=1500)
if 'G1' in which:
    im, m = lt.still(base(lambda bg: lib.talk(bg, "C1536", 27.92, 1000)), "G1", "KEY POINT", [["Break Your Fast With CARBS", 48.50], ["And Fasting Barely Works", 53.30]], 47.9, 55.4, "round1/hf")
    print('G1', m); fin(im, ["anywhere near as", "effective."], "G1")
if 'C2' in which:
    im, m = lt.still(base(lambda bg: lib.square(bg, "C1550", 113.2, 230)), "G2a", "KEY POINT", [["A LOW-CARB First Meal", 58.30], ["Means Far More FAT LOSS", 62.40]], 56.6, 65.3, "round1/hf", at=3.6)
    fin(im, ["like this salad", "for example,"], "C2_square")
    im, m = lt.still(base(lambda bg: lib.talk(bg, "C1550", 113.2, 800)), "G2a", "KEY POINT", [["A LOW-CARB First Meal", 58.30], ["Means Far More FAT LOSS", 62.40]], 56.6, 65.3, "round1/hf", at=3.6)
    fin(im, ["like this salad", "for example,"], "C2")
if 'G2' in which:
    im, m = lt.still(base(lambda bg: lib.talk(bg, "C1536", 37.42, 1000)), "G2", "KEY POINT", [["A LOW-CARB First Meal", 58.30], ["Means Far More FAT LOSS", 62.40]], 56.6, 65.3, "round1/hf")
    print('G2', m); fin(im, ["effective for", "fat loss"], "G2")
if 'T' in which:
    for k, (e, l) in TITLES.items():
        bg = lib.canvas(); sz = lib.band(bg, e, l); bg.crop((0, 0, 1080, 312)).save(f"{O}/T{k}.jpg", quality=92); print('title', k, sz)
if 'HAIR' in which:
    rows = []
    for roll, t in (("C1536", 6.25), ("C1536", 17.0), ("C1536", 30.2), ("C1536", 138.92)):
        im = lib.raw(roll, t).resize((960, 540)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 959, 3), fill=(255, 60, 60)); d.text((12, 500), f"{roll} raw {t:.2f} s: the whole camera frame", font=B.font(24), fill=(255, 255, 0)); rows.append(im)
    sh = Image.new("RGB", (1920, 1080)); [sh.paste(im, ((i % 2) * 960, (i // 2) * 540)) for i, im in enumerate(rows)]; sh.save(f"{O}/HAIR.jpg", quality=88)

# ---- short 5: the phone layouts (new). Film 766.0 = C1541 raw 62.66, screen recording 38.24 s
def phone_png(cam_t, scale):
    """The approved RO-05 iPhone shell (build_r2.iphone), drawn alone on transparency and scaled."""
    S = B
    im = Image.new('RGBA', (660, 1090), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def rr(box, fill, r, outline=None, width=1): d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)
    sh = Image.new('RGBA', im.size); ImageDraw.Draw(sh).rounded_rectangle((91, 34, 573, 1062), 68, fill=(0, 0, 0, 120)); im = sh.filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(im)
    rr((90, 28, 562, 1052), (95, 107, 119), 66, (166, 179, 190), 2); rr((95, 33, 557, 1047), (5, 8, 12), 62)
    scr = Image.new('RGB', (448, 1000), (248, 250, 252)); p = ImageOps.contain(lib.screen(cam_t), (432, 920), Image.Resampling.LANCZOS)
    scr.paste(p, ((448 - p.width)//2, 65)); e = ImageDraw.Draw(scr); e.text((30, 14), '9:41', font=S.font(17), fill=(23, 43, 59))
    for i in range(4): e.rounded_rectangle((352+i*6, 30-i*3, 355+i*6, 35), 1, fill=(25, 32, 40))
    e.rounded_rectangle((391, 22, 418, 34), 3, outline=(25, 32, 40), width=2); e.rectangle((419, 26, 422, 30), fill=(25, 32, 40)); e.rectangle((394, 25, 413, 31), fill=(25, 32, 40))
    e.rounded_rectangle((146, 15, 302, 51), 18, fill=(0, 0, 0)); e.ellipse((276, 26, 288, 38), fill=(18, 26, 36)); e.ellipse((280, 29, 284, 33), fill=(34, 60, 82)); e.rounded_rectangle((153, 984, 295, 989), 3, fill=(24, 28, 32))
    m = Image.new('L', (448, 1000)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 447, 999), 54, fill=255); im.paste(scr, (102, 40), m)
    rr((86, 202, 90, 258), (69, 81, 94), 2); rr((86, 283, 90, 354), (69, 81, 94), 2); rr((562, 253, 566, 352), (86, 96, 110), 2)
    im = im.crop((70, 10, 590, 1085))                                    # shell 472x1024 at (20,18)
    return im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
def rounded(im, r=28):
    m = Image.new('L', im.size); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255); return m
if 'P' in which:
    cam = lib.raw("C1541", 62.66); T5 = TITLES[5]
    import json as _j
    # where Dan is in the camera frame at this moment
    # A: phone on top, Dan in a wide strip under it
    bg = lib.canvas(); lib.band(bg, *T5)
    ph = phone_png(62.66, 1.0); bg.paste(ph, ((1080 - ph.width)//2, 318), ph)
    st = cam.crop((600, 60, 600 + 1300, 60 + 620)).resize((1080, 515), Image.LANCZOS); bg.paste(st, (0, 1405))
    ImageDraw.Draw(bg).line((0, 1404, 1080, 1404), fill=B.GLASS_LINE, width=2)
    lib.caption(bg, ["I then add photos"], top=1650, size=80); lib.wordmark(bg, (64, 1850)); lib.save(bg, f"{O}/P5_A")
    # B: phone and Dan side by side, both tall; captions on the field under them
    bg = lib.canvas(); lib.band(bg, *T5)
    ph = phone_png(62.66, 1.2); bg.paste(ph, (14, 322), ph)
    dw, dh = 440, 1190; sw = round(1080 * dw / dh)
    dn = lib.window(cam, 1130, sw, 1080).resize((dw, dh), Image.LANCZOS); bg.paste(dn, (612, 345), rounded(dn))
    lib.caption(bg, ["I then add photos", "of my batch"], top=1600, size=86); lib.wordmark(bg, (64, 1850)); lib.save(bg, f"{O}/P5_B")
    # C: phone as large as the frame allows, Dan as a small inset
    bg = lib.canvas(); lib.band(bg, *T5)
    ph = phone_png(62.66, 1.42); bg.paste(ph, (-10, 318), ph)
    dw, dh = 350, 620; sw = round(1080 * dw / dh)
    dn = lib.window(cam, 1310, sw, 1080).resize((dw, dh), Image.LANCZOS); bg.paste(dn, (706, 345), rounded(dn))
    lib.caption(bg, ["I then add", "photos"], top=1020, size=64); lib.save(bg, f"{O}/P5_C")
