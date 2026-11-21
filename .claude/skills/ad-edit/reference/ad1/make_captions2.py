#!/usr/bin/env python3
"""Word-timed burned captions from the FINAL mixed audio (never estimated windows).
Chunking = canonical /shorts spec: <=4 words, 0.6s gap flush, sentence flush,
punctuation-token merge, no space before punctuation, ABS/AI uppercased.
V1 = J2 (Manrope), V2 = MadMuscles (Arial Bold). 1920x1080, above the CTA bar.
"""
import json, re

wh = json.load(open("final2.whisper.json"))
raw = [w for s in wh["segments"] for w in s.get("words", [])]

# merge punctuation-leading tokens
ws = []
for w in raw:
    t = w["word"]
    if ws and re.match(r"^\s*[.,!?%]", t):
        ws[-1]["word"] = ws[-1]["word"].rstrip() + t.strip()
        ws[-1]["end"] = w["end"]
    else:
        ws.append({"word": t, "start": w["start"], "end": w["end"]})

chunks, cur = [], []
def flush():
    global cur
    if cur: chunks.append(cur); cur = []
for w in ws:
    if cur and (w["start"] - cur[-1]["end"] > 0.6 or len(cur) >= 4):
        flush()
    cur.append(w)
    txt = w["word"].strip()
    if re.search(r"[.?!…]$", txt) or (txt.endswith(",") and len(cur) >= 2):
        flush()
flush()

def t2ass(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = int(t % 60); cs = round(t % 1 * 100)
    if cs == 100: cs = 99
    return "%d:%02d:%02d.%02d" % (h, m, s, cs)

events = []
for i, c in enumerate(chunks):
    start = c[0]["start"]
    end = c[-1]["end"] + 0.15
    if i + 1 < len(chunks): end = min(end, chunks[i + 1][0]["start"])
    if end - start < 0.3: end = start + 0.3
    text = " ".join(w["word"].strip() for w in c)
    text = re.sub(r"\s+([.,!?%])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    text = re.sub(r"\babs\b", "abs", text, flags=re.I)   # Dan: "abs" ALWAYS lowercase
    text = re.sub(r"\bai\b", "AI", text, flags=re.I)
    text = text.replace("gold picture", "goal picture").replace("Gold picture", "Goal picture")
    text = text.replace("lacking body parts", "lagging body parts").replace("lacking", "lagging")
    events.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,%s" % (t2ass(start), t2ass(end), text))

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
%s

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
# V2 MadMuscles: Arial Bold 64, white, black outline
S2 = "Style: Cap,Arial,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H7F000000,-1,0,0,0,100,100,0,0,1,4,2,2,120,120,116,1"
# V1 J2: Manrope 58, white, near-black J2 outline
S1 = "Style: Cap,Manrope,58,&H00FFFFFF,&H00FFFFFF,&H000B0E0D,&H7F000000,-1,0,0,0,100,100,0,0,1,4,2,2,120,120,116,1"
open("cap_v1.ass", "w").write(HEADER % S1 + "\n".join(events) + "\n")
open("cap_v2.ass", "w").write(HEADER % S2 + "\n".join(events) + "\n")
print(len(chunks), "cues,", len(ws), "words; last cue ends", t2ass(chunks[-1][-1]["end"] + 0.15))
