#!/usr/bin/env python3
"""REV 3 -- patch the C1650 transcript over the hidden restart (ad-edit lesson 98).

The chunked small.en pass stitched "Now, I've been out of shape, -- I've been out of shape, and
now at 40" into ONE stretched token (`and` 48.38-51.20, 2.8 s on the roll), so orphan_scan.py saw
no uncovered energy and Dan heard the repeat at 0:32. An isolated medium.en pass over roll 45-54 s
(condition_on_previous_text=False) reads both attempts; those word times go in here so every later
stage (tight.py's word map, beats.py's phrase anchors, captions.py, qc.py's fidelity diff) sees the
truth. tight.py then removes the first attempt (MANUAL_CUTS) and drops the words inside it.

The original is kept beside it as tx/C1650.whisper.orig.json; re-running is idempotent.
"""
import json, os, shutil
HERE=os.path.dirname(os.path.abspath(__file__))
P=f"{HERE}/tx/C1650.whisper.json"; ORIG=f"{HERE}/tx/C1650.whisper.orig.json"
if not os.path.exists(ORIG): shutil.copy(P,ORIG)
d=json.load(open(ORIG))
LO,HI=47.0,51.85          # roll seconds: replace every original token that STARTS in [LO,HI)
                          # (the original "40" starts 51.60 and must go; the original "I" starts 51.90 and must stay)
# isolated medium.en pass, roll time. "Now" keeps the chunked pass's onset (47.04: the 5 ms envelope
# rises at 47.06; the isolated pass timed it 0.18 s late). The restart's "I've" onset is the measured
# envelope rise at 50.09 (Whisper starts fricatives early, lesson 20).
NEW=[(47.04,47.36," Now,"),
     (47.60,47.78," I've"),(47.78,47.88," been"),(47.88,48.04," out"),(48.04,48.18," of"),(48.18,48.46," shape."),
     (50.08,50.34," I've"),(50.34,50.44," been"),(50.44,50.60," out"),(50.60,50.78," of"),(50.78,50.98," shape"),
     (50.98,51.24," and"),(51.24,51.48," now"),(51.48,51.66," at"),(51.66,51.94," 40,")]
flat=[w for s in d["segments"] for w in s["words"]]
removed=[w for w in flat if LO<=w["start"]<HI]
kept=[w for w in flat if not (LO<=w["start"]<HI)]
kept+=[{"word":t,"start":a,"end":b} for a,b,t in NEW]
kept.sort(key=lambda w:w["start"])
# regroup into the original segment boundaries
bounds=[s["start"] for s in d["segments"]]
segs=[[] for _ in bounds]
for w in kept:
    i=max(k for k,b in enumerate(bounds) if b<=w["start"]+1e-6) if any(b<=w["start"]+1e-6 for b in bounds) else 0
    segs[i].append(w)
out=[]
for ws in segs:
    if not ws: continue
    out.append({"start":ws[0]["start"],"end":ws[-1]["end"],"text":"".join(w["word"] for w in ws),"words":ws})
json.dump({"segments":out},open(P,"w"))
print("removed:",[ (w["start"],w["word"]) for w in removed])
print("inserted:",[(a,t) for a,b,t in NEW])
print(f"words {len(flat)} -> {sum(len(s['words']) for s in out)}   segments {len(d['segments'])} -> {len(out)}")
