import json,re
from pathlib import Path
TERMS = re.compile(r"(fuck|shit|bullshit|Donald Trump|ex-girlfriend|not smart enough|clavicular|steroid)", re.I)
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
    for s in segs:
        if not TERMS.search(s["text"]): continue
        o = to_out(s["start"])
        if o is None: continue
        m,sec = divmod(int(o),60)
        beat = next((r["beat"] for r,off in zip(edl,offs) if r["start"]<=s["start"]<r["end"]),"?")
        print(f"  {m:02d}:{sec:02d}  [{beat}]  {s['text'].strip()[:92]}")
