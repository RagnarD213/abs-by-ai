"""write round6/V/negative_events_scan.json for the exact master after the sheets were looked at. usage: negscan_record.py V 'findings json list'"""
import sys, json, hashlib, datetime
V = sys.argv[1]; D = f"/Volumes/Extreme/_edit_work/ro20/round6/{V}"
h = hashlib.sha256()
with open(f"{D}/MASTER.mp4", "rb") as f:
    for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
fr = json.load(open(f"{D}/negscan/frames.json"))
rec = dict(sha256=h.hexdigest(), when=datetime.datetime.now().isoformat(timespec="seconds"), frames_checked=fr["n"], by="Claude Opus 5.5 (editor), round 4",
           method=f"{fr['n']} frames: one every 10 s plus the middle of every cutaway and card (negscan/sheet_*.jpg), looked at sheet by sheet",
           findings=json.loads(sys.argv[2]))
json.dump(rec, open(f"{D}/negative_events_scan.json", "w"), indent=1); print(V, rec["frames_checked"], rec["sha256"][:12])
