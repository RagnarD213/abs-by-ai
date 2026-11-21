#!/usr/bin/env python3
"""picture.mp4 + captions.mov + audio_final.wav -> the master. Asserts the frame count."""
import subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
OUT = sys.argv[1] if len(sys.argv) > 1 else 'ad2v2_vertical_9x16.mp4'
import beats
PLAN = round(beats.DUR*30000/1001)
r = subprocess.run([FF,'-nostdin','-v','error','-y','-i','picture.mp4','-i','captions.mov','-i','audio_final.wav',
    '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:format=auto[v]',
    '-map','[v]','-map','2:a','-r','30000/1001','-frames:v',str(PLAN),
    '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-video_track_timescale','30000',
    '-c:a','aac','-b:a','256k','-ar','48000','-ac','2','-movflags','+faststart', OUT],
    capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[-2000:])
p = subprocess.run([FP,'-v','error','-select_streams','v','-count_frames','-show_entries',
    'stream=nb_read_frames','-of','csv=p=0',OUT], capture_output=True, text=True).stdout.strip()
a = subprocess.run([FP,'-v','error','-select_streams','a','-show_entries','stream=duration','-of','csv=p=0',OUT],
    capture_output=True, text=True).stdout.strip()
print(f'{OUT}: video {p}  audio {a}  (planned {PLAN} frames)')
n = int(p.split(',')[0])
if n != PLAN: raise SystemExit(f'FRAME COUNT {n} != PLAN {PLAN}')
