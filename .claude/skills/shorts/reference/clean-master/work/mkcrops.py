#!/usr/bin/env python3
"""Regenerate shots/crops.json from the measured per-beat torso centres.

Split out of the one-off analysis so a rebuild cannot silently reuse a stale crop table -
the skill records a build where a hand-edited plan left crops.json stale and the preview
showed the wrong thing. Beats are measured on the CONTAINER timeline (work/splices.py uses
frame-difference peaks in the picture), so they survive the audio-timeline correction.
"""
import json
man = json.load(open('shots/manifest.json'))
geom = json.load(open('work/beatgeom.json'))
by = {(v['seg'], v['beat']): v for v in geom.values()}
missing = [m['name'] for m in man if (m['seg'], m['beat']) not in by]
if missing:
    raise SystemExit(f"no measured torso centre for: {missing}\n"
                     f"  run the beat measurement for those beats first")
crops = {m['name']: by[(m['seg'], m['beat'])]['torso'] for m in man}
json.dump(crops, open('shots/crops.json', 'w'), indent=1)
xs = list(crops.values())
print(f"{len(crops)} crop centres, x {min(xs):.4f}-{max(xs):.4f} "
      f"({(max(xs)-min(xs))*1920:.0f}px of source)")
