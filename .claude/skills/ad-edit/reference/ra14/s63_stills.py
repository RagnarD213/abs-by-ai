#!/usr/bin/env python3
"""RA-14 round 1: every graphic and clip as a STILL on its real frame (PRE-RENDER-APPROVAL step 3/4), 1080x1920.

  s63_stills.py cards      the opaque inserts: G1 (AI goal picture), P1a/P1b (self-generation demo), A1 (analysis card,
                           the approved RA-01 component as it stands), T1a/T1b (app tour B0544)
  s63_stills.py overlays   the template overlays on their real graded frames: L1 L2 L3 R1 C1 (needs beats.json, cap_9x16)

Everything is Soft Blue Light (softblue.py + the HyperFrames vertical templates). Phones use the approved iPhone shell at
the 9:16 size the Soft Blue shorts standard locked (softblue-sl03 `phone_shell`). Stills carry the real caption line of
their moment. Writes round1/stills/<ID>.jpg and round1/stills/meta.json.
"""
import importlib.util, json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
REPO = L.REPO
sys.path.insert(0, f"{REPO}/.claude/skills/_shared")
sys.path.insert(0, f"{REPO}/.claude/skills/_shared/hyperframes")
import softblue as B

W, H = 1080, 1920
OUT = "round1/stills"; os.makedirs(OUT, exist_ok=True)
DEMO = f"{REPO}/Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/simulated-dan-sunglasses-to-pool-ad14-v1.mp4"
TOUR = ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/"
        "screen-recordings/B0544_app-feature-tour-home-macro-tracker-775-cal-ai-trainer-pushu_432x920_10s.mp4")
GOAL = f"{REPO}/Media/example pictures/dan by pool.png"
DISP = (741, 68, 434, 941)          # the demo phone's display inside the approved 1920x1080 demo (measured, ro06/phone_demo.py)
CAP_Y = 1400
META = json.load(open(f"{OUT}/meta.json")) if os.path.exists(f"{OUT}/meta.json") else {}


def grab(path, t, vf="null"):
    p = f"{OUT}/_grab.png"
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                    "-vf", f"scale=in_color_matrix=bt709:in_range=tv,{vf}", p], check=True)
    return Image.open(p).convert("RGB")


def square_corners(a, r=56):
    a = a.copy(); h, w = a.shape[:2]
    for dy in range(r):
        inset = int(math.ceil(r - math.sqrt(r*r - (r - dy)**2))) + 3
        for y in (dy, h - 1 - dy):
            a[y, :inset] = a[y, inset]; a[y, w - inset:] = a[y, w - inset - 1]
    return a


def phone_shell():
    """The approved iPhone shell at the 9:16 size (softblue-sl03 batch.phone_shell, Dan 2026-10-02): 624x1290, the screen
    content goes at (48,114) 518x982."""
    im = Image.new("RGBA", (660, 1090), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((91, 34, 573, 1062), 68, fill=(0, 0, 0, 120))
    im = sh.filter(ImageFilter.GaussianBlur(14)); d = ImageDraw.Draw(im)
    def rr(box, fill, r, outline=None, width=1): d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)
    rr((90, 28, 562, 1052), (95, 107, 119), 66, (166, 179, 190), 2); rr((95, 33, 557, 1047), (5, 8, 12), 62)
    s = Image.new("RGB", (448, 1000), (248, 250, 252)); e = ImageDraw.Draw(s); e.text((30, 14), "9:41", font=B.font(17), fill=(23, 43, 59))
    for i in range(4): e.rounded_rectangle((352 + i*6, 30 - i*3, 355 + i*6, 35), 1, fill=(25, 32, 40))
    e.rounded_rectangle((391, 22, 418, 34), 3, outline=(25, 32, 40), width=2); e.rectangle((419, 26, 422, 30), fill=(25, 32, 40)); e.rectangle((394, 25, 413, 31), fill=(25, 32, 40))
    e.rounded_rectangle((146, 15, 302, 51), 18, fill=(0, 0, 0)); e.ellipse((276, 26, 288, 38), fill=(18, 26, 36)); e.ellipse((280, 29, 284, 33), fill=(34, 60, 82)); e.rounded_rectangle((153, 984, 295, 989), 3, fill=(24, 28, 32))
    m = Image.new("L", (448, 1000)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 447, 999), 54, fill=255); im.paste(s, (102, 40), m)
    rr((86, 202, 90, 258), (69, 81, 94), 2); rr((86, 283, 90, 354), (69, 81, 94), 2); rr((562, 253, 566, 352), (86, 96, 110), 2)
    im = im.crop((70, 10, 590, 1085)); return im.resize((624, 1290), Image.LANCZOS)


PHONE_TOP = 96                       # 96 + 1290 = 1386: the phone ends 14 px above the caption line
def phone_card(t, screen, chip=None):
    """The Soft Blue field with the phone centred, as large as fits above the caption line (VIDEO-RULES 2026-10-02)."""
    im = B.field(t, W, H).convert("RGBA")
    sh = phone_shell()
    scr = ImageOps.fit(screen, (518, 982), Image.LANCZOS, centering=(0.5, 0.0))
    m = Image.new("L", (518, 982)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 517, 981), 58, fill=255)
    m = Image.new("L", (518, 982)); ImageDraw.Draw(m).rounded_rectangle((0, -60, 517, 981), 56, fill=255)   # square top (under the status bar), round bottom
    body = sh.copy(); body.paste(scr, (48, 114), m)
    x = (W - 624)//2
    im.alpha_composite(body, (x, PHONE_TOP))
    box = (x, PHONE_TOP, x + 624, PHONE_TOP + 1290)
    if chip:
        B.disclosure(im, chip, xy=(W//2, 1580), anchor="mt")
    return im.convert("RGB"), box


def caption(im, line, k=None, y=CAP_Y):
    """The caption line as s07_captions.py draws it (Manrope ExtraBold 64, white, heavy shadow, current word in cyan)."""
    if not line: return im
    from motionlib import font
    F = font(64, "ExtraBold"); im = im.convert("RGBA")
    base = y + F.getmetrics()[0]; tw = F.getlength(line); x = int((W - tw)//2)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x, base), line, font=F, fill=(0, 0, 0, 245), anchor="ls")
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9))); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(im); cx = float(x)
    for j, ww in enumerate(line.split(" ")):
        d.text((int(cx), base), ww, font=F, fill=((104, 197, 255) if j == k else (255, 255, 255)) + (255,), anchor="ls")
        cx += F.getlength(ww + " ")
    return im.convert("RGB")


def cap_at(t):
    p = "cap_9x16/caption_states.json"
    if not os.path.exists(p): return None, None
    for s in json.load(open(p))["states"]:
        if s["beat"][0] <= t < s["beat"][1]: return s["line"], s["k"]
    return None, None


def save(gid, im, t, **meta):
    line, k = cap_at(t) if t is not None else (None, None)
    y = meta.pop("cap_y", CAP_Y)
    if line: im = caption(im, line, k, y)
    im.save(f"{OUT}/{gid}.jpg", quality=92)
    META[gid] = dict(t=t, caption=line, **meta)
    json.dump(META, open(f"{OUT}/meta.json", "w"), indent=1)
    print("wrote", gid, meta.get("note", ""))


def beats():
    return json.load(open("beats.json")) if os.path.exists("beats.json") else None


def cards():
    Bt = beats()
    cb = {c["name"]: c["beat"] for c in Bt["cards"]} if Bt else {}
    mid = lambda n, f=0.5: (cb[n][0] + (cb[n][1] - cb[n][0])*f) if n in cb else None
    # G1: the AI goal picture, one photo on the field (softblue.scene_photo), AI-GENERATED chip clear of face and abs
    im = B.scene_photo(1.0, W, H, GOAL, "AI-GENERATED").convert("RGB")
    save("G1", im, mid("G1"), note="softblue.scene_photo, original 'dan by pool.png'")
    # P1a: the approved self-generation demo, phone phase (options -> Generate -> generating), in the approved shell
    # the real-photo chip shows only while his real photo is on the phone (never under a form with no photo)
    for gid, ts, f, chip in (("P1a", 2.55, 0.18, None), ("P1a2", 3.25, 0.40, "Real picture of me. Not AI-generated.")):
        fr = grab(DEMO, ts)
        scr = Image.fromarray(square_corners(np.asarray(fr.crop((DISP[0], DISP[1], DISP[0]+DISP[2], DISP[1]+DISP[3])))))
        im, box = phone_card(1.0, scr, chip=chip)
        save(gid, im, mid("P1", f), box=box, src_t=ts, note="approved demo (Ad 14 R3 g17), simulated/composited provenance kept")
    im = B.scene_photo(1.0, W, H, GOAL, "AI-GENERATED").convert("RGB")
    save("P1b", im, mid("P1", 0.80), note="the demo's settled result, from the original picture, AI-GENERATED")
    # T1: the approved app tour B0544 in the same shell (calorie tracking, then the AI Trainer's demo videos)
    for gid, ts, f in (("T1a", 4.7, 0.30), ("T1b", 7.0, 0.66)):
        scr = grab(TOUR, ts)
        im, box = phone_card(1.0, scr)
        save(gid, im, mid("T1", f), box=box, src_t=ts, note="B0544, approved for reuse 2026-10-10")


def analysis():
    """A1: the analysis card Dan asked to reuse (RA-01), exactly as the shared component draws it today (J2 dark field)."""
    Bt = beats(); c = next(x for x in Bt["cards"] if x["name"] == "A1")
    dur = c["beat"][1] - c["beat"][0]
    out = "cards_9x16/A1_j2"; os.makedirs("cards_9x16", exist_ok=True)
    subprocess.run([sys.executable, f"{REPO}/.claude/skills/_shared/adkit/analysis_card.py", "--image", GOAL, "--aspect", "9x16",
                    "--dur", f"{dur:.3f}", "--label", "ai", "--out", out], check=True)
    mp4 = out + ".mp4" if os.path.exists(out + ".mp4") else next(os.path.join(out, f) for f in os.listdir(out) if f.endswith(".mp4"))
    im = grab(mp4, dur*0.8)
    save("A1", im, c["beat"][0] + dur*0.8, note="adkit.analysis_card as approved on RA-01 (old dark olive look)", clip=mp4)


def overlays():
    """L1 L2 L3 R1 C1 on their real graded frames, composited the way hyperframes/composite.py does it."""
    import vertical as VT, hfbuild as Hh
    Bt = beats(); CUT = json.load(open("cut.json"))
    G = json.load(open("grade.json"))["filter"]
    def src_time(t):
        for p in CUT["pieces"]:
            if p["t_in"] <= t < p["t_out"]: return p["src_in"] + (t - p["t_in"])
        return CUT["pieces"][-1]["src_out"] - 0.02
    def base(t):
        pu = next(p for p in Bt["punch"] if p["beat"][0] <= t < p["beat"][1])
        cw, ch = L.Aspect("9x16").levels[pu["level"]]
        y = int(round(pu["hair_min"] - 0.04*ch)); y = max(0, min(3840-ch, y - y % 2))
        x = int(round(pu["cx"] - cw/2)); x = max(0, min(2160-cw, x - x % 2))
        p = f"{OUT}/_base.png"
        subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{src_time(min(t, CUT['dur']-0.05)):.3f}", "-i", L.ROLL, "-frames:v", "1",
                        "-vf", f"crop={cw}:{ch}:{x}:{y},{L.DECODE},{G},scale={W}:{H}:flags=lanczos", p], check=True)
        return Image.open(p).convert("RGB"), pu
    out = "gfx/r1"
    for g in Bt["overlays"]:
        scenes, meta = VT.scenes_for(g)
        dur = scenes[0][1]["dur"]
        # the settled moment: late enough that every part has landed, before the exit
        last = max([Hh.rel(t, g["t0"]) for _, t in g["config"].get("parts", [])] + [Hh.rel(t, g["t0"]) for t in g["config"].get("reveal", [])] + [0.5])
        snap = min(dur - 0.5, last + 0.7)
        VT.build(scenes, out, render=False, snap=snap, force=True)
        ov = Image.open(f"{out}/stills/{g['id']}.png").convert("RGBA")
        t = g["t0"] + snap
        im, pu = base(t)
        if meta["kind"] == "glass":                      # blur the picture inside the strip, then the content pass (composite.py)
            x0, y0, x1, y1 = meta["box"]
            m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((x0, y0, x1, y1), 36, fill=235)
            im.paste(im.filter(ImageFilter.GaussianBlur(14)), (0, 0), m)
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
        box = meta.get("box")
        cap_y = CAP_Y
        if box and box[1] < CAP_Y + 110 and box[3] > CAP_Y - 20:     # the graphic sits in the caption band: captions lift above it
            cap_y = box[1] - 24 - 96
        save(g["id"], im, t, box=box, level=pu["level"], cap_y=cap_y, copy=g["config"],
             note=f"{g['template']} template, {pu['level']} frame")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        {"cards": cards, "analysis": analysis, "overlays": overlays}[a]()
