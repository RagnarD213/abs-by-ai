"""First-minute QC pictures: a contact sheet (one frame every 1.5 s) and a strip of the five consecutive frames
(-2 -1 | 0 +1 +2) at every picture cut. usage: fm_qc.py MASTER.mp4 OUT_DIR"""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import build as Bd
master, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); FPS = Bd.FPS
n = int(subprocess.run([Bd.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v", "-show_entries", "stream=nb_frames", "-of", "csv=p=0", master], capture_output=True, text=True).stdout)
sg = Bd.all_segments(); cuts = {}
for a, b in zip(sg, sg[1:]):
    if b["o0"] < n and (a["crop"] != b["crop"] or not Bd.same_take(a, b)): cuts[b["o0"]] = f"{a['key']} {a['framing']} > {b['key']} {b['framing']}"
for it in Bd.R:
    if it["kind"] in Bd.FULL and Bd.fr(it["t0"]) < n:
        f0, f1 = Bd.fr(it["t0"]), Bd.fr(it["t1"]); k = len(it.get("src", [1])); per = (f1-f0)//k
        for j in range(k): cuts[f0 + j*per] = f"{it['id']} clip {j+1}" if j else f"into {it['id']}"
        if f1 < n: cuts[f1] = f"out of {it['id']}" + (" > " + cuts[f1] if f1 in cuts else "")
want = sorted({f for c in cuts for f in range(c-2, c+3) if 0 <= f < n} | {int(round(t*1.5*FPS)) for t in range(int(n/FPS/1.5)+1) if int(round(t*1.5*FPS)) < n})
sel = "+".join(f"eq(n\\,{f})" for f in want)
d = f"{out}/_f"; os.makedirs(d, exist_ok=True)
subprocess.run([Bd.FF, "-v", "error", "-y", "-i", master, "-vf", f"select='{sel}',scale=480:270:in_color_matrix=bt709:in_range=tv", "-vsync", "0", "-q:v", "3", f"{d}/%04d.jpg"], check=True)
im = {f: Image.open(f"{d}/{k+1:04d}.jpg") for k, f in enumerate(want)}
cs = sorted(cuts); strip = Image.new("RGB", (480*5+20, 290*len(cs)), (20, 20, 20)); dr = ImageDraw.Draw(strip)
for r, c in enumerate(cs):
    for j, f in enumerate(range(c-2, c+3)):
        if f in im: strip.paste(im[f], (j*480 + (20 if j >= 2 else 0), r*290+20))
    dr.text((6, r*290+4), f"{c/FPS:6.2f} s  frame {c}  {cuts[c]}", fill=(255, 255, 255))
strip.save(f"{out}/fm_joins.jpg", quality=82)
ts = [int(round(t*1.5*FPS)) for t in range(int(n/FPS/1.5)+1) if int(round(t*1.5*FPS)) < n]; cols = 7
sheet = Image.new("RGB", (480*cols, 270*((len(ts)+cols-1)//cols)))
for k, f in enumerate(ts):
    t = im[f].copy(); ImageDraw.Draw(t).text((6, 4), f"{f/FPS:.1f}", fill=(255, 255, 0)); sheet.paste(t, ((k % cols)*480, (k//cols)*270))
sheet.save(f"{out}/fm_sheet.jpg", quality=80)
json.dump({str(c): cuts[c] for c in cs}, open(f"{out}/fm_cuts.json", "w"), indent=1); print(len(cs), "cuts;", len(ts), "sheet frames")
for c in cs: print(f"  {c/FPS:6.2f}  {cuts[c]}")
