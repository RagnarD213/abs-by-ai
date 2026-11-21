#!/usr/bin/env python3
"""Ad 13 round 2: the replacement media for Dan's round 1 revisions (P03, P06, P09-P11, P20, P22) and the opener's
START/END placeholders. Writes into B/assets_sbl/ (vertical kit) and B/round2/assets/ (16:9). No generation here."""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FF = PROJ + "/Media/video_edit/bin/ffmpeg"
B = "/Volumes/Extreme/_edit_work/kit9x16/av11-ad13"
A = B + "/assets_sbl"
R2 = B + "/round2/assets"
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
WV_FINAL = "/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A 1080p.mp4"
P07 = "/Volumes/Extreme/_edit_work/wv01-edit/round4/previews/P07-recipes.mp4"
YT = LIB + "/08 SixPackAbs Archive - CHECK BEFORE USING/3 min ab workout b roll.mp4"
A0060 = LIB + "/04 AI-Generated Clips/food-nutrition/A0060_man-one-bite-chicken-stomach-pain-kitchen_16x9_5s.mp4"
ENC = ["-r", "30000/1001", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p",
       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-an"]
YT_T0 = 8.0            # Dan centred, hands on hips, camera on him, Mike Chang at the side (before the workout starts)
YT_DUR = 8.2


def ff(*a):
    subprocess.run([FF, "-v", "error", "-y", *a], check=True)


def font(size, bold=True):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise SystemExit("no font")


def phones():
    ff("-ss", "26.02", "-t", "5.86", "-i", WV_FINAL, "-vf",
       "crop=478:1028:88:26,scale=956:2056:flags=lanczos,tpad=stop_mode=clone:stop_duration=1", *ENC, A + "/phone_workout_crunch.mp4")
    ff("-i", P07, "-filter_complex",
       "[0:v]trim=0.9:3.9,setpts=PTS-STARTPTS[a];[0:v]trim=5.6:9.0,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1,"
       "crop=478:1028:88:26,scale=956:2056:flags=lanczos,tpad=stop_mode=clone:stop_duration=1[v]", "-map", "[v]", *ENC,
       A + "/phone_recipes_two_taps.mp4")


def meal():
    # the centre square keeps the man and the whole plate (three-step rule: a fill would cut the plate)
    ff("-ss", "0.3", "-i", A0060, "-vf", "crop=1080:1080:420:0,tpad=stop_mode=clone:stop_duration=1", *ENC, A + "/bland_meal_sq.mp4")
    ff("-ss", "0.3", "-i", A0060, "-vf", "tpad=stop_mode=clone:stop_duration=1", *ENC, R2 + "/bland_meal_16x9.mp4")


def youtube():
    """The 4K recording of the real YouTube page. 16:9: the page itself (browser bars cropped off). 9:16: the same
    page re-laid in phone orientation from its own pixels: the player cropped square on Dan, the title, the channel row
    with the subscriber count, the views line."""
    ff("-ss", str(YT_T0), "-t", str(YT_DUR), "-i", YT, "-vf", "crop=3440:1935:0:225,scale=1920:1080:flags=lanczos", *ENC,
       R2 + "/yt3min_16x9.mp4")
    # page furniture, lifted once from a frame of the recording
    fr = R2 + "/_yt_frame.png"
    ff("-ss", str(YT_T0 + 1), "-i", YT, "-frames:v", "1", fr)
    im = Image.open(fr).convert("RGB")
    bg = im.getpixel((2400, 1960))
    page = Image.new("RGB", (1080, 1920), bg)
    logo = im.crop((136, 252, 352, 312)); logo = logo.resize((int(logo.width * 0.95), int(logo.height * 0.95)), Image.LANCZOS)
    page.paste(logo, (28, 40))
    d = ImageDraw.Draw(page)
    y = 150 + 1080 + 22
    f = font(46)
    for line in ("Crazy 3 Min Home Abs Workout - With", "Six Pack Shortcuts CEO Dan Rose"):
        d.text((36, y), line, font=f, fill=(241, 241, 241)); y += 58
    y = 1530                                                   # the caption band (about 1390-1500) stays empty
    d.text((36, y), "2.6M views   15 years ago", font=font(36, False), fill=(170, 170, 170)); y += 70
    chan = im.crop((28, 1944, 500, 2068)); chan = chan.resize((int(chan.width * 1.45), int(chan.height * 1.45)), Image.LANCZOS)
    page.paste(chan, (30, y))
    page.save(R2 + "/_yt_page_9x16.png")
    # the player: 2618x1470 at (32,360); a 1470 square with Dan in its centre
    ff("-ss", str(YT_T0), "-t", str(YT_DUR), "-i", YT, "-i", R2 + "/_yt_page_9x16.png", "-filter_complex",
       "[0:v]crop=1470:1470:40:360,scale=1080:1080:flags=lanczos[p];[1:v][p]overlay=0:150", *ENC, A + "/yt3min_9x16.mp4")


def placeholders():
    """START then END frame of the opener where the motion will go (VIDEO-RULES 'Future contextual previews')."""
    for asp, (w, h) in (("9x16", (1080, 1920)), ("16x9", (1920, 1080))):
        for which in ("start", "end"):
            im = Image.open(f"{B}/round2/opener/{which}_{asp}.png").convert("RGB").resize((w, h), Image.LANCZOS)
            d = ImageDraw.Draw(im, "RGBA")
            txt = f"PLACEHOLDER: {which.upper()} FRAME (motion not generated yet)"
            f = font(30 if asp == "9x16" else 34)
            tw = d.textlength(txt, font=f)
            x, y0 = (w - tw) / 2, 1560 if asp == "9x16" else 40      # 9:16: on the floor, clear of the label, lower third and captions
            d.rounded_rectangle((x - 18, y0 - 10, x + tw + 18, y0 + 46), 12, fill=(0, 0, 0, 170))
            d.text((x, y0), txt, font=f, fill=(255, 220, 90))
            out = (A if asp == "9x16" else R2) + f"/opener_{which}_{asp}_placeholder{'_v2' if asp == '9x16' else ''}.png"
            im.save(out)
            Image.open(f"{B}/round2/opener/{which}_{asp}.png").save(f"{B}/review2/frames/OPENER-{which}-{asp}.png")


if __name__ == "__main__":
    os.makedirs(R2, exist_ok=True); os.makedirs(B + "/review2/frames", exist_ok=True)
    for fn in (sys.argv[1:] or ["phones", "meal", "youtube", "placeholders"]):
        globals()[fn](); print("done", fn)
