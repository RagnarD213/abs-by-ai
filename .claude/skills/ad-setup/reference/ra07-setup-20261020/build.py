#!/usr/bin/env python3
"""RA-07 "Fire Your Trainer" (AD, 9:16 film): five thumbnail options, each in 9:16 and 16:9, 2026-10-20.
Dan's standard mix (VIDEO-RULES, 2026-10-13): 1 pool photo, 1 studio photo, 1 AI image of Dan, 2 AI images of Codex's
choice. Codex (GPT-6.1 Sol, high) made every plate and AI image and chose the concepts and type of options 3 to 5
(assets/plan.json in the media build folder). Options 1 and 2 are his real cutouts, never redrawn. All type is set here.
Option 2 carries "TRAINERS DESPISE HIM", the shape Dan picked on RA-15 (memory ad-thumbnail-arrogant-controversial).
The script lives in the repo; images live in the git-ignored media folder below (photos of Dan, public repo).
Helpers are imported from the RA-06 build. Run: python3 build.py [numbers...]"""
import importlib.util, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
OUT = PROJ + "/social media graphics/youtube/thumbnails/RA-07 Fire Your Trainer"
HERE = OUT + "/_build-2026-10-20"
_spec = importlib.util.spec_from_file_location("ra06b", os.path.join(OUT, "..", "RA-06 Whats The Best Ab Exercise", "_build-2026-10-16", "build.py"))
K = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(K)
K.HERE = HERE  # person masks land in this build's mask/ folder
font, sysfont, tw, th, cover, paste_cut, person, clearance, headroom, fit, trimmed = (
    K.font, K.sysfont, K.tw, K.th, K.cover, K.paste_cut, K.person, K.clearance, K.headroom, K.fit, K.trimmed)
FMT = K.FMT; PH = K.PH
SLUG = "fire-your-trainer"
A, B = "FIRE YOUR", "TRAINER"
WHITE, BLACK = (255, 255, 255), (10, 10, 12)
PINK, NAVY = (255, 62, 150), (6, 36, 72)
YEL = (255, 212, 0)
hexc = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def tile(text, f, fill, bg, angle, padx, pady, paper=False):
    """Text on a solid slanted slip/banner, returned as an RGBA tile."""
    w, h = tw(f, text) + 2 * padx, th(f, text) + 2 * pady
    t = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle([10, 10, 10 + w, 10 + h], fill=bg + (255,))
    if paper:  # a row of perforation dots along the top edge reads as a slip of paper
        for x in range(18, 10 + w, 22): d.ellipse([x, 14, x + 7, 21], fill=tuple(max(0, c - 40) for c in bg) + (255,))
    b = f.getbbox(text); d.text((10 + padx - b[0], 10 + pady - b[1]), text, font=f, fill=fill + (255,))
    return t.rotate(angle, expand=True, resample=Image.BICUBIC)


def place(canvas, t, x, y):
    canvas = canvas.convert("RGBA"); lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); lay.paste(t, (x, y), t)
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh.putalpha(lay.getchannel("A").point(lambda v: int(v * 0.55)).filter(ImageFilter.GaussianBlur(10)))
    sh2 = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sh2.paste(sh, (8, 10), sh)
    canvas = Image.alpha_composite(Image.alpha_composite(canvas, sh2), lay)
    return canvas.convert("RGB"), lay.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()


def shadow_text(d, x, y, t, f, fill, off, scol):
    b = f.getbbox(t)
    if off: d.text((x - b[0] + off, y - b[1] + off), t, font=f, fill=scol)
    d.text((x - b[0], y - b[1]), t, font=f, fill=fill)
    return (x, y, x + tw(f, t) + off, y + th(f, t) + off)


def pool(fmt):
    """1: real pool photo 221 (smiling, hands at hips, black shorts) over a bright Codex pool; FIRE YOUR in white Futura
    Condensed ExtraBold with a navy drop, TRAINER in black on a tilted hot-pink pink slip."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/pool_{fmt}.png").convert("RGB"), W, H)
    cut = trimmed(f"{HERE}/cut/photo-221_CUTOUT.png", 0.86)
    mk = lambda z: sysfont("Futura.ttc", z, 4)
    if fmt == "16x9":
        ph = 1060; s = ph / cut.height; x = W - round(cut.width * s) - 70; y = H - ph
    else:
        ph = 1280; s = ph / cut.height; x = (W - round(cut.width * s)) // 2; y = H - ph
    canvas, am = paste_cut(c, cut, x, y, s)
    if fmt == "16x9":
        left = int(np.where(am.any(0))[0].min()); room = left - 70 - 60; x0 = 70
    else:
        room = W - 140; x0 = 70
    fa = mk(fit(mk, A, room, 420)); fb = mk(fit(mk, B, room - 70, 420))
    d = ImageDraw.Draw(canvas)
    off = max(6, fa.size // 22)
    slip = tile(B, fb, BLACK, PINK, -4, 34, 22, paper=True)
    total = th(fa, A) + off + 26 + slip.height
    y0 = (H - total) // 2 if fmt == "16x9" else 80
    boxa = shadow_text(d, x0, y0, A, fa, WHITE, off, NAVY)
    canvas, boxb = place(canvas, slip, x0 - 10, y0 + th(fa, A) + off + 26)
    return canvas, clearance(am, [boxa, boxb]), headroom(am)


def mob(fmt, angle=4):
    """2: real studio-blue-28 (smug half-smirk, arm behind head) in front of a softened crowd of furious personal trainers
    pointing at him, steel-blue gym; TRAINERS in white Impact, DESPISE HIM in black Impact on a tilted yellow banner."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/mob_{fmt}.png").convert("RGB"), W, H).filter(ImageFilter.GaussianBlur(4))
    c = ImageEnhance.Brightness(c).enhance(0.82)
    cut = trimmed(f"{PH}/_cutouts/studio-blue-28_CUTOUT.png", 0.86)
    mk = lambda z: sysfont("Impact.ttf", z)
    if fmt == "16x9":
        ph = 1060; s = ph / cut.height; x = W - round(cut.width * s) - 60; y = H - ph
    else:
        ph = 1260; s = ph / cut.height; x = (W - round(cut.width * s)) // 2; y = H - ph
    canvas, am = paste_cut(c, cut, x, y, s, glow=(255, 200, 40))
    if fmt == "16x9":
        left = int(np.where(am.any(0))[0].min()); room = left - 60 - 50; x0 = 60
    else:
        room = W - 100; x0 = 50
    a, b = "TRAINERS", "DESPISE HIM"
    fa = mk(fit(mk, a, room, 400)); fb = mk(fit(mk, b, room - 80, 400))
    d = ImageDraw.Draw(canvas)
    ban = tile(b, fb, BLACK, YEL, angle, 30, 18)
    total = th(fa, a) + 18 + ban.height
    y0 = (H - total) // 2 if fmt == "16x9" else 60
    boxa = shadow_text(d, x0, y0, a, fa, WHITE, 8, BLACK)
    canvas, boxb = place(canvas, ban, x0 + (tw(fa, a) - ban.width) // 2, y0 + th(fa, a) + 18)
    return canvas, clearance(am, [boxa, boxb]), headroom(am)


def area_type(canvas, area, rows, align, draw):
    """Fit the two-line headline inside a fractional area; rows = [(text, make, scale, fill)]. Returns boxes."""
    W, H = canvas.size; ax0, ay0, ax1, ay1 = area
    x0, y0, x1, y1 = ax0 * W, ay0 * H, ax1 * W, ay1 * H
    aw, ah = x1 - x0, y1 - y0
    hero = max(rows, key=lambda r: r[2])
    s = fit(hero[1], hero[0], aw * 0.94, 460)
    while True:
        fs = [(t, mk(round(s * sc)), col) for t, mk, sc, col in rows]
        gap = round(s * 0.10)
        tot = sum(th(f, t) for t, f, _ in fs) + gap * (len(fs) - 1)
        if (tot <= ah * 0.90 and all(tw(f, t) <= aw * 0.94 for t, f, _ in fs)) or s < 40: break
        s -= 4
    d = ImageDraw.Draw(canvas); y = y0 + (ah - tot) / 2; boxes = []
    for t, f, col in fs:
        w = tw(f, t); x = x0 if align == "l" else x0 + (aw - w) / 2
        boxes.append(draw(d, round(x), round(y), t, f, col)); y += th(f, t) + gap
    return boxes


def area(o, fmt): return tuple(float(v) for v in o[f"headline_area_{fmt}"].split(","))


PLAN = {o["number"]: o for o in json.load(open(f"{HERE}/assets/plan.json"))["options"]}


def ai3(fmt):
    """3: AI Dan fist-bumps a graphite robot coach as his surprised trainer walks out (emerald gym); Rockwell Bold, FIRE YOUR
    cream and TRAINER chartreuse with a hard dark-green offset shadow."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai3_{fmt}.png").convert("RGB"), W, H)
    am = person(c, f"ai3_{fmt}")
    mk = lambda z: sysfont("Rockwell.ttc", z, 2)
    sh = hexc("#012B23")
    draw = lambda d, x, y, t, f, col: shadow_text(d, x, y, t, f, col, max(6, f.size // 14), sh)
    rows = [(A, mk, 0.62, hexc("#FFF3D5")), (B, mk, 1.0, hexc("#C7FF00"))]
    boxes = area_type(c, area(PLAN[3], fmt), rows, "c" if fmt == "9x16" else "l", draw)
    return c, clearance(am, boxes), headroom(am)


def ai4(fmt):
    """4: a cheerful orange robot gym coach giving two thumbs up, headline across its black polo; Arial Rounded Bold (the
    closest installed face to Codex's Cooper Black), FIRE YOUR white and TRAINER peach, thin black outline, rust offset."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai4_{fmt}.png").convert("RGB"), W, H)
    mk = lambda z: sysfont("Arial Rounded Bold.ttf", z)
    def draw(d, x, y, t, f, col):
        off = max(6, f.size // 14); sw = max(3, f.size // 40); b = f.getbbox(t)
        d.text((x - b[0] + off, y - b[1] + off), t, font=f, fill=hexc("#9B3500"), stroke_width=sw, stroke_fill=hexc("#9B3500"))
        d.text((x - b[0], y - b[1]), t, font=f, fill=col, stroke_width=sw, stroke_fill=BLACK)
        return (x - sw, y - sw, x + tw(f, t) + off + sw, y + th(f, t) + off + sw)
    rows = [(A, mk, 0.62, WHITE), (B, mk, 1.0, hexc("#FFC19A"))]
    area_type(c, area(PLAN[4], fmt), rows, "c", draw)
    return c, 9999, 9999


def ai5(fmt):
    """5: robotic hands tear a blank trainer's workout sheet in half on scarlet; Arial Black, FIRE YOUR near-black, TRAINER
    white with a thick near-black outline, flush left."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai5_{fmt}.png").convert("RGB"), W, H)
    mk = lambda z: sysfont("Arial Black.ttf", z)
    ink = hexc("#170707")
    def draw(d, x, y, t, f, col):
        sw = max(5, f.size // 16) if col == WHITE else 0; b = f.getbbox(t)
        d.text((x - b[0] + sw, y - b[1] + sw), t, font=f, fill=col, stroke_width=sw, stroke_fill=ink)
        return (x, y, x + tw(f, t) + 2 * sw, y + th(f, t) + 2 * sw)
    rows = [(A, mk, 0.62, ink), (B, mk, 1.0, WHITE)]
    area_type(c, area(PLAN[5], fmt), rows, "l", draw)
    return c, 9999, 9999


def mob_flat(fmt):
    """2b (Dan, 2026-10-20: "make all the text horizontal, keep everything else the same"): option 2 with the yellow
    DESPISE HIM banner level instead of tilted. Same words, photo, crowd, fonts and colours."""
    return mob(fmt, angle=0)


def ai3_big(fmt):
    """3b (Dan, 2026-10-20: "significantly bigger, only one word per line, each word as big as possible"): option 3's
    picture and Rockwell type, FIRE / YOUR / TRAINER one word per line, each word fitted to the full text width, then
    all scaled together only if the stack would not fit. In 9:16 the stack starts below his waistband and runs over his
    shorts and legs on a dark ramp; face, hair and abs stay clear (clearance measured on the person above the stack)."""
    W, H = FMT[fmt]
    c = cover(Image.open(f"{HERE}/assets/ai3_{fmt}.png").convert("RGB"), W, H)
    am = person(c, f"ai3_{fmt}")
    mk = lambda z: sysfont("Rockwell.ttc", z, 2)
    sh = hexc("#012B23")
    cols = [hexc("#FFF3D5"), hexc("#FFF3D5"), hexc("#C7FF00")]
    words = ["FIRE", "YOUR", "TRAINER"]
    if fmt == "9x16":
        rows = np.where(am.any(1))[0]
        x0, x1, y0, y1 = 0.05 * W, 0.95 * W, 0.50 * H, 0.975 * H
        ramp = Image.linear_gradient("L").resize((W, H))  # dark ramp behind the stack, from the waistband down
        ramp = ramp.point(lambda v: 0 if v < 0.40 * 255 else min(225, int((v - 0.40 * 255) * 2.6)))
        c = Image.composite(Image.new("RGB", (W, H), (1, 26, 20)), c, ramp)
        align = "c"
    else:
        x0, x1, y0, y1 = 0.55 * W, 0.965 * W, 0.07 * H, 0.93 * H
        align = "l"
    aw, ah = x1 - x0, y1 - y0
    sizes = [fit(mk, w, aw * 0.97, 900) for w in words]
    k = 1.0
    while True:
        fs = [mk(max(30, round(z * k))) for z in sizes]
        gap = round(min(f.size for f in fs) * 0.08)
        offs = [max(6, f.size // 16) for f in fs]
        tot = sum(th(f, w) + o for f, w, o in zip(fs, words, offs)) + gap * 2
        if tot <= ah or k < 0.3: break
        k -= 0.01
    d = ImageDraw.Draw(c); y = y0 + (ah - tot) / 2; boxes = []
    for f, w, col, o in zip(fs, words, cols, offs):
        x = x0 if align == "l" else x0 + (aw - tw(f, w)) / 2
        boxes.append(shadow_text(d, round(x), round(y), w, f, col, o, sh)); y += th(f, w) + o + gap
    am_check = am
    if fmt == "9x16":  # protect face, hair and abs: the person above his waistband (top of the shorts measured at 0.445 H)
        am_check = am.copy(); am_check[round(0.445 * H):, :] = False
    return c, clearance(am_check, boxes), headroom(am)


JOBS = {
    1: ("pool-photo-221-pink-slip", "Real pool photo: you smiling by a bright pool, TRAINER on a hot-pink pink slip", pool),
    2: ("studio-blue-28-trainers-despise-him", "Real studio photo: your smirk, angry trainers pointing at you, TRAINERS DESPISE HIM", mob),
    3: ("ai-dan-robot-fist-bump-rockwell", "AI picture of you: fist bump with a robot coach while your trainer walks out", ai3),
    4: ("ai-orange-robot-coach-rounded", "AI: a cocky orange robot coach giving two thumbs up, headline on its shirt", ai4),
    5: ("ai-robot-hands-tear-plan-scarlet", "AI: robot hands tearing the trainer's workout sheet in half, scarlet", ai5),
}


VARIANTS = {
    "2b": ("studio-blue-28-trainers-despise-him-level", "2b: same as 2, all text level (banner no longer tilted)", mob_flat),
    "3b": ("ai-dan-robot-fist-bump-one-word-per-line", "3b: same picture as 3, FIRE / YOUR / TRAINER one word per line, as big as fits", ai3_big),
}


def variants():
    """Round 2 of the pick: Dan's text variations of 2 and 3, beside the originals. Run: python3 build.py variants"""
    for v, (name, lab, fn) in VARIANTS.items():
        for fmt in FMT:
            canvas, clear, head = fn(fmt)
            f_ = f"{SLUG}_{v}-{name} | {fmt}.jpg"; p = os.path.join(OUT, f_); canvas.save(p, quality=92)
            ok = clear >= 25 and head >= 14 and os.path.getsize(p) < 2_000_000
            print(f"[{v} {fmt}] clearance {clear}px, headroom {head}px, {os.path.getsize(p)//1024}KB -> {'PASS' if ok else 'FAIL'}")
    q = {f"{r['number']}-{r['fmt']}": r["file"] for r in json.load(open(os.path.join(HERE, "qc.json")))}
    rows = [("2", q["2-9x16"], q["2-16x9"], "2 (before): tilted banner"),
            ("2b", f"{SLUG}_2b-{VARIANTS['2b'][0]} | 9x16.jpg", f"{SLUG}_2b-{VARIANTS['2b'][0]} | 16x9.jpg", VARIANTS["2b"][1]),
            ("3", q["3-9x16"], q["3-16x9"], "3 (before): two lines"),
            ("3b", f"{SLUG}_3b-{VARIANTS['3b'][0]} | 9x16.jpg", f"{SLUG}_3b-{VARIANTS['3b'][0]} | 16x9.jpg", VARIANTS["3b"][1])]
    pad, w9, h9, w16, h16 = 30, 360, 640, 1138, 640; rowh = h9 + 70
    sheet = Image.new("RGB", (pad * 4 + 90 + w9 + w16, 150 + len(rows) * rowh), (242, 242, 244)); d = ImageDraw.Draw(sheet)
    d.text((pad, 24), "Fire Your Trainer (RA-07 ad): text variations of 2 and 3", font=font(40), fill=(20, 22, 28))
    d.text((pad, 80), "Each new version sits under the one you saw. Pick one: 2, 2b, 3 or 3b (or 1, 4, 5 from the first sheet).", font=font(24), fill=(70, 72, 80))
    for i, (n, f9, f16, lab) in enumerate(rows):
        y = 140 + i * rowh
        sheet.paste(Image.open(os.path.join(OUT, f9)).resize((w9, h9), Image.LANCZOS), (pad + 90, y))
        sheet.paste(Image.open(os.path.join(OUT, f16)).resize((w16, h16), Image.LANCZOS), (pad * 2 + 90 + w9, y))
        d.text((pad, y + 4), n, font=font(48), fill=(20, 22, 28)); d.text((pad + 90, y + h9 + 10), lab, font=font(24), fill=(40, 42, 50))
    sp = os.path.join(OUT, "REVIEW_fire-your-trainer-variations-2b-3b.jpg"); sheet.save(sp, quality=88); print(sp)


def main():
    if sys.argv[1:] == ["variants"]: return variants()
    want = [int(a) for a in sys.argv[1:]] or sorted(JOBS)
    qp = os.path.join(HERE, "qc.json"); res = {f"{r['number']}-{r['fmt']}": r for r in (json.load(open(qp)) if os.path.exists(qp) else [])}
    for n in want:
        name, lab, fn = JOBS[n]
        for fmt in FMT:
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
    d.text((pad, 24), "Fire Your Trainer (RA-07 ad): five thumbnail choices", font=font(40), fill=(20, 22, 28))
    d.text((pad, 80), "Left: 9:16 (the ad's shape). Right: the 16:9 version. All made with Codex. Pick one number.", font=font(24), fill=(70, 72, 80))
    for i, n in enumerate(sorted(JOBS)):
        y = 140 + i * rowh
        sheet.paste(Image.open(os.path.join(OUT, by[(n, "9x16")]["file"])).resize((w9, h9), Image.LANCZOS), (pad + 60, y))
        sheet.paste(Image.open(os.path.join(OUT, by[(n, "16x9")]["file"])).resize((w16, h16), Image.LANCZOS), (pad * 2 + 60 + w9, y))
        d.text((pad, y + 4), str(n), font=font(52), fill=(20, 22, 28))
        d.text((pad + 60, y + h9 + 10), JOBS[n][1], font=font(24), fill=(40, 42, 50))
    sp = os.path.join(OUT, "REVIEW_fire-your-trainer-five-options.jpg"); sheet.save(sp, quality=88); print(sp)


if __name__ == "__main__":
    main()
