#!/usr/bin/env python3
"""Split every recovered segment at the pause trims HIS cut actually contains.

`segfit.py` matched whole spans and recursively split only where the mel score fell below
0.60, so trims that removed a short pause INSIDE a sentence stayed hidden: the segment
kept one src_in, the source ran slower than the cut, and the last words of the segment
fell off the end. That is how "With AI", "your life", "screen" and "belly fat" went
missing without a single metric noticing.

Method: for every word in the cut, offset = raw_word_start - cut_word_start. Inside one
continuous take that offset is constant. Where it steps up, he removed that much; split
there. Cut boundaries never move, so the frame plan and the picture are untouched.
"""
import json, re, sys
import numpy as np

n = lambda s: re.sub(r"[^a-z0-9]", '', s.lower())
def words(p):
    d = json.load(open(p))
    segs = d['segments'] if isinstance(d, dict) else d
    return [(n(w['word']), float(w['start']), float(w['end']))
            for s in segs for w in s.get('words', []) if n(w['word'])]

HIS = words('m.whisper.json')
RAW = words('/Volumes/Extreme/_edit_work/ad1-8-14/C1591.whisper.json')
RW  = [x[0] for x in RAW]
STEP = 0.14        # an offset step this big is a real trim, not Whisper jitter
MINDUR = 0.22      # never make a sub-segment shorter than this

def locate(seq, near):
    hits = [i for i in range(len(RW)-len(seq)+1)
            if RW[i:i+len(seq)] == seq and abs(RAW[i][1]-near) <= 40]
    return hits

def resplit(s):
    lo, hi = s['cut_in'], s['cut_out']
    ws = [w for w in HIS if lo - 0.02 <= w[1] < hi]
    if len(ws) < 3: return None
    seq = [w[0] for w in ws]
    idx = None
    for k in range(len(seq), 2, -1):
        h = locate(seq[:k], s['src_in'])
        if len(h) == 1: idx = h[0]; k_used = k; break
    if idx is None: return None
    offs = np.array([RAW[idx+j][1] - ws[j][1] for j in range(k_used)])
    # a monotone step detector: split where the running median offset jumps
    cuts, base = [], float(np.median(offs[:min(3, len(offs))]))
    parts = [[0, base]]
    for j in range(1, k_used):
        if offs[j] - parts[-1][1] > STEP:
            parts.append([j, float(np.median(offs[j:min(j+3, k_used)]))])
    if len(parts) == 1 and abs(parts[0][1] - (s['src_in']-lo)) < 0.10:
        return None                                   # already right
    out = []
    for p, (j, off) in enumerate(parts):
        a = lo if p == 0 else round(ws[j][1] - 0.04, 3)
        b = hi if p == len(parts)-1 else round(ws[parts[p+1][0]][1] - 0.04, 3)
        if b - a < MINDUR and out:                    # fold a runt into the previous part
            out[-1]['cut_out'] = b; out[-1]['src_out'] = round(out[-1]['src_in']+(b-out[-1]['cut_in']),3)
            continue
        out.append(dict(cut_in=round(a,3), cut_out=round(b,3),
                        src_in=round(a+off,3), src_out=round(b+off,3)))
    for a, b in zip(out, out[1:]): a['cut_out'] = b['cut_in']
    out[0]['cut_in'] = lo; out[-1]['cut_out'] = hi
    for x in out: x['src_out'] = round(x['src_in'] + (x['cut_out']-x['cut_in']), 3)
    return out if len(out) > 1 or abs(out[0]['src_in']-s['src_in']) > 0.10 else None

if __name__ == '__main__':
    S = json.load(open('edl_final.json'))
    new, changed = [], 0
    for s in S:
        r = resplit(s)
        if r:
            changed += 1
            print(f"seg {s['i']:3d} cut {s['cut_in']:7.2f}-{s['cut_out']:7.2f} src {s['src_in']:7.2f}"
                  f"  ->  {len(r)} part(s): " +
                  ' | '.join(f"{x['cut_in']:.2f}-{x['cut_out']:.2f}@{x['src_in']:.2f}" for x in r))
            for x in r: new.append(dict(x, i=len(new), resplit=True))
        else:
            new.append(dict(s, i=len(new)))
    tot = sum(x['cut_out']-x['cut_in'] for x in new)
    for a, b in zip(new, new[1:]): assert abs(a['cut_out']-b['cut_in']) < 1e-6, (a['i'], b['i'])
    print(f'\n{changed} segments resplit; {len(S)} -> {len(new)} segments; total {tot:.3f}s')
    assert abs(tot-232.768) < 0.01
    json.dump(new, open('edl_resplit.json','w'), indent=1)
