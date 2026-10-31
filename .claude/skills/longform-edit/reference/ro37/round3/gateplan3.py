"""RO-37 round 3: plan.json for the shared delivery gate, built only from the build's records and the delivered file. Dan is a cut-out plate
placed on a moving background, so his talking-head window is his placed rect per run, not the full frame."""
import hashlib, json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "recipe"); import r2
P = r2.P; SK = f"{P}/.claude/skills"; sys.path.insert(0, f"{SK}/_shared"); sys.path.insert(0, f"{SK}/_shared/cut")
import softblue as B, speech
MASTER = "/Volumes/Expansion/_edit_work/RO-37/round3/final/RO37_R3_MASTER.mp4"; OD = os.path.dirname(MASTER); FPS = r2.FPS; N = 14238; W_, H_ = 1920, 1080
def sec(f): return round(f / FPS, 3)
runs = []
for i in range(6):
    for r in json.load(open(f"r3/full/c{i}.build.json"))["runs"]:
        if runs and runs[-1].get("f1") == r["f0"] and all(runs[-1].get(k) == r.get(k) for k in ("kind", "shot", "item", "bg", "framing", "placement")): runs[-1]["f1"] = r["f1"]
        else: runs.append(dict(r))
assert runs[0]["f0"] == 0 and runs[-1]["f1"] == N and all(a["f1"] == b["f0"] for a, b in zip(runs, runs[1:]))
def clip_rect(rc):
    x, y, w, h = rc; x0, y0, x1, y1 = max(0, x), max(0, y), min(W_, x + w), min(H_, y + h); return [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]
pieces = []
for r in runs:
    if r["kind"] == "presenter": pieces.append(dict(a=r["f0"], b=r["f1"], lab=f"{r['framing']}-{r['placement']}", cov=False))
    elif r["kind"] == "closeup": pieces.append(dict(a=r["f0"], b=r["f1"], lab="closeup", cov=False))
    else: pieces.append(dict(a=r["f0"], b=r["f1"], lab=f"insert-{r.get('item')}", cov=True))
joins = sorted({sec(p["a"]) for p in pieces[1:]})
punch = [[sec(p["a"]), sec(p["b"]), p["lab"]] for p in pieces]; punch_cov = [p["cov"] for p in pieces]; covered = [[sec(p["a"]), sec(p["b"])] for p in pieces if p["cov"]]
MAN = json.load(open("hf3/manifest3.json"))
graphics = [dict(name=m["id"], beat=[sec(r2.fr(m["a"])), sec(min(N, r2.fr(m["b"])))], mov=m["mov"], kind=m["kind"]) for m in MAN if os.path.exists(m["mov"])]
audio_joins = json.load(open("checks/joins.json"))
thw = [dict(beat=[sec(r["f0"]), sec(r["f1"])], rect=clip_rect(r["rect"]), motion="tracking", name=f"{r['shot']}-{r['framing']}-{r['placement']}-{r['bg']}({r['bg_type']})") for r in runs if r["kind"] == "presenter"]
os.makedirs(f"{OD}/chips", exist_ok=True)
def chip_png(text, path):
    u = B.unit(W_, H_); tmp = Image.new("RGBA", (W_, 200), (0, 0, 0, 0)); x0, y0, x1, y1 = B.disclosure(tmp, text, (100, 50), u)
    tmp.crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))).save(path); return path
def grab(t):
    raw = subprocess.run([r2.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", MASTER, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H_, W_).astype(np.float32)
def locate(ref_png, t):
    import cv2
    ref = Image.open(ref_png).convert("RGBA"); flat = Image.alpha_composite(Image.new("RGBA", ref.size, (80, 80, 80, 255)), ref); r = np.asarray(flat.convert("L"), np.float32)
    res = cv2.matchTemplate(grab(t)[:300, :], r, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(res); return [int(loc[0]), int(loc[1])], round(float(mx), 3)
AI = chip_png("AI-GENERATED", f"{OD}/chips/ai.png"); chips = dict(ai=AI, real=chip_png("Real picture of me. Not AI-generated.", f"{OD}/chips/real.png"))
ai_ins = []
for c in r2.AI3:
    pos, score = locate(AI, (c["t0"] + c["t1"]) / 2); ai_ins.append(dict(name=c["id"], beat=[round(c["t0"], 3), round(c["t1"], 3)], chip=AI, pos=pos, match=score))
words = [dict(w=w["w"], t=round(w["t0"], 3), e=round(w["t1"], 3)) for w in r2.WORDS if w.get("t0") is not None]
heard, src = speech.transcribe(MASTER, "small"); transcript_words = [dict(w=w["w"].strip()) for w in heard if w["w"].strip()]
h = hashlib.sha256()
with open(MASTER, "rb") as f:
    for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
SHA = h.hexdigest()
plan = dict(target_seconds=round(N / FPS, 3), target_frames=N, joins=joins, audio_joins=audio_joins, covered=covered, punch=punch, punch_covered=punch_cov, graphics=graphics, cards=[], ai_inserts=ai_ins, real_photos=[], label_chips=chips,
            words=words, transcript_words=transcript_words, srt=f"{OD}/RO37_R3.srt", source_audio="/Volumes/Expansion/_edit_work/RO-37/round1/assembled_untreated.wav", watch_log=f"{OD}/logs/watch_pass.json", talking_head_windows=thw, evidence_contract=dict(version=2, video_sha256=SHA))
ne = f"{OD}/negative_events_scan.json"
if os.path.exists(ne):
    d = json.load(open(ne))
    if d["sha256"] == SHA: plan["negative_events_scan"] = d
json.dump(plan, open(f"{OD}/plan.json", "w"), indent=0)
print("sha", SHA[:16], "runs", len(runs), "joins", len(joins), "audio", len(audio_joins), "graphics", len(graphics), "thw", len(thw), "words", len(words), "heard", len(transcript_words), [(x["name"], x["match"]) for x in ai_ins])
