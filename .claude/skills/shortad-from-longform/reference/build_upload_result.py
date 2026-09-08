#!/usr/bin/env python3
"""The 3:03 card (app_upload, 240 frames): the whole flow from the uploaded photo to the FINALISED after
picture inside the same card (Dan, 2026-09-08). Retimed variably: the interaction near real time, the
progress screens fast, then the compliant after-only result holds with a slow push.
  frames   0- 99   recording  0.0 -> 9.5 s   2.85x   (adjust photo, options, tap Generate)
  frames 100-159   recording  9.5 -> 24.5 s  7.5x    (progress 32% -> 91%)
  frames 160-269   the after-only result, slow push (lands at 3:08.5, holds 2.7 s to the card's end)"""
import subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
APP = ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
       "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4")
PNG = "gfx_src/meetnew_after_only.png"
W, H = 660, 1434
nA, nB, nC = 100, 60, 110
fc = (f"[0:v]trim=0.0:9.5,setpts=(PTS-STARTPTS)/{9.5/(nA/29.97003):.4f},fps=30000/1001,scale={W}:{H}:flags=lanczos,trim=end_frame={nA},setpts=PTS-STARTPTS[a];"
      f"[0:v]trim=9.5:24.5,setpts=(PTS-STARTPTS)/{15.0/(nB/29.97003):.4f},fps=30000/1001,scale={W}:{H}:flags=lanczos,trim=end_frame={nB},setpts=PTS-STARTPTS[b];"
      f"[1:v]scale={int(W*1.14)}:{int(H*1.14)}:flags=lanczos,zoompan=z='1+0.05*on/{nC-1}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps=30000/1001,trim=end_frame={nC},setpts=PTS-STARTPTS[c];"
      f"[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]")
r = subprocess.run([FF,'-v','error','-y','-i',APP,'-loop','1','-framerate','30000/1001','-t','5','-i',PNG,'-filter_complex',fc,'-map','[v]',
                    '-r','30000/1001','-frames:v',str(nA+nB+nC),'-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','rev/upload_result.mp4'],
                   capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[-1500:])
n = subprocess.run([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v','-count_frames','-show_entries','stream=nb_read_frames','-of','csv=p=0','rev/upload_result.mp4'],capture_output=True,text=True).stdout.strip()
print('rev/upload_result.mp4 frames', n, '(result from frame', nA+nB, ')')
