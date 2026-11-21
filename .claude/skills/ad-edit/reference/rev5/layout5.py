#!/usr/bin/env python3
"""rev5 -- pass 1 punch/layout over tight_full.mov, pass 2 the overlays.

  python3 layout5.py punch    -> punched5.mov
  python3 layout5.py mix      -> rev5_nocap.mov

PUNCH RULE (lesson 21): every pause cut needs cover, and a punch change is the cheapest
cover, so punch boundaries are placed ON the splices the tight cut left behind -- never
at arbitrary times, where the layout change would be its own visible event. The hook is
protected completely: no splice and no punch change inside the opening line, and the
callout graphic is measured in level-A coordinates so that beat must stay level A.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats5 as B

FF   = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP  = FF.replace("ffmpeg", "ffprobe")
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = "/Volumes/Extreme/_edit_work/ad1-8-14"
AV   = f"{WORK}/assets_v1"
AS   = f"{HERE}/assets"
G    = f"{HERE}/gfx"
FPS  = "30000/1001"
SRC  = f"{HERE}/tight_full.mov"
DUR  = B.DUR

A_DIR   = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets"
CRUDE   = f"{A_DIR}/batch1-ads/clips/ai-clip-crude-photoshop.mp4"
APPFLOW = f"{A_DIR}/ad2-nutritionist/clips/app-flow-generate-future-self.mp4"
AFCROP  = "crop=1320:2500:0:175,"
STOCK   = f"{WORK}/stock"
AIF     = f"{WORK}/aiframes"

PANEL_W = 980
VID_W   = 1920 - PANEL_W
CROP = {
    "A":  "",
    "B":  "crop=1574:886:198:54,scale=1920:1080:flags=lanczos,",
    "C":  "crop=1730:973:104:40,scale=1920:1080:flags=lanczos,",
    "P1": f"crop={VID_W}:1080:450:0,pad=1920:1080:{PANEL_W}:0:black,",
    "P2": f"crop=800:919:530:80,scale={VID_W}:1080:flags=lanczos,pad=1920:1080:{PANEL_W}:0:black,",
}
PANEL_BEATS = [B.BULLETS, B.FREECARD, B.PLANBUL]
MIN_HOLD = 7.0        # seconds between punch changes outside the panels

# ------------------------------------------------------------------ punch plan
def splices():
    """Tight-time positions of the joins the pause removal created."""
    tc = json.load(open(f"{HERE}/tight_cuts_full.json"))
    out, acc = [], 0.0
    for a, b in tc["keeps"][:-1]:
        acc += b - a
        out.append(round(acc, 3))
    return out

def punch_plan():
    sp = splices()
    hook_end = B.CALLOUT[1]
    # forced boundaries: the panel beats must start and end exactly on their beat
    forced = sorted({t for beat in PANEL_BEATS for t in beat} | {hook_end})
    bounds, last = [0.0], 0.0
    for t in sorted(set(sp) | set(forced)):
        if t <= hook_end or t >= DUR - 0.4:
            continue
        if t in forced or t - last >= MIN_HOLD:
            bounds.append(round(t, 3)); last = t
    bounds.append(round(DUR, 3))
    bounds = sorted(set(bounds))

    def in_panel(a, b):
        return any(pa - 0.01 <= a and b <= pb + 0.01 for pa, pb in PANEL_BEATS)

    plan, prev = [], None
    alt = ["B", "A", "C", "A"]
    ai = 0
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        if b - a < 0.25:            # never a sub-0.25s segment
            if plan: plan[-1] = (plan[-1][0], b, plan[-1][2]); continue
        if a < hook_end:
            lvl = "A"
        elif in_panel(a, b):
            lvl = "P1" if (prev != "P1") else "P2"
        else:
            lvl = alt[ai % len(alt)]; ai += 1
            if lvl == prev:                    # the jump-cut assertion
                ai += 1; lvl = alt[ai % len(alt)]
        plan.append((a, b, lvl)); prev = lvl
    return plan

PUNCH = punch_plan()

def punch():
    parts, cat = [], ""
    for i, (a, b, lvl) in enumerate(PUNCH):
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,{CROP[lvl]}setsar=1[v{i}]")
        cat += f"[v{i}]"
    fc = ";".join(parts) + f";{cat}concat=n={len(PUNCH)}:v=1:a=0[vout]"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", SRC, "-filter_complex", fc,
                    "-map", "[vout]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "16", "-pix_fmt", "yuv420p", "-r", FPS, "-c:a", "copy",
                    f"{HERE}/punched5.mov"], check=True)
    print("punched5.mov done")

# ------------------------------------------------------------------ overlays
# full-screen / panel animated graphics: name -> beat
GFX = [
    ("callout",  B.CALLOUT),  ("gen",     B.GEN),      ("phone",  B.PHONE),
    ("today",    B.TODAY),    ("bullets", B.BULLETS),  ("lower3", B.LOWER3),
    ("title",    B.TITLE),    ("lower3b", B.LOWER3B),  ("free",   B.FREECARD),
    ("cta1",     B.CTA1),     ("lower3c", B.LOWER3C),  ("before1", B.BEFORE1),
    ("fatdad",   B.FATDAD),   ("afterpic", B.AFTERPIC),("superior", B.SUPERIOR),
    ("cta2",     B.CTA2),     ("step1",   B.STEP1),    ("planbul", B.PLANBUL),
    ("look",     B.LOOKNOW),
]
# video inserts: (beat, src, src_in, panel_width_or_0, extra_filter, tag)
#   panel width 0 == FULL FRAME -> AI tag goes upper-left at 1.5x (lesson 17)
# Dan's revision 1:09 -- the before/after transform card is replaced by the real app
# flow he linked. He asked for 0:03-0:26, but the source shows the "Meet the new you"
# BEFORE/AFTER screen from 25.25 s and an email-capture screen after that, so the usable
# window is 3.0-24.9 s, sped up to fit (he said to accelerate as necessary).
APPDEMO_IN, APPDEMO_SRC = 3.0, f"{AS}/clip_109_replacement.mp4"
APPDEMO_RATE = round((24.9 - APPDEMO_IN) / (B.APPDEMO[1] - B.APPDEMO[0]), 4)

VID = [
    (B.APPDEMO, APPDEMO_SRC, APPDEMO_IN, 520,
     f"setpts=PTS/{APPDEMO_RATE},crop=1320:2500:0:200,", None),
    (B.DADCLIP,  f"{AIF}/dad/clip_dad.mp4", 0.2, 0,   "", "big"),
    (B.BBUILD,   f"{STOCK}/5319758.mp4",    1.0, 0,   "", None),
    (B.SHOP,     CRUDE,                     0.0, 700, "", "small"),
    (B.AMAZING,  f"{HERE}/aigen/clip_amazing.mp4", 0.2, 0, "", "big"),
    (B.BEN1,     f"{AIF}/clip_a.mp4",       0.3, 0,   "", "big"),
    (B.BEN2,     f"{AIF}/clip_b.mp4",       0.5, 0,   "", "big"),
    (B.BEN3,     f"{AIF}/clip_c.mp4",       0.0, 0,   "", "big"),
    (B.BEN4,     f"{STOCK}/8858426.mp4",    2.0, 0,   "", None),
    (B.MEALPREP, f"{STOCK}/6894099.mp4",    1.5, 0,   "", None),
    (B.ASSESS,   f"{AV}/stats_scan.mp4",    0.0, 0,   "", None),
]
# static image inserts with Ken Burns: (beat, jpg, direction)
KB = [
    (B.WORKOUT, f"{AV}/p_app_workout.jpg", "in"),
    (B.NUTRI,   f"{AV}/p_app_nutri.jpg",   "out"),
]

def _appflow_slices(beat):
    """The live product flow: photo already in the generation screen (never the CROP
    screen, lesson 15) -> generating -> AFTER ALONE. Never the 'Meet the new you' screen,
    which renders before and after together."""
    a, b = beat
    third = (b - a) / 3
    return [(round(a, 3), round(a + third, 3), 3.2),
            (round(a + third, 3), round(a + 2*third, 3), 20.0),
            (round(a + 2*third, 3), round(b, 3), 29.4)]

def mix():
    inp, fc, idx = ["-i", f"{HERE}/punched5.mov"], [], 1
    cur = "[0:v]"

    def over(src, a, b, x=0, y=0, loop=False, pre="", ss=None, tlen=None):
        nonlocal inp, fc, idx, cur
        # tlen matters whenever `pre` retimes the clip: a setpts=PTS/3 insert needs THREE
        # times the beat length read off the source, and defaulting to the beat length
        # silently delivers a third of the intended footage.
        if loop: inp += ["-loop", "1", "-t", str(round(b - a + 0.3, 3))]
        if ss is not None:
            inp += ["-ss", str(ss), "-t", str(round(tlen if tlen else b - a + 0.25, 3))]
        inp += ["-i", src]
        pts = "setpts=PTS-STARTPTS" if ss is not None or not loop else "setpts=PTS"
        fc.append(f"[{idx}:v]{pre}{pts}+{a}/TB[g{idx}]")
        fc.append(f"{cur}[g{idx}]overlay={x}:{y}:enable='between(t,{a},{b})'[s{idx}]")
        cur = f"[s{idx}]"; idx += 1

    for name, beat in GFX:
        p = f"{G}/{name}.mov"
        if not os.path.exists(p):
            print(f"  ! missing {name}.mov -- skipped"); continue
        over(p, beat[0], beat[1])

    for (beat, src, si, wid, extra, tag) in VID:
        a, b = beat
        rate = float(extra.split("setpts=PTS/")[1].split(",")[0]) if "setpts=PTS/" in extra else 1.0
        tlen = (b - a) * rate + 0.3
        if not os.path.exists(src):
            print(f"  ! missing {os.path.basename(src)} -- skipped"); continue
        if wid:
            plate = "plate_app" if wid == 520 else "plate_phone"
            hole_y = 30 if plate == "plate_app" else 0
            hole_h = 1020 if plate == "plate_app" else 1080
            over(f"{G}/{plate}.png", a, b, loop=True)               # field behind
            x = (1920 - wid) // 2
            over(src, a, b, x=x, y=hole_y, ss=si, tlen=tlen,
                 pre=f"{extra}scale={wid}:{hole_h}:flags=lanczos,setsar=1,")
            over(f"{G}/{plate}.png", a, b, loop=True)               # trims the corners
        else:
            over(src, a, b, ss=si, tlen=tlen,
                 pre=f"{extra}scale=1920:1080:force_original_aspect_ratio=increase,"
                     f"crop=1920:1080,setsar=1,")
        if tag == "big":
            over(f"{G}/tag_big.png", a + 0.10, b, x=40, y=40, loop=True)
        elif tag == "small":
            over(f"{G}/tag.png", a + 0.10, b, x=(1920-wid)//2 + 26, y=76, loop=True)

    for (beat, jpg, direc) in KB:
        a, b = beat
        n = max(2, int((b - a) * 29.97))
        z = f"1+0.09*on/{n}" if direc == "in" else f"1.09-0.09*on/{n}"
        # supersample before zoompan or it jitters (lesson 7)
        over(jpg, a, b, loop=True,
             pre=f"scale=7680:4320,zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':"
                 f"y='ih/2-(ih/zoom/2)':s=1920x1080:fps={FPS},setsar=1,")

    # the two live app-flow runs
    for beat in (B.SEQ, B.ENDCARD):
        for (a, b, si) in _appflow_slices(beat):
            over(f"{G}/plate_app.png", a, b, loop=True)
            # geometry must match plate_app's hole [700,30,1220,1050] exactly, or the
            # field shows through under the phone
            over(APPFLOW, a, b, x=700, y=30, ss=si,
                 pre=f"{AFCROP}scale=520:1020:flags=lanczos,setsar=1,")
            over(f"{G}/plate_app.png", a, b, loop=True)
        # the AFTER-alone slice carries the disclosure, which also covers the email form
        la, lb, _ = _appflow_slices(beat)[-1]
        over(f"{AV}/big_ai_cover.png", la, lb, x=675, y=690, loop=True)

    fc[-1] = fc[-1].rsplit("[s", 1)[0] + "[vout]"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + inp +
                   ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "0:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-r", FPS, "-c:a", "copy",
                    f"{HERE}/rev5_nocap.mov"], check=True)
    print("rev5_nocap.mov done")

if __name__ == "__main__":
    if not sys.argv[1:] or "plan" in sys.argv:
        print(f"{len(PUNCH)} punch segments over {DUR:.2f}s")
        for a, b, l in PUNCH: print(f"  {a:7.2f} -> {b:7.2f}  {l}")
    if "punch" in sys.argv: punch()
    if "mix" in sys.argv:   mix()
