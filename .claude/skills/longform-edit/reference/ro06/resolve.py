"""Resolve plan phrases to output times (words_out.json). Items are searched in plan order, each from the previous item's start.
Full-screen items (clip, scene) snap to a shot join that falls just before them and never leave a presenter island < 0.6 s."""
import json, re, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro06/recipe")
from plan import PLAN
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001
WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
NUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "ten": "10", "fifty": "50", "fifteen": "15", "thirty": "30"}
def norm(s):
    s = re.sub(r"[^a-z0-9]", "", s.lower()); return NUM.get(s, s)
TOK = [norm(w["w"]) for w in WO]
def find(phrase, after=0.0):
    p = [norm(x) for x in re.split(r"[\s\-]+", phrase) if norm(x)]
    for i in range(len(TOK)):
        if WO[i]["t0"] < after-0.01: continue
        j = i; ok = True
        for q in p:
            while j < len(TOK) and TOK[j] == "": j += 1
            if j >= len(TOK) or not (TOK[j] == q or (len(q) > 3 and TOK[j].startswith(q[:4]))): ok = False; break
            j += 1
        if ok: return i, j-1
    raise SystemExit(f"phrase not found after {after:.2f}: {phrase!r}")
def resolve():
    S = json.load(open(f"{W}/shots.json")); joins = [s["out_f0"]/FPS for s in S]
    out = []; after = 0.0
    for it in PLAN:
        i, _ = find(it["start"], after); t0 = WO[i]["t0"]
        a, k = find(it["end"], t0); t1 = WO[k]["t1"] + it.get("tail", 0.25)
        r = dict(it); r["t0"] = round(t0, 3); r["t1"] = round(t1, 3); out.append(r); after = t0
    out.sort(key=lambda r: r["t0"])
    FULL = ("clip", "scene")
    for r in out:
        if r["kind"] in FULL:
            if r.get("cover_shot"):                                  # the card hides a whole inserted take: both edges on its joins
                sh = next(s for s in S if s["out_f0"]/FPS <= r["t0"]+0.3 < s["out_f1"]/FPS)
                r["t0"] = round(sh["out_f0"]/FPS+0.0005, 4); r["t1"] = round(sh["out_f1"]/FPS+0.0005 + r.get("extend", 0), 4); continue   # extend: hold the card past the take it hides (round 5: a price needs reading time)
            j = [x for x in joins if r["t0"]-0.85 <= x < r["t0"]]
            if j: r["t0"] = round(max(j)+0.0005, 4)
            j = [x for x in joins if abs(x-r["t1"]) <= 0.6]
            if j: r["t1"] = round(min(j, key=lambda x: abs(x-r["t1"]))+0.0005, 4)
    for r in out:                                                    # round 4: a clip that starts a beat after its phrase (A3 opens on the wind-up)
        if r.get("late"): r["t0"] = round(r["t0"] + r["late"], 4)
    fs = [r for r in out if r["kind"] in FULL]
    for x, y in zip(fs, fs[1:]):
        if 0 < y["t0"]-x["t1"] < 0.9 or x["t1"] > y["t0"]: x["t1"] = y["t0"]
    for r in out:                                                    # side card edges on shot joins
        if r["kind"] == "l3":
            for k in ("t0", "t1"):
                j = min(joins, key=lambda x: abs(x-r[k]))
                if abs(j-r[k]) <= 0.7: r[k] = round(j+0.0005, 4)
    lts = [r for r in out if r["kind"] == "lt"]
    for x, y in zip(lts, lts[1:]):                                   # never two lower thirds at once
        if x["t1"] > y["t0"]-0.2: x["t1"] = round(y["t0"]-0.2, 3)
    for x in lts:                                                    # a lower third ends before a full-screen card starts
        for y in out:
            if y["kind"] == "scene" and x["t0"] < y["t0"] < x["t1"]: x["t1"] = round(y["t0"]-0.1, 3)
    return out
if __name__ == "__main__":
    R = resolve(); json.dump(R, open(f"{W}/plan_resolved.json", "w"), indent=1)
    for r in R: print(f"{r['id']:4s} {r['kind']:5s} {r['t0']:7.2f} - {r['t1']:7.2f} ({r['t1']-r['t0']:.1f}s)")
    lt = [(a["id"], b["id"]) for a in R for b in R if a["kind"] == "lt" and b["kind"] == "scene" and a["t0"] < b["t1"] and b["t0"] < a["t1"]]
    print("lower third under a full-screen card:", lt)
