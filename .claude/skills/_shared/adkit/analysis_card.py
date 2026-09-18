#!/usr/bin/env python3
"""adkit.analysis_card -- the "AI reads your picture" card. REUSE THIS.

Dan, 2026-09-18, approving RA-01 ("The AI Trick That Got Me Abs"): "I especially like this graphic that you
made with the things to lose body fat and gain muscle. Let's make this something that we reuse in future
videos... I think that illustrated it better than we did in past videos."

What it is: a picture of the subject on the J2AD field, a lime scan line sweeping down it, then three
label-and-bar rows building in (BODY FAT / FAT TO LOSE / MUSCLE TO GAIN) and a green plan band
(YOUR WORKOUT PLAN). Use it on any line that says the app ANALYSES the picture and turns it into a plan.

Rules it enforces (they are why it passed three review rounds -- do not route around them):
  * NO PRINTED NUMBERS. Rows are labels and bars, never a weight, a percentage or a date: a printed figure
    is a claim (memory `ad-copy-no-unbelievable-claims`). Digits in --rows/--footer are refused.
  * The picture carries exactly one label chip: `--label ai` (AI-GENERATED) or `--label real` ("Real picture
    of me -- not AI-generated"); placed by person mask, never on face, hair or abs. `--label none` is only
    for a picture with no physique in it.
  * Same person throughout a video: the subject here must be the person whose before/after the video shows.
  * The card stops above the caption band, so captions keep running under it. It enters and leaves on hard
    cuts and never stops moving (slow drift).

CLI (writes <out>.mp4 at the delivered size/rate + <out>.json with the geometry the delivery gate needs):
  python3 .claude/skills/_shared/adkit/analysis_card.py --image "Media/example pictures/dan by pool.png" \
      --aspect 9x16 --dur 5.2 --label ai --out /Volumes/Extreme/_edit_work/<job>/cards/analysis_9x16
Python:
  from analysis_card import build; meta = build(image, "16x9", 5.2, out, label="ai")
Minimum useful duration ~4 s (scan ≈ 26 % of the beat, then the rows); RA-01 ran it 5.2 s under
"AI analyzed it and figured out exactly how much fat I had to lose - and where I had to gain muscle".
Put `meta["chip_png"]`/`meta["chip_pos"]` in the gate plan's `ai_inserts` (or `real_photos`) entry and
`meta["card_rect"]` in `cards`/`graphic_regions`.
"""
import argparse, hashlib, json, os, re, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from PIL import Image, ImageDraw, ImageFilter
import cardlib as L
from cardlib import Aspect, LIME, OLIVE, PLAN_GREEN, CHIP_AI, CHIP_REAL
import motionlib as ml
from motionlib import font

ROWS = ["BODY FAT", "FAT TO LOSE", "MUSCLE TO GAIN"]
FOOTER = "YOUR WORKOUT PLAN"


def _frames(image, A, dur, rows, footer, label, workdir, tag):
    img = ml.oriented(Image.open(image).convert("RGB"))
    cx0, cy0, cx1, cy1 = A.CARD_RECT
    CW_, CH_ = cx1 - cx0, cy1 - cy0
    if A.key == "9x16":
        pw = int(CW_ * 0.585); pw -= pw % 2
        ph = int(pw * img.height / img.width); ph -= ph % 2
        room = CH_ - (26 + 66 * len(rows) + 10 + 70)          # rows + plan band must fit under the picture
        if ph > room:                                         # a taller picture is fitted, never cropped
            ph = room - room % 2; pw = int(ph * img.width / img.height); pw -= pw % 2
        px, py = cx0 + (CW_ - pw) // 2, cy0
        rx0, rx1 = cx0 + 40, cx1 - 40
        ry0, rowh, bandh, fLs, fHs = py + ph + 26, 66, 70, 32, 38
    else:
        STRIP = 86                                            # reserved strip above the picture for the chip
        ph = int((CH_ - STRIP) * 0.99); ph -= ph % 2
        pw = int(ph * img.width / img.height); pw -= pw % 2
        px, py = cx0 + 60, cy0 + STRIP
        rx0, rx1 = px + pw + 70, cx1 - 40
        ry0, rowh, bandh, fLs, fHs = cy0 + STRIP + 150, 96, 104, 36, 44
    img = img.resize((pw, ph), Image.LANCZOS)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=18, fill=255)
    ph_layer = Image.new("RGBA", A.size, (0, 0, 0, 0)); ph_layer.paste(img, (px, py), mask)
    fL, fH = font(fLs, "ExtraBold"), font(fHs, "ExtraBold")
    base = L.field(A)
    n = L.nf(dur)
    barw = int((rx1 - rx0) * 0.46)

    chip_path = chip_pos = chip_why = None
    if label != "none":
        text = CHIP_AI if label == "ai" else CHIP_REAL
        if A.key == "9x16":
            cbox, cmax = A.CHIP_BOX, A.CHIP_BOX[2] - A.CHIP_BOX[0]
        else:
            cbox, cmax = (px, cy0 + 8, px + pw, cy0 + 78), pw - 8
        chip_path = os.path.join(workdir, f"{tag}_chip_{label}.png")
        cw, ch = L.chip_png(text, chip_path, size=40 if A.key == "9x16" else 38, max_w=cmax)
        probe = L.field(A); probe.alpha_composite(ph_layer)
        pm = L.person_mask(probe)
        if pm is None:
            raise SystemExit("analysis card: person mask failed (is the personmask binary on disk?) -- "
                             "a chip is never placed blind")
        if A.key == "9x16":
            chip_pos, chip_why = L.place_chip([pm], (cw, ch), A, box=cbox)
        else:
            chip_pos = (px, cy0 + 8 + max(0, (70 - ch) // 2))
            chip_why = "the reserved strip above the picture"
        if pm[chip_pos[1]:chip_pos[1] + ch, chip_pos[0]:chip_pos[0] + cw].any():
            raise SystemExit(f"analysis card: the chip at {chip_pos} touches the person -- shrink or move the picture")
        chip_im = Image.open(chip_path).convert("RGBA")

    frames = []
    SC = max(1.0, dur * 0.26)
    step = max(0.42, (dur - SC - 0.9) / (len(rows) + 0.6))
    for i in range(n):
        t = i / L.FPS
        f = base.copy()
        f.alpha_composite(L.kb(ph_layer, t, dur, 1, amp=0.045, canvas=A.size))
        d = ImageDraw.Draw(f)
        sp = min(t / SC, 1.0)
        if sp < 1.0:                                           # the scan line
            sy = int(py + sp * ph)
            gl = Image.new("RGBA", A.size, (0, 0, 0, 0))
            ImageDraw.Draw(gl).rectangle([px, sy - 3, px + pw, sy + 3], fill=LIME + (220,))
            f.alpha_composite(gl.filter(ImageFilter.GaussianBlur(6)))
            ImageDraw.Draw(f).rectangle([px, sy - 1, px + pw, sy + 1], fill=LIME + (255,))
            d = ImageDraw.Draw(f)
        for r, lab in enumerate(rows):
            rt = SC + r * step
            if t < rt: continue
            p = min((t - rt) / max(0.42, step * 0.85), 1.0)
            yy = ry0 + r * rowh + int(round(6 * (t / dur)))
            d.text((rx0, yy), lab, font=fL, fill=(255, 255, 255, int(255 * p)))
            bx = rx1 - barw
            d.rounded_rectangle([bx, yy + 4, rx1, yy + 30], radius=13, fill=(34, 38, 30, 255))
            grow = min(1.0, max(0.0, (t - rt) / max(0.6, dur - rt - 0.2)))
            d.rounded_rectangle([bx, yy + 4, bx + int(barw * (0.25 + 0.60 * grow) * p), yy + 30],
                                radius=13, fill=OLIVE + (255,))
        rt = SC + len(rows) * step + 0.2
        if footer and t >= rt:
            p = min((t - rt) / 0.45, 1.0)
            yy = ry0 + len(rows) * rowh + 10 + int(round(6 * (t / dur)))
            d.rounded_rectangle([rx0, yy, rx1, yy + bandh], radius=16, fill=PLAN_GREEN + (int(255 * p),))
            d.text(((rx0 + rx1) // 2, yy + bandh // 2), footer, font=fH,
                   fill=(255, 255, 255, int(255 * p)), anchor="mm")
        if chip_path:
            f.alpha_composite(chip_im, chip_pos)
        frames.append(f)
    meta = {"aspect": A.key, "dur": dur, "frames": n, "rows": rows, "footer": footer, "label": label,
            "chip_png": chip_path, "chip_pos": list(chip_pos) if chip_pos else None, "chip_why": chip_why,
            "photo_box": [px, py, px + pw - 1, py + ph - 1], "card_rect": list(A.CARD_RECT),
            "image": os.path.abspath(image)}
    return frames, meta


def build(image, aspect, dur, out, rows=None, footer=FOOTER, label="ai"):
    """Render the card to <out>.mp4 and <out>.json; returns the metadata dict."""
    rows = list(rows or ROWS)
    for s in rows + [footer or ""]:
        if re.search(r"\d", s):
            raise SystemExit(f"analysis card: '{s}' prints a number -- labels and bars only (see the module docstring)")
    if label not in ("ai", "real", "none"):
        raise SystemExit("--label must be ai, real or none")
    if dur < 3.5:
        raise SystemExit("analysis card: under 3.5 s the rows cannot build; give the beat more time or use a still")
    A = Aspect(aspect)
    workdir = os.path.dirname(os.path.abspath(out)) or "."
    os.makedirs(workdir, exist_ok=True)
    frames, meta = _frames(image, A, float(dur), rows, footer, label, workdir, os.path.basename(out))
    mp4 = out + ".mp4"
    L.encode_h264(frames, mp4, A.size)
    meta["mp4"] = os.path.abspath(mp4)
    meta["sha256"] = hashlib.sha256(open(mp4, "rb").read()).hexdigest()
    json.dump(meta, open(out + ".json", "w"), indent=1)
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--image", required=True, help="the subject's picture (portrait works best)")
    ap.add_argument("--aspect", required=True, choices=["9x16", "16x9"])
    ap.add_argument("--dur", type=float, required=True, help="beat length in seconds (>= 3.5; RA-01 used 5.2)")
    ap.add_argument("--out", required=True, help="output path WITHOUT extension")
    ap.add_argument("--label", required=True, choices=["ai", "real", "none"])
    ap.add_argument("--rows", nargs="+", default=ROWS)
    ap.add_argument("--footer", default=FOOTER)
    a = ap.parse_args()
    m = build(a.image, a.aspect, a.dur, a.out, a.rows, a.footer, a.label)
    print(json.dumps({k: m[k] for k in ("mp4", "frames", "chip_pos", "chip_why", "photo_box")}, indent=1))
