"""RO-07 round 2 review media (new folder round2/, nothing in round1/ is touched).
usage: r2media.py first | stills | context
first:   the rebuilt first minute (colour D, voice 4 through the shared chain, new opener), 540p review copy, poster.
stills:  a still of every changed or new item on its real graded frame (round2/stills.json).
context: moving context clips (3 s of speech either side) for the groups in CTX; voice sliced from the whole-film chain render."""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro07/recipe")
import numpy as np
from PIL import Image
import frames as F, gfx as G, build as Bd
W = "/Volumes/Extreme/_edit_work/ro07"; OUT = f"{W}/round2"; FF = Bd.FF
FM = f"{OUT}/first-minute/DRAFT - RO-07 round 2 - first minute.mp4"
R = Bd.R; BY = {r["id"]: r for r in R}
CHANGED_G = "G02 G03 G04 G07 G08 G09 G11 G13 G15 G17 G18 G19 G21 G22 G23 G24 G26 G28 G30 G32 G33 G34 G35 G36 G38 G39 G40 G41 G42 G43A G43B G44".split()
CHANGED_C = "C01 C08 C18 C20 C21 C22 C23 C24 A2".split()
NEW_C = "C30 C31 C32 C33 C34 C35 C37 C38 C42 C39".split()
CTX = {  # name: ids shown together in one moving clip
 "C08": ["C08"], "C18": ["C18"], "C20": ["C20"], "C21": ["C21"], "C22-C23-C24": ["C22", "C23", "C24"], "C31-A2": ["C31", "A2"], "G43A-G43B": ["G43A", "G43B"],
 "C30": ["C30"], "C32": ["C32"], "C33-C34": ["C33", "C34"], "C35": ["C35"], "C37": ["C37"], "C38": ["C38"], "C42": ["C42"], "C39": ["C39"],
}
def review_copy(path, poster_t=1.5):
    base = path[:-4]
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", base + " - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", str(poster_t), "-i", path, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", base + ".jpg"], check=True)
def first_end():
    lim = max([60.0] + [it["t1"] + 0.3 for it in R if it["t0"] < 60.0])
    return min(s["out_f0"] for s in Bd.S if s["out_f0"]/Bd.FPS >= lim)/Bd.FPS
def clean(out, more=()):
    for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4") + tuple(more):
        try: os.remove(out + ext)
        except OSError: pass
def stills():
    os.makedirs(f"{OUT}/stills", exist_ok=True)
    WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
    BEATS = {b["id"]: b for b in json.load(open(f"{W}/hf/beats.json"))}
    HC = Bd.HC.Compositor(json.load(open(Bd.MANIFEST)))
    speech = lambda a, b: " ".join(w["w"] for w in WO if a <= w["t0"] < b)
    rows = []
    for i in CHANGED_G + CHANGED_C + NEW_C + ["A3"]:
        it = BY[i]; t1 = it["t1"]; n = len(it.get("src", [1]))
        shots = []
        for k in range(n if it["kind"] == "clip" and not it.get("frames") else 1):       # one still per source of a multi-clip item
            if i in BEATS:
                land = [r["t"] for r in BEATS[i]["rows"] if not any(x in r["beat"] for x in ("fades", "gone", "sweep", "pulse"))]; t = min(max(land) + 0.9, t1 - 0.4)
            else: t = it["t0"] + (t1 - it["t0"]) * (k + 0.5) / n
            g = Bd.fr(t); sg = next(s for s in Bd.all_segments() if s["o0"] <= g < s["o1"])
            if it["kind"] == "clip":
                if it.get("frames"): im = Bd.ai_placeholder(it, 0, 2)
                else:
                    per = (Bd.fr(t1) - Bd.fr(it["t0"])) // n; sp = it["src"][k]; vf = "fps=30000/1001," + G.clip_vf(1.0)
                    if it.get("grade"):
                        gk = it["grade"][k] if isinstance(it["grade"], list) else it["grade"]
                        vf = vf.replace(",format=rgb24", f",format=gbrp16le,{F.GR[gk][F.LOOK]},format=rgb24")
                    off = (g - Bd.fr(it["t0"]) - per * k) / Bd.FPS
                    p = subprocess.run([FF, "-v", "error", "-ss", f"{G.src_start(sp) + max(0, off):.3f}", "-i", G.src_path(sp), "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
                    im = Image.frombytes("RGB", (1920, 1080), p)
                    if it.get("label") and not it.get("label_in_picture"): G.ai_chip(im)
                    if HC.active(g): im = Image.fromarray(HC.apply(np.asarray(im), g))
            else:
                im = F.frame_src(sg["src0"] + g - sg["o0"], sg["shot"], sg["framing"]); im = Image.fromarray(HC.apply(np.asarray(im), g))
            name = f"{i}" + (f"_{k+1}" if n > 1 and it["kind"] == "clip" and not it.get("frames") else ""); im.save(f"{OUT}/stills/{name}.jpg", quality=88); shots.append(name)
        rows.append(dict(id=i, kind=it["kind"], t0=it["t0"], t1=t1, stills=shots, before=speech(it["t0"] - 5, it["t0"]), during=speech(it["t0"], t1), after=speech(t1, t1 + 5),
                         copy={k: it[k] for k in ("topic", "point", "label") if k in it}, note=it.get("note"), pending=it.get("pending", False),
                         group="new" if i in NEW_C else "changed"))
        print("still", i, flush=True)
    json.dump(rows, open(f"{OUT}/stills.json", "w"), indent=1)
if __name__ == "__main__":
    what = sys.argv[1]
    if what == "first":
        os.makedirs(os.path.dirname(FM), exist_ok=True); e = first_end()
        Bd.render_range(0.0, e, FM); review_copy(FM, 3.0); clean(FM); print("first minute to", round(e, 2), flush=True)
    if what == "stills": stills()
    if what == "context":
        os.makedirs(f"{OUT}/context", exist_ok=True); end = Bd.S[-1]["out_f1"]/Bd.FPS; only = set(sys.argv[2:])
        for name, ids in CTX.items():
            if only and name not in only: continue
            out = f"{OUT}/context/{name}-context.mp4"
            if os.path.exists(out[:-4] + " - REVIEW 540p.mp4") and not only: continue
            a, b = max(0.0, min(BY[i]["t0"] for i in ids) - 3.0), min(end, max(BY[i]["t1"] for i in ids) + 3.0)
            Bd.render_range(a, b, out, audio="slice"); review_copy(out, 3.6); clean(out); os.remove(out)
            print("context", name, round(a, 1), round(b, 1), flush=True)
