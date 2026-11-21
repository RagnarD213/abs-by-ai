"""RO-08 round 2 finish (the work-out-every-day film's finish with this film's chapters): SRT sidecar (roll words on the delivered timeline plus the words heard
only on the finished film, proofread), YouTube chapters (each on its section's first sentence), label-chip references and plan.json for the delivery gate.
usage: finish08.py MASTER.mp4   (writes next to the master)"""
import sys, os, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro08"; FPS = 30000/1001
master = os.path.abspath(sys.argv[1]); od = os.path.dirname(master); NAME = "RO08"
R = json.load(open(f"{W}/plan_resolved.json")); S = json.load(open(f"{W}/shots.json"))
BJ = json.load(open(master + ".build.json")); total_f = BJ["frames"]; total = total_f/FPS
def fr(t): return int(round(t*FPS))

# ---------------------------------------------------------------- words on the delivered timeline (medium.en)
WO = json.load(open(f"{W}/words_out.json"))
for k, w in enumerate(WO):     # a word whose start fell in a cut gap but whose end survives (heard on the delivered audio: "We" at 545.9)
    if w["t0"] is None and w["t1"] is not None and k and WO[k-1]["t1"] is not None: w["t0"] = min(w["t1"] - 0.05, max(WO[k-1]["t1"], w["t1"] - 0.25))
for k, w in enumerate(WO):     # the mirror case: a word whose end fell in a cut gap but whose start survives
    if w["t0"] is not None and w["t1"] is None:
        nx = next((x["t0"] for x in WO[k+1:] if x["t0"] is not None), w["t0"] + 0.25); w["t1"] = max(w["t0"] + 0.05, min(w["t0"] + 0.25, nx))
mw = [dict(w=w["w"], t0=w["t0"], t1=w["t1"]) for w in WO if w["t0"] is not None]
sw_ = f"{W}/round2/srt_words.json"                      # words heard on the delivered audio whose roll-word start fell in a cut gap (the first word of a take): [t0, t1, word] from the transcript of the finished film
if os.path.exists(sw_): mw += [dict(w=w, t0=a, t1=b) for a, b, w in json.load(open(sw_))]
sd_ = f"{W}/round2/srt_drop.json"                       # a word the roll transcript doubled ("day. days." on one syllable): [t0, word], heard once on the finished film
if os.path.exists(sd_):
    for t, wd in json.load(open(sd_)):
        k = [i for i, x in enumerate(mw) if abs(x["t0"] - t) < 0.06 and x["w"].strip() == wd]; assert len(k) == 1, (t, wd, k); mw.pop(k[0])
mw.sort(key=lambda x: x["t0"])
_m = []                                                  # Whisper splits "over -training", "nine-to -five": a token that opens with a hyphen belongs to the word before it
for w in mw:
    if _m and w["w"].startswith("-") and len(w["w"]) > 1: _m[-1] = dict(_m[-1], w=_m[-1]["w"] + w["w"], t1=w["t1"])
    else: _m.append(w)
mw = _m
# ---------------------------------------------------------------- SRT (sidecar only; never burned)
FIX = [(r" -(\w)", r"-\1"), (r"(\d) \.(\d)", r"\1.\2"), (r"(\d) %", r"\1%"), (r"5 '7", "5'7\""),
       (r"\bZep down\b", "Zepbound"), (r"\bClean Eats\b", "Clean Eatz"), (r"\bchat JPT\b", "ChatGPT"),
       (r"\babsbyai ?\.com\b", "AbsByAI.com"), (r"\bTry hours out\b", "Try ours out"),
       (r"\by 'all\b", "y'all"), (r" '(s|re|ll|ve|d|t|m)\b", r"'\1"), (r"\bAbs by AI\b", "Abs By AI"), (r"(?i)\bads ?by ?ai ?\.com\b", "AbsByAI.com"), (r"\bo ?'? ?clock\b", "o'clock"), (r"(\d) ?(a|p) ?\.m\.", r"\1 \2.m."), (r"\byou all guys\b", "y'all guys"), (r"\b1230\b", "12:30"), (r"\bset up\b(?= for| around| that)", "setup")]
FIX += json.load(open(f"{W}/round2/srt_fixes.json")) if os.path.exists(f"{W}/round2/srt_fixes.json") else []   # heard on the delivered audio
def fix(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return re.sub(r"(?<![ap]\.m)([.?!] )([a-z])", lambda m: m[1] + m[2].upper(), s)          # a sentence that starts inside a cue starts with a capital
cues, cur = [], []
def flush():
    global cur
    if cur:
        a0 = cur[0]["t0"]                                 # a short first word that lasts over half a second carries the pause before it (Whisper): the cue comes up with the word, not the pause
        if cur[0]["t1"] - a0 > 0.5 and len(cur[0]["w"]) <= 4: a0 = cur[0]["t1"] - 0.3
        cues.append([a0, cur[-1]["t1"], fix(" ".join(w["w"] for w in cur))]); cur = []
for w in mw:
    if cur:
        gap = w["t0"] - cur[-1]["t1"]; txt = " ".join(x["w"] for x in cur + [w])
        if gap >= 0.45 or len(txt) > 78 or w["t1"] - cur[0]["t0"] > 5.5: flush()
    cur.append(w)
    if w["w"][-1:] in ".?!" and w["w"].strip().lower() not in (".m.", "a.m.", "p.m.") and (cur[-1]["t1"] - cur[0]["t0"]) > 1.2: flush()     # "9 a.m." does not end a sentence
flush()
def wrap(s):
    if len(s) <= 45: return s
    ws = s.split(); best = None
    for k in range(1, len(ws)):
        a, b = " ".join(ws[:k]), " ".join(ws[k:]); m = max(len(a), len(b))
        if best is None or m < best[0]: best = (m, a + "\n" + b)
    return best[1]
def ts(t):
    t = max(0, t); h = int(t//3600); m = int(t % 3600//60); s = t % 60
    ms = int(round((s - int(s))*1000))
    if ms == 1000: ms = 999
    return f"{h:02d}:{m:02d}:{int(s):02d},{ms:03d}"
for i in range(len(cues)):
    if cues[i][2] and cues[i][2][0].islower() and (i == 0 or (cues[i-1][2].rstrip()[-1:] in ".?!" and not re.search(r"[ap]\.m\.$", cues[i-1][2].rstrip()))): cues[i][2] = cues[i][2][0].upper() + cues[i][2][1:]
out = []
for i, (a, b, s) in enumerate(cues):
    b = max(b, a + 0.9)
    if i + 1 < len(cues): b = min(b, cues[i+1][0] - 0.02)
    b = min(b, total - 0.05)
    out.append(f"{i+1}\n{ts(a)} --> {ts(b)}\n{wrap(s)}\n")
srt = f"{od}/{NAME}.srt"; open(srt, "w").write("\n".join(out))

# ---------------------------------------------------------------- chapters: each starts on its section's first sentence (the lower third's start phrase)
def mmss(t): return f"{int(t//60)}:{int(t % 60):02d}"
byid = {i["id"]: i for i in R}
CH = [("G03", "What Intermittent Fasting Is"), ("G07", "The Daily Fast I Do"), ("G10", "Reason 1: The Simplest Way To Eat Less"),
      ("G15", "Reason 2: What Fasting Does For Your Health"), ("G18", "Reason 3: It Saves Your Mornings"), ("G19", "Reason 4: You Get More Done"),
      ("G23", "Reason 5: Your Body Adapts"), ("G29", "How To Start: Just Skip Breakfast"), ("G33", "Your First Month"),
      ("G39", "The Next Level: Break Your Fast With A Salad"), ("G41", "Mistake 1: Binge Eating At Night"), ("G44", "Mistake 2: Eating Right Before Bed"),
      ("G46", "Mistake 3: Breaking Your Fast With Alcohol"), ("P01", "See Your Future Self With AI")]
def at(*ws, after=0.0):
    for i in range(len(mw) - len(ws) + 1):
        if mw[i]["t0"] >= after and all(mw[i+k]["w"].lower().strip(".,?!") == x for k, x in enumerate(ws)): return mw[i]["t0"]
    raise SystemExit(f"chapter anchor not found: {ws}")
CHP = {"G03": (("intermittent", "fasting", "is", "super"), 30), "G07": (("what", "i", "personally", "do"), 80), "G10": (("number", "one", "intermittent"), 148),
       "G15": (("the", "second", "reason"), 250), "G18": (("here's", "the", "third", "reason"), 300), "G19": (("another", "reason", "why"), 338),
       "G23": (("now", "here's", "the", "most"), 418), "G29": (("the", "easiest", "way"), 540), "G33": (("okay", "so", "your", "first"), 597),
       "G39": (("here's", "how", "you", "take"), 666), "G41": (("the", "first", "one", "is"), 702), "G44": (("the", "second", "mistake"), 763),
       "G46": (("here", "is", "the", "number", "one"), 790), "P01": (("on", "adsbyai"), 842)}   # every chapter starts on its section's first sentence, not where the lower third or clip comes up
ch = ["0:00 Why Fasting Is The Best Way To Get Abs"]; ts_ = []
for k, title in CH:
    t = at(*CHP[k][0], after=CHP[k][1]) if k in CHP else byid[k]["t0"]
    ts_.append(t); ch.append(f"{mmss(t + 0.25)} {title}")          # whole seconds: at most 0.25 s into the sentence, never a full second before it
assert all(y - x >= 10 for x, y in zip([0] + ts_, ts_)), "chapters under 10 s apart"
open(f"{od}/{NAME}.chapters.txt", "w").write("\n".join(ch) + "\n")

# ---------------------------------------------------------------- picture timeline: presenter segments split at full-frame items
FULL = [i for i in R if i["kind"] in ("clip", "scene") and i["t1"]]
segs = BJ["segments"]
pieces = []
for sg in segs:
    cuts = {sg["o0"], sg["o1"]} | {fr(i["t0"]) for i in FULL if sg["o0"] < fr(i["t0"]) < sg["o1"]} | {fr(i["t1"]) for i in FULL if sg["o0"] < fr(i["t1"]) < sg["o1"]}
    cuts = sorted(cuts)
    for a, b in zip(cuts, cuts[1:]):
        cov = next((i for i in FULL if fr(i["t0"]) <= a and b <= fr(i["t1"])), None)
        pieces.append(dict(a=a, b=b, lab=f"insert-{cov['id']}" if cov else f"{sg['shot']}-{sg['framing']}", cov=bool(cov)))
# merge consecutive pieces under the same insert (a cutaway spanning a presenter join is one visible shot)
merged = []
for p in pieces:
    if merged and merged[-1]["lab"] == p["lab"] and p["cov"] and merged[-1]["b"] == p["a"]: merged[-1]["b"] = p["b"]; continue
    merged.append(dict(p))
# multi-source clips are hard cuts inside the insert
subcuts = []
for i in FULL:
    if i["kind"] == "clip" and len(i.get("src", [])) > 1:
        n = fr(i["t1"]) - fr(i["t0"]); per = n // len(i["src"])
        subcuts += [fr(i["t0"]) + per*k for k in range(1, len(i["src"]))]
    if i["kind"] == "clip": subcuts += [fr(i["t0"]) + k for k in i.get("subcuts", [])]      # round 3: a cut inside a pre-cut clip (A5, a5_cut.py), in frames from the clip's first
joins = sorted(set(round(p["a"]/FPS, 3) for p in merged[1:]) | set(round(f/FPS, 3) for f in subcuts))
punch = [[round(p["a"]/FPS, 3), round(p["b"]/FPS, 3), p["lab"]] for p in merged]
punch_cov = [p["cov"] for p in merged]
covered = [[round(fr(i["t0"])/FPS, 3), round(fr(i["t1"])/FPS, 3)] for i in FULL]
cards = [[round(fr(i["t0"])/FPS, 3), round(fr(i["t1"])/FPS, 3)] for i in R if i["kind"] in ("scene", "title")]
graphics = [dict(name=i["id"], beat=[round(fr(i["t0"])/FPS, 3), round(fr(i["t1"])/FPS, 3)]) for i in R if i["kind"] in ("lt", "l3", "phone", "scene", "title")]

# ---------------------------------------------------------------- label chips: exact references from the renderer, located on the delivered frame
import softblue as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def grab(t):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", master, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1080, 1920).astype(np.float32)
def chip_png(text, path):
    u = B.unit(1920, 1080); tmp = Image.new("RGBA", (1920, 200), (0, 0, 0, 0))
    x0, y0, x1, y1 = B.disclosure(tmp, text, (100, 50), u)
    tmp.crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))).save(path); return path
def locate(ref_png, t):
    ref = Image.open(ref_png).convert("RGBA"); flat = Image.alpha_composite(Image.new("RGBA", ref.size, (80, 80, 80, 255)), ref)
    r = np.asarray(flat.convert("L"), np.float32); h, w = r.shape; g = grab(t)
    import cv2
    res = cv2.matchTemplate(g, r, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(res)
    return [int(loc[0]), int(loc[1])], round(float(mx), 3)
os.makedirs(f"{od}/chips", exist_ok=True)
def chip_u(text, path, u):
    tmp = Image.new("RGBA", (1920, 200), (0, 0, 0, 0)); x0, y0, x1, y1 = B.disclosure(tmp, text, (100, 50), u)
    tmp.crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))).save(path); return path
def crop_png(t, box, path):                             # a label that is part of an approved picture: its own pixels are the reference
    x0, y0, x1, y1 = box; g = grab(t)[y0:y1, x0:x1]; Image.fromarray(g.astype(np.uint8)).convert("RGBA").save(path); return path
ai_ins, real = [], []
for i in R:
    if not i["t1"]: continue
    a, z = fr(i["t0"])/FPS, fr(i["t1"])/FPS
    if i["id"] == "P01":                                # the approved demo: REAL chip beside the phone (frames 0..107), then the result with ITS OWN approved AI chip
        cut = (fr(i["t0"]) + 108)/FPS
        png = chip_u("Real picture of me. Not AI-generated.", f"{od}/chips/P01-real.png", 1.6); pos, score = locate(png, a + 1.5)
        real.append(dict(name="P01-before", beat=[round(a, 3), round(cut, 3)], chip=png, pos=pos, match=score))
        png = crop_png(cut + 2.0, (1052, 932, 1312, 990), f"{od}/chips/P01-ai.png"); pos, score = locate(png, (cut + z)/2)
        ai_ins.append(dict(name="P01-result", beat=[round(cut + 0.4, 3), round(z, 3)], chip=png, pos=pos, match=score))
    elif i.get("label"):
        png = chip_png(i["label"], f"{od}/chips/{i['id']}.png")
        pos, score = locate(png, (a + z)/2)
        if i["kind"] == "scene" and score < 0.9:           # the price cards' chip is drawn by HyperFrames in the browser (same text, other font rendering: 0.83 against
            ref = Image.open(png)                           # the PIL chip). Its own rendered pixels at the located place are the reference the gate tracks through the beat.
            png = crop_png((a + z)/2, (pos[0], pos[1], pos[0] + ref.width, pos[1] + ref.height), f"{od}/chips/{i['id']}.png"); pos, score = locate(png, a + 1.2)
        rec = dict(name=i["id"], beat=[round(a, 3), round(z, 3)], chip=png, pos=pos, match=score)
        (ai_ins if i["label"] == "AI-GENERATED" else real).append(rec)
chips = dict(ai=chip_png("AI-GENERATED", f"{od}/chips/ai.png"), real=chip_png("Real picture of me. Not AI-generated.", f"{od}/chips/real.png"))

plan = dict(target_seconds=round(total, 3), target_frames=total_f, ai_inserts=ai_ins, real_photos=real, label_chips=chips,
            joins=joins, covered=covered, punch=punch, punch_covered=punch_cov, graphics=graphics, cards=sorted(cards),
            words=[dict(w=w["w"], t=w["t0"], e=w["t1"]) for w in mw], srt=srt,
            source_audio=master + ".untreated.wav" if os.path.exists(master + ".untreated.wav") else None,
            source_picture=master + ".base.mp4",
            banned_source="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4", banned_times=[12.0, 18.0, 288.0], watch_log=f"{od}/logs/watch_pass.json")
fw = f"{od}/final.whisper.json"
if os.path.exists(fw):
    r = json.load(open(fw)); plan["transcript_words"] = [dict(w=w["word"].strip()) for s in r["segments"] for w in s.get("words", [])]
ne = f"{od}/negative_events_scan.json"
if os.path.exists(ne): plan["negative_events_scan"] = json.load(open(ne))
plan = {k: v for k, v in plan.items() if v is not None}
json.dump(plan, open(f"{od}/plan.json", "w"), indent=0)
print("words", len(mw), "cues", len(out), "chapters", len(ch), "joins", len(joins), "pieces", len(merged), "graphics", len(graphics))
print("labels:", [(x["name"], x["pos"], x["match"]) for x in ai_ins + real])
print("\n".join(ch))
