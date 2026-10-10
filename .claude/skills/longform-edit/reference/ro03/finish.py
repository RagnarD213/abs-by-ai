"""RO-03 round 2 finish (from the RO-02 finish): SRT sidecar (medium.en words on the delivered timeline, proofread against
the delivered audio), YouTube chapters (Set 1, Rest, Set 2, Rest, Set 3, How to start), and plan.json for the delivery gate.
No picture in this film carries a label: the opening clip is real moving footage of Dan (VIDEO-RULES: real videos are not
still photos). usage: finish.py MASTER.mp4   (writes next to the master)"""
import sys, os, json, re
W = "/Volumes/Extreme/_edit_work/ro03"; FPS = 30000/1001
master = os.path.abspath(sys.argv[1]); od = os.path.dirname(master); NAME = "RO03"
R = json.load(open(f"{W}/plan_resolved.json")); S = json.load(open(f"{W}/shots.json")); MK = json.load(open(f"{W}/marks.json"))
BJ = json.load(open(master + ".build.json")); total_f = BJ["frames"]; total = total_f/FPS
def fr(t): return int(round(t*FPS))

# ---------------------------------------------------------------- words on the delivered timeline (medium.en)
WO = json.load(open(f"{W}/words_out.json"))
# srt_words.json (beside the master), every row checked on the delivered audio's level before it was written:
#   drop   [t0, word, why]                  words the transcriber printed over a hold where nobody speaks
#   retime [t0, word, new_t0, new_t1, why]  a word the transcriber timed across a join (its start or end fell in the other shot)
SW = json.load(open(f"{od}/srt_words.json")) if os.path.exists(f"{od}/srt_words.json") else dict(drop=[], retime=[])
def key(w): return (round(w["t0"], 2), w["w"])
drop = {(round(t, 2), x) for t, x, _ in SW["drop"]}; ret = {(round(t, 2), x): (a, b) for t, x, a, b, _ in SW["retime"]}
assert drop | set(ret) <= {key(w) for w in WO if w["t0"] is not None}, "srt_words.json names a word that is not in words_out.json"
mw = []
for w in WO:
    if w["t0"] is None or key(w) in drop: continue
    t0, t1 = ret.get(key(w), (w["t0"], w["t1"])); assert t1 is not None, f"word with no end, add a retime row: {w['w']} at {w['t0']}"
    mw.append(dict(w=w["w"], t0=t0, t1=t1))
mw.sort(key=lambda x: x["t0"])
# ---------------------------------------------------------------- SRT (sidecar only; never burned)
FIX = [(r" -(\w)", r"-\1"), (r"(\d) \.(\d)", r"\1.\2"), (r"(\d) %", r"\1%"), (r"\babsbyai ?\.com\b", "AbsByAI.com"),
       (r"\by 'all\b", "y'all"), (r" '(s|re|ll|ve|d|t|m)\b", r"'\1"), (r"\bAlright\b", "All right")]
FIX += json.load(open(f"{od}/srt_fixes.json")) if os.path.exists(f"{od}/srt_fixes.json") else []   # heard on the delivered audio
def fix(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return s
# sentences first (a full stop, or a pause of 0.45 s), then each sentence in the fewest cues of 84 characters or less,
# split where the pieces come out most even, a comma preferred. No one-word leftovers.
sents, cur = [], []
for w in mw:
    if cur and w["t0"] - cur[-1]["t1"] >= 0.45 and cur[-1]["w"][-1:] in ".?!,": sents.append(cur); cur = []
    cur.append(w)
    if w["w"][-1:] in ".?!": sents.append(cur); cur = []
if cur: sents.append(cur)
def text(ws): return fix(" ".join(x["w"] for x in ws))
JOINERS = ("and", "but", "because", "before", "so", "when", "if", "as"); DANGLE = ("the", "a", "to", "of", "your", "that", "these", "you're", "i'm", "deep", "little", "my", "totally", "in", "and", "for", "is", "be")
def split(ws):
    if len(text(ws)) <= 84 and ws[-1]["t1"] - ws[0]["t0"] <= 6.5: return [ws]
    best = None
    for k in range(2, len(ws) - 1):
        a, b = text(ws[:k]), text(ws[k:]); prev, nxt = ws[k-1]["w"].lower(), ws[k]["w"].lower()
        cost = abs(len(a) - len(b)) - (30 if prev[-1:] == "," else 0) - (12 if nxt in JOINERS and prev[-1:] != "," else 0) + (25 if prev in DANGLE else 0)
        if best is None or cost < best[0]: best = (cost, k)
    k = best[1]; return split(ws[:k]) + split(ws[k:])
cues = []
for sn in sents:
    for c in split(sn): cues.append([c[0]["t0"], c[-1]["t1"], text(c)])
i = 0
while i < len(cues) - 1:                                   # a short opener ("So,") joins the cue it leads into
    if len(cues[i][2].split()) <= 2 and cues[i+1][0] - cues[i][1] < 1.0 and len(cues[i][2]) + len(cues[i+1][2]) < 84:
        cues[i+1] = [cues[i][0], cues[i+1][1], cues[i][2] + " " + cues[i+1][2]]; del cues[i]
    else: i += 1
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

# ---------------------------------------------------------------- chapters: each starts on its first picture (the flash into a set, the cut to a rest)
def mmss(t): t = int(round(t)); return f"{t//60}:{t % 60:02d}"          # the nearest whole second: 27.96 is 0:28, on the rest, not 0:27, still on the hold (round 2 review)
st = {s["id"]: s["out_f0"]/FPS for s in S}
ch = [(0.0, "Set 1"), (st["rest1.0r0"], "Rest (30 Seconds)"), (st["set2.0"], "Set 2"), (st["rest2.0r0"], "Rest (30 Seconds)"),
      (st["set3.0"], "Set 3"), (st["outro.0"], "How To Start If You're A Beginner")]
assert all(b[0] - a[0] >= 10 for a, b in zip(ch, ch[1:])) and total - ch[-1][0] >= 10, "YouTube needs chapters 10 s apart or more"
open(f"{od}/{NAME}.chapters.txt", "w").write("\n".join(f"{mmss(t)} {n}" for t, n in ch) + "\n")

# ---------------------------------------------------------------- picture timeline: presenter segments split at full-frame items
FULL = [i for i in R if i["kind"] in ("clip",) and i["t1"]]
pieces = []
for sg in BJ["segments"]:
    cuts = sorted({sg["o0"], sg["o1"]} | {fr(i["t0"]) for i in FULL if sg["o0"] < fr(i["t0"]) < sg["o1"]} | {fr(i["t1"]) for i in FULL if sg["o0"] < fr(i["t1"]) < sg["o1"]})
    for a, b in zip(cuts, cuts[1:]):
        cov = next((i for i in FULL if fr(i["t0"]) <= a and b <= fr(i["t1"])), None)
        pieces.append(dict(a=a, b=b, lab=f"insert-{cov['id']}" if cov else f"{sg['shot']}-{sg['framing']}", cov=bool(cov)))
merged = []
for p in pieces:
    if merged and merged[-1]["lab"] == p["lab"] and p["cov"] and merged[-1]["b"] == p["a"]: merged[-1]["b"] = p["b"]; continue
    merged.append(dict(p))
joins = sorted(set(round(p["a"]/FPS, 3) for p in merged[1:]))
punch = [[round(p["a"]/FPS, 3), round(p["b"]/FPS, 3), p["lab"]] for p in merged]
punch_cov = [p["cov"] for p in merged]
covered = [[round(fr(i["t0"])/FPS, 3), round(fr(i["t1"])/FPS, 3)] for i in FULL]
graphics = [dict(name=i["id"], beat=[round(fr(i["t0"])/FPS, 3), round(fr(i["t1"])/FPS, 3)]) for i in R if i["kind"] in ("lt", "wtitle", "work")]

plan = dict(target_seconds=round(total, 3), target_frames=total_f, ai_inserts=[], real_photos=[],
            joins=joins, covered=covered, punch=punch, punch_covered=punch_cov, graphics=graphics, cards=[],
            words=[dict(w=w["w"], t=w["t0"], e=w["t1"]) for w in mw], srt=srt,
            source_audio=f"{W}/film_untreated.wav", source_picture=master + ".base.mp4",
            banned_source="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4", banned_times=[12.0, 18.0, 288.0],
            watch_log=f"{od}/logs/watch_pass.json")
fw = f"{od}/final.whisper.json"
if os.path.exists(fw):
    r = json.load(open(fw)); plan["transcript_words"] = [dict(w=w["word"].strip()) for s in r["segments"] for w in s.get("words", [])]
ne = f"{od}/negative_events_scan.json"
if os.path.exists(ne): plan["negative_events_scan"] = json.load(open(ne))
json.dump(plan, open(f"{od}/plan.json", "w"), indent=0)
print("words", len(mw), "dropped", len(drop), "retimed", len(ret), "cues", len(out), "chapters", len(ch), "joins", len(joins), "pieces", len(merged), "graphics", len(graphics))
print("holds", MK["holds"], "beeps", MK["beeps"])
print("\n".join(f"{mmss(t)} {n}" for t, n in ch))
