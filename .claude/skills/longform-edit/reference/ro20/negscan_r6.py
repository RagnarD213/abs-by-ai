"""RO-20 round 4: contact sheets for the negative-events scan (Google 'Negative Events and Imagery'): one frame every STEP s plus the middle of every
clip with people in it, labelled with its time. usage: negscan_r4.py V [STEP]  -> round6/V/negscan/sheet_NN.jpg + frames.json"""
import sys, os, json, subprocess
from PIL import Image, ImageDraw
W = "/Volumes/Extreme/_edit_work/ro20"; FPS = 30000/1001; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
V = sys.argv[1]; STEP = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0; D = f"{W}/round6/{V}"; O = f"{D}/negscan"; os.makedirs(O, exist_ok=True)
P = json.load(open(f"{D}/plan.json")); total = P["target_seconds"]
ts = [round(STEP*k + STEP/2, 2) for k in range(int(total // STEP))]
ts += [round((a + b)/2, 2) for a, b in P["covered"]]                 # every cutaway / card, once
ts = sorted(set(ts))
tiles = []
for t in ts:
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", f"{D}/MASTER.mp4", "-frames:v", "1", "-vf", "scale=384:216", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    im = Image.frombytes("RGB", (384, 216), raw); d = ImageDraw.Draw(im); d.rectangle((0, 0, 70, 16), fill=(0, 0, 0)); d.text((3, 2), f"{int(t//60)}:{t % 60:04.1f}", fill=(255, 255, 0))
    tiles.append(im)
for k in range(0, len(tiles), 30):
    sh = Image.new("RGB", (384*6, 216*5))
    for j, im in enumerate(tiles[k:k+30]): sh.paste(im, (384*(j % 6), 216*(j//6)))
    sh.save(f"{O}/sheet_{k//30:02d}.jpg", quality=72)
json.dump(dict(times=ts, n=len(ts)), open(f"{O}/frames.json", "w")); print(V, len(ts), "frames,", (len(tiles) + 29)//30, "sheets")
