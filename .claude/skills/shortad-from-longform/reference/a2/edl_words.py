#!/usr/bin/env python3
"""Re-derive every segment's src_in from WORD alignment, not envelope correlation.

The envelope is ambiguous on windows under ~2 s (Dan repeats lines across takes, so a
different take often scores higher). Words are not: take his words inside the cut range,
find that exact run in the raw roll's own transcript, and read the offset off it.

This is what found the four clipped words the envelope check only hinted at -- "With AI",
"your life", "screen" and "belly fat" were each falling into the gap between two
recovered in/out points.
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

def find_run(seq, near, span=40.0):
    """All raw positions where `seq` occurs, preferring those near `near` seconds."""
    hits = []
    for i in range(len(RW)-len(seq)+1):
        if RW[i:i+len(seq)] == seq and abs(RAW[i][1]-near) <= span:
            hits.append(i)
    return hits

def fit_segment(s):
    lo, hi = s['cut_in'], s['cut_out']
    ws = [w for w in HIS if lo - 0.02 <= w[1] < hi]
    if len(ws) < 3: return None
    seq = [w[0] for w in ws]
    for k in range(len(seq), 2, -1):          # longest run that occurs exactly once
        sub = seq[:k]
        hits = find_run(sub, s['src_in'])
        if len(hits) == 1:
            i = hits[0]
            offs = [RAW[i+j][1] - ws[j][1] for j in range(min(k, 6))]
            off = float(np.median(offs))
            last = RAW[i+k-1][2]
            return dict(off=off, src_in=round(lo + off, 3), n=k,
                        spread=round(max(offs)-min(offs), 3),
                        covers_last=bool(lo + off + (hi-lo) >= last - 0.02),
                        raw_last_end=last)
    return None

if __name__ == '__main__':
    S = json.load(open('edl_final.json'))
    fixes = []
    for s in S:
        r = fit_segment(s)
        if not r: continue
        d = r['src_in'] - s['src_in']
        bad = abs(d) > 0.10 or not r['covers_last']
        if bad:
            fixes.append((s['i'], s['src_in'], r))
            print(f"seg {s['i']:3d} cut {s['cut_in']:7.2f}-{s['cut_out']:7.2f}  src {s['src_in']:8.2f} -> "
                  f"{r['src_in']:8.2f}  ({d:+.2f}s, {r['n']} words, spread {r['spread']:.2f}"
                  f"{'' if r['covers_last'] else ', TAIL CLIPPED'})")
    print(f'\n{len(fixes)} of {len(S)} segments need correcting')
    json.dump([dict(i=i, old=o, new=r['src_in'], n=r['n'], spread=r['spread'],
                    covers_last=r['covers_last']) for i, o, r in fixes],
              open('ref_audit/edl_word_fixes.json','w'), indent=1)
