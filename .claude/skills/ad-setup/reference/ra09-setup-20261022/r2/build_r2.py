#!/usr/bin/env python3
"""RA-09 thumbnails round 2, 2026-10-22. Dan picked the feel of round 1 option 2 (real studio photo on a wired globe) and
asked for three new designs, all with a real photo of him: USE AI TO GET REAL ABS on his left, and on his right, larger
than usual, the disclosure REAL PHOTO OF ME, NOT AI-GENERATED (house wording, AGENTS 2026-10-17). Codex (GPT-6.1 Sol,
high) planned the three designs and made the background plates (r2/plan.json); his real cutouts are layered in code,
never redrawn; all type is set here. Run: python3 build_r2.py [A B C]"""
import importlib.util, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OUT = PROJ + "/social media graphics/youtube/thumbnails/RA-09 Do You Think AI Is Changing The World/r2"
HERE = PROJ + "/social media graphics/youtube/thumbnails/RA-09 Do You Think AI Is Changing The World/_build-2026-10-22/r2"
_spec = importlib.util.spec_from_file_location("ra06b", PROJ + "/social media graphics/youtube/thumbnails/RA-06 Whats The Best Ab Exercise/_build-2026-10-16/build.py")
K = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(K)
font, tw, th, cover, paste_cut, clearance, headroom, trimmed = K.font, K.tw, K.th, K.cover, K.paste_cut, K.clearance, K.headroom, K.trimmed
FMT = K.FMT; PH = K.PH
hexc = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
SYS, SUP = "/System/Library/Fonts/", "/System/Library/Fonts/Supplemental/"
impact = lambda z: ImageFont.truetype(SUP + "Impact.ttf", z)
avenir = lambda z: ImageFont.truetype(SYS + "Avenir Next Condensed.ttc", z, index=8)   # Heavy
futc = lambda z: ImageFont.truetype(SUP + "Futura.ttc", z, index=4)                    # Condensed ExtraBold
hncb = lambda z: ImageFont.truetype(SYS + "HelveticaNeue.ttc", z, index=9)             # Condensed Black
din = lambda z: ImageFont.truetype(SUP + "DIN Condensed Bold.ttf", z)
ablack = lambda z: ImageFont.truetype(SUP + "Arial Black.ttf", z)
# headline lines: each a list of (word, emphasis?)
HEAD = [[("USE ", 0), ("AI", 1)], [("TO GET", 0)], [("REAL ABS", 1)]]
LABEL = ["REAL PHOTO", "OF ME, NOT", "AI-GENERATED"]
DESIGNS = {
    "A": dict(photo="studio-gray-67", name="midnight-city-cyan", lab="Midnight city with cyan light, white and cyan Impact, outlined badge"),
    "B": dict(photo="studio-white-59", name="circuit-mountains-lime", lab="Circuit mountains, lime type on black bands, lime capsule"),
    "C": dict(photo="studio-blue-150", name="data-center-crimson-gold", lab="Crimson data centre, ivory type with red underlines, gold stamp"),
}


def seg_w(f, segs): return tw(f, "".join(s for s, _ in segs))


def fit_lines(make, lines, width, height, gapk, start=400):
    s = start
    while s > 20:
        f = make(s)
        if max(seg_w(f, l) for l in lines) <= width and sum(th(f, "".join(w for w, _ in l)) for l in lines) + gapk * s * (len(lines) - 1) <= height:
            return f
        s -= 2
    return make(20)


def draw_segs(d, x, y, segs, f, cols, shadow=None, off=0):
    b0 = f.getbbox("".join(s for s, _ in segs))
    xx = x
    for s, e in segs:
        if shadow: d.text((xx - b0[0] + off, y - b0[1] + off), s, font=f, fill=shadow)
        d.text((xx - b0[0], y - b0[1]), s, font=f, fill=cols[e]); xx += f.getlength(s)


def columns(am, fmt):
    """The free boxes left and right of Dan. 16:9: full height beside him. 9:16: upper left and upper right, above his head."""
    W, H = FMT[fmt]; ys, xs = np.where(am)
    if fmt == "16x9":
        return (50, 70, int(xs.min()) - 50, H - 70), (int(xs.max()) + 50, 70, W - 50, H - 70)
    top = int(ys.min())  # 9:16: the empty space above his head, split into an upper-left and an upper-right column
    return (40, 60, W // 2 - 20, top - 30), (W // 2 + 20, 60, W - 40, top - 30)


def headline(c, box, HEAD, D):
    x0, y0, x1, y1 = box; W = x1 - x0; Hh = y1 - y0; d = ImageDraw.Draw(c); boxes = []
    if D == "A":
        f = fit_lines(impact, HEAD, W * 0.96, Hh * 0.8, 0.06); gap = round(f.size * 0.06)
        cols = {0: (255, 255, 255), 1: hexc("#49EAFF")}
        tot = sum(th(f, "".join(w for w, _ in l)) for l in HEAD) + gap * 2; y = y0 + (Hh - tot) // 2
        glow = Image.new("L", c.size, 0); gd = ImageDraw.Draw(glow); yy = y
        for l in HEAD:
            draw_segs(gd, x0, yy, l, f, {0: 255, 1: 255}); yy += th(f, "".join(w for w, _ in l)) + gap
        g = Image.new("RGBA", c.size, hexc("#00CFFF") + (0,)); g.putalpha(glow.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.55)))
        c.paste(Image.alpha_composite(c.convert("RGBA"), g).convert("RGB")); d = ImageDraw.Draw(c)
        for l in HEAD:
            draw_segs(d, x0, y, l, f, cols, hexc("#020A16"), max(5, f.size // 18))
            hh = th(f, "".join(w for w, _ in l)); boxes.append((x0, y, x0 + seg_w(f, l) + f.size // 18, y + hh + f.size // 18)); y += hh + gap
    elif D == "B":
        padx, pady = 0.10, 0.12
        f = fit_lines(futc, HEAD, W * 0.96 / (1 + 2 * padx * 0.4), Hh * 0.62, 0.40); gap = round(f.size * 0.16)
        tot = sum(th(f, "".join(w for w, _ in l)) + 2 * round(f.size * pady) for l in HEAD) + gap * 2; y = y0 + (Hh - tot) // 2
        for l in HEAD:
            t = "".join(w for w, _ in l); px, py = round(f.size * padx), round(f.size * pady)
            bw, bh = seg_w(f, l) + 2 * px, th(f, t) + 2 * py
            d.rectangle([x0, y, x0 + bw, y + bh], fill=hexc("#071117"))
            draw_segs(d, x0 + px, y + py, l, f, {0: hexc("#C7FF28"), 1: hexc("#C7FF28")}, hexc("#1749CC"), max(4, f.size // 22))
            boxes.append((x0, y, x0 + bw, y + bh)); y += bh + gap
    else:
        f = fit_lines(din, HEAD, W * 0.94, Hh * 0.72, 0.30); gap = round(f.size * 0.20)
        tot = sum(th(f, "".join(w for w, _ in l)) for l in HEAD) + gap * 2; y = y0 + (Hh - tot) // 2
        ivory, ink, red = hexc("#FFF2D5"), hexc("#110C0D"), hexc("#FF3038")
        for l in HEAD:
            t = "".join(w for w, _ in l); hh = th(f, t); b0 = f.getbbox(t); sw = max(3, f.size // 26)
            d.text((x0 - b0[0] + sw * 2, y - b0[1] + sw * 2), t, font=f, fill=(0, 0, 0))
            d.text((x0 - b0[0], y - b0[1]), t, font=f, fill=ivory, stroke_width=sw, stroke_fill=ink)
            xx = x0
            for s, e in l:
                wpx = f.getlength(s.rstrip())
                if e: d.rectangle([xx, y + hh + gap * 0.18, xx + wpx, y + hh + gap * 0.18 + max(8, f.size // 11)], fill=red)
                xx += f.getlength(s)
            boxes.append((x0, y, x0 + seg_w(f, l) + sw * 2, y + hh + round(gap * 0.18) + max(8, f.size // 11))); y += hh + gap
    return boxes


def label(c, box, LABEL, D):
    x0, y0, x1, y1 = box; W = x1 - x0; Hh = y1 - y0; d = ImageDraw.Draw(c)
    lines = [[(t, 0)] for t in LABEL]
    mk = {"A": avenir, "B": hncb, "C": ablack}[D]
    pad = 0.30
    f = fit_lines(mk, lines, W * 0.92 / (1 + pad * 0.5), Hh * 0.70, 0.22, 200)
    gap = round(f.size * 0.22); p = round(f.size * pad)
    tw_ = max(seg_w(f, l) for l in lines); tot = sum(th(f, l[0][0]) for l in lines) + gap * (len(lines) - 1)
    bw, bh = tw_ + 2 * p, tot + 2 * p + (round(f.size * 0.5) if D == "C" else 0)
    bx = x0 + (W - bw) // 2; by = y0 + (Hh - bh) // 2
    if D == "A":
        d.rectangle([bx, by, bx + bw, by + bh], fill=hexc("#061522"), outline=hexc("#49EAFF"), width=max(4, f.size // 12)); col = (255, 255, 255)
    elif D == "B":
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=round(min(bw, bh) * 0.28), fill=hexc("#C7FF28"), outline=(255, 255, 255), width=max(3, f.size // 16)); col = hexc("#071117")
    else:
        g = hexc("#FFB84A"); lw = max(3, f.size // 16)
        d.rectangle([bx, by, bx + bw, by + bh], fill=hexc("#170B0D"), outline=g, width=lw)
        d.rectangle([bx + lw * 3, by + lw * 3, bx + bw - lw * 3, by + bh - lw * 3], outline=g, width=max(2, lw // 2)); col = hexc("#FFF2D5")
    y = by + p
    for i, l in enumerate(lines):
        t = l[0][0]; b = f.getbbox(t)
        d.text((bx + (bw - tw(f, t)) // 2 - b[0], y - b[1]), t, font=f, fill=col); y += th(f, t) + gap
        if D == "C" and i == 1:
            ex = round(f.size * 0.5); dh = max(5, f.size // 10); mid = y - gap + (gap + ex) / 2
            dw = bw * 0.3; d.rectangle([bx + (bw - dw) / 2, mid - dh / 2, bx + (bw + dw) / 2, mid + dh / 2], fill=hexc("#FF3038")); y += ex
    return [(bx, by, bx + bw, by + bh)]


def build(D, fmt):
    W, H = FMT[fmt]; cfg = DESIGNS[D]; plan = PLAN[D]
    c = cover(Image.open(f"{HERE}/{D}_{fmt}.png").convert("RGB"), W, H)
    c = Image.blend(c, Image.new("RGB", (W, H), (0, 0, 0)), 0.10)
    cut = trimmed(f"{PH}/_cutouts/{cfg['photo']}_CUTOUT.png", 0.80)
    ph = 1010 if fmt == "16x9" else 1260
    s = ph / cut.height; x = (W - round(cut.width * s)) // 2; y = H - ph
    canvas, am = paste_cut(c, cut, x, y, s, glow=hexc(plan["rim_light"]))
    lb, rb = columns(am, fmt)
    boxes = headline(canvas, lb, HEAD, D) + label(canvas, rb, LABEL, D)
    return canvas, clearance(am, boxes), headroom(am), lb, rb


PLAN = {p["letter"]: p for p in json.load(open(f"{HERE}/plan.json"))["designs"]}


def main():
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or sorted(DESIGNS); res = {}
    qp = f"{HERE}/qc.json"; res = {f"{r['design']}-{r['fmt']}": r for r in (json.load(open(qp)) if os.path.exists(qp) else [])}
    for D in want:
        for fmt in FMT:
            if not os.path.exists(f"{HERE}/{D}_{fmt}.png"): print(f"[{D} {fmt}] plate missing"); continue
            canvas, clear, head, lb, rb = build(D, fmt)
            fn = f"ai-changing-world-r2_{D}-{DESIGNS[D]['name']} | {fmt}.jpg"; p = os.path.join(OUT, fn); canvas.save(p, quality=92)
            ok = clear >= 25 and head >= 14 and os.path.getsize(p) < 2_000_000
            print(f"[{D} {fmt}] clearance {clear}px, headroom {head}px, cols {lb[2]-lb[0]}/{rb[2]-rb[0]}px, {os.path.getsize(p)//1024}KB -> {'PASS' if ok else 'FAIL'}")
            res[f"{D}-{fmt}"] = dict(design=D, fmt=fmt, file=fn, clearance_px=clear, headroom_px=head, ok=bool(ok))
    res = [res[k] for k in sorted(res)]; json.dump(res, open(qp, "w"), indent=2)
    if len(res) != 6: return
    by = {(r["design"], r["fmt"]): r for r in res}
    pad, w9, h9, w16, h16 = 30, 360, 640, 1138, 640; rowh = h9 + 70
    sheet = Image.new("RGB", (pad * 4 + 60 + w9 + w16, 150 + 3 * rowh), (242, 242, 244)); d = ImageDraw.Draw(sheet)
    d.text((pad, 24), "Do You Think AI Is Changing The World? (RA-09 ad): round 2, three designs", font=font(40), fill=(20, 22, 28))
    d.text((pad, 80), "All real photos of you; backgrounds by Codex. Left: 9:16 (installed). Right: 16:9. Pick one letter.", font=font(24), fill=(70, 72, 80))
    for i, D in enumerate(sorted(DESIGNS)):
        y = 140 + i * rowh
        sheet.paste(Image.open(os.path.join(OUT, by[(D, "9x16")]["file"])).resize((w9, h9), Image.LANCZOS), (pad + 60, y))
        sheet.paste(Image.open(os.path.join(OUT, by[(D, "16x9")]["file"])).resize((w16, h16), Image.LANCZOS), (pad * 2 + 60 + w9, y))
        d.text((pad, y + 4), D, font=font(52), fill=(20, 22, 28))
        d.text((pad + 60, y + h9 + 10), DESIGNS[D]["lab"], font=font(24), fill=(40, 42, 50))
    sp = os.path.join(OUT, "..", "REVIEW_ai-changing-world-round2.jpg"); sheet.save(sp, quality=88); print(os.path.abspath(sp))


if __name__ == "__main__":
    main()
