#!/usr/bin/env python3
"""Verify EVERY segment of the recovered EDL by aligning HIS mix against the raw roll on
the speech ENERGY ENVELOPE, which survives his EQ, his music bed and our grade.

Attempt 1 verified the EDL by eyeballing pose at 14 timecodes and never checked the audio.
Segment 0's src_in was 2.5 s early -- pointing at silence -- so the hook line was missing
from the mix, and no metric noticed.
"""
import json, subprocess, sys
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = ("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, "
       "outdoor workout content | jeff chagrin | dan rose/C1591.MP4")
HIS = 'ref_audit/his.wav'
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio'); from common import load_source
SR, HOP = 16000, 160          # 100 envelope samples per second

def load(p, ss=None, t=None, af='anull'):
    c = [FF, '-v', 'error']
    if ss is not None: c += ['-ss', f'{ss:.4f}']
    if t is not None:  c += ['-t', f'{t:.4f}']
    c += ['-i', p, '-af', af, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(c, capture_output=True).stdout, dtype=np.float32).astype(float)

def env(a):
    n = len(a)//HOP*HOP
    e = np.sqrt((a[:n].reshape(-1, HOP)**2).mean(1) + 1e-12)
    e = np.log(e)
    return (e - e.mean())/(e.std() + 1e-9)

if __name__ == '__main__':
    S = json.load(open('edl_final.json'))
    RAW = load(SRC, 0, 700, load_source(SRC)['filter'])   # the lav per pick_lav, not a channel number
    RE = env(RAW)
    print(f'raw envelope {len(RE)/100:.1f}s')
    bad = []
    for s in S:
        d = s['cut_out'] - s['cut_in']
        if d < 0.55: 
            print(f"{s['i']:3d} {s['cut_in']:7.2f} dur {d:4.2f}s  (too short to align)"); continue
        c = env(load(HIS, s['cut_in'], d))
        n = len(c)
        lo = max(0, int((s['src_in']-8)*100)); hi = min(len(RE)-n, int((s['src_in']+8)*100))
        best = (-9, None)
        for off in range(lo, hi):
            v = float((RE[off:off+n]*c).mean())
            if v > best[0]: best = (v, off)
        t = best[1]/100.0
        delta = t - s['src_in']
        flag = ''
        if abs(delta) > 0.20 and best[0] > 0.35: flag = '  <== EDL WRONG'; bad.append((s['i'], s['src_in'], t, delta, best[0]))
        print(f"{s['i']:3d} cut {s['cut_in']:7.2f}-{s['cut_out']:7.2f}  src {s['src_in']:7.2f} -> "
              f"{t:7.2f}  delta {delta:+6.2f}s  corr {best[0]:.2f}{flag}", flush=True)
    print(f'\nsegments whose recovered src_in is off by more than 0.20 s: {len(bad)}')
    for i, a, b, d, c in bad: print(f'  seg {i}: {a:.2f} -> {b:.2f} ({d:+.2f}s, corr {c:.2f})')
    json.dump([dict(i=i, old=a, new=b, delta=d, corr=c) for i,a,b,d,c in bad],
              open('ref_audit/edl_deltas.json','w'), indent=1)
