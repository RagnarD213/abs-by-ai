#!/usr/bin/env python3
"""AV-07 Ad 10 media map for the locked 9:16 kit.

The camera base is conformed from C1601.MP4. These entries are only the approved
master's insert content or clean project-owned stills that replace its unsafe
burned-in labels. Any 16:9 motion source is put in the kit's olive card.
"""

MASTER = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/"
          "my dad bod at 38 my dad bod at 40 - ad 10/"
          "my dad bod at 38 my dad bod at 40 | muhammad | 16x9 | ad 10.mp4")
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
PHOTOS = f"{LIB}/06 Dan Photo Shoot Stills"
BA = f"{LIB}/01 Before and After Images"

MEDIA = {
    # Clean stills: the 16:9 master's italic labels crossed Dan's torso/abs.
    "before_deckchair": ("img", f"{BA}/00_ORIGINAL_deckchair_upscaled3x.jpg", 0, 1.0,
                         {"oy": 0.0}),
    "real_red_shorts": ("img", f"{PHOTOS}/photo-137_FINAL_PRIMARY.jpg", 0, 1.0,
                        {"oy": 0.0}),
    "real_towel": ("img", f"{PHOTOS}/dan-pool-shoot-towel-smile-retouched-final.jpg", 0, 1.0,
                   {"oy": 0.0}),
    "real_park_close": ("img", f"{PHOTOS}/photo-180_FINAL_PRIMARY.png", 0, 1.0,
                        {"oy": 0.0}),
    "real_flag": ("img", f"{PHOTOS}/Dan-flag-FINAL.jpg", 0, 1.0,
                  {"oy": 0.0}),
    "real_pool_stand": ("img", f"{PHOTOS}/photo-10_FINAL_PRIMARY.jpg", 0, 1.0,
                        {"oy": 0.0}),
    "real_pool_flex": ("img", f"{PHOTOS}/photo-125_FINAL_PRIMARY.jpg", 0, 1.0,
                       {"oy": 0.0}),
    "ai_goal": ("img", f"{BA}/dan by pool - AI GOAL IMAGE.png", 0, 1.0,
                {"oy": 0.0}),

    # Exact approved-master lifts. They are displayed in a card, never enlarged
    # from 16:9 to full-bleed 9:16.
    "family_kitchen": ("vid", MASTER, 54.221),
    "daughter_trip": ("vid", MASTER, 63.130),
    "daughter_event": ("vid", MASTER, 65.098),
    "ai_beach": ("vid", MASTER, 112.012),
    # Ends on a held copy of the final clean food frame. The next master shot
    # begins with an eyes-down talking-head moment and must not leak into card.
    "food_snap": ("vid", "assets_ad10/food_snap_hold.mp4", 0.0),
    "wife_notices": ("vid", MASTER, 165.032),
    "gym_respect": ("vid", MASTER, 167.300),
    "ai_beach_end": ("vid", MASTER, 169.469),

    # Portrait crops cut from the approved master in prepare_assets.sh. Splitting
    # them lets the real/AI label stay mutually exclusive as the app flow changes.
    "phone_goal": ("img", "assets_ad10/phone_goal_labeled.png", 0.0, 1.0,
                   {"oy": 0.0}),
    "app1_before": ("vid", "assets_ad10/app1_before.mp4", 0.0),
    "app1_form": ("vid", "assets_ad10/app1_form.mp4", 0.0),
    # The approved-master app reveal carries its own internal AI chip. Reusing it
    # under the kit's measured chip produced two contradictory disclosures during
    # the slide. Use the exact clean Dan goal image for the result beat instead.
    "app1_goal_clean": ("img", f"{BA}/dan by pool - AI GOAL IMAGE.png", 0, 1.0,
                        {"oy": 0.0}),
    "app2_before": ("vid", "assets_ad10/app2_before.mp4", 0.0),
    "app2_form": ("vid", "assets_ad10/app2_form.mp4", 0.0),
    "app2_goal_clean": ("img", f"{BA}/dan by pool - AI GOAL IMAGE.png", 0, 1.0,
                        {"oy": 0.0}),
}
