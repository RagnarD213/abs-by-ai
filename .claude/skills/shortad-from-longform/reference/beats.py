#!/usr/bin/env python3
"""Beat sheet for the 9:16 rebuild -- Muhammad's final cut, beat for beat.

Anchored to PHRASES, not seconds. The timeline is his and will not move, but a phrase
anchor still beats a hardcoded second: it says WHY a graphic is where it is, and it
survives the 0:59 cutdown, which re-times everything.

kinds:
  talk      full-bleed Dan (default; any gap between beats is talk)
  window    Dan in a top window, olive eyebrow + white bullets below
  card      olive card on the field holding a photo / clip / phone screen
  title     olive card holding a heavy oblique headline
  statement mixed-weight lines on the bare field
  bleed     full-frame footage (only for natively-vertical or 4K sources)
  cta       sage pill OVER Dan
  callout   animated stroke box OVER Dan
"""
import json, re

W = json.load(open('m.whisper.json'))
_n = lambda s: re.sub(r"[^a-z0-9]", '', s.lower())
WORDS = [(_n(w['word']), float(w['start']), float(w['end']))
         for s in W['segments'] for w in s.get('words', []) if _n(w['word'])]
SEQ = [w[0] for w in WORDS]
DUR = 232.768

def _i(phrase, after=0.0):
    toks = [_n(x) for x in phrase.split() if _n(x)]
    start = next((i for i, w in enumerate(WORDS) if w[1] >= after), 0)
    for i in range(start, len(SEQ)-len(toks)+1):
        if SEQ[i:i+len(toks)] == toks: return i
    raise KeyError(f'phrase not found after {after}: {phrase!r}')

def at(p, pad=-0.10, after=0.0):   return round(WORDS[_i(p, after)][1] + pad, 3)
def end(p, pad=0.12, after=0.0):
    i = _i(p, after) + len([x for x in p.split() if _n(x)]) - 1
    return round(WORDS[i][2] + pad, 3)

def B(kind, a, b, **kw): return dict(kind=kind, t0=round(a,3), t1=round(b,3), **kw)

CTA_TOP, CTA_BIG = 'Get A FREE AI Image Of Yourself', 'With Abs'

BEATS = [
 # ---------------------------------------------------------------- hook
 B('callout', 0.0, at('i generated this picture'), rect_src=(52, 300, 175, 592)),
 # HIS 0:03 CARD IS A SIDE-BY-SIDE BEFORE/AFTER, WHICH IS BANNED IN OUR PAID ADS.
 # Cut sequentially instead: the 200-lb photo first, the goal phone second.
 B('card', at('i generated this picture'), end('when i was 200 pounds'),
   media='before_200lb', kicker='200 pounds'),
 B('card', at('i made it my phone lock screen'), end('for more than a year'),
   media='phone_mock', portrait=True, label='AI-GENERATED'),
 B('bleed', at('and this is where im at today'), end('and this is where im at today'),
   media='outdoor_dan'),
 B('window', at('in todays episode'), end('with abs for free'),
   header="In today's episode", bullets=[
     'How I got limitless motivation to work out, to eat healthy.',
     'What I needed to do to lose my belly fat and get six-pack abs.',
     'How you can generate a goal picture of yourself with abs for free.']),
 # ---------------------------------------------------------------- conditioning
 B('bleed', at('you would lose your belly fat'), end('the knowledge isnt the problem'),
   media='bl_dumbbell'),
 B('title', at('visualizing your goal'), end('to motivate yourself'),
   headline='Visualizing your goal',
   sub='One of the most powerful ways to motivate yourself'),
 B('card', at('fitness models and bodybuilders'), end('for decades'), media='standing'),
 B('card', at('would literally photoshop'), end('it looked ridiculous'),
   media='photoshop_gag', caption='The old way: someone else’s body, your face'),
 B('bleed', at('with ai you can create a picture'), end('youve always wanted'),
   media='app_form'),
 B('bleed', at('youd realize how amazing youd look'), end('if you lost your stomach fat'),
   media='bl_home_abs'),
 B('window', at('and right now you can generate'), end('completely free'),
   header=None, bullets=[
     'You can generate an AI image of yourself with ripped six-pack abs — completely free.']),
 B('cta', at('just tap the button below'), end('to see yourself with abs'),
   top=CTA_TOP, big=CTA_BIG),
 # ---------------------------------------------------------------- stakes
 B('card', at('youre more attractive to women'), end('men respect you more'),
   media='ai_women_pool'),
 B('card', at('you feel better'), end('youve got more energy'), media='ai_respect_gym'),
 B('bleed', at('and youll probably live longer too'), end('and youll probably live longer too'),
   media='bl_run'),
 B('bleed', at('and eating healthy right now'), end('and eating healthy right now'),
   media='bl_salad'),
 # ---------------------------------------------------------------- personal story
 B('card', at('i wanted to get my abs back so bad'), end('or to eat healthy', after=126.0),
   media='before_200lb'),
 B('card', at('as a 38 year old dad'), end('stressful life', after=128.0),
   media='ai_busydad'),
 B('card', at('nothing worked to motivate me'), end('made it my phone lock screen', after=136.0),
   media='dad_kids'),
 B('bleed', at('and thats what gave me the fire'), end('to train hard and consistently'),
   media='outdoor_abs'),
 B('bleed', at('to meal prep every week'), end('to meal prep every week'), media='bl_mealprep'),
 B('bleed', at('to track my calories'), end('lose your belly fat', after=150.0),
   media='bl_crunch_gym'),
 # ---------------------------------------------------------------- product
 B('card', at('this one ai picture helped me so much'), end('this one ai picture helped me so much'),
   media='p_goal', label='AI-GENERATED'),
 B('window', at('that i created an app'), end('of men like you'), header=None, bullets=[
   'I created an app that helps other guys generate a picture of their fitness goal for free.',
   'It’s designed purely for making fitness transformation images of men like you.']),
 B('statement', at('so its far superior'), end('or any general purpose ai'),
   parts=[('Its far superior at making these images than', 'ink'),
          ('Chat GPT', 'olive'), ('Or any general purpose AI', 'big')]),
 B('cta', at('tap the button below', after=176.0), end('tap the button below', after=176.0) + 1.6,
   top=CTA_TOP, big=CTA_BIG),
 B('bleed', at('once you generate an image'), end('to make it real'), media='app_describe'),
 B('bleed', at('our ai scans your current picture'), end('your training status'), media='app_tuning'),
 B('bleed', at('then it scans your goal picture'), end('where you want to be'), media='app_render'),
 B('card', at('then it builds your customized'), end('just for you and your goal'),
   media='app_workout', portrait=True),
 B('bleed', at('it targets your lacking body parts'), end('equipment you actually have'),
   media='bl_kneeraise'),
 B('card', at('your nutrition plan is calibrated'), end('for your goal', after=212.0),
   media='app_nutri', portrait=True),
 B('bleed', at('and its built around the healthy foods'), end('actually stick to it'),
   media='bl_eating'),
 B('window', at('generating an image of yourself with abs is just'), end('helps you make it real'),
   header=None, bullets=[
     'Generating an image of yourself with abs is the first step.',
     'Our personalized AI fitness program helps you make it real.']),
 B('cta', at('to start losing your belly fat'), DUR, top=CTA_TOP, big=CTA_BIG),
]

# Captions are suppressed where the graphic carries its own words -- two text systems in
# a 1080-wide frame is unreadable, and the bullets paraphrase the very line being spoken.
NO_CAPS = {'window', 'title', 'statement', 'cta'}

BASE_KINDS = {'talk', 'window', 'card', 'title', 'statement', 'bleed'}
OVERLAY_KINDS = {'cta', 'callout'}

def timeline():
    """Base layer covering 0..DUR with `talk` filling every gap, plus the overlay list."""
    base = sorted([b for b in BEATS if b['kind'] in BASE_KINDS], key=lambda b: b['t0'])
    fixed, t = [], 0.0
    for b in base:
        b = dict(b)
        b['t0'] = max(b['t0'], t)
        if b['t1'] - b['t0'] < 0.30: continue
        gap = b['t0'] - t
        if gap > 1.0:  fixed.append(dict(kind='talk', t0=round(t,3), t1=round(b['t0'],3)))
        elif gap > 0:  b['t0'] = t          # a sub-second talk island reads as a glitch, not a cut
        fixed.append(b); t = b['t1']
    if DUR - t > 0.10: fixed.append(dict(kind='talk', t0=round(t,3), t1=DUR))
    return fixed, [b for b in BEATS if b['kind'] in OVERLAY_KINDS]

if __name__ == '__main__':
    tl, ov = timeline()
    print(f'{"kind":10s} {"t0":>8s} {"t1":>8s} {"len":>6s}  detail')
    for b in tl:
        det = b.get('media') or b.get('header') or b.get('headline') or ''
        print(f'{b["kind"]:10s} {b["t0"]:8.2f} {b["t1"]:8.2f} {b["t1"]-b["t0"]:6.2f}  {det}')
    print('\noverlays:')
    for b in ov: print(f'  {b["kind"]:8s} {b["t0"]:7.2f}-{b["t1"]:7.2f}  {b.get("big","")}')
    tot = sum(b['t1']-b['t0'] for b in tl)
    ins = sum(b['t1']-b['t0'] for b in tl if b['kind'] != 'talk')
    assert abs(tot-DUR) < 0.02, f'timeline {tot} != {DUR}'
    print(f'\nsegments {len(tl)}  covers {tot:.3f}s (= {DUR})')
    print(f'insert/graphic coverage {ins:.1f}s = {100*ins/DUR:.0f}%   (his cut: 59%)')
    short=[b for b in tl if b["t1"]-b["t0"]<1.0]
    print(f'segments under 1.0s: {len(short)}', [f'{b["kind"]}@{b["t0"]}' for b in short])
