#!/usr/bin/env python3
"""Record the negative-imagery scan for one delivered master, after the sheet has been LOOKED AT.
  s20_neg.py <9x16|16x9> <master> <frames_checked> '<json findings>'
"""
import hashlib, json, os, sys
from datetime import datetime, timezone
KEY, MASTER, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
findings = json.loads(sys.argv[4]) if len(sys.argv) > 4 else []
h = hashlib.sha256()
with open(MASTER, "rb") as f:
    for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
os.makedirs("logs", exist_ok=True)
d = {"sha256": h.hexdigest(), "when": datetime.now(timezone.utc).isoformat(),
     "frames_checked": N, "findings": findings,
     "method": "evenly spaced frames across the delivered render, tiled and inspected for Google's "
               "Negative Events and Imagery triggers -- above all a zoomed-in close-up of an "
               "overweight body part framed with disgust or shame"}
json.dump(d, open(f"logs/negative_scan_{KEY}.json", "w"), indent=1)
print(f"logs/negative_scan_{KEY}.json  {N} frames, {len(findings)} finding(s), sha {d['sha256'][:12]}")
