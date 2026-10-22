#!/usr/bin/env python3
"""RA-09 thumbnails round 3, 2026-10-22. Dan: three real pool-shoot photos with their natural background, USE AI TO GET
REAL ABS and REAL PHOTO OF ME, NOT AI-GENERATED (house wording) on either side; in the vertical the headline on top and
the label at the bottom. Photos 247, 230, 13. Where a frame is wider or taller than the photo, Codex (GPT-6.1 Sol, high)
continued the photo's own scenery into the empty area (prep_r3.py); the real photo is pasted back over its region here,
feathered only at the seam, so Dan is never redrawn. All type is set here. Run: python3 build_r3.py [p247 p230 p13]"""
import importlib.util, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
PH = PROJ + "/photos/finalized social media photos"
TOP = PROJ + "/social media graphics/youtube/thumbnails/RA-09 Do You Think AI Is Changing The World"
OUT, HERE = TOP + "/r3", TOP + "/_build-2026-10-22/r3"
_spec = importlib.util.spec_from_file_location("ra06b", TOP + "/../RA-06 Whats The Best Ab Exercise/_build-2026-10-16/build.py")
K = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(K)
K.HERE = HERE
font, tw, th, person, clearance, headroom = K.font, K.tw, K.th, K.person, K.clearance, K.headroom
FMT = K.FMT
hexc = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
SYS, SUP = "/System/Library/Fonts/", "/System/Library/Fonts/Supplemental/"
futc = lambda z: ImageFont.truetype(SUP + "Futura.ttc", z, index=4)          # Condensed ExtraBold
ablack = lambda z: ImageFont.truetype(SUP + "Arial Black.ttf", z)
impact = lambda z: ImageFont.truetype(SUP + "Impact.ttf", z)
avenir = lambda z: ImageFont.truetype(SYS + "Avenir Next Condensed.ttc", z, index=8)  # Heavy
hncb = lambda z: ImageFont.truetype(SYS + "HelveticaNeue.ttc", z, index=9)            # Condensed Black
PLACE = json.load(open(f"{HERE}/place.json"))
# headline lines as (word, accent?) segments; 9:16 runs two wide lines on top, 16:9 three lines on the left
HEAD = {"9x16": [[("USE AI TO GET", 0)], [("REAL ABS", 1)]], "16x9": [[("USE ", 0), ("AI", 1)], [("TO GET", 0)], [("REAL ABS", 1)]]}
LABEL = {"9x16": ["REAL PHOTO OF ME,", "NOT AI-GENERATED"], "16x9": ["REAL PHOTO", "OF ME, NOT", "AI-GENERATED"]}
DESIGNS = {
    "p247": dict(name="pool-247-yellow", lab="Pool photo 247: standing in the pool, white and yellow Futura, white pill label",
                 head=futc, ink=(255, 255, 255), accent=hexc("#FFD43B"), shadow=hexc("#06202E"),
                 lab_font=hncb, lab_fill=(255, 255, 255), lab_ink=hexc("#0B2A3C"), lab_border=None, lab_shape="pill"),
    "p230": dict(name="pool-230-orange", lab="Pool photo 230: towel round your neck, white and orange Arial Black, black box label",
                 head=ablack, ink=(255, 255, 255), accent=hexc("#FF8A1F"), shadow=(0, 0, 0),
                 lab_font=ablack, lab_fill=hexc("#0C0C0E"), lab_ink=(255, 255, 255), lab_border=hexc("#FF8A1F"), lab_shape="box"),
    "p13": dict(name="pool-13-lime", lab="Pool photo 13: by the trees, white and lime Impact, lime badge label",
                head=impact, ink=(255, 255, 255), accent=hexc("#C7FF28"), shadow=hexc("#0A1408"),
                lab_font=avenir, lab_fill=hexc("#C7FF28"), lab_ink=hexc("#0A1408"), lab_border=None, lab_shape="badge"),
}


def compose(key, fmt):
    """Codex's extended scene, with the real photo pasted back over its own region (feathered only on fill sides)."""
    W, H = FMT[fmt]; p = PLACE[f"{key}_{fmt}"]
    photo = Image.open(f"{HERE}/{key}_{fmt}_canvas.png").convert("RGB")
    if not p["needs_fill"]: return photo
    fill = Image.open(f"{HERE}/{key}_{fmt}_fill.png").convert("RGB").resize((W, H), Image.LANCZOS)
    x, y, w, h = p["x"], p["y"], p["w"], p["h"]; m, pad = 40, 80
    rect = [x + (m if x > 0 else -pad), y + (m if y > 0 else -pad), x + w - (m if x + w < W else -pad), y + h - (m if y + h < H else -pad)]
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rectangle(rect, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    region = Image.new("L", (W, H), 0); ImageDraw.Draw(region).rectangle([x, y, x + w - 1, y + h - 1], fill=255)
    mask = Image.fromarray(np.minimum(np.asarray(mask), np.asarray(region)))  # never show grey outside the photo
    return Image.composite(photo, fill, mask)


def shade(c, box, side, strength=0.62):
    """A soft dark gradient behind a type area so it reads over the photo."""
    W, H = c.size; g = np.zeros((H, W), np.float32); x0, y0, x1, y1 = box
    if side == "top": g[:y1 + 120] = np.clip(1 - (np.arange(y1 + 120) - y1 * 0.55) / (y1 * 0.45 + 120), 0, 1)[:, None]
    elif side == "bottom": r = np.arange(H); g[:] = np.clip((r - (y0 - 140)) / ((y1 - y0) * 0.5 + 140), 0, 1)[:, None]
    elif side == "left": cc = np.arange(W); g[:] = np.clip(1 - (cc - x1 * 0.6) / (x1 * 0.4 + 160), 0, 1)[None, :]
    else: cc = np.arange(W); g[:] = np.clip((cc - (x0 - 160)) / ((x1 - x0) * 0.4 + 160), 0, 1)[None, :]
    a = Image.fromarray((g * 255 * strength).astype(np.uint8))
    return Image.composite(Image.new("RGB", (W, H), (4, 8, 12)), c, a)


def fit(make, lines, width, height, gapk, start=420):
    s = start
    while s > 20:
        f = make(s)
        if max(tw(f, "".join(t for t, _ in l)) for l in lines) <= width and \
           sum(th(f, "".join(t for t, _ in l)) for l in lines) + gapk * s * (len(lines) - 1) <= height:
            return f
        s -= 2
    return make(20)


def headline(c, box, lines, D, align):
    x0, y0, x1, y1 = box; d = ImageDraw.Draw(c)
    f = fit(D["head"], lines, (x1 - x0) * 0.98, (y1 - y0) * 0.92, 0.08); gap = round(f.size * 0.08)
    tot = sum(th(f, "".join(t for t, _ in l)) for l in lines) + gap * (len(lines) - 1); y = y0 + ((y1 - y0) - tot) // 2
    off = max(4, f.size // 20); boxes = []
    for l in lines:
        full = "".join(t for t, _ in l); b = f.getbbox(full); wl = tw(f, full); hl = th(f, full)
        x = x0 if align == "l" else x0 + ((x1 - x0) - wl) // 2; xx = x
        for t, e in l:
            d.text((xx - b[0] + off, y - b[1] + off), t, font=f, fill=D["shadow"])
            d.text((xx - b[0], y - b[1]), t, font=f, fill=D["accent"] if e else D["ink"]); xx += f.getlength(t)
        boxes.append((x, y, x + wl + off, y + hl + off)); y += hl + gap
    return boxes


def label(c, box, lines, D):
    x0, y0, x1, y1 = box; d = ImageDraw.Draw(c); pad = 0.34
    f = fit(D["lab_font"], [[(t, 0)] for t in lines], (x1 - x0) * 0.94 / (1 + pad * 0.6), (y1 - y0) * 0.66, 0.24, 220)
    gap = round(f.size * 0.24); p = round(f.size * pad)
    tw_ = max(tw(f, t) for t in lines); tot = sum(th(f, t) for t in lines) + gap * (len(lines) - 1)
    bw, bh = tw_ + 2 * p, tot + 2 * p; bx = x0 + ((x1 - x0) - bw) // 2; by = y0 + ((y1 - y0) - bh) // 2
    r = {"pill": round(min(bh // 2, bw * 0.10)), "badge": round(bh * 0.18), "box": 0}[D["lab_shape"]]
    lw = max(4, f.size // 12)
    d.rounded_rectangle([bx + 8, by + 10, bx + bw + 8, by + bh + 10], radius=r, fill=(0, 0, 0))  # drop shadow
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=r, fill=D["lab_fill"], outline=D["lab_border"], width=lw if D["lab_border"] else 0)
    y = by + p
    for t in lines:
        b = f.getbbox(t); d.text((bx + (bw - tw(f, t)) // 2 - b[0], y - b[1]), t, font=f, fill=D["lab_ink"]); y += th(f, t) + gap
    return [(bx, by, bx + bw + 8, by + bh + 10)]


def build(key, fmt):
    W, H = FMT[fmt]; D = DESIGNS[key]
    c = compose(key, fmt)
    am = person(c, f"{key}_{fmt}"); ys, xs = np.where(am); top = int(ys.min())
    if fmt == "9x16":
        hb = (50, 46, W - 50, top - 36); lb = (60, H - 240, W - 60, H - 30)
        c = shade(shade(c, hb, "top"), lb, "bottom", 0.55)
        boxes = headline(c, hb, HEAD[fmt], D, "c")
        lab = label(c, lb, LABEL[fmt], D)
        upper = am & (np.arange(H)[:, None] < top + 0.45 * (H - top))  # face, chest and abs; the label may sit over his legs
        return c, min(clearance(am, boxes), clearance(upper, lab)), headroom(am)
    band = am[: int(top + 0.6 * (H - top))]; cols = np.where(band.any(0))[0]
    hb = (50, 90, int(cols.min()) - 50, H - 90); lb = (int(cols.max()) + 50, 90, W - 50, H - 90)
    c = shade(shade(c, hb, "left"), lb, "right", 0.5)
    boxes = headline(c, hb, HEAD[fmt], D, "l") + label(c, lb, LABEL[fmt], D)
    return c, clearance(am, boxes), headroom(am)


def main():
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or list(DESIGNS)
    qp = f"{HERE}/qc.json"; res = {f"{r['design']}-{r['fmt']}": r for r in (json.load(open(qp)) if os.path.exists(qp) else [])}
    for key in want:
        for fmt in FMT:
            p = PLACE[f"{key}_{fmt}"]
            if p["needs_fill"] and not os.path.exists(f"{HERE}/{key}_{fmt}_fill.png"): print(f"[{key} {fmt}] fill missing"); continue
            canvas, clear, head = build(key, fmt)
            fn = f"ai-changing-world-r3_{DESIGNS[key]['name']} | {fmt}.jpg"; path = os.path.join(OUT, fn); canvas.save(path, quality=92)
            ok = clear >= 25 and os.path.getsize(path) < 2_000_000
            print(f"[{key} {fmt}] clearance {clear}px, headroom {head}px, {os.path.getsize(path)//1024}KB -> {'PASS' if ok else 'FAIL'}")
            res[f"{key}-{fmt}"] = dict(design=key, fmt=fmt, file=fn, clearance_px=clear, headroom_px=head, ok=bool(ok))
    res = [res[k] for k in sorted(res)]; json.dump(res, open(qp, "w"), indent=2)
    if len(res) != 6: return
    by = {(r["design"], r["fmt"]): r for r in res}
    pad, w9, h9, w16, h16 = 30, 360, 640, 1138, 640; rowh = h9 + 70
    sheet = Image.new("RGB", (pad * 4 + 60 + w9 + w16, 150 + 3 * rowh), (242, 242, 244)); d = ImageDraw.Draw(sheet)
    d.text((pad, 24), "Do You Think AI Is Changing The World? (RA-09 ad): round 3, pool photos", font=font(40), fill=(20, 22, 28))
    d.text((pad, 80), "Real pool-shoot photos, natural backgrounds. Left: 9:16 (installed). Right: 16:9. Pick one letter.", font=font(24), fill=(70, 72, 80))
    for i, key in enumerate(DESIGNS):
        y = 140 + i * rowh
        sheet.paste(Image.open(os.path.join(OUT, by[(key, "9x16")]["file"])).resize((w9, h9), Image.LANCZOS), (pad + 60, y))
        sheet.paste(Image.open(os.path.join(OUT, by[(key, "16x9")]["file"])).resize((w16, h16), Image.LANCZOS), (pad * 2 + 60 + w9, y))
        d.text((pad, y + 4), "ABC"[i], font=font(52), fill=(20, 22, 28))
        d.text((pad + 60, y + h9 + 10), DESIGNS[key]["lab"], font=font(24), fill=(40, 42, 50))
    sp = os.path.join(TOP, "REVIEW_ai-changing-world-round3.jpg"); sheet.save(sp, quality=88); print(sp)


if __name__ == "__main__":
    main()
