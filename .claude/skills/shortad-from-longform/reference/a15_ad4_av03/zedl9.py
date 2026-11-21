#!/usr/bin/env python3
"""AV-03 round 1 review (2026-10-03): the picture EDL on HIS PICTURE's frames (skill A12.1, A5.13).

Two faults of the 09-11 conform, both measured in the build's own pic.json (his frame n -> the raw frame k it shows):
  1 every segment's offset came from the ACOUSTIC profile, which sits 2.05 frames behind his picture in 54 of 55 measured
    segments (his export's audio trails his picture by two frames). Our talking head therefore ran two frames late
    against the approved master for the whole film. The acoustic offset is kept for its precision and the constant added:
    d = round(off * FPS + 2.05), so our frame n shows the raw frame his frame n shows.
  2 nine talk-to-talk cuts sat on his AUDIO splice. His picture cuts later, on a pose-matched frame, or simply holds the
    outgoing take until the next insert or flash hides the change. Each boundary now sits where pic.json's d steps from
    the outgoing segment's value to the incoming one's; where it never steps before the insert, the outgoing take is held
    to the insert, as he does.
Writes edl_picture.json (the old one is kept as edl_picture_acoustic.json) and prints every boundary that moved."""
import json, os, sys, numpy as np
sys.path.insert(0, '.')
FPS = 30000/1001; BIAS = 2.05
import beats as B
src = 'edl_picture_acoustic.json' if os.path.exists('edl_picture_acoustic.json') else 'edl_picture.json'
E = json.load(open(src))
if src == 'edl_picture.json': json.dump(E, open('edl_picture_acoustic.json', 'w'))
P = {o['n']: o for o in json.load(open('pic.json'))}
tl, _ = B.timeline(); BASE = set()
for b in tl:
    if b['kind'] in ('talk', 'window'): BASE.update(range(b['n0'], b['n1']))
FR = {}                                             # his framing per frame (a property of HIS timeline, not of a segment)
for s in E:
    for k, f in enumerate(s['framing']): FR[s['n0'] + k] = f
D = [int(round(s['off']*FPS + BIAS)) for s in E]
# the 09-11 list split some takes at a beat edge (1264, 5905, 928): one take is one segment here
_E, _D = [], []
for s, d in zip(E, D):
    if _E and _D[-1] == d and _E[-1]['n1'] == s['n0']: _E[-1] = dict(_E[-1], n1=s['n1'])
    else: _E.append(dict(s)); _D.append(d)
E, D = _E, _D
def cls(n, d):
    o = P.get(n)
    return o is not None and o.get('d') is not None and o['r'] >= 0.90 and abs(o['d'] - d) <= 1
bounds = [s['n0'] for s in E] + [E[-1]['n1']]
moved = []
for i in range(1, len(E)):
    j = E[i]['n0']
    if E[i-1]['n1'] != j or (j - 1) not in BASE or j not in BASE: continue        # an insert already sits between them
    dA, dB = D[i-1], D[i]
    if abs(dA - dB) <= 2: continue
    lo = max(bounds[i-1], j - 30); hi = j
    while hi in BASE and hi < E[i]['n1'] and hi < j + 240: hi += 1             # the end of this continuous stretch of his picture
    a = [n for n in range(lo, hi) if cls(n, dA)]; b = [n for n in range(lo, hi) if cls(n, dB)]
    if j - bounds[i-1] < 12 and (bounds[i-1] - 1) not in BASE and not a:      # round 2 review: 639-647 was 8 frames of the OLD take
        early = [n for n in range(bounds[i-1], j) if P.get(n) and P[n].get('d') is not None and P[n]['r'] >= 0.85 and abs(P[n]['d'] - dB) <= 1]
        if len(early) >= 2: bounds[i] = bounds[i-1]; moved.append((j, bounds[i-1], dA, dB, 'his picture is already on the incoming take when the insert ends')); continue
    if not b: c = hi                                                           # he never shows the incoming take here: hold to the insert
    else:
        c = min(n for n in b if not any(x > n for x in a)) if any(not any(x > n for x in a) for n in b) else b[0]
        # unreadable frames between the last outgoing and the first incoming frame are a window wiping off or a flash: the
        # cut is the first frame that READS as the incoming take (1267 and 5912, where his window slides away over the cut)
        if c - bounds[i-1] <= 3: c = bounds[i-1]              # a 1-3 frame sliver of the outgoing take (inside his flash at 4792): none
    if abs(c - j) <= 1: c = j                                  # the matcher's own +-1 frame jitter is not a moved cut
    if hi - c < 4 and hi < E[i]['n1'] + 1 and b and (hi not in BASE): c = hi     # a 1-3 frame sliver of the new take before an insert: hold to the insert
    if c != j: moved.append((j, c, dA, dB, 'held to the insert' if c == hi and hi not in BASE else ''))
    bounds[i] = c
out = []
for i, s in enumerate(E):
    n0, n1 = bounds[i], (bounds[i+1] if i + 1 < len(E) and E[i]['n1'] == E[i+1]['n0'] else s['n1'])
    n0 = max(n0, s['n0']) if (i == 0 or E[i-1]['n1'] != s['n0']) else n0
    if n1 - n0 <= 0: print(f"  segment {s['n0']}-{s['n1']} (d {D[i]}) is never shown in his picture: dropped"); continue
    off = D[i]/FPS
    out.append(dict(n0=n0, n1=n1, t0=round(n0/FPS, 4), t1=round(n1/FPS, 4), off=off, d=D[i], src_in=round(n0/FPS + off, 4),
                    framing=[FR.get(n, [1.0, 0.0, 0.0]) for n in range(n0, n1)], framing_mode=s.get('framing_mode'), run=s.get('run')))
# ---- ROUND 2 REVIEW: two stretches where his picture is not one constant-offset run -----------------------------------
# THE HOOK (0-85). The acoustic profile and his mouth (zlips.py) both show two micro pause trims: in step with d 266 through
# frame 50, then two frames behind by 60 and three by 76-84 (the reviewer read the same off his mouth: closes on our 60 /
# his 62, opens on our 76 / his 79). Cuts in the word gaps after "money" (44.7-54.9) and after "on" (56.7-61.0).
# THE CLOSING SHOT (7100-7160). After "started." his picture slows to about 40 %: it advances one raw frame every two or
# three of his frames (his256.gray: frame-to-frame change 0.5-1.1, then ~0.0, ~0.0, repeating), so Dan holds his smile at
# the camera under the pill. Ours ran on in real time into him turning away. kmap = the raw frame for each of his frames,
# advanced exactly where HIS picture changes.
import numpy as _np
_G = _np.memmap('his256.gray', _np.uint8, 'r').reshape(-1, 144, 256)
def _chg(n): return float(_np.abs(_G[n, :90].astype(_np.int16) - _G[n-1, :90].astype(_np.int16)).mean())
def _split(out, n0, pieces, micro=True):
    i = next(k for k, s in enumerate(out) if s['n0'] <= n0 < s['n1']); s = out[i]; new = []
    for a, b, d in pieces:
        new.append(dict(s, n0=a, n1=b, t0=round(a/FPS, 4), t1=round(b/FPS, 4), off=d/FPS, d=d, src_in=round(a/FPS + d/FPS, 4),
                        framing=[FR.get(n, [1.0, 0.0, 0.0]) for n in range(a, b)], micro=bool(micro and a != s['n0'])))
    assert new[0]['n0'] == s['n0'] and new[-1]['n1'] == s['n1']
    out[i:i+1] = new
_split(out, 0, [(0, 50, 266), (50, 59, 264), (59, 85, 263)])
_e = next(s for s in out if s['n0'] <= 7100 < s['n1']); assert _e['d'] == 3005 and _e['n1'] == 7160
_split(out, 7100, [(_e['n0'], 7100, 3005), (7100, 7160, 3005)])
_k = [7099 + 3005]
for n in range(7100, 7160): _k.append(_k[-1] + (1 if _chg(n) >= 0.25 else 0))
out[-1]['kmap'] = _k[1:]; out[-1]['micro'] = True
print(f"closing shot: his frames 7100-7159 show raw {_k[1]}..{_k[-1]} ({_k[-1]-_k[1]+1} raw frames over 60: {(_k[-1]-_k[1])/59:.2f}x)")
# contiguity inside the base beats
for a, b in zip(out[:-1], out[1:]):
    assert b['n0'] >= a['n1'], (a['n0'], a['n1'], b['n0'])
json.dump(out, open('edl_picture.json', 'w'))
print(f'{len(E)} -> {len(out)} segments; every offset +{BIAS} frames (his picture); boundaries moved:')
for j, c, dA, dB, why in moved: print(f'  {j} -> {c}  ({c-j:+d} frames; d {dA} -> {dB}) {why}')
