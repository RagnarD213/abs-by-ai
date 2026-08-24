#!/usr/bin/env python3
"""Map each EDL range to its already-rendered segment in clips_graded/.

The cache key is sha1("{src_path}|{start:.3f}|{end:.3f}|{filter}|final|{fps}").
The cached files were written BEFORE the drive was repathed, so the key has to be
rebuilt with the OLD /Volumes/Seagate 4TB/ path or nothing matches.
"""
import hashlib, json, subprocess
from pathlib import Path

B   = Path("/Volumes/Extreme/_edit_work/abwheel")
FFP = "/Volumes/Extreme/_edit_work/bin/ffprobe"
OLD = "/Volumes/Seagate 4TB/"
NEW = "/Volumes/Extreme/"

def seg_for(r, srcpath, fps, use_old=True):
    p = srcpath.replace(NEW, OLD) if use_old else srcpath
    f = r.get("grade", "")
    if r.get("vf"): f = ",".join(x for x in (f, r["vf"]) if x)
    key = f"{p}|{float(r['start']):.3f}|{float(r['end']):.3f}|{f}|final|{fps}"
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    return B / "clips_graded" / f"seg_{r['source']}_{h}.mp4"

def vdur(p):
    o = subprocess.run([FFP, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True).stdout.strip()
    return float(o) if o and o != "N/A" else None

def build():
    edl = json.load(open(B / "edl.json"))
    fps = str(edl.get("fps") or "24")
    out, acc = [], 0.0
    for i, r in enumerate(edl["ranges"]):
        src = edl["sources"][r["source"]]
        p = seg_for(r, src, fps, True)
        if not p.exists():
            p2 = seg_for(r, src, fps, False)
            p = p2 if p2.exists() else p
        d = vdur(p) if p.exists() else None
        out.append({"i": i, "beat": r["beat"], "source": r["source"],
                    "start": r["start"], "end": r["end"],
                    "plan": round(r["end"] - r["start"], 3),
                    "seg": p.name, "exists": p.exists(), "dur": d,
                    "out_start": round(acc, 4)})
        acc += (d if d else r["end"] - r["start"])
    return out, round(acc, 4)

if __name__ == "__main__":
    rows, total = build()
    miss = [r for r in rows if not r["exists"]]
    for r in rows:
        print(f"{r['i']:2d} {r['source']} {r['beat']:26s} plan {r['plan']:7.3f} "
              f"seg {str(r['dur']):>8s}  out@{r['out_start']:8.3f}  "
              f"{'OK' if r['exists'] else 'MISS'}")
    print(f"\ntotal {total:.3f}s   picture 538.365s   drift {total-538.365:+.3f}s")
    print("missing:", len(miss))
    json.dump(rows, open(B / "r2" / "segmap.json", "w"), indent=1)
