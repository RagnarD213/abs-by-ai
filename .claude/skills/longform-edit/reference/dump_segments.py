import json,sys
d=json.load(open(sys.argv[1]))
prev_end=0.0
for s in d["segments"]:
    gap=s["start"]-prev_end
    g=f"  [GAP {gap:.1f}s]" if gap>2.0 else ""
    print(f"{s['start']:8.2f}-{s['end']:8.2f}{g} {s['text'].strip()}")
    prev_end=s["end"]
