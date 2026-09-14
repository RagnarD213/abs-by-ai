#!/usr/bin/env python3
"""Ad 3 "Stop Paying Human Trainers! Use AI Instead" -- VERTICAL from MUHAMMAD's v6 HD (29.97 fps, 7,948 frames = his,
to the frame). Frame n of this timeline IS frame n of his cut; his audio stream goes under it untouched.

Every boundary is HIS, read off his render at the frame (ref/hd_diff.npy spikes: 82 cuts, 13 light-leak flashes with the
cut on the peak); every overlay in/out is his (zov3.py: the lower-third bar inside talk beats, the pill); every bullet's
blur-in onset is his (the left-panel text curve inside each window, ref/ov3.npz; five of them were re-measured
against his panel-brightness step and moved 8-11 frames earlier -- audit 4, item 3); every graphic's text was read at full
resolution off his frames (ref/sheet_text_left.jpg, ref/sheet_lt.jpg) and is reproduced verbatim.

DEVIATIONS FROM HIS CUT, EVERY ONE LOGGED (the rest is literal):
  * his two NATIVE 9:16 AI robot-trainer clips (library ai-trainer-vs-robot-*) sat in his olive card because they are
    portrait in a 16:9 frame; in 9:16 they FILL the frame (skill A6.7: translate his card language by its logic), on
    his own time map, with the big AI-GENERATED chip low over the waistline (never a face) instead of his small
    "[AI-generated]" caption.
  * his 16:9 stock clips (SixPackAbs, dumbbell row, kitchen, push-ups, landmine, the man on his phone) and our exercise
    demos sit in HIS olive card on HIS field -- the vertical mirror of how he cards portrait media (rule 3).
  * his TEXT LEFT / DAN RIGHT screens become DAN ABOVE / TEXT BELOW (the phone window: the phone below Dan).
  * captions: his 16:9 has none; a vertical paid ad without them loses the muted feed, so ours carries word-timed
    captions in his olive (CTC forced alignment), muted under every graphic that prints its own words.
  * talking head: Dan's locked hair-anchored NEAR/FAR standard (zcrop.py), the level changing at every VISIBLE join.
"""
import json, os
FPS = 30000/1001
NTOT = 7948
DUR = NTOT / FPS          # 265.1982
_HERE = os.path.dirname(os.path.abspath(__file__))

LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
REF = f"{LIB}/00 ASSETS USED IN THE REFERENCE AD"
BA  = f"{LIB}/01 Before and After Images"
REV5 = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets"
GOAL = f"{BA}/dan by pool - AI GOAL IMAGE.png"
WORK = f"{REF}/11_APP_monday-workout.png"
ASSESS = f"{REF}/10_APP_trainer-assessment.png"
ED = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/exercise-demos"

_MMP = os.path.join(_HERE, 'media_map.json')
MM = json.load(open(_MMP)) if os.path.exists(_MMP) else {}
def _mm(key, field, default=None):
    return MM.get(key, {}).get(field, default) if isinstance(MM.get(key), dict) else default
def _seq():
    s = MM.get('seq') or []
    out, last = [], None
    for n, bx, c, v in s:
        p = c[0] if isinstance(c, list) and c else None
        if p and p != last and v and v > 0.5: out.append((n, p)); last = p
    return out or [(4854, f"{REF}/07_SHOT4_photoshoot-standing.jpg")]
def _clean(key, lo=0.70, floor=None):
    """his matched samples [(n, t, score)] kept only where confident AND running forward -- a backward sample in a
    retimed clip is a mis-match on a near-static frame, and following it would seek the clip backwards (a visible glitch)

    floor: earliest source time this clip may open on. The one real app recording uploads a STRANGER's photo, not Dan
    (coordination 09-10), and the screen is still scrolling past it at his in-point: his 5.583 s head put a stranger's
    legs on screen for ~15 frames while the card blurred in. A floor of 5.85 s opens the card on the questionnaire
    instead -- the same screen, a third of a second further down its own scroll. r_phonecard's monotonic guard holds
    the floor until the map catches up (~frame 5293), so nothing seeks backwards."""
    out, last = [], -1.0
    for n, t, sc in (MM.get(key, {}).get('map') or []):
        if sc is not None and sc >= lo and t >= last: out.append((n, t, sc)); last = t
    if floor is not None: out = [(n, max(t, floor), sc) for n, t, sc in out]
    return out


def _anchor(key, lo=0.78, every=8, floor=None, keep=(), ceil=None):
    """The same confident samples, but ANCHORED: keep every `every`-th, the ends, and any frame in `keep`, and let
    the renderer's linear interpolation carry the frames between.

    Why: a per-frame NCC map of a phone SCROLL is right on average and wrong frame to frame. Followed literally, the
    upload recording advanced 1,2,1,1,1,2,1,3,3,3,4,2,3,3,2,3,3,3,4,2,2,4,1,6,3,1,4,0,4,1,4,1,6,0 source frames per
    output frame -- it juddered, where his is a smooth decay (audit 2026-09-11, item 9). This is the same lesson the
    story clip already carries in STORY_MAP: a straight line between anchors has neither the flicker of following
    the noise nor the freeze of a stale sample. `keep` holds HIS own internal cuts, which must stay exact."""
    S = _clean(key, lo, floor)
    if len(S) < 3: return S
    if ceil is not None:
        # COMPRESS his scroll into [floor, ceil] instead of clamping it -- a clamp would freeze the card's tail.
        # Why there is a ceiling at all: the app recording's "Creating your future self" progress screen shows the
        # uploaded BEFORE PICTURE, which first appears at source 7.967 s and is large and sharp by 8.8 s.
        # ⚠ MEASURE THE BASELINE OUTSIDE THE CONTAMINATED RANGE. A first pass read the photo's arrival as 8.52 s
        # because it sampled from 8.0 s, where the photo was ALREADY on screen at the bottom, and took that for
        # the clean baseline; a ceiling set from it still left his head in the card's last frames. From 6.0 s the
        # baseline is 0.0001 and the arrival is unmistakable, and that picture is the STRANGER, not Dan
        # (both library recordings are the same session -- coordination 09-10, and Dan raised it with Muhammad).
        # His cut runs to 10.23 s and shows him for ~1.4 s. Ending on the questionnaire and the Generate button is
        # also the better match for the line being read over it.
        lo_t = float(S[0][1]); hi_t = float(S[-1][1])
        if hi_t > ceil and hi_t > lo_t:
            k = (ceil - lo_t)/(hi_t - lo_t)
            S = [(n, lo_t + (t - lo_t)*k, sc) for n, t, sc in S]
    idx = sorted({0, len(S)-1} | {i for i in range(0, len(S), every)} |
                 {i for i, (n, _, _) in enumerate(S) if n in keep})
    return [S[i] for i in idx]
# the opening card: two pieces of the story clip, 1:1, with a hard jump at HIS internal cut (91) -- the fat trainer
# (story 0.09-1.45 s) then the robot trainer (25.67-30.07 s); fitted on his samples at r 0.94-0.96 (media_map ai8)
AI8_MAP = [(49, 1.42 - 40/FPS, 1.0), (90, 1.42 + 1/FPS, 1.0), (91, 26.0 - 10/FPS, 1.0), (223, 26.0 + 122/FPS, 1.0)]

# the story card: he played the library clip at ONE uniform speed. His "internal cuts" (2065, 2202, 2339, 2477, 2614, 2751 --
# exactly 137 frames apart) are the source clip's own 5-second shots: t(2065) = 5.000 s, t(2202) = 10.000 s, and the line
# gives t(1944) = 0.584 s, his first sample (0.5833). The per-sample NCC map was noise in the slow shots (residual sd up to
# 0.5 s, max 2.6 s): followed, it froze the clip for 0.3-0.67 s where his moves (frame diff 0.24-0.35) and switched shots
# 9 frames early; followed with extrapolation, it flickered across the clip's own cut. A straight line has neither.
# MEASURED, not assumed: the source clip is 24 fps and its own shots are exactly 121 FRAMES -- 5.0417 s, not 5.000.
# Reading them as 5-second shots made our slope 1.0938 against his 1.1029, so our shots ran 138 of his frames against
# his 137 and the clip's cuts drifted +1,+2,+3,+3,+5,+6 frames late across the beat (audit 2026-09-11, item 10).
STORY_T0 = 121/24.0                             # 5.041667 s -- the source's first shot boundary
STORY_SLOPE = STORY_T0/(137/FPS)                # 1.1029 source s per his s: his 137-frame shots ARE its 121-frame ones
STORY_MAP = [(1944, STORY_T0 - STORY_SLOPE*121/FPS, 1.0), (2844, STORY_T0 + STORY_SLOPE*779/FPS, 1.0)]
B = lambda n, items: dict(n=n, items=items)
bul = lambda text, n, **k: dict(kind='bullet', text=text, n=n, **k)
ohd = lambda text, n, **k: dict(kind='ohdr', text=text, n=n, **k)
hdr = lambda text, n, **k: dict(kind='hdr', text=text, n=n, **k)

# (kind, n0, n1, spec) -- frames on HIS 29.97 grid
T = [
 ('talk',        0,   49, {}),
 ('bleedv',     49,  224, dict(media=_mm('ai8', 'src'), tmap=AI8_MAP, scrim=True, blur=True, blur_dur=0.73, blur_top=18)),   # his blur-in: sharpness 74 at 49 -> 595 at 71 (audit item 18)
 ('window',    224,  639, dict(body='blocks', blocks=[
        B(224, [ohd("NEXT FEW MINUTES", 234, indent=False),
                bul("Better results than any human trainer.", 269),
                bul("Using free AI tools.", 378)]),
        B(439, [bul("I've spent thousands on personal trainers.", 439),
                bul("And I am a personal trainer myself.", 561)])])),
 ('cardv',     639,  877, dict(media='lifts/spa.mp4', rate=238/235)),      # his clean frames 639-874 (his flash starts 874) played 1.3 % slower: no held tail, no double flash
 ('talk',      877, 1081, {}),
 ('window',   1081, 1300, dict(body='blocks', blocks=[
        B(1081, [bul("I'm going to prove it to you in the", 1090),
                 ohd("NEXT FEW MINUTES", 1116),
                 bul("I'll show you exactly how to use AI to lose your belly fat and get", 1158),
                 ohd("SIX-PACK ABS.", 1189)])])),
 ('talk',     1300, 1544, {}),
 ('cardv',    1544, 1665, dict(media='lifts/row.mp4')),
 ('talk',     1665, 1819, {}),
 ('cardv',    1819, 1944, dict(media='lifts/kitchen.mp4')),
 ('bleedv',   1944, 2845, dict(media=_mm('story', 'src'), tmap=STORY_MAP, scrim=True)),   # ONE uniform retime (see STORY_MAP)
 ('talk',     2845, 2998, {}),
 ('window',   2998, 3248, dict(body='blocks', blocks=[
        B(2998, [bul("Most human trainers have a very limited understanding of the actual science.", 3000),
                 bul("They're passing along bro-science they picked up in the gym", 3096),
                 ohd("TEN YEARS AGO.", 3216)])])),
 ('talk',     3248, 3594, {}),
 ('phonecard', 3594, 3701, dict(src='png', media=WORK, offsets=_mm('work1', 'offsets'), blur=True)),
 ('cardv',    3701, 3797, dict(media='lifts/pushups.mp4')),
 ('talk',     3797, 3964, {}),
 ('window',   3964, 4289, dict(body='blocks', blocks=[
        B(3964, [hdr("HOW DO I KNOW ALL THIS?", 3966),
                 bul("Because even though I was a personal trainer back in my 20s, as a 38 year old dad running a "
                     "successful ad agency.", 4019, olive=("personal trainer", "38 year old", "ad agency.")),
                 bul("I started getting fat.", 4214)])])),
 ('talk',     4289, 4392, {}),
 ('card',     4392, 4482, dict(media=f'{REV5}/fatdad_standing.jpg', blur=True)),
 ('card',     4482, 4593, dict(media=f'{REV5}/fatdad_ride.jpg', blur=True)),     # his card re-opens on the second photo (a blur-in, 4482-4505)
 ('talk',     4593, 4643, {}),
 ('card',     4643, 4718, dict(media=GOAL, blur=True, label=True)),            # never back to back with a before picture: camera scene 4593-4643 (Dan's round-4 rule)
 ('talk',     4718, 4854, {}),
 ('photoseq', 4854, 4886, dict(stills=[(4854, f"{REF}/07_SHOT4_photoshoot-standing.jpg"),     # his rapid sequence, each still
                                       (4859, f"{REF}/06_SHOT3_photoshoot-towel-smile.jpg"),     # template-matched on his frames
                                       (4867, f"{REF}/04_SHOT1_photoshoot-smiling-trees.png"),  # at r 0.98-0.99 (4856, 4862) and
                                       (4874, f"{REF}/05_SHOT2_photoshoot-flag.jpg")], pop=(4881, 4884, 1.128))),   # his flag still pops 1487->1678 px over 4881-83 (audit item 18)       # 0.72-0.80 (4867, 4874)
 ('talk',     4886, 5278, {}),
 ('phonecard', 5278, 5362, dict(src='video', media=_mm('upload', 'src'), tmap=_anchor('upload', 0.78, every=8, floor=5.85, keep=(5307, 5308), ceil=7.90), blur=True)),   # floor: no stranger's photo (see _clean); anchored: no judder (see _anchor); 5308 is HIS cut inside the recording
 ('talk',     5362, 5509, {}),
 ('phonecard', 5509, 5640, dict(src='still', media=os.path.join(_HERE, 'assets/lock_screen_dan.png'), blur=True)),   # his own screen lifted from his render (n 5600) -- BUT the picture inside it was the STRANGER from the app
                                 # recording, not Dan, presented as "Download Your Future Self" (audit 2, 2026-09-11). Dan's own AI goal
                                 # image is composited into the screen's photo block (assets/lock_screen_dan.png, zero rows of the original
                                 # photo left) with the AI-GENERATED tag redrawn in place, so no second chip
 ('talk',     5640, 5732, {}),
 ('window',   5732, 6099, dict(body='phone', media=ASSESS, offsets=_mm('assess', 'offsets'))),
 ('talk',     6099, 6260, {}),
 ('window',   6260, 6781, dict(body='blocks', blocks=[
        B(6260, [bul("It also identifies your strong body parts and your lagging body parts", 6260),
                 bul("It tailors your program to focus on making you look exactly like your goal picture.", 6377)]),
        B(6530, [hdr("IT DESIGNS THE WHOLE PLAN", 6530),
                 bul("To work around any injuries you have.", 6600),
                 bul("The equipment you actually own", 6649),
                 bul("How many days a week you can really train.", 6710)])])),
 ('talk',     6781, 6822, {}),   # his window->talk cut is at 6781 -- under his leak's SECOND pulse, not the 6777 peak
                                 # and not the dip at 6779 between them (pic.json steps 2963 -> 3091 at 6781; audit 3, item 8): cutting on the peak
                                 # showed the old take zoomed full-frame for one 77%-visible frame (audit 2026-09-11, item 7)
 ('phonecard', 6822, 6913, dict(src='png', media=WORK, offsets=_mm('work2', 'offsets'), blur=True)),
 ('cardv',    6913, 6967, dict(media=f"{ED}/lat-pulldown/lat-pulldown-AIDAN-narrated-FINAL.mp4", ss=0.10*FPS, label=True)),   # our clean demo at his in-point, 1:1 (his burned label not lifted)
 ('cardv',    6967, 7022, dict(media=f"{ED}/db-curl/db-curl-AIDAN-narrated-FINAL.mp4", ss=0.84*FPS, label=True)),        # reps repeat, so NCC wanders +-1 rep: in-point approximate, logged
 ('talk',     7022, 7329, {}),
 ('cardv',    7329, 7399, dict(media='lifts/landmine.mp4')),
 ('cardv',    7399, 7454, dict(media='lifts/phoneguy.mp4')),
 ('window',   7454, 7687, dict(body='blocks', blocks=[
        B(7454, [hdr("IT ADAPTS TO YOU", 7456, big=True),
                 bul("Didn't sleep well?\nIt adjusts your workout for that too.", 7459),
                 bul("No human trainer can do that.", 7559),
                 bul("Not at any price.", 7635)])])),
 ('talk',     7687, NTOT, {}),
]

# his overlays on the footage (frames): bar in-frames from zov3 minus his ~8-frame tab lead, out on his cut / his fade
OVERLAYS = [
 dict(kind='lt', n0=963,  n1=1079, lines=["AI has made personal trainers", "like me totally obsolete."]),
 dict(kind='lt', n0=1319, n1=1418, lines=["Why AI is better than any", "human trainer, including me."]),
 dict(kind='lt', n0=1430, n1=1544, lines=["Human trainers are incredibly", "expensive."], num=1),
 dict(kind='lt', n0=1949, n1=2067, lines=["Human trainers hand everybody", "the same generic workout plan."], num=2),
 dict(kind='lt', n0=2849, n1=2947, lines=["AI gives you a science-based", "workout plan."], num=3),
 dict(kind='lt', n0=3254, n1=3404, lines=["AI can be there for you", "for every workout."], num=4),
 dict(kind='pill', n0=4895, n1=5202, top="Get A FREE AI Image Of Yourself", big="With Abs"),
 dict(kind='lt', n0=7027, n1=7117, lines=["You can get any exercise question", "answered immediately"]),
 dict(kind='lt', n0=7694, n1=7812, lines=["So generate your future self image", "and let your AI trainer help"]),
 dict(kind='pill', n0=7853, n1=NTOT, top="Get A FREE AI Image Of Yourself", big="With Abs"),
]

# his light-leak flashes: a ~10-frame strobe with the cut ON the peak, at 13 cuts (ref/hd_diff.npy + ref/hd_luma.npy).
# The screen-blend strength per frame is recovered from HIS luma trace against the unflashed level on each side
# (k = (his - base) / (255 - base); base = the frame before the window outgoing, the settled level after it incoming)
# and applied to OUR frames with the same k -- not a guessed envelope (skill A7.4).
FLASH_WINDOWS = [(222, 233), (874, 885), (1298, 1309), (2842, 2853), (3246, 3257), (4287, 4298), (4715, 4726),
                 (4884, 4895), (5638, 5649), (6096, 6106), (6775, 6786), (7019, 7030), (7685, 7696)]
def _flash_windows():
    import numpy as np
    his = np.memmap(os.path.join(_HERE, 'his256.gray'), np.uint8, 'r').reshape(-1, 144, 256)
    m = his.reshape(len(his), -1).mean(1)
    out = {}
    for n0, n1 in FLASH_WINDOWS:
        seg = m[n0:n1]; peak = n0 + int(np.argmax(seg))
        pre, post = float(m[n0-1]), float(np.median(m[n1+1:n1+5]))
        for n in range(n0, n1):
            base = pre if n < peak else post
            k = (float(m[n]) - base) / max(255.0 - base, 1.0)
            if k > 0.10: out[n] = round(min(k, 1.0), 3)
    return out
FLASH = _flash_windows() if os.path.exists(os.path.join(_HERE, 'his256.gray')) else {}
FLASHES = sorted(FLASH)

NO_CAPS_KINDS = {'phonecard'}                    # beats that print their own words (app UI)
NO_CAPS_BODIES = {'blocks', 'phone'}             # window bodies that print words
NO_CAPS_OVERLAYS = {'lt', 'pill'}

def timeline():
    tl = [dict(kind=k, t0=a/FPS, t1=b/FPS, n0=a, n1=b, **s) for k, a, b, s in T]
    ov = [dict(o, t0=o['n0']/FPS, t1=o['n1']/FPS) for o in OVERLAYS]
    return tl, ov

def muted_ranges():
    tl, ov = timeline()
    return [(b['t0'], b['t1']) for b in tl if b['kind'] in NO_CAPS_KINDS or (b['kind'] == 'window' and b.get('body') in NO_CAPS_BODIES)] + \
           [(o['t0'], o['t1']) for o in ov if o['kind'] in NO_CAPS_OVERLAYS]

_ZOOM = None
def push_at(t):
    """Crop zoom relative to FAR at time t (1.0 = FAR). qc check 12 reads this."""
    global _ZOOM
    if _ZOOM is None:
        _ZOOM = json.load(open(os.path.join(_HERE, 'crop.json')))['zoom_per_frame']
    n = int(t*FPS)
    return _ZOOM[n] if 0 <= n < len(_ZOOM) else 1.0

if __name__ == '__main__':
    tl, ov = timeline()
    assert tl[0]['n0'] == 0 and tl[-1]['n1'] == NTOT
    bad = [i for i in range(1, len(tl)) if tl[i]['n0'] != tl[i-1]['n1']]
    print(f'{len(tl)} beats, {NTOT} frames ({DUR:.3f}s); gaps/overlaps: {bad or "none"}')
    ins = sum(b['n1']-b['n0'] for b in tl if b['kind'] != 'talk')
    print(f'insert/graphic coverage {100*ins/NTOT:.0f}%   changes/min {len(tl)/(DUR/60):.1f}')
    for b in tl:
        miss = [k for k in ('tmap', 'offsets', 'media') if k in b and not b[k]]
        print(f"{b['kind']:9s} {b['n0']:5d}-{b['n1']:5d}  {b['t0']:8.3f}-{b['t1']:8.3f}  {str(b.get('media', b.get('body', '')))[-44:]}"
              + (f"   !! missing {miss}" if miss else ''))
    for o in ov: assert o['n1'] > o['n0'], o
    print(len(FLASH), 'flash frames')
