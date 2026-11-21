#!/usr/bin/env python3
"""Phrase-repeat shingle scan over the v3 KEPT timeline (source words mapped
through edl.json). Longer window than QC's +/-30s because a cut-down is hunting
RESTATEMENTS inside a section, not stutters: 3-6 word shingles, +/-120s window.
Anaphora is deliberate; re-statements of the same claim are the cut targets."""
import json, sys
from pathlib import Path

BASE = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/invest-health")
edl = json.load(open(BASE / "edit" / "edl.json"))
ranges = edl["ranges"]

STOP = set("the a an and or but so it is was to of in on for that this i you we they he she "
           "if then than at as be been are am my your our their his her its me them us".split())

words = []
for s in json.load(open(BASE / "C1511.whisper.json"))["segments"]:
    for w in s.get("words", []):
        t = w["word"].strip().lower().strip(".,!?\"'")
        if not t: continue
        mid = 0.5 * (w["start"] + w["end"])
        if any(r["start"] <= mid <= r["end"] for r in ranges):
            words.append((t, w["start"]))

WIN = float(sys.argv[1]) if len(sys.argv) > 1 else 120.0
hits = {}
for N in (6, 5, 4, 3):
    seen = {}
    for i in range(len(words) - N):
        toks = [w for w, _ in words[i:i+N]]
        if all(t in STOP for t in toks):      # pure function-word shingles are noise
            continue
        if sum(1 for t in toks if t not in STOP) < 2:
            continue
        key = " ".join(toks)
        t = words[i][1]
        for prev in seen.get(key, []):
            if 0 < t - prev <= WIN:
                hits.setdefault(key, set()).add((round(prev, 1), round(t, 1)))
        seen.setdefault(key, []).append(t)

keys = sorted(hits, key=lambda k: -len(k.split()))
final = []
for k in keys:
    if not any(k in kk for kk in (x[0] for x in final)):
        final.append((k, sorted(hits[k])))
final.sort(key=lambda x: x[1][0][0])
for k, pairs in final:
    print(f"{pairs[0][0]:8.1f} -> {pairs[0][1]:8.1f}  ({len(k.split())}w) {k!r}"
          + (f"  +{len(pairs)-1} more" if len(pairs) > 1 else ""))
print(f"\n{len(final)} phrase repeats (window {WIN:.0f}s)")
