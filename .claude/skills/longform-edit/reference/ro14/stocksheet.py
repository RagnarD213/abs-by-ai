"""Contact sheets of stock candidates: 4 frames per clip (10/35/60/85 %), labelled id + duration + size. usage: stocksheet.py OUTPREFIX id id ..."""
import sys, subprocess, json, os
from PIL import Image, ImageDraw, ImageFont
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FP = FF.replace("ffmpeg", "ffprobe")
D = "/Volumes/Extreme/_edit_work/RO-14/round1/stock"
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
rows = []
for i in sys.argv[2:]:
    p = f"{D}/p{i}.mp4" if os.path.exists(f"{D}/p{i}.mp4") else i
    j = json.loads(subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", p], capture_output=True, text=True).stdout)
    dur = float(j["format"]["duration"]); w, h = j["streams"][0]["width"], j["streams"][0]["height"]
    fr = []
    for q in (.1, .35, .6, .85):
        b = subprocess.run([FF, "-v", "error", "-ss", f"{dur*q:.2f}", "-i", p, "-frames:v", "1", "-vf", "scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        fr.append(Image.frombytes("RGB", (320, 180), b) if len(b) == 320*180*3 else Image.new("RGB", (320, 180)))
    row = Image.new("RGB", (1280, 204), (20, 20, 20)); [row.paste(f, (k*320, 24)) for k, f in enumerate(fr)]
    ImageDraw.Draw(row).text((6, 2), f"{os.path.basename(p)}  {dur:.1f}s  {w}x{h}", fill=(255, 230, 0), font=font)
    rows.append(row)
for k in range(0, len(rows), 8):
    S = Image.new("RGB", (1280, 204*len(rows[k:k+8]))); [S.paste(r, (0, 204*n)) for n, r in enumerate(rows[k:k+8])]
    S.save(f"{sys.argv[1]}_{k//8}.jpg", quality=82); print(f"{sys.argv[1]}_{k//8}.jpg")
