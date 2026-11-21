#!/usr/bin/env python3
"""Resolved media for every beat key, matched one-for-one to what Muhammad shows.

TREATMENT RULE: 16:9 SOURCE IS NEVER CROPPED TO FULL-BLEED 9:16 -- that is a 2.7x upscale
and it looks it. 16:9 material goes in the olive CARD, which is his own design language
and a DOWNSCALE. Only natively-vertical or >=1440-tall sources go full bleed.

⚠ The product recording's usable window is 0-25.0 s ONLY: at 26 s it reaches the in-app
"Meet the new you" BEFORE/AFTER split and at 29 s the email-capture form. Both are banned
on screen in a paid ad. HIS cut runs the recording past both of them; ours does not, and
qc.py asserts it.
"""
REV5 = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/assets"
GAG  = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/"
        "batch1-ads/full/gag_crude_photoshop_dan.png")
ABW  = "/Volumes/Extreme/Abs By AI Photo Shoots/The Ultimate 1 Minute Ab Workout - DESCRIPT RAW CUTDOWN.mp4"
APP  = f"{REV5}/clip_109_replacement.mp4"
APP_SAFE_END = 25.0

MEDIA = {
  # --- stills in the olive card ------------------------------------------------
  'before_200lb' : ('img', f'{REV5}/dan_before_200lb.jpg'),      # his 0:03 + 2:06
  'dad_kids'     : ('img', f'{REV5}/fatdad_standing.jpg'),       # his 2:13
  'bodybuilder'  : ('img', 'stock3/p_5327549.jpg'),              # his 0:48 fitness model
  # p_goal / p_phone_mock already carry a burned AI-GENERATED chip above the picture,
  # so the plate must NOT add a second one.
  'p_goal'       : ('img', 'assets_v/p_goal.png'),               # his 2:40
  'phone_mock'   : ('img', 'assets_v/p_phone_mock.png'),         # his 0:05 + 2:18
  # --- stills full bleed (portrait or >=1440 tall) -----------------------------
  'today_towel'  : ('img', f'{REV5}/shoot07_standing.jpg'),      # his 0:12 montage, 1 of 3
  'today_trees'  : ('img', f'{REV5}/shoot04_trees.jpg'),         # 2 of 3
  'today_flag'   : ('img', f'{REV5}/shoot05_flag.jpg'),          # 3 of 3
  'photoshop_gag': ('img', GAG),                                 # his 1:01
  # --- the product recording, pre-retimed inside the safe window ---------------
  'app_flow_a'   : ('vid', 'assets_v/app_flow_a.mp4', 0.0),      # his 1:08 phone + Dan
  'app_flow_b'   : ('vid', 'assets_v/app_flow_b.mp4', 0.0),      # his 3:07 full-frame phone
  # --- our AI clips (1280x720 -> label them, and they still go full bleed at his
  #     beat lengths because his are full frame; see notes.md) -------------------
  'ai_women_pool': ('vid', f'{REV5}/ai_women_pool.mp4', 0.20),   # his 1:41 resort
  'ai_respect_gym':('vid', f'{REV5}/ai_respect_gym.mp4', 0.20),  # his 1:46 handshake
  'ai_beachrun'  : ('vid', f'{REV5}/ai_health_beachrun.mp4', 0.10),  # his 1:48 beach run
  'ai_busydad'   : ('vid', f'{REV5}/ai_busydad_kitchen.mp4', 0.20),  # his 2:14 stressed dad
  # --- our own footage ---------------------------------------------------------
  'outdoor_abs'  : ('vid', ABW, 392.0),                          # his 2:29 med-ball situps
  # --- stock, all natively vertical or >=1440 tall ------------------------------
  'bl_home_abs'  : ('vid', 'stock2/abs_floor_4921658.mp4', 1.0),      # his 1:21 floor abs
  'bl_older_man' : ('vid', 'stock/elderly_beach_8636810.mp4', 1.5),   # his 1:54 older man
  'bl_salad'     : ('vid', 'stock/salad_fork_6327114.mp4', 1.0),      # his 1:56
  'bl_alone_gym' : ('vid', 'stock3/v_35585564.mp4', 0.8),             # his 2:16 alone in gym
  'bl_mealprep'  : ('vid', 'stock/mealprep_6894121.mp4', 0.5),        # his 2:32
  'bl_track'     : ('vid', 'stock3/v_8103667.mp4', 3.0),              # his 2:34 tracking
  'bl_crunch_gym': ('vid', 'stock2/crunches_gym_36484275.mp4', 1.5),  # his 2:35
  'bl_abwheel'   : ('vid', 'stock/abroller_32067977.mp4', 1.0),       # his 3:28 ab wheel
  'bl_eating'    : ('vid', 'stock/eating_man_8164074.mp4', 2.0),      # his 3:36
}

if __name__ == '__main__':
    import os, subprocess
    FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
    os.makedirs('assets_v', exist_ok=True)
    # Retime the product recording to the two beat lengths, both ending well inside the
    # 25.0 s safe window.
    for name, (ss, src_end, want) in {
        # +0.5 s of headroom on each: cut to the exact beat length they came out ONE
        # FRAME short, and -stream_loop wrapped that last frame back to the app's first
        # screen -- a visible content jump on the final frame of the beat.
        'app_flow_a': (0.50, 12.30, 7.85),
        'app_flow_b': (1.00, 24.60, 12.95),
    }.items():
        assert src_end <= APP_SAFE_END, name
        out = f'assets_v/{name}.mp4'
        if os.path.exists(out): continue
        pts = want / (src_end - ss)
        subprocess.run([FF,'-v','error','-y','-ss',f'{ss:.3f}','-t',f'{src_end-ss:.3f}','-i',APP,
                        '-vf',f'setpts={pts:.6f}*PTS,fps=30000/1001','-an',
                        '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',out],
                       check=True)
        print(name, f'src {ss:.2f}-{src_end:.2f}s -> {want:.2f}s ({1/pts:.2f}x)')
    for k, v in MEDIA.items():
        p = v[1]
        if not os.path.exists(p): print('MISSING', k, p)
    print('assets ok')
