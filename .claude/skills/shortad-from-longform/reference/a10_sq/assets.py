#!/usr/bin/env python3
"""Every media asset the vertical Ad 2 uses.  ('img', path) or ('vid', path, src_in)."""
L    = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
REF  = f"{L}/00 ASSETS USED IN THE REFERENCE AD"
APP  = f"{L}/02 App Screen Recordings and Screenshots"
ARCH = f"{L}/08 SixPackAbs Archive - CHECK BEFORE USING"
STK  = "/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/stock"
PROJ = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
HERE = "/Volumes/Extreme/_edit_work/ad2-sq"

MEDIA = {
    # --- Dan's revisions -------------------------------------------------------
    'museum':    ('vid', f'{HERE}/rev/obsolete.mp4', 2.00),   # REV 1, his stated 0:02-0:06
    # SQUARE: a 1080 px window of the 1920 px clip has 840 px of freedom against the vertical's
    # 1312, but it is 472 px WIDER -- so it holds the MEAL PLANS sign AND "ONE SIZE FITS ALL",
    # which the vertical's 608 px window at 0.78 cut off (sqtest/_sheet_conveyor.png: 0.72 keeps
    # both whole, 0.78 and above slice "ONE SIZE" mid-word). This is the one place the square
    # shows MORE of his frame than the approved vertical does.
    'conveyor':  ('vid', f'{HERE}/rev/clipD.mp4',    0.00, 1.0, dict(ox=0.72)),
    'fatdad_a':  ('img', f'{PROJ}/before-photo-candidates/fat dad pic - standing_RECENTERED-4x5.jpg', 0, 1.0, dict(ox=0.37)),  # room for the girl at the left edge
    'fatdad_b':  ('img', f'{HERE}/rev/fatdad_ride.jpg', 0, 1.0, dict(ox=0.15)),   # REV 4; Dan centred, stomach in (2026-09-08)
    # REV 5. The beat is 4.905 s and the clip 4.50 s, so it is stretched 1.15x (a touch of slow motion
    # on a toe-touch, invisible) rather than looped -- a loop wraps to frame 0 mid-rep.
    # ... and then motion-interpolated (minterpolate mci) to 29.97 so the stretch repeats no frames:
    # the frame-repeated version duplicated 39 of 145 frames, judder on the one clip that is all movement.
    'workout':   ('vid', f'{HERE}/rev/workout_smooth.mp4', 0.00),
    # V2's phone-beside-Dan split: the app scanning (retimed) then the COMPLIANT after-only result,
    # pre-composited by build_scan_result.py. His V2 shows the email-capture screen here; ours never does.
    'scan_result': ('vid', f'{HERE}/rev/scan_result_male2.mp4', 0.0),   # same split, a DIFFERENT person's before/after (Dan 2026-09-08)
    'scan':      ('vid', f'{APP}/app-flow-generate-future-self.mp4', 11.5),  # REV 6a, progress screens
    'meetnew':   ('img', f'{HERE}/gfx_src/meetnew_after_only.png'),          # REV 6b, built compliant

    # --- his own beats ---------------------------------------------------------
    'spa':       ('vid', f'{ARCH}/dan-sixpackabs-8s-dan-solo.mp4', 0.0),
    'groceries': ('vid', f'{STK}/salad_fork_6327114.mp4', 1.0),
    'mealprep':  ('vid', f'{STK}/mealprep_6894121.mp4', 0.3),
    'app_soup':  ('vid', f'{APP}/app-flow-macro-tracker-soup.mp4', 30.0),
    'app_item':  ('vid', f'{HERE}/rev/meal_new.mp4', 0.0),   # new meal clip: better meal -> calories broken down and logged (Dan 2026-09-08)
    'app_upload':('vid', f'{HERE}/rev/upload_result.mp4', 0.0),   # upload -> options -> progress -> the FINALISED after picture, in one card (Dan 2026-09-08)
    'app_gen':   ('img', f'{HERE}/gfx_src/meetnew_after_only.png', 0, 1.0, dict(amt=0.04)),   # holds on the result the previous card landed on
    'app_supp':  ('vid', f'{APP}/app-supplement-audit-scroll.mp4', 0.0),
    'app_brief': ('img', f'{APP}/11_app_daily_brief.png'),
    'before_dan':('img', f'{REF}/02_BEFORE-PICTURE_dan-200lb.png', 0, 1.0, dict(oy=0.9, amt=0.035)),   # stomach stays in frame (Dan 2026-09-08); gentle push, bottom-anchored
    'goal_dan':  ('img', f'{REF}/01_HOOK+ENDCARD_ai-goal-image_dan-by-pool.png'),
    'flag':      ('img', f'{REF}/05_SHOT2_photoshoot-flag.jpg'),
    'after_standing': ('img', f'{REF}/07_SHOT4_photoshoot-standing.jpg'),
    'after_smiling':  ('img', f'{REF}/04_SHOT1_photoshoot-smiling-trees.png'),
}
