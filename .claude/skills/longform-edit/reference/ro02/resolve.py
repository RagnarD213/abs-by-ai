"""Resolve plan phrases to output times (words_out.json). Items are searched in order, each after the previous item's start."""
import json, re, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro02/recipe")
from plan import PLAN
W="/Volumes/Extreme/_edit_work/ro02"
WO=[w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
SH=json.load(open(f"{W}/shots.json")); FPS_=30000/1001
NUM={"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9","ten":"10","fifteen":"15","thirty":"30","ninety":"90","twenty":"20","first":"first"}
def norm(s):
    s=re.sub(r"[^a-z0-9]", "", s.lower()); return NUM.get(s, s)
TOK=[norm(w["w"]) for w in WO]
def find(phrase, after=0.0):
    p=[norm(x) for x in re.split(r"[\s\-]+", phrase) if norm(x)]
    for i in range(len(TOK)):
        if WO[i]["t0"] < after-0.01: continue
        j=i; ok=True
        for q in p:
            while j < len(TOK) and TOK[j]=="" : j+=1
            if j>=len(TOK) or not (TOK[j]==q or (len(q)>3 and TOK[j].startswith(q[:4]))): ok=False; break
            j+=1
        if ok: return i, j-1
    raise SystemExit(f"phrase not found after {after:.2f}: {phrase!r}")
def resolve():
    out=[]; after=0.0; sec=0.0
    for it in PLAN:
        if it["kind"]=="skip": continue
        if it.get("shot"):                                    # an item that lives on one shot (the live set's countdown)
            sh=next(x for x in SH if x["id"]==it["shot"]); r=dict(it); r["t0"]=round(sh["out_f0"]/FPS_+0.0005,4); r["t1"]=round(sh["out_f1"]/FPS_,4)
            r["hold_t"]=round(sh["out_f0"]/FPS_+(it["beep_src"]-it["secs"]-sh["src_f0"]/FPS_),3); out.append(r); continue
        i,_=find(it["start"], after); t0=WO[i]["t0"]
        if it.get("end"):
            a,k=find(it["end"], t0); t1=WO[a]["t0"] if it.get("end_at_start") else WO[k]["t1"]+it.get("tail",0.25)
        else: t1=t0+it["dur"] if it.get("dur") else None
        r=dict(it); r["t0"]=round(t0,3)
        if it.get("x_ph"): r["x"]={k: WO[find(ph, 0.0)[0]]["t0"] for k,ph in it["x_ph"].items()}       # the red X lands on the heard word
        if it.get("stage_ph"): r["stage_t"]=[WO[find(ph, t0)[0]]["t0"] for ph in it["stage_ph"]]
        if it["kind"]=="title": sec=t0
        r["t1"]=None if t1 is None else round(t1,3)
        out.append(r); after=sec
    out.sort(key=lambda r: r["t0"])
    # full-screen items: start on a cut that falls up to 0.85 s before them; close gaps < 0.9 s to the next full-screen item
    # (round-2 review: 0.5-0.82 s presenter flashes right before a card or clip at 2:49.8, 6:04.2, 6:54.8, 8:09.6, 11:51.6)
    FULL=("scene","title","clip","ai","opener")
    joins=[sh["out_f0"]/(30000/1001) for sh in json.load(open(f"{W}/shots.json"))]
    for r in out:
        if r["kind"] in FULL:
            j=[x for x in joins if r["t0"]-0.85 <= x < r["t0"]]
            if j: r["t0"]=round(max(j)+0.0005,4)
    fs=[r for r in out if r["kind"] in FULL]
    for x,y in zip(fs,fs[1:]):
        if x["t1"] and 0 < y["t0"]-x["t1"] < 0.9: x["t1"]=y["t0"]
        if x["t1"] and x["t1"] > y["t0"]: x["t1"]=y["t0"]          # never two full-screen items at once: the later one wins its start
    # a side card that would outlive a shot join by < 0.35 s ends on the join (no stub of card over the next shot)
    S=json.load(open(f"{W}/shots.json")); FPS=30000/1001
    # side cards (3A list, cycle, phone) move Dan: both edges snap to a shot join within 0.7 s so the reframe hides in a cut
    J=[sh["out_f0"]/FPS for sh in S]
    for r in out:
        if r["kind"] in ("l3","phone","cycle","anat") and r["t1"]:
            for k in ("t0","t1"):
                j=min(J, key=lambda x: abs(x-r[k]))
                if abs(j-r[k]) <= 0.7: r[k]=round(j+0.0005,4)
    # a side card that follows a full-screen item by < 0.8 s starts where it ends (round-2 review: 10-frame T2 flash G19 -> G20)
    for r in out:
        if r["kind"] in ("l3","phone","anat"):
            prev=[x for x in fs if x["t1"] and 0 < r["t0"]-x["t1"] < 0.8]
            if prev: r["t0"]=prev[-1]["t1"]
    for r in out:
        if r.get("max_len") and r["t1"] and r["t1"]-r["t0"] > r["max_len"]: r["t1"]=round(r["t0"]+r["max_len"],4)
    # no presenter island < 0.5 s between a full-screen item's end and the next framing cut (round-2 re-review: 0.30 s
    # of T2 after C12 at 5:54.49). A length-capped clip slides back so it ends on the cut; any other item runs on to it.
    for r in out:
        if r["kind"] in FULL and r["t1"]:
            j=[x for x in joins if r["t1"] < x <= r["t1"]+0.5]
            if j and not any(y is not r and y["kind"] in FULL and y["t1"] and y["t0"] <= r["t1"] < y["t1"] for y in out):
                if r.get("max_len"): d=j[0]-r["t1"]; r["t0"]=round(r["t0"]+d,4); r["t1"]=round(j[0],4)
                else: r["t1"]=round(j[0],4)
    # template overlays (lt, l3, cycle) never share a frame with a full-screen item: a side card that starts inside one
    # ends it on the card's cut; a lower third that starts inside one waits for it; either ends where the next one starts
    for h in out:
        if h["kind"] not in ("lt", "l3", "cycle", "anat") or not h["t1"]: continue
        for f in out:
            if f["kind"] not in FULL or not f["t1"]: continue
            if f["t0"] <= h["t0"] < f["t1"]:
                if h["kind"] == "lt": h["t0"] = round(f["t1"] + 0.034, 4)
                else: f["t1"] = h["t0"]
            if h["t0"] < f["t0"] < h["t1"]: h["t1"] = round(f["t0"] - (0.034 if h["kind"] == "lt" else 0), 4)
    for a,b in zip(out,out[1:]):
        if a.get("pad_to_next"): a["t1"]=b["t0"]
    return out
if __name__=="__main__":
    R=resolve(); json.dump(R,open(f"{W}/plan_resolved.json","w"),indent=1)
    for r in R: print(f"{r['id']:4s} {r['kind']:6s} {r['t0']:7.2f} - {r['t1'] if r['t1'] is None else round(r['t1'],2)}  {r.get('reveal_t','')}")
