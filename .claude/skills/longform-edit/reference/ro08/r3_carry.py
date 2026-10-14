"""RO-08 round 3: carry the independent judges' watch-pass verdicts to the delivered round 3 film from the films already judged: the round 2
film Dan reviewed (round2/, 0 open defects) and this round's earlier renders (round3/render1/ to render4/, each judged fresh on the
images that had changed). Every frame of every master is compared with the delivered one (480x270 grey, PSNR). A strip or pair keeps a
verdict only when every frame within 4 frames of its boundary is unchanged against the film that verdict was given on (PSNR >= 38 dB);
a sheet only when no frame in its span changed. Images are matched on their kind and time, not on the running number in the name (two
clips left the film, so the numbers after 1:58 shift). A verdict of "defect" is never carried. Everything else is listed for a fresh judge.
usage: r3_carry.py -> round3/logs/psnr_vs_<film>.json, findings_carried.json, judge_list.json"""
import json, subprocess, numpy as np, re
B = "/Volumes/Extreme/_edit_work/ro08"; W = f"{B}/round3"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001; N = "RO-08 round 3 - full film.mp4"; NEW = f"{W}/{N}"; TH = 38.0; SZ = 480*270; import os
FILMS = [("round2", "the judged round 2 film", f"{B}/round2/RO-08 round 2 - full film.mp4", f"{B}/round2/logs/findings.json")]
FILMS += [(r, f"this round's judged {w} render", f"{W}/{r}/{N}", f"{W}/{r}/logs/findings_new.json") for r, w in (("render1", "first"), ("render2", "second"), ("render3", "third"), ("render4", "fourth")) if os.path.exists(f"{W}/{r}/{N}")]
def reader(p): return subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", p, "-vf", "scale=480:270,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
def psnr(x, y):
    d = np.frombuffer(x, np.uint8).astype(np.float32) - np.frombuffer(y, np.uint8).astype(np.float32); mse = float((d*d).mean()); return 99.0 if mse < 1e-6 else round(10*np.log10(255*255/mse), 2)
rd = [reader(f[2]) for f in FILMS]; c = reader(NEW); PS = [[] for _ in FILMS]
while True:
    z = c.stdout.read(SZ); xs = [r.stdout.read(SZ) for r in rd]
    if min([len(z)] + [len(x) for x in xs]) < SZ: assert all(len(x) == len(z) for x in xs), "the films differ in length"; break
    for k, x in enumerate(xs): PS[k].append(psnr(x, z))
def runs(ps):
    ch = np.nonzero(ps < TH)[0]; r = []
    for f in ch:
        if r and f - r[-1][1] <= 2: r[-1][1] = int(f)
        else: r.append([int(f), int(f)])
    return len(ch), [[x[0], x[1], round(x[0]/FPS, 3), round((x[1]+1)/FPS, 3)] for x in r]
PS = [np.array(p) for p in PS]
for (name, _, _, _), ps in zip(FILMS, PS):
    n, r = runs(ps); json.dump(dict(frames=len(ps), threshold=TH, changed_frames=n, changed_runs=r, min_psnr_unchanged=float(ps[ps >= TH].min()), median=float(np.median(ps))), open(f"{W}/logs/psnr_vs_{name}.json", "w"), indent=1)
    print(f"against {name}: {len(ps)} frames; {n} changed in {[(x[0], x[1], x[2], x[3]) for x in r]} | lowest PSNR among the unchanged: {ps[ps >= TH].min()}")
def key(im):
    m = re.match(r"^(strip|pair)_\d+_(\d+-\d+\.\d+)", im) or re.match(r"^(sheet)_\d+_(\d+-\d+\.\d+_to_\d+-\d+\.\d+)", im); return (m[1], m[2]) if m else (im, "")
def load(p):
    o = {}
    for e in json.load(open(p))["entries"]: o.setdefault(key(e["image"]), []).append(e)
    return {k: v for k, v in o.items() if not any(e["verdict"] == "defect" for e in v)}
SRC = [(what, load(fj), ps) for (_, what, _, fj), ps in zip(FILMS, PS)][::-1]        # the latest judged render first
wp = json.load(open(f"{W}/logs/watch_pass.json")); carried, todo = [], []
def carry(im, f0, f1):
    k = key(im)
    for what, old, ps in SRC:
        if k in old and not bool((ps[max(0, f0):min(len(ps), f1 + 1)] < TH).any()):
            carried.extend(dict(e, image=im, note=f"[carried from {what}: frames unchanged] " + re.sub(r"^\[carried[^\]]*\] ", "", e.get("note", ""))) for e in old[k]); return
    todo.append(im)
for bnd in wp["boundary_list"]:
    f = int(round(bnd["t"]*FPS)); s = bnd["strip"]; p = re.sub(r"^strip_(\d+_[\d\-.]+).*$", r"pair_\1.jpg", s)
    for im in (s, p): carry(im, f - 4, f + 4)
for sh in wp["sheets"]:
    m = re.match(r"sheet_\d+_(\d+)-(\d+\.\d+)_to_(\d+)-(\d+\.\d+)", sh); t0 = int(m[1])*60 + float(m[2]); t1 = int(m[3])*60 + float(m[4]); carry(sh, int(t0*FPS), int(t1*FPS) + 2)
json.dump(dict(entries=carried), open(f"{W}/logs/findings_carried.json", "w"), indent=0); json.dump(todo, open(f"{W}/logs/judge_list.json", "w"), indent=0)
print("carried", len({e["image"] for e in carried}), "images;", "to judge fresh:", len(todo), todo)
