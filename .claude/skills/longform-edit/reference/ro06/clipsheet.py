"""Contact sheet of an AI take: every Nth frame, numbered with frame and time, for the frame-by-frame fault read.
usage: clipsheet.py CLIP.mp4 OUT.jpg [every=3] [cols=6] [width=480] [x:y:w:h crop in source px]"""
import sys, subprocess, json
from PIL import Image, ImageDraw
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
clip, out = sys.argv[1], sys.argv[2]; ev = int(sys.argv[3]) if len(sys.argv) > 3 else 3; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
wd = int(sys.argv[5]) if len(sys.argv) > 5 else 480; crop = sys.argv[6] if len(sys.argv) > 6 else None
pr = json.loads(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries", "stream=nb_read_frames,r_frame_rate,width,height", "-of", "json", clip], capture_output=True, text=True).stdout)["streams"][0]
n = int(pr["nb_read_frames"]); a, b = pr["r_frame_rate"].split("/"); fps = int(a)/int(b); W, H = pr["width"], pr["height"]
if crop: x, y, w, h = map(int, crop.split(":"))
else: x, y, w, h = 0, 0, W, H
ht = int(round(wd*h/w/2))*2
vf = f"crop={w}:{h}:{x}:{y},scale={wd}:{ht}:in_color_matrix=bt709:in_range=tv,format=rgb24"
raw = subprocess.run([FF, "-v", "error", "-i", clip, "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
idx = list(range(0, n, ev)); sheet = Image.new("RGB", (wd*cols, ht*((len(idx)+cols-1)//cols)))
for k, f in enumerate(idx):
    im = Image.frombytes("RGB", (wd, ht), raw[f*wd*ht*3:(f+1)*wd*ht*3]); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 92, 14), fill=(0, 0, 0)); d.text((3, 1), f"{f}  {f/fps:.2f}s", fill=(255, 255, 0)); sheet.paste(im, ((k % cols)*wd, (k//cols)*ht))
sheet.save(out, quality=85); print(n, "frames", fps, "fps", W, H, "->", out)
