#!/usr/bin/env python3
"""SRT timed to the FINAL REV1 EDIT.

Two fixes over make_srt_generic.py, both real defects inherited from rev 0:

1. STABLE ORDER. Whisper emits ZERO-LENGTH WORD CLUSTERS - here, "the amount of
   money you get to spend on the spray tan" is thirteen words all stamped
   1257.98. `mapped.sort()` sorts (t0, t1, text) tuples, so a tie breaks
   ALPHABETICALLY and the caption shipped as "is a amount get money of on spend
   spray the to you is tan that". Sorting on (t0, original index) keeps reading
   order. Same defect at 6:29 and 13:49.
2. MIDPOINT MAPPING (Step 3 rule 9): a word belongs to a kept range when its
   MIDPOINT is inside it, so a word straddling a new cut is dropped rather than
   captioned over speech that no longer exists.

Plus the brand/drug/name fix table applied to the JOINED cue text, with a hard
assertion that no forbidden string reaches the file - Whisper renders "GLP-1"
as "GOP1", and shipping an invented political term is not recoverable.
usage: make_srt_spraytan.py <slug> <SRC> <out.srt>
"""
import json, re, sys
from pathlib import Path

slug, src, outname = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = Path(f"/Volumes/Extreme/_edit_work/{slug}")
edl = json.load(open(BASE / "edl.json"))
words = [w for s in json.load(open(BASE / f"{src}.whisper.json"))["segments"]
         for w in s.get("words", [])]

# ---- 3. DROP HALLUCINATED ZERO-LENGTH CLUMPS -----------------------------
# Step 3 trap 1: a CLUSTER of zero-length word timestamps is text Whisper
# invented. Two of them shipped in the rev-0 SRT as whole fabricated sentences.
# Re-transcribing the source audio proved both are absent:
#   642.76  "you're going to be getting a shower before you get into bed at
#            night."  -> audio: "In that first shower you can't use any soap"
#  1257.98  "the amount of money you get to spend on a spray tan is"
#            -> audio: "Another drawback of a spray tan is that for certain
#                       people, such as myself..."
# A clump is >=3 consecutive words that each last <=0.05s and together span
# <0.10s. The word AFTER a clump is dropped too when it starts at the clump's
# own timestamp (that is "night."), and the word BEFORE when it is itself a
# <=0.05s fragment ending there (that is "you're"). Isolated zero-length words
# are kept - those are ordinary timestamp glitches on real speech.
def hallucinated(ws):
    bad, i, n = set(), 0, len(ws)
    while i < n:
        if ws[i]["end"] - ws[i]["start"] > 0.05: i += 1; continue
        j = i
        while (j + 1 < n and ws[j+1]["end"] - ws[j+1]["start"] <= 0.05
               and ws[j+1]["start"] - ws[i]["start"] < 0.10): j += 1
        if j - i + 1 >= 3:
            bad.update(range(i, j + 1))
            # the word AFTER a clump belongs to the same hallucination when it
            # carries the clump's DOMINANT timestamp ("night." at 642.76, where
            # 12 of the 13 clump words also sit). Comparing against the clump's
            # first or last member instead gets it wrong both ways: "you're"
            # (0.04s) opens the 642.76 clump at 642.72, and the 1257.98 clump
            # ENDS at 1258.02 where the perfectly real word "that" begins.
            from collections import Counter
            mode = Counter(round(ws[k]["start"], 3) for k in range(i, j + 1)).most_common(1)[0][0]
            if j + 1 < n and abs(ws[j+1]["start"] - mode) < 1e-6: bad.add(j + 1)
            if i > 0 and ws[i-1]["end"] - ws[i-1]["start"] <= 0.05 \
               and abs(ws[i-1]["end"] - ws[i]["start"]) < 1e-6: bad.add(i - 1)
        i = j + 1
    return bad
DROP = hallucinated(words)
print(f"dropping {len(DROP)} hallucinated words in zero-length clumps: "
      + " ".join(words[i]["word"].strip() for i in sorted(DROP))[:200])

mapped, off = [], 0.0
for r in edl["ranges"]:
    a, b = r["start"], r["end"]; d = round(b - a, 3)
    for idx, w in enumerate(words):
        if idx in DROP: continue
        mid = (w["start"] + w["end"]) / 2
        if a <= mid < b:
            t0 = round(off + (max(w["start"], a) - a), 3)
            t1 = round(off + (min(w["end"], b) - a), 3)
            txt = w["word"].strip()
            if txt: mapped.append((t0, idx, max(t1, t0 + 0.06), txt))
    off = round(off + d, 3)
mapped.sort(key=lambda x: (x[0], x[1]))          # tie -> READING ORDER, never text
mapped = [(t0, t1, txt) for t0, _, t1, txt in mapped]

MAXLINE, MAXCHARS, MAXDUR, MINDUR, PAUSE = 45, 84, 5.5, 0.5, 0.45
cues, cur = [], []
for i, w in enumerate(mapped):
    if cur and len(" ".join(x[2] for x in cur)) + 1 + len(w[2]) > MAXCHARS:
        cues.append(cur); cur = []
    cur.append(w)
    text = " ".join(x[2] for x in cur)
    nxt = mapped[i+1] if i+1 < len(mapped) else None
    gap = (nxt[0] - w[1]) if nxt else 99
    if (len(text) >= MAXCHARS or (w[1]-cur[0][0]) >= MAXDUR or gap >= PAUSE
            or w[2].endswith(('.', '!', '?')) or nxt is None):
        cues.append(cur); cur = []
if cur: cues.append(cur)

def join_words(ws):
    """Whisper splits "y'all" -> ["y","'all"] and "0.8" -> ["0",".8"]; a naive
    join renders "y 'all" and "0 .8"."""
    out = ""
    for x in ws:
        if out and not x[:1] in "'.,%)-’": out += " "
        out += x
    return out

# Applied to the JOINED cue text so multi-token names are caught. Every entry is
# a name Whisper got wrong, not a rewrite of what Dan said.
FIXES = [
 (r"\bGOP\s*-?\s*1\b", "GLP-1"), (r"\bGOP1\b", "GLP-1"), (r"\bGLP one\b", "GLP-1"),
 (r"\bGOP\b", "GLP-1"),
 (r"\bBrian Johnson\b", "Bryan Johnson"),
 (r"\bads by AI\b", "Abs By AI"), (r"\bAds by AI\b", "Abs By AI"),
 (r"\babsbyai\s*\.\s*com\b", "AbsByAI.com"), (r"\bAbsbyai\.com\b", "AbsByAI.com"),
 (r"\bchat GPT\b", "ChatGPT"), (r"\bChat GPT\b", "ChatGPT"),
 (r"\bsix\s*-\s*pack\b", "six-pack"),
 (r"\bexfoliating face clubs\b", "exfoliating face scrubs"),
 (r"\ba natural tank and look healthy\b", "a natural tan can look healthy"),
 (r"\bself apply\b", "self-apply"),
]
FORBIDDEN = ["GOP", "GLP one", "ads by AI", "Brian Johnson", "chat GPT"]
def fix_text(t):
    for pat, rep in FIXES: t = re.sub(pat, rep, t)
    return t

def wrap(t):
    """Balanced 2-line wrap: split nearest the MIDPOINT so neither line runs long."""
    if len(t) <= MAXLINE: return t
    ws = t.split(); best, bi = None, 1
    for i in range(1, len(ws)):
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        cost = abs(len(a) - len(b)) + 400 * (max(len(a), len(b)) > MAXLINE)
        if best is None or cost < best: best, bi = cost, i
    return " ".join(ws[:bi]) + "\n" + " ".join(ws[bi:])

def ts(s):
    ms = int(round(s*1000)); h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); sec, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

total = round(sum(round(r["end"]-r["start"], 3) for r in edl["ranges"]), 3)
lines, prev_end, n, worst = [], 0.0, 0, 0
for j, c in enumerate(cues):
    a = max(c[0][0], prev_end + 0.01); b = max(c[-1][1], a + MINDUR)
    if j + 1 < len(cues): b = min(b, cues[j+1][0][0] - 0.01)
    else: b = max(b, total)
    if b <= a: b = a + MINDUR
    prev_end = b; n += 1
    body = wrap(fix_text(join_words([x[2] for x in c])))
    worst = max(worst, max(len(l) for l in body.split("\n")))
    lines += [str(n), f"{ts(a)} --> {ts(b)}", body, ""]
text = "\n".join(lines)
bad = [f for f in FORBIDDEN if re.search(rf"\b{re.escape(f)}\b", text)]
assert not bad, f"forbidden strings reached the SRT: {bad}"
assert "\n\n\n" not in text
# a cue block is index + timestamp + 1-2 text lines, so >4 means a 3-line caption
three = [b for b in text.strip().split("\n\n") if len(b.split("\n")) > 4]
assert not three, f"{len(three)} cues have 3+ text lines"
open(BASE / "roughcuts" / outname, "w").write(text)
print(f"{n} cues -> {outname}  (plan {total:.2f}s)  worst line {worst} chars")
