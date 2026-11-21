"""RO-08 round 2: the time-lapse opener (Dan's idea), assembled from the four Veo moves between his five approved key frames.
Time-lapse part: OTa (8 to 10), OTb (10 to 12) and OTc (12 to 2, the salad arrives), frames DROPPED (never blended) so 12 s of source runs
in TL seconds. Normal speed after that: OTd alone (he eats), 24 fps laid on 29.97 by repeating frames, never retimed.
usage: opener_ot.py OUT.mp4 [TL seconds=2.9] [total seconds=8.0]"""
import sys, subprocess, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; M = "/Volumes/Extreme/_edit_work/ro08/round2/motion"
out = sys.argv[1]; TL = float(sys.argv[2]) if len(sys.argv) > 2 else 3.2; TOT = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0; FPS = 30000/1001; SZ = 1920*1080*3//2
def frames(tag):
    raw = subprocess.run([FF, "-v", "error", "-i", f"{M}/{tag}.mp4", "-pix_fmt", "yuv420p", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return [raw[i:i+SZ] for i in range(0, len(raw), SZ)]
a, b, c, d = (frames(t) for t in ("OTa-t1", "OTb-t1", "OTc-t1", "OTd-t1")); K = 89     # the time-lapse ends on OTc frame 88, the frame closest to OTd's first (mean difference 2.2 levels, less than OTc's own frame-to-frame change; its LAST frame is 9.7 away: Veo overshoots the key frame and drifts). The first build cut from OTc's tail to OTd at normal speed and the join read as a jump (independent review, 0:04.3)
lapse = a + b[1:] + c[1:K]; normal = d[6:]          # OTd holds almost still for its first quarter second: skipped, so the picture never reads frozen where the time-lapse stops            # b[0] is a's last key frame and c[0] is b's: dropped so no picture shows twice
n_tl = int(round(TL*FPS)); n_all = int(round(TOT*FPS)); seq = [lapse[min(len(lapse)-1, int(round(i*(len(lapse)-1)/(n_tl-1))))] for i in range(n_tl)]
seq += [normal[min(len(normal)-1, int(j*24/FPS))] for j in range(n_all - n_tl)]
assert int((n_all - n_tl - 1)*24/FPS) < len(normal), "the normal-speed part runs out of source: never hold a frame"
enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-", "-an", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                        "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out], stdin=subprocess.PIPE)
for f in seq: enc.stdin.write(f)
enc.stdin.close(); enc.wait()
print(out, len(seq), "frames;", len(lapse), "source frames in", n_tl, f"({len(lapse)/24/TL:.2f}x); normal speed from", round(n_tl/FPS, 2), "s using", int((n_all-n_tl-1)*24/FPS)+1, "of", len(normal), "source frames")
