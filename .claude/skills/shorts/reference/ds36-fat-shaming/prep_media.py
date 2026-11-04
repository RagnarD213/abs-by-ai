"""DS-36 R1 media caches (decoded once, BT.709 TV range -> RGB, rgb24 memmaps), shared by both versions:
  src/clip_355-381_30fps.npy  the Bill Maher clip (Real Time, "New Rule: The Fudge Report", Dm4TAdiEFn0, 720p upscaled to 1920x1080)
                              355.0-381.0 s at its own 29.97 fps: the opening, the spoken panel, and the silent panel behind
                              Dan's reply (the clip simply continues; one camera, no repeat)
  src/A0197_30fps.npy         library A0197 (AI, man on an analog scale, needle swings; approved in SL-07), 24 -> 29.97 fps, 1080x1920
  src/B0419_30fps.npy         library B0419 (Dan's front-on stomach vacuum by the pool, approved grade from DS-04): its top 380 rows
                              are a reserved dark title band, so the picture (rows 380-1920) is scaled x1.247 and centre-cropped
                              to fill 1080x1920
  src/B0019_30fps.npy         library B0019 (Pexels stock, gloved hands packing prepared meals; approved in SL-07), 25 -> 29.97 fps,
                              vertical window x 740-1347 on the containers, 1080x1920"""
import subprocess, numpy as np, sys
from pathlib import Path
W = Path(__file__).resolve().parents[1]; F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
LIB = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library'
CLIP = str(W/'src/maher_full.mkv')
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
dump(W/'src/clip_355-381_30fps.npy', CLIP, DEC + ':w=1920:h=1080:flags=lanczos', (1920, 1080), ss=355.0, t=26.0)
dump(W/'src/A0197_30fps.npy', LIB + '/04 AI-Generated Clips/concepts-and-gags/A0197_man-on-analog-scale-needle-swings-metronome_9x16_6s.mp4',
     'fps=30000/1001,' + DEC, (1080, 1920))
dump(W/'src/B0419_30fps.npy', LIB + '/03 B-Roll - Real Footage/dan-filmed/B0419_dan-stomach-vacuum-front-poolside_9x16_4s.mp4',
     'crop=1080:1540:0:380,' + DEC + ',scale=1347:1920:flags=lanczos,crop=1080:1920:133:0', (1080, 1920))
dump(W/'src/B0019_30fps.npy', LIB + '/03 B-Roll - Real Footage/stock/food-nutrition/B0019_gloved-hands-packing-prepared-meal-containers_16x9_17s.mp4',
     'fps=30000/1001,crop=607:1080:740:0,' + DEC + ',scale=1080:1920:flags=lanczos', (1080, 1920), t=8.0)
