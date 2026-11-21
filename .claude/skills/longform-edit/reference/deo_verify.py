#!/usr/bin/env python3
"""Render each deodorant window twice, LOSSLESSLY, and prove three things:
  1. zero pixels change outside the box,
  2. the change inside the box is a reduction of the grey residue,
  3. nothing else in the box (bright background, skin) is smudged.
Point 3 is the one that bites: the first pass used a box that reached past his
arm onto the white fridge, whose shadowed side reads val 0.55-0.62 - inside the
filter's own gate - and the "fix" painted a grey smudge across it, which is far
worse than the residue. Comparison is lossless because x264 rate allocation is
global: at CRF 20 a 19k-pixel edit in one corner changes every macroblock in the
frame, so a lossy A/B can never show zero.
usage: deo_verify.py
"""
import json, subprocess, io, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

B = "/Volumes/Extreme/_edit_work/spraytan"
OUTPNG = "/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/dae62b2c-e3c9-48e6-8e67-6badf48f7e80/scratchpad/DEO_VERIFY.png"
edl = json.load(open(f"{B}/edl.json")); SRC = edl["sources"]["C1512"]; G = edl["grade"]
rng = {r["beat"]: r for r in edl["ranges"]}
sys.path.insert(0, B)
import importlib.util
spec = importlib.util.spec_from_file_location("av", f"{B}/apply_vf.py")
# SHORT windows only. The armpit is on screen for well under a second at a time
# in these gestures, so this is the only regime where a static box is valid at
# all - over 2.5s his arm travels right out of it (measured: intro t=148.9 the
# pit sits at x1150-1225, by t=150.1 it has left the frame region entirely).
DEO = [
 ("intro",              12.90, 13.70, [(1145, 630, 1235, 775)]),
 ("how-long-it-lasts",   4.60,  5.30, [(1285, 682, 1355, 810)]),
 ("how-long-it-lasts",   5.90,  6.40, [(1325, 632, 1400, 770)]),
]
FEATHER = 14

def graph(boxes, tag):
    n = len(boxes)
    parts = [f"split={n+1}[{tag}m0]" + "".join(f"[{tag}k{i}]" for i in range(n))]
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        w, h = x1-x0, y1-y0
        MX = "max(max(r(X,Y),g(X,Y)),b(X,Y))"; MN = "min(min(r(X,Y),g(X,Y)),b(X,Y))"
        SAT = f"(({MX})-({MN}))/max({MX},1)"; VAL = f"({MX})/255"
        BOX = f"clip(min(X\\,{w}-X)/{FEATHER}\\,0\\,1)*clip(min(Y\\,{h}-Y)/{FEATHER}\\,0\\,1)"
        W = f"({BOX})*clip((0.45-({SAT}))/0.20\\,0\\,1)*clip((0.62-({VAL}))/0.15\\,0\\,1)"
        parts.append(f"[{tag}k{i}]crop={w}:{h}:{x0}:{y0},format=gbrap,"
                     f"geq=r='r(X\\,Y)*(1-0.28*({W}))':g='g(X\\,Y)*(1-0.45*({W}))'"
                     f":b='b(X\\,Y)*(1-0.63*({W}))':a='255*({W})',format=yuva420p[{tag}p{i}]")
    main = f"{tag}m0"
    for i,(x0,y0,x1,y1) in enumerate(boxes):
        nxt=f"{tag}m{i+1}"
        parts.append(f"[{main}][{tag}p{i}]overlay={x0}:{y0}:format=yuv420[{nxt}]"); main=nxt
    return ";".join(parts), main

def grab(path, idx):
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    o = subprocess.run(["ffmpeg","-nostdin","-v","error","-i",path,"-vf",f"select='{sel}'",
        "-vsync","0","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
    out=[]; i=0
    while True:
        j=o.find(b"\x89PNG",i+1)
        out.append(np.asarray(Image.open(io.BytesIO(o[i:j if j>0 else len(o)])).convert("RGB")).astype(int))
        if j<0: break
        i=j
    return out

f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 22)
tiles, ok_all = [], True
for beat, a, b, boxes in DEO:
    r = rng[beat]; ss = r["start"] + a; dur = b - a
    g, out = graph(boxes, "".join(c for c in beat if c.isalpha())[:7])
    for name, extra in (("plain", None), ("deo", f"{g};[{out}]null")):
        vf = f"scale=1920:-2,{G}" + (f",{extra}" if extra else "")
        subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{ss:.3f}","-i",SRC,
            "-t",f"{dur:.3f}","-vf",vf,"-an","-c:v","ffv1","-pix_fmt","yuv420p",
            "-r","30000/1001",f"/tmp/V_{name}.mkv"],check=True)
    n = max(1, int(dur*29.97))
    idx = sorted({int(n*0.15), int(n*0.5), int(n*0.85)})
    A, Bf = grab("/tmp/V_plain.mkv", idx), grab("/tmp/V_deo.mkv", idx)
    x0,y0,x1,y1 = boxes[0]
    outside_max = 0; inside = []
    for pa, pb in zip(A, Bf):
        d = np.abs(pa-pb).sum(2); m = d.copy(); m[y0:y1, x0:x1] = 0
        outside_max = max(outside_max, int(m.max()))
        inside.append((int((d[y0:y1,x0:x1]>0).sum()), int(d[y0:y1,x0:x1].max())))
    ok = outside_max == 0
    ok_all &= ok
    print(f"{beat:20s} box {boxes[0]}  outside-max {outside_max}  inside {inside}  {'OK' if ok else 'LEAK'}")
    cx,cy = (x0+x1)//2, (y0+y1)//2
    cw,ch = 150,140
    crop = (max(0,cx-cw), max(0,cy-ch), min(1920,cx+cw), min(1080,cy+ch))
    for pa,lab in ((A[len(A)//2],"BEFORE"),(Bf[len(Bf)//2],"AFTER")):
        c = Image.fromarray(np.uint8(pa)).crop(crop); c = c.resize((c.width*2, c.height*2))
        d = ImageDraw.Draw(c)
        d.rectangle([(x0-crop[0])*2,(y0-crop[1])*2,(x1-crop[0])*2,(y1-crop[1])*2], outline=(255,60,60), width=2)
        d.text((6,6), f"{beat[:14]} {lab}", font=f, fill=(255,230,0))
        tiles.append(c)
Wd = max(c.width for c in tiles); Ht = max(c.height for c in tiles)
sh = Image.new("RGB",(Wd*4, Ht*3),(18,18,18))
for i,c in enumerate(tiles): sh.paste(c,(Wd*(i%4), Ht*(i//4)))
sh.save(OUTPNG)
print("\nzero leakage outside every box:", ok_all)
print("wrote DEO_VERIFY.png")
