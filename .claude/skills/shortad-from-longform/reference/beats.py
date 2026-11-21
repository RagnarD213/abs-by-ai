#!/usr/bin/env python3
"""Beat sheet for the 9:16 rebuild -- Muhammad's final cut, STEPPED AT 1 SECOND AND
REPRODUCED BEAT FOR BEAT.

Attempt 1 sampled his cut at 4-second intervals and substituted freely where inspection
was thin; Dan's verdict was "a lot missing ... not reproducing Muhammad's video at all".
Every entry below is a MEASUREMENT off his render:

  * 233 frames at 1 s were read as contact sheets, then every boundary was pinned to
    +-0.05 s from a 10 fps frame-difference peak (ref_audit/feat10.json);
  * the talking head's framing was fitted per 0.25 s against the conform
    (ref_audit/cover.json) -- see PUSHES;
  * the ten white light-leak transitions were found by luma (>1.9x the median);
  * the seven lower thirds and every text reveal were read off the frames.

Deviations from his cut are ONLY the standing content rules, and each is logged in
DEVIATIONS with the reason.
"""
import json, re

W = json.load(open('m.whisper.json'))
_n = lambda s: re.sub(r"[^a-z0-9]", '', s.lower())
WORDS = [(_n(w['word']), float(w['start']), float(w['end']))
         for s in W['segments'] for w in s.get('words', []) if _n(w['word'])]
DUR = 232.768

def B(kind, a, b, **kw): return dict(kind=kind, t0=round(a, 3), t1=round(b, 3), **kw)

CTA_TOP, CTA_BIG = 'Get A FREE AI Image Of Yourself', 'With Abs'

# ---------------------------------------------------------------------------
#  BASE LAYER -- what fills the frame. Gaps are `talk`.
#  kinds: talk | bleed | card | window | stmt | title | winmedia
# ---------------------------------------------------------------------------
BEATS = [
 # -- hook -------------------------------------------------------------------
 # 2.80-6.75 HIS CARD IS A SIDE-BY-SIDE BEFORE/AFTER (heavier Dan left, goal phone right,
 # dashed arrow between). BANNED in our paid ads -> cut SEQUENTIALLY instead, same total
 # length, same "200 POUNDS" kicker on the first half.
 B('card',  2.95,  4.95, media='before_200lb', kicker='200 pounds', caps=False),
 # phone_mock and p_goal already carry a burned AI-GENERATED chip above the picture;
 # a plate label would print a second one.
 B('card',  4.95,  6.75, media='phone_mock'),
 # 12.30-13.05 three "today" photos, ~0.25 s each
 B('bleed', 12.30, 12.55, media='today_towel'),
 B('bleed', 12.55, 12.80, media='today_trees'),
 # the flag photo holds under the flash instead of leaving a 0.55 s talk island
 B('bleed', 12.80, 13.60, media='today_flag'),
 B('window', 13.60, 26.95, header="In today's episode", bullets=[
     'How I got limitless motivation to work out, to eat healthy.',
     'What I needed to do to lose my belly fat and get six-pack abs.',
     'How you can generate a goal picture of yourself with abs for free.']),
 # -- conditioning -----------------------------------------------------------
 B('title', 43.90, 47.95, headline='Visualizing your goal',
   sub='One of the most powerful ways to motivate yourself'),
 B('card',  47.95, 50.45, media='bodybuilder'),
 B('bleed', 61.45, 66.30, media='photoshop_gag'),
 B('winmedia', 68.45, 75.80, media='app_flow_a'),
 B('bleed', 81.20, 86.90, media='bl_home_abs'),
 B('window', 91.85, 97.05, header=None, bullets=[
     'You can generate an AI image of yourself with ripped six-pack abs',
     'COMPLETELY FREE']),
 # -- stakes -----------------------------------------------------------------
 B('card',  101.50, 106.25, media='ai_women_pool', label='AI-GENERATED'),
 B('card',  106.25, 107.60, media='ai_respect_gym', label='AI-GENERATED'),
 B('card',  107.60, 111.00, media='ai_beachrun', label='AI-GENERATED'),
 B('bleed', 113.95, 116.30, media='bl_older_man'),
 B('bleed', 116.30, 117.95, media='bl_salad'),
 # -- personal story ---------------------------------------------------------
 B('card',  126.40, 128.75, media='before_200lb'),
 B('card',  132.40, 134.00, media='dad_kids'),
 B('card',  134.00, 136.30, media='ai_busydad', label='AI-GENERATED'),
 B('bleed', 136.30, 137.90, media='bl_alone_gym'),
 B('card',  137.90, 142.85, media='phone_mock'),
 # HIS 2:29 runs full frame; Dan lies horizontally across it, so a 9:16 crop shows
 # grass and his legs. Carded at 4:3 -- the whole movement stays on screen.
 B('card',  148.80, 152.45, media='outdoor_abs'),
 B('bleed', 152.45, 153.75, media='bl_mealprep'),
 B('bleed', 153.75, 155.10, media='bl_track'),
 B('bleed', 155.10, 159.50, media='bl_crunch_gym'),
 # -- product ----------------------------------------------------------------
 B('card',  159.50, 162.40, media='p_goal'),
 B('window', 162.40, 171.80, header=None, bullets=[
     'I created an app that helps other guys generate a picture of their fitness goal for free.',
     'It’s designed purely for making fitness transformation images of men like you.']),
 B('stmt',  171.80, 177.25, parts=[
     ('Its far superior at making these images than', 'ink'),
     ('Chat GPT', 'olive'), ('Or any general purpose AI', 'big')]),
 B('bleed', 187.30, 199.75, media='app_flow_b'),
 B('bleed', 208.10, 213.10, media='bl_abwheel'),
 B('bleed', 216.30, 220.75, media='bl_eating'),
 B('window', 220.75, 228.50, header=None, bullets=[
     'Generating an image of yourself with abs is the first step.',
     'Our personalized AI fitness program helps you make it real.']),
]

# ---------------------------------------------------------------------------
#  OVERLAYS -- sit ON the picture, they do not replace it
# ---------------------------------------------------------------------------
LOWER_THIRDS = [
 B('lt',  36.90,  43.90, lines=['The Problem', 'No time, no motivation']),
 B('lt',  86.90,  91.85, lines=["If you saw yourself with abs, you'd be MOTIVATED",
                                'to make your dream body a reality']),
 B('lt', 111.00, 113.95, lines=['You will probably live longer too']),
 B('lt', 118.60, 126.40, lines=["You don't need more knowledge",
                                'You need motivation to execute what you know']),
 B('lt', 183.00, 185.04, lines=['Your AI generated picture is just step 1']),
 B('lt', 200.00, 203.40, lines=['It builds you a customized',
                                'Workout & Nutrition Plan']),
 B('lt', 213.20, 216.30, lines=['Your Nutrition Plan',
                                'Is calibrated exactly for your goal']),
]
CTAS = [
 B('cta',  99.00, 100.62, top=CTA_TOP, big=CTA_BIG),
 B('cta', 179.70, 181.30, top=CTA_TOP, big=CTA_BIG),
 B('cta', 231.40, DUR,    top=CTA_TOP, big=CTA_BIG),
]
# White light-leak transitions, centred on the ten luma peaks in his render.
FLASHES = [(6.72, 7.16), (13.16, 13.60), (27.01, 27.45), (50.46, 50.90), (66.21, 66.65),
           (75.77, 76.21), (128.68, 129.22), (142.76, 143.26), (177.22, 177.70),
           (199.61, 200.12), (152.10, 152.62)]
# 152.10 is his eleventh: the luma detector folded it into the bright white-kitchen
# run that follows, but the paired 105.9/63.5 frame-diff spikes are the flash's own.

# ---------------------------------------------------------------------------
#  ZOOM PUSHES on the talking head -- (ramp-in start, ramp-in end, ramp-out start,
#  ramp-out end). Scale 1.20, crop recentred 85 px UP in the 1080-tall source.
#
#  THIS IS THE THING ATTEMPT 1 DID NOT HAVE. It rendered every talk segment at one fixed
#  crop. His cut pushes in and pulls out fourteen times, and roughly a third of the
#  talking head is in a push at any moment -- which is what stops a locked-off tripod
#  shot reading as a webcam recording. (The [R1] rule that he "alternates 1.00/1.20
#  ACROSS SPLICES" is not what the frames show: the pushes RAMP over ~0.5 s and mostly
#  span splices rather than landing on them. Measured, not assumed -- see notes.md.)
# ---------------------------------------------------------------------------
PUSHES = [
 ( 0.00,  0.00,   2.60,  2.78),   # hook opens already punched
 (10.55, 11.05,  12.20, 12.30),
 (32.65, 33.20,  35.60, 36.30),
 (51.90, 52.50,  54.80, 55.60),
 (66.25, 66.80,  68.10, 68.45),
 (76.05, 76.55,  78.85, 79.60),
 (99.90, 100.50, 101.35, 101.50),
 (110.90, 111.50, 113.05, 113.60),
 (128.85, 129.35, 132.30, 132.40),
 (143.10, 143.55, 147.25, 148.60),
 (177.30, 177.80, 179.70, 179.95),
 (184.95, 185.50, 187.10, 187.30),
 (203.85, 204.30, 206.55, 207.85),
 (228.40, 229.00, 231.25, 231.95),
]
PUSH_Z = 1.20

DEVIATIONS = [
 ("2.80-6.75", "His card is a SIDE-BY-SIDE before/after with a dashed arrow. Banned in "
               "our paid ads. Cut sequentially: the 200-lb photo with his '200 POUNDS' "
               "kicker, then the phone holding the goal image."),
 ("68.45-75.80 and 187.30-199.75",
               "His product recording runs to its own end, which reaches the in-app "
               "BEFORE/AFTER at 26 s and the email-capture form at 29 s. Ours is held to "
               "the 0-25.0 s window and asserted in QC."),
 ("0.00-2.20",  "His animated callout box frames the photo taped to the door at the far "
                "LEFT of his 16:9 frame. That x-range is outside the 9:16 crop, so the "
                "box would point at nothing. Dropped."),
 ("all AI clips", "AI-GENERATED labels added; his cut labels only some of them. His four\n                  AI clips also run FULL FRAME; ours are 1280x720, which is a 2.67x\n                  upscale at full bleed, so they go in his olive card instead -- a\n                  downscale, and still his own design language."),
 ("captions",   "His cut has none. Dan asked for full word-timed captions (his call from "
                "attempt 1); suppressed under every graphic that carries its own words."),
]

NO_CAPS_KINDS = {'window', 'title', 'stmt', 'cta'}
BASE_KINDS    = {'talk', 'window', 'card', 'title', 'stmt', 'bleed', 'winmedia'}

def timeline():
    """Base layer covering 0..DUR with `talk` filling every gap."""
    base = sorted([b for b in BEATS if b['kind'] in BASE_KINDS], key=lambda b: b['t0'])
    fixed, t = [], 0.0
    for b in base:
        b = dict(b)
        b['t0'] = max(b['t0'], t)
        if b['t1'] - b['t0'] < 0.20: continue
        gap = b['t0'] - t
        if gap > 0.40: fixed.append(dict(kind='talk', t0=round(t, 3), t1=round(b['t0'], 3)))
        elif gap > 0:  b['t0'] = t
        fixed.append(b); t = b['t1']
    if DUR - t > 0.10: fixed.append(dict(kind='talk', t0=round(t, 3), t1=DUR))
    return fixed, LOWER_THIRDS + CTAS

def push_at(t):
    """Scale of the talking-head crop at time t (1.00 wide .. 1.20 punched)."""
    best = 0.0
    for a1, a2, b1, b2 in PUSHES:
        k = 1.0 if a2 <= a1 else max(0.0, min(1.0, (t - a1) / (a2 - a1)))
        ko = 0.0 if b2 <= b1 else max(0.0, min(1.0, (t - b1) / (b2 - b1)))
        r = min(k, 1 - ko)
        if t < a1: r = 0.0
        best = max(best, r * r * (3 - 2 * r))
    return 1.0 + (PUSH_Z - 1.0) * best

if __name__ == '__main__':
    tl, ov = timeline()
    print(f'{"kind":9s} {"t0":>8s} {"t1":>8s} {"len":>6s}  detail')
    for b in tl:
        det = b.get('media') or b.get('header') or b.get('headline') or ''
        if b['kind'] == 'window' and not det: det = b['bullets'][0][:46]
        print(f'{b["kind"]:9s} {b["t0"]:8.2f} {b["t1"]:8.2f} {b["t1"]-b["t0"]:6.2f}  {det}')
    tot = sum(b['t1']-b['t0'] for b in tl)
    ins = sum(b['t1']-b['t0'] for b in tl if b['kind'] != 'talk')
    assert abs(tot-DUR) < 0.02, f'timeline {tot} != {DUR}'
    short = [b for b in tl if b['t1']-b['t0'] < 0.30]
    print(f'\nbase segments {len(tl)}   covers {tot:.3f}s')
    print(f'insert/graphic coverage {ins:.1f}s = {100*ins/DUR:.0f}%   (his cut: 58%)')
    print(f'lower thirds {len(LOWER_THIRDS)} (his: 7)   CTAs {len(CTAS)} (his: 3)   '
          f'flashes {len(FLASHES)} (his: 10)   pushes {len(PUSHES)} (his: 14)')
    print(f'segments under 0.30s: {len(short)}')
    pushed = sum(1 for i in range(int(DUR*10)) if push_at(i/10) > 1.05)/10
    talk = sum(b['t1']-b['t0'] for b in tl if b['kind']=='talk')
    print(f'talk {talk:.1f}s, of which pushed {pushed:.1f}s = {100*pushed/talk:.0f}%')
