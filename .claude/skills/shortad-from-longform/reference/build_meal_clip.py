#!/usr/bin/env python3
"""The 3:59 card (app_item, 162 frames): the REAL Macro Tracker on absbyai.com with the new salmon plate,
assembled from the Playwright screenshots (record_meal.py): photo -> Analyze -> the itemized calories
with the 815-cal total -> Log Meal -> logged. Ends on the point of the feature, not on a spinner."""
import json, subprocess, os
import numpy as np
from PIL import Image
FPS = 30000/1001
log = {}
for l in json.load(open('rev/meal/shots.json')): log.setdefault(l['tag'], l['path'])      # FIRST shot of each state
W, H = 780, 1328
def load(tag_or_path): return Image.open(log.get(tag_or_path, tag_or_path)).convert('RGB').resize((W, H), Image.LANCZOS)
photo, analyzing, res_top, res_list, logged = (load('rev/meal/shots/002c_photo_loaded_scrolled2.png'), load('analyzing'),
                                               load('result_top'), load('result_scroll3'), load('logged_c'))
# analyzing: the app's own spinner is CSS-animated and static in a screenshot -> rotate its arc by hand is fabrication,
# so the state simply holds (1.3 s), which is what a phone recording of a 17 s analysis compressed 13x shows anyway.
seq = [(photo, 27), (analyzing, 39), (res_top, 22), (res_list, 44), (logged, 40)]      # 172 frames >= 162 + headroom
X = 4                                                                                 # crossfade frames
frames = []
for k, (im, n) in enumerate(seq):
    a = np.asarray(im, dtype=np.float32)
    for i in range(n):
        if k > 0 and i < X:
            p = (i+1)/(X+1); prev = np.asarray(seq[k-1][0], dtype=np.float32)
            frames.append(((1-p)*prev + p*a).astype(np.uint8))
        else:
            frames.append(a.astype(np.uint8))
os.makedirs('rev/meal/frames', exist_ok=True); subprocess.run('rm -f rev/meal/frames/*.png', shell=True)
for i, f in enumerate(frames): Image.fromarray(f).save(f'rev/meal/frames/{i:04d}.png')
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
subprocess.run([FF,'-v','error','-y','-framerate','30000/1001','-i','rev/meal/frames/%04d.png','-r','30000/1001','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','rev/meal_new.mp4'], check=True)
n = subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-count_frames','-show_entries','stream=nb_read_frames','-of','csv=p=0','rev/meal_new.mp4'],capture_output=True,text=True).stdout.strip()
print('rev/meal_new.mp4 frames', n, 'size', W, 'x', H)
