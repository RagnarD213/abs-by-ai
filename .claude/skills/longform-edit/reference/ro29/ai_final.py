"""RO-29 R2: every AI slot rendered to its exact film length from the chosen take, colour corrected. Run after resolve."""
import json, subprocess, sys
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
W = "/Volumes/Expansion/_edit_work/RO-29/round2"; V = f"{W}/ai/veo"; O = f"{W}/ai/final"
AIG = "eq=brightness=-0.03:contrast=1.05:saturation=0.96"
#  id: (take, in, out, grade); out-in is retimed to the slot, so only a time-lapse may be faster than real time
T = {"A0": ("A0-flow-t1", 1.9, None, AIG), "A1": ("A1o-flow-t1", 0.0, None, AIG),
     "A1B": ("A1B-flow-t2", 0.0, 6.5, None), "A2": ("A2b-flow-t1", 0.0, None, None), "A3": ("A3-flow-t1", 2.6, None, AIG),
     "A5": ("A5b-flow-t1", 0.0, None, AIG), "A6": ("A6b-flow-t1", 0.0, None, None), "A7": ("A7-flow-t1", 3.3, None, None)}
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
        inp += ["-i", f"{W}/ai/a1_phone.png"]; fl = ["-filter_complex", f"[0:v][1:v]overlay=330:652:eof_action=repeat,{vf}", "-t", f"{d + 0.1:.3f}"]
    subprocess.run([FF, "-v", "error", "-y"] + inp + fl + [ "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", f"{O}/{id_}.mp4"], check=True)
    print(id_, tk, f"{a}-{b2:.2f}", "x%.2f" % f, round(d, 2))
