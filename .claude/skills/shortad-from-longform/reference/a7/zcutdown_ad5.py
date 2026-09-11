#!/usr/bin/env python3
"""The <=0:59 cutdown PLAN: interval selection over the approved master (never a re-cut from source).

Ad 5's cutdown (2026-09-10): hook (why diets fail / what I looked like), proof (today), mechanism (the strange AI trick,
the lock screen), the shift (wish -> fact -> where I'm at today), CTA, one nutrition-coach beat, CTA again. Skill [R1]: the transcript is printed and read as
prose FIRST; every seam is a sentence AND a thought boundary.

Edge rules, each one paid for on this build:
  * sentences contiguous in the master are ONE range (a seam there is a cut that removes nothing);
  * an edge may only move AWAY from the words. A start snaps to a beat/picture edge that sits BEFORE the pre-rolled
    first word; if the nearest edge sits just AFTER the word onset (the pool card starts 0.18 s into "You're"), the
    PICTURE keeps the edge and the AUDIO LEADS it by a few frames -- a J-cut, taking those frames out of the previous
    range's silent tail so the total stays exact. Snapping forward cut "You're" off the first draft of this plan;
  * an end snaps to a beat edge OR one of his picture cuts at least 50 ms after the last word: ending one frame past a
    picture cut leaks a one-frame shot into the seam;
  * a seam with TALK on both sides flips the incoming hold's level (FAR<->NEAR): the framing standard never lets a join
    between two takes of the talking head go out as a naked jump cut.
Writes cut_plan.json and prints the prose, the seams and the total (asserted <= 59.0 s)."""
import json, re, sys
sys.path.insert(0, '.')
import beats as B
FPS = 30000/1001
W = [(w['word'], float(w['start']), float(w['end'])) for w in json.load(open('words_ctc.json')) if w['word'].strip()]
norm = lambda s: re.sub(r"[^a-z0-9 ]", '', s.lower().replace("'", '').replace('-', ' '))
toks = []
for i, (w, s, e) in enumerate(W):
    for t in norm(w).split(): toks.append((t, i))
def find(phrase, after=0.0):
    p = norm(phrase).split()
    for k in range(len(toks) - len(p) + 1):
        if [toks[k+j][0] for j in range(len(p))] == p and W[toks[k][1]][1] >= after:
            return toks[k][1], toks[k+len(p)-1][1]
    raise SystemExit(f'phrase not found: {phrase!r} after {after}')
def at(ph, after=0.0): return W[find(ph, after)[0]][1]
def end(ph, after=0.0): return W[find(ph, after)[1]][2]
RANGES = [
 (0.0,                                            end('to eat healthy')),
 (at('but this is what i look like today'),       end('i look like today')),
 (at('i just used this one strange'),             end('work far better for me')),
 (at('i generated an ai picture'),                end('for over a year')),
 (at('and at some point'),                        end('where im at today')),
 (at('generate an ai picture of yourself'),       end('to see your future self')),
 (at('your ai nutrition coach'),                  end('every single meal')),
 (at('take the first step now'),                  end('future self image')),
 (at('tap the button below to get started'),      B.DUR),
]
merged = []
for a, b in RANGES:
    if merged and a - merged[-1][1] < 0.7: merged[-1] = (merged[-1][0], b)
    else: merged.append((a, b))
PRE, POST = 0.10, 0.16
tl, _ = B.timeline()
EDL = json.load(open('edl_picture.json'))
EDGES = sorted({0.0, B.DUR} | {x for b in tl for x in (b['t0'], b['t1'])} | {s['n0']/FPS for s in EDL})
kind_at = lambda n: next(b['kind'] for b in tl if b['n0'] <= n < b['n1'])
plan = []
for a, b in merged:
    lead = 0
    if a <= 0: p0 = 0
    else:
        s = a - PRE
        before = [e for e in EDGES if s - 0.30 <= e <= a - 0.03]
        after_ = [e for e in EDGES if a - 0.03 < e <= a + 0.25]
        if before: p0 = int(round(max(before)*FPS))
        elif after_:
            p0 = int(round(min(after_)*FPS)); lead = max(1, int(-(-(p0/FPS - s)*FPS // 1)))   # ceil, frames
        else: p0 = int(round(s*FPS))
    if b >= B.DUR: p1 = B.NTOT
    else:
        # his cut may land within a couple of frames of the word's end (a hard cut right after the line): an edge in
        # [b-0.10, b+0.30] wins over b+POST, so the range never leaks the first frames of the next beat (a title card typing on)
        ends = [e for e in EDGES if b - 0.10 <= e <= b + 0.30]
        p1 = int(round((min(ends, key=lambda e: abs(e - b - 0.08)) if ends else b + POST)*FPS))
    plan.append(dict(p0=p0, p1=p1, lead=lead, words=(round(a, 3), round(b, 3))))
c = 0
for i, p in enumerate(plan):
    p['c0'] = c; c += p['p1'] - p['p0']; p['c1'] = c
    assert i == 0 or p['p0'] >= plan[i-1]['p1'], 'ranges overlap'
# the audio window of range i is [p0 - lead_i + tail_{i-1}, p1 - lead_{i+1} + tail_i): a J-cut lead lets the next range's
# audio start early; an L-cut TAIL lets a word that ends a few frames past his picture cut ("...future self." under the
# title card's first frames) finish over the next range's first frames instead of being clipped. No word may be lost.
import math
for i, p in enumerate(plan):
    over = [e for w, s, e in W if s < p['p1']/FPS - 0.02 and e > p['p1']/FPS + 0.005]
    p['tail'] = (int(math.ceil((max(over) - p['p1']/FPS)*FPS)) + 1) if (over and i + 1 < len(plan)) else 0
for i, p in enumerate(plan):
    nxt = plan[i+1]['lead'] if i + 1 < len(plan) else 0
    prev_tail = plan[i-1]['tail'] if i > 0 else 0
    p['a0'], p['a1'] = p['p0'] - p['lead'] + prev_tail, p['p1'] - nxt + p['tail']
    cut_words = [w for w, s, e in W if p['a1']/FPS < e - 0.005 and s < p['p1']/FPS - 0.02]
    assert not cut_words, f'range {i}: the seam drops spoken words {cut_words}'
    early = [w for w, s, e in W if p['p0']/FPS <= s < p['a0']/FPS]
    assert not early, f'range {i}: the previous range\'s tail covers its own words {early}'
# talk-to-talk seams flip the incoming level
for i in range(1, len(plan)):
    a, b = plan[i-1]['p1'] - 1, plan[i]['p0']
    plan[i]['flip'] = kind_at(a) == 'talk' and kind_at(b) == 'talk'
plan[0]['flip'] = False
print('THE CUTDOWN, READ AS PROSE:\n')
for p in plan:
    txt = ' '.join(w for w, s, e in W if p['a0']/FPS - 0.02 <= s and e <= p['a1']/FPS + 0.05)
    print(f"  pic [{p['p0']/FPS:7.2f}-{p['p1']/FPS:7.2f}] audio lead {p['lead']}f tail {p['tail']}f{'  FLIP' if p['flip'] else ''}\n      {txt}")
tot = plan[-1]['c1']
print(f'\n{len(plan)} ranges, {tot} frames = {tot/FPS:.2f} s')
for i in range(1, len(plan)):
    print(f"  seam {i}: {kind_at(plan[i-1]['p1']-1)} -> {kind_at(plan[i]['p0'])}{'  (level flipped)' if plan[i]['flip'] else ''}")
assert tot/FPS <= 59.0, f'CUTDOWN IS {tot/FPS:.2f}s -- Shorts ads must never exceed 0:59'
json.dump(plan, open('cut_plan.json', 'w'), indent=1)
