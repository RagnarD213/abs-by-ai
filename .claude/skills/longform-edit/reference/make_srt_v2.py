#!/usr/bin/env python3
"""SRT timed to the FINAL EDIT: map Whisper source-word timestamps through
edl.json. Words on the cutting-room floor are dropped. Longform format:
max 2 lines x <=45 chars, break on pauses >=0.45s / sentence ends / 5.5s,
min 0.5s per cue, no overlaps, final cue extended to container duration."""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
edl = json.load(open(HERE / "edl.json"))
ranges = edl["ranges"]

offs = []; acc = 0.0
for r in ranges:
    offs.append(acc); acc += round(r["end"] - r["start"], 3)
TOTAL = acc

words = []
for s in json.load(open(BASE / "C1511.whisper.json"))["segments"]:
    for w in s.get("words", []):
        t = w["word"].strip()
        if t:
            words.append({"text": t, "start": w["start"], "end": w["end"]})

def to_render(t):
    for r, o in zip(ranges, offs):
        if r["start"] - 0.02 <= t <= r["end"] + 0.02:
            return o + max(0.0, t - r["start"])
    return None

mapped = []
for w in words:
    a = to_render(w["start"]); b = to_render(w["end"])
    if a is None:
        continue
    if b is None or b < a:
        b = a + 0.25
    mapped.append({"t": w["text"], "a": a, "b": b})

MAXCHARS = 90  # 2 lines x 45
cues = []; cur = []
def join_tokens(toks):
    # Whisper splits ".com", ",000", "%" into their own tokens — rejoin them
    out = ""
    for t in toks:
        if out and (t[0] in ".,%" or t.startswith("'")):
            out += t
        else:
            out += (" " if out else "") + t
    return out

def flush():
    global cur
    if not cur:
        return
    txt = join_tokens([x["t"] for x in cur]).strip()
    a = cur[0]["a"]; b = max(cur[-1]["b"], a + 0.8)
    cues.append((a, b, txt)); cur = []
for w in mapped:
    if cur:
        gap = w["a"] - cur[-1]["b"]
        cand = len(" ".join(x["t"] for x in cur)) + 1 + len(w["t"])
        if gap >= 0.45 or cand > MAXCHARS or (w["a"] - cur[0]["a"]) > 5.5 or cur[-1]["t"].endswith((".", "?", "!")):
            flush()
    cur.append(w)
flush()

# container duration for the tail extension
final_video = sys.argv[1] if len(sys.argv) > 1 else None
container = TOTAL
if final_video:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", final_video], capture_output=True, text=True)
    try:
        container = float(out.stdout.strip())
    except ValueError:
        pass

out_cues = []
for i, (a, b, t) in enumerate(cues):
    if i + 1 < len(cues):
        b = min(b, cues[i + 1][0] - 0.04)
    if b - a < 0.5:
        b = a + 0.5
        if i + 1 < len(cues):
            b = min(b, cues[i + 1][0] - 0.02)
    if b > a:
        out_cues.append([a, b, t])
# extend the final cue to the true container end (summed rounded durations come up short)
if out_cues:
    out_cues[-1][1] = max(out_cues[-1][1], min(container, TOTAL + (container - TOTAL)))

def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = int(x % 60); ms = int(round((x - int(x)) * 1000))
    if ms == 1000: s += 1; ms = 0
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

def wrap(t, width=45):
    if len(t) <= width:
        return t
    ws = t.split(); l1 = ""
    for i, w in enumerate(ws):
        if len(l1) + len(w) + 1 > width and l1:
            return l1 + "\n" + " ".join(ws[i:])
        l1 = (l1 + " " + w).strip()
    return t

dst = BASE / "roughcuts" / "INVEST_HEALTH_v1.srt"
with open(dst, "w") as f:
    for i, (a, b, t) in enumerate(out_cues, 1):
        f.write("%d\n%s --> %s\n%s\n\n" % (i, ts(a), ts(b), wrap(t)))
print("cues:", len(out_cues), "->", dst)
print("last cue ends %.2fs (EDL total %.2fs, container %.2fs)" % (out_cues[-1][1], TOTAL, container))
print("words kept %d of %d" % (len(mapped), len(words)))
