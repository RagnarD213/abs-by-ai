#!/usr/bin/env python3
"""Cut-point ground truth: the INTERSECTION of two independent silence measurements.

This source has no music bed, so both tools are valid here and neither has to be trusted
alone:
  * work/vad.py  - speech-band energy against a rolling local floor. Finds 1638 gaps / 430s.
    More permissive: it will call a breath or a lip smack a gap, because they carry no
    speech-band modulation.
  * silencedetect -26dB/0.05 - level in the whole mix. 1476 intervals / 284s. Blind to a
    quiet breath, but it is what the skill calibrated on for OUR OWN cuts.

Intersecting them means a cut point has to be both "nobody is talking" and "nothing is
audible". 85% of silencedetect's intervals already sit inside a VAD gap, so the cost is
small and the safety is real.
"""
import json, re, subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
r = subprocess.run([FF, '-nostdin', '-hide_banner', '-i', 'work/audio48k.wav', '-af',
                    'silencedetect=noise=-26dB:d=0.05', '-f', 'null', '-'],
                   capture_output=True, text=True)
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
sd = [[a, b] for a, b in zip(st, en)]
assert len(sd) > 500, f'silencedetect found only {len(sd)} intervals - check stderr capture'
vad = json.load(open('work/gaps_vad.json'))

out, i, j = [], 0, 0
while i < len(sd) and j < len(vad):
    a0, a1 = sd[i]; b0, b1 = vad[j]
    lo, hi = max(a0, b0), min(a1, b1)
    if hi - lo >= 0.06:
        out.append([round(lo, 3), round(hi, 3)])
    if a1 < b1: i += 1
    else: j += 1
json.dump(out, open('work/gaps.json', 'w'))
print(f"silencedetect {len(sd)} / vad {len(vad)} -> {len(out)} confirmed gaps, "
      f"{sum(b-a for a,b in out):.1f}s total, median {sorted(b-a for a,b in out)[len(out)//2]:.3f}s")
