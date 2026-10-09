"""RO-06 builder (from the RO-10 recipe, made multi-roll). render_range(a, b, out): graded presenter (per-roll grade, three
fixed sizes solved for the whole film, round 2: tight by default; W under the side list) + every plan item, hard cuts, shared voice chain.
usage: build.py range <t0> <t1> <out.mp4> | build.py voice <t0> <t1> <out.mp4> | build.py segs [seconds to list]"""
import sys, os, json, subprocess, hashlib, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import frames as F, gfx as G, softblue as B
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
import composite as HC
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001; FPSS = "30000/1001"; FF = F.FF; SR = 48000
S = json.load(open(f"{W}/shots.json")); R = json.load(open(f"{W}/plan_resolved.json"))
MANIFEST = f"{W}/hf/manifest.json"
VC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
def fr(t): return int(round(t*FPS))
def run(c): subprocess.run(c, check=True)
def hf_item(it): return it["kind"] in ("lt", "l3") or (it["kind"] == "scene" and it.get("scene") == "fact")
FULL = ("scene", "clip")
OVERRIDE = {"hook.0r0": "X", "hook.0r1": "W",          # round 2 (Dan): open tight, B-roll, then the wide that shows the equipment
            "hook.0r2+c": "T", "exc1.0": "X", "exc2.0r0": "T", "exc2.0r1": "X",   # first minute: tight on the punch lines, medium between
            "exc3.0r0": "W",                              # "the stuff in front of me right here": the wide, motivated
            "exc3.0r1b": "T"}                             # he leans and points at the equipment ("I still recommend this stuff"): too big a move for the tight
# round 5: the approved first minute is pinned to its round 4 sizes (the solve is global: a change later in the film must not move it)
OVERRIDE.update({"hook.0r0+c": "X", "hook.0r1b": "X", "hook.0r2": "X", "exc2.0r0+c": "X", "exc2.0r0+c2": "X", "exc2.0r1+c": "X", "exc2.0r1+c2": "X", "exc3.0r1": "X"})
# round 5 leans scan (leanscan.py): he bends to the equipment inside these shots, which the tight size cannot hold. Medium, not wide: a lower third is up on three of them
OVERRIDE.update({"exc3.0r3": "T", "mat.0r2": "T", "rope.1r0": "T", "wheel.0r0": "T",
                 "towel.0r0": "T", "towel.0r0b": "W"})   # he bends to the ground for the towel: split at "mention | even though" (split_shot.py), the camera frame for the reach (no lower third up yet)
# round 5: db3.0r10 to r12 held one medium crop for 24.4 s (over the 22 s rule); r12 split at "as you go | You're going to progress" (split_shot.py), tight then medium
OVERRIDE.update({"db3.0r12": "X", "db3.0r12b": "T"})
PINCROP = {g["key"]: tuple(g["crop"]) for g in json.load(open(f"{W}/round4/first-minute/DRAFT - RO-06 round 4 - first minute.mp4.build.json"))["segments"]}
# round 5: under the side list L01 he points toward the card (5:21) and came within 57 px of it (the checker's minimum is 60). A 2 % punch-in anchored
# top left moves him 18 px further from the card; the top row stays the camera's own (hair), 22 rows come off the bottom.
# round 5: the retimed lower thirds G05 and G14 no longer cover enough of these shots to count in the solve, which then flipped them to the wide
# (strip on the equipment at his feet) or the tight (he bends out of it). Held at the medium they had in the first full render.
OVERRIDE.update({"mat.0r0": "T", "kb1.0r1": "T", "kb1.0r2": "T"})
# round 5 (both reviews): the operator re-aimed inside these two shots. mb2.0r0 goes to the medium so its crop has room to take the tilt out (stab.py);
# mb1.0r5 goes to the camera frame because he lifts the medicine ball overhead and the tight size cut the ball and both hands off the top.
OVERRIDE.update({"mb2.0r0": "T", "mb1.0r5": "W"})
# round 5, third render: every shot keeps the size and crop it had in the second render (the one both reviews and the three watch judges looked at). Adding
# cutaways and moving lower thirds re-ran the whole-film solve and flipped 17 shots; only the two changes above are wanted. A new piece after a cutaway takes its shot's size.
# round 6: every shot keeps the size and crop of the round 5 film Dan reviewed (its build.json), except the two 9:24 shots he asked to have wider and higher.
_R2 = {g["key"]: g for g in json.load(open(f"{W}/round5/RO-06 round 5 - full film.mp4.build.json"))["segments"]}
MB2 = ("mb2.0r0", "mb2.0r1")                              # round 6 (Dan, 9:24): one wider, higher crop on a taller canvas (mb2_fix.py); the two shots are one take, so one size and no cut
BREAK = ("mb2.0r2",)                                      # the take runs on after the toe-touch cutaway at its round 5 crop: not part of the widened run
for _k, _g in _R2.items():
    if _k.split("+")[0] not in MB2: OVERRIDE[_k] = _g["framing"]
OVERRIDE.update({"mb2.0r0": "T", "mb2.0r1": "T"})
class _Base(dict):
    def __missing__(self, k): raise KeyError(k)
    def __contains__(self, k): return dict.__contains__(self, k) or ("+c" in k and dict.__contains__(self, k.split("+")[0]))
    def __getitem__(self, k): return dict.__getitem__(self, k) if dict.__contains__(self, k) else dict.__getitem__(self, k.split("+")[0])
OVERRIDE = _Base(OVERRIDE)
STAB = json.load(open(f"{W}/round5/stab.json")) if os.path.exists(f"{W}/round5/stab.json") and not os.environ.get("RO06_NOSTAB") else {}
STAB.pop("mb2.0r0", None)                                # round 6: mb2_fix.py applies this shot's offsets itself, on the taller canvas
import mb2_fix
CROPFIX = {"mb2.0r0": mb2_fix.CROP, "mb2.0r1": mb2_fix.CROP, "tot2.0r0": (1880, 1058, 0, 0), "tot2.0r1": (1880, 1058, 0, 0),
           "mb1.0r6": (984, 554, 428, 0), "mb1.0r7": (984, 554, 428, 0)}     # the crop these two had with mb1.0r5 in their run (top row = the camera's: his hair is at the edge on this roll)
HOLD = 22.0                                              # one size never holds longer than this with nothing else changing
CLOSE = ("C1580", "C1581")                               # the camera frame is already tighter than Dan's tight shot
_SEGS = None
def cont(p, s): return p["src_f1"] == s["src_f0"] and p["out_f1"] == s["out_f0"]      # a reframe cut: the same take runs on
def klass(shot):
    v = F.SF[shot["id"]]
    return "wide" if v["zt"] == 1.5 else ("close" if shot["roll"] in CLOSE else "medium")
def options(sg):
    """{size: own cost}. Wide rolls: X tight (the default), T medium, W the camera frame (the equipment at his feet: only
    when asked for, on an active shot, or under the side list). Medium rolls: their 1.3x T is already hair to shorts.
    Close rolls: the camera frame."""
    if sg["key"] in OVERRIDE: return {OVERRIDE[sg["key"]]: 0.0}
    if sg["forced"]: return {"W": 0.0}
    k, act = sg["klass"], sg["active"]
    if k == "wide":
        o = {"T": 1.0, "W": 0.0} if act else {"X": 0.0, "T": 0.5, "W": 1.5}
        if sg["lt"]: o["W"] += 3.0                                    # in W the strip sits on the equipment at his feet
        return o
    if k == "medium": return {"W": 0.0, "T": 3.0} if act else {"T": 0.0, "W": 0.8}
    return {"W": 0.0, "T": 3.0} if act else {"W": 0.0, "T": 0.8}
def size(sg, o): return 1920.0/F.crop_of(sg["shot"], o)[0]*F.SF[sg["shot"]]["xw_med"]     # how big he is on screen
def same_take(a, b): return a["shot"] == b["shot"] or cont(SBY[a["shot"]], SBY[b["shot"]])
def pair(a, qa, b, qb):
    if b["covered_in"]: return 0.0
    r = size(a, qa)/size(b, qb); near = 1/1.2 < r < 1.2
    if same_take(a, b): return 0.0 if qa == qb else (10.0 if near else 0.3)        # no cut needed inside one take
    return 10.0 if near else 0.0                                                    # a real join needs a real size change
SBY = {s["id"]: s for s in S}
def all_segments():
    """One picture segment per shot (a shot is split where a full-screen clip or card starts inside it, so the picture may
    come back at another size), framing solved for the whole film: dynamic programming over the sizes each shot allows,
    then no size holds over HOLD seconds, then every run of one take at one size shares ONE crop (no shift at a non-cut)."""
    global _SEGS
    if _SEGS is not None: return _SEGS
    cards = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] == "l3"]
    full = sorted((fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in FULL)
    lts = [(fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] == "lt"]
    segs = []
    for s in S:
        edges = [s["out_f0"]] + [a for a, b in full if s["out_f0"] < a < s["out_f1"]] + [s["out_f1"]]
        for j, (o0, o1) in enumerate(zip(edges, edges[1:])):
            n = o1-o0; under = sum(max(0, min(b, o1)-max(a, o0)) for a, b in lts)
            hid = sum(max(0, min(b, o1)-max(a, o0)) for a, b in full)
            segs.append(dict(o0=o0, o1=o1, src0=s["src_f0"] + o0 - s["out_f0"], shot=s["id"], roll=s["roll"],
                             key=s["id"] + ("" if j == 0 else "+c" + (str(j) if j > 1 else "")), klass=klass(s), active=F.SF[s["id"]]["active"],
                             forced=any(a < o1 and o0 < b for a, b in cards), lt=under > 0.45*max(1, n-hid), vis=max(0, n-hid),
                             covered_in=any(a <= o0 < b for a, b in full)))
    cost = [dict(options(segs[0]))]; back = [{}]
    for k in range(1, len(segs)):
        c, bk = {}, {}
        for o, own in options(segs[k]).items():
            best = min((cost[-1][q] + pair(segs[k-1], q, segs[k], o), q) for q in cost[-1]); c[o] = best[0] + own; bk[o] = best[1]
        cost.append(c); back.append(bk)
    o = min(cost[-1], key=cost[-1].get)
    for k in range(len(segs)-1, -1, -1):
        segs[k]["framing"] = o
        if k: o = back[k][o]
    def runs():
        out, cur = [], [0]
        for k in range(1, len(segs)):
            if same_take(segs[k-1], segs[k]) and segs[k-1]["framing"] == segs[k]["framing"] and segs[k]["key"] not in BREAK: cur.append(k)
            else: out.append(cur); cur = [k]
        return out + [cur]
    def longest(run):                                                 # the longest stretch of this run on screen with no cover
        a, b = segs[run[0]]["o0"], segs[run[-1]]["o1"]; best = (0, a, a); t = a
        for x, y in full + [(b, b)]:
            if y <= a or x > b: continue
            if x - t > best[0]: best = (x - t, t, x)
            t = max(t, y)
        return best
    for _ in range(200):                                              # the hold rule: flip a middle shot of a long run
        done = True
        for run in runs():
            n, x, y = longest(run)
            if n/FPS <= HOLD or len(run) < 2: continue
            mid = (x + y)/2; alt = {"X": "T", "T": "X"} if segs[run[0]]["klass"] == "wide" else {"T": "W", "W": "T"}
            for k in sorted(run, key=lambda k: abs((segs[k]["o0"] + segs[k]["o1"])/2 - mid)):
                q = alt.get(segs[k]["framing"]); sg = segs[k]
                if q is None or q not in options(sg) or options(sg)[q] >= 3 or sg["o1"] <= x or sg["o0"] >= y: continue
                if k and pair(segs[k-1], segs[k-1]["framing"], sg, q) >= 10: continue
                if k < len(segs)-1 and pair(sg, q, segs[k+1], segs[k+1]["framing"]) >= 10: continue
                sg["framing"] = q; done = False; break
        if done: break
    for run in runs():                                                # one crop per run
        seen = [k for k in run if segs[k]["vis"] > 0] or run        # a piece wholly under a full-screen clip never moves the crop of the pieces you see (round 3)
        cs = [F.crop_of(segs[k]["shot"], segs[k]["framing"]) for k in seen]; w = [segs[k]["vis"] or segs[k]["o1"] - segs[k]["o0"] for k in seen]
        cw, ch = max(cs)[:2]; x0 = sum(c[2]*n for c, n in zip(cs, w))/sum(w); y0 = min(c[3] for c in cs)
        crop = (cw, ch, int(min(max(0, round(x0/2)*2), 1920-cw)), int(min(y0, 1080-ch)))
        pin = [PINCROP[segs[k]["key"]] for k in run if segs[k]["key"] in PINCROP]     # round 5: a run that reaches into the approved first minute keeps that minute's crop
        if pin: crop = pin[0]; cw = crop[0]
        r2 = [tuple(_R2[segs[k]["key"].split("+")[0] if segs[k]["key"] not in _R2 else segs[k]["key"]]["crop"]) for k in run
              if (segs[k]["key"] in _R2 or segs[k]["key"].split("+")[0] in _R2) and _R2[segs[k]["key"] if segs[k]["key"] in _R2 else segs[k]["key"].split("+")[0]]["framing"] == segs[k]["framing"]]
        if r2 and not pin: crop = r2[0]; cw = crop[0]
        fix = [CROPFIX[segs[k]["key"].split("+")[0] if segs[k]["shot"] in MB2 else segs[k]["key"]] for k in run if segs[k]["key"] in CROPFIX or segs[k]["shot"] in MB2]
        if fix: crop = fix[0]; cw = crop[0]
        for k in run: segs[k]["crop"] = crop; segs[k]["zoom"] = round(1920/cw, 3)
    _SEGS = segs; return segs
def jumps():
    sg = all_segments()
    return [(round(b["o0"]/FPS, 2), a["key"], b["key"], a["framing"], b["framing"]) for a, b in zip(sg, sg[1:])
            if not same_take(a, b) and pair(a, a["framing"], b, b["framing"]) >= 10]
def holds():
    sg = all_segments(); full = sorted((fr(it["t0"]), fr(it["t1"])) for it in R if it["kind"] in FULL); out = []; a = 0
    cuts = [s["o0"] for p, s in zip(sg, sg[1:]) if p["crop"] != s["crop"] or not same_take(p, s)] + [x for xy in full for x in xy] + [sg[-1]["o1"]]
    for c in sorted(set(cuts)):
        if not any(x <= a < y for x, y in full): out.append((round((c-a)/FPS, 1), round(a/FPS, 2)))
        a = c
    return sorted(out, reverse=True)[:8]
def segments(f0, f1):
    out = []
    for s in all_segments():
        a, b = max(s["o0"], f0), min(s["o1"], f1)
        if a < b: out.append(dict(s, o0=a, o1=b, src0=s["src0"] + a - s["o0"]))
    return out
SHARP = "unsharp=5:5:{a}:5:5:0.0"
def sharpen(zoom):                                       # a punch-in on a 1080p roll is an enlargement: restore edge contrast in step with it
    return None if zoom < 1.1 else SHARP.format(a=0.5 if zoom < 1.7 else TIGHT_SHARP)
TIGHT_SHARP = 0.9
def render_seg_stab(sg, offs):
    """A shot the operator re-aimed in: every source frame is cropped at crop + that frame's measured background travel (sub-pixel, bilinear), so the
    background holds still; then the usual scale, grade and sharpen."""
    import cv2
    cw, ch, cx, cy = sg["crop"]; roll, lf = F.roll_of(sg["src0"]); n = sg["o1"] - sg["o0"]; offs = offs[sg["src0"] - sg["stab_src0"]:][:n]; assert len(offs) == n
    vf = F.vf(roll, (cw, ch, 0, 0)).replace("format=rgb24", "format=yuv420p").replace(f"crop={cw}:{ch}:0:0,", "")
    if sharpen(sg["zoom"]): vf = vf.replace(",format=yuv420p", f",{sharpen(sg['zoom'])},format=yuv420p")
    key = hashlib.sha1(json.dumps([sg["src0"], n, vf, list(sg["crop"]), offs]).encode()).hexdigest()[:12]; out = f"{W}/cache/seg_{sg['src0']}_{key}.mp4"
    if os.path.exists(out): return out
    ts = lf/FPS; ss_in = max(0, ts-1)
    dec = subprocess.Popen([FF, "-v", "error", "-ss", f"{ss_in:.4f}", "-i", F.ROLLS[roll]["path"], "-ss", f"{max(0, ts-ss_in-0.4/FPS):.4f}", "-frames:v", str(n),
                            "-pix_fmt", "yuv444p", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv444p", "-s", f"{cw}x{ch}", "-framerate", FPSS, "-color_range", "tv", "-colorspace", "bt709", "-i", "-",
                            "-vf", vf, "-an", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        a = np.frombuffer(dec.stdout.read(1920*1080*3), np.uint8).reshape(3, 1080, 1920); dx, dy = offs[i]
        x, y = cx + dx, cy + dy; assert -0.5 <= x and x + cw <= 1920.5 and -0.5 <= y and y + ch <= 1080.5, (sg["key"], i, x, y)
        Mx = np.float32([[1, 0, -x], [0, 1, -y]])
        enc.stdin.write(np.stack([cv2.warpAffine(a[c], Mx, (cw, ch), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) for c in range(3)]).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait(); os.rename(out + ".tmp.mp4", out); return out
def render_seg(sg):
    if sg["shot"] in MB2: return mb2_fix.render(sg, sharpen(sg["zoom"]))
    if sg["key"].split("+")[0] in STAB or sg["key"] in STAB:
        k = sg["key"] if sg["key"] in STAB else sg["key"].split("+")[0]; base = next(s for s in all_segments() if s["key"] == k)
        return render_seg_stab(dict(sg, stab_src0=base["src0"]), STAB[k])
    crop = sg["crop"]; roll, lf = F.roll_of(sg["src0"])
    vf = F.vf(roll, crop).replace("format=rgb24", "format=yuv420p")
    if sharpen(sg["zoom"]): vf = vf.replace(",format=yuv420p", f",{sharpen(sg['zoom'])},format=yuv420p")
    key = hashlib.sha1(json.dumps([sg["src0"], sg["o1"]-sg["o0"], vf]).encode()).hexdigest()[:12]
    out = f"{W}/cache/seg_{sg['src0']}_{key}.mp4"
    if not os.path.exists(out):
        os.makedirs(f"{W}/cache", exist_ok=True)
        ts = lf/FPS; ss_in = max(0, ts-1)
        run([FF, "-v", "error", "-y", "-ss", f"{ss_in:.4f}", "-i", F.ROLLS[roll]["path"], "-ss", f"{max(0, ts-ss_in-0.4/FPS):.4f}", "-frames:v", str(sg["o1"]-sg["o0"]),
             "-vf", vf, "-an", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast",
             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".tmp.mp4"])
        os.rename(out + ".tmp.mp4", out)
    return out
def ai_placeholder(it, i, n):
    """A new AI clip whose motion is not generated yet: its approved-for-review START frame for the first half of the slot,
    its END frame for the second half, labelled (the 2026-09-28 preview convention). Never a finished clip."""
    k = 0 if i < n/2 else 1
    im = Image.open(it["frames"][k]).convert("RGB").resize((1920, 1080), Image.LANCZOS)
    B.disclosure(im, f"{it['id']} PLACEHOLDER: {('START', 'END')[k]} frame, motion not generated yet", (960, 990), 2.0, anchor="mt")
    return im
def clip_frames(it):
    n = fr(it["t1"]) - fr(it["t0"])
    if it.get("frames"):
        for i in range(n): yield ai_placeholder(it, i, n)
        return
    s = it["src"]; per = n // len(s)
    for k, sp in enumerate(s):
        m = per if k < len(s)-1 else n - per*(len(s)-1)
        path = G.src_path(sp); st = G.src_start(sp)
        dur = float(subprocess.run([FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
        assert dur - st >= m/FPS - 0.02, f"{it['id']}: {os.path.basename(path)} too short ({dur-st:.2f}s for {m/FPS:.2f}s) -- never hold a clip"
        vf = "fps=30000/1001," + G.clip_vf(1.0)
        if it.get("grade"): vf = vf.replace(",format=rgb24", f",format=gbrp,{F.GR[it['grade']][F.LOOK]},format=rgb24")
        p = subprocess.Popen([FF, "-v", "error", "-ss", f"{st:.3f}", "-i", path, "-frames:v", str(m), "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        for _ in range(m):
            b = p.stdout.read(1920*1080*3); assert len(b) == 1920*1080*3, f"{it['id']} short read"
            yield Image.frombytes("RGB", (1920, 1080), b)
        p.stdout.close(); p.wait()
def voice_shots():
    """Shots as the voice track is cut. A picture-only split (split_shot.py) is merged back, so adding a reframe cut never
    moves a sample of approved audio (each shot is placed by its own rounded sample position)."""
    out = []
    for s in S:
        if s.get("split_of") and out and cont(out[-1], s): out[-1] = dict(out[-1], src_f1=s["src_f1"], out_f1=s["out_f1"])
        else: out.append(dict(s))
    return out
def render_range(a, b, out, audio=True, picture=True):
    HCOMP = HC.Compositor(json.load(open(MANIFEST)))
    f0, f1 = fr(a), fr(b); segs = segments(f0, f1)
    if picture: render_picture(a, b, out, f0, f1, segs, HCOMP)
    items = [it for it in R if it["t0"] < b and it["t1"] > a]
    if not audio: os.replace(out + ".v.mp4", out); return
    render_voice(out, f0, f1)
    json.dump(dict(range=[a, b], frames=f1-f0, segments=segs, items=[i["id"] for i in items]), open(out + ".build.json", "w"), indent=1)
    print("built", out, f1-f0, "frames", flush=True)
def render_picture(a, b, out, f0, f1, segs, HCOMP):
    base = out + ".base.mp4"; txt = base + ".txt"
    open(txt, "w").write("".join(f"file '{render_seg(s)}'\n" for s in segs))
    run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", base])
    items = [it for it in R if it["t0"] < b and it["t1"] > a]
    readers = {it["id"]: clip_frames(it) for it in items if it["kind"] == "clip"}
    dec = subprocess.Popen([FF, "-v", "error", "-i", base, "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", FPSS, "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out + ".v.mp4"], stdin=subprocess.PIPE)
    for g in range(f0, f1):
        buf = dec.stdout.read(1920*1080*3); assert len(buf) == 1920*1080*3, g
        im = Image.frombytes("RGB", (1920, 1080), buf)
        for it in items:
            if it["kind"] == "clip" and fr(it["t0"]) <= g < fr(it["t1"]):
                im = next(readers[it["id"]])
                if it.get("label") and not it.get("label_in_picture"): G.ai_chip(im)     # P01 / P02 carry their label inside the clip (phone_demo.py)
        if HCOMP.active(g): im = Image.fromarray(HCOMP.apply(np.asarray(im), g))
        enc.stdin.write(im.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
def render_voice(out, f0, f1):
    S = voice_shots()                                  # round 6: RO06_LAV = lav.round6.wav, lav.wav with the blown-out 3.6 s repaired (audiofix6.py)
    wv = wave.open(os.environ.get("RO06_LAV", f"{W}/lav.wav")); wv.setpos(0); L = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    N = int(round((f1-f0)/FPS*SR)); v = np.zeros(N, np.float32); r = int(0.010*SR)
    for k, s in enumerate(S):
        o0, o1 = max(s["out_f0"], f0), min(s["out_f1"], f1)
        if o0 >= o1: continue
        si = int(round((s["src_f0"] + o0 - s["out_f0"])/FPS*SR)); n = int(round((o1-o0)/FPS*SR)); at = int(round((o0-f0)/FPS*SR))
        x = L[si:si+n].copy()
        cin = k > 0 and cont(S[k-1], s); cout = k < len(S)-1 and cont(s, S[k+1])
        if o0 == s["out_f0"] and not cin: x[:r] *= np.linspace(0, 1, r)
        if o1 == s["out_f1"] and not cout: x[-r:] *= np.linspace(1, 0, r)
        e = min(N, at+len(x)); v[at:e] += x[:e-at]
    raw = out + ".untreated.wav"; o = wave.open(raw, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(v, -1, 1)*32767).astype("<i2").tobytes()); o.close()
    eq = ["--eq", json.load(open(f"{W}/FIT.voice_chain.json"))["eq"]] if os.path.exists(f"{W}/FIT.voice_chain.json") else []
    bed = []
    if os.environ.get("RO06_BED"):                       # round 5 (Dan: "add a quiet bed"): bed.py's looped Pixabay bed, ducked by the chain; level measured on the gate's floor row
        bed = ["--bed", os.environ["RO06_BED"], "--bed-db", os.environ.get("RO06_BED_DB", "-20")]
    run(["python3", VC, "--in", raw, "--video", out + ".v.mp4", "--frame-lock", out + ".v.mp4", "--out", out, "--work", out + ".work"] + eq + bed)
if __name__ == "__main__":
    if sys.argv[1] == "segs":
        sg = all_segments(); tot = sum(s["o1"]-s["o0"] for s in sg)
        print(len(sg), "segments;", {o: f"{sum(s['framing'] == o for s in sg)} shots, {100*sum(s['o1']-s['o0'] for s in sg if s['framing'] == o)/tot:.0f} % of the time" for o in "XTW"})
        print("jumps:", jumps()); print("longest holds (s, at):", holds())
        for s in sg:
            if s["o0"]/FPS < float(sys.argv[2] if len(sys.argv) > 2 else 80): print(f"  {s['o0']/FPS:7.2f} {s['key']:14s} {s['roll']} {s['klass']:6s} {s['framing']} {s['crop']} x{s['zoom']}{' lt' if s['lt'] else ''}{' covered' if s['covered_in'] else ''}{' ACTIVE' if s['active'] else ''}")
    if sys.argv[1] == "range": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
    if sys.argv[1] == "voice": render_range(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], picture=False)   # picture kept, voice track rebuilt
