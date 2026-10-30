"""RO-29 R2: every AI slot rendered to its exact film length from the chosen take, colour corrected. Run after resolve."""
import json, subprocess, sys
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
W = "/Volumes/Expansion/_edit_work/RO-29/round2"; V = f"{W}/ai/veo"; O = f"{W}/ai/final"
AIG = "eq=brightness=-0.03:contrast=1.05:saturation=0.96"
#  id: (take, in, out, grade); out-in is retimed to the slot, so only a time-lapse may be faster than real time
T = {"A0": ("A0-flow-t1", 1.9, None, AIG), "A1": ("A1o-flow-t1", 0.0, None, AIG),
     "A1B": ("A1B-flow-t2", 0.0, 6.5, None), "A2": ("A2b-flow-t1", 0.0, None, None), "A3": ("A3-flow-t1", 2.6, None, AIG),
     "A5": ("A5b-flow-t1", 0.0, None, AIG), "A6": ("A6c-flow-t1", 0.0, None, None), "A4D": ("A4Db-flow-t1", 1.2, None, None), "A7": ("A7e-flow-t1", 1.0, None, None)}
def still_pitcher():
    """R3 (Dan): the pitcher shimmered through the end of A0. Hold it on its first frame; anything that really moves (phone, hand) stays live."""
    import numpy as np, cv2
    src = f"{O}/A0.mp4"; tmp = f"{O}/A0_still.mp4"
    r = subprocess.Popen([FF, "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    e = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                          "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
    x0, y0, x1, y1 = 90, 60, 520, 980
    box = np.zeros((1080, 1920), np.float32); box[y0:y1, x0:x1] = 1; box = cv2.GaussianBlur(box, (0, 0), 8)
    plate = None
    while True:
        b = r.stdout.read(1920*1080*3)
        if len(b) < 1920*1080*3: break
        f = np.frombuffer(b, np.uint8).reshape(1080, 1920, 3).astype(np.float32)
        if plate is None: plate = f.copy()
        d = cv2.GaussianBlur(np.abs(f - plate).max(2), (0, 0), 3)
        moving = cv2.GaussianBlur(((d > 70) & (np.arange(1920)[None, :] > 430)).astype(np.float32), (0, 0), 4)   # the phone only ever reaches the right edge of the pitcher
        moving = np.clip(moving*3, 0, 1)
        a = (box*(1 - moving))[..., None]
        e.stdin.write(np.clip(f*(1 - a) + plate*a, 0, 255).astype(np.uint8).tobytes())
    e.stdin.close(); e.wait(); r.wait(); os.replace(tmp, src)

def steady_a7():
    """R3: the START-only eating take bumps the camera about 19 px; hold the room still on its first frame."""
    import numpy as np, cv2
    src = f"{O}/A7.mp4"; tmp = f"{O}/A7_still.mp4"
    r = subprocess.Popen([FF, "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    e = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                          "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", tmp], stdin=subprocess.PIPE)
    x0, y0, x1, y1 = 1500, 160, 1900, 520     # the lit wall at the right: nothing crosses it
    ref = None; maxd = 0
    while True:
        b = r.stdout.read(1920*1080*3)
        if len(b) < 1920*1080*3: break
        f = np.frombuffer(b, np.uint8).reshape(1080, 1920, 3)
        g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY).astype(np.float32)[y0:y1, x0:x1]
        if ref is None: ref = g
        (dx, dy), _ = cv2.phaseCorrelate(ref, g); maxd = max(maxd, abs(dy))
        M = np.float32([[1, 0, -dx], [0, 1, -dy]])
        o = cv2.warpAffine(f, M, (1920, 1080), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        e.stdin.write(o.tobytes())
    e.stdin.close(); e.wait(); r.wait(); os.replace(tmp, src); print("A7 steadied, largest shift", round(maxd, 1))

P = json.load(open(f"{W}/plan_resolved.json")); items = P if isinstance(P, list) else P["items"]
import os; os.makedirs(O, exist_ok=True)
for id_, (tk, a, b, g) in T.items():
    it = next(x for x in items if x["id"] == id_); d = it["t1"] - it["t0"]
    b2 = b if b else a + d
    f = (b2 - a) / d
    vf = f"trim=start={a}:end={b2 + 0.15*f},setpts=(PTS-STARTPTS)/{f:.5f},fps=30000/1001" + (f",{g}" if g else "") + ",format=yuv420p"
    inp = ["-i", f"{V}/{tk}.mp4"]; fl = ["-vf", vf]
    if id_ == "A1B":  # time-lapse: jump past the half second where cups form from nothing (take 2.75 to 3.55), more hours gone
        f = 5.7 / d
        fl = ["-filter_complex", f"[0:v]trim=start=0:end=2.75,setpts=PTS-STARTPTS[a];[0:v]trim=start=3.55:end=6.65,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1,setpts=PTS/{f:.5f},fps=30000/1001,format=yuv420p"]
    if id_ == "A1":   # the take garbles the phone's text; the phone never moves, so pin the approved frame's phone over it
        inp += ["-i", f"{W}/ai/a1_phone.png"]; fl = ["-filter_complex", f"[0:v][1:v]overlay=140:610:eof_action=repeat,{vf}", "-t", f"{d + 0.1:.3f}"]
    subprocess.run([FF, "-v", "error", "-y"] + inp + fl + [ "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", f"{O}/{id_}.mp4"], check=True)
    print(id_, tk, f"{a}-{b2:.2f}", "x%.2f" % f, round(d, 2))
still_pitcher()
