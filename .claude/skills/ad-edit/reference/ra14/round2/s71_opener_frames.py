#!/usr/bin/env python3
"""RA-14 round 2: finish the six opener frames (O1 Character creator, O2 8-bit power-up, O3 Arcade combo).

Codex made the pictures with NO lettering (round2/opener/raw, prompts beside them). Here:
  round2/frames/<ID>-start.png / -end.png   the clean 1080x1920 frame a motion model would be given (nothing drawn on it)
  round2/stills/<ID>-start.jpg / -end.jpg   the same frame AS IT WOULD PLAY: our drawn interface (O1 slider, O2 counter),
                                            the AI-GENERATED chip clear of every face, and the real caption of that moment
Every letter on screen is drawn here, in code. No motion is generated in round 2.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra14")
import ra01lib as L
sys.path.insert(0, f"{L.REPO}/.claude/skills/_shared")
import softblue as B
W, H = 1080, 1920
RAW = "round2/opener/raw"; FR = "round2/frames"; ST = "round2/stills"
CAPS = json.load(open("cap_9x16/caption_states.json"))["states"]
CYAN = B.CYAN


def clean(k, which):
    im = Image.open(f"{RAW}/{k}_{which}.png").convert("RGB")
    s = max(W/im.width, H/im.height); nw, nh = round(im.width*s), round(im.height*s)
    flt = Image.NEAREST if k == "o2" else Image.LANCZOS            # pixel art keeps its hard edges
    im = im.resize((nw, nh), flt).crop(((nw-W)//2, (nh-H)//2, (nw-W)//2+W, (nh-H)//2+H))
    im.save(f"{FR}/{k.upper()}-{which}.png"); return im.convert("RGBA")


def caption(im, t):
    for s in CAPS:
        if s["beat"][0] <= t < s["beat"][1]:
            im.alpha_composite(Image.open(s["image"]).convert("RGBA")); return s["line"]
    return None


def slider(im, v):
    """O1's interface: one body slider in a glass panel above his head, the knob at v (0..1), a pointer on the knob."""
    x0, y0, x1, y1 = 84, 200, 996, 328
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0, y0+6, x1, y1+6), 26, fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    pn = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(pn)
    d.rounded_rectangle((x0, y0, x1, y1), 26, fill=(10, 30, 56, 225), outline=(99, 176, 224, 200), width=2)
    im.alpha_composite(pn); d = ImageDraw.Draw(im)
    f1, f2 = B.font(38, True), B.font(42, True)
    d.text((x0+34, y0+14), "BODY: ABS", font=f1, fill=CYAN)
    val = f"{round(v*100)}%"; d.text((x1-34-B.text_w(val, f2), y0+10), val, font=f2, fill=(255, 255, 255))
    tx0, tx1, ty = x0+40, x1-40, y0+94
    d.rounded_rectangle((tx0, ty-7, tx1, ty+7), 7, fill=(34, 62, 96))
    kx = tx0 + (tx1-tx0)*v
    if v > 0: d.rounded_rectangle((tx0, ty-7, kx, ty+7), 7, fill=CYAN)
    d.ellipse((kx-21, ty-21, kx+21, ty+21), fill=(255, 255, 255), outline=CYAN, width=5)
    cx, cy = kx+6, ty+8                                           # the pointer that is dragging the knob
    pts = [(0, 0), (0, 44), (11, 34), (19, 52), (27, 48), (19, 31), (33, 31)]
    d.polygon([(cx+px+3, cy+py+4) for px, py in pts], fill=(0, 0, 0, 150))
    d.polygon([(cx+px, cy+py) for px, py in pts], fill=(255, 255, 255), outline=(8, 18, 30))


GLY = {  # 5x7 pixel letters for O2's counter (drawn by us, not generated)
 "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"], "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
 "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"], "X": ["00000", "00000", "10001", "01010", "00100", "01010", "10001"],
 "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"], "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
 " ": ["00000"]*7}


def pixel_text(im, s, x, y, px=12, fill=(255, 255, 255)):
    d = ImageDraw.Draw(im)
    for off, col in (((px//2, px//2), (0, 0, 0)), ((0, 0), fill)):
        cx = x
        for ch in s:
            for r, row in enumerate(GLY[ch]):
                for c, bit in enumerate(row):
                    if bit == "1": d.rectangle((cx+c*px+off[0], y+r*px+off[1], cx+(c+1)*px-1+off[0], y+(r+1)*px-1+off[1]), fill=col)
            cx += 6*px
    return cx


def main():
    META = {}
    T_START, T_END = 0.75, 3.35                 # caption moments: "Guys have figured out" / "... six-pack abs."
    for k in ("o1", "o2", "o3"):
        for which, t in (("start", T_START), ("end", T_END)):
            im = clean(k, which)
            if k == "o1": slider(im, 0.0 if which == "start" else 1.0)
            if k == "o2": pixel_text(im, "ABS X0" if which == "start" else "ABS X6", 70, 216)
            chip = B.disclosure(im, "AI-GENERATED", xy=(60, 1296), anchor="lt")       # low left, above the caption line, on no face
            line = caption(im, t)
            im.convert("RGB").save(f"{ST}/{k.upper()}-{which}.jpg", quality=93)
            META[f"{k.upper()}-{which}"] = dict(caption=line, t=t, chip=[round(c) for c in chip])
    json.dump(META, open(f"{ST}/opener_meta.json", "w"), indent=1)
    print(json.dumps(META, indent=1))


if __name__ == "__main__":
    main()
