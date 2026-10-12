"""RO-19 round 3: carry the independent judge's watch-pass verdicts from the judged render (round3/film_v2) to the corrected render (round3/film).
Every frame of both masters is compared (480x270 grey, PSNR). A strip or pair keeps its verdict only when every frame within 4 frames of its boundary is
unchanged (PSNR >= 38 dB) AND the judged render had a boundary at the same time (matched by time, not by file name: the boundary count changed);
a sheet keeps it only when no frame in its span changed. Everything else is listed for a fresh judge.
usage: carry19r3.py [JUDGED_DIR FINDINGS.json]   (default film_v2 logs/findings.json; for the last render: film_v3 logs/findings_merged.json)
-> film/logs/psnr_vs_<dir>.json, film/logs/findings_carried.json, film/logs/judge_list.json"""
import json, subprocess, numpy as np, re, sys
OLD = sys.argv[1] if len(sys.argv) > 1 else "film_v2"; OLDF = sys.argv[2] if len(sys.argv) > 2 else "logs/findings.json"
W = "/Volumes/Extreme/_edit_work/ro19/round3"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001; M = "RO-19 round 3 - full film.mp4"; TH = 38.0
def reader(p): return subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", p, "-vf", "scale=480:270,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
a, b = reader(f"{W}/{OLD}/{M}"), reader(f"{W}/film/{M}"); ps = []
while True:
    x, y = a.stdout.read(480*270), b.stdout.read(480*270)
    if len(x) < 480*270 or len(y) < 480*270: assert len(x) == len(y), "the two renders differ in length"; break
    d = np.frombuffer(x, np.uint8).astype(np.float32) - np.frombuffer(y, np.uint8).astype(np.float32); mse = float((d*d).mean())
    ps.append(99.0 if mse < 1e-6 else round(10*np.log10(255*255/mse), 2))
ps = np.array(ps); ch = np.nonzero(ps < TH)[0]; runs = []
for f in ch:
    if runs and f - runs[-1][1] <= 2: runs[-1][1] = int(f)
    else: runs.append([int(f), int(f)])
json.dump(dict(frames=len(ps), threshold=TH, changed_frames=len(ch), changed_runs=[[r[0], r[1], round(r[0]/FPS, 3), round((r[1]+1)/FPS, 3)] for r in runs],
               min_psnr_unchanged=float(ps[ps >= TH].min()), median=float(np.median(ps))), open(f"{W}/film/logs/psnr_vs_{OLD}.json", "w"), indent=1)
print(len(ps), "frames;", len(ch), "changed in", len(runs), "runs:", [(round(r[0]/FPS, 1), round((r[1]+1)/FPS, 1)) for r in runs], "| lowest PSNR among the unchanged:", ps[ps >= TH].min())
old = {}
for e in json.load(open(f"{W}/{OLD}/{OLDF}"))["entries"]: old.setdefault(e["image"], []).append(e)
def pair_of(s): return re.sub(r"^strip_(\d+_[\d\-.]+).*$", r"pair_\1.jpg", s)
wo = json.load(open(f"{W}/{OLD}/logs/watch_pass.json")); wp = json.load(open(f"{W}/film/logs/watch_pass.json"))
oldb = {int(round(x["t"]*FPS)): x["strip"] for x in wo["boundary_list"]}; carried, todo = [], []
def changed(f0, f1): return bool((ps[max(0, f0):min(len(ps), f1 + 1)] < TH).any())
TAG = "[carried from the judged render of this round: frames unchanged] "
def tag(n): return n if n.startswith("[carried") else TAG + n
for bnd in wp["boundary_list"]:
    f = int(round(bnd["t"]*FPS)); s = bnd["strip"]; so = oldb.get(f)
    for im, imo in ((s, so), (pair_of(s), pair_of(so) if so else None)):
        if imo and imo in old and not changed(f - 4, f + 4): carried += [dict(e, image=im, note=tag(e.get("note", ""))) for e in old[imo]]
        else: todo.append(im)
for sh in wp["sheets"]:
    m = re.match(r"sheet_\d+_(\d+)-(\d+\.\d+)_to_(\d+)-(\d+\.\d+)", sh); t0 = int(m[1])*60 + float(m[2]); t1 = int(m[3])*60 + float(m[4])
    if sh in old and not changed(int(t0*FPS), int(t1*FPS) + 2): carried += [dict(e, note=tag(e.get("note", ""))) for e in old[sh]]
    else: todo.append(sh)
assert not [e for e in carried if e["verdict"] == "defect"], "a defect verdict was carried: its frames must have changed"
json.dump(dict(entries=carried), open(f"{W}/film/logs/findings_carried.json", "w"), indent=0); json.dump(todo, open(f"{W}/film/logs/judge_list.json", "w"), indent=0)
print("carried", len({e["image"] for e in carried}), "images;", "to judge fresh:", len(todo))
