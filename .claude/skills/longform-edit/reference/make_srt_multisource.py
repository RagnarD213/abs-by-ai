#!/usr/bin/env python3
"""SRT timed to the FINAL EDIT: maps every word through the EDL.
    render_t = beat_offset + (word_t - beat_start)
offsets accumulate from the SAME 3-dp-rounded durations the build used, so the
mapping cannot drift; words outside a kept beat are dropped.
usage: make_srt.py <slug> <SRC> <out.srt>"""
import json, sys
from pathlib import Path

slug, outname = sys.argv[1], sys.argv[2]
BASE = Path(f"/Volumes/Extreme/_edit_work/{slug}")
edl = json.load(open(BASE / "edl.json"))
# MULTI-SOURCE: words are per roll, so a range must only ever pull from its own
# roll -- identical timecodes exist in all four rolls.
WORDS = {}
for name in edl["sources"]:
    WORDS[name] = [w for sg in json.load(open(BASE / f"{name}.whisper.json"))["segments"]
                   for w in sg.get("words", [])]

mapped, off = [], 0.0
for r in edl["ranges"]:
    a, b = r["start"], r["end"]; d = round(b - a, 3)
    for w in WORDS[r["source"]]:
        if w["start"] >= a and w["end"] <= b:
            t0 = round(off + (w["start"] - a), 3)
            t1 = round(off + (min(w["end"], b) - a), 3)
            txt = w["word"].strip()
            if txt: mapped.append((t0, max(t1, t0 + 0.06), txt))
    off = round(off + d, 3)
mapped.sort()

MAXLINE, MAXCHARS, MAXDUR, MINDUR, PAUSE = 45, 84, 5.5, 0.5, 0.45
cues, cur = [], []
for i, w in enumerate(mapped):
    # close BEFORE appending, or a cue overruns MAXCHARS by a whole word and the
    # balanced wrap then has to put 48+ chars on each line
    if cur and len(" ".join(x[2] for x in cur)) + 1 + len(w[2]) > MAXCHARS:
        cues.append(cur); cur = []
    cur.append(w)
    text = " ".join(x[2] for x in cur)
    nxt = mapped[i+1] if i+1 < len(mapped) else None
    gap = (nxt[0] - w[1]) if nxt else 99
    ends_sentence = w[2].endswith(('.', '!', '?'))
    if (len(text) >= MAXCHARS or (w[1]-cur[0][0]) >= MAXDUR or gap >= PAUSE
            or ends_sentence or nxt is None):
        cues.append(cur); cur = []
if cur: cues.append(cur)

def join_words(ws):
    """Whisper splits tokens like "y'all" -> ["y","'all"] and "0.8" -> ["0",".8"].
    A naive " ".join() renders those as "y 'all" / "0 .8". Never put a space
    before a token that opens with punctuation."""
    out = ""
    for x in ws:
        if out and not x[:1] in "'.,%)-\u2019": out += " "
        out += x
    return out

# Whisper's own spelling of two brand terms is wrong on the page even though the
# audio is right: it writes "Abwheel" as one word and lowercases the domain.
# Fix at the JOINED-cue level, after join_words, so token splits cannot hide them.
SPELL = [("Abwheel", "ab wheel"), ("abwheel", "ab wheel"),
         ("absbyai.com", "AbsByAI.com"), ("Absbyai.com", "AbsByAI.com")]
def respell(t):
    for a, b in SPELL: t = t.replace(a, b)
    return t

def wrap(t):
    """Balanced 2-line wrap: split at the word boundary nearest the midpoint, so
    neither line runs long. A greedy first-line fill leaves the remainder
    uncapped and produces 60+ char second lines."""
    if len(t) <= MAXLINE: return t
    ws = t.split()
    best, bi = None, 1
    for i in range(1, len(ws)):
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        cost = abs(len(a) - len(b)) + 400 * (max(len(a), len(b)) > MAXLINE)
        if best is None or cost < best: best, bi = cost, i
    return " ".join(ws[:bi]) + "\n" + " ".join(ws[bi:])

def ts(s):
    ms = int(round(s*1000)); h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); sec, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

total = round(sum(round(r["end"]-r["start"], 3) for r in edl["ranges"]), 3)
lines, prev_end, n = [], 0.0, 0
for j, c in enumerate(cues):
    a = max(c[0][0], prev_end + 0.01); b = max(c[-1][1], a + MINDUR)
    if j + 1 < len(cues): b = min(b, cues[j+1][0][0] - 0.01)
    else: b = max(b, total)          # extend final cue to true container duration
    if b <= a: b = a + MINDUR
    prev_end = b; n += 1
    lines += [str(n), f"{ts(a)} --> {ts(b)}", wrap(respell(join_words([x[2] for x in c]))), ""]
open(BASE / "roughcuts" / outname, "w").write("\n".join(lines))
print(f"{n} cues -> {BASE/'roughcuts'/outname}  (plan {total:.2f}s)")
