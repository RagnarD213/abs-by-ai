#!/usr/bin/env python3
"""RA-12 "The First Step To Getting Abs Isn't A Workout" (AD, 9:16 film): five thumbnail options, each in 9:16 and 16:9,
2026-10-21. Dan's standard mix (VIDEO-RULES, 2026-10-13): 1 pool photo, 1 studio photo, 1 AI image of Dan, 2 AI images of
Codex's choice. Codex (GPT-6.1 Sol, high) made every plate and AI image and chose the concepts and type of options 3 to 5
(assets/plan.json in the media build folder). Options 1 and 2 are his real cutouts, never redrawn. All type is set here.
Same headline on all five: THE FIRST STEP / ISN'T A WORKOUT. Option 3 never shows an AI version of his abs as a goal
picture (Dan, RA-12 R2: "using my own picture makes it seem like I don't really have abs"): the print faces away.
The script lives in the repo; images live in the git-ignored media folder below (photos of Dan, public repo).
Helpers are imported from the RA-06 build. Run: python3 build.py [numbers...]"""
import importlib.util, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OUT = PROJ + "/social media graphics/youtube/thumbnails/RA-12 The First Step To Getting Abs"
HERE = OUT + "/_build-2026-10-21"
_spec = importlib.util.spec_from_file_location("ra06b", os.path.join(OUT, "..", "RA-06 Whats The Best Ab Exercise", "_build-2026-10-16", "build.py"))
K = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(K)
K.HERE = HERE  # person masks land in this build's mask/ folder
font, tw, th, cover, paste_cut, person, clearance, headroom, fit, trimmed = (
    K.font, K.tw, K.th, K.cover, K.paste_cut, K.person, K.clearance, K.headroom, K.fit, K.trimmed)
FMT = K.FMT; PH = K.PH
SLUG = "first-step-abs"
A, B = "THE FIRST STEP", "ISN'T A WORKOUT"
WHITE, BLACK = (255, 255, 255), (10, 10, 12)
hexc = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
SYS, SUP = "/System/Library/Fonts/", "/System/Library/Fonts/Supplemental/"
avenir = lambda z: ImageFont.truetype(SYS + "Avenir Next Condensed.ttc", z, index=8)  # Heavy
marker = lambda z: ImageFont.truetype(SYS + "MarkerFelt.ttc", z, index=1)          # Wide
impact = lambda z: ImageFont.truetype(SUP + "Impact.ttf", z)
phos = lambda z: ImageFont.truetype(SUP + "Phosphate.ttc", z, index=1)              # Solid
futura = lambda z: ImageFont.truetype(SUP + "Futura.ttc", z, index=2)               # Bold
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


def poly_mask(size, pts):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).polygon(pts, fill=255); return m


def place(canvas, t, x, y):
    canvas = canvas.convert("RGBA"); lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); lay.paste(t, (x, y), t)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh.putalpha(lay.getchannel("A").point(lambda v: int(v * 0.55)).filter(ImageFilter.GaussianBlur(12)))
    sh2 = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh2.paste(sh, (10, 14), sh)
    canvas = Image.alpha_composite(Image.alpha_composite(canvas, sh2), lay)
    return canvas.convert("RGB"), lay.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()


def pool(fmt):
    """1: real pool photo 125 (big smile, double-biceps flex, navy shorts) over a warm golden-hour Codex pool; a slanted
    white band (bottom in 9:16, right side in 16:9) with THE FIRST STEP in burnt orange and ISN'T A WORKOUT large in deep
    navy, Avenir Next Condensed Heavy."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/pool_{fmt}.png").convert("RGB"), W, H)
    cut = trimmed(f"{HERE}/cut/photo-125_CUTOUT.png", 0.84)
    if fmt == "9x16":
        s = min(1420 / cut.height, (W - 40) / cut.width); x = (W - round(cut.width * s)) // 2; y = 110
        band = [(0, round(0.625 * H)), (W, round(0.675 * H)), (W, H), (0, H)]
        tbox = (0.06, 0.69, 0.94, 0.985); align = "c"
    else:
        ph = 1040; s = ph / cut.height; x = 40; y = H - ph
        band = [(round(0.575 * W), 0), (W, 0), (W, H), (round(0.525 * W), H)]
        tbox = (0.60, 0.10, 0.965, 0.90); align = "l"
    canvas, am = paste_cut(c, cut, x, y, s)
    bm = poly_mask((W, H), band)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(bm.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.5)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), sh).convert("RGB")
    canvas.paste(Image.new("RGB", (W, H), (252, 250, 245)), (0, 0), bm)
    am = am & ~(np.asarray(bm) > 0)
    navy, orange = hexc("#0B1F3A"), hexc("#E2620B")
    rows = [(A, avenir, 0.56, orange), ("ISN'T A", avenir, 1.0, navy), ("WORKOUT", avenir, 1.0, navy)]
    boxes = area_type(canvas, tbox, rows, align, lambda d, x, y, t, f, col: put(d, x, y, t, f, col), gapk=0.06)
    return canvas, clearance(am, boxes), headroom(am)


def card(lines, W):
    """A white paper card, handwritten black Marker Felt, red marker underline under the hero line, red pushpin."""
    W = int(W)
    f1 = marker(fit(marker, lines[0], W * 0.62, 300)); f2 = marker(fit(marker, lines[1], W * 0.86, 360))
    padx, pady, gap = round(W * 0.06), round(f2.size * 0.42), round(f2.size * 0.16)
    w = max(tw(f1, lines[0]), tw(f2, lines[1])) + 2 * padx
    h = th(f1, lines[0]) + gap + th(f2, lines[1]) + round(f2.size * 0.30) + 2 * pady
    t = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle([20, 20, 20 + w, 20 + h], fill=(250, 248, 240, 255))
    y = 20 + pady
    put(d, 20 + (w - tw(f1, lines[0])) // 2, y, lines[0], f1, (20, 20, 22))
    y += th(f1, lines[0]) + gap
    x2 = 20 + (w - tw(f2, lines[1])) // 2
    put(d, x2, y, lines[1], f2, (20, 20, 22))
    uy = y + th(f2, lines[1]) + round(f2.size * 0.12)
    d.line([(x2, uy + 6), (x2 + tw(f2, lines[1]), uy)], fill=(214, 30, 36, 255), width=max(8, f2.size // 12))
    r = max(16, W // 50); cx = 20 + w // 2
    d.ellipse([cx - r, 20 + 6, cx + r, 20 + 6 + 2 * r], fill=(205, 24, 30, 255))
    d.ellipse([cx - r // 3, 20 + 12, cx + r // 4, 20 + 12 + r // 2], fill=(255, 150, 150, 255))
    return t


def board(fmt):
    """2: real studio-blue-11 (smiling, hands on hips, green shorts) in front of a Codex cork vision board of pinned
    polaroids and notes; the headline handwritten in black Marker Felt on a tilted white paper card with a red pushpin
    and a red marker underline (top in 9:16, left in 16:9)."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/board_{fmt}.png").convert("RGB"), W, H)
    c = Image.blend(c, Image.new("RGB", (W, H), (40, 26, 14)), 0.18)
    cut = trimmed(f"{PH}/_cutouts/studio-blue-11_CUTOUT.png", 0.86)
    if fmt == "9x16":
        ph = 1240; s = ph / cut.height; x = (W - round(cut.width * s)) // 2; y = H - ph
    else:
        ph = 1030; s = ph / cut.height; x = W - round(cut.width * s) - 90; y = H - ph
    canvas, am = paste_cut(c, cut, x, y, s, glow=(255, 236, 200))
    if fmt == "9x16":
        t = card([A, B], W * 0.92).rotate(-3, expand=True, resample=Image.BICUBIC); px, py = (W - t.width) // 2, 40
    else:
        left = int(np.where(am.any(0))[0].min())
        t = card([A, B], (left - 100) * 0.95).rotate(3, expand=True, resample=Image.BICUBIC); px, py = 50, (H - t.height) // 2
    canvas, bb = place(canvas, t, px, py)
    return canvas, clearance(am, [bb]), headroom(am)


def ai3(fmt):
    """3: AI Dan (his real physique, reference-matched) holds a big print turned toward himself, its blank cobalt back to
    the viewer, under a cobalt spotlight; Impact, THE FIRST STEP sky blue, ISN'T A WORKOUT white, tight navy hard shadow."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai3_{fmt}.png").convert("RGB"), W, H)
    am = person(c, f"ai3_{fmt}")
    sh = hexc("#020A20")
    draw = lambda d, x, y, t, f, col: put(d, x, y, t, f, col, max(5, f.size // 18), sh)
    rows = [(A, impact, 0.62, hexc("#53CFFF")), (B, impact, 1.0, WHITE)]
    box = area(PLAN[3], fmt)
    if fmt == "16x9": box = (box[0], 0.03, box[2], 0.27)  # 0.32 bottom left 24 px over his hair
    boxes = area_type(c, box, rows, "c", draw)
    return c, clearance(am, boxes), headroom(am)


def ai4(fmt):
    """4: a different man presents his glowing phone on a black cushion like a trophy, a giant dumbbell abandoned, acid
    yellow; Phosphate Solid near-black, flush-left tall stack, hero lines with a sharp white offset shadow."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai4_{fmt}.png").convert("RGB"), W, H)
    box = area(PLAN[4], fmt)
    if fmt == "9x16":  # Codex's left column is too narrow for phone-size type: shrink the picture into the bottom right
        k = 0.66; sm = c.resize((round(W * k), round(H * k)), Image.LANCZOS)
        bg = Image.new("RGB", (W, H), c.getpixel((5, 5)))
        edge = Image.new("L", sm.size, 0); ImageDraw.Draw(edge).rectangle([24, 24, sm.width, sm.height], fill=255)
        bg.paste(sm, (W - sm.width, H - sm.height), edge.filter(ImageFilter.GaussianBlur(12))); c = bg
        box = (0.05, 0.03, 0.95, 0.36)
    am = person(c, f"ai4_{fmt}")
    ink = hexc("#111111")
    draw = lambda d, x, y, t, f, col: put(d, x, y, t, f, ink, max(6, f.size // 16) if col == "hero" else 0, WHITE)
    rows = ([("THE FIRST", phos, 0.55, "lead"), ("STEP", phos, 0.55, "lead"), ("ISN'T A", phos, 1.0, "hero"), ("WORKOUT", phos, 1.0, "hero")]
            if fmt == "16x9" else  # 9:16: three lines across the top
            [(A, phos, 0.55, "lead"), ("ISN'T A", phos, 1.0, "hero"), ("WORKOUT", phos, 1.0, "hero")])
    boxes = area_type(c, box, rows, "l", draw, gapk=0.08)
    return c, clearance(am, boxes), headroom(am)


def ai5(fmt):
    """5: a giant phone showing a different man's goal portrait set in sprint starting blocks on a petrol-teal track;
    Futura Bold flush right, THE FIRST STEP aqua, ISN'T A / WORKOUT off-white with a thin aqua underline."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai5_{fmt}.png").convert("RGB"), W, H)
    am = person(c, f"ai5_{fmt}")  # the man on the phone screen
    aqua, ice = hexc("#3DE8DD"), hexc("#EAF3F5")
    def draw(d, x, y, t, f, col):
        b = put(d, x, y, t, f, col)
        if t == "WORKOUT":
            uy = b[3] + max(8, f.size // 10); hh = max(5, f.size // 22)
            d.rectangle([b[0], uy, b[2], uy + hh], fill=aqua); b = (b[0], b[1], b[2], uy + hh)
        return b
    rows = [(A, futura, 0.42, aqua), ("ISN'T A", futura, 1.0, ice), ("WORKOUT", futura, 1.0, ice)]
    boxes = area_type(c, area(PLAN[5], fmt), rows, "r", draw, gapk=0.10)
    return c, clearance(am, boxes), 9999


JOBS = {
    1: ("pool-photo-125-white-band", "Real pool photo: you flexing and smiling at golden hour, headline on a white band", pool),
    2: ("studio-blue-11-vision-board-card", "Real studio photo: you in front of a vision board, headline handwritten on a pinned card", board),
    3: ("ai-dan-print-cobalt-impact", "AI picture of you: holding up your goal print (its back to us), cobalt spotlight", ai3),
    4: ("ai-phone-trophy-acid-yellow", "AI: a guy presents his phone like a trophy, giant dumbbell abandoned, acid yellow", ai4),
    5: ("ai-phone-starting-blocks-teal", "AI: a giant phone with a goal picture set in sprint starting blocks, petrol teal", ai5),
}


def main():
    want = [int(a) for a in sys.argv[1:]] or sorted(JOBS)
    qp = os.path.join(HERE, "qc.json"); res = {f"{r['number']}-{r['fmt']}": r for r in (json.load(open(qp)) if os.path.exists(qp) else [])}
    for n in want:
        name, lab, fn = JOBS[n]
        for fmt in FMT:
            if not os.path.exists(f"{HERE}/assets/{fn.__name__}_{fmt}.png"): print(f"[{n} {fmt}] plate missing"); continue
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
    d.text((pad, 24), "The First Step To Getting Abs (RA-12 ad): five thumbnail choices", font=font(40), fill=(20, 22, 28))
    d.text((pad, 80), "Left: 9:16 (the ad's shape). Right: the 16:9 version. All made with Codex. Pick one number.", font=font(24), fill=(70, 72, 80))
    for i, n in enumerate(sorted(JOBS)):
        y = 140 + i * rowh
        sheet.paste(Image.open(os.path.join(OUT, by[(n, "9x16")]["file"])).resize((w9, h9), Image.LANCZOS), (pad + 60, y))
        sheet.paste(Image.open(os.path.join(OUT, by[(n, "16x9")]["file"])).resize((w16, h16), Image.LANCZOS), (pad * 2 + 60 + w9, y))
        d.text((pad, y + 4), str(n), font=font(52), fill=(20, 22, 28))
        d.text((pad + 60, y + h9 + 10), JOBS[n][1], font=font(24), fill=(40, 42, 50))
    sp = os.path.join(OUT, "REVIEW_first-step-abs-five-options.jpg"); sheet.save(sp, quality=88); print(sp)


if __name__ == "__main__":
    main()
