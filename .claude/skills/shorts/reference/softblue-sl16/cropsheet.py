"""SL-16: for every cover clip, 3 frames (in, mid, out of its used range) with the vertical fill window drawn at its fx (scaled to cover 1080x1610)."""
import sys, json, subprocess, numpy as np, plans as P
from PIL import Image, ImageDraw
FF = "/Users/danielrose/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real"
OUT = "/tmp/absbyai-scratch/SL-16/crops"
for S in sys.argv[1:]:
    rows = []
    for sh in [x for x in json.load(open(f"build/{S}/shots.json")) if x["kind"] == "clip"]:
        c = sh["cover"]; ims = []
        for k, t in enumerate((sh["raw0"] + 0.03, (sh["raw0"] + sh["raw1"]) / 2, sh["raw1"] - 0.03)):
            b = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", c["src"], "-frames:v", "1", "-vf", "scale=640:360:in_color_matrix=bt709", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            im = Image.frombytes("RGB", (640, 360), b); dr = ImageDraw.Draw(im)
            ww = 640 * (1080 / (1610 * 16 / 9)); x0 = (640 - ww) * c.get("fx", 0.5)
            dr.rectangle((x0, 0, x0 + ww, 359), outline=(255, 40, 40), width=3)
            for g in range(1, 10): dr.line((g * 64, 0, g * 64, 8), fill=(255, 255, 0))
            dr.text((6, 6), f"{c['id']} fx{c.get('fx',0.5)} t{t:.2f}", fill=(255, 255, 0)); ims.append(im)
        row = Image.new("RGB", (1920, 360)); [row.paste(im, (k * 640, 0)) for k, im in enumerate(ims)]; rows.append(row)
    sh = Image.new("RGB", (1920, 360 * len(rows))); [sh.paste(r, (0, k * 360)) for k, r in enumerate(rows)]
    sh.save(f"{OUT}/{S}.jpg", quality=80); print(f"{OUT}/{S}.jpg")
