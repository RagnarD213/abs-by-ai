#!/usr/bin/env python3
"""Find every 'on screen / I'm going to show you' moment and map it to FINAL-EDIT time."""
import json,re,sys
from pathlib import Path
PAT = re.compile(r"(on (the )?screen|on your screen|show you (a |the |some |each |what)|"
                 r"here on the (left|right)|you're seeing|like you're seeing|showing you a picture)", re.I)
for slug, src in [("spraytan","C1512"),("zepbound","C1513"),("supplements","C1514")]:
    B = Path(f"/Volumes/Seagate 4TB/_edit_work/{slug}")
    edl = json.load(open(B/"edl.json"))["ranges"]
    segs = json.load(open(B/f"{src}.whisper.json"))["segments"]
    offs, acc = [], 0.0
    for r in edl: offs.append(acc); acc += round(r["end"]-r["start"],3)
    def to_out(t):
        for r,o in zip(edl,offs):
            if r["start"] <= t < r["end"]: return o + (t-r["start"])
        return None
    print(f"\n### {slug}")
    seen=set()
    for s in segs:
        if not PAT.search(s["text"]): continue
        o = to_out(s["start"])
        if o is None: continue
        k = int(o//8)
        if k in seen: continue
        seen.add(k)
        m,sec = divmod(int(o), 60)
        print(f"  {m:02d}:{sec:02d}  {s['text'].strip()[:96]}")
