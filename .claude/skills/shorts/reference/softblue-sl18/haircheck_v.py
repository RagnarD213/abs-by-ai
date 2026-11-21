#!/usr/bin/env python3
"""SL-18 headroom check on the DELIVERED vertical (VIDEO-RULES 2026-10-20, "Head and hair clearance blocks review delivery"):
every 0.25 s of presenter picture plus both native frames at every talking-shot join, Apple Vision person mask, top of the
mask (hair) measured from the top of the picture area (canvas y 310, under the title band) in delivered 1080 x 1920 pixels.
Pass: at least 20 px on every valid sample; a missed detection is UNRESOLVED, never a pass. Writes OUT.json + a native-scale
proof strip of the eight tightest samples.
usage: haircheck_v.py S"""
import sys, os, json, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import plans as P, batch as Bt
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sl18_deliver", os.path.join(HERE, "deliver.py")); Dl = _iu.module_from_spec(_sp); _sp.loader.exec_module(Dl)
FF = Bt.lib.FF; PM = Bt.PM; FPS = Bt.FPS; DROP = 310
S = sys.argv[1]; d = Bt.D(S); V = Dl.dname(S); sha = Dl.sha(V)
shots = json.load(open(f"{d}/shots.json")); talk = [s for s in shots if s["kind"] == "talk"]
want = []
for s in talk:
    a, b = s["f0"], s["f1"]
    want += list(range(a + 1, b - 1, max(1, int(round(FPS / 4)))))
    want += [a, a + 1, b - 2, b - 1]                       # native frames at both sides of every join
want = sorted(set(want))
wd = f"{d}/hair"; os.makedirs(wd + "/m", exist_ok=True)
for f in glob.glob(wd + "/*.png") + glob.glob(wd + "/m/*"): os.remove(f)
sel = "+".join(f"eq(n\\,{n})" for n in want)
subprocess.run([FF, "-v", "error", "-y", "-i", V, "-vf", f"select='{sel}',scale=in_color_matrix=bt709:in_range=tv", "-vsync", "0", f"{wd}/f_%05d.png"], check=True)
fs = sorted(f for f in glob.glob(wd + "/f_*.png") if not os.path.basename(f).startswith("._"))
assert len(fs) == len(want), (len(fs), len(want))
crops = []
for f in fs:                                              # the mask runs on the picture area only (the title band is not him)
    im = Image.open(f).convert("RGB"); c = im.crop((0, DROP, 1080, 1920)); p = f[:-4] + "_pic.png"; c.save(p); crops.append(p)
for i in range(0, len(crops), 150): subprocess.run([PM, wd + "/m"] + crops[i:i + 150], check=True, capture_output=True)
rows = []
for n, f, p in zip(want, fs, crops):
    mp = f"{wd}/m/{os.path.basename(p)[:-4]}.mask.png"
    sh = next(s for s in talk if s["f0"] <= n < s["f1"])
    if not os.path.exists(mp): rows.append(dict(f=n, t=round(n / FPS, 3), shot=sh["idx"], top=None)); continue
    m = np.asarray(Image.open(mp).convert("L")) > 127
    from scipy import ndimage
    lab, k = ndimage.label(m)
    if not k: rows.append(dict(f=n, t=round(n / FPS, 3), shot=sh["idx"], top=None)); continue
    big = lab == (int(np.argmax(ndimage.sum(m, lab, range(1, k + 1)))) + 1)
    sc = 1610 / m.shape[0]; ys = np.where(big.sum(1) >= max(3, int(6 / sc)))[0]
    rows.append(dict(f=n, t=round(n / FPS, 3), shot=sh["idx"], win=sh.get("win"), top=round(float(ys[0]) * sc, 1) if len(ys) else None, frame=f))
valid = [r for r in rows if r["top"] is not None]; bad = [r for r in valid if r["top"] < 20]; miss = [r for r in rows if r["top"] is None]
worst = sorted(valid, key=lambda r: r["top"])[:8]
strip = Image.new("RGB", (8 * 540, 700), (0, 0, 0))
for i, r in enumerate(worst):
    im = Image.open(r["frame"]).convert("RGB").crop((0, DROP - 40, 1080, DROP + 660)).resize((540, 350)); dd = ImageDraw.Draw(im)
    dd.line((0, 20, 540, 20), fill=(255, 0, 0), width=1); dd.text((4, 30), f"{r['t']:.2f}s shot {r['shot']} {r.get('win')}: {r['top']:.0f} px", fill=(255, 255, 0))
    strip.paste(im, (i * 540, 0))
    nat = Image.open(r["frame"]).convert("RGB").crop((270, DROP, 810, DROP + 350)); strip.paste(nat, (i * 540, 350))      # native scale, the top 350 rows
strip.save(f"{d}/hair_worst.jpg", quality=90)
res = dict(file=V, sha256=sha, samples=len(rows), valid=len(valid), unresolved=len(miss), min_px=min(r["top"] for r in valid) if valid else None,
           median_px=float(np.median([r["top"] for r in valid])) if valid else None, under_20=[(r["t"], r["top"]) for r in bad],
           worst=[(r["t"], r["shot"], r.get("win"), r["top"]) for r in worst], verdict="PASS" if valid and not bad and not miss else "FAIL",
           proof=f"{d}/hair_worst.jpg", method="every ~0.25 s of each talking shot + its first two and last two native frames; Vision person mask on the 1080 x 1610 picture area; largest component; first row with >= 6 px of mask")
json.dump(dict(summary=res, rows=[{k: v for k, v in r.items() if k != "frame"} for r in rows]), open(f"{d}/hair_check.json", "w"), indent=1)
print(json.dumps(res, indent=1))
