"""RO-19 round 4: carry the independent judge's watch-pass verdicts from the round 3 film Dan reviewed (round3/film, logs/findings.json: 664 entries, 0 open)
to the round 4 film. The round 4 cut removes film frames 16350..16412 of round 3 (round4-plan/timeline_shift.json), so the two files are compared BY SOURCE
CONTENT: round 4 frame f against round 3 frame f (f < 16350) or f + 63 (f >= 16350). Every frame is compared (480x270 grey, PSNR). A strip or pair keeps its
verdict only when every frame within 4 frames of its boundary is unchanged (PSNR >= 38 dB) AND round 3 had a boundary at the matching frame (its time moved by
the same 63 frames); the carried note says so. Contact sheets are never carried: the film is 2.1 s shorter, so every sheet samples different frames.
Everything not carried is listed for a fresh, independent judge.
usage: carry19r4.py  -> round4/film/logs/psnr_vs_round3.json, findings_carried.json, judge_list.json"""
import json, subprocess, numpy as np, re
W = "/Volumes/Extreme/_edit_work/ro19"; FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001; TH = 38.0; OLD = f"{W}/round3/film"; NEW = f"{W}/round4/film"; MO = "RO-19 round 3 - full film.mp4"; MN = "RO-19 round 4 - full film.mp4"
SH = json.load(open(f"{W}/round4-plan/timeline_shift.json")); AT = SH["at_out_frame"]; CUT = -SH["frames"]
def reader(p): return subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", p, "-vf", "scale=480:270,format=gray", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
a, b = reader(f"{OLD}/{MO}"), reader(f"{NEW}/{MN}"); ps = []; N = 480*270
while True:
    if len(ps) == AT: assert len(a.stdout.read(N*CUT)) == N*CUT          # the removed stretch of round 3
    x, y = a.stdout.read(N), b.stdout.read(N)
    if len(x) < N or len(y) < N: assert len(x) == len(y), ("the two renders do not line up", len(ps)); break
    d = np.frombuffer(x, np.uint8).astype(np.float32) - np.frombuffer(y, np.uint8).astype(np.float32); mse = float((d*d).mean())
    ps.append(99.0 if mse < 1e-6 else round(10*np.log10(255*255/mse), 2))
ps = np.array(ps); assert len(ps) == SH["new_total"], len(ps); ch = np.nonzero(ps < TH)[0]; runs = []
for f in ch:
    if runs and f - runs[-1][1] <= 2: runs[-1][1] = int(f)
    else: runs.append([int(f), int(f)])
json.dump(dict(frames=len(ps), threshold=TH, mapping=f"round 4 frame f = round 3 frame f (f < {AT}) or f + {CUT}", changed_frames=len(ch),
               changed_runs=[[r[0], r[1], round(r[0]/FPS, 3), round((r[1]+1)/FPS, 3), float(ps[r[0]:r[1]+1].min())] for r in runs],
               min_psnr_unchanged=float(ps[ps >= TH].min()), median=float(np.median(ps))), open(f"{NEW}/logs/psnr_vs_round3.json", "w"), indent=1)
print(len(ps), "frames;", len(ch), "changed in", len(runs), "runs (round 4 time):", [(round(r[0]/FPS, 2), round((r[1]+1)/FPS, 2)) for r in runs], "| lowest PSNR among the unchanged:", ps[ps >= TH].min())
old = {}
for e in json.load(open(f"{OLD}/logs/findings.json"))["entries"]: old.setdefault(e["image"], []).append(e)
def pair_of(s): return re.sub(r"^strip_(\d+_[\d\-.]+).*$", r"pair_\1.jpg", s)
wo = json.load(open(f"{OLD}/logs/watch_pass.json")); wp = json.load(open(f"{NEW}/logs/watch_pass.json"))
def to_new(fo): return fo if fo <= AT else (fo - CUT if fo >= AT + CUT else None)
oldb = {}
for x in wo["boundary_list"]:
    fn = to_new(int(round(x["t"]*FPS)))
    if fn is not None: oldb[fn] = x["strip"]
carried, todo = [], []
def changed(f0, f1): return bool((ps[max(0, f0):min(len(ps), f1 + 1)] < TH).any())
def tag(n, moved):
    n = re.sub(r"^\[carried[^\]]*\]\s*", "", n)
    return "[carried from the round 3 film Dan reviewed: the frames at this cut are unchanged" + (f"; it is {CUT} frames (2.10 s) earlier than in round 3, so times inside this note are round 3 times" if moved else "") + "] " + n
for bnd in wp["boundary_list"]:
    f = int(round(bnd["t"]*FPS)); s = bnd["strip"]; so = oldb.get(f)
    for im, imo in ((s, so), (pair_of(s), pair_of(so) if so else None)):
        if imo and imo in old and not changed(f - 4, f + 4) and not (AT - 4 <= f <= AT + 4):
            carried += [dict(e, image=im, t=(round(e["t"] - CUT/FPS, 2) if isinstance(e.get("t"), (int, float)) and f > AT else e.get("t")), note=tag(e.get("note", ""), f > AT)) for e in old[imo]]
        else: todo.append(im)
todo += list(wp["sheets"])
assert not [e for e in carried if e["verdict"] == "defect"], "a defect verdict was carried: its frames must have changed"
json.dump(dict(entries=carried), open(f"{NEW}/logs/findings_carried.json", "w"), indent=0); json.dump(todo, open(f"{NEW}/logs/judge_list.json", "w"), indent=0)
print("boundaries: round 3", len(wo["boundary_list"]), "round 4", len(wp["boundary_list"]), "| carried", len({e["image"] for e in carried}), "images | to judge fresh:", len(todo), [t for t in todo if not t.startswith("sheet_")])
