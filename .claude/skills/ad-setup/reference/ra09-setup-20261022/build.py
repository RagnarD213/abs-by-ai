#!/usr/bin/env python3
"""RA-09 "Do You Think AI Is Changing The World?" (AD, 9:16 film): five thumbnail options, each in 9:16 and 16:9,
2026-10-22. Dan's standard mix (VIDEO-RULES, 2026-10-13): 1 pool photo, 1 studio photo, 1 AI image of Dan, 2 AI images of
Codex's choice. Codex (GPT-6.1 Sol, high) made every plate and AI image and chose the concepts and type of options 3 to 5
(assets/plan.json in the media build folder). Options 1 and 2 are his real cutouts, never redrawn. All type is set here.
Same headline on all five: AI IS CHANGING THE WORLD / USE IT FOR ABS. Option 3 shows no goal picture at all.
The script lives in the repo; images live in the git-ignored media folder below (photos of Dan, public repo).
Helpers are imported from the RA-06 build. Run: python3 build.py [numbers...]"""
import importlib.util, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OUT = PROJ + "/social media graphics/youtube/thumbnails/RA-09 Do You Think AI Is Changing The World"
HERE = OUT + "/_build-2026-10-22"
_spec = importlib.util.spec_from_file_location("ra06b", os.path.join(OUT, "..", "RA-06 Whats The Best Ab Exercise", "_build-2026-10-16", "build.py"))
K = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(K)
K.HERE = HERE  # person masks land in this build's mask/ folder
font, tw, th, cover, paste_cut, person, clearance, headroom, fit, trimmed = (
    K.font, K.tw, K.th, K.cover, K.paste_cut, K.person, K.clearance, K.headroom, K.fit, K.trimmed)
FMT = K.FMT; PH = K.PH
SLUG = "ai-changing-world"
LEAD, H1, H2 = "AI IS CHANGING THE WORLD", "USE IT", "FOR ABS"
WHITE = (255, 255, 255)
hexc = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
SUP = "/System/Library/Fonts/Supplemental/"
din = lambda z: ImageFont.truetype(SUP + "DIN Condensed Bold.ttf", z)
ablack = lambda z: ImageFont.truetype(SUP + "Arial Black.ttf", z)
futc = lambda z: ImageFont.truetype(SUP + "Futura.ttc", z, index=4)       # Condensed ExtraBold
impact = lambda z: ImageFont.truetype(SUP + "Impact.ttf", z)
phos = lambda z: ImageFont.truetype(SUP + "Phosphate.ttc", z, index=0)    # Inline
PLAN = {o["number"]: o for o in json.load(open(f"{HERE}/assets/plan.json"))["options"]}


def area(o, fmt): return tuple(float(v) for v in o[f"headline_area_{fmt}"].split(","))


def put(d, x, y, t, f, col, off=0, scol=None):
    b = f.getbbox(t)
    if off: d.text((x - b[0] + off, y - b[1] + off), t, font=f, fill=scol)
    d.text((x - b[0], y - b[1]), t, font=f, fill=col)
    return (x, y, x + tw(f, t) + off, y + th(f, t) + off)


def area_type(canvas, box, rows, align, draw, gapk=0.10):
    """Fit rows [(text, make, scale, colour)] in a fractional box; the tightest row sets the size. Returns text boxes."""
    W, H = canvas.size; x0, y0, x1, y1 = box[0] * W, box[1] * H, box[2] * W, box[3] * H
    aw, ah = x1 - x0, y1 - y0
    s = min(fit(lambda z, r=r: r[1](max(8, round(z * r[2]))), r[0], aw * 0.94, 520) for r in rows)
    while True:
        fs = [(t, mk(round(s * sc)), col) for t, mk, sc, col in rows]
        gap = round(s * gapk)
        tot = sum(th(f, t) for t, f, _ in fs) + gap * (len(fs) - 1)
        if tot <= ah * 0.92 or s < 40: break
        s -= 4
    d = ImageDraw.Draw(canvas); y = y0 + (ah - tot) / 2; boxes = []
    for t, f, col in fs:
        w = tw(f, t); x = x0 if align == "l" else (x1 - w if align == "r" else x0 + (aw - w) / 2)
        boxes.append(draw(d, round(x), round(y), t, f, col)); y += th(f, t) + gap
    return boxes


def glow_under(canvas, boxes_fn, colour=(0, 8, 24), radius=22, strength=0.85):
    """Draw the type once on a mask, blur it into a dark glow under the real type."""
    W, H = canvas.size; m = Image.new("L", (W, H), 0); boxes_fn(ImageDraw.Draw(m))
    g = Image.new("RGBA", (W, H), colour + (0,))
    g.putalpha(m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(min(255, v * strength * 1.6))))
    return Image.alpha_composite(canvas.convert("RGBA"), g).convert("RGB")


def place(canvas, t, x, y):
    canvas = canvas.convert("RGBA"); lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); lay.paste(t, (x, y), t)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh.putalpha(lay.getchannel("A").point(lambda v: int(v * 0.55)).filter(ImageFilter.GaussianBlur(12)))
    sh2 = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh2.paste(sh, (10, 14), sh)
    canvas = Image.alpha_composite(Image.alpha_composite(canvas, sh2), lay)
    return canvas.convert("RGB"), lay.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()


def pool(fmt):
    """1: real pool photo 247 (big smile, standing in teal board shorts) over a Codex blue-hour pool with faint circuit
    light on the water; DIN Condensed Bold stacked at the top (9:16) or left (16:9), white lead, electric cyan hero,
    a soft dark glow behind the type, no band."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/pool_{fmt}.png").convert("RGB"), W, H)
    cut = trimmed(f"{PH}/_cutouts/photo-247_CUTOUT.png", 0.80)
    if fmt == "9x16":
        ph = 1330; s = ph / cut.height; x = (W - round(cut.width * s)) // 2; y = H - ph
        tbox = (0.05, 0.025, 0.95, 0.29); align = "c"
    else:
        ph = 1000; s = ph / cut.height; x = W - round(cut.width * s) - 150; y = H - ph
        tbox = (0.04, 0.10, 0.52, 0.90); align = "l"
    canvas, am = paste_cut(c, cut, x, y, s)
    cyan = hexc("#29E3FF")
    rows = [(LEAD, din, 0.42, WHITE), (H1, din, 1.0, cyan), (H2, din, 1.0, cyan)]
    tmp = canvas.copy(); boxes = area_type(tmp, tbox, rows, align, lambda d, x, y, t, f, col: put(d, x, y, t, f, col), gapk=0.02)
    canvas = glow_under(canvas, lambda d: area_type(Image.new("L", (W, H)), tbox, [(r[0], r[1], r[2], 255) for r in rows], align,
                                                     lambda dd, x, y, t, f, col: put(d, x, y, t, f, 255), gapk=0.02))
    area_type(canvas, tbox, rows, align, lambda d, x, y, t, f, col: put(d, x, y, t, f, col), gapk=0.02)
    return canvas, clearance(am, boxes), headroom(am)


def block(t, f, fill, ink, padk=0.16, angle=-3):
    pad = round(f.size * padk); w, h = tw(f, t) + 2 * pad, th(f, t) + 2 * pad
    im = Image.new("RGBA", (w, h), fill + (255,)); put(ImageDraw.Draw(im), pad, pad, t, f, ink)
    return im.rotate(angle, expand=True, resample=Image.BICUBIC)


def globe(fmt):
    """2: real studio-gray-67 (big smile, hands on hips, green shorts) with an orange rim glow in front of a Codex navy
    globe wired with orange network lines; Arial Black, black letters on solid tilted safety-orange blocks, one per line
    (stacked top-centre in 9:16, left in 16:9)."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/globe_{fmt}.png").convert("RGB"), W, H)
    cut = trimmed(f"{PH}/_cutouts/studio-gray-67_CUTOUT.png", 0.80)
    if fmt == "9x16":
        ph = 1300; s = ph / cut.height; x = (W - round(cut.width * s)) // 2; y = H - ph
    else:
        ph = 1010; s = ph / cut.height; x = W - round(cut.width * s) - 170; y = H - ph
    canvas, am = paste_cut(c, cut, x, y, s, glow=(255, 140, 40))
    orange, ink = hexc("#FF7A1A"), hexc("#0A0A0C")
    if fmt == "9x16":
        hero = ablack(fit(ablack, "FOR ABS", W * 0.66, 300)); lead = ablack(fit(ablack, LEAD, W * 0.80, 120))
        tiles = [(block(LEAD, lead, orange, ink, angle=-3), "c"), (block(H1, hero, orange, ink, angle=-3), "c"), (block(H2, hero, orange, ink, angle=-3), "c")]
        y, boxes = 36, []
        for t, _ in tiles:
            canvas, bb = place(canvas, t, (W - t.width) // 2, y); boxes.append(bb); y += t.height - 6
    else:
        left = int(np.where(am.any(0))[0].min()); room = left - 90
        hero = ablack(fit(ablack, "FOR ABS", room * 0.86, 260)); lead = ablack(fit(ablack, LEAD, room * 0.92, 110))
        tiles = [block(LEAD, lead, orange, ink, angle=3), block(H1, hero, orange, ink, angle=3), block(H2, hero, orange, ink, angle=3)]
        tot = sum(t.height - 6 for t in tiles); y, boxes = (H - tot) // 2, []
        for t in tiles:
            canvas, bb = place(canvas, t, 60, y); boxes.append(bb); y += t.height - 6
    return canvas, clearance(am, boxes), headroom(am)


def ai3(fmt):
    """3: AI Dan (reference-matched) at a cable station whose steel mechanical arm adjusts the pulley for him, racing red;
    Futura Condensed ExtraBold flush right, white lead, cream hero, a hard charcoal extrusion downward."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai3_{fmt}.png").convert("RGB"), W, H)
    am = person(c, f"ai3_{fmt}")
    ext = hexc("#171717")
    def draw(d, x, y, t, f, col):
        n = max(4, f.size // 16)
        for k in range(n, 0, -1): put(d, x, y + k, t, f, ext)
        b = put(d, x, y, t, f, col); return (b[0], b[1], b[2], b[3] + n)
    rows = [("AI IS CHANGING", futc, 0.48, WHITE), ("THE WORLD", futc, 0.48, WHITE), (H1, futc, 1.0, hexc("#FFF1D0")), (H2, futc, 1.0, hexc("#FFF1D0"))]
    boxes = area_type(c, area(PLAN[3], fmt), rows, "r", draw, gapk=0.04)
    return c, clearance(am, boxes), headroom(am)


def ai4(fmt):
    """4: a deadly serious giant ivory robot supervises one ordinary dumbbell curl on a grass-green set; a straight
    warm-white bottom panel with flat Impact, dark lead and green hero."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai4_{fmt}.png").convert("RGB"), W, H)
    am = person(c, f"ai4_{fmt}")
    box = area(PLAN[4], fmt); d = ImageDraw.Draw(c)
    d.rectangle([0, round((box[1] - 0.02) * H), W, H], fill=hexc("#F5F3E8"))
    am = am & (np.arange(H)[:, None] < round((box[1] - 0.02) * H))
    rows = ([(LEAD, impact, 0.42, hexc("#202820")), (H1, impact, 1.0, hexc("#136B2D")), (H2, impact, 1.0, hexc("#136B2D"))] if fmt == "9x16"
            else [(LEAD, impact, 0.50, hexc("#202820")), (H1 + " " + H2, impact, 1.0, hexc("#136B2D"))])
    boxes = area_type(c, box, rows, "c", lambda d, x, y, t, f, col: put(d, x, y, t, f, col), gapk=0.03)
    return c, clearance(am, boxes), 9999


def ai5(fmt):
    """5: a giant laptop whose keyboard is a miniature home gym, royal blue; Phosphate Inline centred on the laptop
    screen, white lead, yellow hero."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai5_{fmt}.png").convert("RGB"), W, H)
    am = person(c, f"ai5_{fmt}")
    rows = [("AI IS CHANGING", phos, 0.48, WHITE), ("THE WORLD", phos, 0.48, WHITE), (H1, phos, 1.0, hexc("#FFD43B")), (H2, phos, 1.0, hexc("#FFD43B"))]
    boxes = area_type(c, area(PLAN[5], fmt), rows, "c", lambda d, x, y, t, f, col: put(d, x, y, t, f, col), gapk=0.06)
    return c, clearance(am, boxes), 9999


JOBS = {
    1: ("pool-photo-247-cyan-din", "Real pool photo: you smiling in the pool at blue hour, cyan headline on top", pool),
    2: ("studio-gray-67-orange-globe", "Real studio photo: you in front of a wired-up globe, orange block headline", globe),
    3: ("ai-dan-smart-cable-red", "AI picture of you: a smart cable machine adjusts itself for you, racing red", ai3),
    4: ("ai-robot-supervises-curl-green", "AI: a giant robot very seriously supervises one dumbbell curl", ai4),
    5: ("ai-laptop-home-gym-blue", "AI: a giant laptop that turns into a mini home gym, royal blue", ai5),
}


def main():
    want = [int(a) for a in sys.argv[1:]] or sorted(JOBS)
    qp = os.path.join(HERE, "qc.json"); res = {f"{r['number']}-{r['fmt']}": r for r in (json.load(open(qp)) if os.path.exists(qp) else [])}
    for n in want:
        name, lab, fn = JOBS[n]
        for fmt in FMT:
            plate = {"pool": "pool", "globe": "globe"}.get(fn.__name__, fn.__name__)
            if not os.path.exists(f"{HERE}/assets/{plate}_{fmt}.png"): print(f"[{n} {fmt}] plate missing"); continue
            canvas, clear, head = fn(fmt)
            f_ = f"{SLUG}_{n}-{name} | {fmt}.jpg"; p = os.path.join(OUT, f_); canvas.save(p, quality=92)
            ok = clear >= 25 and head >= 14 and os.path.getsize(p) < 2_000_000
            print(f"[{n} {fmt}] clearance {clear}px, headroom {head}px, {os.path.getsize(p)//1024}KB -> {'PASS' if ok else 'FAIL'}")
            res[f"{n}-{fmt}"] = dict(number=n, fmt=fmt, name=name, label=lab, file=f_, clearance_px=clear, headroom_px=head, ok=bool(ok))
    res = [res[k] for k in sorted(res)]
    json.dump(res, open(qp, "w"), indent=2)
    if len(res) != 10: return
    by = {(r["number"], r["fmt"]): r for r in res}
    pad, w9, h9, w16, h16 = 30, 360, 640, 1138, 640
    rowh = h9 + 70
    sheet = Image.new("RGB", (pad * 4 + 60 + w9 + w16, 150 + 5 * rowh), (242, 242, 244)); d = ImageDraw.Draw(sheet)
    d.text((pad, 24), "Do You Think AI Is Changing The World? (RA-09 ad): five thumbnail choices", font=font(40), fill=(20, 22, 28))
    d.text((pad, 80), "Left: 9:16 (the ad's shape, the one installed). Right: the 16:9 version. All made with Codex. Pick one number.", font=font(24), fill=(70, 72, 80))
    for i, n in enumerate(sorted(JOBS)):
        y = 140 + i * rowh
        sheet.paste(Image.open(os.path.join(OUT, by[(n, "9x16")]["file"])).resize((w9, h9), Image.LANCZOS), (pad + 60, y))
        sheet.paste(Image.open(os.path.join(OUT, by[(n, "16x9")]["file"])).resize((w16, h16), Image.LANCZOS), (pad * 2 + 60 + w9, y))
        d.text((pad, y + 4), str(n), font=font(52), fill=(20, 22, 28))
        d.text((pad + 60, y + h9 + 10), JOBS[n][1], font=font(24), fill=(40, 42, 50))
    sp = os.path.join(OUT, "REVIEW_ai-changing-world-five-options.jpg"); sheet.save(sp, quality=88); print(sp)


if __name__ == "__main__":
    main()
