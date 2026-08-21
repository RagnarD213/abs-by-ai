#!/usr/bin/env python3
"""Modern-edit 60s sample -- graphics build + layout over tight60.mov.

Beat sheet mirrors the Upwork trial edit's placements in Abs By AI CONTENT style
(bright paper, near-black ink, brand red) rather than its pastel-cyan template look.
Every animated element comes from motionlib; this file only composes.

  python3 modern60.py gfx     # render the animated graphics (slow, cached on disk)
  python3 modern60.py cut     # punch/layout pass  -> punched_modern.mp4
  python3 modern60.py mix     # overlay pass       -> modern_nocap.mp4
"""
import importlib.util, json, os, subprocess, sys

SKILL = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec = importlib.util.spec_from_file_location("ml", f"{SKILL}/motionlib.py")
ml = importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
from PIL import Image, ImageDraw

FF   = ml.FF
A    = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
CLIPS = f"{A}/Media/ad-assets/batch1-ads/clips"
GOAL   = f"{A}/Media/example pictures/dan by pool.png"
BEFORE = f"{A}/Media/ad-assets/ad2-nutritionist/full/03_before_picture.png"
BROLL  = f"{CLIPS}/broll-dan-training-abs.mp4"
CRUDE  = f"{CLIPS}/ai-clip-crude-photoshop.mp4"
G      = "gfx"
FPS    = "30000/1001"
os.makedirs(G, exist_ok=True)

# ---------------------------------------------------------------- beat sheet (tight60 time)
CALLOUT   = (0.00,  3.30)     # "This picture got me abs and it's not even real."
GEN       = (3.62,  7.82)     # "I generated this picture with AI back when I was 200 pounds."
PHONE     = (7.86,  9.72)     # "I made it my phone lock screen"
TODAY     = (12.74, 14.79)    # "And this is where I'm at today."
BULLETS   = (14.79, 29.49)    # "In today's episode ... for free."
LOWER3    = (39.97, 46.30)    # "The problem is that finding that motivation is really hard"
TITLE     = (47.05, 50.60)    # "Visualizing your goal is one of the most powerful ways..."
SHOP      = (59.02, 63.62)    # "Some of them would literally Photoshop their own face..."

PHOTO_RECT = (161, 217, 396, 547)      # the print taped to the door, measured on level A
BULLET_TIMES = (17.21, 20.90, 25.40)   # "how I got limitless" / "what I needed" / "how you can"

# punch levels over the tight cut. 'P*' are the bullets-panel layouts (video pushed right).
PANEL_W = 886
PUNCH = [
    (0.00,  3.30, "A"),      # callout is measured in level-A coordinates -- do not punch
    (3.30,  7.86, "B"),
    (7.86, 11.78, "A"),
    (11.78, 14.79, "C"),
    (14.79, 16.02, "P1"),
    (16.02, 19.49, "P2"),
    (19.49, 24.56, "P1"),
    (24.56, 29.49, "P2"),
    (29.49, 31.10, "A"),
    (31.10, 36.14, "B"),
    (36.14, 39.97, "A"),
    (39.97, 47.05, "C"),
    (47.05, 54.32, "A"),
    (54.32, 55.72, "B"),
    (55.72, 63.62, "A"),
    (63.62, None,  "B"),
]
CROP = {
    "A":  "",
    "B":  "crop=1574:886:198:54,scale=1920:1080:flags=lanczos,",
    "C":  "crop=1730:973:104:40,scale=1920:1080:flags=lanczos,",
    "P1": f"crop=1034:1080:435:0,pad=1920:1080:{PANEL_W}:0:black,",
    "P2": f"crop=880:919:504:80,scale=1034:1080:flags=lanczos,pad=1920:1080:{PANEL_W}:0:black,",
}

# ---------------------------------------------------------------- graphics
def build_gfx():
    tag_f  = ml.font(30, "ExtraBold")
    cap_f  = ml.font(40, "Bold")
    pop_f  = ml.font(96, "ExtraBold")

    ml.callout_box(f"{G}/callout.mov", PHOTO_RECT, CALLOUT[1] - CALLOUT[0],
                   draw_dur=0.55, delay=0.20, label="THIS PICTURE")

    # --- "I generated this picture with AI" -> "back when I was 200 pounds"
    # The two photos are SEQUENCED, never both on screen: holding a before and an after
    # together is the banned pattern, and building it into the sample would put it in
    # the library for every future ad.
    goal   = Image.open(GOAL).convert("RGB")
    before = Image.open(BEFORE).convert("RGB")
    CB = [630, 70, 1290, 890]
    goal_p   = ml.rounded_photo(goal,   CB[2]-CB[0]-36, CB[3]-CB[1]-36-56, radius=18)
    before_p = ml.rounded_photo(before, CB[2]-CB[0]-36, CB[3]-CB[1]-36-56, radius=18)
    SWAP = 2.48
    def gen_build(im, t):
        ml.card(im, CB, radius=26)
        first = t < SWAP
        im.alpha_composite(before_p if not first else goal_p, (CB[0]+18, CB[1]+18))
        cap = "The picture I generated" if first else "Me, back then"
        ImageDraw.Draw(im).text(((CB[0]+CB[2])//2, CB[3]-40), cap, font=cap_f,
                                fill=ml.INK, anchor="mm")
        if first:
            ml.chip(im, (CB[0]+30, CB[1]+30), "AI-GENERATED", tag_f,
                    (12, 14, 18, 235), (255, 255, 255, 255), radius=8)
        else:
            ml.pop_text(im, t - 3.00, "200 pounds", pop_f, (960, 975))
    ml.card_in(f"{G}/gen.mov", GEN[1] - GEN[0], gen_build)

    # --- "I made it my phone lock screen"
    PH_W, PH_H, PAD = 470, 950, 14
    px, py = (ml.W - PH_W)//2, (ml.H - PH_H)//2 + 18
    scr = ml.fit_cover(goal, PH_W - PAD*2, PH_H - PAD*2)
    scr_m = Image.new("L", scr.size, 0)
    ImageDraw.Draw(scr_m).rounded_rectangle([0, 0, scr.width-1, scr.height-1], radius=44, fill=255)
    def phone_build(im, t):
        im.alpha_composite(ml.drop_shadow(im.size, [px, py, px+PH_W, py+PH_H], 60,
                                          blur=32, spread=10, opacity=70))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([px-7, py-7, px+PH_W+6, py+PH_H+6], radius=66, fill=(28, 31, 38))
        d.rounded_rectangle([px, py, px+PH_W, py+PH_H], radius=58, fill=(6, 6, 8))
        im.paste(scr, (px+PAD, py+PAD), scr_m)
        ml.chip(im, (px, py - 88), "AI-GENERATED", tag_f, (12, 14, 18, 235),
                (255, 255, 255, 255), radius=8)
    ml.card_in(f"{G}/phone.mov", PHONE[1] - PHONE[0], phone_build)

    # --- video cards: paper plate with a rounded window the clip shows through
    ml.panel_plate([510, 90, 1410, 990]).save(f"{G}/plate_today.png")
    ml.panel_plate([610, 40, 1310, 1040]).save(f"{G}/plate_shop.png")
    tag = Image.new("RGBA", (ml.W, ml.H), (0, 0, 0, 0))
    ml.chip(tag, (0, 0), "AI-GENERATED", tag_f, (12, 14, 18, 235), (255, 255, 255, 255), radius=8)
    tag.crop(tag.getbbox()).save(f"{G}/tag.png")

    ml.bullets_build(f"{G}/bullets.mov", "In this video",
                     [(BULLET_TIMES[0] - BULLETS[0], "How I got limitless motivation to work out and eat healthy"),
                      (BULLET_TIMES[1] - BULLETS[0], "What I needed to do to lose my belly fat and get six-pack abs"),
                      (BULLET_TIMES[2] - BULLETS[0], "How to generate a goal picture of yourself with abs — free")],
                     BULLETS[1] - BULLETS[0], panel_w=PANEL_W)

    ml.lower_third(f"{G}/lower3.mov", "The Problem", "No time. No motivation.",
                   LOWER3[1] - LOWER3[0])

    ml.title_card(f"{G}/title.mov", "Visualizing\nYour Goal",
                  "One of the most powerful ways to motivate yourself", TITLE[1] - TITLE[0])
    print("graphics done")

# ---------------------------------------------------------------- pass 1: punch / layout
def cut():
    dur = float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error",
                                "-show_entries", "format=duration", "-of", "csv=p=0",
                                "tight60.mov"], capture_output=True, text=True).stdout.strip())
    parts, cat = [], ""
    for i, (a, b, lvl) in enumerate(PUNCH):
        b = dur if b is None else b
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,{CROP[lvl]}setsar=1[v{i}]")
        cat += f"[v{i}]"
    fc = ";".join(parts) + f";{cat}concat=n={len(PUNCH)}:v=1:a=0[vout]"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", "tight60.mov",
                    "-filter_complex", fc, "-map", "[vout]", "-map", "0:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-r", FPS, "-c:a", "copy", "punched_modern.mov"], check=True)
    print("punched_modern.mov done")

# ---------------------------------------------------------------- pass 2: overlays
def mix():
    inp, fc, idx = ["-i", "punched_modern.mov"], [], 1
    cur = "[0:v]"

    def over(src, a, b, x=0, y=0, loop=False, pre=""):
        """Overlay `src` on the running chain for [a,b]. Returns nothing; mutates state."""
        nonlocal inp, fc, idx, cur
        if loop: inp += ["-loop", "1", "-t", str(round(b - a + 0.3, 3))]
        inp += ["-i", src]
        fc.append(f"[{idx}:v]{pre}setpts=PTS-STARTPTS+{a}/TB[g{idx}]")
        fc.append(f"{cur}[g{idx}]overlay={x}:{y}:enable='between(t,{a},{b})'[s{idx}]")
        cur = f"[s{idx}]"; idx += 1

    over(f"{G}/callout.mov", *CALLOUT)
    over(f"{G}/gen.mov",     *GEN)
    over(f"{G}/phone.mov",   *PHONE)

    # today b-roll: clip first (square corners), then the plate trims it to a card
    over(BROLL, *TODAY, x=510, y=90,
         pre="crop=1080:1080:0:820,scale=900:900:flags=lanczos,setsar=1,")
    over(f"{G}/plate_today.png", *TODAY, loop=True)

    over(f"{G}/bullets.mov", *BULLETS)
    over(f"{G}/lower3.mov",  *LOWER3)
    over(f"{G}/title.mov",   *TITLE)

    over(CRUDE, *SHOP, x=610, y=40,
         pre="crop=716:1023:0:100,scale=700:1000:flags=lanczos,setsar=1,")
    over(f"{G}/plate_shop.png", *SHOP, loop=True)
    over(f"{G}/tag.png", SHOP[0] + 0.15, SHOP[1], x=644, y=76, loop=True)

    fc[-1] = fc[-1].rsplit("[s", 1)[0] + "[vout]"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + inp +
                   ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "0:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-r", FPS, "-c:a", "copy", "modern_nocap.mov"], check=True)
    print("modern_nocap.mov done")

if __name__ == "__main__":
    for step in (sys.argv[1:] or ["gfx", "cut", "mix"]):
        {"gfx": build_gfx, "cut": cut, "mix": mix}[step]()
