#!/usr/bin/env python3
"""Find runs of 6+ words our script shares with a model VSL transcript (copied lines, not just copied structure).

    python3 copycheck.py <our-script.md> <transcripts.md> "<model start heading>" "<model end heading>"

Prints each shared run with its position in minutes (at Dan's ~165 words a minute). Runs of 8+ words are flagged:
rewrite those beats in our own words, especially inside the first 5 minutes. Stock phrases ("no questions asked")
can stay. Bracketed notes in our script are ignored.
"""
import re, sys
ours, tx, start, end = sys.argv[1:5]
model = open(tx).read().split(start, 1)[1].split(end, 1)[0].lower()
t = open(ours).read().lower()
body = t.split("## the script", 1)[-1].split("## hook takes", 1)[0]
body = re.sub(r'\[[^\]]*\]', '', body)
def words(s): return re.findall(r"[a-z']+", s)
mw = words(model); g = set(tuple(mw[i:i+6]) for i in range(len(mw) - 5))
w = words(body); i = 0; n8 = 0
while i < len(w) - 5:
    if tuple(w[i:i+6]) in g:
        j = i + 6
        while j < len(w) and tuple(w[j-5:j+1]) in g: j += 1
        run = " ".join(w[i:j]); flag = "  <== 8+ words" if j - i >= 8 else ""
        n8 += bool(flag); print(f"{i/165:5.1f} min  {run}{flag}"); i = j
    else: i += 1
print(f"{n8} runs of 8+ words")
