#!/usr/bin/env python3
"""RA-01 SQUARE: every card clip at 1080x1080.  sq_assets.py   (ONLY=name,name to rebuild some)

A re-layout of the approved 9:16 cards (s06_assets.py), same beats, same frame counts, same chips,
same J2AD field, same motion (Ken Burns drift + entry spring, hard cuts, static chips):

  * every card except the end card lives inside A.CARD_RECT (y 64-836), ABOVE the caption band
    (ink top 880), so captions run under it on the field exactly as in the vertical (R1);
  * the chip sits on the field ABOVE the picture, as in the vertical: never on his face, hair or abs,
    and proven clear of him by person mask on the rendered frame;
  * a standing portrait is shown as its 1:1 crop, hair to shorts line (square rules 4-5: a 1:1 frame
    cannot show a 2:3 portrait at a useful size; which photos survive a 1:1 crop is MEASURED here
    with the person mask, and the crop keeps the whole head and the shorts line). The BEFORE picture
    is NOT cropped: its belly sits at the bottom of the photograph, so it is fitted whole;
  * the analysis card (Dan-approved, shared kit) goes side by side: picture left, rows right;
  * the macro recording keeps the vertical's exact window (the whole result, 40.50-43.60 s);
  * the end card is the one full-screen card: chip, picture, CTA, URL, stacked.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01-sq")
import ra01lib as L
from ra01lib import Aspect, ASSETS, CHIP_AI, CHIP_REAL, FIELD, OLIVE, LIME
import motionlib as ml
from motionlib import font, text_size

KEY = "1x1"
A = Aspect(KEY)
OUT = f"cards_{KEY}"
os.makedirs(OUT, exist_ok=True)
B = json.load(open("beats.json"))
MS = B["macro_slice"]
CX0, CY0, CX1, CY1 = A.CARD_RECT            # 60, 64, 1020, 836
CHIP_Y, CHIP_SLOT, CHIP_GAP = CY0, 72, 24   # the chip's slot on the field above the picture
PIC_TOP = CHIP_Y + CHIP_SLOT + CHIP_GAP     # 160: every chipped picture starts here
CHIP_TEXT = {"ai": CHIP_AI, "real": CHIP_REAL}
_chips = {}


def chip_for(kind):
    if kind not in _chips:
        p = f"{OUT}/chip_{kind}.png"
        _chips[kind] = (p, L.chip_png(CHIP_TEXT[kind], p, size=40, max_w=CX1 - CX0))
    return _chips[kind]


def chip_xy(kind, cx):
    """Centred on the picture's own centre line, inside its 72 px slot above the picture."""
    p, (w, h) = chip_for(kind)
    x = int(round(cx - w/2)); x = max(CX0, min(CX1 - w, x))
    return p, (x, CHIP_Y + (CHIP_SLOT - h)//2), (w, h)


def square_crop(asset):
    """The 1:1 crop of a standing portrait: full width, hair top ~7 % below the crop's top edge.
    Returns the cropped image and the measurements that justify it."""
    img = ml.oriented(Image.open(ASSETS[asset]).convert("RGB"))
    small = img.copy(); small.thumbnail((900, 1400))
    k = img.height/small.height
    m = L.person_mask(small)
    if m is None or not m.any():
        raise SystemExit(f"{asset}: person mask failed; the 1:1 crop cannot be measured")
    rows = np.where(m.any(1))[0]
    top, bot = int(rows[0]*k), int(rows[-1]*k)
    side = img.width
    y0 = int(round(top - 0.07*side)); y0 = max(0, min(img.height - side, y0))
    head_room = top - y0
    assert head_room >= 0, (asset, "the crop would cut his hair")
    crop = img.crop((0, y0, side, y0 + side))
    return crop, {"src": [img.width, img.height], "crop": [0, y0, side, y0 + side],
                  "hair_top_src": top, "headroom_frac": round(head_room/side, 3),
                  "person_bottom_src": bot, "shows_frac_of_body": round((y0 + side - top)/max(1, bot - top), 3)}


def layer_from(img, rect, radius=22):
    """`img` fitted whole into rect (never cover-cropped here), centred, rounded."""
    rx0, ry0, rx1, ry1 = rect
    k = min((rx1-rx0)/img.width, (ry1-ry0)/img.height)
    nw, nh = int(img.width*k), int(img.height*k); nw -= nw % 2; nh -= nh % 2
    im = img.resize((nw, nh), Image.LANCZOS)
    layer = Image.new("RGBA", A.size, (0, 0, 0, 0))
    x, y = rx0 + ((rx1-rx0)-nw)//2, ry0 + ((ry1-ry0)-nh)//2
    mask = Image.new("L", (nw, nh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, nw-1, nh-1], radius=radius, fill=255)
    layer.paste(im, (x, y), mask)
    return layer, (x, y, x+nw-1, y+nh-1)


def assert_chip_clear(name, frames_probe, pos, wh, pad=8):
    """The chip rectangle (+pad) touches no person pixel on the rendered card, start/mid/end."""
    x, y = pos; w, h = wh
    for f in frames_probe:
        m = L.person_mask(f)
        if m is None:
            raise SystemExit(f"{name}: person mask failed; the label cannot be proven clear of him")
        hit = int(m[max(0, y-pad):y+h+pad, max(0, x-pad):x+w+pad].sum())
        assert hit == 0, f"{name}: the chip touches {hit} person px"


def photo_frames(asset, dur, chip_kind, direction, name):
    crop_meta = None
    if chip_kind:                                   # the AI image and the three after pictures
        img, crop_meta = square_crop(asset)
        rect = (CX0, PIC_TOP, CX1, CY1)
    else:                                           # the BEFORE picture: whole, no chip, no crop
        img = ml.oriented(Image.open(ASSETS[asset]).convert("RGB"))
        rect = A.CARD_RECT
    layer, box = layer_from(img, rect)
    base = L.field(A)
    n = L.nf(dur)
    pos = chip_png = wh = None
    why = "no chip on this card"
    if chip_kind:
        chip_png, pos, wh = chip_xy(chip_kind, (box[0]+box[2])/2)
        probes = []
        for t in (0.0, dur*0.5, dur):
            f = L.field(A); f.alpha_composite(L.kb(layer, t, dur, direction)); probes.append(f)
        assert_chip_clear(name, probes, pos, wh)
        why = "on the field above the picture, as in the vertical; person mask clear at start/mid/end"
    frames = []
    for i in range(n):
        t = i/L.FPS
        f = base.copy()
        lay = L.kb(layer, t, dur, direction)
        k, a = L.entry(t)
        if k != 1.0: lay = ml.scale_about(lay, k, canvas=A.size)
        f.alpha_composite(lay)
        if chip_kind: f.alpha_composite(Image.open(chip_png).convert("RGBA"), pos)
        frames.append(f)
    return frames, {"chip_pos": pos, "chip_why": why, "chip_png": chip_png, "photo_box": list(box),
                    "square_crop": crop_meta}


def scan_frames(dur):
    """The analysis card, side by side for 1:1: the WHOLE AI picture left, the three label-and-bar
    rows and the plan band right. No printed number (unchanged). Timing identical to the vertical."""
    img = ml.oriented(Image.open(ASSETS["ai"]).convert("RGB"))
    ph = CY1 - PIC_TOP; ph -= ph % 2
    pw = int(ph*img.width/img.height); pw -= pw % 2
    px, py = CX0, PIC_TOP
    img = img.resize((pw, ph), Image.LANCZOS)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw-1, ph-1], radius=18, fill=255)
    ph_layer = Image.new("RGBA", A.size, (0, 0, 0, 0)); ph_layer.paste(img, (px, py), mask)
    photo_box = (px, py, px+pw-1, py+ph-1)
    ROWS = ["BODY FAT", "FAT TO LOSE", "MUSCLE TO GAIN"]
    rx0, rx1 = px + pw + 48, CX1
    fL = font(38, "ExtraBold"); fH = font(34, "ExtraBold")
    rowh, barh, bandh = 118, 28, 86
    block = len(ROWS)*rowh + 10 + bandh
    ry0 = py + (ph - block)//2
    for lab in ROWS: assert text_size(lab, fL)[0] <= rx1 - rx0, lab
    assert text_size("YOUR WORKOUT PLAN", fH)[0] <= rx1 - rx0 - 24
    base = L.field(A)
    n = L.nf(dur)
    chip_path, chip_pos, (cw, ch) = chip_xy("ai", (photo_box[0]+photo_box[2])/2)
    AMP = 0.03

    SRC = ml.oriented(Image.open(ASSETS["ai"]).convert("RGB"))

    def pic(t):
        # the drift zooms the picture about ITS OWN centre, inside its fixed box, with a FLOAT source
        # box so it moves a fraction of a pixel every frame (an integer resize stepped once per ~14
        # frames and the watch scan read a 0.3 s frozen run between two row reveals).
        p = min(max(t/dur, 0.0), 1.0); k = 1.0 + AMP*p
        sw, sh = SRC.width/k, SRC.height/k
        bx = ((SRC.width-sw)/2, (SRC.height-sh)/2, (SRC.width+sw)/2, (SRC.height+sh)/2)
        im = SRC.resize((pw, ph), Image.LANCZOS, box=bx)
        lay = Image.new("RGBA", A.size, (0, 0, 0, 0)); lay.paste(im, (px, py), mask)
        return lay
    probes = []
    for t in (0.0, dur):
        f = L.field(A); f.alpha_composite(pic(t)); probes.append(f)
    assert_chip_clear("stats_scan", probes, chip_pos, (cw, ch))
    frames = []
    SC = max(1.0, dur*0.26)
    step = max(0.42, (dur - SC - 0.9)/(len(ROWS) + 0.6))
    for i in range(n):
        t = i/L.FPS
        f = base.copy()
        f.alpha_composite(pic(t))
        d = ImageDraw.Draw(f)
        sp = min(t/SC, 1.0)
        if sp < 1.0:
            sy = int(py + sp*ph)
            gl = Image.new("RGBA", A.size, (0, 0, 0, 0))
            ImageDraw.Draw(gl).rectangle([px, sy-3, px+pw, sy+3], fill=LIME + (220,))
            f.alpha_composite(gl.filter(ImageFilter.GaussianBlur(6)))
            ImageDraw.Draw(f).rectangle([px, sy-1, px+pw, sy+1], fill=LIME + (255,))
            d = ImageDraw.Draw(f)
        for r, label in enumerate(ROWS):
            rt = SC + r*step
            if t < rt: continue
            p = min((t-rt)/max(0.42, step*0.85), 1.0)
            yy = ry0 + r*rowh + int(round(6*(t/dur)))
            c = int(255*p)
            d.text((rx0, yy), label, font=fL, fill=(c, c, c, 255) if p < 1 else (255, 255, 255, 255))
            by = yy + 58
            d.rounded_rectangle([rx0, by, rx1, by+barh], radius=14, fill=(34, 38, 30, 255))
            grow = min(1.0, max(0.0, (t - rt)/max(0.6, dur - rt - 0.2)))
            bw = int((rx1-rx0)*(0.25 + 0.60*grow)*p)
            if bw > 28:
                d.rounded_rectangle([rx0, by, rx0+bw, by+barh], radius=14, fill=OLIVE + (255,))
        rt = SC + len(ROWS)*step + 0.2
        if t >= rt:
            p = min((t-rt)/0.45, 1.0)
            yy = ry0 + len(ROWS)*rowh + 10 + int(round(6*(t/dur)))
            ov = Image.new("RGBA", A.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            od.rounded_rectangle([rx0, yy, rx1, yy+bandh], radius=16, fill=(28, 52, 33, int(255*p)))
            od.text(((rx0+rx1)//2, yy+bandh//2), "YOUR WORKOUT PLAN", font=fH,
                    fill=(255, 255, 255, int(255*p)), anchor="mm")
            f.alpha_composite(ov)
        f.alpha_composite(Image.open(chip_path).convert("RGBA"), chip_pos)
        frames.append(f)
    return frames, {"chip_pos": chip_pos, "chip_png": chip_path, "photo_box": list(photo_box),
                    "chip_why": "on the field above the picture (stats card); person mask clear",
                    "rows_box": [rx0, ry0, rx1, ry0+block]}


def endcard_frames(dur):
    """The one FULL-SCREEN card: chip, the AI picture (its 1:1 crop), the CTA and the URL, stacked.
    No caption shares a frame with it (the last line's hold is clipped to its in-point)."""
    img, crop_meta = square_crop("ai")
    top = 150
    side = 580
    layer, box = layer_from(img, ((A.VW-side)//2, top, (A.VW+side)//2, top+side))
    base = L.field(A)
    fB = font(58, "ExtraBold"); fU = font(52, "ExtraBold")
    n = L.nf(dur)
    # NO "AbsByAI.com" LINE (Dan, 2026-10-01: no AbsByAI.com mark at the end of a video). The approved
    # 9:16 end card predates that rule and prints it; the square is a new file, so it carries the
    # "Tap the button below" call to action only.
    pill = [A.SAFE, 776, A.VW-A.SAFE, 776+124]
    url_y = None
    assert pill[3] <= 980, "CTA below the square's bottom safe line"
    chip_path, chip_pos, wh = chip_xy("ai", A.VW/2)
    AMP = 0.03

    w = box[2]-box[0]+1; h = box[3]-box[1]+1
    emask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(emask).rounded_rectangle([0, 0, w-1, h-1], radius=22, fill=255)

    def pic(t):
        # zoom in place (float source box): continuous sub-pixel motion, the box itself never grows
        p = min(max(t/dur, 0.0), 1.0); k = 1.0 + AMP*p
        sw, sh = img.width/k, img.height/k
        bx = ((img.width-sw)/2, (img.height-sh)/2, (img.width+sw)/2, (img.height+sh)/2)
        im = img.resize((w, h), Image.LANCZOS, box=bx)
        lay = Image.new("RGBA", A.size, (0, 0, 0, 0)); lay.paste(im, (box[0], box[1]), emask)
        return lay
    probes = []
    for t in (0.0, dur):
        f = L.field(A); f.alpha_composite(pic(t)); probes.append(f)
    assert_chip_clear("end_card", probes, chip_pos, wh)
    assert box[3] < pill[1] - 8 and box[1] > chip_pos[1] + wh[1] + 4
    frames = []
    for i in range(n):
        t = i/L.FPS
        f = base.copy()
        f.alpha_composite(pic(t))
        d = ImageDraw.Draw(f)
        d.rounded_rectangle(pill, radius=18, fill=(28, 52, 33, 255))
        d.text((A.VW//2, (pill[1]+pill[3])//2), "Tap the button below", font=fB,
               fill=(255, 255, 255, 255), anchor="mm")
        f.alpha_composite(Image.open(chip_path).convert("RGBA"), chip_pos)
        frames.append(f)
    return frames, {"chip_pos": chip_pos, "chip_png": chip_path, "photo_box": list(box),
                    "chip_why": "on the field above the picture (end card); person mask clear",
                    "square_crop": crop_meta, "pill": pill, "url_y": url_y}


def macro_clip(dur, nfr, out):
    """The real macro-tracker recording inside A.CARD_RECT: the vertical's exact window and pan
    (1280x1420 at x 20, y 900 -> 1000 over the beat; recording 40.50 s on), fitted whole."""
    cw, ch, cxs = 1280, 1420, 20
    y0, y1 = 900, 1000
    rx0, ry0, rx1, ry1 = A.CARD_RECT
    k = min((rx1-rx0)/cw, (ry1-ry0)/ch)
    nw, nh = int(cw*k), int(ch*k); nw -= nw % 2; nh -= nh % 2
    ox, oy = rx0 + ((rx1-rx0)-nw)//2, ry0 + ((ry1-ry0)-nh)//2
    fieldp = f"{OUT}/_macro_field.png"
    fim = L.field(A)
    hole = Image.new("L", A.size, 255)
    ImageDraw.Draw(hole).rounded_rectangle([ox, oy, ox+nw-1, oy+nh-1], radius=22, fill=0)
    fim.putalpha(hole); fim.save(fieldp)
    pan = f"{y0}+({y1}-{y0})*t/{dur:.3f}"
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
    raw = subprocess.run([L.FF, "-v", "error", "-nostdin", "-i", out, "-vf", "format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, A.VH, A.VW)
    m = [float(a[i].mean()) for i in (0, 1, len(a)-2, len(a)-1)]
    assert min(m[0], m[-1]) > 0.5*max(m), f"macro card: frame luma {m}"
    return {"slice": [MS["in"], MS["out"]], "crop": [cw, ch, cxs, y0, y1], "scale": round(k, 4),
            "frame_luma_first_last": [round(x, 1) for x in m], "placed": [ox, oy, ox+nw-1, oy+nh-1]}


ONLY = set(x for x in os.environ.get("ONLY", "").split(",") if x)
meta = json.load(open(f"{OUT}/meta.json"))["cards"] if (ONLY and os.path.exists(f"{OUT}/meta.json")) else {}
for i, c in enumerate(B["cards"]):
    if ONLY and c["name"] not in ONLY: continue
    nfr = c["frames"]; dur = nfr/L.FPS
    out = f"{OUT}/{c['name']}.mp4"
    if c["kind"] == "clip":
        assert MS["in"] + dur <= MS["out"] + 1e-3
        meta[c["name"]] = macro_clip(dur, nfr, out)
    elif c["kind"] == "scan":
        fr, m = scan_frames(dur); L.encode_h264(fr[:nfr], out, A.size); meta[c["name"]] = m
    elif c["kind"] == "endcard":
        fr, m = endcard_frames(dur); L.encode_h264(fr[:nfr], out, A.size); meta[c["name"]] = m
    else:
        # the same drift direction the vertical gave this card (index parity in the sorted list)
        fr, m = photo_frames(c["asset"], dur, c["chip"], 1 if i % 2 == 0 else -1, c["name"])
        L.encode_h264(fr[:nfr], out, A.size); meta[c["name"]] = m
    print(f"  {c['name']:<11} {nfr:4d}f -> {out}  chip {meta[c['name']].get('chip_pos')}  "
          f"box {meta[c['name']].get('photo_box') or meta[c['name']].get('placed')}")
chips = {k: chip_for(k) for k in ("ai", "real")}
json.dump({"chips": {k: v[0] for k, v in chips.items()}, "chip_size": {k: v[1] for k, v in chips.items()},
           "card_rect": list(A.CARD_RECT), "chip_box": list(A.CHIP_BOX), "cards": meta},
          open(f"{OUT}/meta.json", "w"), indent=1)
print("cards done ->", OUT)
