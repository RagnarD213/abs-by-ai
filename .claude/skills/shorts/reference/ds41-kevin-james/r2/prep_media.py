"""DS-41 R1 media caches (decoded once, BT.709 TV range -> RGB, rgb24 memmaps), shared by both versions:
  src/clip_40-78_30fps.npy    the Kevin James clip (JRE Clips "Kevin James on Cheat Days and Losing 60lbs After Fasting for 41 Days",
                              tX5ZQ8rfHzY, 1080p), 40.0-78.0 s at its own 29.97 fps: the opening (41.40-47.78), the spoken panel
                              (58.25-65.90) and the silent panel behind Dan's reply (65.90 on; one camera to 82.5 s)
  src/clip_face_x.json        Kevin's face centre x over piece 1 (median of skin-coloured pixels in the top 55 % of the frame)
  src/A0197_30fps.npy         library A0197 (AI, man on an analog scale, needle swings around one reading; approved in SL-07 and
                              used in Fat Shaming), 24 -> 29.97 fps, native 1080x1920
  src/A0202_30fps.npy         library A0202 (AI, heavy man at a table piled with hot dogs, fries, chips, donuts and soda, pouts and
                              shrugs; used in RO-20C), 24 -> 29.97 fps, vertical window x 560-1167 on the man and the food in
                              front of him, 1080x1920"""
import subprocess, numpy as np, sys
from pathlib import Path
W = Path(__file__).resolve().parents[1]; F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
LIB = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library'
CLIP = str(W/'src/kevin_full.mkv')
def dump(out, src, vf, wh, ss=None, t=None):
    if Path(out).exists() and '--force' not in sys.argv: print('have', out); return
    cmd = [F, '-nostdin', '-v', 'error']
    if ss is not None: cmd += ['-ss', str(ss)]
    cmd += ['-i', src]
    if t is not None: cmd += ['-t', str(t)]
    p = subprocess.Popen(cmd + ['-an', '-vf', vf + ',format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    fb = wh[0]*wh[1]*3; frames = []
    while True:
        b = p.stdout.read(fb)
        if len(b) < fb: break
        frames.append(np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], 3))
    p.wait(); a = np.stack(frames)
    mm = np.lib.format.open_memmap(out, 'w+', np.uint8, a.shape); mm[:] = a; mm.flush(); print(out, a.shape)
DEC = 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc'
dump(W/'src/clip_40-78_30fps.npy', CLIP, DEC + ':w=1920:h=1080:flags=lanczos', (1920, 1080), ss=40.0, t=38.0)
dump(W/'src/A0197_30fps.npy', LIB + '/04 AI-Generated Clips/concepts-and-gags/A0197_man-on-analog-scale-needle-swings-metronome_9x16_6s.mp4',
     'fps=30000/1001,' + DEC, (1080, 1920))
dump(W/'src/A0202_30fps.npy', LIB + '/04 AI-Generated Clips/concepts-and-gags/A0202_overweight-man-hotdogs-excuse-pout_16x9_5s.mp4',
     'fps=30000/1001,crop=607:1080:560:0,' + DEC + ',scale=1080:1920:flags=lanczos', (1080, 1920))
import json
c = np.load(W/'src/clip_40-78_30fps.npy', mmap_mode='r'); FPS = 30000/1001; xs = []
for k in range(int(1.4*FPS), int(7.8*FPS), 3):
    f = c[k][:594:4, ::4].astype(np.float32); r, g, b = f[..., 0], f[..., 1], f[..., 2]
    skin = (r > 95) & (g > 40) & (b > 20) & (r > g + 15) & (r > b + 15) & ((r - np.minimum(g, b)) > 25) & (r < 250) & (g > 0.45*r) & (g < 0.85*r) & (b < 0.75*r)
    cols = np.where(skin)[1]
    if len(cols) > 200: xs.append(float(np.median(cols))*4)
(W/'src/clip_face_x.json').write_text(json.dumps(dict(face_x=round(float(np.median(xs)), 1), n=len(xs), lo=round(float(np.percentile(xs, 5)), 1), hi=round(float(np.percentile(xs, 95)), 1))))
print(open(W/'src/clip_face_x.json').read())
# review 1: A0202 replaced by A0242 (9:16, 24 fps; cached to src/A0242_30fps.npy with the same decode, fps=30000/1001 + DEC, 1080x1920)
