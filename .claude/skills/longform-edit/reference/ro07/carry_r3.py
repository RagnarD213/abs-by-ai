"""RO-07 round 3: carry the independent judge's watch-pass verdicts from the judged first render (round3/render1) to the corrected
render. Every frame of both masters is compared (480x270 grey, PSNR). A strip or pair keeps its verdict only when every frame
within 4 frames of its boundary is unchanged (PSNR >= 38 dB); a sheet keeps it only when no frame in its span changed. Everything
else is listed for a fresh judge. usage: carry_r3.py   -> logs/psnr_vs_render1.json, logs/findings_carried.json, logs/judge_list.json"""
import json, subprocess, numpy as np, re
W = "/Volumes/Extreme/_edit_work/ro07/round3"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001; M = "RO-07 round 3 - full film.mp4"; TH = 38.0
def reader(p): return subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", p, "-vf", "scale=480:270,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
a, b = reader(f"{W}/render1/{M}"), reader(f"{W}/{M}"); ps = []
while True:
    x, y = a.stdout.read(480*270), b.stdout.read(480*270)
    if len(x) < 480*270 or len(y) < 480*270: assert len(x) == len(y), "the two renders differ in length"; break
    d = np.frombuffer(x, np.uint8).astype(np.float32) - np.frombuffer(y, np.uint8).astype(np.float32); mse = float((d*d).mean())
    ps.append(99.0 if mse < 1e-6 else round(10*np.log10(255*255/mse), 2))
ps = np.array(ps); ch = np.nonzero(ps < TH)[0]
runs = []
for f in ch:
    if runs and f - runs[-1][1] <= 2: runs[-1][1] = int(f)
    else: runs.append([int(f), int(f)])
json.dump(dict(frames=len(ps), threshold=TH, changed_frames=len(ch), changed_runs=[[r[0], r[1], round(r[0]/FPS, 3), round((r[1]+1)/FPS, 3)] for r in runs],
               min_psnr_unchanged=float(ps[ps >= TH].min()), median=float(np.median(ps))), open(f"{W}/logs/psnr_vs_render1.json", "w"), indent=1)
print(len(ps), "frames;", len(ch), "changed in", [(r[0], r[1]) for r in runs], "| lowest PSNR among the unchanged:", ps[ps >= TH].min())
old = {}
for e in json.load(open(f"{W}/render1/logs/findings.json"))["entries"]: old.setdefault(e["image"], []).append(e)
wp = json.load(open(f"{W}/logs/watch_pass.json")); carried, todo = [], []
def changed(f0, f1): return bool((ps[max(0, f0):min(len(ps), f1 + 1)] < TH).any())
for bnd in wp["boundary_list"]:
    f = int(round(bnd["t"]*FPS)); s = bnd["strip"]; p = re.sub(r"^strip_(\d+_[\d\-.]+).*$", r"pair_\1.jpg", s)
    for im in (s, p):
        if im in old and not changed(f - 4, f + 4): carried += [dict(e, note="[carried from the judged first render: frames unchanged] " + e.get("note", "")) for e in old[im]]
        else: todo.append(im)
for sh in wp["sheets"]:
    m = re.match(r"sheet_\d+_(\d+)-(\d+\.\d+)_to_(\d+)-(\d+\.\d+)", sh); t0 = int(m[1])*60 + float(m[2]); t1 = int(m[3])*60 + float(m[4])
    if sh in old and not changed(int(t0*FPS), int(t1*FPS) + 2): carried += [dict(e, note="[carried from the judged first render: frames unchanged] " + e.get("note", "")) for e in old[sh]]
    else: todo.append(sh)
json.dump(dict(entries=carried), open(f"{W}/logs/findings_carried.json", "w"), indent=0); json.dump(todo, open(f"{W}/logs/judge_list.json", "w"), indent=0)
print("carried", len({e["image"] for e in carried}), "images;", "to judge fresh:", len(todo), todo)
