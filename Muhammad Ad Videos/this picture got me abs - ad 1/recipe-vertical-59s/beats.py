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


# --- phrase anchors -----------------------------------------------------------
# The cutdown selects by WHAT IS SAID, not by timecode, so its ranges survive every beat
# edit. `after=` is not optional wherever a phrase repeats ("tap the button below",
# "lose your belly fat"): without it the anchor matches the first occurrence and the beat
# comes out with a negative duration.
def _seq(phrase, after=0.0):
    toks = [_n(t) for t in phrase.split() if _n(t)]
    for i in range(len(WORDS)):
        if WORDS[i][1] < after: continue
        if [w[0] for w in WORDS[i:i+len(toks)]] == toks: return i, len(toks)
    raise ValueError(f'phrase not found after {after}: {phrase!r}')

def at(phrase, after=0.0):
    i, _ = _seq(phrase, after); return WORDS[i][1]

def end(phrase, after=0.0):
    i, n = _seq(phrase, after); return WORDS[i+n-1][2]

# Filled in by sqcutdown.py so captions.py can stop a held last word at a cutdown seam
# (lesson A6.14): without it the last line of every range rides across the join.
SEAMS = []

CTA_TOP, CTA_BIG = 'Get A FREE AI Image Of Yourself', 'With Abs'

# ---------------------------------------------------------------------------
#  BASE LAYER -- what fills the frame. Gaps are `talk`.
#  kinds: talk | bleed | card | window | stmt | title | winmedia
# ---------------------------------------------------------------------------
BEATS = [
 # -- hook -------------------------------------------------------------------
 # ATTEMPT 3 REV 1 (Dan): deviate from Muhammad here -- the goal picture FULL SCREEN
 # over the whole hook line, as a freshly AI-GENERATED video: a high-tech holographic
 # scan animating over the photograph (Veo 3.1 Fast from the clean goal still, chip
 # burned in). Replaces the inset-graphic approach from Dan's earlier rewrite.
 # REV 3 (Dan's pick after seeing both variants): the picture ALONE with the slow push --
 # no scan animation. The scan variant asset stays in assets_v/ if he ever wants it back.
 B('bleed', 0.00,  2.95, media='ai_goal_plain'),
 B('card',  2.95,  6.75, media='before_200lb', kicker='200 pounds', caps=False),
 # ATTEMPT 3 rev 5: Dan -- hold the "today" photos 1-2 s longer. Montage now runs
 # 11.45-14.30 (2.85 s, was 1.30): backwards over "And this is where I'm at today"
 # (11.60-13.10, exactly these photos' subject) and forwards 0.70 s into the episode
 # window. The one place Dan authorised running longer than his cut.
 B('bleed', 11.45, 12.40, media='today_towel'),
 B('bleed', 12.40, 13.35, media='today_trees'),
 B('bleed', 13.35, 14.30, media='today_flag'),
 B('window', 14.30, 26.95, header="In today's episode", bullets=[
     'How I got limitless motivation to work out, to eat healthy.',
     'What I needed to do to lose my belly fat and get six-pack abs.',
     'How you can generate a goal picture of yourself with abs for free.']),
 # -- conditioning -----------------------------------------------------------
 B('title', 43.90, 47.95, headline='Visualizing your goal',
   sub='One of the most powerful ways to motivate yourself'),
 B('card',  47.95, 50.45, media='bodybuilder'),
 B('bleed', 61.45, 66.30, media='photoshop_gag'),
 # ATTEMPT 3 rev 3: "you have to show the after when we generate like that" (Dan, 1:14).
 # The recording is still capped at 0-25 s (the in-app before/after and email form stay
 # banned) -- so the payoff is the app's own "Download Your Future Self" screen at 27-30 s
 # CROPPED to exclude the email form (crop=1320:1600:0:170 ends above it; verified frame
 # by frame), shown SEQUENTIALLY as its own card. after_reveal.mp4 carries confetti +
 # the finished after image.
 B('winmedia', 68.45, 73.60, media='app_flow_a'),
 B('card',  73.60, 75.80, media='after_reveal'),
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
 # ATTEMPT 3 rev 8: BOTH fat-dad photos, head AND stomach in frame, backpack child
 # cropped out (subject-sized crops in assets_v/, not the media's own centre).
 B('card',  132.40, 133.25, media='dad_ride'),
 B('card',  133.25, 134.00, media='dad_standing'),
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
 # ATTEMPT 3 rev 3, second site (Dan's 3:19): the full-frame product run now ends on
 # the after-reveal card instead of cutting away before the payoff.
 B('bleed', 187.30, 197.30, media='app_flow_b'),
 B('card',  197.30, 199.75, media='after_reveal'),
 B('bleed', 208.10, 213.10, media='bl_gym_workout'),
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
# (rev 1: the inset-graphic opening was replaced by the full-screen AI scan video above)
INSETS = []
# White light-leak transitions -- HIS extracted template (gfx/flash_tmpl.mp4), peak at
# a+0.11. MEASURED PROPERTY OF HIS CUT: the content cut lands EXACTLY on the flash peak
# (verified on his w01/w06/w09 instances) -- so each peak below sits ON our matching beat
# boundary, not on his absolute timecode (attempt 2's windows were 0-5 frames off our
# cuts, which reads as a flash that happens NEAR a cut instead of hiding it).
# The 13.16 flash moved with the montage->window boundary to 14.30 (rev 5).
FLASHES = [(6.64, 7.08), (14.19, 14.63), (26.84, 27.28), (50.34, 50.78), (66.19, 66.63),
           (75.69, 76.13), (128.64, 129.08), (142.74, 143.18), (177.14, 177.58),
           (199.64, 200.08), (152.10, 152.62)]
# 152.10 is his eleventh: the luma detector folded it into the bright white-kitchen
# run that follows, but the paired 105.9/63.5 frame-diff spikes are the flash's own.
# It sits mid-beat in his cut too, so it keeps his absolute time.

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
 ("0.00-2.75",  "His callout frames the print taped to the door, which is outside the "
                "9:16 crop. ATTEMPT 3: per Dan's rewrite the goal picture is shown as an "
                "inset GRAPHIC with his callout stroke instead (INSETS)."),
 ("11.45-14.30","Dan's rev 5: the 'today' photos hold 1.55 s longer than his cut -- the "
                "one authorised duration deviation. Time taken from the preceding talk "
                "('And this is where I'm at today') and 0.70 s of the episode window."),
 ("73.60-75.80 and 197.30-199.75",
                "Dan's rev 3: his cut never shows the generation's result. The app's own "
                "after-reveal screen (cropped above the email form) is added as a card at "
                "both product beats' ends."),
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
    return fixed, LOWER_THIRDS + CTAS + INSETS

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
