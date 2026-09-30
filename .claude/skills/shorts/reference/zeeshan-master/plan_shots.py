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

# (seg, source-start-of-shot, treatment, window, x-centre px, note). A shot runs until the
# next row's start (output time). `lcut` rows name a source start that is NOT lip-synced.
PLAN = {
 'A': [
  (27.60,  'talk', 'zoom', 925, 'wide; the #1 pill (27.6-28.9) is excluded whole by the zoom window'),
  (38.46,  'card', None, None, 'Zeeshan\'s "Large Shoulders Make Your Waist Look Smaller" pill (39.5-41.2) shown whole. Round-2b review: his pill slides in from x0-60, so x173 sliced it for 5 frames; the card now spans x0-1699; runs to the start of his push-in', None, {'cardCrop': [0.0, 0.885, 0, 1], 'cardY': 310}),
  (42.115, 'talk', 'full', 953, "medium, entered through Zeeshan's own 0.5 s push-in (42.115-42.615)", None, {'cam': 'medium'}),
  (50.90,  'talk', 'mid', 953, '1.2x punch on the medium at gap 50.77-51.16 ("even though"); abs stay above the caption band', None, {'cam': 'medium'}),
  # L-CUT over the join: Zeeshan cuts back to a wide at 59.232 mid-"better", and piece 2 opens on a
  # wide too. The picture cuts from the medium straight to the wide that precedes piece 2 (source
  # 212.582-), so there is one picture cut, medium -> wide, instead of wide | wide.
  ('lcut:59.232:212.582', 'talk', 'zoom', 925, 'wide NEAR across the join (L-cut picture). Round 2b: he is bent over picking up the dumbbells 212.58-213.8 (body x594-1112), then upright; the old fixed zoom left him off the left edge (reviewer) and a FULL window showed Zeeshan\'s "Exercise #2" pill sliced (rows 804-907, from 210.97). Custom 536x800 window ends above the pill band holds x825 while he is bent (per-frame person mask: >= 27 px margin both sides, hair/ab) (round-2b review: a glide from the first frame drifted off him), then glides to x925 over 16 frames from 213.80 as he stands', None, {'cw': 536, 'ch': 800, 'slideFrom': 825, 'slideDelay': 36, 'slideFrames': 16}),
  (218.94, 'talk', 'full', 925, 'full body while he sets the weights down (bends to the mat ~220-222); gap 218.34-218.94'),
  (223.327, 'card', None, None, "Zeeshan's medium where he shows the arm angle: his arm reaches x328-1202, wider than any 9:16 window, and the angle IS the lesson; inset card x230-1306 at 1.0x", None, {'cardCrop': [0.12, 0.68, 0, 1], 'cardY': 310, 'cam': 'medium'}),
 ],
 'F': [
  (100.40, 'talk', 'full', 937, 'wide full body opening; frames 0-6 would carry the tail of Zeeshan\'s zoom-blur transition (reviewer, 2026-09-24), so the first clean frame (source 100.634) is held for 7 frames while Dan is still silent (speech from 100.57)', None, {'holdHead': 7}),
  (103.60, 'card', None, None, 'Dan 2026-09-25: Zeeshan\'s "Great Exercise Before A Photo Shoot" pill becomes ours, "Use this 2-minute workout to pump up before a photo shoot", centred. His pill lives in source rows 804-907 on every frame (measured 103.6-106.6, pill/), so the card keeps rows 0-798 only and never shows it, whole or sliced; our pill (overlays.json F-pill) sits on the black field under the card on his beat; gap 103.56-103.65', None, {'cardCrop': [0.09, 0.88, 0, 0.739], 'cardY': 310}),
  (106.60, 'talk', 'full', 937, 'back out after the pill has FULLY faded (its fade runs ~6 frames past the scan; reviewer saw a ghost to 6.14 out)'),
  (109.50, 'talk', 'mid', 937, '1.2x punch-in at gap 109.36-109.73 ("Just take two minutes"); no graphic up. Last 5 frames (source 114.64+) are the head of Zeeshan\'s motion-blur transition, so the last clean frame is held (Dan silent from 114.49)', None, {'holdTail': 5}),
  (458.00, 'card', None, None, 'Zeeshan\'s "How To Do The Workout" pill (458.0-459.4, x553-1362) shown whole; ends at gap 459.93-460.03 before the "Timed Sets" chip (x35-437, from 460.5) would straddle the card edge', None, {'cardCrop': [0.09, 0.88, 0, 1], 'cardY': 310}),
  (460.30, 'talk', 'mid', 925, 'wide at the mid level; window x623-1227 excludes the "Timed Sets" chip (x35-437) whole'),
  (468.10, 'card', None, None, 'round-2 review (twice): the close NEAR shot 468.10-469.01 ended on him looking down at his phone (from 468.74) and the glasses touch; that shot is dropped and the card starts at 468.10 (no Zeeshan chip until 470.1, Dan facing camera). Zeeshan\'s 30s-on chip stack (470.1-478.5, x44-622) with Dan whole while he turns to set his phone down (the NEAR window lost him at 470-474, reviewer). Card x0-1632 holds both; the J2 chips sit UNDER the card on the black field, never on him', None, {'cardCrop': [0, 0.85, 0, 1], 'cardY': 310}),
  (479.00, 'talk', 'full', 892, 'wide after the chips clear; gap 478.88-479.20'),
  (482.024,'talk', 'full', 920, "Zeeshan's own cut to the medium"),
  (515.00, 'card', None, None, 'live round: curls, timer + pill', 'EXERCISE 1 OF 3', {'cardCrop': [0, 0.85, 0, 1], 'cardY': 470}),
  (546.00, 'card', None, None, 'live round: side laterals, arms span 0.12-0.84', 'EXERCISE 2 OF 3', {'cardCrop': [0, 0.85, 0, 1], 'cardY': 470}),
  (575.30, 'card', None, None, 'live round: tricep extensions', 'EXERCISE 3 OF 3', {'cardCrop': [0, 0.85, 0, 1], 'cardY': 470}),
 ],
 'C': [
  (208.90, 'talk', 'full', 1000, 'context line naming the exercise, wide FULL; window x638-1362 holds his gestures (x766-1258); hair 12-30 source px clear (hair/Calt.json)'),
  (210.70, 'talk', 'zoom', 918, 'punch-in on "side laterals" just after gap 210.57-210.65 (round-2 review: from 210.30 it cut his left hand off while he walked across; his centre moves x729->375 in the window). Custom 536x800 window (1.35x vs full, looser than the 530x790 zoom) still ends above Zeeshan\'s "Exercise #2" pill band (rows 804-907, measured from 210.967); x650-1186 holds him: per-frame person mask 210.70-211.37 at 15 fps spans x659-1174 (hair/cz)', None, {'cw': 536, 'ch': 800}),
  (264.22, 'talk', 'full', 930, 'wide full body, upright, fists at chest (a real size step back from the zoom)'),
  (266.00, 'card', None, None, 'wide demo of the elbow positions; Zeeshan\'s top-left chip "Elbow In The Wrong Position" (269.6-272.6, x<=763) and his "Focus On Your Elbow" pill (274.7-281.6) would each straddle any 9:16 window that holds Dan (x626-1238), so the whole frame is shown x0-1690 with both graphics whole', None, {'cardCrop': [0, 0.88, 0, 1], 'cardY': 310}),
  (283.022, 'card', None, None, "Zeeshan's medium: arms out to x360-1540 while he compares elbow low vs high; inset card x326-1574", None, {'cardCrop': [0.17, 0.82, 0, 1], 'cardY': 310, 'cam': 'medium'}),
 ],
 'K': [
  (179.70, 'talk', 'full', 966, 'wide full body, standing with the dumbbells'),
  (182.05, 'card', None, None, 'Round-2 review: his labels start sliding out at 190.30 and his zoom blur runs 190.43-191.11, so the card plays normally to 189.40, then source 189.40-190.30 slowed to ~0.63x fills the rest (to source 191.114 of piece 2): no sliced label, no freeze while he says "When". Zeeshan\'s top-left chips ("Don\'t Use A Weight That\'s Too Heavy" / "Do Not Swing", 183.2-190.5, x<=763) beside the swinging demo; no window holding Dan (x750-1254) clears them, so the frame x0-1344 is shown whole', None, {'cardCrop': [0, 0.70, 0, 1], 'cardY': 310, 'slow': [189.40, 190.30]}),
  (191.114, 'talk', 'full', 966, 'strict reps on the wide, FULL, from the first sharp frame after Zeeshan\'s zoom blur (the card covers 190.88-191.114); window x604-1328 excludes the "Strict Form / No Swinging" chips (x<=441). Round-2c review: its last 8 frames ease x966->1030 into the continuous K-s03 so the first curl\'s plate is not cut at 18.79-18.99', None, {'xKeys': [[0, 966], [222, 966], [230, 1030]]}),
  (198.786, 'talk', 'full', 1000, "Zeeshan's push-in to the medium, strict curls. Round-2 review: a one-frame switch from x966 read as a 101 px sideways jump inside his zoom, and x1037 cut the dumbbell off the left with ~300 px empty on the right. Round-2b: his curls span source x585-1435, wider than the 724 window, and he drifts left ~150 px after 19.2 s, so a fixed window cut a plate on one side or the other. Keyframed (cosine ease): glide x966->1075 over 12 frames inside his zoom, hold x1075 to frame 66 (21.0 s out), ease to x945 by frame 104 (22.25 s) while he lowers the right arm, hold", None, {'cam': 'medium', 'xKeys': [[0, 1030], [6, 1075], [66, 1075], [104, 938]]}),
 ],
 'H': [
  (125.20, 'talk', 'zoom', 1001, 'wide NEAR; zoom excludes the "Exercise #1: Bicep Curls" pill (125.8-140.7) whole; the one-arm curl with the wrist twist stays in frame (x785-1218)'),
  (142.351, 'card', None, None, 'Zeeshan\'s "2nd Way To Do Bicep Curls" pill (143.05-151.55) on the medium, shown whole; cropped to x173-1690', None, {'cardCrop': [0.09, 0.88, 0, 1], 'cardY': 310, 'cam': 'medium'}),
  (152.93, 'talk', 'full', 1019, 'medium after the pill has FULLY faded (reviewer: visible in the window to 152.8; gap between "this" and "is"); window x657-1381 holds him (x677-1361) and excludes the "Quick Workout / Balanced Sets" chips (x<=623)', None, {'cam': 'medium'}),
  (162.438, 'talk', 'full', 967, "Zeeshan's zoom-out back to the wide. Round-2 review: a one-frame switch from x1019 read as a 76 px jump inside his zoom, so the window glides from x1019 to x967 over 9 frames", None, {'slideFrom': 1019, 'slideFrames': 9}),
  (165.20, 'card', None, None, 'the "Less Range Of Motion / Hard To Maintain Form" chips (165.4-176.3, x<=745) touch his left edge (x745); the frame x0-1344 is shown whole', None, {'cardCrop': [0, 0.70, 0, 1], 'cardY': 310}),
 ],
}

man, labels = [], {}
for seg, rows in PLAN.items():
    total = sum(p['end'] - p['start'] for p in P[seg])
    starts = []
    for r in rows:
        k = r[0]
        if isinstance(k, str) and k.startswith('lcut:'):
            _, out_at, src = k.split(':'); T = src2out(seg, float(out_at)); S = float(src)
        else:
            T = src2out(seg, k); S = k
        starts.append((round(T * FPS), S, r))
    starts.sort(key=lambda x: x[0])
    total_f = round(total * FPS)
    for i, (f0, S, r) in enumerate(starts):
        f1 = starts[i + 1][0] if i + 1 < len(starts) else total_f
        name = f'{seg}-s{i:02d}'
        e = {'seg': seg, 'name': name, 'absStart': round(S, 3), 'frames': f1 - f0, 'dur': round((f1 - f0) / FPS, 4),
             'outStart': round(f0 / FPS, 4), 't': r[1], 'why': r[4]}
        if r[1] == 'talk': e.update(win=r[2], xc=r[3])
        if len(r) > 5 and r[5]: labels[name] = r[5]
        if len(r) > 6: e.update(r[6])
        man.append(e)
    print(seg, 'frames', total_f, '=', sum(m['frames'] for m in man if m['seg'] == seg))
json.dump(man, open('shots/manifest.json', 'w'), indent=1)
json.dump(labels, open('shots/labels.json', 'w'), indent=1)
for m in man: print(f"{m['name']} out {m['outStart']:6.2f} src {m['absStart']:8.3f} {m['frames']:4d}f {m['t']:4s} {m.get('win','')} {m.get('xc','')}")
