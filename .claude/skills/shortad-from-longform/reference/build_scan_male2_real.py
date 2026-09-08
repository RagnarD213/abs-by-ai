#!/usr/bin/env python3
"""The 3:18 split's phone media from a REAL generation (record_gen_male2.py): the app's own loader with
the other person's photo (screencast frames, retimed: the first 1.3 s at real speed, then fast to 100 %),
then the app's own result screen rendered after-only (before column and body-fat row hidden in the live
DOM), with a slow push. 115 + 90 frames, like the first split. Usage: build_scan_male2_real.py <run dir> [result dir]"""
import json, os, subprocess, sys, shutil
import numpy as np
from PIL import Image
RUN = sys.argv[1] if len(sys.argv) > 1 else 'rev/gen2'
RES = sys.argv[2] if len(sys.argv) > 2 else RUN
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001; nA, nC = 115, 90
L = json.load(open(f'{RUN}/log.json')); cast = L['cast']; T0 = L['T0']
ts = np.array([c['t'] - T0 for c in cast]); t_click = L['t_click']; t_end = L['t_loader_end']
# frames from the click to the end of the loader; the loader's photo appears ~0.3 s after the click
sel = np.where((ts >= t_click + 0.25) & (ts <= t_end - 0.3))[0]
tt = ts[sel] - ts[sel][0]; T = tt[-1]
real = 1.3                                   # seconds of real-time scanning at the start
out_t = np.arange(nA) / FPS                  # 0..3.83 s
src_t = np.where(out_t <= real, out_t, real + (out_t - real) * (T - real) / max(1e-6, out_t[-1] - real))
pick = [sel[int(np.argmin(np.abs(tt - t)))] for t in src_t]
im0 = Image.open(f'{RUN}/cast/{pick[0]:05d}.png'); W0, H0 = im0.size
W, H = 780, 1328                      # cast frames x2 (lanczos), the dpr-3 result down: the hole is ~515 px wide
os.makedirs('rev/m2r', exist_ok=True); subprocess.run('rm -f rev/m2r/*.png', shell=True)
for k, i in enumerate(pick):
    Image.open(f'{RUN}/cast/{i:05d}.png').convert('RGB').resize((W, H), Image.LANCZOS).save(f'rev/m2r/{k:04d}.png')
after = [s for s in json.load(open(f'{RES}/log.json'))['shots'] if s['tag'] == 'result_after_only'][-1]['path']
res = Image.open(after).convert('RGB').resize((W, H), Image.LANCZOS); res.save('rev/m2r/result.png')
fc = (f"[0:v]setpts=PTS-STARTPTS[a];"
      f"[1:v]scale={int(W*1.14)}:{int(H*1.14)}:flags=lanczos,zoompan=z='1+0.05*on/{nC-1}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps=30000/1001,trim=end_frame={nC},setpts=PTS-STARTPTS[c];"
      f"[a][c]concat=n=2:v=1:a=0,format=yuv420p[v]")
r = subprocess.run([FF,'-v','error','-y','-framerate','30000/1001','-i','rev/m2r/%04d.png','-loop','1','-framerate','30000/1001','-t','4','-i','rev/m2r/result.png',
                    '-filter_complex',fc,'-map','[v]','-r','30000/1001','-frames:v',str(nA+nC),'-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','rev/scan_result_male2.mp4'],
                   capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[-1500:])
n = subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-count_frames','-show_entries','stream=nb_read_frames,width,height','-of','csv=p=0','rev/scan_result_male2.mp4'],capture_output=True,text=True).stdout.strip()
print(f'rev/scan_result_male2.mp4 {n} (loader {T:.1f} s of real time -> {nA} frames, result from frame {nA}); source {W0}x{H0}')
