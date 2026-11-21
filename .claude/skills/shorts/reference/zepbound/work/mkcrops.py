#!/usr/bin/env python3
"""shots/crops.json from the PER-SHOT HEAD median (work/shotgeom.json, work/measure_shots.py).

⚠ NOT the torso block, on THIS roll. Dan is framed cut at the waist with his arms hanging into
the anchor's 60%-coverage band, so the "torso block" flips shoulder-to-shoulder between two
modes 0.50 / 0.58 within one shot (drawn and checked on frames: the torso line lands right of his
face whenever the bulkier frame-right arm counts as tall). The head is fully in frame on every
frame, moves only when HE moves, and is where the viewer looks: within-shot sd 14-80px, cross-shot
spread 134px delivered against 206px for the torso. Same anchor is used by work/centregate.py.
"""
import json
man = json.load(open('shots/manifest.json'))
geom = json.load(open('work/shotgeom.json'))
man = [m for m in man if m.get('src') != 'ai']
missing = [m['name'] for m in man if m['name'] not in geom]
if missing: raise SystemExit(f"no per-shot measurement for: {missing} - run work/measure_shots.py")
crops = {m['name']: geom[m['name']]['head'] for m in man}
json.dump(crops, open('shots/crops.json', 'w'), indent=1)
xs = list(crops.values())
print(f"{len(crops)} crop centres (per-shot HEAD median), x {min(xs):.4f}-{max(xs):.4f} ({(max(xs)-min(xs))*1920:.0f}px of source)")
