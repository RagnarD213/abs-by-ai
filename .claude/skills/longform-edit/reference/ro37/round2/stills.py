"""RO-37 round 2: one still per background segment (the scene plan at a glance), through the real assembler, graphics off
(they have their own context clips). The frame is the segment's middle, moved off any lower third so the still shows the
segment's own placement.  python3 stills.py [BG01,BG05]  -> round2/review/scenes/<BGid>.jpg + scenes.json"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
OUT = f"{r2.W2}/review/scenes"; os.makedirs(OUT, exist_ok=True)
only = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None
plan = json.load(open(f"{r2.W2}/bg_plan.json"))["segments"]; shots = r2.final_shots(plan); res = []
for g in plan:
    f0, f1 = r2.fr(g["t0"]), r2.fr(g["t1"])
    cand = [s for s in shots if s["out_f1"] > f0 and s["out_f0"] < f1 and not s["covered"]]
    pick = sorted(cand, key=lambda s: (bool(s["lt"]), -(min(s["out_f1"], f1) - max(s["out_f0"], f0))))[0]
    a, b = max(pick["out_f0"], f0), min(pick["out_f1"], f1)
    k0 = r2.src_index(pick["src0"]) + (a - pick["out_f0"])
    geo = sorted(r2.geo_frames([pick]).get(pick["roll"], []))  # a frame whose matte exists (the sparse pass; none for the close-up)
    mid = (a + b) // 2; q = min((k - r2.src_index(pick["src0"]) + pick["out_f0"] for k in geo if a <= k - r2.src_index(pick["src0"]) + pick["out_f0"] < b),
                                key=lambda x: abs(x - mid), default=mid)
    out = f"{OUT}/{g['id']}.jpg"
    if (not only and not os.path.exists(out)) or (only and g["id"] in only):
        subprocess.run(["python3", "assemble.py", out, "--frame", str(q), "--no-graphics"], check=True, capture_output=True)
    res.append(dict(id=g["id"], frame=q, t=round(q / r2.FPS, 2), type=g["type"], why=g["why"], t0=g["t0"], t1=g["t1"],
                    clip=g.get("clip", {}).get("id"), lines=g.get("lines"), still=f"scenes/{g['id']}.jpg"))
    print(g["id"], g["type"], round(q / r2.FPS, 2), flush=True)
json.dump(res, open(f"{OUT}/scenes.json", "w"), indent=1)
