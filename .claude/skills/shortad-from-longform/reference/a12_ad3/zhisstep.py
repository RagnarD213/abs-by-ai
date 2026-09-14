#!/usr/bin/env python3
"""For every talk-to-talk picture cut, find HIS picture cut frame and snap ours to it.

Two independent things decide where a cut belongs, and the build got both wrong in places:
  1. HIS step  -- pic.json measures, per frame, the offset (source frame - his frame) he is showing. Where that
     steps from our segment A's offset to segment B's, that is his picture cut. Our EDL instead cut at the AUDIO
     splice, which is 5-15 frames away wherever he used a J/L cut.
  2. A WORD GAP -- the skill's rule. Our 1286 cut landed inside the word "six-pack abs.", so the 9-frame trim it
     carried was spent mid-syllable.
This prints his step, the enclosing word gap, and the frame to use: his step when it is confident and lands in a
gap, otherwise the middle of the nearest gap to it.
"""
import json
import numpy as np

FPS = 30000/1001
WIN = 42


def main():
    P = {p['n']: p for p in json.load(open('pic.json'))}
    E = json.load(open('edl_picture.json'))
    Wd = json.load(open('words_ctc.json'))
    ws = Wd['words'] if isinstance(Wd, dict) and 'words' in Wd else Wd
    spans = [(w['start']*FPS, w['end']*FPS) for w in ws if w.get('start') is not None]
    spans.sort()
    gaps = [(spans[i][1], spans[i+1][0]) for i in range(len(spans)-1) if spans[i+1][0] - spans[i][1] >= 3.0]

    def in_gap(n):
        for a, b in gaps:
            if a <= n <= b: return (a, b)
        return None

    def nearest_gap(n):
        best = None
        for a, b in gaps:
            d = 0 if a <= n <= b else min(abs(n-a), abs(n-b))
            if best is None or d < best[0]: best = (d, a, b)
        return best

    segs = {s['n0']: s for s in E}
    order = sorted(segs)
    print(f"{'cut':>6} {'step':>5} {'hisstep':>8} {'conf':>5} {'gap':>15}  decision")
    out = {}
    for i in range(1, len(order)):
        a, b = segs[order[i-1]], segs[order[i]]
        if a['n1'] != b['n0']: continue
        n = b['n0']; oA, oB = round(a['off']*FPS), round(b['off']*FPS)
        if abs(oB-oA) > 40:                      # a take change: his step is unmistakable, find it the same way
            pass
        lo = max(a['n0']+3, n-WIN); hi = min(b['n1']-3, n+WIN)
        seq = []
        for m in range(lo, hi+1):
            p = P.get(m)
            if not p or p['r'] < 0.85: seq.append((m, '?')); continue
            seq.append((m, 'A' if abs(p['d']-oA) < abs(p['d']-oB) else 'B'))
        s = ''.join(c for _, c in seq)
        best = None
        for j in range(6, len(seq)-6):
            L = s[max(0, j-10):j].replace('?', ''); R = s[j:j+10].replace('?', '')
            if len(L) < 3 or len(R) < 3: continue
            sc = (L.count('A')/len(L)) * (R.count('B')/len(R))
            if best is None or sc > best[0]: best = (sc, seq[j][0])
        conf, hs = (best if best else (0.0, n))
        g = in_gap(hs)
        if conf >= 0.85 and g:
            pick, why = hs, 'his step, in a word gap'
        elif conf >= 0.85:
            d, ga, gb = nearest_gap(hs)
            pick, why = (hs, 'his step (no gap within reach)') if d > 12 else (int(round((max(ga, hs-12)+min(gb, hs+12))/2)), f'his step snapped into gap {int(ga)}-{int(gb)}')
        else:
            d, ga, gb = nearest_gap(n)
            pick, why = (n, 'kept (his step not confident)') if d > 12 else (int(round((ga+gb)/2)), f'no confident step; snapped into gap {int(ga)}-{int(gb)}')
        pick = int(min(max(pick, a['n0']+3), b['n1']-3))
        mark = '' if pick == n else '   <<< MOVE'
        print(f"{n:6d} {oB-oA:5d} {hs:8d} {conf:5.2f} {str(g and (int(g[0]), int(g[1]))):>15}  -> {pick}  ({why}){mark}")
        if pick != n: out[n] = pick
    print(f"\nPIC_CUT_OVERRIDES = {out}")
    json.dump(out, open('hisstep_overrides.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
