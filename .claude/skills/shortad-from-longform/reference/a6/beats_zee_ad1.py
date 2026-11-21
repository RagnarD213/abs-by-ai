#!/usr/bin/env python3
"""Ad 1 vertical from ZEESHAN's final (24 fps, 5980 frames = his, to the frame).

Every boundary is HIS, read off his render at the frame (`scenes.npy` spikes; `edl_picture.json` for the talk);
every overlay in/out is his, measured on his frames (zov.py / the row-residual scans). Frame n of this timeline IS
frame n of his cut, and his mix goes underneath verbatim, so lip sync is his.

DEVIATIONS FROM HIS CUT, EVERY ONE LOGGED (the rest is literal):
  * 188.75-190.33: his phone shows the app's EMAIL-CAPTURE screen ("Download Your Future Self ... Enter Your Email"),
    banned in our ads. Ours shows the AFTER IMAGE ALONE in his black-bordered card, AI-labelled, under his "Final
    Result AI" label -- no heading, no form, no confetti. (The first build cropped the screen above the form; the
    independent audit, 2026-09-10, found it still carried that screen's own heading and confetti.)
  * landscape media (his four full-frame AI clips, the anatomy clip) sit in HIS black-bordered card on HIS field --
    the vertical mirror of how he cards the portrait photos in 16:9 -- instead of a 2.7x upscaled crop.
  * 3.71-6.50: his callout box highlights the goal photo taped to the door, which sits outside any 9:16 crop of Dan;
    ours splits the frame: Dan above, the door photo below with his lime box, sized so the caption band stays clear
    and the hook's key line ("I generated this picture with AI back when...") is captioned.
  * 62.88-69.92: the crude-photoshop gag carries an AI-GENERATED label (the asset index files it under AI clips; his
    has none -- our standing rule).
  * the second phone-on-marble beat (150.75-157.96) reuses the FIRST beat's frames (his second copy has his CTA bar
    burned into the phone), retimed to his length.
  * captions: his 16:9 has none; a vertical paid ad without them loses the muted feed, so ours carries the approved
    word-timed captions in HIS lime, muted under every graphic that prints its own words.
  * talking head: hair-anchored NEAR/FAR (Dan's 2026-09-08 standard) with the level changing at every VISIBLE talk
    join; his five pose-matched splices keep one level (zcrop.py); his two big punch-ins (108.96, 161.46) are NEAR,
    entered on his own 4-frame ramp.
  * end card: his "Tap The Button Below" lands at his frame 5942; his last 7 frames (5973-5979) go black -- ours holds
    the end card to the last frame (a CTA on screen beats black in a feed).
"""
FPS = 24.0
NTOT = 5980
DUR = NTOT / FPS          # 249.166667 -- his video stream

LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/00 ASSETS USED IN THE REFERENCE AD"
REV5 = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets"

# (kind, n0, n1, spec) -- frames on HIS 24 fps grid
T = [
 ('card',     0,   89, dict(media=f'{LIB}/01_HOOK+ENDCARD_ai-goal-image_dan-by-pool.png', w0=680, w1=860, cy=730, label=True)),
 ('split',   89,  156, dict(t_box=(102-89)/FPS)),                        # his callout box draws on at 4.25 s
 ('card',   156,  216, dict(media=f'{LIB}/02_BEFORE-PICTURE_dan-200lb.png', w0=780, w1=858, cy=760)),
 ('bleedv', 216,  327, dict(media='assets/lift_phone.mp4', label=True, scrim=True)),   # caption scrim: see zrender.r_bleedv
 ('bleed',  327,  340, dict(media=f'{LIB}/07_SHOT4_photoshoot-standing.jpg', pop=True, oy=0.30)),
 ('bleed',  340,  353, dict(media=f'{LIB}/06_SHOT3_photoshoot-towel-smile.jpg', oy=0.30)),
 ('bleed',  353,  364, dict(media=f'{LIB}/04_SHOT1_photoshoot-smiling-trees.png', ox=0.50, oy=0.20)),
 ('bleed',  364,  372, dict(media=f'{LIB}/05_SHOT2_photoshoot-flag.jpg', ox=0.52, oy=0.35)),
 ('talk',   372, 1180, {}),
 ('title1',1180, 1284, {}),
 ('bleedv',1284, 1400, dict(media='assets/lift_handphone.mp4', label=True)),
 ('talk',  1400, 1509, {}),
 ('bleedv',1509, 1678, dict(media=f'{LIB}/08_CLIP_crude-photoshop-gag.mp4', hold_last=True, label=True)),   # a still (his frame diff 0.32): held, with the push; an AI clip -> labelled
 ('talk',  1678, 1808, {}),
 ('app',   1808, 1999, dict(media='assets/app_a.mp4')),
 ('talk',  1999, 2430, {}),
 ('title2',2430, 2610, {}),
 ('talk',  2610, 2748, {}),
 ('cardv', 2748, 2792, dict(media=f'{REV5}/ai_women_pool.mp4', label=True)),
 ('cardv', 2792, 2832, dict(media=f'{REV5}/ai_respect_gym.mp4', label=True)),
 ('cardv', 2832, 2970, dict(media=f'{REV5}/ai_health_beachrun.mp4', label=True)),
 ('talk',  2970, 3478, {}),
 ('cardv', 3478, 3618, dict(media=f'{REV5}/ai_busydad_kitchen.mp4', label=True)),
 ('bleedv',3618, 3791, dict(media='assets/lift_phone.mp4', label=True, hold_last=True, scrim=True)),   # his: the same 111 frames 1:1, then held
 ('talk',  3791, 4291, {}),
 ('app',   4291, 4530, dict(media='assets/app_b.mp4')),
 ('appres',4530, 4568, dict(media='assets/after_still.png')),              # the after image ALONE (see the deviations)
 ('talk',  4568, 4919, {}),
 ('cardv', 4919, 5132, dict(media='assets/lift_anatomy.mp4', label=True)),
 ('talk',  5132, 5477, {}),
 ('png',   5477, 5675, dict(media=f'{LIB}/12_APP_meal-plan.png')),
 ('talk',  5675, 5893, {}),
 ('end',   5893, NTOT, dict(t_second=(5942-5893)/FPS)),                 # his second line at his frame 5942
]

# his overlays on the footage (frames). CTA bar: continuous 106.21 -> 244.71 s.
OVERLAYS = [
 dict(kind='checklist', n0=380, n1=749, items=[435, 526, 630]),
 dict(kind='problem',   n0=1017, n1=1180, sub=1061),
 dict(kind='ifyousaw',  n0=2298, n1=2414),
 dict(kind='num', n0=3095, n1=3141, num='#1', text="You Don't Need More Knowledge"),
 dict(kind='num', n0=3146, n1=3221, num='#2', text='You Need Motivation To Execute What You Already Know.'),
 dict(kind='cta',       n0=2549, n1=5873),
 dict(kind='final',     n0=4540, n1=4568),
]
FLASHES = [372, 749, 1999, 2970, 3225, 4048, 5294, 5758]    # his one-frame white flashes (measured luma ~212 vs ~65)
FLASH_K = 0.78
TITLE1_CUES = [1180, 1200, 1222, 1244]                        # his: header fades up 1180-1190, then each stair line
TITLE1_FADEOUT = (1266, 1284)                                  # ... and the whole card fades out over its last 0.75 s

# captions do not run under graphics that print their own words, nor over the white app screens. The split prints no
# words (Dan + the door photo + his box), so it is captioned: it carries the hook's key line.
NO_CAPS_KINDS = {'title1', 'title2', 'app', 'appres', 'png', 'end'}
NO_CAPS_OVERLAYS = {'checklist', 'problem', 'ifyousaw', 'num', 'final'}

def timeline():
    tl = [dict(kind=k, t0=a/FPS, t1=b/FPS, n0=a, n1=b, **s) for k, a, b, s in T]
    ov = [dict(o, t0=o['n0']/FPS, t1=o['n1']/FPS) for o in OVERLAYS]
    return tl, ov

def muted_ranges():
    tl, ov = timeline()
    return [(b['t0'], b['t1']) for b in tl if b['kind'] in NO_CAPS_KINDS] + \
           [(o['t0'], o['t1']) for o in ov if o['kind'] in NO_CAPS_OVERLAYS]

_ZOOM = None
def push_at(t):
    """Crop zoom relative to FAR at time t (1.0 = FAR). qc check 12 reads this."""
    global _ZOOM
    if _ZOOM is None:
        import json
        _ZOOM = json.load(open('crop.json'))['zoom_per_frame']
    n = int(t*FPS)
    return _ZOOM[n] if 0 <= n < len(_ZOOM) else 1.0

if __name__ == '__main__':
    tl, ov = timeline()
    assert tl[0]['n0'] == 0 and tl[-1]['n1'] == NTOT
    bad = [i for i in range(1, len(tl)) if tl[i]['n0'] != tl[i-1]['n1']]
    print(f'{len(tl)} beats, {NTOT} frames ({DUR:.3f}s); gaps/overlaps: {bad or "none"}')
    ins = sum(b['n1']-b['n0'] for b in tl if b['kind'] != 'talk')
    print(f'insert/graphic coverage {100*ins/NTOT:.0f}%   changes/min {len(tl)/(DUR/60):.1f}')
    for b in tl: print(f"{b['kind']:7s} {b['n0']:5d}-{b['n1']:5d}  {b['t0']:8.3f}-{b['t1']:8.3f}  {b.get('media','')[-44:]}")
