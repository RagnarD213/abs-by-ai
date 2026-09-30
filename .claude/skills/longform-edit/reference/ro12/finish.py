#!/usr/bin/env python3
"""RO-12 finish: SRT sidecar + chapters from the DELIVERED audio's own transcript (final.whisper.json; the roll's Whisper words
are wrong inside the retake regions), plan.json for the delivery gate.  usage: finish.py MASTER.mp4"""
import sys, os, json, re, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FPS = 30000/1001
OD = "/Volumes/Extreme/_edit_work/ro12/out"; final = os.path.abspath(sys.argv[1]); NAME = "RO12"
T = json.load(open(f"{OD}/timeline.json")); ITEMS = T["items"]; SH = T["shots"]; total = T["total_frames"]/FPS
r = json.load(open(f"{OD}/final.whisper.json"))
mw = [dict(w=w["word"].strip(), t0=round(w["start"], 3), t1=round(w["end"], 3)) for s in r["segments"] for w in s.get("words", []) if w["word"].strip()]
json.dump(mw, open(f"{OD}/mapped-words.json", "w"))

FIX = [(r"\b(?:[Ss]et|[Zz]ap|[Zz]ep|[Zz]eph|[Zz]ip|[Ss]ep)[ -]?[Bb]ound(?:s)?\b", "Zepbound"), (r"\bZepbam\b", "Zepbound"),
       (r"\bon that bound\b", "on Zepbound"), (r"\b[Qq]uick [Pp]en(s?)\b", r"KwikPen\1"), (r"\bthe dough\b", "the dose"),
       (r"\b[Rr]otate your sights\b", "Rotate your sites"), (r"\bYou We will\b", "You will"), (r"\b[Aa]lmost everyone [Mm]ost everyone\b", "Almost everyone"),
       (r"\bswitching the Thursday\b", "switching to Thursday"), (r"\bunder eat\b", "under-eat"), (r"\bgets your results\b", "gets you results"),
       (r"(\d) \.(\d)", r"\1.\2"), (r" \.(\d)", r" 0.\1"), (r" -(\w)", r"-\1"), (r"\bmg\b", "mg"), (r"out of the Zepbound so you", "out of Zepbound, so you"), (r"\bOK\b", "Okay"), (r"\bCOVID\b", "COVID"),
       (r"\bZepbound 2 it\b", "Zepbound too, it"), (r"\bNeeds instead of pens\b", "Needles instead of pens"), (r"\bwhite knuckle\b", "white-knuckle"),
       (r"\bfires a drug\b", "fires the drug"), (r"\bIf you were on this\b", "If you're on this"), (r"\bis a ramp I already\b", "is the ramp I already"),
       (r"\bprotein focused\b", "protein-focused"), (r"within a few months And now", "within a few months, and now"),
       (r"possible way So here's", "possible way. So here's"), (r"I use instead instead of going off totally Start", "I use instead. Instead of going off totally, start"),
       (r"milligrams to two if you do not", "milligrams to two. If you do not"), (r"one and a half Keep", "one and a half. Keep"),
       (r"goal weight If you go above", "goal weight. If you go above"), (r"\bpeople but it is a tool it only", "people. But it is a tool, it only"),
       (r"never lift you're", "never lift, you're"), (r"about to be go and", "about to be, go and")]
def fix(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return s
# ---------------------------------------------------------------- SRT (RO-05 round 4 cue rules)
def join(tok): return " ".join(tok)
cues = []; cur = []
def flush():
    global cur
    if cur: cues.append([cur[0]["t0"], cur[-1]["t1"], fix(join([w["w"] for w in cur]))]); cur = []
for w in mw:
    if cur:
        gap = w["t0"] - cur[-1]["t1"]; txt = join([x["w"] for x in cur + [w]])
        if gap >= 0.45 or len(txt) > 80 or w["t1"] - cur[0]["t0"] > 5.5: flush()
    cur.append(w)
    if w["w"][-1:] in ".?!" and (cur[-1]["t1"] - cur[0]["t0"]) > 1.2: flush()
flush()
def wrap(s):
    if len(s) <= 44: return s
    ws = s.split(); best = None
    for k in range(1, len(ws)):
        a, b = " ".join(ws[:k]), " ".join(ws[k:]); m = max(len(a), len(b))
        if best is None or m < best[0]: best = (m, a + "\n" + b)
    return best[1]
def ts(t):
    t = max(0, t); h = int(t//3600); m = int(t % 3600//60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)) % 1000:03d}"
for i in range(len(cues)):
    if cues[i][2] and cues[i][2][0].islower() and (i == 0 or cues[i-1][2].rstrip()[-1:] in ".?!"): cues[i][2] = cues[i][2][0].upper() + cues[i][2][1:]
out = []
for i, (a, b, s) in enumerate(cues):
    b = max(b, a + 0.9)
    if i + 1 < len(cues): b = min(b, cues[i+1][0] - 0.02)
    out.append(f"{i+1}\n{ts(a)} --> {ts(b)}\n{wrap(s)}\n")
srt = f"{OD}/{NAME}.srt"; open(srt, "w").write("\n".join(out))
# ---------------------------------------------------------------- chapters (tip titles)
def mmss(t): return f"{int(t//60)}:{int(t % 60):02d}"
CH = {"T01": "Tip 1: Use needles and vials, not pens", "T02": "Tip 2: How to actually inject", "T03": "Tip 3: Inject on Thursday evening",
      "T04": "Tip 4: Ramp on slowly, taper off even slower", "T05": "Tip 5: Focus on protein", "S04": "Recap: the 5 tips"}
ch = ["0:00 Before and after"] + [f"{mmss(it['o0'])} {CH[it['id']]}" for it in sorted(ITEMS, key=lambda i: i["o0"]) if it["id"] in CH]
open(f"{OD}/{NAME}.chapters.txt", "w").write("\n".join(ch) + "\n")
# ---------------------------------------------------------------- plan.json
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 23), b""): h.update(b)
    return h.hexdigest()
FULL = ("insert", "title", "beforenow", "ramp", "week", "recap", "photo")
covers = [[round(it["f0"]/FPS, 3), round(it["f1"]/FPS, 3)] for it in ITEMS if it["kind"] in FULL]
joins = [round(s["f0"]/FPS, 3) for s in SH[1:]]
punch = [[round(s["f0"]/FPS, 3), round(s["f1"]/FPS, 3), s["fr"]] for s in SH]
pc = [any(a - 0.02 <= p[0] and p[1] <= b + 0.02 for a, b in covers) for p in punch]
vsha = sha(final)
plan = dict(target_seconds=round(total, 3), target_frames=T["total_frames"], joins=joins, covered=covers, punch=punch, punch_covered=pc,
            graphics=[dict(name=i["id"], beat=[round(i["o0"], 3), round(i["o1"], 3)]) for i in ITEMS if i["kind"] in ("lt", "l3", "title", "phone", "ramp", "week", "recap", "beforenow", "photo")],
            cards=sorted(covers), ai_inserts=[], real_photos=[dict(name="S01 before + now (real)", beat=[round(i["o0"], 3), round(i["o1"], 3)]) for i in ITEMS if i["id"] in ("S01", "S01b")],
            words=[dict(w=w["w"], t=w["t0"], e=w["t1"]) for w in mw], transcript_words=[dict(w=w["w"]) for w in mw],
            speech_words=[dict(w=w["w"], t=w["t0"], e=w["t1"]) for w in mw], speech_words_evidence=dict(method="delivered_asr", video_sha256=vsha),
            srt=srt, source_audio=f"{OD}/voice_raw.wav", source_picture=f"{OD}/BASE.mp4", watch_log=f"{OD}/logs/watch_pass.json",
            junk_report="/Volumes/Extreme/_edit_work/ro12/check/junk_prerender.json")
# compliance:labels inputs: the two real photos (S01, S01b) carry the real-picture chip drawn by softblue.scene_photo; no AI
# image of Dan in this cut (A0058 / A0064 are other men). Chip PNGs rendered with the same softblue.disclosure call.
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"); import softblue as S
from PIL import Image
def chip_png(txt, path):
    im = Image.new("RGBA", (1920, 200), (0, 0, 0, 0)); x0, y0, x1, y1 = S.disclosure(im, txt, (100, 50), 2)
    im.crop((int(x0), int(y0), int(x1 + 0.999), int(y1 + 0.999))).save(path); return (x1 - x0)
bw_real = chip_png("Real picture of me. Not AI-generated.", f"{OD}/chip_real.png"); chip_png("AI-GENERATED", f"{OD}/chip_ai.png")
plan["label_chips"] = dict(ai=f"{OD}/chip_ai.png", real=f"{OD}/chip_real.png")
rp = []
for it in ITEMS:
    if it["kind"] != "photo": continue
    pw, ph = S.photo_size(it["photo"], 1920 - 210*2, 1080 - 115*2); py = (1080 - ph)/2 - 20
    rp.append(dict(name=f"{it['id']} {it['eyebrow']} (real photo)", beat=[round(it["o0"] + 0.5, 3), round(it["o1"] - 0.1, 3)],
                   chip=f"{OD}/chip_real.png", pos=[int(960 - bw_real/2), int(py + ph + 44)]))
plan["real_photos"] = rp; plan["ai_inserts"] = []
plan["banned_source"] = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4"
plan["banned_times"] = [12.0, 18.0, 288.0]
ne = f"{OD}/negative_events_scan.json"
if os.path.exists(ne): plan["negative_events_scan"] = json.load(open(ne))
json.dump(plan, open(f"{OD}/plan.json", "w"), indent=0)
print("words", len(mw), "cues", len(out), "joins", len(joins), "graphics", len(plan["graphics"])); print("\n".join(ch))
