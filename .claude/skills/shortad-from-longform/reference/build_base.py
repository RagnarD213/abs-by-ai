#!/usr/bin/env python3
"""Conform C1591 to Muhammad's cut and apply his tone curve. Output stays 1920x1080 --
all vertical reframing happens downstream, so one base serves both the full-bleed and
the windowed layouts.

Frame counts are CUMULATIVE, not per-segment. Rounding each segment's duration on its
own put 16 ms of overshoot into every one of the 73 cuts and the conform finished 1.17 s
long -- enough to walk the captions off the words by the end of the ad."""
import json, os, subprocess
from grade import CURVES
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC="/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/C1591.MP4"
FPS=30000/1001
S=json.load(open('edl_final.json'))
os.makedirs('seg',exist_ok=True)
prev=0
plan=[]
for s in S:
    cum=round(s['cut_out']*FPS)
    plan.append((s, cum-prev)); prev=cum
json.dump([{**s,'frames':n} for s,n in plan], open('edl_frames.json','w'), indent=1)
with open('seg/list.txt','w') as lst:
    for s,n in plan:
        out=f'seg/b{s["i"]:03d}.mp4'
        if not os.path.exists(out) or os.path.getsize(out)<10000:
            subprocess.run([FF,'-v','error','-y','-ss',f'{s["src_in"]:.4f}','-i',SRC,
                '-an','-vf',CURVES,'-r','30000/1001','-frames:v',str(max(1,n)),
                '-c:v','libx264','-preset','medium','-crf','12','-pix_fmt','yuv420p',out],check=True)
            print('seg',s['i'],n,'frames',flush=True)
        lst.write(f'file b{s["i"]:03d}.mp4\n')
subprocess.run([FF,'-v','error','-y','-f','concat','-safe','0','-i','seg/list.txt','-c','copy','base.mp4'],check=True)
p=subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-count_frames','-select_streams','v',
   '-show_entries','stream=nb_read_frames','-show_entries','format=duration','-of','csv=p=0','base.mp4'],
   capture_output=True,text=True).stdout.split()
print('base.mp4:',p,' target frames',round(232.768*FPS),'target dur 232.768')
