"""DS-40 R6 burned captions: word-timed cues on the film timeline (the Soft Blue shorts caption: Arial Bold 86, white,
7 px black outline). Maher's words from the clip transcript, Dan's from the roll transcript mapped through the cuts.
During the clip the captions sit at top 1040 (under Maher's face, whose lowest point is y 1014, and above the small
Dan, whose head starts about y 1290); from the move on, the standard top line 1412.

    python3 captions.py   -> cues.json, words_film.json
"""
import json, re, sys
sys.path.insert(0, "/Users/danielrose/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude/Projects/Abs By AI/"
                   ".claude/worktrees/stoic-cartwright-8bfcc9/.claude/skills/shorts/reference/softblue-sl03")
from PIL import ImageFont, ImageDraw, Image
import plan as PL
FPS = PL.FPS
ARIAL = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CLIP_IN = 4.40
ROLLW = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.roll/words.json"
FIX = {"-fat": "overfat"}

words = []
d = json.load(open("/Volumes/Expansion/_edit_work/ds40/r3/clip/maher_words.json"))
for s in d["segments"]:
    for x in s["words"]:
        if CLIP_IN - 0.05 <= x["start"] < 23.55:          # "that" begins after the cut (24.36 measured in R3)
            w = x["word"].strip()
            words.append(dict(w=w, t=round(x["start"] - CLIP_IN, 3), e=round(min(x["end"], 23.78) - CLIP_IN, 3), p=0))
for w in words:
    if w["w"].lower() == "let": w["w"] = "Let"
    if w["w"] == "90": w["w"] = "90-year-old?"
words = [w for w in words if w["w"] not in ("year", "old?")]
rw = json.load(open(ROLLW)); rw = rw.get("words", rw) if isinstance(rw, dict) else rw
roll_end = (PL.ROLLF0 + PL.j_end + 1) / FPS
c1, c2 = PL.CUT1, PL.CUT2
for x in rw:
    s, e, w = x.get("start", x.get("s")), x.get("end", x.get("e")), (x.get("word") or x.get("w")).strip()
    if not (1400.30 <= s < roll_end): continue
    # Whisper starts "Most" at 1436.30, inside the measured silence before the cut; it really starts after it
    if c1[0] - 0.1 <= s < c1[0] + c1[1] / FPS or c2[0] - 0.1 <= s < c2[0] + c2[1] / FPS: continue
    words.append(dict(w=w, t=round(PL.film_s(s), 3), e=round(PL.film_s(min(e, roll_end - 0.01)), 3), p=1))
# Whisper split "overfat" into "over" + "-fat"
for i in range(len(words) - 1):
    if words[i]["w"] == "over" and words[i + 1]["w"] == "-fat":
        words[i]["w"] = "overfat"; words[i]["e"] = words[i + 1]["e"]; words[i + 1]["w"] = None
words = [w for w in words if w["w"]]
json.dump(words, open("words_film.json", "w"), indent=0)

f = ImageFont.truetype(ARIAL, 86); dr = ImageDraw.Draw(Image.new("RGB", (8, 8)))
tw = lambda s: dr.textlength(s, font=f)


def cap_lines(text, maxw=960):
    if tw(text) <= maxw: return [text]
    ws = text.split(); best = None
    for k in range(1, len(ws)):
        a, b = " ".join(ws[:k]), " ".join(ws[k:]); m = max(tw(a), tw(b))
        if best is None or m < best[0]: best = (m, [a, b])
    assert best[0] <= 1000, text
    return best[1]


cues, cur = [], []
def flush():
    if cur: cues.append(list(cur)); cur.clear()
for w in words:
    ends = bool(re.search(r"[.!?]$", w["w"])); n = len(" ".join(x["w"] for x in cur)) + len(w["w"])
    if cur and (w["p"] != cur[-1]["p"] or w["t"] - cur[-1]["e"] > 0.6 or (len(cur) >= 4 and not (ends and n <= 30)) or (n > 24 and not (ends and n <= 30))):
        flush()
    cur.append(w)
    if re.search(r"[.!?:]$", w["w"]) or (re.search(r",$", w["w"]) and len(cur) >= 2): flush()
flush()
out = []
for c in cues:   # a one-word cue that does not end a sentence leads into the next one
    if out and len(out[-1]) == 1 and not re.search(r"[.!?,]$", out[-1][0]["w"]) and out[-1][0]["p"] == c[0]["p"] and len(c) <= 4:
        out[-1] = out[-1] + c
    else: out.append(c)
res = []
clip_end = PL.N_CLIP / FPS
for i, c in enumerate(out):
    a = c[0]["t"]; e = c[-1]["e"] + 0.30
    if i + 1 < len(out): e = min(e, out[i + 1][0]["t"])
    if a < clip_end <= e: e = clip_end
    text = " ".join(x["w"] for x in c)
    res.append(dict(a=round(a, 3), b=round(e, 3), text=text, lines=cap_lines(text), top=1040 if c[0]["p"] == 0 else 1412))
json.dump(res, open("cues.json", "w"), indent=1)
for r in res: print(f"{r['a']:7.2f} {r['b']:7.2f} {r['top']}  {' / '.join(r['lines'])}")
