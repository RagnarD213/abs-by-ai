"""Round 5: one findings.json for the watch pass on the delivered (fourth) render, from three independent judgements.
A cut strip whose frames did not change between a judged render and the delivered one keeps that judge's verdict (proved
frame by frame: PSNR of the delivered film against the judged render's 540p copy, logs/r3_vs_r2_psnr.txt and
logs/r4_vs_r3_psnr.txt). Strips that changed, and all contact sheets, were judged fresh on the delivered file.
Dispositions: a hair_top defect in a shot whose crop starts on the camera's own top row is the camera's framing, which Dan
accepted for this film in his own words; nothing else is accepted here. usage: merge_findings.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["RO06_NOSTAB"] = "1"
import build as Bd
W = Bd.W + "/round5"; FPS = Bd.FPS
DAN = "Dan, 2026-10-08, on this film: 'hair, leave as shot'. The crop's top row is the camera's own top row in this shot, so the camera framed it."
def tsec(fn):
    m = re.search(r"_(\d\d)-(\d\d\.\d\d)", fn); return int(m.group(1))*60 + float(m.group(2))
def idx(E):
    d = {}
    for e in E:
        if e["image"].startswith("strip_"): d.setdefault(round(tsec(e["image"]), 2), []).append(e)
    return d
r2 = idx(json.load(open(f"{W}/render2/findings_render2.json"))["entries"]); r3 = idx(json.load(open(f"{W}/render3/findings_r3_fresh.json"))["entries"])
r4 = json.load(open(f"{W}/logs/findings_r4_fresh.json"))["entries"]; split = json.load(open(f"{W}/logs/judge4_split.json"))
segs = Bd.all_segments()
def cam_top(t):
    s = next((s for s in segs if s["o0"]/FPS - 0.05 <= t < s["o1"]/FPS + 0.05), None); return bool(s) and s["crop"][3] == 0
out = []
for fn, src in split["carry"]:
    t = tsec(fn); pool = r3 if src == "r3" else r2
    for e in next(v for k, v in pool.items() if abs(k - t) <= 0.03):
        n = dict(e, image=fn); n["note"] = (e.get("note") or "") + f" [verdict carried from the judged {'third' if src == 'r3' else 'second'} render: these frames are unchanged in the delivered file]"
        out.append(n)
names = {x for x in os.listdir(f"{W}/watch/strips") if x.startswith("strip_")} | {x for x in os.listdir(f"{W}/watch/sheets") if x.startswith("sheet_")}
for e in r4:
    assert e["image"] in names, e["image"]; out.append(dict(e))
acc = 0
for e in out:
    if e["verdict"] == "defect" and e.get("item") == "hair_top":
        t = e.get("t") if isinstance(e.get("t"), (int, float)) else tsec(e["image"]) if e["image"].startswith("strip_") else None
        if t is not None and cam_top(float(t)): e["disposition"] = "accepted_by_dan"; e["note"] = (e.get("note") or "") + " | " + DAN; acc += 1
# the tool also wants a verdict on each strip's pair image (the -1|0 frames of that strip at half size). The same two frames are in the strip, so a pair takes its strip's worst verdict.
rank = {"clean": 0, "expected": 1, "defect": 2}
for pf in sorted(x for x in os.listdir(f"{W}/watch/strips") if x.startswith("pair_")):
    num = pf.split("_")[1]; mine = [e for e in out if e["image"].startswith(f"strip_{num}_")]; w = max(mine, key=lambda e: rank[e["verdict"]])
    n = dict(image=pf, verdict=w["verdict"], t=w.get("t"), note=f"the -1|0 pair of strip {num} (the same two frames, judged in the strip): " + (w.get("note") or "")[:300])
    if w.get("item"): n["item"] = w["item"]
    if w.get("disposition"): n["disposition"] = w["disposition"]
    out.append(n); names.add(pf)
have = {e["image"] for e in out}; missing = sorted(names - have)
json.dump(dict(entries=out), open(f"{W}/logs/findings.json", "w"), indent=0)
import collections
print(len(out), "entries for", len(have), "of", len(names), "images; missing:", missing[:5])
print("verdicts:", dict(collections.Counter(e["verdict"] for e in out)), "| hair entries accepted in Dan's words:", acc)
op = [e for e in out if e["verdict"] == "defect" and e.get("disposition") != "accepted_by_dan"]
print("open defects:", dict(collections.Counter(e.get("item") for e in op)))
for e in op: print("  ", e.get("item"), e.get("t"), e["image"][:26], "|", (e.get("note") or "")[:150])
