#!/usr/bin/env python3
"""RA-12 thumbnails, round 2 (Dan, 2026-10-21): "I don't like any of these. I want three new designs with image number 2
and two other similar images. Change the text to 'The key to getting abs' and make three unique designs."
Image 2 = his real studio-blue-11 cutout (smiling, hands on hips); the two similar ones are studio-blue-222 and
studio-blue-145 (same smile and pose, unused on any ad). Codex (GPT-6.1 Sol, high) planned the three designs and made the
three background plates (r2/plan.json); his real cutouts are layered on and all type is set here.
Run: python3 build_r2.py [A B C]"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as R1  # round 1 helpers (and, through it, the RA-06 ones)

K = R1.K; FMT = R1.FMT; PH = R1.PH; OUT = R1.OUT
HERE = R1.HERE + "/r2"; K.HERE = HERE
tw, th, cover, paste_cut, person, clearance, headroom, fit, trimmed, font = (
    K.tw, K.th, K.cover, K.paste_cut, K.person, K.clearance, K.headroom, K.fit, K.trimmed, K.font)
hexc, place = R1.hexc, R1.place
SLUG = "key-to-abs"
SUP = "/System/Library/Fonts/Supplemental/"
arialblack = lambda z: ImageFont.truetype(SUP + "Arial Black.ttf", z)
impact = lambda z: ImageFont.truetype(SUP + "Impact.ttf", z)
rockwell = lambda z: ImageFont.truetype(SUP + "Rockwell.ttc", z, index=2)  # Bold
PLAN = {o["letter"]: o for o in json.load(open(f"{HERE}/plan.json"))["options"]}
WHITE = (255, 255, 255)


def area(L, fmt): return tuple(float(v) for v in PLAN[L][f"headline_area_{fmt}"].split(","))


def cutout(name, keep, c, fmt, side, ph, inset=60):
    W, H = FMT[fmt]
    cut = trimmed(f"{PH}/_cutouts/studio-{name}_CUTOUT.png", keep)
    s = ph / cut.height; w = round(cut.width * s)
    x = {"c": (W - w) // 2, "l": inset, "r": W - w - inset}[side] if isinstance(side, str) else round(side * W - w / 2)
    return paste_cut(c, cut, x, H - ph, s)


def stack(c, box, rows, align, draw, gapk=0.06):
    """rows: [(segments [(text, colour)], make, scale)]; the tightest row sets the size inside the fractional box."""
    W, H = c.size; x0, y0, x1, y1 = box[0] * W, box[1] * H, box[2] * W, box[3] * H
    aw, ah = x1 - x0, y1 - y0
    txt = lambda r: "".join(t for t, _ in r[0])
    s = min(fit(lambda z, r=r: r[1](max(8, round(z * r[2]))), txt(r), aw * 0.94, 600) for r in rows)
    while True:
        fs = [(r[0], r[1](round(s * r[2]))) for r in rows]
        gap = round(s * gapk); tot = sum(th(f, "".join(t for t, _ in sg)) for sg, f in fs) + gap * (len(fs) - 1)
        if tot <= ah * 0.94 or s < 40: break
        s -= 4
    d = ImageDraw.Draw(c); y = y0 + (ah - tot) / 2; boxes = []
    for sg, f in fs:
        full = "".join(t for t, _ in sg); w = tw(f, full)
        x = x0 if align == "l" else (x1 - w if align == "r" else x0 + (aw - w) / 2)
        boxes.append(draw(d, round(x), round(y), sg, f)); y += th(f, full) + gap
    return boxes


def segs(d, x, y, sg, f, fill_fn):
    """Draw segments left to right on one baseline; fill_fn(d, x, y, text, colour, font, bbox_origin)."""
    full = "".join(t for t, _ in sg); b = f.getbbox(full); cx = x - b[0]
    for t, col in sg:
        fill_fn(d, cx, y - b[1], t, col, f); cx += f.getlength(t)
    return (x, y, x + tw(f, full), y + th(f, full))


def vault(fmt):
    """A: real studio-blue-11 in front of an open steel vault with an oversized gold key, deep navy; Arial Black stack
    THE KEY / TO GETTING / ABS, KEY and ABS gold, the rest white, navy outline and a hard black drop."""
    W, H = FMT[fmt]
    # 16:9 uses A2 (Dan, round 3: "move the text up and make the key fully visible beneath the text"): Codex moved the
    # key left onto open floor (x 215-1000, y 655-960) so his body no longer hides its toothed end.
    c = cover(Image.open(f"{HERE}/{'A' if fmt == '9x16' else 'A2'}_{fmt}.png").convert("RGB"), W, H)
    c, am = cutout("blue-11", 0.86, c, fmt, "c" if fmt == "9x16" else "r", 1250 if fmt == "9x16" else 1030)
    gold, navy = hexc("#FFD348"), hexc("#06172D")
    def fill(d, x, y, t, col, f):
        sw = max(4, f.size // 22); off = max(6, f.size // 14)
        d.text((x + off, y + off), t, font=f, fill=(0, 0, 0), stroke_width=sw, stroke_fill=(0, 0, 0))
        d.text((x, y), t, font=f, fill=col, stroke_width=sw, stroke_fill=navy)
    def draw(d, x, y, sg, f):
        bx = segs(d, x, y, sg, f, fill); sw = max(4, f.size // 22); off = max(6, f.size // 14)
        return (bx[0] - sw, bx[1] - sw, bx[2] + sw + off, bx[3] + sw + off)
    rows = [([("THE ", WHITE), ("KEY", gold)], arialblack, 0.80), ([("TO GETTING", WHITE)], arialblack, 0.62), ([("ABS", gold)], arialblack, 1.0)]
    box = area("A", fmt)
    box = (box[0], 0.025, box[2], 0.33) if fmt == "9x16" else (0.04, 0.04, 0.58, 0.565)  # 16:9: text above the key
    boxes = stack(c, box, rows, "c" if fmt == "9x16" else "l", draw, gapk=0.13)
    return c, clearance(am, boxes), headroom(am)


def band(text, f, angle):
    """Black Impact on a solid acid-yellow band, tilted, with a hard dark-blue offset shadow."""
    padx, pady = round(f.size * 0.22), round(f.size * 0.14)
    w, h = tw(f, text) + 2 * padx, th(f, text) + 2 * pady; o = max(8, f.size // 12)
    t = Image.new("RGBA", (w + o + 20, h + o + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle([10 + o, 10 + o, 10 + o + w, 10 + o + h], fill=hexc("#062463") + (255,))
    d.rectangle([10, 10, 10 + w, 10 + h], fill=hexc("#F5FF36") + (255,))
    b = f.getbbox(text); d.text((10 + padx - b[0], 10 + pady - b[1]), text, font=f, fill=hexc("#07111E"))
    return t.rotate(angle, expand=True, resample=Image.BICUBIC)


def frame(fmt):
    """B: real studio-blue-222 standing inside a glowing cyan picture frame on cobalt (the picture is the key); Impact
    THE KEY TO / GETTING ABS in black on two acid-yellow bands tilted opposite ways."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/B_{fmt}.png").convert("RGB"), W, H)
    if fmt == "9x16": c, am = cutout("blue-222", 0.86, c, fmt, "c", 1230)
    else: c, am = cutout("blue-222", 0.86, c, fmt, 0.16, 1000)
    x0, y0, x1, y1 = [v * s for v, s in zip(area("B", fmt), (W, H, W, H))]
    l1, l2 = "THE KEY TO", "GETTING ABS"
    s = fit(impact, l2, (x1 - x0) * 0.82, 400)
    t1, t2 = band(l1, impact(round(s * 0.86)), 3), band(l2, impact(s), -2)
    while t1.height + t2.height - 10 > (y1 - y0) and s > 40:
        s -= 4; t1, t2 = band(l1, impact(round(s * 0.86)), 3), band(l2, impact(s), -2)
    top = y0 + ((y1 - y0) - (t1.height + t2.height - 10)) / 2
    cx = (x0 + x1) / 2
    c, b1 = place(c, t1, round(cx - t1.width / 2), round(top))
    c, b2 = place(c, t2, round(cx - t2.width / 2), round(top + t1.height - 10))
    return c, clearance(am, [b1, b2]), headroom(am)


def key(fmt):
    """C: real studio-blue-145 beside a giant chrome key hanging in an orange-lit concrete room; Rockwell Bold flush
    left, THE KEY TO / GETTING warm white, ABS in vivid orange about 1.6x, soft black shadow."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/C_{fmt}.png").convert("RGB"), W, H)
    if fmt == "9x16": c, am = cutout("blue-145", 0.86, c, fmt, 0.44, 1200)
    else: c, am = cutout("blue-145", 0.86, c, fmt, "r", 1030)
    cream, orange = hexc("#FFF4DE"), hexc("#FF7A16")
    def draw(d, x, y, sg, f):
        full = "".join(t for t, _ in sg); b = f.getbbox(full)
        sh = Image.new("L", c.size, 0); ImageDraw.Draw(sh).text((x - b[0] + 6, y - b[1] + 8), full, font=f, fill=200)
        c.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(max(6, f.size // 18))))
        return segs(ImageDraw.Draw(c), x, y, sg, f, lambda d2, xx, yy, t, col, ff: d2.text((xx, yy), t, font=ff, fill=col))
    rows = [([("THE KEY TO", cream)], rockwell, 0.62), ([("GETTING", cream)], rockwell, 0.62), ([("ABS", orange)], rockwell, 1.0)]
    boxes = stack(c, area("C", fmt), rows, "l", draw, gapk=0.12)
    return c, clearance(am, boxes), headroom(am)


JOBS = {
    "A": ("vault-gold-key-studio-blue-11", "A: you in front of an open vault with a gold key, gold and white block type", vault),
    "B": ("glow-frame-yellow-bands-studio-blue-222", "B: you inside a glowing picture frame on cobalt, black type on two yellow bands", frame),
    "C": ("chrome-key-orange-room-studio-blue-145", "C: you beside a giant chrome key in an orange-lit room, slab-serif type, ABS in orange", key),
}


def main():
    want = sys.argv[1:] or sorted(JOBS)
    qp = os.path.join(HERE, "qc.json"); res = {f"{r['letter']}-{r['fmt']}": r for r in (json.load(open(qp)) if os.path.exists(qp) else [])}
    for L in want:
        name, lab, fn = JOBS[L]
        for fmt in FMT:
            canvas, clear, head = fn(fmt)
            f_ = f"{SLUG}_r2-{L}-{name} | {fmt}.jpg"; p = os.path.join(OUT, f_); canvas.save(p, quality=92)
            ok = clear >= 25 and head >= 14 and os.path.getsize(p) < 2_000_000
            print(f"[{L} {fmt}] clearance {clear}px, headroom {head}px, {os.path.getsize(p)//1024}KB -> {'PASS' if ok else 'FAIL'}")
            res[f"{L}-{fmt}"] = dict(letter=L, fmt=fmt, name=name, label=lab, file=f_, clearance_px=clear, headroom_px=head, ok=bool(ok))
    res = [res[k] for k in sorted(res)]
    json.dump(res, open(qp, "w"), indent=2)
    if len(res) != 6: return
    by = {(r["letter"], r["fmt"]): r for r in res}
    pad, w9, h9, w16, h16 = 30, 360, 640, 1138, 640; rowh = h9 + 70
    sheet = Image.new("RGB", (pad * 4 + 60 + w9 + w16, 150 + 3 * rowh), (242, 242, 244)); d = ImageDraw.Draw(sheet)
    d.text((pad, 24), "The Key To Getting Abs (RA-12 ad): round 2, three designs", font=font(40), fill=(20, 22, 28))
    d.text((pad, 80), "Real studio photos (A is your option 2 photo). Left: 9:16. Right: 16:9. Pick a letter.", font=font(24), fill=(70, 72, 80))
    for i, L in enumerate(sorted(JOBS)):
        y = 140 + i * rowh
        sheet.paste(Image.open(os.path.join(OUT, by[(L, "9x16")]["file"])).resize((w9, h9), Image.LANCZOS), (pad + 60, y))
        sheet.paste(Image.open(os.path.join(OUT, by[(L, "16x9")]["file"])).resize((w16, h16), Image.LANCZOS), (pad * 2 + 60 + w9, y))
        d.text((pad, y + 4), L, font=font(52), fill=(20, 22, 28))
        d.text((pad + 60, y + h9 + 10), JOBS[L][1], font=font(24), fill=(40, 42, 50))
    sp = os.path.join(OUT, "REVIEW_key-to-abs-round2-three-designs.jpg"); sheet.save(sp, quality=88); print(sp)


if __name__ == "__main__":
    main()
