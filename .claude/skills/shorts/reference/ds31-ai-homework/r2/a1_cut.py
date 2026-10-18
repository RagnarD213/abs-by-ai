"""DS-31 R2: cut the gated A1 Flow take into stock/A1.mp4 for the opener slot (0:00-0:02.80, 84 film frames).
  python3 recipe/a1_cut.py TAKE.mp4 SRC_START SRC_END
The window [SRC_START, SRC_END] of the 24 fps take is retimed to fill the slot exactly (a slight speed-up is the approved
way to tighten an AI clip; never slowed). Writes stock/A1.mp4 (29.97 fps, 1080x1920) and a1-cut.json with the range
in take frames for clipcheck --frames.
"""
from pathlib import Path
import subprocess, sys, json, os
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; SLOT = 84
take, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
speed = (b - a)/(SLOT/FPS); assert 1.0 <= speed <= 1.25, ('speed must be 1.00-1.25x', speed)
out = W/'stock/A1.mp4'
subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a:.4f}', '-i', take, '-t', f'{b - a:.4f}', '-an',
                '-vf', f'setpts=(PTS-STARTPTS)/{speed:.5f},fps=30000/1001,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p',
                '-frames:v', str(SLOT), '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-colorspace', 'bt709', '-color_primaries', 'bt709',
                '-color_trc', 'bt709', '-color_range', 'tv', str(out)], check=True)
(W/'a1-cut.json').write_text(json.dumps(dict(take=str(take), src_start=a, src_end=b, speed=round(speed, 4),
                                            take_frames=[int(round(a*24)), int(round(b*24)) - 1], slot_frames=SLOT), indent=1))
print('A1 CUT', take, a, b, f'{speed:.3f}x')
