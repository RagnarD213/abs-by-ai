"""Keep the lip sync on the CLIENT only. sync/lipsync-2-pro with active_speaker also moved the trainer's mouth (A1, last
0.8 s), so the delivered clip is the untouched trimmed take everywhere except a soft-edged box round the client's face,
which comes from the synced clip. Both files are the same frames at the same size, so nothing moves at the box edge.
Merged on the raw YUV planes: an RGB round trip darkened the whole clip by about 2 levels.
usage: syncfix.py TRIM.mp4 SYNC.mp4 x:y:w:h OUT.mp4 [feather=40]"""
import sys, subprocess, numpy as np
from PIL import Image, ImageFilter
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
trim, sync, box, out = sys.argv[1:5]; fe = int(sys.argv[5]) if len(sys.argv) > 5 else 40
x, y, w, h = map(int, box.split(":")); WW, HH = 1920, 1080; NY = WW*HH; NC = NY//4
m = Image.new("L", (WW, HH), 0); m.paste(255, (x+fe, y+fe, x+w-fe, y+h-fe)); m = m.filter(ImageFilter.GaussianBlur(fe/2))
my = np.asarray(m, np.float32).ravel()/255; mc = np.asarray(m.resize((WW//2, HH//2), Image.BILINEAR), np.float32).ravel()/255; mk = np.concatenate([my, mc, mc])
def rd(p): return subprocess.Popen([FF, "-v", "error", "-i", p, "-pix_fmt", "yuv420p", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
a, b = rd(trim), rd(sync); n = 0; sz = NY + 2*NC
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", f"{WW}x{HH}", "-framerate", "24", "-i", "-", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                        "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
while True:
    fa, fb = a.stdout.read(sz), b.stdout.read(sz)
    if len(fa) < sz or len(fb) < sz: break
    A = np.frombuffer(fa, np.uint8).astype(np.float32); B = np.frombuffer(fb, np.uint8).astype(np.float32)
    enc.stdin.write(np.clip(A*(1-mk) + B*mk + 0.5, 0, 255).astype(np.uint8).tobytes()); n += 1
enc.stdin.close(); enc.wait(); print(n, "frames ->", out)
