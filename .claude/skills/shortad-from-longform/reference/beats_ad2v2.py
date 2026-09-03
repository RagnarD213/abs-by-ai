#!/usr/bin/env python3
"""Ad 2 vertical, V2 -- his beat sheet stepped off MUHAMMAD'S V2 HD render (2026-09-03).

V2 differs from his V1 in exactly five picture windows (measured: per-frame diff of the two
renders, everything else identical to the frame) -- his own execution of Dan's six round-1
notes -- and in a few seconds of SFX. Every boundary inside those windows is his, read off
V2 at the frame: `F(n)` is frame n of his render. Everything outside them is the V1-derived
sheet Dan has already reviewed three times.

DEVIATIONS FROM HIS V2, EVERY ONE LOGGED:
  * his museum clip and conveyor clip carry no AI label; ours do (standing rule).
  * 149.85-155.39: he puts the two fat-dad photos in olive CARDS; Dan's own note asked for
    them "full screen with motion", so they stay full-bleed with the slow push, at HIS timing
    and with his blur-through between them.
  * 193.26-198.16: his stock air-bike clip is 16:9 and dark; Dan's own toe-touch footage
    stays (real, graded, no casting question), at his timing.
  * 198.16-204.17: his phone-beside-Dan split is reproduced (Dan above, phone below), but
    the phone shows the EMAIL-CAPTURE SCREEN from 202.0 in his cut -- a banned screen for our
    ads -- so ours shows the compliant after-only result there instead.
  * the "Meet the new you" after-only card that rev 3 ran 204.0-207.67 is gone: his V2 cuts
    back to Dan at 204.17 under a flash.
"""
import json
FPS = 30000/1001
DUR = 276.109167
PUSH_Z = 1.20
F = lambda n: n/FPS          # frame n of HIS render, exactly (cumulative rounding lands on it)

# ---- his push schedule, read off the per-0.25 s framing fit of his own render ----------
def _pushes():
    C = json.load(open('cover.json'))
    on = [c['t'] for c in C if c['r'] >= 0.62 and c['scale'] >= 1.13]
    runs, cur = [], []
    for t in on:
        if cur and t - cur[-1] > 1.01: runs.append(cur); cur = []
        cur.append(t)
    if cur: runs.append(cur)
    out = []
    for r in runs:
        if len(r) < 2: continue
        a, b = r[0], r[-1] + 0.5
        out.append((round(a-0.55,3), round(a,3), round(b,3), round(b+0.55,3)))
    return out
PUSHES = _pushes()

INK_C, OLIVE_C = (255, 255, 255), (140, 153, 91)
HOWDO = [('Because even though I was a nutrition coach back in the day, as a', INK_C),
         ('38 year old', OLIVE_C),
         ('dad running a successful', INK_C),
         ('ad agency.', OLIVE_C)]

# ---- the timeline ---------------------------------------------------------------------
T = [
 ('talk',   0.000,   F(107), {}),
 ('bleed',  F(107),  F(216), dict(media='museum', label='AI-GENERATED', chip_y=1060)),   # V2: hard cut in AND out; chip above his caption band, plaque left readable below
 ('talk',   F(216),  23.991, {}),                                              # V2: camera runs through; his flash at F(422)
 ('card',  23.991,  31.630, dict(media='spa')),
 ('talk',  31.630,  39.072, {}),
 ('window',39.072,  45.010, dict(header="I'll show you", bullets=[
      'How to use AI to fix your diet.', 'Lose your belly fat.', 'And get six pack abs.'])),
 ('talk',  45.010,  50.384, {}),
 ('window',50.384,  56.690, dict(header='1) Why AI is better than human nutritionists.', bullets=[
      'Human nutritionists are incredibly expensive.', 'A hundred bucks or more for one session'])),
 ('talk',  56.690,  63.096, {}),
 ('bleed', 63.096,  66.667, dict(media='groceries')),
 ('bleed', 66.667,  F(2066), dict(media='mealprep')),
 ('bleed', F(2066), F(2199), dict(media='conveyor', label='AI-GENERATED')),   # V2: 68.94 -> flash at 73.37
 ('talk',  F(2199), 98.950, {}),
 ('window',98.950, 108.210, dict(header='3) AI gives you a science-based nutrition plan.', bullets=[
      'Most human nutrition coaches are just repeating bro-science.',
      'Whatever diet happens to be trending that year.'])),
 ('talk', 108.210, 118.485, {}),
 ('card', 118.485, 127.390, dict(media='app_soup')),
 ('talk', 127.390, 141.074, {}),
 ('window',141.074, F(4491), dict(header='How do I know all this?', bullets=[HOWDO])),   # V2: flash at 149.85
 ('bleed2',F(4491), F(4657), dict(media_a='fatdad_a', media_b='fatdad_b', split=F(4563))),  # V2: blur-through at 152.24, flash out at 155.39
 ('talk',  F(4657), 157.250, {}),
 ('bleed',157.250, 161.061, dict(media='before_dan')),
 ('bleed',161.061, 165.230, dict(media='goal_dan', label='AI-GENERATED')),
 ('talk', 165.230, 169.903, {}),
 ('bleed',169.903, 171.170, dict(media='flag')),
 ('talk', 171.170, 183.170, {}),
 ('card', 183.170, 191.191, dict(media='app_upload')),
 ('card', 191.191, F(5792), dict(media='app_gen')),                            # V2: flash at 193.26 into the workout clip
 ('bleed', F(5792), F(5939), dict(media='workout')),                           # V2: hard cut at 198.16 into the split
 ('winmedia', F(5939), F(6119), dict(media='scan_result')),                    # V2: phone + Dan, flash out at 204.17
 ('talk',  F(6119), 222.150, {}),                                              # V2: Dan full frame (no "Meet the new you" card)
 ('window',222.150,229.260, dict(header='It builds your meal plan', bullets=[
      'Around the foods you actually like.', 'Your diet style.', 'Your allergies',
      "How much time you've got to cook."])),
 ('talk', 229.260, 238.950, {}),
 ('card', 238.950, 244.340, dict(media='app_item')),
 ('talk', 244.340, 262.300, {}),
 ('card', 262.300, 268.000, dict(media='app_supp')),
 ('talk', 268.000, DUR,     {}),
]

# ---- his flashes ---------------------------------------------------------------------
# His light-leak covers every insert -> talk return in the V1-derived sheet (verified on his
# render), EXCEPT the museum clip's exit, which V2 hard-cuts. Three more were measured on V2
# that the auto rule cannot see: mid-talk at F(422) (left over from the deleted cartoon's
# return, over the 13.70 splice), the bullets -> photo card at F(4491), and the app card ->
# workout clip at F(5792). His content cut lands ON the flash peak, so the window is
# asymmetric: 0.10 s before the cut, 0.30 s after, peak at the cut (vlib.overlay_flash).
FLASH_PRE, FLASH_POST = 0.10, 0.30
NO_FLASH = {round(F(216), 3)}
EXTRA_FLASH = [F(422), F(4491), F(5792)]
FLASHES = []
for i in range(1, len(T)):
    if T[i][0] == 'talk' and T[i-1][0] != 'talk' and round(T[i][1], 3) not in NO_FLASH:
        FLASHES.append((round(T[i][1]-FLASH_PRE, 4), round(T[i][1]+FLASH_POST, 4)))
for a in EXTRA_FLASH:
    FLASHES.append((round(a-FLASH_PRE, 4), round(a+FLASH_POST, 4)))
FLASHES.sort()

OVERLAYS = [
 # V2 runs his caption band over the museum clip; our unboxed captions overprinted the exhibit's
 # engraved plaque (audit). His words, in his lower-third box, set low enough to sit over the plaque.
 dict(kind='lt',  t0=F(107)+0.10, t1=F(216)-0.15, lines=['AI has made human nutritionists',
                                                        'completely obsolete.'], y_bottom=1420),
 dict(kind='lt',  t0=F(2066), t1=73.250, lines=['2   Human nutritionists hand everybody',
                                               'the same generic meal plan.']),
 dict(kind='cta', t0=171.500, t1=176.000, top='Get A FREE AI Image of Yourself', big='With Abs'),
 dict(kind='cta', t0=176.200, t1=180.400, top='', big='Get access to the AI nutrition plan', big_size=46),
 dict(kind='cta', t0=272.300, t1=DUR,     top='Get A FREE AI Image of Yourself', big='With Abs'),
]

def timeline():
    tl = []
    for kind, t0, t1, spec in T:
        b = dict(kind=kind, t0=t0, t1=t1); b.update(spec); tl.append(b)
    ov = [dict(o) for o in OVERLAYS]
    return tl, ov

# beats whose own graphics carry words, or whose media fills the caption band -- captions
# are suppressed under these. His split (phone + Dan) runs without captions in V2 too.
NO_CAPS_KINDS = {'window', 'stmt', 'title', 'winmedia'}

def push_at(t):
    """His zoom at time t, for the QC check that the talking head is not one fixed crop."""
    z = 1.0
    for a1, a2, b1, b2 in PUSHES:
        if t < a1 or t > b2: continue
        k = 1.0 if t >= a2 else (t-a1)/max(a2-a1, 1e-6)
        if t > b1: k = min(k, max(0.0, 1-(t-b1)/max(b2-b1, 1e-6)))
        z = max(z, 1 + (PUSH_Z-1)*k)
    return z

if __name__ == '__main__':
    tl, ov = timeline()
    tot = sum(b['t1']-b['t0'] for b in tl)
    ins = sum(b['t1']-b['t0'] for b in tl if b['kind'] != 'talk')
    print(f'{len(tl)} beats, {tot:.3f}s (target {DUR:.3f})')
    print(f'insert/graphic coverage {100*ins/tot:.0f}%   changes/min {len(tl)/(tot/60):.1f}')
    longest = max((b['t1']-b['t0'], b['t0']) for b in tl if b['kind']=='talk')
    print(f'longest talking stretch {longest[0]:.1f}s at {longest[1]:.1f}')
    print(f'{len(PUSHES)} pushes, {len(FLASHES)} flashes, {len(ov)} overlays')
    bad = [i for i in range(1,len(tl)) if abs(tl[i]['t0']-tl[i-1]['t1'])>1e-6]
    print('gaps/overlaps:', bad if bad else 'none')
    prev = 0
    for i, b in enumerate(tl):
        cum = round(b['t1']*FPS); print(f'{i:3d} {b["kind"]:9s} {b["t0"]:8.3f}-{b["t1"]:8.3f} {cum-prev:5d}f  {b.get("media") or b.get("media_a") or b.get("header","")}'); prev = cum
    print('flashes at', [round(a+FLASH_PRE,3) for a, b in FLASHES])
