"""Check ONE plan part on its own (plan_parts/pNN_*.py) without touching the film's plan_resolved.json: resolves every phrase
on words_out.json, prints each item's film time and length, pre-flights every clip source against its slot, lists overlaps,
gaps with nothing on screen, and cutaway cover. Writes plan_parts/_resolved_<part>.json for a from_plan.py dry run.
usage: resolve_part.py plan_parts/p03_cuts.py T0 T1     (T0/T1 = the part's film range in seconds)"""
import json, re, sys, os, subprocess
W = "/Volumes/Extreme/_edit_work/ro20"; FPS = 30000/1001
FP = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe"
_C = json.load(open("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/clip-library/catalog.json")); _ROOT = _C.get("library_root", "") if isinstance(_C, dict) else ""; _C = _C if isinstance(_C, list) else (_C.get("clips") or _C.get("items") or list(_C.values()))
LIBC = {c["id"]: c for c in _C if isinstance(c, dict) and "id" in c}
part = sys.argv[1]; T0 = float(sys.argv[2]); T1 = float(sys.argv[3])
SHOOT = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera"; AI = f"{W}/aiframes"; ST = f"{W}/stock"
g = dict(br=lambda roll, t: f"{SHOOT}/{roll}.MP4@{t}", stock=lambda name, t=0.0: f"{ST}/{name}@{t}", DAN=dict(people="dan", physique=False),
         OTHER=dict(people="other", physique=False), NONE=dict(people="none", physique=False), AIL=dict(label="AI-GENERATED"), AI=AI, ST=ST, W=W)
exec(compile(open(part).read(), part, "exec"), g); PLAN = g["PART"]
WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
NUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "ten": "10", "fifty": "50", "fifteen": "15", "thirty": "30"}
def norm(s):
    s = re.sub(r"[^a-z0-9]", "", s.lower()); return NUM.get(s, s)
TOK = [norm(w["w"]) for w in WO]
def find(phrase, after):
    p = [norm(x) for x in re.split(r"[\s\-]+", phrase) if norm(x)]
    for i in range(len(TOK)):
        if WO[i]["t0"] < after-0.01: continue
        j = i; ok = True
        for q in p:
            while j < len(TOK) and TOK[j] == "": j += 1
            if j >= len(TOK) or not (TOK[j] == q or (len(q) > 3 and TOK[j].startswith(q[:4]))): ok = False; break
            j += 1
        if ok: return i, j-1
    return None
bad = 0; out = []; after = T0 - 2
for it in PLAN:
    for k in ("id", "kind", "start", "end"): assert k in it, (it.get("id"), "missing", k)
    f = find(it["start"], after)
    if not f: print("PHRASE NOT FOUND (start)", it["id"], repr(it["start"]), "after", round(after, 1)); bad += 1; continue
    t0 = WO[f[0]]["t0"]; e = find(it["end"], t0)
    if not e: print("PHRASE NOT FOUND (end)", it["id"], repr(it["end"])); bad += 1; continue
    t1 = WO[e[1]]["t1"] + it.get("tail", 0.25); r = dict(it, t0=round(t0, 3), t1=round(t1, 3)); out.append(r); after = t0
    if not (T0-1 <= t0 <= T1+1): print("OUTSIDE THE PART'S RANGE", it["id"], round(t0, 1)); bad += 1
    if it["kind"] == "lt":
        ph = [p[1] for p in it["parts"]]; tt = [find(p, t0-0.5) for p in ph]
        if any(x is None for x in tt): print("PART PHRASE NOT FOUND", it["id"], [p for p, x in zip(ph, tt) if x is None]); bad += 1
        else:
            ts = [WO[x[0]]["t0"] for x in tt]
            if ts != sorted(ts) or ts[-1] > t1: print("PARTS OUT OF ORDER OR AFTER THE END", it["id"], [round(x, 2) for x in ts], "end", round(t1, 2)); bad += 1
        if t1-t0 < 2.5: print("LOWER THIRD UNDER 2.5 s", it["id"], round(t1-t0, 1)); bad += 1
        if "".join(p[0] for p in it["parts"]).replace(" ", "") != it["point"].replace(" ", ""): print("PARTS DO NOT SPELL THE POINT", it["id"]); bad += 1
    if it["kind"] == "clip" and not it.get("frames"):
        n = t1-t0; per = n/len(it["src"])
        for s in it["src"]:
            p, st = (s.split("@") + ["0"])[:2]; st = float(st)
            if not p.startswith("/"):
                if p not in LIBC: print("NOT IN THE LIBRARY", it["id"], p); bad += 1; continue
                p = LIBC[p]["library_path"]; p = p if p.startswith("/") else os.path.join(_ROOT, p)
            if not os.path.exists(p): print("FILE MISSING", it["id"], p); bad += 1; continue
            d = float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout or 0)
            if d - st < per - 0.02: print(f"CLIP TOO SHORT {it['id']}: {os.path.basename(p)} has {d-st:.1f} s from {st}, slot needs {per:.1f} s"); bad += 1
        for k in ("people", "physique", "note"):
            if k not in it: print("CLIP MISSING FIELD", it["id"], k); bad += 1
        if n < 2.0: print("CLIP UNDER 2 s", it["id"], round(n, 1)); bad += 1
out.sort(key=lambda r: r["t0"]); json.dump(out, open(f"{os.path.dirname(part)}/_resolved_{os.path.basename(part)[:-3]}.json", "w"), indent=1)
for r in out: print(f"{r['id']:6s} {r['kind']:5s} {int(r['t0']//60)}:{r['t0']%60:05.2f} - {int(r['t1']//60)}:{r['t1']%60:05.2f} ({r['t1']-r['t0']:.1f}s)  " + (r.get("point") or (r.get("note") or "")[:70]))
lts = [r for r in out if r["kind"] == "lt"]; cl = [r for r in out if r["kind"] in ("clip", "scene")]
for x, y in zip(lts, lts[1:]):
    if x["t1"] > y["t0"]-0.2: print(f"LOWER THIRDS OVERLAP {x['id']} / {y['id']} (the first will be cut short to {y['t0']-0.2-x['t0']:.1f} s)")
for x, y in zip(cl, cl[1:]):
    if x["t1"] > y["t0"]+0.05: print(f"CLIPS OVERLAP {x['id']} / {y['id']}"); bad += 1
ev = sorted([(r["t0"], r["t1"]) for r in out]); t = T0; gaps = []
for a, b in ev:
    if a - t > 25: gaps.append((round(t, 1), round(a, 1)))
    t = max(t, b)
if T1 - t > 25: gaps.append((round(t, 1), T1))
cov = sum(min(r["t1"], T1)-max(r["t0"], T0) for r in cl)
print(f"\n{len(lts)} lower thirds, {len(cl)} clips; cutaway cover {100*cov/(T1-T0):.0f} % of {T1-T0:.0f} s; stretches over 25 s with nothing on screen: {gaps}")
caps = [r["id"] for r in lts if re.search(r"\b[A-Z]{3,}\b", r["point"])]
print(f"lower thirds with a FULL CAPS word: {len(caps)} of {len(lts)} {caps}")
print("ERRORS:", bad)
