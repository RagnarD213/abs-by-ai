"""Round 3 negative-events frames: every 10 s plus the middle of every clip and AI insert, 3x3 labelled sheets, final/negscan."""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
OUT = "final/negscan"; V = "final/RO37_R3_MASTER.mp4"; FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
sys.path.insert(0, "recipe"); import r2
pts = [(float(t), f"{t // 60:.0f}:{t % 60:04.1f}") for t in range(0, 475, 10)]
for c in r2.CLIPS: t = (c["t0"] + c["t1"]) / 2; pts.append((t, f"{c['id']} {t // 60:.0f}:{t % 60:04.1f}"))
pts.sort(); os.makedirs(OUT, exist_ok=True); rec = []
for k, (t, lab) in enumerate(pts):
    p = f"{OUT}/f{k:03d}.jpg"
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", V, "-frames:v", "1", "-vf", "scale=640:360", "-q:v", "3", p], check=True); rec.append(dict(t=round(t, 3), label=lab, path=p))
json.dump(rec, open(f"{OUT}/frames.json", "w"), indent=1)
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
for s in range(0, len(rec), 9):
    sheet = Image.new("RGB", (1920, 1080), "black"); d = ImageDraw.Draw(sheet)
    for j, r in enumerate(rec[s:s + 9]):
        x, y = (j % 3) * 640, (j // 3) * 360; sheet.paste(Image.open(r["path"]), (x, y)); d.rectangle([x, y, x + 280, y + 34], fill="black"); d.text((x + 6, y + 4), r["label"], fill="yellow", font=font)
    sheet.save(f"{OUT}/sheet_{s // 9:02d}.jpg", quality=85)
print(len(rec), "frames")
