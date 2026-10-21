"""RO-14 round 2: independent EVERY-FRAME top-edge hair test (VIDEO-RULES 2026-10-20, test B), calibrated on this set.
Over every presenter frame (not under a full-frame clip/scene/title), the top TOP rows across Dan's head band must not be
hair-coloured: the fraction of pixels darker than LUMA_MAX (his black hair reads ~20-35; the dark green backdrop's darkest
texture ~45+ after the grade, measured on round 1 frames) must stay under DARK_MAX. usage: hairedge.py MASTER plan_resolved.json OUT.json"""
import sys, json, subprocess, numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real"; FPS = 30000/1001
master, planp, outp = sys.argv[1:4]
R = json.load(open(planp)); fr = lambda t: int(round(t * FPS))
FULL = [(fr(r["t0"]), fr(r["t1"])) for r in R if r["kind"] in ("clip", "scene", "title") and r["t1"]]   # frame numbers, as the builder cuts
p = subprocess.run(["/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=width,height", "-of", "csv=p=0", master], capture_output=True, text=True).stdout.strip().split(",")
W, H = int(p[0]), int(p[1]); s = H / 1080
TOP = max(4, round(12 * s)); X0, X1 = round(660 * s), round(1260 * s); LUMA_MAX = 40; DARK_MAX = 0.20
dec = subprocess.Popen([FF, "-v", "error", "-i", master, "-vf", f"crop={X1-X0}:{TOP}:{X0}:0,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
n = 0; checked = 0; worst = (0.0, None); bad = []
while True:
    b = dec.stdout.read((X1 - X0) * TOP)
    if len(b) < (X1 - X0) * TOP: break
    t = n / FPS; g = n; n += 1
    if any(a <= g < z for a, z in FULL): continue
    a = np.frombuffer(b, np.uint8); f = float((a < LUMA_MAX).mean()); checked += 1
    if f > worst[0]: worst = (f, round(t, 3))
    if f >= DARK_MAX: bad.append((round(t, 3), round(f, 3)))
res = dict(master=master, size=[W, H], frames=n, presenter_frames_checked=checked, top_rows=TOP, band=[X0, X1], luma_max=LUMA_MAX,
           dark_max=DARK_MAX, worst_fraction=round(worst[0], 4), worst_t=worst[1], failing_frames=len(bad), failing=bad[:50])
json.dump(res, open(outp, "w"), indent=1); print(json.dumps({k: v for k, v in res.items() if k != "failing"}))
