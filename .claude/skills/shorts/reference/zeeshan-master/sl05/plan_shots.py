#!/usr/bin/env python3
"""SL-04 picture plan -> shots/manifest.json (the file render.js reads).

Picture is planned in OUTPUT time and quantised to the 29.97 frame grid so shot lengths
cannot accumulate rounding drift against the continuous audio. Each shot names its SOURCE
start; for a lip-synced shot that is piece.start + (T - piece_out_start).

Windows (source px, subject.json / gfx.json measurements, 2026-09-24):
  full : 724x1080 from row 0 -> 1080x1610 (1.49x). Hair touches row 0-12 on every shot, so
         y0 is 0: nothing the camera captured above his hair is cropped.
  zoom : 530x790 from row 0 -> 1080x1610 (2.04x). Excludes Zeeshan's lower-third band
         (rows 804-907) WHOLE, so a pill is never sliced. Used only on WIDE shots: on a
         medium shot rows 0-790 end at his hips and the caption band would sit on his abs.
  card : the whole 16:9 frame on the stage, for moments whose burned graphic is the content
         and cannot survive any 9:16 window (the workout-structure chip stack, the #3 pill on
         a medium shot, the live-round timer + exercise pill with arms spanning 0.12-0.84).
"""
import json
FPS = 30000 / 1001
segs = json.loads(__import__('subprocess').check_output(
    ['node', '-e', "console.log(JSON.stringify(require('./segments.js').SEGMENTS))"]))
P = {s['id']: s['pieces'] for s in segs}

def src2out(seg, t):
    """map a source time inside a piece of `seg` to output time"""
    off = 0
    for p in P[seg]:
        if p['start'] - 1e-6 <= t <= p['end'] + 1e-6: return off + t - p['start']
        off += p['end'] - p['start']
    raise ValueError(f'{seg}: {t} not in any piece')

# (seg, source-start-of-shot, treatment, window, x-centre px, note, label, opts). A shot runs until the
# next row's start. `lcut:<src in a piece>:<picture src>` rows start at the output frame of the first number but show
# the picture from the second (not lip-synced; B-roll only). F(n) = the source time of frame n.
#
# SL-05 ROUND 2 LAYOUT, after the five independent reviews of the first build (r2/review/S*/ROUND-1-REVIEW.md), which
# all rejected Dan shown small in an inset card on black while a key point was up (up to 58% of a short; VIDEO-RULES
# "Short-form footage fills the vertical frame"):
#  * Dan talking is ALWAYS a full-height window. FULL = 724x1080 from row 0 (1.49x). PUNCH = 527x786 from row 0
#    (2.05x; a 1.37x step, his medium then reads like Zeeshan's own close). Hair at source row 0 (accepted by Dan).
#  * Zeeshan's lower-centre pill (rows 762-967) would be sliced by any window, so OUR key-point bar covers it: a
#    full-width olive bar (his colours and font, his words) at exactly his pill's rows, on from 0.35 s before his pill
#    is visible to 1.2 s after its last 5% frame (round 2: at 0.5 s his ghost still showed through our fade, short 5) (BARS below). The bar is our graphic, so it also holds across a PUNCH
#    (rows 0-786, where his pill is out of the window) and under a K card.
#  * K card (stock / AI clip that carries his pill): rows 0-778 or less, 1080 wide at y420, the bar at the same place.
#  * W card (exercise demos, AI clips without a pill, Dan's lat demo): the whole 16:9 frame at y420.
#  * Every inherited same-framing jump cut in Zeeshan's footage (r2/jumps.py: face-band frame-difference spikes the
#    full-rate cut finder missed) gets a FULL<->PUNCH step on its exact frame.
#  * Zeeshan's animated zooms between medium and close: the window glides (slideFrom, 14 frames, cosine) from the
#    medium's head centre to the close's, starting 7 frames before the zoom's middle, instead of one shared window
#    that left Dan up to 186 px off centre (short 3 review).
import os
SAMPLE = False
F = lambda n: n / FPS
K = {'cardCrop': [0.0, 1.0, 0.0, 0.72], 'cardY': 420}
W = {'cardY': 420}
NONE = {'grade': 'none'}
PUNCH = {'cw': 527, 'ch': 786}
PUNCH13 = {'cw': 556, 'ch': 830}   # 1.30x, where his pill is not up: the gate's push row counts holds within 1.40x of the dominant level
def k(**o): return {**K, **o}
def w(**o): return {**W, **NONE, **o}
def kx(x0, **o): return {**K, 'cardCrop': [x0, round(x0 + 1170 / 1920, 4), 0.0, 0.72], **o}   # K cropped to 1170 px of width: 1080x718 instead of a 438 px strip (round-2 review)

def med(**o): return {'cam': 'medium', **o}
def clo(**o): return {'cam': 'close', **o}
def glide(frm, n=14, **o): return {'slideFrom': frm, 'slideFrames': n, **o}
Z = 7 / FPS   # a glide starts 7 frames before the middle of his zoom
PLAN = {
 'S1': [
  (117.27, 'talk', 'mid', 1021, "medium; head c 974-1075. Opens on 'Number one drawback...' after Zeeshan's zoom blur (round-1 build held a ghost frame under 'The')", None, med()),
  (F(3731), 'card', None, None, "K, 1170 px wide around the hand (x480-1650): Zeeshan's stock photo; his KEY POINT pill is cropped out and our bar carries it", None, kx(0.25, grade='none')),
  (F(4029), 'talk', 'punch', 999, "medium, PUNCH (card -> punch); the bar holds until his pill is gone (136.50)", None, med(**PUNCH)),
  (193.40, 'talk', 'full', 970, "medium, FULL: the piece join 139.75|193.40 is punch -> full (1.37x); bar 'An Injury Costs You Months...' 195.18-198.57", None, med()),
  (210.551 - Z, 'talk', 'full', 1035, "Zeeshan's animated zoom to his close (head 458 px vs 330); the window glides 970 -> 1035 with it. Head c 958-1108 in the close", None, clo(**glide(970))),
  (223.631 - Z, 'talk', 'full', 1000, "his zoom back out to the medium (0.5 s); glide 1035 -> 1000", None, med(**glide(1035))),
  (F(6717), 'card', None, None, "K: Zeeshan's AI clip (man quitting on a bench; '*AI Generated' top-left kept whole), bar 'Most People Who Quit The Gym Quit Because Of An INJURY'. The card is the left 1170 px (label and the man, who sits at x~860)", None, kx(0.0, grade='none')),
 ],
 'S2': [
  (0.45, 'card', None, None, "W: Zeeshan's AI cold open (deadlift, '*AI Generated' top-left) on 'Stop doing deadlifts.'", None, w()),
  (F(32), 'card', None, None, "W (same box): second AI deadlift shot. It runs 0.5 s past the piece join (source 2.95-3.45 of the same AI clip) so Zeeshan's zoom blur-in on Dan (240.74-241.25) is never shown; 'Now,' plays over it", None, w()),
  (241.27, 'talk', 'mid', 979, "medium, MID (1.2x), first sharp frame after the blur; head c 928-1020", None, med()),
  (249.40, 'talk', 'full', 979, "FULL from the speech gap 248.96-249.63, as the bar 'Over 40, One Bad Injury...' comes on (249.80-262.10): the one framing change of our own on his continuous take (the push_coverage gate row)", None, med()),
  (271.371, 'talk', 'full', 996, "Zeeshan's animated zoom to his close (271.37-271.9); glide 979 -> 996. Bar 'Lower Risk Exercises Build MORE MUSCLE...' from 272.52 to the end. The last 16 frames fade to the field over Zeeshan's blur-out (287.9 on) while 'exercises.' finishes", None, clo(**glide(979), fadeOutV=16)),
 ],
 'S3': [
  (295.68, 'talk', 'full', 1036, "medium; his KEY POINT pill is up at the in-point, so our bar is on from frame 0", None, med()),
  (F(8929), 'card', None, None, "K (rows 0-745, above his pill's top row 771): Zeeshan's AI powerlifter clip, '*AI Generated' kept whole; the bar holds to 303.80", None, {'cardCrop': [0.0, 1.0, 0.0, 0.69], 'cardY': 420, 'grade': 'none'}),
  (F(9161), 'broll', 'full', 1040, "Zeeshan's stock pec close-up, no text: a full-bleed window (x678-1402, right of the AI label that fades across the cut)", None, NONE),
  (F(9249), 'talk', 'mid', 1060, "medium after his one-frame white flash; head c 1033-1063", None, med()),
  (F(9311), 'card', None, None, "W: Zeeshan's AI 'fitness model' clip, '*AI Generated' whole", None, w()),
  (F(9395), 'card', None, None, 'W (same box): second AI shot', None, w()),
  (321.60, 'talk', 'full', 1028, "medium: the context line 'there are ways with your deadlift that you can counteract that' (added in round 2)", None, med()),
  (325.338 - Z, 'talk', 'full', 938, "Zeeshan's animated zoom to his close; glide 1028 -> 938. Head c 889-975", None, clo(**glide(1028, 13))),
  (331.31 - 8 / FPS, 'talk', 'full', 1061, "Zeeshan's zoom-blur back to the medium (331.03-331.6, his transition, kept: Dan is speaking through it); glide 938 -> 1061 inside it. His blur-out from 338.07 plays to the join at 338.46 as his outgoing transition: Dan says 'direction' through it, so no frame is held (a hold froze his mouth) and the word is whole", None, med(**glide(938, 17))),
  (349.88, 'talk', 'punch', 1034, "medium, PUNCH: the piece join 338.46|349.80 is full -> punch (1.37x). Bar 'You Do Not Need Deadlifts To Look Good With Your Shirt Off' 351.90-358.79 holds across it", None, med(**PUNCH)),
 ],
 'S4': [
  (363.56, 'talk', 'full', 1037, "medium; head c 1025-1064. Zeeshan zoom-blurs out from 369.00: the frame at 368.97 is held 7 frames while Dan is silent (gap 369.03-369.23)", None, med(holdTail=7)),
  ('lcut:369.234:%.4f' % F(11207), 'card', None, None, "W: T-bar row stock with his 'Exercise #1: T-Bar Row' pill, in 5 frames early over 'instead?' (its first frame held 5 frames), then frame for frame at source speed: the round-1 build slowed it to 93% and the review saw stutter", None, w(holdHead=5)),
  (F(11363), 'card', None, None, "W (same box): Zeeshan's AI barbell row with his 'Barbell Row' pill and '*AI Generated' label; his white flash starts on its last frame", None, w()),
  (F(11516), 'talk', 'mid', 1019, "medium, MID (1.2x; his head travels x738-1300 here, wider than a PUNCH) from the two flash frames on. Head c 906-1132", None, med()),
  (F(11792), 'talk', 'full', 1040, "Zeeshan's same-framing jump cut 393.46|393.49: MID -> FULL on its frame; then his animated zoom to the close (393.93) and back", None, clo()),
  (398.772 - Z, 'talk', 'full', 1006, "his zoom back out to the medium; glide 1040 -> 1006. Bar 'Exercise #2: Lat Pulldowns' 401.12-402.17", None, med(**glide(1040))),
  (F(12052), 'card', None, None, "W, Dan's own frame whole (graded): Zeeshan's jump cut 402.14|402.17 is full -> card, and the lat demo (he raises each arm and points at his lat, hands x360-1640 and down to row 1000) is whole. His 'Exercise #2' pill is whole inside the card until it fades. The card is x150-1780 of the frame (his raised elbow reaches x1769), 1080x716 at y330", None, {'cardY': 330, 'cardCrop': [0.0781, 0.9271, 0.0, 1.0]}),
  (F(12310), 'talk', 'punch', 1054, "Zeeshan's jump cut 410.71|410.74: card -> PUNCH (1.30x) on its frame; head c ~1054", None, med(**PUNCH13)),
  (F(12369), 'card', None, None, 'W: lat pulldown stock, whole machine and every rep, on "slow controlled motion on screen right now"', None, w()),
  (F(12521), 'talk', 'full', 1009, "medium after his one-frame flash; head c 982-1036. Bar 'Wide Grip Builds WIDTH. Narrow Grip Builds Powerlifter THICKNESS.' 419.00-427.03. Zeeshan's own zoom-blur between two takes plays at 421.2-421.9 (his transition, kept)", None, med()),
 ],
 'S5': [
  (427.90, 'talk', 'full', 1015, "medium; head c 994-1034. Bar 'Leg Presses Build Nearly The Same Legs With Almost NONE Of The Risk' 429.18-433.57", None, med()),
  (431.371 - Z, 'talk', 'full', 1048, "Zeeshan's animated zoom to his close; glide 1015 -> 1048", None, clo(**glide(1015))),
  (436.376 - Z, 'talk', 'full', 998, "his zoom back to the medium; glide 1048 -> 998. Bar 'Leg Presses' 435.82-439.10", None, med(**glide(1048))),
  (F(13092), 'talk', 'punch', 998, "Zeeshan's jump cut 436.80|436.84: FULL -> PUNCH on its frame (the bar holds)", None, med(**PUNCH)),
  (F(13172), 'card', None, None, 'W: the leg press stock, whole frame (the round-1 build cropped it into a 437 px strip)', None, w()),
  (F(13449), 'talk', 'full', 1027, "medium, FULL, from his one-frame flash; head c 971-1101", None, med()),
  (F(13556), 'talk', 'punch', 1027, "Zeeshan's jump cut 452.29|452.32: FULL -> PUNCH (1.30x)", None, med(**PUNCH13)),
  (F(13651), 'talk', 'full', 1027, "Zeeshan's jump cut 455.46|455.49: PUNCH -> FULL", None, med()),
  (F(13776), 'talk', 'mid', 1027, "Zeeshan's jump cut 459.63|459.66: FULL -> MID (1.2x), a punch-in that his own zoom to the close then continues (the round-2 build stepped out to FULL for 0.23 s before his zoom in: a flicker)", None, med()),
  (460.099 - 5 / FPS, 'talk', 'mid', 1075, "his animated zoom to the close inside the MID window; glide 1027 -> 1075", None, clo(**glide(1027, 12))),
  (464.05, 'talk', 'full', 1054, "close, FULL: the junk cut 463.70|464.05 ('but, but') joins close to close, so the second side steps OUT 1.2x (the round-2 build stepped in and his ear left the frame)", None, clo()),
  (466.219 - Z, 'talk', 'full', 990, "his zoom out to the medium over the last 0.3 s; glide 1054 -> 990", None, med(**glide(1054))),
 ],
}
# OUR key-point bars. id -> (seg, lines, his pill's rows (r2 measure), on (source s), off (source s; None = end of short))
BARS = {
 'S1-kp1': ('S1', (795, 937), F(3731) - 0.03, 137.70),
 'S1-kp2': ('S1', (794, 937), 195.18, 199.27),
 'S1-kp3': ('S1', (795, 937), F(6717) - 0.03, None),
 'S2-kp1': ('S2', (806, 932), 249.80, 262.10),
 'S2-kp2': ('S2', (762, 967), 272.52, None),
 'S3-kp1': ('S3', (771, 896), 295.68, 304.50),
 'S3-kp2': ('S3', (794, 937), 351.90, 359.50),
 'S4-ex2': ('S4', (828, 903), 401.12, F(12052) - 0.02),
 'S4-kp1': ('S4', (794, 937), 419.00, None),
 'S5-kp1': ('S5', (794, 937), 429.18, 434.27),
 'S5-ex3': ('S5', (828, 903), 435.82, 439.10),
}
man, labels = [], {}
for seg, rows in PLAN.items():
    total = sum(p['end'] - p['start'] for p in P[seg])
    # Frame-exact mapping (round 2): each piece's output frames map 1:1 onto source frames from the piece's first
    # source frame, so a hard cut in the source lands exactly on our shot boundary (round-1 plans rounded output
    # time instead, and `-ss` then returned the frame AFTER a cut: a 1-frame flash of the next shot, r2/cutframe.py).
    pf, off = [], 0.0
    for p_ in P[seg]:
        pf.append((p_['start'], p_['end'], round(p_['start'] * FPS), round(off * FPS))); off += p_['end'] - p_['start']
    def fmap(t):
        for a, b, sp, fp in pf:
            if a - 1e-6 <= t <= b + 1e-6: return fp + round(t * FPS) - sp
        raise ValueError(f'{seg}: {t} not in any piece')
    starts = []
    for r in rows:
        k = r[0]
        if isinstance(k, str) and k.startswith('lcut:'):
            _, out_at, src = k.split(':'); f0 = fmap(float(out_at)); S = float(src)
        else:
            f0 = fmap(k); S = k
        starts.append((f0, S, r))
    starts.sort(key=lambda x: x[0])
    total_f = round(total * FPS)
    for i, (f0, S, r) in enumerate(starts):
        f1 = starts[i + 1][0] if i + 1 < len(starts) else total_f
        name = f'{seg}-s{i:02d}'
        e = {'seg': seg, 'name': name, 'absStart': round(S, 3), 'ss': round((round(S * FPS) - 0.3) / FPS, 5), 'frames': f1 - f0, 'dur': round((f1 - f0) / FPS, 4),
             'outStart': round(f0 / FPS, 4), 't': r[1], 'why': r[4]}
        if r[1] in ('talk', 'broll'): e.update(win=r[2], xc=r[3])
        if len(r) > 5 and r[5]: labels[name] = r[5]
        if len(r) > 6: e.update(r[6])
        man.append(e)
    print(seg, 'frames', total_f, '=', sum(m['frames'] for m in man if m['seg'] == seg))
json.dump(man, open('shots/manifest.json', 'w'), indent=1)
json.dump(labels, open('shots/labels.json', 'w'), indent=1)
OV = {'note': 'SL-05 round 2: our key-point bars (pill/make_pill5.py), full width, at the rows of Zeeshan\'s pill. Output time, written by plan_shots.py.'}
bar_geo = {}
for pid, (seg, rows, on, off) in BARS.items():
    t0 = max(0.0, src2out(seg, on)); tot = sum(p_['end'] - p_['start'] for p_ in P[seg])
    t1 = tot if off is None else src2out(seg, off)
    y = round(310 + (rows[0] - 9) * 1080 / 724); h = round((rows[1] - rows[0] + 18) * 1080 / 724); bar_geo[pid] = [y, h]
    hard_off = off is None or pid == 'S4-ex2'
    OV.setdefault(seg, []).append({'id': pid, 'png': f'pill-{pid}.png', 't0': round(t0, 3), 't1': round(t1, 3),
        'fadeIn': 0.001 if t0 < 0.01 or pid in ('S1-kp1',) else 0.15, 'fadeOut': 0.001 if hard_off else 0.15, 'y': y, 'h': h,
        'why': f'his pill rows {rows[0]}-{rows[1]} -> bar y{y}-{y + h}'})
json.dump(bar_geo, open('pill/bar_geo.json', 'w'))
json.dump(OV, open('overlays.json', 'w'), indent=1)
for m in man: print(f"{m['name']} out {m['outStart']:6.2f} src {m['absStart']:8.3f} {m['frames']:4d}f {m['t']:4s} {m.get('win','')} {m.get('xc','')}")
