#!/usr/bin/env python3
"""Build every card clip for one aspect. Usage: s06_assets.py 9x16|16x9

ROUND 2 (plan section 12):
  * R1 -- every card except the end card is laid out inside A.CARD_RECT, which stops ABOVE the
    caption band, so the captions run under it on the J2AD field instead of being switched off.
  * R6 -- the field is the FLAT J2AD field, never a blurred copy of the photograph; in 9:16 every
    chip sits inside the platform-safe band (y >= 200, x <= 940, above the caption band) and in
    16:9 every chip sits FULLY INSIDE the card. Position is still chosen by measuring the person
    mask on the RENDERED frame, and the chip shrinks (then wraps) before it is allowed to overflow.

Each card is a full-frame h264 clip at the delivered size and rate, cut into the timeline as a
hard cut (never a dissolve: two physique pictures can never blend). Every card keeps moving
(ad-edit lesson 52) and every chip is STATIC so the label gate reads it at one position.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from ra01lib import Aspect, ASSETS, CHIP_AI, CHIP_REAL, FIELD, OLIVE, LIME
import motionlib as ml
from motionlib import font, text_size

KEY = sys.argv[1]
A = Aspect(KEY)
OUT = f"cards_{KEY}"
os.makedirs(OUT, exist_ok=True)
B = json.load(open("beats.json"))
MS = B["macro_slice"]

CHIP_TEXT = {"ai": CHIP_AI, "real": CHIP_REAL}
_chip_cache = {}


def chip_for(kind, max_w, tag):
    """A chip sized to the width it is allowed. 9:16 chips share one width (the safe band), 16:9
    chips are cut to their own card, so they are cached per (kind, width)."""
    key = (kind, int(max_w))
    if key not in _chip_cache:
        p = f"{OUT}/chip_{kind}_{int(max_w)}.png"
        _chip_cache[key] = (p, L.chip_png(CHIP_TEXT[kind], p, size=40 if KEY == "9x16" else 38,
                                          max_w=max_w))
    return _chip_cache[key]


def paste_chip(im, chip_path, pos):
    ch = Image.open(chip_path).convert("RGBA")
    im.alpha_composite(ch, pos)


# ⚠ THE HEADER MUST BE TALLER THAN THE TALLEST CHIP. At 96 px the two-line "Real picture of me —
# not AI-generated" chip (114 px) stuck 21 px out of the top of the panel -- D8's own defect, in a
# new place. 140 px clears the tallest chip by 13 px top and bottom, and the assertion below is
# what stops it recurring.
HEADER, PAD = 140, 20


def panel_for(asset):
    """16:9 only: a J2AD PANEL with a header strip, the photograph inside it.

    ⚠ WHY THIS EXISTS. R6 says a 16:9 chip "sits fully inside the card", and D8 is about chips
    straddling the card's top edge. But a portrait photograph fitted to the height of a 16:9 frame
    is filled by Dan head to toe: measured on the round-2 cards, `place_chip` found NO CLEAR BAND
    inside any of them and fell back to a corner, i.e. onto him. So the card is given a header the
    layout RESERVES for the label -- the chip is then fully inside the card, above the photograph,
    and provably clear of his face, hair and abs. (9:16 has room above the picture on the field and
    keeps its round-1 arrangement, which the reviewer did not fault.)
    """
    img = ml.oriented(Image.open(ASSETS[asset]).convert("RGB"))
    cx0, cy0, cx1, cy1 = A.CARD_RECT
    max_h = (cy1-cy0) - HEADER - PAD
    ph = max_h; pw = int(ph*img.width/img.height)
    if pw > (cx1-cx0) - 2*PAD:
        pw = (cx1-cx0) - 2*PAD; ph = int(pw*img.height/img.width)
    pw -= pw % 2; ph -= ph % 2
    panel_w, panel_h = pw + 2*PAD, ph + HEADER + PAD
    panel_x = cx0 + ((cx1-cx0) - panel_w)//2
    panel_y = cy0 + ((cy1-cy0) - panel_h)//2
    photo_rect = (panel_x + PAD, panel_y + HEADER, panel_x + PAD + pw, panel_y + HEADER + ph)
    header = (panel_x + PAD, panel_y + 12, panel_x + panel_w - PAD, panel_y + HEADER - 12)
    return (panel_x, panel_y, panel_x+panel_w, panel_y+panel_h), photo_rect, header


def panel_layer(panel):
    im = Image.new("RGBA", A.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([panel[0], panel[1], panel[2]-1, panel[3]-1], radius=26,
                        fill=ml.J2AD.field_hi + (255,), outline=(38, 42, 32, 255), width=2)
    return im


def photo_frames(asset, dur, chip_kind, direction, name):
    if KEY == "9x16":
        panel = None
        layer, box = L.photo_layer(ASSETS[asset], A, rect=A.CARD_RECT)
        card_box = box
        cbox, cmax = A.CHIP_BOX, A.CHIP_BOX[2] - A.CHIP_BOX[0]
    else:
        panel, prect, header = panel_for(asset)
        layer, box = L.photo_layer(ASSETS[asset], A, rect=prect, radius=16)
        card_box = panel
        cbox, cmax = header, header[2] - header[0] - 8
    base = L.field(A)                               # R6: the FLAT J2AD field, nothing behind it
    if panel: base.alpha_composite(panel_layer(panel))
    n = L.nf(dur)
    masks = []
    plain = L.field(A)
    for t in (0.0, dur*0.5, dur):
        f = plain.copy(); f.alpha_composite(L.kb(layer, t, dur, direction))
        m = L.person_mask(f)
        if m is not None: masks.append(m)
    pos, why, chip_png_path = None, "no chip on this card", None
    if chip_kind:
        if not masks:
            raise SystemExit(f"{name}: person mask failed; a label cannot be placed by measurement")
        chip_png_path, wh = chip_for(chip_kind, cmax, name)
        pos, why = L.place_chip(masks, wh, A, box=cbox)
        if panel:                                   # centre it in the reserved header
            pos = (cbox[0] + ((cbox[2]-cbox[0]) - wh[0])//2,
                   cbox[1] + ((cbox[3]-cbox[1]) - wh[1])//2)
            why = "the card's reserved header strip, above the photograph"
            assert (pos[0] >= panel[0] and pos[1] >= panel[1] and
                    pos[0]+wh[0] <= panel[2] and pos[1]+wh[1] <= panel[3]), (
                f"{name}: the chip {wh} at {pos} is not fully inside the card {panel} -- R6")
            assert pos[1]+wh[1] <= cbox[3] + 1 and pos[1] >= cbox[1] - 1, (
                f"{name}: the chip {wh} overflows the reserved header {cbox}")
            # prove the reserved strip really is clear of him on the rendered frame
            for m in masks:
                assert not m[pos[1]:pos[1]+wh[1], pos[0]:pos[0]+wh[0]].any(), \
                    f"{name}: the reserved header is not clear of him"
        why += f" (search box {cbox}, chip {wh})"
    frames = []
    for i in range(n):
        t = i/L.FPS
        f = base.copy()
        lay = L.kb(layer, t, dur, direction)
        k, a = L.entry(t)
        if k != 1.0: lay = ml.scale_about(lay, k, canvas=A.size)
        if a < 1.0: lay = ml.with_alpha(lay, a)
        if panel:                                   # the photo never spills out of its panel
            m = Image.new("L", A.size, 0)
            ImageDraw.Draw(m).rounded_rectangle([box[0], box[1], box[2], box[3]], radius=16, fill=255)
            lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", A.size, 0), m))
        f.alpha_composite(lay)
        if chip_kind: paste_chip(f, chip_png_path, pos)
        frames.append(f)
    return frames, {"chip_pos": pos, "chip_why": why, "chip_png": chip_png_path,
                    "photo_box": list(card_box)}


def scan_frames(dur):
    """The 'AI reads your picture' device (ad-edit lessons 11/16), rebuilt for RA-01.

    ⚠ NO PRINTED NUMBER. Each row reveals a LABEL and a bar rather than a weight or a body-fat
    figure, and the last line is the plan teaser with the plan itself not revealed. The subject is
    Dan's OWN AI image, tagged. R1: the whole device lives inside A.CARD_RECT so the caption band
    below it is clear.
    """
    img = ml.oriented(Image.open(ASSETS["ai"]).convert("RGB"))
    cx0, cy0, cx1, cy1 = A.CARD_RECT
    CW_, CH_ = cx1-cx0, cy1-cy0
    if KEY == "9x16":
        pw = int(CW_*0.585); pw -= pw % 2
        ph = int(pw*img.height/img.width); ph -= ph % 2
        px, py = cx0 + (CW_-pw)//2, cy0
        rx0, rx1 = cx0 + 40, cx1 - 40
        ry0, rowh = py + ph + 26, 66
        bandh, fLs, fHs = 70, 32, 38
    else:
        # a reserved strip above the picture carries the chip (the same fix as the photo cards:
        # a portrait picture fitted to a 16:9 height has no clear band inside it)
        STRIP = 86
        ph = int((CH_-STRIP)*0.99); ph -= ph % 2
        pw = int(ph*img.width/img.height); pw -= pw % 2
        px, py = cx0 + 60, cy0 + STRIP
        rx0, rx1 = px + pw + 70, cx1 - 40
        ry0, rowh = cy0 + STRIP + 150, 96
        bandh, fLs, fHs = 104, 36, 44
    img = img.resize((pw, ph), Image.LANCZOS)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw-1, ph-1], radius=18, fill=255)
    ph_layer = Image.new("RGBA", A.size, (0, 0, 0, 0)); ph_layer.paste(img, (px, py), mask)
    photo_box = (px, py, px+pw-1, py+ph-1)
    ROWS = ["BODY FAT", "FAT TO LOSE", "MUSCLE TO GAIN"]
    fL = font(fLs, "ExtraBold"); fH = font(fHs, "ExtraBold")
    base = L.field(A)
    n = L.nf(dur)
    barw = int((rx1-rx0)*0.46)
    if KEY == "9x16":
        cbox, cmax = A.CHIP_BOX, A.CHIP_BOX[2] - A.CHIP_BOX[0]
    else:
        cbox, cmax = (px, cy0 + 8, px + pw, cy0 + 78), pw - 8
    chip_path, (cw, ch) = chip_for("ai", cmax, "stats_scan")
    probe = L.field(A); probe.alpha_composite(ph_layer)
    pm = L.person_mask(probe)
    if pm is None:
        raise SystemExit("stats card: person mask failed")
    chip_pos, chip_why = L.place_chip([pm], (cw, ch), A, box=cbox)
    if KEY != "9x16":
        chip_pos = (px, cy0 + 8 + max(0, (70-ch)//2))
        chip_why = "the stats card's reserved strip above the picture"
        assert not pm[chip_pos[1]:chip_pos[1]+ch, chip_pos[0]:chip_pos[0]+cw].any(), \
            "stats card: the reserved chip strip is not clear of him"
    frames = []
    SC = max(1.0, dur*0.26)
    step = max(0.42, (dur - SC - 0.9)/(len(ROWS) + 0.6))
    for i in range(n):
        t = i/L.FPS
        f = base.copy()
        f.alpha_composite(L.kb(ph_layer, t, dur, 1, amp=0.045, canvas=A.size))
        d = ImageDraw.Draw(f)
        sp = min(t/SC, 1.0)
        if sp < 1.0:
            sy = int(py + sp*ph)
            gl = Image.new("RGBA", A.size, (0, 0, 0, 0))
            ImageDraw.Draw(gl).rectangle([px, sy-3, px+pw, sy+3], fill=LIME + (220,))
            f.alpha_composite(gl.filter(ImageFilter.GaussianBlur(6)))
            ImageDraw.Draw(f).rectangle([px, sy-1, px+pw, sy+1], fill=LIME + (255,))
        for r, label in enumerate(ROWS):
            rt = SC + r*step
            if t < rt: continue
            p = min((t-rt)/max(0.42, step*0.85), 1.0)
            yy = ry0 + r*rowh + int(round(6*(t/dur)))
            d.text((rx0, yy), label, font=fL, fill=(255, 255, 255, int(255*p)))
            bx = rx1 - barw
            d.rounded_rectangle([bx, yy+4, rx1, yy+30], radius=13, fill=(34, 38, 30, 255))
            grow = min(1.0, max(0.0, (t - rt)/max(0.6, dur - rt - 0.2)))
            d.rounded_rectangle([bx, yy+4, bx+int(barw*(0.25 + 0.60*grow)*p), yy+30],
                                radius=13, fill=OLIVE + (255,))
        rt = SC + len(ROWS)*step + 0.2
        if t >= rt:
            p = min((t-rt)/0.45, 1.0)
            yy = ry0 + len(ROWS)*rowh + 10 + int(round(6*(t/dur)))
            d.rounded_rectangle([rx0, yy, rx1, yy+bandh], radius=16, fill=(28, 52, 33, int(255*p)))
            d.text(((rx0+rx1)//2, yy+bandh//2), "YOUR WORKOUT PLAN", font=fH,
                   fill=(255, 255, 255, int(255*p)), anchor="mm")
        paste_chip(f, chip_path, chip_pos)
        frames.append(f)
    return frames, {"chip_pos": chip_pos, "chip_why": chip_why + " (stats card, inside the picture)",
                    "chip_png": chip_path, "photo_box": list(photo_box)}


def _flat(base, lay):
    f = base.copy(); f.alpha_composite(lay); return f


def endcard_frames(dur):
    """The end card: the AI image (tagged), the CTA and the URL.

    This is the ONE card that is still full-screen: the last word ends 0.3 s before it starts and
    s07_captions.py clips the final line's hold to its in-point, so no caption ever shares a frame
    with it. It is the only beat declared in the gate plan's `cards`.
    """
    layer, box = L.photo_layer(ASSETS["ai"], A, margin_frac=0.10)
    img_shift = int(A.VH*(0.10 if KEY == "9x16" else 0.06))
    base = L.field(A)
    fB = font(62 if KEY == "9x16" else 56, "ExtraBold")
    fU = font(56 if KEY == "9x16" else 50, "ExtraBold")
    n = L.nf(dur)
    lay0 = Image.new("RGBA", A.size, (0, 0, 0, 0))
    lay0.alpha_composite(layer, (0, -img_shift))
    y = A.VH - (330 if KEY == "9x16" else 250)
    pill = [A.SAFE, y, A.VW-A.SAFE, y+120]
    url_y = y+180
    pm = L.person_mask(_flat(L.field(A), lay0))
    if pm is None: raise SystemExit("end card: person mask failed")
    block = pm.copy()
    block[max(0, pill[1]-14):min(A.VH, url_y+70), max(0, pill[0]-14):min(A.VW, pill[2]+14)] = True
    # the end card is the one FULL-SCREEN card, so "inside the card" is the whole safe frame
    cbox = A.CHIP_BOX
    chip_path, wh = chip_for("ai", cbox[2]-cbox[0], "end_card")
    chip_pos, chip_why = L.place_chip([block], wh, A, box=cbox)
    frames = []
    for i in range(n):
        t = i/L.FPS
        f = base.copy()
        f.alpha_composite(L.kb(lay0, t, dur, 1, amp=0.03, canvas=A.size))
        d = ImageDraw.Draw(f)
        d.rounded_rectangle(pill, radius=18, fill=(28, 52, 33, 255))
        d.text((A.VW//2, y+60), "Tap the button below", font=fB, fill=(255, 255, 255, 255), anchor="mm")
        d.text((A.VW//2, url_y), "AbsByAI.com", font=fU, fill=OLIVE + (255,), anchor="mm")
        paste_chip(f, chip_path, chip_pos)
        frames.append(f)
    return frames, {"chip_pos": chip_pos, "chip_why": chip_why + " (CTA pill and URL excluded)",
                    "chip_png": chip_path, "photo_box": list(box)}


def macro_clip(dur, nfr, out):
    """The real macro-tracker recording, inside A.CARD_RECT on the flat field (R1 + R6).

    R3: the window is the app's RESULT -- the itemized list, its three rows and the calorie total,
    plus the "logged" confirmation -- over the only stretch of the recording where nothing changes:
    40.50-43.60 s of its own timeline. 43.80 is where it changes screen, so the slice ends 6 frames
    early. The crop is tighter than round 1's whole-phone window because the card is no longer
    full-bleed: at this size the whole phone would put the list at 0.47x and it would not read.
    A slow pan over the result keeps the card moving (ad-edit lesson 52) -- the recording itself is
    deliberately static here, which is the price of R3's stability requirement.
    """
    cw, ch, cxs = 1280, 1420, 20
    y0, y1 = 900, 1000
    rx0, ry0, rx1, ry1 = A.CARD_RECT
    k = min((rx1-rx0)/cw, (ry1-ry0)/ch)
    nw, nh = int(cw*k), int(ch*k)
    nw -= nw % 2; nh -= nh % 2
    ox, oy = rx0 + ((rx1-rx0)-nw)//2, ry0 + ((ry1-ry0)-nh)//2
    # the field, with a rounded hole punched where the recording goes
    fieldp = f"{OUT}/_macro_field.png"
    fim = L.field(A)
    hole = Image.new("L", A.size, 255)
    ImageDraw.Draw(hole).rounded_rectangle([ox, oy, ox+nw-1, oy+nh-1], radius=22, fill=0)
    fim.putalpha(hole)
    fim.save(fieldp)
    pan = f"{y0}+({y1}-{y0})*t/{dur:.3f}"
    # ⚠ setpts=PTS-STARTPTS. Without it the seeked recording's first frame arrived after the colour
    # source's frame 0, so the card's FIRST FRAME was an empty field -- one near-black frame at the
    # cut into the card, on both aspects (luma 14.9 against 124.8 for every other frame). The
    # delivery gate's black-frame bound is luma 6.0, so nothing measured it; it was found by looking.
    fc = (f"[1:v]crop={cw}:{ch}:{cxs}:'{pan}',scale={nw}:{nh}:flags=lanczos,"
          f"setpts=PTS-STARTPTS,fps=30000/1001[fg];"
          f"[0:v][fg]overlay={ox}:{oy}:shortest=1[a];"
          f"[a][2:v]overlay=0:0:format=auto,format=yuv420p[v]")
    subprocess.run([L.FF, "-nostdin", "-y", "-v", "error",
                    "-f", "lavfi", "-i", f"color=c=0x{FIELD[0]:02x}{FIELD[1]:02x}{FIELD[2]:02x}:"
                                         f"s={A.VW}x{A.VH}:r=30000/1001",
                    "-ss", str(MS["in"]), "-t", f"{dur:.3f}", "-i", ASSETS["macro"],
                    "-loop", "1", "-i", fieldp,
                    "-filter_complex", fc, "-map", "[v]", "-an", "-frames:v", str(nfr),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "30000/1001",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0",
                    out], check=True)
    # prove the first and last frames of the card actually contain the recording
    import numpy as _np
    _raw = subprocess.run([L.FF, "-v", "error", "-nostdin", "-i", out, "-vf", "format=gray",
                           "-f", "rawvideo", "-"], capture_output=True).stdout
    _a = _np.frombuffer(_raw, _np.uint8).reshape(-1, A.VH, A.VW)
    _m = [float(_a[i].mean()) for i in (0, 1, len(_a)-2, len(_a)-1)]
    assert min(_m[0], _m[-1]) > 0.5*max(_m), (
        f"macro card: frame luma {_m} -- the first or last frame does not contain the recording")
    return {"slice": [MS["in"], MS["out"]], "crop": [cw, ch, cxs, y0, y1],
            "frame_luma_first_last": [round(x, 1) for x in _m],
            "placed": [ox, oy, ox+nw-1, oy+nh-1],
            "_why": "R3: the only stretch of the recording where the itemized list and the calorie "
                    "total are stable; it ends 6 frames before the screen changes at 43.80 s."}


ONLY = set(x for x in os.environ.get("ONLY", "").split(",") if x)
meta = json.load(open(f"{OUT}/meta.json"))["cards"] if (ONLY and os.path.exists(f"{OUT}/meta.json")) else {}
for i, c in enumerate(B["cards"]):
    if ONLY and c["name"] not in ONLY: continue
    nfr = c["frames"]
    dur = nfr/L.FPS            # the timeline's own frame count, never the beat length
    if c["kind"] == "clip":
        assert MS["in"] + dur <= MS["out"] + 1e-3, (
            f"the macro slice would end at {MS['in']+dur:.3f}s of the recording; it must end by "
            f"{MS['out']:.3f}s (3 frames before the screen changes at 43.80 s)")
    out = f"{OUT}/{c['name']}.mp4"
    if c["kind"] == "clip":
        meta[c["name"]] = macro_clip(dur, nfr, out)
    elif c["kind"] == "scan":
        fr, m = scan_frames(dur); L.encode_h264(fr[:nfr], out, A.size); meta[c["name"]] = m
    elif c["kind"] == "endcard":
        fr, m = endcard_frames(dur); L.encode_h264(fr[:nfr], out, A.size); meta[c["name"]] = m
    else:
        fr, m = photo_frames(c["asset"], dur, c["chip"], 1 if i % 2 == 0 else -1, c["name"])
        L.encode_h264(fr[:nfr], out, A.size); meta[c["name"]] = m
    print(f"  {c['name']:<11} {dur:5.2f}s -> {out}  {meta[c['name']].get('chip_pos','')} "
          f"{meta[c['name']].get('chip_why','')}")

# the per-KIND fallback pair the gate's `label_chips` needs on disk (every insert also declares its
# own chip, which is what the gate actually correlates against)
fallback = {k: chip_for(k, (A.CHIP_BOX[2]-A.CHIP_BOX[0]) if KEY == "9x16" else 560, "fallback")
            for k in ("ai", "real")}
json.dump({"chips": {k: v[0] for k, v in fallback.items()},
           "chip_size": {k: v[1] for k, v in fallback.items()},
           "card_rect": list(A.CARD_RECT), "chip_box": list(A.CHIP_BOX), "cards": meta},
          open(f"{OUT}/meta.json", "w"), indent=1)
print("cards done ->", OUT)
