#!/usr/bin/env python3
"""Ad 4 "Stop Wasting Money on Supplements! Ask AI Instead" -- VERTICAL from MUHAMMAD's V4 HD (29.97 fps, 7,160
frames = his, to the frame; Drive 14on08ZTz2bXPJtwp8_fAENrtEGASo0bg, verified identical to the approved round-3 draft).
Frame n of this timeline IS frame n of his cut; his audio stream goes under it untouched.

Every boundary is HIS, read off his render at the frame (ref/hd_diff.npy spikes, consecutive-frame strips at every cut in
ref/cutstrips_*.png); every overlay in/out is his (olive-tab / pill / card detection on his192.rgb, ref/feat192.npy);
every bullet cue is the frame his bright-pixel count steps (ref/feat.npy).

AV-03 (2026-10-03), DAN'S RULES SINCE THE 09-11 BUILD, APPLIED TO BOTH THE 9:16 AND THE 1:1:
  * clips and photos FILL the frame (10-01 / 10-02); a square card only where the sides hold something the clip needs
    (the stack pan and the overhead meal prep spread across the frame; the ride photo has a second person);
  * labels placed by measurement, never over his face or abs (09-12); a hyphen in the real-picture label (09-18);
  * the crop lands on him, then holds (10-03); phones as large as fits (10-02).
  The 09-11 notes below describe the OLD card layout where they mention cards.

DEVIATIONS FROM HIS CUT, EVERY ONE LOGGED (the rest is literal):
  * his 16:9 stock (influencer, library, label, pill bottles, supermarket, meal prep) and Dan's 16:9 supplement-stack
    pan sit in HIS olive card on HIS field -- the vertical mirror of how he cards portrait media (skill rule 3: never a
    2.7x full-bleed crop). The label clip's card is cropped in to the tub (still a downscale) so "PROPRIETARY BLENDS"
    stays legible on a phone.
  * his TEXT LEFT / DAN RIGHT screens (four bullet builds) become DAN ABOVE / TEXT BELOW.
  * his two audit-results phones beside Dan's head (201.6-207.1, 209.6-213.3) become Dan above / the phone below: a
    9:16 frame has no room beside him, and the recordings are native 1080x1920 so the phone can be big.
  * the robot clip's "AI-generated video" label + dashed arrow points DOWN at the clip instead of right (left/right
    becomes above/below).
  * captions: his 16:9 has none; a vertical paid ad without them loses the muted feed, so ours carries word-timed
    captions in his olive, muted under every graphic that prints its own words.
  * talking head: Dan's locked hair-anchored NEAR/FAR standard (zcrop.py), the level changing at every VISIBLE join.
"""
import json, os
FPS = 30000/1001
NTOT = 7160
DUR = NTOT / FPS          # 238.9054
_D = os.path.dirname(os.path.abspath(__file__))

LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
REF = f"{LIB}/00 ASSETS USED IN THE REFERENCE AD"
BA  = f"{LIB}/01 Before and After Images"
APPS = f"{LIB}/02 App Screen Recordings and Screenshots"
REV5 = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets"
ADA = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/public/ad-assets"
STUDIO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/photos/finalized social media photos"
GOAL = f"{BA}/dan by pool - AI GOAL IMAGE.png"
BEFORE = f"{BA}/00_ORIGINAL_deckchair_upscaled3x.jpg"
BEFORE_STANDING = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/before-photo-candidates/fat dad pic - standing_RECENTERED-4x5.jpg"
ROBOT = f"{LIB}/04 AI-Generated Clips/ai-robot-supplement-audit-10s.mp4"
STACK = f"{ADA}/dan-real-supplement-stack_pan_5s_1080p_muted.mp4"
RESULTS = f"{ADA}/app-supplement-audit-results_20s_1080x1920_muted.mp4"
SAFETY = f"{ADA}/app-supplement-audit-safety-flags_11s_1080x1920_muted.mp4"
APPGEN = f"{REF}/09_CLIP_app-generate-future-self.mp4"
AUDIT = f"{APPS}/app-supplement-audit-scroll.mp4"

# (kind, n0, n1, spec) -- frames on HIS 29.97 grid
T = [
 ('talk',      0,   85, {}),
 ('fillv',    85,  262, dict(media='assets/robot.mp4', label='ai', sq=dict(card_ar=9/16))),   # shot 1: the action runs head -> arm -> trash can, so the 1:1 shows the WHOLE portrait clip in a card (75 % of it lost the trash can: review round 2)
 ('fillv',   262,  437, dict(media='assets/robot.mp4', ss=177, label='ai', sq=dict(cy=0.30))),               # shot 2 (the clip's own cut at 262): head + the bottle held up fill the 1:1                                             # his card fades in 85-95; his clip cut at 262 is the clip's own
 ('sqv',     437,  639, dict(media='assets/stack.mp4', cx=0.5)),                                # his cut ON the flash peak (437); Dan's real stack, on his time map
 ('talk',    639,  928, {}),
 ('window',  928, 1267, dict(body='bullets', header=None,   # to HIS cut (1267): ending at 1264 left a 3-frame shot of the old take (audit 1)
                             items=["Why you must use AI to audit your supplement stack.",
                                    "Which AI model and prompt I use to personally ensure I'm taking the best stuff."], item_n=[955, 1090])),
 ('talk',   1267, 1307, {}),
 ('sqv',    1307, 1477, dict(media='lifts/influencer.mp4', cx=0.375, ar=1.333, sq=dict(card_ar=1.333, cx=0.375))),   # 75 % of the clip's width holds his shaker with the hand on it (far left) AND his face (right of centre); a square halves the shaker (reviews, rounds 1 and 2)
 ('talk',   1477, 1754, {}),
 ('fillv',  1754, 1827, dict(media='lifts/library.mp4', cx=0.68, sq=dict(cx=0.62))),
 ('talk',   1827, 2016, {}),
 ('window', 2016, 2304, dict(body='bullets', header=None,
                             items=["AI can read all of it and build you a supplement stack based on what the evidence actually supports"],
                             item_n=[2040], tails=[("NOT WHAT'S TRENDING", 2203), ("NOT WHAT WORKED FOR SOME GUY ON YOUTUBE", 2249)])),
 ('talk',   2304, 2488, {}),
 ('window', 2488, 2713, dict(body='bullets', header=None,
                             items=["Every review site", "Every influencer", "Every top 5 supplements list you've ever read"],
                             item_n=[2504, 2546, 2588], tails=[("IT'S ALL AFFILIATE LINKS", 2660)])),
 ('talk',   2713, 3086, {}),
 ('fillv',  3086, 3167, dict(media='lifts/label.mp4', cx=0.545, cy=0.61, zoom=1.28, sq=dict(cx=0.52, cy=0.5, zoom=1.0))),   # 9:16: pushed in so his PROPRIETARY BLENDS highlight sits ABOVE the caption line, not under it     # his highlight box is in the lift; cropped to the tub
 ('talk',   3167, 3775, {}),
 ('fillv',  3775, 3864, dict(media='lifts/pills.mp4', cx=0.71, sq=dict(cx=0.68))),
 ('talk',   3864, 4186, {}),
 ('bleed',  4186, 4219, dict(media=BEFORE, blur=True, ox=0.62, oy=0.0, sq=dict(fit='fith', fith_h=846))),      # the push is anchored at the TOP (his hair is 27 px under the photo's edge); 1:1: the whole photo, 846 px tall, so the caption sits on the field under it and his belly is clear
 ('sqcard', 4219, 4251, dict(media=BEFORE_STANDING, ar=0.8, sq=dict(ox=0.5, oy=0.0))),      # the RECENTERED 4x5 Dan approved as a before picture (the original cuts his hair and cheek at the photo's own edge); 9:16: the WHOLE photo in a card, because a full-screen crop cuts the girl's face in half
 ('sqcard', 4251, 4289, dict(media=f'{REV5}/fatdad_ride.jpg', ox=0.40, sq=dict(ox=0.40, oy=0.0))),      # 1:1: the push is anchored at the top, his hair is 10 px under the photo's own edge
 ('talk',   4289, 4524, {}),
 ('bleed',  4524, 4595, dict(media=GOAL, blur=True, label='ai', sq=dict(fit='fith'))),                          # his cut to talk is 4595; the flash peaks 2 frames later (4597)
 ('talk',   4595, 4723, {}),
 ('shot',   4723, 4741, dict(media=f'{REF}/07_SHOT4_photoshoot-standing.jpg', sq=dict(fit='fith'))),
 ('shot',   4741, 4759, dict(media=f'{REF}/06_SHOT3_photoshoot-towel-smile.jpg', sq=dict(fit='fith'))),
 ('shot',   4759, 4777, dict(media=f'{LIB}/06 Dan Photo Shoot Stills/photo-221_FINAL_PRIMARY.jpg', sq=dict(fit='fith'))),     # his landscape SHOT1 -> a portrait (Dan r1 on Ad 5: all after pictures vertical + full screen)
 ('shot',   4777, 4792, dict(media=f'{STUDIO}/studio-blue-110_FINAL_PRIMARY.jpg', sq=dict(fit='fith'))),                          # his landscape SHOT2 (flag) -> a studio portrait (Dan: 'you can also use the studio pictures')
 ('talk',   4792, 5145, {}),
 ('app',    5145, 5238, dict(media='assets/appgen.mp4')),
 ('talk',   5238, 5351, {}),
 ('dl',     5351, 5435, dict(media='assets/download.png')),
 ('title',  5435, 5534, dict(headline="You lock in", sub="And get serious about\nyour fitness goals")),
 ('phonecard', 5534, 5704, dict(media='assets/audit.mp4')),
 ('window', 5704, 5912, dict(body='bullets', header=None, items=["AI reads every label", "The actual ingredients", "The actual doses"],
                             item_n=[5716, 5762, 5806], tails=[("NOT THE MARKETING", 5846)])),
 ('talk',   5912, 6041, {}),   # W4 ends ON his PICTURE cut (5912, pic.json): 5905 was his audio splice, and his window wipes off across it   # W4 ends ON his cut (5905), not 7 frames after it (audit 1: a pose jump inside our window)
 ('window', 6041, 6206, dict(body='phonev', media='assets/results.mp4')),
 ('talk',   6206, 6282, {}),
 ('window', 6282, 6391, dict(body='phonev', media='assets/safety.mp4')),
 ('talk',   6391, 6514, {}),
 ('fillv',  6514, 6634, dict(media='lifts/supermarket.mp4', cx=0.36, sq=dict(cx=0.38))),
 ('sqv',    6634, 6773, dict(media='lifts/mealprep.mp4', cx=0.58)),
 ('talk',   6773, 6836, {}),
 ('bleed',  6836, 6909, dict(media=GOAL, label='ai', sq=dict(fit='fith'))),
 ('talk',   6909, NTOT, {}),
]

# his overlays (frames; the olive tab's first/last visible frame on his192)
OVERLAYS = [
 dict(kind='lt',    n0=469,  n1=588,  lines=["I have spent tens of thousands of dollars", "on supplements over my lifetime"],   # to the end of 'lifetime.' (583): ended at 564 the caption re-printed 'my lifetime.' under it (watch pass, render 1)
      weights=["Bold", "Bold"], sizes=[44, 44], y_bottom=1650),
 dict(kind='numlt', n0=1478, n1=1625, num="1", lines=["AI can design a truly science-based", "supplement stack for you"]),
 dict(kind='numlt', n0=2362, n1=2486, num="2", lines=["The people telling you what to take", "are the people selling it to you"]),
 dict(kind='lt',    n0=2718, n1=2789, lines=["AI has nothing to sell you"], weights=["Bold"], sizes=[54]),
 dict(kind='numlt', n0=2971, n1=3082, num="3", lines=["The label doesn't tell you", "what's actually in it"]),
 dict(kind='lt',    n0=3344, n1=3396, lines=["AI can read the label"], weights=["Bold"], sizes=[54]),
 dict(kind='numlt', n0=3491, n1=3644, num="4", lines=["Nobody is checking your supplements", "against your medications"]),
 dict(kind='lt',    n0=4363, n1=4477, lines=["A truly science-based fitness plan", "designed by AI"], weights=["Bold", "Bold"], sizes=[46, 46]),
 dict(kind='pill',  n0=4795, n1=5055, top="Get A FREE AI Image Of Yourself", big="With Abs"),
 dict(kind='lt',    n0=6041, n1=6155, lines=["It shows you exactly which", "supplements are helping you"], weights=["Bold", "Bold"], sizes=[44, 44], y_bottom=802, sq_y=1040),
 dict(kind='lt',    n0=6282, n1=6391, lines=["It flags anything that interacts", "with the medications you're on"], weights=["Bold", "Bold"], sizes=[44, 44], y_bottom=802, sq_y=1040),
 dict(kind='pill',  n0=7036, n1=NTOT, top="Get A FREE AI Image Of Yourself", big="With Abs"),
]

# his light-leak flashes: a 3-pulse strobe over ~10 frames at nine cuts. The screen-blend strength per frame is recovered
# from HIS luma trace against the unflashed level on each side of the content cut (k = (his - base) / (255 - base); base =
# the outgoing side's last clean frame before the cut, the incoming side's settled level from the cut on).
FLASH_CUTS = [(437, 433, 448), (639, 636, 649), (3864, 3861, 3874), (4289, 4286, 4299), (4595, 4594, 4607),
              (4792, 4789, 4802), (5704, 5701, 5714), (6773, 6770, 6783), (6909, 6906, 6919)]
def _flash_windows():
    import numpy as np
    his = np.memmap(os.path.join(_D, 'his256.gray'), np.uint8, 'r').reshape(-1, 144, 256)
    m = his.reshape(len(his), -1).mean(1)
    out = {}
    for cut, n0, n1 in FLASH_CUTS:
        pre, post = float(m[n0-1]), float(np.median(m[n1+11:n1+16]))      # the level his picture SETTLES at (review round 2:
        for n in range(n0, n1 + 11):                                      # the old window ended while his veil was still fading)
            base = pre if n < cut else post
            k = (float(m[n]) - base) / max(255.0 - base, 1.0)
            if k > 0.015: out[n] = round(min(k, 1.0), 3)
    return out
FLASH = _flash_windows()
FLASHES = sorted(FLASH)

NO_CAPS_KINDS = {'title', 'app', 'dl', 'phonecard'}                  # beats that print their own words / white app screens
NO_CAPS_BODIES = {'bullets', 'phonev'}                              # window bodies that print words / fill the caption band
NO_CAPS_OVERLAYS = {'lt', 'numlt', 'pill'}

def timeline():
    tl = [dict(kind=k, t0=a/FPS, t1=b/FPS, n0=a, n1=b, **s) for k, a, b, s in T]
    ov = [dict(o, t0=o['n0']/FPS, t1=o['n1']/FPS) for o in OVERLAYS]
    return tl, ov

def caption_stops():
    """times a held caption word must stop at: the first frame of every full-frame PICTURE of Dan"""
    tl, _ = timeline()
    return [b['t0'] for b in tl]            # ...and every other beat edge: a held last word never rides onto the next picture (round 4: 'you what to take.' sat one frame on the talking head at 1477)

def muted_ranges():
    tl, ov = timeline()
    return [(b['t0'], b['t1']) for b in tl if b['kind'] in NO_CAPS_KINDS or (b['kind'] == 'window' and b.get('body') in NO_CAPS_BODIES)] + \
           [(o['t0'], o['t1']) for o in ov if o['kind'] in NO_CAPS_OVERLAYS]

_ZOOM = None
def push_at(t):
    """Crop zoom relative to FAR at time t (1.0 = FAR). qc check 12 reads this."""
    global _ZOOM
    if _ZOOM is None:
        _ZOOM = json.load(open(os.path.join(_D, 'crop.json')))['zoom_per_frame']
    n = int(t*FPS)
    return _ZOOM[n] if 0 <= n < len(_ZOOM) else 1.0

if __name__ == '__main__':
    tl, ov = timeline()
    assert tl[0]['n0'] == 0 and tl[-1]['n1'] == NTOT
    bad = [i for i in range(1, len(tl)) if tl[i]['n0'] != tl[i-1]['n1']]
    print(f'{len(tl)} beats, {NTOT} frames ({DUR:.3f}s); gaps/overlaps: {bad or "none"}')
    ins = sum(b['n1']-b['n0'] for b in tl if b['kind'] != 'talk')
    print(f'insert/graphic coverage {100*ins/NTOT:.0f}%   changes/min {len(tl)/(DUR/60):.1f}')
    for b in tl: print(f"{b['kind']:9s} {b['n0']:5d}-{b['n1']:5d}  {b['t0']:8.3f}-{b['t1']:8.3f}  {str(b.get('media', b.get('body', '')))[-44:]}")
    for o in ov:
        assert o['n1'] > o['n0'], o
    print('flash frames:', FLASHES)
