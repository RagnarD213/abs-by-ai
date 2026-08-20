#!/usr/bin/env python3
"""Study a reference ad: scene-detect + shot stats + per-shot contact sheets.

Usage:  python3 study_ad.py <video.mp4> [outdir]
Needs:  the static ffmpeg/ffprobe at Media/video_edit/bin (edit FF/FFPROBE below),
        PIL. Download the video first with the yt-dlp android-client command in
        AD_STUDY.md. Sheets land in <outdir>/sheets, stats print to stdout.
"""
import re, sys, os, math, statistics, subprocess
from PIL import Image, ImageDraw

BIN = os.path.expanduser("~/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin")
FF, FFPROBE = os.path.join(BIN, "ffmpeg"), os.path.join(BIN, "ffprobe")

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(src) or "."
vid = os.path.splitext(os.path.basename(src))[0]
os.makedirs(os.path.join(out, "frames"), exist_ok=True)
os.makedirs(os.path.join(out, "sheets"), exist_ok=True)

scenes = os.path.join(out, f"scenes_{vid}.txt")
if not os.path.exists(scenes):
    subprocess.run([FF, "-nostdin", "-i", src,
                    "-vf", f"select='gt(scene,0.25)',metadata=print:file={scenes}",
                    "-an", "-f", "null", "-"],
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
times = [float(m) for m in re.findall(r"pts_time:([\d.]+)", open(scenes).read())]
dur = float(subprocess.check_output([FFPROBE, "-v", "error", "-show_entries",
                                     "format=duration", "-of", "csv=p=0", src]).strip())
bounds = [0.0] + times + [dur]
shots = [b - a for a, b in zip(bounds, bounds[1:])]

def seg(pred):
    s = [d for a, d in zip(bounds, shots) if pred(a)]
    return f"n={len(s)} median={statistics.median(s):.2f}s mean={statistics.mean(s):.2f}s max={max(s):.1f}s" if s else "-"
print(f"{vid}: {dur:.1f}s, {len(times)} cuts")
print("  all     :", seg(lambda a: True))
print("  first30 :", seg(lambda a: a < 30))
print("  after60 :", seg(lambda a: a >= 60))

mids = [(a + b) / 2 for a, b in zip(bounds, bounds[1:])]
tiles = []
for i, (t, a) in enumerate(zip(mids, bounds)):
    p = os.path.join(out, "frames", f"{vid}_{i:03d}.jpg")
    if not os.path.exists(p):
        subprocess.run([FF, "-nostdin", "-ss", str(t), "-i", src, "-frames:v", "1",
                        "-q:v", "5", p], stdin=subprocess.DEVNULL,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tiles.append((p, a))
TW, TH, COLS, PER = 384, 216, 6, 30
for s in range(math.ceil(len(tiles) / PER)):
    chunk = tiles[s * PER:(s + 1) * PER]
    rows = math.ceil(len(chunk) / COLS)
    img = Image.new("RGB", (COLS * TW, rows * (TH + 18)), (20, 20, 20))
    d = ImageDraw.Draw(img)
    for j, (p, start) in enumerate(chunk):
        r, c = divmod(j, COLS)
        try:
            img.paste(Image.open(p).resize((TW, TH)), (c * TW, r * (TH + 18)))
        except Exception:
            pass
        d.text((c * TW + 4, r * (TH + 18) + TH + 2),
               f"#{s*PER+j} @{int(start//60)}:{start%60:04.1f}", fill=(255, 255, 0))
    img.save(os.path.join(out, "sheets", f"{vid}_s{s}.jpg"), quality=82)
print(f"  sheets  : {math.ceil(len(tiles)/PER)} in {out}/sheets/")
