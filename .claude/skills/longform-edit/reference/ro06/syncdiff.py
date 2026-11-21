"""Where did the lip sync change the picture? Mean absolute difference per frame between the trimmed take and the synced
clip inside named boxes (source px), so a moved trainer mouth shows as a number. usage: syncdiff.py TRIM.mp4 SYNC.mp4 name=x:y:w:h ..."""
import sys, subprocess, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def load(p): 
    raw = subprocess.run([FF, "-v", "error", "-i", p, "-vf", "scale=960:540,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 540, 960).astype(np.float32)
a, b = load(sys.argv[1]), load(sys.argv[2]); n = min(len(a), len(b)); d = np.abs(a[:n]-b[:n])
print(n, "frames; whole frame mean diff", round(float(d.mean()), 2))
for s in sys.argv[3:]:
    name, box = s.split("="); x, y, w, h = [int(v)//2 for v in box.split(":")]; r = d[:, y:y+h, x:x+w].mean((1, 2))
    print(f"  {name:10s} mean {r.mean():5.2f}  max {r.max():5.2f}  frames over 3.0: {int((r > 3).sum())}")
