#!/usr/bin/env python3
"""Ad 5 "Every diet you've tried failed for the same reason" -- VERTICAL from MUHAMMAD's V3 HD (29.97 fps, 7,036
frames = his, to the frame). Frame n of this timeline IS frame n of his cut; his audio stream goes under it untouched.

Every boundary is HIS, read off his render at the frame (ref/hd_diff.npy spikes + the 0.5 s contact sheets); every
overlay in/out is his (the small-peak spans of the same trace and the sheets, +-0.25 s where the sheet decides).

DEVIATIONS FROM HIS CUT, EVERY ONE LOGGED (the rest is literal):
  * his 16:9 stock and AI clips (salad, stressed dad, pizza, training, salad-eating, eggs, dad at the laptop, salad
    guy, cooking, steak, chicken, phone-on-plate, couple, gym, beach) sit in HIS olive card on HIS field -- the
    vertical mirror of how he cards the portrait photos in 16:9 (skill rule 3: never a 2.7x full-bleed crop).
  * his TEXT LEFT / DAN RIGHT screens (the note + title, IN TODAY'S EPISODE, the four bullet builds, the two photo
    panels, the meal-plan phone) become DAN ABOVE / TEXT BELOW.
  * 180.9-183.0: his "And adjust the calories... / So you still lose weight" lower third runs 2 s into the meal-plan
    phone beat; in the vertical the phone sits where the lower third would, so it ends when the phone comes in.
  * the app demo's last 1.6 s (6905-6954) is his own result screen (the goal image alone under "YOUR GOAL IMAGE",
    AI-labelled) -- rebuilt from the goal image, because that screen is not in the recording's usable window.
  * captions: his 16:9 has none; a vertical paid ad without them loses the muted feed, so ours carries the
    word-timed captions in his olive, muted under every graphic that prints its own words.
  * talking head: Dan's locked hair-anchored NEAR/FAR standard (zcrop.py), the level changing at every VISIBLE join.
"""
import json
FPS = 30000/1001
NTOT = 7036
DUR = NTOT / FPS          # 234.7678

LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
REF = f"{LIB}/00 ASSETS USED IN THE REFERENCE AD"
BA  = f"{LIB}/01 Before and After Images"
REV5 = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets"
GOAL = f"{BA}/dan by pool - AI GOAL IMAGE.png"
BEFORE = f"{BA}/00_ORIGINAL_deckchair_upscaled3x.jpg"

# (kind, n0, n1, spec) -- frames on HIS 29.97 grid
T = [
 ('window',    0,  138, dict(body='note', strikes=[0.45, 0.95, 1.45, 1.95, 2.45], text_h=450)),   # note ends ~1445, the lower third starts 1492 (audit: they overlapped at text_h 560)
 ('card',    138,  211, dict(media=BEFORE, blur=True)),
 ('cardv',   211,  280, dict(media='lifts/salad.mp4')),
 ('card',    280,  392, dict(media=f'{REV5}/fatdad_standing.jpg', ox=0.62, ar=3/4)),
 ('card',    392,  439, dict(media=f'{REV5}/fatdad_ride.jpg', ox=0.45)),
 ('bleed',   439,  449, dict(media=f'{REF}/07_SHOT4_photoshoot-standing.jpg', oy=0.30)),
 ('bleed',   449,  459, dict(media=f'{REF}/06_SHOT3_photoshoot-towel-smile.jpg', oy=0.30)),
 ('card',    459,  469, dict(media=f'{REF}/04_SHOT1_photoshoot-smiling-trees.png')),
 ('card',    469,  500, dict(media=f'{REF}/05_SHOT2_photoshoot-flag.jpg')),
 ('window',  500, 1035, dict(body='bullets', header="IN TODAY'S EPISODE", t_hdr=513,
                             items=["The one key change I made to finally lose my belly fat and get six-pack abs",
                                    "I didn't change my eating plan or my workouts at all",
                                    "One strange AI trick made my eating plan work far better"], item_n=[540, 734, 824])),
 ('why',    1035, 1194, dict(media=BEFORE)),
 ('talk',   1194, 1413, {}),
 ('cardv',  1413, 1488, dict(media=f'{REV5}/ai_busydad_kitchen.mp4', label=True)),        # his clip at 1:1 from 0 s (NCC r 0.98 on 5 frames)
 ('cardv',  1488, 1552, dict(media='lifts/pizza.mp4')),
 ('talk',   1552, 1736, {}),
 ('cardv',  1736, 1810, dict(media='lifts/training.mp4')),
 ('cardv',  1810, 1895, dict(media='lifts/salad_eat.mp4', ss=(1810-1794))),
 ('talk',   1895, 2061, {}),
 ('cardv',  2061, 2133, dict(media='lifts/eggs.mp4')),
 ('card',   2133, 2209, dict(media=f'{REV5}/fatdad_ride.jpg', ox=0.45, blur=True)),
 ('talk',   2209, 2306, {}),
 ('cardv',  2306, 2445, dict(media='lifts/dad_laptop.mp4', label=True, crop=(0.12, 0.09, 0.88, 0.91))),         # lifted 2306-2445 (139 frames = the beat: no held tail)   # lifted from his render: the window is inset past his burned label (top-left) -- still a downscale
 ('talk',   2445, 2605, {}),
 ('fatdan', 2605, 2763, dict(media=f'{REF}/03_CLIP_heavier-dan-looks-at-phone.mp4', caption='AI picture of myself with the body I wanted')),
 ('talk',   2763, 2882, {}),
 ('lock',   2882, 3020, dict(media=GOAL, blur=True)),
 ('talk',   3020, 3122, {}),
 ('card',   3122, 3220, dict(media=GOAL, blur=True, label=True)),
 ('talk',   3220, 3549, {}),
 ('window', 3549, 3616, dict(body='panels', media=[f'{REF}/06_SHOT3_photoshoot-towel-smile.jpg', f'{REF}/07_SHOT4_photoshoot-standing.jpg'], text_h=520)),
 ('talk',   3616, 3753, {}),
 ('window', 3753, 3911, dict(body='bullets', header=None, items=["You can generate an AI image of yourself with ripped six-pack abs"],
                             item_n=[3763], tail=("COMPLETELY FREE", 3866))),
 ('talk',   3911, 3994, {}),
 ('title',  3994, 4105, dict(headline="There's a second reason", sub="Every one of those diets failed")),
 ('talk',   4105, 4240, {}),
 ('window', 4240, 4463, dict(body='bullets', header=None, items=["Somebody with different work hours", "Different budget", "Different body",
                             "Different taste for foods that you honestly hate"], item_n=[4249, 4286, 4316, 4361])),
 ('cardv',  4463, 4561, dict(media='lifts/salad_guy.mp4', ss=5)),            # his cut is ON the flash peak (4463); the lift (4458-4561) is entered 5 frames in (re-audit N1: five frames of his 16:9 screen inside our card)
 ('talk',   4561, 4739, {}),
 ('window', 4739, 4860, dict(body='bullets', header="YOUR PLAN GETS BUILT AROUND", t_hdr=4741,
                             items=["The foods you actually eat", "Your real schedule"], item_n=[4749, 4825])),
 ('cardv',  4860, 4930, dict(media='lifts/cooking.mp4', crop=(0.12, 0.02, 0.88, 0.66), rate=70/58)),   # his clip dissolves into Dan over its last 12 frames; ours plays the clean 58 frames 1.2x slower to fill the beat (no held tail -- the watch scan flagged 9 frozen frames)   # his burned lower third sits in the clip's bottom fifth; the window stays above it (still a downscale)
 ('talk',   4930, 5120, {}),
 ('cardv',  5120, 5156, dict(media='lifts/steak.mp4')),
 ('cardv',  5156, 5229, dict(media='lifts/chicken.mp4')),
 ('talk',   5229, 5422, {}),
 ('window', 5422, 5638, dict(body='phone', media=f'{REF}/12_APP_meal-plan.png', scroll=(130, 530), text_h=760)),   # ends ON his picture cut (5638), not 3 frames before it (audit: a 3-frame flicker shot)
 ('talk',   5638, 5752, {}),
 ('cardv',  5752, 5903, dict(media='lifts/phone_plate.mp4')),
 ('window', 5903, 6031, dict(body='bullets', header=None, items=["No weighing everything out.", "No guessing.", "No giving up on day 11."],
                             item_n=[5913, 5953, 5982])),
 ('talk',   6031, 6360, {}),
 ('card',   6360, 6425, dict(media=f'{REF}/07_SHOT4_photoshoot-standing.jpg', blur=True)),
 ('cardv',  6425, 6510, dict(media=f'{REV5}/ai_women_pool.mp4', label=True)),
 ('cardv',  6510, 6558, dict(media=f'{REV5}/ai_respect_gym.mp4', label=True)),
 ('cardv',  6558, 6635, dict(media=f'{REV5}/ai_health_beachrun.mp4', label=True)),
 ('talk',   6635, 6716, {}),
 ('app',    6716, 6954, dict(media=f'{REF}/09_CLIP_app-generate-future-self.mp4', result_n=6905, blur=True)),
 ('talk',   6954, NTOT, {}),
]

# his overlays on the footage (frames)
OVERLAYS = [
 dict(kind='lt',   n0=75,   n1=138,  lines=["For the same reason", "they failed me"], y_bottom=1650),
 dict(kind='chip', n0=1198, n1=1258, label="Day 1",  text="You're motivated"),
 dict(kind='chip', n0=1258, n1=1330, label="Day 3",  text="It's still new."),
 dict(kind='chip', n0=1330, n1=1355, label="Day 3",  text="It's still kind of exciting."),
 dict(kind='chip', n0=1355, n1=1413, label="Day 11", text="You're tired"),
 dict(kind='lt',   n0=1606, n1=1736, lines=["Your diet doesn't lose to a craving", "It loses to a bad week"]),
 dict(kind='lt',   n0=1903, n1=1975, lines=["Average motivation"], weights=["ExtraBold"], sizes=[56]),
 dict(kind='lt',   n0=1975, n1=2061, lines=["Average results"], weights=["ExtraBold"], sizes=[56]),
 dict(kind='lt',   n0=2458, n1=2605, lines=["That's where our strange", "AI trick comes in"]),
 dict(kind='lt',   n0=3035, n1=3122, lines=["It's so much better than saying", "“I want to lose twenty pounds.”"]),
 dict(kind='lt',   n0=3324, n1=3438, lines=["It stopped being a wish", "It started being a fact"]),
 dict(kind='lt',   n0=3438, n1=3549, lines=["This is how I'm supposed to look", "This is how I need to look"]),
 dict(kind='lt',   n0=3623, n1=3753, lines=["So take the first step, and give yourself the fuel", "to finally lose your stubborn belly fat."],
      weights=["SemiBold", "SemiBold"], sizes=[40, 40]),
 dict(kind='pill', n0=3931, n1=3994, top="Get A FREE AI Image Of Yourself", big="With Abs"),
 dict(kind='lt',   n0=4572, n1=4655, lines=["That is not weak willpower", "That's a bad plan"]),
 dict(kind='lt',   n0=4874, n1=4930, lines=["How much time you've", "actually got to cook"], y_bottom=1650),
 dict(kind='lt',   n0=4941, n1=5022, lines=["Hate most vegetables?", "No problem"]),
 dict(kind='lt',   n0=5028, n1=5120, lines=["It builds your plan", "around the few you like"]),
 dict(kind='lt',   n0=5232, n1=5319, lines=["AI will build your meal plan", "around steak"]),
 dict(kind='lt',   n0=5319, n1=5422, lines=["And adjust the calories in your other foods", "So you still lose weight"]),
 dict(kind='lt',   n0=5642, n1=5752, lines=["Your AI nutrition coach", "will be there with you at every single meal"],
      weights=["ExtraBold", "SemiBold"], sizes=[52, 40]),
 dict(kind='lt',   n0=6125, n1=6210, lines=["Fat loss stalls?", "It adjusts your calories"]),
 dict(kind='lt',   n0=6210, n1=6336, lines=["Starving all day?", "It changes the foods"]),
 dict(kind='pill', n0=6961, n1=NTOT, top="Get A FREE AI Image Of Yourself", big="With Abs"),
]

# his light-leak flashes: a 3-pulse strobe over ~10 frames at four cuts, measured on his 256x144 cut. The screen-blend
# strength per frame is recovered from HIS luma trace against the unflashed level on each side of the cut
# (k = (his - base) / (255 - base); base = the frame before the window on the outgoing side, the settled level after it
# on the incoming side; the cut is the first peak). Applied to OUR frames with the same k -- not a guessed envelope.
def _flash_windows():
    import numpy as np
    his = np.memmap('his256.gray', np.uint8, 'r').reshape(-1, 144, 256)
    m = his.reshape(len(his), -1).mean(1)
    out = {}
    for n0, n1 in ((208, 221), (497, 509), (2760, 2772), (4460, 4470)):
        seg = m[n0:n1]; peak = n0 + int(np.argmax(seg))
        pre, post = float(m[n0-1]), float(np.median(m[n1+1:n1+5]))
        for n in range(n0, n1):
            base = pre if n < peak else post
            k = (float(m[n]) - base) / max(255.0 - base, 1.0)
            if k > 0.10: out[n] = round(min(k, 1.0), 3)
    return out
FLASH = _flash_windows()
FLASHES = sorted(FLASH)

NO_CAPS_KINDS = {'why', 'title', 'lock', 'app', 'fatdan'}          # beats that print their own words
NO_CAPS_BODIES = {'note', 'bullets', 'phone'}                       # window bodies that print words
NO_CAPS_OVERLAYS = {'lt', 'chip', 'pill'}

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
    for b in tl: print(f"{b['kind']:7s} {b['n0']:5d}-{b['n1']:5d}  {b['t0']:8.3f}-{b['t1']:8.3f}  {str(b.get('media', b.get('body', '')))[-44:]}")
    for o in ov:
        assert o['n1'] > o['n0'], o
