#!/usr/bin/env python3
"""rev5 -- render every animated graphic to an alpha MOV.

Design system: Muhammad's screen STRUCTURE (Dan preferred it, 2026-08-22) in the paid-ad
palette from his 2026-08-23 revision doc -- BLACK field, olive/dark-green headers, WHITE
body copy, i.e. the YouTube Shorts cover system he pointed at. That is `motionlib.J2AD`.

Every element animates (lesson 19). Alpha rides on QTRLE MOV -- libx264 has no alpha.

  python3 gfx5.py          # everything (slow, cached on disk -- skips what exists)
  python3 gfx5.py NAME ... # just those
"""
import importlib.util, os, sys
from PIL import Image, ImageDraw

SK = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec = importlib.util.spec_from_file_location("ml", f"{SK}/motionlib.py")
ml = importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats5 as B

PAL = ml.J2AD
A   = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
WORK = "/Volumes/Extreme/_edit_work/ad1-8-14"
AV  = f"{WORK}/assets_v1"
AS  = "assets"
G   = "gfx"
os.makedirs(G, exist_ok=True)

# Dan's revision, item 0:11 -- the "where I'm at today" beat uses these four shoot
# photos, not the ab-workout b-roll and not video frames.
TODAY_SHOTS = [f"{AS}/shoot04_trees.jpg", f"{AS}/shoot05_flag.jpg"]
LOOK_SHOTS  = [f"{AS}/shoot07_standing.jpg", f"{AS}/shoot06_towel.jpg"]
GOAL   = f"{A}/Media/example pictures/dan by pool.png"
BEFORE = f"{AV}/p_before.jpg"

PHOTO_RECT = (161, 217, 396, 547)      # the print taped to the door, measured on level A

tag_f  = ml.font(30, "ExtraBold")
cap_f  = ml.font(44, "Bold")
pop_f  = ml.font(104, "ExtraBold")

def _tag(im, xy, text="AI-GENERATED", f=None):
    ml.chip(im, xy, text, f or tag_f, (10, 12, 8, 240), (255, 255, 255, 255), radius=8)

def _skip(name):
    p = f"{G}/{name}.mov"
    if os.path.exists(p) and os.environ.get("FORCE") != "1":
        print(f"  [cached] {name}"); return True
    return False

# ------------------------------------------------------------------ builders
def g_callout():
    if _skip("callout"): return
    ml.callout_box(f"{G}/callout.mov", PHOTO_RECT, B.CALLOUT[1] - B.CALLOUT[0],
                   draw_dur=0.55, delay=0.20, label="THIS PICTURE")

def g_gen():
    """'I generated this picture with AI' -> 'back when I was 200 pounds'.

    The two photos are SEQUENCED, never both on screen. Holding a before and an after
    together is the banned pattern and Dan's #1 compliance rule.
    """
    if _skip("gen"): return
    goal, before = Image.open(GOAL).convert("RGB"), Image.open(BEFORE).convert("RGB")
    def layer(img, caption, tag):
        lay, box = ml.photo_on_field(img, 1120, 800, centre=(960, 452))
        if caption:
            ImageDraw.Draw(lay).text((960, box[3] + 54), caption, font=cap_f,
                                     fill=PAL.ink, anchor="mm")
        if tag: _tag(lay, (box[0] + 26, box[1] + 26))
        return lay
    gl, bl = layer(goal, "The picture I generated", "AI-GENERATED"), layer(before, None, None)
    dur = B.GEN[1] - B.GEN[0]
    swap = round(dur * 0.62, 3)
    def build(im, t):
        im.alpha_composite(gl if t < swap else bl)
        if t >= swap:
            ml.pop_text(im, t - swap - 0.45, "200 pounds", pop_f, (960, 962),
                        color=PAL.ink, accent=PAL.hot)
    ml.card_in(f"{G}/gen.mov", dur, build, pal=PAL)

def g_phone():
    if _skip("phone"): return
    goal = Image.open(GOAL).convert("RGB")
    PW, PH, PAD = 470, 950, 14
    px, py = (ml.W - PW)//2, (ml.H - PH)//2 + 18
    scr = ml.fit_cover(goal, PW - PAD*2, PH - PAD*2)
    m = Image.new("L", scr.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, scr.width-1, scr.height-1], radius=44, fill=255)
    def build(im, t):
        im.alpha_composite(ml.drop_shadow(im.size, [px, py, px+PW, py+PH], 60,
                                          blur=34, spread=12, opacity=150))
        d = ImageDraw.Draw(im)
        # olive hairline: a near-black phone on a near-black field has no edge otherwise
        d.rounded_rectangle([px-9, py-9, px+PW+8, py+PH+8], radius=68, fill=PAL.accent)
        d.rounded_rectangle([px-6, py-6, px+PW+5, py+PH+5], radius=66, fill=(20, 22, 18))
        d.rounded_rectangle([px, py, px+PW, py+PH], radius=58, fill=(6, 6, 8))
        im.paste(scr, (px+PAD, py+PAD), m)
        _tag(im, (px, py - 88))
    ml.card_in(f"{G}/phone.mov", B.PHONE[1] - B.PHONE[0], build, pal=PAL)

def g_today():
    """Dan's revision 0:11 -- four shoot photos, in sequence, on the field."""
    if _skip("today"): return
    dur = B.TODAY[1] - B.TODAY[0]
    n = len(TODAY_SHOTS)
    step = dur / n
    items = [(round(i*step, 3), round((i+1)*step, 3), Image.open(p), None, None)
             for i, p in enumerate(TODAY_SHOTS)]
    ml.photo_sequence(f"{G}/today.mov", items, dur, pal=PAL,
                      maxw=1560, maxh=930, in_dur=0.26)

def g_look():
    """The remaining two of Dan's four shoot photos, on the line about how he looks now."""
    if _skip("look"): return
    dur = B.LOOKNOW[1] - B.LOOKNOW[0]
    half = round(dur / 2, 3)
    ml.photo_sequence(f"{G}/look.mov",
                      [(0.0, half, Image.open(LOOK_SHOTS[0]), None, None),
                       (half, dur, Image.open(LOOK_SHOTS[1]), None, None)],
                      dur, pal=PAL, maxw=1500, maxh=940, in_dur=0.26)

def g_bullets():
    """Dan's revision 0:14: header large dark green ALL CAPS, body white, background black,
    even spacing between all three points, and the stray backtick typo gone."""
    if _skip("bullets"): return
    b0 = B.BULLETS[0]
    ml.bullets_build(
        f"{G}/bullets.mov", "In today's episode",
        [(round(B.at("how I got limitless") - b0, 3),
          "How I got limitless motivation to work out and to eat healthy."),
         (round(B.at("what I needed to do") - b0, 3),
          "What I needed to do to lose my belly fat and get six-pack abs."),
         (round(B.at("how you can generate") - b0, 3),
          "How you can generate a goal picture of yourself with abs for free.")],
        B.BULLETS[1] - b0, panel_w=980, pal=PAL, head_color=PAL.accent)

def g_lower3():
    """Dan's revision 0:39 -- green bar left, white text on black."""
    if _skip("lower3"): return
    ml.lower_third_bar(f"{G}/lower3.mov", ["The problem", "No time. No motivation."],
                       B.LOWER3[1] - B.LOWER3[0], pal=PAL, size=40, lead_size=44)

def g_title():
    """Dan's revision 0:45 -- all white text, green highlight box, black background."""
    if _skip("title"): return
    ml.title_card(f"{G}/title.mov", "Visualizing\nYour Goal",
                  "One of the most powerful ways to motivate yourself",
                  B.TITLE[1] - B.TITLE[0], pal=PAL,
                  band=PAL.deep, band_ink=(255, 255, 255))

def g_lower3b():
    """Dan's revision 1:37 -- retexted, green bar, white on black."""
    if _skip("lower3b"): return
    ml.lower_third_bar(f"{G}/lower3b.mov",
                       ["If you saw yourself with abs, you'd be MOTIVATED",
                        "to make your dream body a reality."],
                       B.LOWER3B[1] - B.LOWER3B[0], pal=PAL, size=40, lead_size=44)

def g_lower3c():
    """The contrast beat. Restyled per the revision; the bar stays RED because this is the
    one 'stop and read this' moment in the ad and red is the reserved attention colour."""
    if _skip("lower3c"): return
    ml.lower_third_bar(f"{G}/lower3c.mov",
                       ["You don't need more knowledge",
                        "You need the motivation to execute what you already know"],
                       B.LOWER3C[1] - B.LOWER3C[0], pal=PAL, size=38, lead_size=46,
                       bar_color=PAL.hot)

def g_free():
    """Dan's revision 1:34 -- the free-offer panel, same treatment as the opening bullets."""
    if _skip("free"): return
    f0 = B.FREECARD[0]
    ml.bullets_build(f"{G}/free.mov", "Right now, free",
                     [(0.35, "You can generate an AI image of yourself with ripped six-pack abs."),
                      (round(B.at("completely free") - f0, 3), "Completely free.")],
                     B.FREECARD[1] - f0, panel_w=980, pal=PAL, head_color=PAL.accent)

def _cta_card(out, dur, headline, sub):
    """Dan's revision 1:38 -- white text on a DARK GREEN background (not the black field)."""
    fH, fS = ml.font(104, "ExtraBold"), ml.font(54, "Medium")
    lines = ml.wrap(headline, fH, 1480)
    subl  = ml.wrap(sub, fS, 1300) if sub else []
    LH, LHS = int(104 * 0.98), int(54 * 1.2)
    block = len(lines) * LH + (46 + len(subl) * LHS if subl else 0)
    top = (ml.H - block) // 2
    green = Image.new("RGBA", (ml.W, ml.H), PAL.deep + (255,))
    def build(im, t):
        im.alpha_composite(green)
        d = ImageDraw.Draw(im)
        y = top
        for i, l in enumerate(lines):
            p = ml.ease_out_cubic((t - 0.14 - i * 0.10) / 0.42)
            if p <= 0.01: y += LH; continue
            lay = Image.new("RGBA", (ml.W, ml.H), (0, 0, 0, 0))
            w, _ = ml.text_size(l, fH)
            ImageDraw.Draw(lay).text(((ml.W - w) / 2, y + (1 - p) * 18), l, font=fH,
                                     fill=(255, 255, 255), anchor="lt")
            im.alpha_composite(ml.with_alpha(lay, p)); y += LH
        if subl:
            y += 46
            for i, l in enumerate(subl):
                p = ml.ease_out_cubic((t - 0.55 - i * 0.09) / 0.4)
                if p <= 0.01: y += LHS; continue
                lay = Image.new("RGBA", (ml.W, ml.H), (0, 0, 0, 0))
                w, _ = ml.text_size(l, fS)
                ImageDraw.Draw(lay).text(((ml.W - w) / 2, y), l, font=fS,
                                         fill=(226, 234, 210), anchor="lt")
                im.alpha_composite(ml.with_alpha(lay, p)); y += LHS
    ml.card_in(out, dur, build, pal=PAL)

def g_cta1():
    if _skip("cta1"): return
    _cta_card(f"{G}/cta1.mov", B.CTA1[1] - B.CTA1[0],
              "Get a FREE AI image of yourself with abs", "Tap the button below")

def g_cta2():
    if _skip("cta2"): return
    _cta_card(f"{G}/cta2.mov", B.CTA2[1] - B.CTA2[0],
              "Get a FREE AI image of yourself with abs", "Tap the button below")

def g_before1():
    """Dan's revision 2:06 -- his actual 200 lb before picture."""
    if _skip("before1"): return
    dur = B.BEFORE1[1] - B.BEFORE1[0]
    ml.photo_sequence(f"{G}/before1.mov",
                      # no caption: the same photo already carried "200 POUNDS" at 0:05,
                      # and repeating the number reads as a mistake rather than a callback
                      [(0.0, dur, Image.open(f"{AS}/dan_before_200lb.jpg"), None, None)],
                      dur, pal=PAL, maxw=1000, maxh=900, in_dur=0.30)

def g_fatdad():
    """Dan's revision 2:11-2:17 -- the 'fat dad' pictures of him."""
    if _skip("fatdad"): return
    dur = B.FATDAD[1] - B.FATDAD[0]
    half = round(dur / 2, 3)
    ml.photo_sequence(f"{G}/fatdad.mov",
                      [(0.0, half, Image.open(f"{AS}/fatdad_standing.jpg"), None, None),
                       (half, dur, Image.open(f"{AS}/fatdad_ride.jpg"), None, None)],
                      dur, pal=PAL, maxw=1460, maxh=920, in_dur=0.26)

def g_afterpic():
    """Dan's revision 2:18 -- eliminate the man-looking-at-his-phone picture. This becomes a
    FULL-SCREEN graphic of the AI after picture ALONE, with the disclosure, in brand colour."""
    if _skip("afterpic"): return
    dur = B.AFTERPIC[1] - B.AFTERPIC[0]
    goal = Image.open(GOAL).convert("RGB")
    lay, box = ml.photo_on_field(goal, 980, 880, centre=(960, 452))
    _tag(lay, (box[0], box[3] + 30))
    ImageDraw.Draw(lay).text((960, box[3] + 150), "The picture that changed everything",
                             font=cap_f, fill=PAL.ink_soft, anchor="mm")
    ml.card_in(f"{G}/afterpic.mov", dur, lambda im, t: im.alpha_composite(lay), pal=PAL)

def g_planbul():
    if _skip("planbul"): return
    p0 = B.PLANBUL[0]
    ml.bullets_build(f"{G}/planbul.mov", "Your workout plan",
                     [(round(B.at("works around your injuries") - p0, 3), "Works around your injuries."),
                      (round(B.at("It targets your lagging") - p0, 3), "Targets your lagging body parts."),
                      (round(B.at("And it uses a specific equipment") - p0, 3),
                       "Uses the equipment you actually have.")],
                     B.PLANBUL[1] - p0, panel_w=980, pal=PAL, head_color=PAL.accent)

def g_superior():
    if _skip("superior"): return
    ml.title_card(f"{G}/superior.mov", "Built for\nmen like you",
                  "Not a general-purpose AI — trained on one job",
                  B.SUPERIOR[1] - B.SUPERIOR[0], pal=PAL,
                  band=PAL.deep, band_ink=(255, 255, 255), size=118, sub_size=56)

def g_step1():
    if _skip("step1"): return
    ml.number_pop(f"{G}/step1.mov", "The picture is just step one",
                  B.STEP1[1] - B.STEP1[0], size=78, pal=PAL)

def g_plates():
    """Static plates + tags: a video panel gets rounded corners from a PLATE, not a mask.

    The plate also carries an olive hairline round the hole. panel_plate bakes a drop
    shadow, but a shadow on a (13,14,11) field is invisible, so a white app screenshot
    sat on black with no edge at all and read as an unfinished floating rectangle.
    """
    def plate(box, radius=30):
        im = ml.panel_plate(box, radius=radius, pal=PAL)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([box[0]-4, box[1]-4, box[2]+3, box[3]+3], radius=radius+4,
                            outline=PAL.accent + (255,), width=4)
        return im
    plate([610, 40, 1310, 1040]).save(f"{G}/plate_phone.png")
    plate([700, 30, 1220, 1050]).save(f"{G}/plate_app.png")
    t = Image.new("RGBA", (ml.W, ml.H), (0, 0, 0, 0)); _tag(t, (0, 0))
    t.crop(t.getbbox()).save(f"{G}/tag.png")
    tb = Image.new("RGBA", (ml.W, ml.H), (0, 0, 0, 0))
    ml.chip(tb, (0, 0), "AI-GENERATED", ml.font(45, "ExtraBold"),
            (10, 12, 8, 240), (255, 255, 255, 255), radius=10)
    tb.crop(tb.getbbox()).save(f"{G}/tag_big.png")
    print("  plates + tags")

BUILDERS = {n[2:]: f for n, f in sorted(globals().items()) if n.startswith("g_")}

if __name__ == "__main__":
    for name in (sys.argv[1:] or list(BUILDERS)):
        print(name); BUILDERS[name]()
    print("gfx done")
