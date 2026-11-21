#!/usr/bin/env python3
"""Write cut/edl_frames.json so the landing gate can run on the CUTDOWN.

A selection cutdown has no picture EDL of its own: its picture cuts are (a) the master's
own cuts that survive inside a kept range and (b) the seams between ranges. Both are
mapped through cut_plan.json into cut-timeline frames, in the same cumulative-`frames`
shape sqlanding.py reads. A seam is a picture cut by construction, so it is included --
that is precisely where a duplicated first frame or a failed landing would appear.
"""
import json
P = json.load(open('cut_plan.json'))
E = json.load(open('edl_frames.json'))

# master cut frames (cumulative), excluding frame 0
mcuts, n = [], 0
for s in E:
    if n: mcuts.append((n, s['i']))
    n += s['frames']
MTOT = n

# cut-timeline frame for a master frame, per range
def cutn(m):
    off = 0
    for r in P['ranges']:
        if r['n0'] <= m < r['n0'] + r['frames']: return off + (m - r['n0'])
        off += r['frames']
    return None

pts = set()
for m, i in mcuts:
    c = cutn(m)
    if c: pts.add(c)                     # a master cut that survives inside a range
off = 0
for r in P['ranges'][:-1]:
    off += r['frames']; pts.add(off)     # every seam

pts = sorted(p for p in pts if 0 < p < P['frames'])
out, prev = [], 0
for k, p in enumerate(pts + [P['frames']]):
    out.append(dict(i=k, frames=p - prev)); prev = p
json.dump(out, open('cut/edl_frames.json', 'w'), indent=1)
print(f"cut/edl_frames.json: {len(out)} segments, {sum(s['frames'] for s in out)} frames "
      f"(plan {P['frames']}); {len(pts)} picture cuts = "
      f"{len([p for p in pts])} total, of which {len(P['ranges'])-1} are seams")
