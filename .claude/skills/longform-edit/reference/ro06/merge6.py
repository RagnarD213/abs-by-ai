"""Round 6 watch pass: which cut strips are unchanged against the round 5 film (already judged, 482 images), and one findings.json for the delivered file.
split: per-frame PSNR of the round 6 film against the round 5 film (ffmpeg psnr, full size). A strip (frames -2..+2 round a boundary) whose five frames
       all read 38 dB or more, and which has a round 5 strip at the same time, keeps that strip's verdict. Everything else, and every contact sheet, goes
       to a fresh judge: writes logs/judge6_split.json and logs/judge6_fresh_list.txt.
merge: carried verdicts + the fresh judge's logs/findings_r6_fresh.json -> logs/findings.json (pairs take their strip's verdict; a hair_top entry in a shot
       whose crop starts on the camera's own top row keeps Dan's 'leave as shot').   usage: merge6.py split | merge"""
import json, os, re, sys, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as Bd
W6 = Bd.W + "/round6"; W5 = Bd.W + "/round5"; FPS = Bd.FPS; NEW = f"{W6}/RO-06 round 6 - full film.mp4"; OLD = f"{W5}/RO-06 round 5 - full film.mp4"
DAN = "Dan, 2026-10-08, on this film: 'hair, leave as shot' (repeated 2026-10-09: 'hair as shot'). The crop's top row is the camera's own top row in this shot, so the camera framed it."
def tsec(fn):
    m = re.search(r"_(\d\d)-(\d\d\.\d\d)", fn); return int(m.group(1))*60 + float(m.group(2))
def psnr():
    p = f"{W6}/logs/r6_vs_r5_psnr.txt"
    if not os.path.exists(p):
        subprocess.run([Bd.FF, "-nostdin", "-v", "error", "-i", NEW, "-i", OLD, "-lavfi", f"[0:v][1:v]psnr=stats_file='{p}'", "-an", "-f", "null", "-"], check=True, cwd=W6)
    return [float(re.search(r"psnr_avg:(\S+)", l).group(1).replace("inf", "99")) for l in open(p)]
if sys.argv[1] == "split":
    P = psnr(); old = {}
    for e in json.load(open(f"{W5}/logs/findings.json"))["entries"]:
        if e["image"].startswith("strip_"): old.setdefault(round(tsec(e["image"]), 2), []).append(e)
    carry, fresh = [], []
    for fn in sorted(x for x in os.listdir(f"{W6}/watch/strips") if x.startswith("strip_")):
        t = tsec(fn); f = int(round(t*FPS)); lo = min(P[max(0, f-2):f+3]); k = next((k for k in old if abs(k - t) <= 0.03), None)
        (carry if lo >= 38.0 and k is not None else fresh).append([fn, round(lo, 1), k])
    json.dump(dict(carry=carry, fresh=fresh), open(f"{W6}/logs/judge6_split.json", "w"), indent=0)
    sheets = sorted(x for x in os.listdir(f"{W6}/watch/sheets") if x.startswith("sheet_"))
    open(f"{W6}/logs/judge6_fresh_list.txt", "w").write("\n".join([f"watch/sheets/{s}" for s in sheets] + [f"watch/strips/{f[0]}" for f in fresh]) + "\n")
    ch = [i for i, v in enumerate(P) if v < 38.0]; runs = []
    for i in ch:
        if runs and i - runs[-1][1] <= 15: runs[-1][1] = i
        else: runs.append([i, i])
    print(len(carry), "strips carried,", len(fresh), "fresh,", len(sheets), "sheets fresh; frames under 38 dB:", len(ch), "of", len(P))
    print("changed stretches (s):", [(round(a/FPS, 2), round(b/FPS, 2)) for a, b in runs])
if sys.argv[1] == "merge":
    split = json.load(open(f"{W6}/logs/judge6_split.json")); r6 = json.load(open(f"{W6}/logs/findings_r6_fresh.json"))["entries"]
    old = {}
    for e in json.load(open(f"{W5}/logs/findings.json"))["entries"]:
        if e["image"].startswith("strip_"): old.setdefault(round(tsec(e["image"]), 2), []).append(e)
    segs = Bd.all_segments()
    def cam_top(t):
        s = next((s for s in segs if s["o0"]/FPS - 0.05 <= t < s["o1"]/FPS + 0.05), None); return bool(s) and s["crop"][3] == 0
    out = []
    for fn, lo, k in split["carry"]:
        for e in old[k]:
            n = dict(e, image=fn); n["note"] = re.sub(r" \[verdict carried.*?\]", "", e.get("note") or "") + f" [verdict carried from the judged round 5 film: these five frames are unchanged in the round 6 file, lowest PSNR {lo} dB]"
            out.append(n)
    names = {x for x in os.listdir(f"{W6}/watch/strips") if x.startswith("strip_")} | {x for x in os.listdir(f"{W6}/watch/sheets") if x.startswith("sheet_")}
    for e in r6:
        e = dict(e, image=os.path.basename(e["image"])); assert e["image"] in names, e["image"]; out.append(e)
    acc = 0
    for e in out:
        if e["verdict"] == "defect" and e.get("item") == "hair_top" and e.get("disposition") != "accepted_by_dan":
            t = e.get("t") if isinstance(e.get("t"), (int, float)) else tsec(e["image"]) if e["image"].startswith("strip_") else None
            if t is not None and cam_top(float(t)): e["disposition"] = "accepted_by_dan"; e["note"] = (e.get("note") or "") + " | " + DAN; acc += 1
    rank = {"clean": 0, "expected": 1, "defect": 2}
    for pf in sorted(x for x in os.listdir(f"{W6}/watch/strips") if x.startswith("pair_")):
        num = pf.split("_")[1]; mine = [e for e in out if e["image"].startswith(f"strip_{num}_")]; w = max(mine, key=lambda e: rank[e["verdict"]])
        n = dict(image=pf, verdict=w["verdict"], t=w.get("t"), note=f"the -1|0 pair of strip {num} (the same two frames, judged in the strip): " + (w.get("note") or "")[:300])
        for k in ("item", "disposition"):
            if w.get(k): n[k] = w[k]
        out.append(n); names.add(pf)
    have = {e["image"] for e in out}; missing = sorted(names - have)
    json.dump(dict(entries=out), open(f"{W6}/logs/findings.json", "w"), indent=0)
    print(len(out), "entries for", len(have), "of", len(names), "images; missing:", missing[:8])
    print("verdicts:", dict(collections.Counter(e["verdict"] for e in out)), "| hair entries accepted in Dan's words:", acc)
    op = [e for e in out if e["verdict"] == "defect" and e.get("disposition") != "accepted_by_dan"]
    print("open defects:", dict(collections.Counter(e.get("item") for e in op)))
    for e in op: print("  ", e.get("item"), e.get("t"), e["image"][:26], "|", (e.get("note") or "")[:170])
