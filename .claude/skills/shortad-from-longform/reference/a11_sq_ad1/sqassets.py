#!/usr/bin/env python3
"""How every beat's media is treated in the SQUARE frame, and which label it carries.

Decided by CONTACT-SHEETING the 1:1 crop of every asset (`_sq/media_1to1.jpg`,
`_sq/photo_treatments.jpg`), never from the aspect ratio alone -- what a 1:1 crop takes off
a standing photo of a person is their head or their shorts, and only looking shows which.

modes
  cover  full-bleed 1080x1080 cover crop. Only where the 1:1 crop keeps the subject whole,
         and only for natively-vertical or >=1440-tall sources (a 1280x720 clip cropped to
         1:1 is a 1.5x upscale -- it goes in his card instead, which is a downscale).
  fith   full HEIGHT on the field, the picture's own width, centred. A 2:3 portrait cannot
         be full-bleed in a square without cutting head or shorts, so this is the square's
         "vertical and full screen" (shared square rule 4).
  card   his olive card, hole at the MEDIA's own aspect (rule 3).
  sbs    side-by-side: his own phone-left / Dan-right split, which a 1:1 frame has the
         width to keep (rule 2).

labels  (AGENTS.md, Dan 2026-09-11 -- mutually exclusive, exactly one per picture of Dan's
         physique shown as a result)
  'real' "Real picture of me - not AI-generated"   on his real photo-shoot afters
  'ai'   "AI-GENERATED"                            on AI imagery
  None   nothing: BEFORE pictures are neither (his 09-11 rule is about the AFTER pictures),
         and an asset whose chip is already burned in does not get a second one.

`cover_chip` is a box in DELIVERED-frame coordinates that our chip must fully cover: the
hook's goal video carries a chip burned in for a 1080x1920 frame, which lands 411 px wide
at full height here -- 38 % of the frame against the ~68 % the skill asks for. Our chip is
drawn over it rather than beside it, so the label is one label.
"""

SQ = {
  # --- hook ---------------------------------------------------------------
  # AI video of the goal image. Burned chip measured at x 186..896, y 1253..1368 of
  # 1080x1920 -> x 341..740, y 705..770 at full height in the square.
  # top 690, not 698: the burned chip's own LIGHT 1-px outline sits at y=693 and showed as
  # a ghost above our box (audit F5). Measure the outline, not just the dark box.
  'ai_goal_plain' : dict(mode='fith', label='ai', cover_chip=(341, 690, 740, 780)),
  'before_200lb'  : dict(mode='card', label=None),          # BEFORE picture: unlabelled
  # --- "this is where I'm at today": his three REAL after pictures ---------
  'today_towel'   : dict(mode='cover', label='real', oy=0.14, anchor_top=True),
  'today_trees'   : dict(mode='cover', label='real', anchor_top=True),
  'today_flag'    : dict(mode='cover', label='real', anchor_top=True),
  # --- conditioning -------------------------------------------------------
  # His 0:48 model slot is Dan's own pool photo = a real after picture. Dan's 09-11 rule
  # takes it out of the card and gives it the frame (cf. the Ad 5 revisions table).
  'bodybuilder'   : dict(mode='fith', label='real'),
  # The crude-photoshop gag is filed under "04 AI-Generated Clips" and ran unlabelled in
  # the approved vertical -- the A6.19b defect. Labelled here.
  'photoshop_gag' : dict(mode='fith', label='ai', anchor_top=True),
  # --- product ------------------------------------------------------------
  'app_flow_a'    : dict(mode='sbs',  label=None),          # phone LEFT / Dan RIGHT, his own
  'app_flow_b'    : dict(mode='fith', label=None),          # his full-frame phone beat
  # the app's own "Download Your Future Self" screen -- the image in it is the generated
  # one, so it carries the AI chip (A6.13: the standing rule is ours, not the editor's)
  'after_reveal'  : dict(mode='card', label='ai'),
  'p_goal'        : dict(mode='card', label=None),          # chip already burned in, above the picture
  'phone_mock'    : dict(mode='card', label=None),          # chip already burned in
  # --- stakes: our AI clips, 1280x720 -> his card (a downscale) ------------
  'ai_women_pool' : dict(mode='card', label='ai'),
  'ai_respect_gym': dict(mode='card', label='ai'),
  'ai_beachrun'   : dict(mode='card', label='ai'),
  'ai_busydad'    : dict(mode='card', label='ai'),
  # --- personal story -----------------------------------------------------
  'dad_ride'      : dict(mode='card', label=None),          # BEFORE pictures
  'dad_standing'  : dict(mode='card', label=None),
  'outdoor_abs'   : dict(mode='card', label=None),          # 1920x1080 footage of Dan working out
  # --- stock b-roll, all natively vertical or >=1440 tall -----------------
  'bl_home_abs'   : dict(mode='cover', label=None),
  'bl_older_man'  : dict(mode='cover', label=None),
  'bl_salad'      : dict(mode='cover', label=None),
  'bl_alone_gym'  : dict(mode='cover', label=None),
  'bl_mealprep'   : dict(mode='cover', label=None),
  'bl_track'      : dict(mode='cover', label=None),
  'bl_crunch_gym' : dict(mode='cover', label=None),
  'bl_gym_workout': dict(mode='cover', label=None),
  'bl_eating'     : dict(mode='cover', label=None),
  # unused in the beat sheet but kept resolvable
  'ai_goal_scan'  : dict(mode='fith', label='ai'),
}

def treat(key):
    t = dict(mode='card', label=None, ox=0.5, oy=0.5, cover_chip=None, anchor_top=False)
    t.update(SQ.get(key, {}))
    return t

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '.')
    from assets import MEDIA
    import beats as BT
    used = {b['media'] for b in BT.BEATS if b.get('media')}
    miss = used - set(SQ)
    extra = set(SQ) - set(MEDIA)
    print('beat media', len(used), 'without a square treatment:', miss or 'none')
    print('SQ keys not in MEDIA:', extra or 'none')
    for b in sorted(BT.BEATS, key=lambda x: x['t0']):
        if not b.get('media'): continue
        t = treat(b['media'])
        print(f"{b['t0']:8.2f} {b['kind']:9s} {b['media']:16s} -> {t['mode']:5s} label={t['label']}")
    assert not miss
