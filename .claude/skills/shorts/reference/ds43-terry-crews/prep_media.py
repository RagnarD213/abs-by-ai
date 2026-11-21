"""DS-43 R1 media caches (decoded once, BT.709 TV range -> RGB, rgb24 memmaps), shared by both versions:
  src/clip_0-32_24fps.npy   the Terry Crews clip (Business Insider, dW_99QcCTzE) 0-32 s at its own 23.976 fps, 1920x1080
                            (the opening and the spoken panel read frames from it)
  src/clip_silent_24fps.npy  the same clip from frame 576 (24.02 s, "Now, the times I don't eat...") to 34 s, for the silent panel
                            behind Dan's reply: the clip's own 19.9-23.7 s re-says the cold-open hook ("My first meal is at 2 p.m."),
                            so the silent panel starts after it (R1 watch judge: never repeat the clip)
  src/A0210_30fps.npy        library A0210 (AI Dan, 2:3 1026x1533, 29.97 fps) filled to 1080x1920 (height fit, centred)
  src/A0086_30fps.npy        library A0086 (AI, 16:9, 24 fps) -> 29.97 fps, vertical window x 752-1359 on the man eating, 1080x1920
  src/B0317_30fps.npy        library B0317 (Pexels stock, restaurant table of steak, bread and wine, 3840x2160 25 fps) -> 29.97 fps,
                             vertical window x 1250-2465, 1080x1920 (replaces A0086: its library note bans it from verticals, cut-out
                             outline on every edge, frame-reviewer FAIL 2026-10-16; R1 independent review)
  src/NYSE.npy               one clean frame of the clip's photo of Terry shirtless (clip 4.70 s, before the title text starts at
                             4.80), vertical window x 657-1264 on Terry, 1080x1920 (the cutaway pushes in on it slowly)"""
import subprocess, numpy as np, sys
from pathlib import Path
W = Path(__file__).resolve().parents[1]; F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
LIB = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library'
CLIP = str(W/'src/terry_full.mkv')
def dump(out, src, vf, wh, ss=None, t=None):
    if Path(out).exists() and '--force' not in sys.argv: print('have', out); return
    cmd = [F, '-nostdin', '-v', 'error']
    if ss is not None: cmd += ['-ss', str(ss)]
    cmd += ['-i', src]
    if t is not None: cmd += ['-t', str(t)]
    raw = subprocess.check_output(cmd + ['-an', '-vf', vf + ',format=rgb24', '-f', 'rawvideo', '-'])
    a = np.frombuffer(raw, np.uint8).reshape(-1, wh[1], wh[0], 3)
    mm = np.lib.format.open_memmap(out, 'w+', np.uint8, a.shape); mm[:] = a; mm.flush(); print(out, a.shape)
DEC = 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc'
dump(W/'src/clip_0-32_24fps.npy', CLIP, DEC, (1920, 1080), ss=0.0, t=32.0)
dump(W/'src/clip_silent_24fps.npy', CLIP, 'select=gte(n\\,576),setpts=N/FRAME_RATE/TB,' + DEC, (1920, 1080), t=34.0)
dump(W/'src/A0210_30fps.npy', LIB + '/04 AI-Generated Clips/ai-dan/A0210_dan-fasting-dawn-clock-to-afternoon-meal_2x3_6s.mp4',
     DEC + ',scale=1285:1920:flags=lanczos,crop=1080:1920:102:0', (1080, 1920))
dump(W/'src/A0086_30fps.npy', LIB + '/04 AI-Generated Clips/food-nutrition/A0086_man-eating-steak-rice-kitchen-counter_16x9_8s.mp4',
     'fps=30000/1001,crop=607:1080:752:0,' + DEC + ',scale=1080:1920:flags=lanczos', (1080, 1920))
dump(W/'src/B0317_30fps.npy', LIB + '/03 B-Roll - Real Footage/stock/food-nutrition/B0317_restaurant-table-steak-bread-wine_16x9_11s.mp4',
     'fps=30000/1001,crop=1215:2160:1250:0,' + DEC + ',scale=1080:1920:flags=lanczos', (1080, 1920))
dump(W/'src/NYSE.npy', CLIP, 'crop=607:1080:657:0,' + DEC + ',scale=1080:1920:flags=lanczos', (1080, 1920), ss=4.70, t=0.05)
