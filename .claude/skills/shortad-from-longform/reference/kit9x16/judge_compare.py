#!/usr/bin/env python3
"""Side by side: which defects did the Gemini judge and the session judges each catch on the same watch images?
  python3 judge_compare.py --session <findings*.json ...> --gemini <findings_part*.json ...> [--tol 0.35]
A defect MOMENT is a time (+-tol) with a defect verdict on any image; recall = session moments the Gemini judge
also flagged; extra = Gemini moments no session judge flagged (each one is looked at, not assumed false)."""
import argparse, json


def moments(paths):
    out = []
    for p in paths:
        for e in json.load(open(p)).get("entries", []):
            if e.get("verdict") == "defect":
                out.append((float(e.get("t", 0)), e.get("item"), e.get("image"), e.get("note", "")[:140]))
    out.sort()
    merged = []
    for m in out:
        if merged and m[0] - merged[-1][-1][0] <= 0.35:
            merged[-1].append(m)
        else:
            merged.append([m])
    return merged


ap = argparse.ArgumentParser()
ap.add_argument("--session", nargs="+", required=True)
ap.add_argument("--gemini", nargs="+", required=True)
ap.add_argument("--tol", type=float, default=0.35)
ap.add_argument("--out")
a = ap.parse_args()
S, G = moments(a.session), moments(a.gemini)
hit = lambda m, pool: any(abs(m[0][0] - q[0][0]) <= a.tol for q in pool)
rep = dict(session_moments=len(S), gemini_moments=len(G),
           caught=[(m[0][0], m[0][1]) for m in S if hit(m, G)], missed=[(m[0][0], m[0][1], m[0][2]) for m in S if not hit(m, G)],
           gemini_only=[(m[0][0], m[0][1], m[0][2], m[0][3]) for m in G if not hit(m, S)])
rep["recall"] = f"{len(rep['caught'])}/{len(S)}"
print(json.dumps(rep, indent=1))
if a.out:
    json.dump(rep, open(a.out, "w"), indent=1)
