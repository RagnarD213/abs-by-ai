#!/usr/bin/env python3
"""Word counts per section, for matching a script's proportions to the model VSL.

    python3 sections.py transcripts.md "## 1. TestoGreens" "## 2."   -> per-paragraph words + running total
    python3 sections.py --script script.md                           -> spoken words per ### section of our script
Bracketed notes ([B-ROLL ...], [JANUARY VERSION ...]) are not counted as spoken words.
"""
import re, sys
if sys.argv[1] == "--script":
    t = open(sys.argv[2]).read()
    body = t.split("## The script", 1)[-1].split("## Hook takes", 1)[0]
    tot = 0
    for sec in re.split(r'^### ', body, flags=re.M)[1:]:
        title = sec.split('\n', 1)[0]
        n = len(re.sub(r'\[[^\]]*\]', '', sec.split('\n', 1)[1]).split()); tot += n
        print(f"{n:6d}  {title[:60]}")
    print(f"{tot:6d}  total (about {tot/165:.0f} min at Dan's ~165 words a minute)")
else:
    t = open(sys.argv[1]).read()
    part = t.split(sys.argv[2], 1)[1].split(sys.argv[3], 1)[0] if len(sys.argv) > 3 else t
    tot = 0
    for m, s, x in re.findall(r'\*\*\[(\d\d):(\d\d)\]\*\* (.*)', part):
        tot += len(x.split()); print(f"{m}:{s}  {len(x.split()):5d}  {tot:6d}")
