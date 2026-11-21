"""RO-06 round 3, C02: the equipment shot as a tight crop that pans left to right (Dan, 2026-10-08: "take a tighter crop
where the workout stuff is centered and then pan through that. Start at the kettlebell and then move ... all the way to the
right by the end of that clip's duration"). Source is the locked-off C1557 (1920x1080) or an upscaled copy of the same frames.
A fixed-height window travels on a float x (never integer steps), eased at both ends, with half-frame shutter blur so the
move reads as a camera pan, not a strobing slide. Output is UNGRADED BT.709 (build.py applies grade C1559 as before).
usage: c02_pan.py SRC.mp4 START_S OUT.mp4 [frames=88]"""
import sys, subprocess, math, numpy as np
from PIL import Image
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
src, st, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]; N = int(sys.argv[4]) if len(sys.argv) > 4 else 88
ZOOM = 2.25; Y0 = 598.0; X_START = 0.0; X_END = 732.0          # in 1920x1080 source pixels: kettlebell at left -> dumbbells at right
SUB = 8; SHUTTER = 0.5; RAMP = 0.22
pr = subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
SW, SH = int(pr[0]), int(pr[1]); k = SW/1920.0; cw, ch = 1920/ZOOM*k, 1080/ZOOM*k
def ease(t):                                                # trapezoid speed with cosine ramps: steady in the middle, soft at both ends
    t = min(1.0, max(0.0, t)); r = RAMP; v = 1/(1-r)
    if t < r: return v*(t/2 - r/(2*math.pi)*math.sin(math.pi*t/r))
    if t > 1-r: return 1 - ease(1-t)
    return v*(t - r/2)
dec = subprocess.Popen([FF, "-v", "error", "-ss", f"{st:.3f}", "-i", src, "-frames:v", str(N), "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-",
                        "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "6", "-preset", "medium",
                        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
for f in range(N):
    b = dec.stdout.read(SW*SH*3); assert len(b) == SW*SH*3, f"short read at frame {f}"
    im = Image.frombytes("RGB", (SW, SH), b); acc = np.zeros((1080, 1920, 3), np.float32)
    for j in range(SUB):
        t = (f + SHUTTER*(j + 0.5)/SUB)/N
        x = (X_START + (X_END - X_START)*ease(t))*k
        acc += np.asarray(im.resize((1920, 1080), Image.LANCZOS, box=(x, Y0*k, x + cw, Y0*k + ch)), np.float32)
    enc.stdin.write(np.clip(acc/SUB + 0.5, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); dec.wait(); print("pan written", out, N, "frames; window", round(cw/k), "x", round(ch/k), "at y", Y0, "x", X_START, "->", X_END)
