"""RO-03: plan -> plan_resolved.json (film seconds). Phrases resolve on words_out.json; ("hold", n, s) on the shots."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan as P
W = P.W; FPS = 30000/1001
WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]; SH = json.load(open(f"{W}/shots.json"))
NUM = {"twenty": "20", "thirty": "30", "one": "1", "two": "2", "three": "3"}
def norm(s):
    s = re.sub(r"[^a-z0-9]", "", s.lower()); return NUM.get(s, s)
TOK = [norm(w["w"]) for w in WO]
def find(phrase, after=0.0):
    p = [norm(x) for x in re.split(r"[\s\-]+", phrase) if norm(x)]
    for i in range(len(TOK)):
        if WO[i]["t0"] < after-0.01: continue
        if all(i+k < len(TOK) and (TOK[i+k] == q or (len(q) > 3 and TOK[i+k].startswith(q[:4]))) for k, q in enumerate(p)): return i, i+len(p)-1
    raise SystemExit(f"phrase not found after {after:.2f}: {phrase!r}")
def src_out(piece, src):
    for s in SH:
        if s["piece"] == piece and s["src_f0"]/FPS-1e-3 <= src <= s["src_f1"]/FPS+1e-3: return s["out_f0"]/FPS+src-s["src_f0"]/FPS
    raise SystemExit(f"{piece} {src} not in a shot")
def shot(i): return next(s for s in SH if s["id"] == i)
HOLDS = [round(src_out(p, P.HOLD_SRC), 3) for p in P.SETS]; BEEPS = [round(src_out(p, P.BEEP_SRC), 3) for p in P.SETS]
def tt(x):
    if isinstance(x, (tuple, list)) and x[0] == "hold": return round(HOLDS[x[1]-1]+x[2], 3)
    return x
def resolve():
    out = []
    for it in P.PLAN:
        r = dict(it)
        if "t0" in it: t0 = tt(it["t0"])
        elif it.get("start_shot"): t0 = shot(it["start_shot"])["out_f0"]/FPS+0.0005
        else: t0 = WO[find(it["start"])[0]]["t0"]
        if "t1" in it: t1 = tt(it["t1"])
        elif it.get("end_shot"): t1 = shot(it["end_shot"])["out_f1"]/FPS
        else:
            a, k = find(it["end"], t0); t1 = WO[a]["t0"]+it.get("lead", 0) if it.get("end_at_start") else WO[k]["t1"]+it.get("tail", 0.25)
        r["t0"] = round(t0, 4); r["t1"] = round(t1, 4)
        if r.get("parts"): r["parts"] = [[p, tt(ph)] for p, ph in r["parts"]]
        if it["kind"] == "work":
            r["holds"] = HOLDS; r["beeps"] = BEEPS; r["secs"] = P.SECS
        out.append(r)
    out.sort(key=lambda r: r["t0"]); return out
if __name__ == "__main__":
    R = resolve(); json.dump(R, open(f"{W}/plan_resolved.json", "w"), indent=1)
    for r in R: print(f"{r['id']:4s} {r['kind']:6s} {r['t0']:7.2f} - {r['t1']:7.2f}")
    print("holds", HOLDS, "beeps", BEEPS, "rests", [round(h-b, 3) for h, b in zip(HOLDS[1:], BEEPS)])
    json.dump(dict(holds=HOLDS, beeps=BEEPS, flashes=[shot(i)["out_f0"] for i in P.FLASH_INTO]), open(f"{W}/marks.json", "w"))
