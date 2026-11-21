#!/usr/bin/env python3
"""The phone media for V2's phone-beside-Dan split (198.16-204.17, 180 frames).

His phone: the options screen with the photo just after "Generate" is tapped, the progress
screens, then -- at 202.0 -- the app's EMAIL-CAPTURE screen. That screen is banned in our
ads, so ours shows the compliant after-only result (gfx_src/meetnew_after_only.png, the
"Meet the new you" screen rebuilt with the BEFORE column and the body-fat row removed).

Retimed VARIABLY (rule 13): the interaction near real time, the progress screens ~5x.
  frames   0- 29  recording  8.0 ->  9.5 s   1.5x   (the tap, the photo, "Generating...")
  frames  30-114  recording  9.5 -> 24.5 s   5.3x   (progress 32% -> 91%; 24.5 stays clear of
                                                     the before/after pair at ~25.5)
  frames 115-204  the after-only result, slow push  (result lands at frame 115 = 202.0, his time)
"""
import subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
APP = ("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/"
       "02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4")
PNG = "gfx_src/meetnew_after_only.png"
W, H = 660, 1434
nA, nB, nC = 30, 85, 90
fc = (f"[0:v]trim=8.0:9.5,setpts=(PTS-STARTPTS)/1.5,fps=30000/1001,scale={W}:{H}:flags=lanczos,"
      f"trim=end_frame={nA},setpts=PTS-STARTPTS[a];"
      f"[0:v]trim=9.5:24.5,setpts=(PTS-STARTPTS)/{15.0/(nB/29.97003):.4f},fps=30000/1001,scale={W}:{H}:flags=lanczos,"
      f"trim=end_frame={nB},setpts=PTS-STARTPTS[b];"
      f"[1:v]scale={int(W*1.14)}:{int(H*1.14)}:flags=lanczos,"
      f"zoompan=z='1+0.05*on/{nC-1}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps=30000/1001,"
      f"trim=end_frame={nC},setpts=PTS-STARTPTS[c];"
      f"[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]")
cmd = [FF, '-v', 'error', '-y', '-i', APP, '-loop', '1', '-framerate', '30000/1001', '-t', '4', '-i', PNG,
       '-filter_complex', fc, '-map', '[v]', '-r', '30000/1001', '-frames:v', str(nA+nB+nC),
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', 'rev/scan_result.mp4']
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode: raise SystemExit(r.stderr[-2000:])
p = subprocess.run([FF.replace('ffmpeg','ffprobe'), '-v', 'error', '-select_streams', 'v', '-count_frames',
                    '-show_entries', 'stream=width,height,nb_read_frames,duration', '-of', 'csv=p=0',
                    'rev/scan_result.mp4'], capture_output=True, text=True).stdout.strip()
print('rev/scan_result.mp4 ->', p, f'(planned {nA+nB+nC} frames; result screen from frame {nA+nB})')
