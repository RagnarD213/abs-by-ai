#!/usr/bin/env python3
"""Correlate stage_times.log with ffmpeg_calls.log and print the timing table.

The interesting number is the GAP: stage wall time minus the ffmpeg time inside
that stage's window is the single-threaded Python work (PIL, numpy, Whisper) --
i.e. what parallelising could reach, as opposed to what only a faster chip can.
"""
import sys, os

D = os.environ.get('ABSBYAI_TIMING_DIR', '/Volumes/Extreme/_edit_work/_timing')

def load(p, n):
    out = []
    if not os.path.exists(p):
        return out
    for line in open(p):
        f = line.rstrip('\n').split('\t')
        if len(f) >= n:
            out.append(f)
    return out

stages = [(float(a), b, float(c), int(d)) for a, b, c, d in
          (r[:4] for r in load(f'{D}/stage_times.log', 4))]
calls = [(float(r[0]), float(r[1]), int(r[2]), r[3], r[4]) for r in
         load(f'{D}/ffmpeg_calls.log', 5)]

if not stages:
    sys.exit('no stage_times.log yet')

print(f'{"stage":<22}{"wall":>9}{"ffmpeg":>9}{"python":>9}{"calls":>7}{"%":>7}  bound')
print('-' * 78)
total = sum(s[2] for s in stages)
for t0, name, wall, rc in stages:
    t1 = t0 + wall
    inside = [c for c in calls if t0 <= c[0] < t1]
    ff = sum(c[1] for c in inside)
    py = wall - ff
    bound = 'ffmpeg/x264' if ff > 0.65 * wall else ('python (1 core)' if py > 0.65 * wall else 'mixed')
    flag = '' if rc == 0 else f'  RC={rc}'
    print(f'{name:<22}{wall:>8.1f}s{ff:>8.1f}s{py:>8.1f}s{len(inside):>7}'
          f'{100 * wall / total:>6.1f}%  {bound}{flag}')
print('-' * 78)
ff_all = sum(sum(c[1] for c in calls if s[0] <= c[0] < s[0] + s[2]) for s in stages)
print(f'{"TOTAL":<22}{total:>8.1f}s{ff_all:>8.1f}s{total - ff_all:>8.1f}s')
print(f'\ntotal {total/60:.1f} min   ffmpeg {ff_all/60:.1f} min ({100*ff_all/total:.0f}%)   '
      f'python {(total-ff_all)/60:.1f} min ({100*(total-ff_all)/total:.0f}%)')
