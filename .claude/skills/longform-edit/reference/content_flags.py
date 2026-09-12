# ⚠ SUPERSEDED BY `.claude/skills/_shared/deliver/gate.py` (2026-09-11, Phase 1 of
#   Handoffs/handoff-20260911-video-quality-engine.md). Its rows are folded into the shared gate,
#   with every bound moved to `_shared/deliver/formats.py` beside the file and the date it was
#   measured on. DO NOT add a check here -- add it there, or it lands in one of six pipelines and
#   the other five keep the bug.
#   ⚠ STILL ON DISK ON PURPOSE: three sessions were mid-build against these scripts when the shared
#   gate landed (ad1-sq, ad2-sq, ad3-vert, ad4-vert, ad5-vert). It is deleted once those deliver,
#   and it still carries rows the shared gate has not absorbed yet -- framing is Phase 2, the watch
#   pass Phase 3. RUN BOTH until those land.
import json,re
from pathlib import Path
TERMS = re.compile(r"(fuck|shit|bullshit|Donald Trump|ex-girlfriend|not smart enough|clavicular|steroid)", re.I)
for slug, src in [("spraytan","C1512"),("zepbound","C1513"),("supplements","C1514")]:
    B = Path(f"/Volumes/Extreme/_edit_work/{slug}")
    edl = json.load(open(B/"edl.json"))["ranges"]
    segs = json.load(open(B/f"{src}.whisper.json"))["segments"]
    offs, acc = [], 0.0
    for r in edl: offs.append(acc); acc += round(r["end"]-r["start"],3)
    def to_out(t):
        for r,o in zip(edl,offs):
            if r["start"] <= t < r["end"]: return o + (t-r["start"])
        return None
    print(f"\n### {slug}")
    for s in segs:
        if not TERMS.search(s["text"]): continue
        o = to_out(s["start"])
        if o is None: continue
        m,sec = divmod(int(o),60)
        beat = next((r["beat"] for r,off in zip(edl,offs) if r["start"]<=s["start"]<r["end"]),"?")
        print(f"  {m:02d}:{sec:02d}  [{beat}]  {s['text'].strip()[:92]}")
