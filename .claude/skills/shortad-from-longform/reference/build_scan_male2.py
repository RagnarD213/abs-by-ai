#!/usr/bin/env python3
"""The 3:19 split's phone media with a DIFFERENT PERSON (Dan, 2026-09-08: 'use this exact same clip
again, but with a different before-and-after picture'). Same clip, same timing, same compliant result --
the photo in the app's scanning box is male2-before (asset library) and the after-only result screen
carries male2-after. 115 frames of scanning (recording 12.0-24.5 s, static layout, retimed 3.3x) then
90 frames of the result with a slow push."""
import subprocess, os, numpy as np
from PIL import Image, ImageOps, ImageDraw
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
APP = ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
       "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4")
L = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/01 Before and After Images"
FPS = 30000/1001; nA, nC = 115, 90
BOX = (144, 450, 1176, 1600)          # the photo inside the scanning card, measured on the 1320x2868 frames
INSET = 26                            # keep the app's white corner brackets visible
os.makedirs('rev/m2', exist_ok=True); subprocess.run('rm -f rev/m2/*.png', shell=True)
subprocess.run([FF,'-v','error','-y','-i',APP,'-vf',f"trim=12.0:24.5,setpts=(PTS-STARTPTS)/{12.5/(nA/FPS):.4f},fps=30000/1001,trim=end_frame={nA},setpts=PTS-STARTPTS",
                '-frames:v',str(nA),'rev/m2/%04d.png'], check=True)
ph = ImageOps.exif_transpose(Image.open(f'{L}/male2-before.webp')).convert('RGB')
bw, bh = BOX[2]-BOX[0]-2*INSET, BOX[3]-BOX[1]-2*INSET
s = max(bw/ph.width, bh/ph.height); r = ph.resize((int(ph.width*s)+1, int(ph.height*s)+1), Image.LANCZOS)
x = (r.width-bw)//2; y = int((r.height-bh)*0.15); photo = r.crop((x, y, x+bw, y+bh))
frames = sorted(f for f in os.listdir('rev/m2') if f.endswith('.png') and not f.startswith('._'))
for i, f in enumerate(frames):
    im = Image.open(f'rev/m2/{f}').convert('RGB')
    im.paste(photo, (BOX[0]+INSET, BOX[1]+INSET))
    # the app's scanning band: a soft light band sweeping down the photo every ~1.6 s
    band = Image.new('RGBA', (bw, bh), (0,0,0,0)); d = ImageDraw.Draw(band)
    p = (i % 48)/48.0; yc = int(p*bh)
    for k in range(-40, 41):
        a = int(90*max(0, 1-abs(k)/40)); yy = yc+k
        if 0 <= yy < bh: d.line([(0, yy), (bw, yy)], fill=(255,255,255,a))
    im.paste(band, (BOX[0]+INSET, BOX[1]+INSET), band)
    im.save(f'rev/m2/{f}')
W, H = 660, 1434
fc = (f"[0:v]scale={W}:{H}:flags=lanczos,setpts=PTS-STARTPTS[a];"
      f"[1:v]scale={int(W*1.14)}:{int(H*1.14)}:flags=lanczos,zoompan=z='1+0.05*on/{nC-1}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps=30000/1001,trim=end_frame={nC},setpts=PTS-STARTPTS[c];"
      f"[a][c]concat=n=2:v=1:a=0,format=yuv420p[v]")
r_ = subprocess.run([FF,'-v','error','-y','-framerate','30000/1001','-i','rev/m2/%04d.png','-loop','1','-framerate','30000/1001','-t','4','-i','gfx_src/meetnew_after_only_male2.png',
                     '-filter_complex',fc,'-map','[v]','-r','30000/1001','-frames:v',str(nA+nC),'-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','rev/scan_result_male2.mp4'],
                    capture_output=True, text=True)
if r_.returncode: raise SystemExit(r_.stderr[-1500:])
n = subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-count_frames','-show_entries','stream=nb_read_frames','-of','csv=p=0','rev/scan_result_male2.mp4'],capture_output=True,text=True).stdout.strip()
print('rev/scan_result_male2.mp4 frames', n, '(result from frame', nA, ')')
