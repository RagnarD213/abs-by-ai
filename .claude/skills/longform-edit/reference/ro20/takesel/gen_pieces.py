"""Turn plan.RANGES into the PIECES list of recipe/edl.py: phrase anchors (first / last words as medium.en heard them),
a roll-local hint, the beat text and the why. Checks that find() resolves every phrase to the planned words."""
import json, re, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/takesel"); sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/recipe")
from takeplan import RANGES
import edl
W = edl.WORDS; norm = edl.norm
rows = []
for r in RANGES:
    rid, a, b, why = r[:4]; fo = r[4] if len(r) > 4 else None; fi = r[5] if len(r) > 5 else None
    idx = [k for k, w in enumerate(W) if w["start"] >= a-0.06 and w["end"] <= b+0.06 and norm(w["word"])]
    i0, i1 = idx[0], idx[-1]
    assert -0.07 <= W[i0]["start"]-a <= 1.1 and abs(W[i1]["end"]-b) <= 0.07, (rid, W[i0], W[i1])   # a first word may sit later than planned: retime_first.py moves it to the lav onset
    hint = round(W[i0]["start"], 1)
    n = min(6, len(idx)); p_in = " ".join(W[k]["word"].strip() for k in idx[:n])
    while edl.find("C1511", p_in, hint)[0] != i0: raise SystemExit(f"{rid}: first phrase resolves elsewhere")
    m = min(4, len(idx))
    while True:
        p_out = " ".join(W[k]["word"].strip() for k in idx[-m:])
        if norm(p_in).endswith(norm(p_out)): j1 = edl.find("C1511", p_in, hint)[1]
        else: j1 = edl.find("C1511", p_out, W[i0]["start"])[1]
        if j1 == i1: break
        m += 1
        if m > len(idx): raise SystemExit(f"{rid}: last phrase never resolves")
    txt = " ".join(W[k]["word"].strip() for k in range(i0, i1+1) if norm(W[k]["word"]) or W[k]["word"].strip() == "%").replace(" %", "%")
    t = txt.split()
    beat = txt if len(t) <= 34 else " ".join(t[:16]) + " ... " + " ".join(t[-12:])
    row = [rid, "C1511", p_in, p_out, hint, beat, why]
    if fo is not None or fi is not None: row += [fo, fi]
    rows.append(row)
def lit(x): return json.dumps(x, ensure_ascii=False) if isinstance(x, str) else ("None" if x is None else repr(x))
body = "PIECES = [\n" + "".join(" (" + ", ".join(lit(x) for x in row[:5]) + ",\n  " + lit(row[5]) + ",\n  " + lit(row[6]) + ("" if len(row) == 7 else ", " + ", ".join(lit(x) for x in row[7:])) + "),\n" for row in rows) + "]\n"
p = "/Volumes/Extreme/_edit_work/ro20/recipe/edl.py"; s = open(p).read()
a = s.index("PIECES = ["); b = s.index("def norm(s)")
s = s[:a] + body + s[b:]
open(p, "w").write(s); print(len(rows), "pieces written")
