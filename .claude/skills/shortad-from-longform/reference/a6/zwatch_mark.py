#!/usr/bin/env python3
"""Record the HUMAN half of the watch pass in logs/watch_pass.json -- only after every boundary strip of THIS exact
file has been looked at (watch/sheets/watch_sheet_*.jpg). qc.py check 15 reads `reviewed`, `boundaries`, `inspected`
and the video name. The note says what was checked, so the claim can be audited.
  python3 zwatch_mark.py <video.mp4> "<what was looked at and found>" """
import json, os, sys, hashlib, datetime
V, note = sys.argv[1], sys.argv[2]
d = json.load(open('logs/watch_pass.json'))
assert d['video'] == os.path.basename(V), f"watch log is for {d['video']}, not {V} -- re-run watch.py on this file first"
h = hashlib.sha256()
with open(V, 'rb') as f:
    for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
d.update(reviewed=d['boundaries'], inspected=True, sha256=h.hexdigest(), note=note,
         reviewed_at=datetime.datetime.now().isoformat(timespec='seconds'))
json.dump(d, open('logs/watch_pass.json', 'w'), indent=1)
print(f"watch pass recorded: {d['boundaries']} boundaries on {d['video']} ({d['sha256'][:12]})")
