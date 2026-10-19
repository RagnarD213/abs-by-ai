"""RO-20 round 4 finish, per video (from finish_r3.py): SRT sidecar (medium.en film words + the pickups' own word files, mapped onto the
video's timeline), YouTube chapters per video, label-chip references located on the delivered frame, and plan.json for the delivery gate.
usage: finish_r4.py V   (reads round4/V/layout.json and MASTER.mp4; writes next to them)"""
import sys, os, json, re, subprocess, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import films_r4 as F4
W = F4.W; FPS = F4.FPS; FF = F4.FF; fr = F4.fr
V = sys.argv[1]; od = f"{W}/round4/{V}"; master = f"{od}/MASTER.mp4"; NAME = F4.VIDEOS[V]["job"].replace("-", "")
LAY = json.load(open(f"{od}/layout.json")); total_f = LAY["frames"]; total = total_f/FPS
R = F4.Bd.R; byid = {i["id"]: i for i in R}          # the plan as films_r4 builds it (round 4 review fixes applied in memory)
PK = F4.PK
def film_map(t):
    """film time -> this video's time (None when the film moment is not in this video)"""
    f = t*FPS
    for P in LAY["parts"]:
        p = P["part"]
        if p[0] == "film" and p[1] <= f < p[2]: return (f - p[1] + P["out"][0])/FPS
    return None
def film_part(t):
    f = t*FPS
    return next((P for P in LAY["parts"] if P["part"][0] == "film" and P["part"][1] <= f < P["part"][2]), None)
# ---------------------------------------------------------------- words on the delivered timeline
WO = json.load(open(f"{W}/words_out.json"))
for k, w in enumerate(WO):
    if w["t0"] is None and w["t1"] is not None and k and WO[k-1]["t1"] is not None: w["t0"] = min(w["t1"] - 0.05, max(WO[k-1]["t1"], w["t1"] - 0.25))
for k, w in enumerate(WO):
    if w["t0"] is not None and w["t1"] is None:
        nx = next((x["t0"] for x in WO[k+1:] if x["t0"] is not None), w["t0"] + 0.25); w["t1"] = max(w["t0"] + 0.05, min(w["t0"] + 0.25, nx))
mw = []
for P in LAY["parts"]:
    p, (a, b) = P["part"], P["out"]
    if p[0] == "film":
        for w in WO:
            if w["t0"] is None: continue
            if p[1] <= (w["t0"] + w["t1"])/2*FPS < p[2]:            # by the word's middle: video 3's "All" starts 4 ms before its own range
                off = (a - p[1])/FPS; mw.append(dict(w=w["w"], t0=w["t0"] + off, t1=min(w["t1"] + off, b/FPS)))
    elif p[0] == "pickup":
        for w in json.load(open(f"{PK}/words_{p[1]}.json"))["words"]:
            mw.append(dict(w=w["w"], t0=w["t0"] + a/FPS, t1=w["t1"] + a/FPS))
mw.sort(key=lambda x: x["t0"])
_m = []                                                          # one word, not two cues: "y" + "'all", "long" + "-term"
for w in mw:
    if _m and (w["w"][:1] in "'-" or w["w"].startswith("'")) and w["t0"] - _m[-1]["t1"] < 0.25: _m[-1] = dict(_m[-1], w=_m[-1]["w"] + w["w"], t1=w["t1"])
    else: _m.append(w)
mw = _m
# a capital in mid-sentence (Whisper medium started a new segment without its full stop: "So Let's say", "dead If"): the delivered-audio transcript
# (final.whisper.json) decides: a full stop there in it -> add one; otherwise the word goes lower case. "I" and names keep their capital.
_KEEP = {"I", "I'm", "I'll", "I've", "I'd", "AI", "Dan", "Zepbound", "Oura", "Whoop", "Apple", "Purple", "Costco", "Bryan", "Brian", "Johnson", "Clean", "Eatz",
         "GLP", "TRT", "Taco", "Bell", "U.S.", "OK", "Okay", "Netflix", "Abs", "By", "AbsByAI.com", "Instagram", "YouTube", "Uber", "DoorDash", "Christmas"}
_STARTERS = {"So", "Now", "You", "And", "But", "If", "Then", "The", "That", "This", "It", "We", "They", "There", "Here", "What", "When", "Once", "Or",
             "Because", "Even", "Just", "Instead", "Leading", "Draining", "Let's", "Go", "Get", "My", "Your", "A", "An", "In", "On", "At", "For", "With",
             "As", "Not", "No", "All", "Some", "Most", "Make", "Don't", "Do", "He", "She", "His", "Her", "Their", "Those", "These", "Which", "Who", "Also"}
_fw = f"{od}/final.whisper.json"
if os.path.exists(_fw):
    _r = json.load(open(_fw)); _W = [(w["start"], w["word"].strip()) for sg in _r["segments"] for w in sg.get("words", [])]
    _ws = [t for t, _ in _W]
    import bisect
    for k in range(1, len(mw)):
        w, pw = mw[k]["w"], mw[k-1]["w"]
        if w.strip(",.?!") not in _STARTERS or pw[-1:] in ".?!": continue        # only common sentence starters; names keep their capitals
        j = bisect.bisect_left(_ws, mw[k]["t0"] - 0.4); stop = False
        for t, ww in _W[max(0, j - 2): j + 4]:
            if abs(t - mw[k]["t0"]) < 0.6 and ww.lower().strip(",.?!") == w.lower().strip(",.?!"):
                prev = _W[_W.index((t, ww)) - 1][1] if _W.index((t, ww)) else ""; stop = prev[-1:] in ".?!"; break
        if stop: mw[k-1] = dict(mw[k-1], w=pw.rstrip(",") + ".")
        else: mw[k] = dict(mw[k], w=w[0].lower() + w[1:])
# word-level corrections heard on the delivered audio (reviews 2026-10-18); they work across subtitle cue edges. Matched without punctuation or case.
def _k(x): return re.sub(r"[^a-z0-9']", "", x.lower())
for seq, rep in (json.load(open(f"{W}/round4/word_fixes.json")) if os.path.exists(f"{W}/round4/word_fixes.json") else []):
    n = len(seq)
    for k in range(len(mw) - n + 1):
        if [_k(mw[k + j]["w"]) for j in range(n)] == seq:
            for j in range(n): mw[k + j] = dict(mw[k + j], w=rep[j].strip())    # an empty replacement drops that word (its time joins the one before)
mw = [w for w in mw if w["w"]]
# ---------------------------------------------------------------- SRT
FIX = [(r" -(\w)", r"-\1"), (r"(\d) \.(\d)", r"\1.\2"), (r"(\d) %", r"\1%"), (r"(\d) ,(\d{3})", r"\1,\2"),
       (r"\bZep down\b", "Zepbound"), (r"\bchat JPT\b", "ChatGPT"), (r"\babsbyai ?\.com\b", "AbsByAI.com"), (r"\babsbyai \.com\b", "AbsByAI.com"),
       (r"\by 'all\b", "y'all"), (r" '(s|re|ll|ve|d|t|m)\b", r"'\1"), (r"\bAbs by AI\b", "Abs By AI"), (r"\bsix -pack\b", "six-pack")]
FIX += [tuple(x) for x in json.load(open(f"{W}/recipe/srt_fixes.json"))]
if os.path.exists(f"{W}/round4/srt_fixes.json"): FIX += [tuple(x) for x in json.load(open(f"{W}/round4/srt_fixes.json"))]   # heard on the delivered audio
def fix(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return re.sub(r"(?<!U\.S)([.?!] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)     # a sentence starts with a capital ("U.S." is not an end)
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
    t = max(0, t); h = int(t//3600); m = int(t % 3600//60); s = t % 60; ms = int(round((s - int(s))*1000))
    if ms == 1000: ms = 999
    return f"{h:02d}:{m:02d}:{int(s):02d},{ms:03d}"
for i in range(len(cues)):
    if cues[i][2] and cues[i][2][0].islower() and (i == 0 or (cues[i-1][2].rstrip()[-1:] in ".?!" and not cues[i-1][2].rstrip().endswith("U.S."))): cues[i][2] = cues[i][2][0].upper() + cues[i][2][1:]
out = []
for i, (a, b, s) in enumerate(cues):
    b = max(b, a + 0.9)
    if i + 1 < len(cues): b = min(b, cues[i+1][0] - 0.02)
    b = min(b, total - 0.05)
    out.append(f"{i+1}\n{ts(a)} --> {ts(b)}\n{wrap(s)}\n")
srt = f"{od}/{NAME}.srt"; open(srt, "w").write("\n".join(out))
# ---------------------------------------------------------------- chapters (each on its section's first lower third; pickups by their own start)
def mmss(t): return f"{int(t//60)}:{int(t % 60):02d}"
def pk_start(pid): return next(P["out"][0]/FPS for P in LAY["parts"] if P["part"][0] == "pickup" and P["part"][1] == pid)
CH = {   # (lower third that marks the section, title, the spoken words that open the section: the chapter starts on them, reviewer note 2026-10-18)
 "v1": [("Ga01", "Reason 1: The Halo Effect", None), ("Gb01", "How Your Weight Changes Your Relationship", "let's say that you're in a relationship"),
        ("Gb05", "Online Dating", "and obviously if you are single"), ("Gb10", "Reason 2: You Get More Done", "alright let's talk about the second reason"),
        ("Gb14", "Gym Time Or Doctor's Office Time", "here's another reason why looking good"), ("Gb19", "Reason 3: Better Mental Health", "the third reason why"),
        ("Gc01", "Reason 4: Bad Health Is Ludicrously Expensive", "the fourth reason why"), ("Gc09", "Money Does You No Good If You're Dead", "now here's the final point"),
        ("@P1", "What's Next", None), ("Gi01", "See Yourself With Six-Pack Abs", "alright guys that's today's video")],
 "v2": [("Gc17", "The \"I'm Broke\" Excuse", "but i know at this point"), ("Gc19", "3 Things You Should Never Cut", "alright so before we go into what to cut"),
        ("Gd01", "What To Sacrifice", "okay so let's talk about what we should sacrifice"), ("Gd03", "1: Bars And Clubs", "the number one thing that we wanna cut"),
        ("Gd08", "2: Eating At Restaurants", "here's the next thing you need to sacrifice"), ("Gd14", "3: Junk Food In The House", "the next thing you need to sacrifice is the junk food"),
        ("Gd17", "4: Vacations", "the final thing you need to sacrifice"), ("Gd23", "5: Therapy And Psychiatric Medication", "and here's one more thing that you should sacrifice"),
        ("Gd28", "Subscriptions, Car Payments And Clothes", "now there's also a few other things"), ("@P3", "What's Next", None)],
 "v3": [("Gd31", "If You're Dead Broke", "so let's say you're dead broke"), ("Ge01", "Middle Class: The Best Protein", "okay so now that i told"),
        ("Ge08", "A Better Mattress", "number two thing you middle class"), ("Ge20", "A Membership At The Best Gym", "the next thing you have to invest in"),
        ("Ge27", "A Sleep Tracker", "here's the next thing you middle class guys need"), ("Gf01", "GLP-1 Medication", "all right here's the next thing you need to be putting"),
        ("Gf08", "TRT", "here's the next thing you middle class guys"), ("Gf13", "Supplements", "here's the final thing you need to be investing"),
        ("Gf24", "Over $10,000 A Month: A Home Gym", "so now let's talk about"), ("Gg01", "A Meal Prep Service Or A Personal Chef", "here is the next thing that you need"),
        ("Gg06", "A Maid And A Laundry Service", "the next thing that you need if you're rich"), ("Gg08", "A Personal Trainer And Nutritionist", "now the final thing you should consider"),
        ("Gg13", "Beyond The List", "so now i want to talk to you guys who are the mega"), ("Gg18", "Summary", "all right so let's summarize"),
        ("Gh01", "Your First Step", "alright guys that's today's video")],
}[V]
FIRST = {"v1": "Why You Should Invest More In Your Health", "v2": "You're Being Too Cheap With Your Health", "v3": "What To Buy For Your Health At Every Income Level"}[V]
ch = [(0.0, FIRST)]
def _n(x): return re.sub(r"[^a-z' ]", "", x.lower().replace("-", " ")).replace("alright", "all right")
def phrase_at(ph, t_lt):
    """start of the words `ph` in this video's words, inside the 45 s before the lower third"""
    target = _n(ph).split(); toks = [(_n(w["w"]).strip(), w["t0"]) for w in mw]; toks = [(a, t) for a, t in toks if a]
    flat = []
    for a, t in toks: flat += [(x, t) for x in a.split()]
    for i in range(len(flat) - len(target) + 1):
        if t_lt - 45 <= flat[i][1] <= t_lt + 1 and [x for x, _ in flat[i:i + len(target)]] == target: return flat[i][1]
    raise SystemExit(f"chapter phrase not found: {ph!r} before {t_lt:.1f}")
for k, title, ph in CH:
    t = pk_start(k[1:]) if k.startswith("@") else film_map(byid[k]["t0"])
    assert t is not None, (V, k)
    if ph:
        t0p = phrase_at(ph, t); part0 = next(P["out"][0]/FPS for P in LAY["parts"] if P["out"][0]/FPS <= t0p < P["out"][1]/FPS)
        t = max(part0, t0p + 0.05)                     # on the first word (a lead before it showed the last second of the previous section)                     # never before the part it is in (the sign-off chapter landed on the pickup's last second)
    if t < 10.0: ch[0] = (0.0, title); continue          # YouTube needs 10 s per chapter: an early first section becomes 0:00
    ch.append((t, title))
ch.sort()
for (x, _), (y, _) in zip(ch, ch[1:]): assert y - x >= 10, f"chapters under 10 s apart: {x:.1f} {y:.1f}"
open(f"{od}/{NAME}.chapters.txt", "w").write("\n".join(f"{mmss(t)} {s}" for t, s in ch) + "\n")
# ---------------------------------------------------------------- picture timeline
FULL = [i for i in R if i["kind"] == "clip" and i["t1"]]
def mapped_items(kinds):
    res = []
    for i in R:
        if i["kind"] not in kinds: continue
        P = film_part(i["t0"])
        if not P or (len(P["part"]) > 3 and P["part"][3] == "bare"): continue
        off = P["out"][0] - P["part"][1]
        res.append(dict(i, f0=fr(i["t0"]) + off, f1=min(fr(i["t1"]) + off, P["out"][1]), part=LAY["parts"].index(P)))
    return res
CLIPS = mapped_items(("clip",)); LTS = mapped_items(("lt",))
pieces = []
for P in LAY["parts"]:
    a, b = P["out"]
    if P["part"][0] == "pickup":
        pieces.append(dict(a=a, b=b, lab=f"pickup-{P['part'][1]}", cov=True)); continue
    for sg in P["segments"]:
        cuts = {sg["o0"], sg["o1"]} | {c["f0"] for c in CLIPS if sg["o0"] < c["f0"] < sg["o1"]} | {c["f1"] for c in CLIPS if sg["o0"] < c["f1"] < sg["o1"]}
        cuts = sorted(cuts)
        for x, y in zip(cuts, cuts[1:]):
            cov = next((c for c in CLIPS if c["f0"] <= x and y <= c["f1"]), None)
            pieces.append(dict(a=x, b=y, lab=f"insert-{cov['id']}" if cov else f"{sg['shot']}-{sg['framing']}", cov=bool(cov)))
# one continuous take at one crop is one piece, even where the solve split it at a cutaway that has since been removed (round 4: Cb04, Cc21 ...)
_src_end = {}
for P in LAY["parts"]:
    for sg in P.get("segments", []): _src_end[sg["o0"]] = (sg["src0"], sg["o1"] - sg["o0"], tuple(sg["crop"]))
def _continues(a, b):
    sa = next((v for k, v in _src_end.items() if k <= a["a"] < k + v[1]), None); sb = next((v for k, v in _src_end.items() if k <= b["a"] < k + v[1]), None)
    if not sa or not sb: return False
    ka = next(k for k, v in _src_end.items() if v is sa); kb = next(k for k, v in _src_end.items() if v is sb)
    return sa[2] == sb[2] and sa[0] + (a["b"] - ka) == sb[0] + (b["a"] - kb)
merged = []
for p in pieces:
    if merged and merged[-1]["lab"] == p["lab"] and p["cov"] and merged[-1]["b"] == p["a"]: merged[-1]["b"] = p["b"]; continue
    if merged and not p["cov"] and not merged[-1]["cov"] and merged[-1]["b"] == p["a"] and _continues(merged[-1], p): merged[-1]["b"] = p["b"]; continue
    merged.append(dict(p))
subcuts = []
for c in CLIPS:
    if len(c.get("src", [])) > 1:
        n = c["f1"] - c["f0"]; per = n // len(c["src"]); subcuts += [c["f0"] + per*k for k in range(1, len(c["src"]))]
PKCUES = {}
for P in LAY["parts"]:
    if P["part"][0] != "pickup": continue
    cj = json.load(open(f"{PK}/{P['part'][1]}.mp4.cues.json")); PKCUES[P["part"][1]] = (P["out"][0]/FPS, cj)
    for bl in cj["built"]:
        for t in (bl["t"], bl.get("end")):
            if t: subcuts.append(int(round(P["out"][0] + t*FPS)))
joins = sorted(set(round(p["a"]/FPS, 3) for p in merged[1:]) | set(round(f/FPS, 3) for f in subcuts if 0 < f < total_f))
punch = [[round(p["a"]/FPS, 3), round(p["b"]/FPS, 3), p["lab"]] for p in merged]
punch_cov = [p["cov"] for p in merged]
covered = [[round(c["f0"]/FPS, 3), round(c["f1"]/FPS, 3)] for c in CLIPS] + [[round(P["out"][0]/FPS, 3), round(P["out"][1]/FPS, 3)] for P in LAY["parts"] if P["part"][0] == "pickup"]
cards = [[round(P["out"][0]/FPS, 3), round(P["out"][1]/FPS, 3)] for P in LAY["parts"] if P["part"][0] == "pickup"]
cards += [[round(c["f0"]/FPS, 3), round(c["f1"]/FPS, 3)] for c in CLIPS if str(c.get("src", [""])[0]).find("/cards/") >= 0]
MAN = {m["id"]: m for m in F4.MAN}                     # with the round 4 re-timed copies
def lt_mov(i):
    o = F4.PART_MAN.get((V, i["part"]), {})
    if i["id"] in o: return {"mov": o[i["id"]]["mov"]} if o[i["id"]] else {}
    return {"mov": MAN[i["id"]]["mov"]} if i["id"] in MAN else {}
graphics = [dict(name=i["id"], beat=[round(i["f0"]/FPS, 3), round(i["f1"]/FPS, 3)], **lt_mov(i)) for i in LTS]
# audio joins: where the voice itself was joined (part edges, and inside film parts where the source is not continuous)
audio_joins = sorted(set([round(P["out"][0]/FPS, 3) for P in LAY["parts"][1:]] +
                         [round(b["o0"]/FPS, 3) for P in LAY["parts"] if P.get("segments") for a, b in zip(P["segments"], P["segments"][1:]) if b["src0"] != a["src0"] + (a["o1"] - a["o0"])]))
# ---------------------------------------------------------------- label chips, located on the delivered frame
import softblue as B
import cv2
def grab(t):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", master, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1080, 1920).astype(np.float32)
def chip_img(text, u, size=None):
    tmp = Image.new("RGBA", (1920, 240), (0, 0, 0, 0)); kw = {"size": size} if size else {}
    x0, y0, x1, y1 = B.disclosure(tmp, text, (100, 60), u, **kw)
    return tmp.crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))))
def locate_img(ref, t):
    flat = Image.alpha_composite(Image.new("RGBA", ref.size, (80, 80, 80, 255)), ref.convert("RGBA"))
    r = np.asarray(flat.convert("L"), np.float32); g = grab(t)
    res = cv2.matchTemplate(g, r, cv2.TM_CCOEFF_NORMED); _, mx, _, loc = cv2.minMaxLoc(res); return [int(loc[0]), int(loc[1])], float(mx), r.shape
def own_pixels(t, pos, shape, path):
    h, w = shape; g = grab(t)[pos[1]:pos[1] + h, pos[0]:pos[0] + w]; Image.fromarray(g.astype(np.uint8)).convert("RGBA").save(path); return path
os.makedirs(f"{od}/chips", exist_ok=True)
U = B.unit(1920, 1080)
def best_chip(text, t, sizes=(None,), units=(U,)):
    best = None
    for u in units:
        for s in sizes:
            ref = chip_img(text, u, s); pos, sc, shape = locate_img(ref, t)
            if best is None or sc > best[1]: best = (pos, sc, shape)
    return best
ai_ins, real = [], []
P01_AI_BOX = (980, 932, 1308, 981)    # the demo's own AI-GENERATED pill on its pool result, measured on the delivered frame (2026-10-18)
def add(lst, name, text, a, z, at, sizes=(None,), units=(U,), box=None):
    pos, sc, shape = best_chip(text, at, sizes, units)
    if box and sc < 0.8: pos, shape = [box[0], box[1]], (box[3] - box[1], box[2] - box[0])
    png = own_pixels(at, pos, shape, f"{od}/chips/{name}.png")       # the reference is the chip's own delivered pixels where it was found
    pos2, sc2, _ = locate_img(Image.open(png), at)
    lst.append(dict(name=name, beat=[round(a, 3), round(z, 3)], chip=png, pos=pos2, match=round(sc2, 3), found_score=round(sc, 3)))
for i in CLIPS:
    if not i.get("label"): continue
    a, z = i["f0"]/FPS, i["f1"]/FPS
    if i["id"] in ("P01", "P03"):                      # P03 is the same approved demo (video 1 sign-off)
        cut = a + 108/FPS
        add(real, f"{i['id']}-before", "Real picture of me. Not AI-generated.", a, cut, a + 1.5, units=(1.6, U))
        add(ai_ins, f"{i['id']}-result", "AI-GENERATED", cut + 0.4, z, (cut + z)/2, units=(U, 1.0, 1.2, 1.6), box=P01_AI_BOX)
    else:
        add(ai_ins if i["label"] == "AI-GENERATED" else real, i["id"], i["label"], a, z, (a + z)/2, units=(U, 1.0, 1.2, 1.6))
for pid, (t0, cj) in PKCUES.items():
    for k, bl in enumerate(cj["built"]):
        s = bl["shows"]
        if "AI-GENERATED chip" in s:
            a, z = t0 + bl["t"] + 0.30, t0 + bl["end"] - 0.30
            if z - a < 0.1: a, z = t0 + (bl["t"] + bl["end"])/2 - 0.05, t0 + (bl["t"] + bl["end"])/2 + 0.05
            add(ai_ins, f"{pid}-w{k}", "AI-GENERATED", a, z, (a + z)/2, sizes=(17, 16, 18), units=(U,))
        elif "self-generation app demo" in s:
            a, z = t0 + bl["t"], t0 + bl["end"]; cut = a + 108/FPS
            add(real, f"{pid}-P01-before", "Real picture of me. Not AI-generated.", a + 0.2, cut - 0.2, a + 1.5, units=(1.6, U))
            add(ai_ins, f"{pid}-P01-result", "AI-GENERATED", cut + 0.4, z - 0.2, (cut + z)/2, units=(U, 1.0, 1.2, 1.6), box=P01_AI_BOX)
chips = dict(ai=f"{od}/chips/_ai.png", real=f"{od}/chips/_real.png"); chip_img("AI-GENERATED", U).save(chips["ai"]); chip_img("Real picture of me. Not AI-generated.", U).save(chips["real"])
plan = dict(audio_joins=audio_joins, target_seconds=round(total, 3), target_frames=total_f, ai_inserts=ai_ins, real_photos=real, label_chips=chips,
            joins=joins, covered=covered, punch=punch, punch_covered=punch_cov, graphics=graphics, cards=sorted(cards),
            words=[dict(w=w["w"], t=w["t0"], e=w["t1"]) for w in mw], srt=srt, source_audio=f"{od}/untreated.wav", source_picture=f"{od}/base.mp4",
            banned_source="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4", banned_times=[12.0, 18.0, 288.0],
            watch_log=f"{od}/logs/watch_pass.json")
fw = f"{od}/final.whisper.json"
if os.path.exists(fw):
    r = json.load(open(fw)); plan["transcript_words"] = [dict(w=w["word"].strip()) for s in r["segments"] for w in s.get("words", [])]
ne = f"{od}/negative_events_scan.json"
if os.path.exists(ne): plan["negative_events_scan"] = json.load(open(ne))
json.dump(plan, open(f"{od}/plan.json", "w"), indent=0)
print(V, "words", len(mw), "cues", len(out), "chapters", len(ch), "joins", len(joins), "pieces", len(merged), "graphics", len(graphics))
print("labels:", [(x["name"], x["pos"], x["found_score"], x["match"]) for x in ai_ins + real])
print(open(f"{od}/{NAME}.chapters.txt").read())
