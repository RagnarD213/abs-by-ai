#!/usr/bin/env python3
"""Resolved media for every beat key.

TREATMENT RULE (the one that matters in a vertical rebuild):
  16:9 SOURCE IS NEVER CROPPED TO FULL-BLEED 9:16. Cropping 1280x720 to 9:16 is a 2.7x
  upscale and it looks it. 16:9 material goes in the olive CARD instead -- which is his
  own design language, and a downscale rather than an upscale. Only natively-vertical or
  >=1440p-tall sources go full-bleed.
"""
REV5 = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets"
A1   = "/Volumes/Extreme/_edit_work/ad1-8-14/assets_v1"
GAG  = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/batch1-ads/full/gag_crude_photoshop_dan.png"
ABW  = "/Volumes/Extreme/Abs By AI Photo Shoots/The Ultimate 1 Minute Ab Workout - DESCRIPT RAW CUTDOWN.mp4"
# Native-vertical screen recording of the real product generating a preview.
# USABLE WINDOW IS 0-25.0s ONLY: at 26s it hits the "Meet the new you" BEFORE/AFTER
# split (banned in paid ads) and at 29s the email-capture form (also banned).
APP  = f"{REV5}/clip_109_replacement.mp4"

MEDIA = {
  # stills -> olive card
  'before_200lb' : ('img', f'{REV5}/dan_before_200lb.jpg'),
  'dad_kids'     : ('img', f'{REV5}/fatdad_standing.jpg'),
  'flag'         : ('img', f'{REV5}/shoot05_flag.jpg'),
  'standing'     : ('img', f'{REV5}/shoot07_standing.jpg'),
  'photoshop_gag': ('img', GAG),
  'p_goal'       : ('img', f'{A1}/p_goal.jpg'),
  'phone_mock'   : ('img', f'{A1}/p_phone_mock.jpg'),
  'app_assess'   : ('img', f'{A1}/p_app_assess.jpg'),
  'app_workout'  : ('img', f'{A1}/p_app_workout.jpg'),
  'app_nutri'    : ('img', f'{A1}/p_app_nutri.jpg'),
  # product recording -- native vertical, FULL BLEED
  'app_crop'     : ('vid', APP, 0.30),
  'app_form'     : ('vid', APP, 3.40),
  'app_describe' : ('vid', APP, 8.60),
  'app_tuning'   : ('vid', APP, 13.60),
  'app_render'   : ('vid', APP, 19.40),
  # our AI clips -- 1280x720, so CARD, never bleed
  'ai_women_pool': ('vid', f'{REV5}/ai_women_pool.mp4', 0.20),
  'ai_respect_gym':('vid', f'{REV5}/ai_respect_gym.mp4', 0.20),
  'ai_busydad'   : ('vid', f'{REV5}/ai_busydad_kitchen.mp4', 0.20),
  'ai_beachrun'  : ('vid', f'{REV5}/ai_health_beachrun.mp4', 0.20),
  # our own footage -- 1080p 16:9, bleed is a 1.78x upscale, same as Dan's own talking head
  'outdoor_dan'  : ('vid', ABW, 20.0),
  'outdoor_abs'  : ('vid', ABW, 392.0),   # the V-sit itself; 387.5 landed on the rest between reps
  'outdoor_push' : ('vid', ABW, 299.0),
  # stock -- all natively vertical or >=1440 tall, FULL BLEED
  'bl_home_abs'  : ('vid', 'stock2/abs_floor_4921658.mp4', 1.0),
  'bl_crunch_gym': ('vid', 'stock2/crunches_gym_36484275.mp4', 1.5),
  'bl_dumbbell'  : ('vid', 'stock2/dumbbell_home_8836851.mp4', 10.0),  # head in frame from 10s
  # knee_raise_6455076 was cast wrong (off Dan's white/Asian men 30-50 rule) -- replaced
  'bl_kneeraise' : ('vid', 'stock2/young_home_8836739.mp4', 4.0),
  'bl_run'       : ('vid', 'stock2/sunrise_run_4065480.mp4', 1.0),
  'bl_eating'    : ('vid', 'stock/eating_man_8164074.mp4', 2.0),
  'bl_salad'     : ('vid', 'stock/salad_fork_6327114.mp4', 1.0),
  'bl_mealprep'  : ('vid', 'stock/mealprep_6894121.mp4', 0.5),
}
