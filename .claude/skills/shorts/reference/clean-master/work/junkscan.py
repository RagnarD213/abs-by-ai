#!/usr/bin/env python3
"""Find everything a viewer would call junk: dead air, source jump cuts, and a slow start.

Dan's rev-1 notes named four "awkward cut" timecodes and two "junk footage" ones. Rather than
patch those six, find every instance of each CLASS across all eight shorts:

  PAUSE  - a measured speech gap inside the short. Anything over ~0.55s reads as dead air in a
           vertical short, where the viewer's thumb is already moving.
  SPLICE - a picture cut inherited from the source edit. The long-form joins 62 takes of the
           same locked camera, so every splice inside a short is a NAKED JUMP CUT unless it is
           hidden. This is what "awkward cut" means at 0:26 / 0:10 / 0:28.
  HEAD   - how long after the first frame speech actually starts, and whether the first word
           sits behind a breath or a false start.
"""
import json, subprocess
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
GAPS = json.load(open('work/gaps.json'))
SPL = [s['cut'] for s in json.load(open('work/splices.json'))]
segs = json.loads(subprocess.check_output(
    ['node', '-e', "const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify(SEGMENTS))"]).decode())
W = json.load(open('work/words.json'))['chunks']
PAUSE_MIN = 0.55

for s in segs:
    print(f"\n=== {s['id']}  {s['slug']} ===")
    off = 0.0
    for pi, p in enumerate(s['pieces']):
        a, b = p['start'], p['end']
        # dead air inside the piece
        for g0, g1 in GAPS:
            if g0 < a + 0.05 or g1 > b - 0.05: continue
            if g1 - g0 >= PAUSE_MIN:
                print(f"  PAUSE  out {off + g0 - a:6.2f}s  {g1-g0:.2f}s of silence "
                      f"(src {g0:.2f}-{g1:.2f})")
        # inherited picture cuts
        for c in SPL:
            if a + 0.25 < c < b - 0.25:
                print(f"  SPLICE out {off + c - a:6.2f}s  source jump cut at {c:.2f}")
        off += b - a
    # head: when does speech actually start?
    a = s['pieces'][0]['start']
    first = min((w['timestamp'][0] for w in W if w['timestamp'][0] >= a - 0.01), default=a)
    print(f"  HEAD   first word {first - a:+.2f}s after the cut"
          f"{'   <- slow start' if first - a > 0.45 else ''}")
