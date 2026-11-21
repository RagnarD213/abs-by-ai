"""RO-19 round 3 finish (from RO-07's finish_r3): SRT sidecar (medium.en words on the delivered timeline, proofread), YouTube chapters (each on its
section's first sentence, found by its words), label-chip references (our AI chip, the photo scenes' own disclosure, the approved demo's chips, the in-phone chip of
the app tour), and plan.json for the delivery gate. usage: finish19r3.py MASTER.mp4   (writes next to the master)"""
import sys, os, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro19"; FPS = 30000/1001
master = os.path.abspath(sys.argv[1]); od = os.path.dirname(master); NAME = "RO19"
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
mw.sort(key=lambda x: x["t0"])
# Proofread against the delivered audio (a second transcript of the master, final.whisper.json, and the roll): word-for-word replacements, same number of words.
SEQ = [("tan and And here", "tan, _ and here"), ("for ads by AI.", "for Abs By AI."), ("go to chatgpt,", "go to ChatGPT,"), ("do it? my AI", "do it? My AI"), ("shoot. find me", "shoot. Find me"),
       ("dudes and thongs", "dudes in thongs"), ("because From what", "because from what"), ("face clubs.", "face scrubs."), ("won't is noticeable.", "won't be noticeable."),
       ("life I'm the water", "life I'm in-the water"), ("Brian Johnson's", "Bryan Johnson's"), ("in the sun. sun exposure", "in the sun. Sun exposure"),
       ("natural tank and look healthy it is not healthy it is sun damage and is aging you Not only the sun damage give you cancer and age your body It also makes you look older if you look",
        "natural tan can look healthy, it is not healthy. It is sun damage and is aging you. Not only the sun damage give you cancer and age your body, it also makes you look older. If you look"),
       ("Florida say who have lived their entire life in the Sun They look", "Florida, say, who have lived their entire life in the sun, they look"), ("50s and 60s Their skin", "50s and 60s. Their skin"),
       ("you were placed at with", "you replaced that _ with"), ("strapped for fonts,", "strapped for funds,"), ("GOP1,", "GLP-1,"), ("a Sprite tan.", "a spray tan."),
       ("a week. a little sooner", "a week, a little sooner"), ("near as defined Now there", "near as defined. Now there"), ("photographer did But the main reason why is that I was too pale I wasn't", "photographer did. But the main reason why is that I was too pale. I wasn't"),
       ("super pale But I was", "super pale, but I was"), ("bodybuilders They're spray", "bodybuilders, they're spray"), ("huge extent they're going", "huge extent, they're going"), ("oh I don't", "oh, I don't"), ("Researchers coming out", "Research is-coming out"), ("damage, And that's", "damage, and that's"), ("cancer. in my opinion,", "cancer. In my opinion,")]
def _n(x): return re.sub(r"[^a-z0-9']", "", x.lower())
for old, new in SEQ:
    o, nw = old.split(), new.split(); assert len(o) == len(nw), (old, new)
    hits = [k for k in range(len(mw) - len(o) + 1) if [x["w"] for x in mw[k:k + len(o)]] == o]
    assert len(hits) == 1, ("caption fix not found exactly once", old, len(hits))
    for x, v in zip(mw[hits[0]:], nw): x["w"] = v
for x in mw: x["w"] = x["w"].replace("in-the", "in the").replace("is-coming", "is coming")
mw = [x for x in mw if x["w"] != "_"]     # a doubled or misheard extra word
# ---------------------------------------------------------------- SRT (sidecar only; never burned)
FIX = [(r" -(\w)", r"-\1"), (r"(\d) \.(\d)", r"\1.\2"), (r"(\d) %", r"\1%"), (r"5 '7", "5'7\""),
       (r"\bZep down\b", "Zepbound"), (r"\bClean Eats\b", "Clean Eatz"), (r"\bchat JPT\b", "ChatGPT"),
       (r"\babsbyai ?\.com\b", "AbsByAI.com"), (r"\bTry hours out\b", "Try ours out"),
       (r"\by 'all\b", "y'all"), (r" '(s|re|ll|ve|d|t|m)\b", r"'\1"), (r"\bAbs by AI\b", "Abs By AI"), (r"\bset up\b(?= for| around| that)", "setup")]
FIX += json.load(open(f"{W}/round3/srt_fixes.json")) if os.path.exists(f"{W}/round3/srt_fixes.json") else []   # heard on the delivered audio
def fix(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return s
cues, cur = [], []
def flush():
    global cur
    if cur: cues.append([cur[0]["t0"], cur[-1]["t1"], fix(" ".join(w["w"] for w in cur))]); cur = []
for w in mw:
    if cur:
        gap = w["t0"] - cur[-1]["t1"]; txt = " ".join(x["w"] for x in cur + [w])
        if gap >= 0.45 or len(txt) > 84 or w["t1"] - cur[0]["t0"] > 5.5: flush()
    cur.append(w)
    if w["w"][-1:] in ".?!" and (cur[-1]["t1"] - cur[0]["t0"]) > 1.2: flush()
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
    if cues[i][2] and cues[i][2][0].islower() and (i == 0 or cues[i-1][2].rstrip()[-1:] in ".?!"): cues[i][2] = cues[i][2][0].upper() + cues[i][2][1:]
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
def norm(x): return re.sub(r"[^a-z0-9]", "", x.lower())
def at(phrase):
    toks = [norm(x) for x in phrase.split()]
    hits = [mw[k]["t0"] for k in range(len(mw) - len(toks) + 1) if [norm(x["w"]) for x in mw[k:k + len(toks)]] == toks]
    assert len(hits) == 1, (phrase, hits); return hits[0]
# the round 1 page's chapter titles; its times sat a few seconds into each section, so each one is re-found on the section's first sentence
CH = [("if you guys want to look good in photos", "Why A Tan Makes You Look More Defined"), ("so let me tell you about my first spray tanning", "How I Found A Studio"),
      ("So for me, I bought a premium", "What It Costs"), ("there are other options that you can do", "Tanning At Home"),
      ("so if you do do professional", "What The Appointment Is Like"), ("so let's talk about the drying time", "Drying Time And Aftercare"),
      ("so let's talk about that first shower", "The First Shower"), ("so let's talk about how long your spray tan", "How Long It Lasts"),
      ("Now here is another downside", "The Downside: Water"), ("so on screen right now I'm going to show", "My Before And After Photos"),
      ("Let's talk about the pros and cons", "The Biggest Pro: No Sun Damage"), ("Now here's another reason why you might", "If You're Very Pale"),
      ("so let's talk about the cons of spray", "The Cons"), ("So who should be spray tanning", "Who Should Get A Spray Tan"),
      ("if you're at that level where you can only", "Get The Most Out Of It: The Photo Shoot"), ("so that's today's video", "Your Next Step")]
ch = ["0:00 My First Spray Tan: Before And After"]; ts_ = []
for ph, title in CH:
    t = at(ph); t = max((w["t1"] for w in mw if w["t1"] <= t and w["w"][-1:] in ".?!"), default=0.0) + 0.05 if True else t      # back to the end of the sentence before (takes in "Alright," / "Okay," / "Now,")
    t = min(x["t0"] for x in mw if x["t0"] >= t - 0.05); ts_.append(t); ch.append(f"{mmss(t)} {title}")
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
import phone_side19 as PS
def own(png, a, z, name, lst, t_ref=None, size=None, u=None):
    """A label drawn inside a rendered scene: the renderer's chip is the reference; if the scene drew it at another size, its own pixels at the located place are."""
    pos, score = locate(png, t_ref or (a + z)/2)
    if score < 0.9:
        ref = Image.open(png); png = crop_png(t_ref or (a + z)/2, (pos[0], pos[1], pos[0] + ref.width, pos[1] + ref.height), png); pos, score = locate(png, min(z - 0.3, (t_ref or (a + z)/2) + 0.5))
    lst.append(dict(name=name, beat=[round(a, 3), round(z, 3)], chip=png, pos=pos, match=score))
def chip_sz(text, path, size):
    tmp = Image.new("RGBA", (1920, 200), (0, 0, 0, 0)); x0, y0, x1, y1 = B.disclosure(tmp, text, (100, 50), B.unit(1920, 1080), size=size)
    tmp.crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)))).save(path); return path
for i in R:
    if i["kind"] != "clip": continue
    a, z = fr(i["t0"])/FPS, fr(i["t1"])/FPS
    if i["id"] == "P06":                                # the approved self-generation demo: REAL chip beside the phone (frames 0..107), then the result with ITS OWN approved AI chip
        cut = (fr(i["t0"]) + 108)/FPS
        png = chip_u("Real picture of me. Not AI-generated.", f"{od}/chips/P06-real.png", 1.6); pos, score = locate(png, a + 1.5)
        real.append(dict(name="P06-before", beat=[round(a, 3), round(cut, 3)], chip=png, pos=pos, match=score))
        png = crop_png(cut + 2.0, (1052, 932, 1312, 990), f"{od}/chips/P06-ai.png"); pos, score = locate(png, (cut + z)/2)
        ai_ins.append(dict(name="P06-result", beat=[round(cut + 0.4, 3), round(z, 3)], chip=png, pos=pos, match=score))
    elif i["id"] == "P07":                              # the app tour: the two AI exercise demos inside the side phone; the chip sits on the video, where the app puts it (phone_side19.py)
        for nm, k0, k1, ex in (("P07-pushup", PS.T_S1 + 8, PS.T_S2, "pushup"), ("P07-reverse-lunge", PS.T_S2 + 8, PS.T_H2, "reverse-lunge")):
            vx, vy = [int(round(v*432/390)) for v in json.load(open(f"{PS.CAP}/sheet_{ex}.json"))["video"][:2]]; tw = int(B.text_w("AI-GENERATED", B.font(12)))
            x0 = 102 + PS.OX + 8 + vx + 9; y0 = 40 + 65 + vy + 9; ta = (fr(i["t0"]) + k0)/FPS; tz = (fr(i["t0"]) + k1)/FPS
            png = crop_png(ta + 0.5, (x0, y0, x0 + tw + 19, y0 + 23), f"{od}/chips/{nm}.png"); pos, score = locate(png, (ta + tz)/2)
            ai_ins.append(dict(name=nm, beat=[round(ta, 3), round(tz, 3)], chip=png, pos=pos, match=score))
    elif i.get("pair"): own(chip_sz(i["label"], f"{od}/chips/{i['id']}.png", 19), a, z, i["id"], real)
    elif i.get("photo") or i.get("portraits"): own(chip_png(i["label"], f"{od}/chips/{i['id']}.png"), a, z, i["id"], real)
    elif i.get("label"):
        png = chip_png(i["label"], f"{od}/chips/{i['id']}.png"); pos, score = locate(png, (a + z)/2)
        (ai_ins if i["label"] == "AI-GENERATED" else real).append(dict(name=i["id"], beat=[round(a, 3), round(z, 3)], chip=png, pos=pos, match=score))
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
