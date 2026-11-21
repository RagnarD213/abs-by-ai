"""RO-21 round 3 (from RO-20 negscan_r4): contact sheets for the negative-events scan: one frame every STEP s plus the middle of every
covered clip/card, labelled with its time.  usage: negscan.py [STEP]  -> round3/final/negscan/sheet_NN.jpg + frames.json
            negscan.py record 'findings json list'  -> round3/final/negative_events_scan.json for the exact master"""
import sys, os, json, subprocess, hashlib, datetime
from PIL import Image, ImageDraw
D = "/Volumes/Expansion/_edit_work/RO-21/round3/final"; M = f"{D}/RO21_MASTER.mp4"; O = f"{D}/negscan"
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
if len(sys.argv) > 1 and sys.argv[1] == "record":
    h = hashlib.sha256()
    with open(M, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    fr = json.load(open(f"{O}/frames.json"))
    rec = dict(sha256=h.hexdigest(), when=datetime.datetime.now().astimezone().isoformat(timespec="seconds"), frames_checked=fr["n"],
               by="Claude Opus 5.5 (editor), RO-21 round 3", method=f"{fr['n']} frames: one every 10 s plus the middle of every cutaway and card, looked at sheet by sheet",
               findings=json.loads(sys.argv[2]))
    json.dump(rec, open(f"{D}/negative_events_scan.json", "w"), indent=1); print(rec["frames_checked"], rec["sha256"][:12]); sys.exit()
os.makedirs(O, exist_ok=True); STEP = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
P = json.load(open(f"{D}/plan.json")); total = P["target_seconds"]
ts = sorted(set([round(STEP*k + STEP/2, 2) for k in range(int(total // STEP))] + [round((a + b)/2, 2) for a, b in P["covered"]]))
tiles = []
for t in ts:
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", M, "-frames:v", "1", "-vf", "scale=384:216", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    im = Image.frombytes("RGB", (384, 216), raw); d = ImageDraw.Draw(im); d.rectangle((0, 0, 70, 16), fill=(0, 0, 0)); d.text((3, 2), f"{int(t//60)}:{t % 60:04.1f}", fill=(255, 255, 0))
    tiles.append(im)
for k in range(0, len(tiles), 30):
    sh = Image.new("RGB", (384*6, 216*5))
    for j, im in enumerate(tiles[k:k+30]): sh.paste(im, (384*(j % 6), 216*(j//6)))
    sh.save(f"{O}/sheet_{k//30:02d}.jpg", quality=72)
json.dump(dict(times=ts, n=len(ts)), open(f"{O}/frames.json", "w")); print(len(ts), "frames,", (len(tiles) + 29)//30, "sheets")
