"""DS-44 R1 media caches (decoded once, BT.709, rgb24 memmaps):
  src/clip_30-52_24fps.npy   the Hormozi clip file 30.0-52.0 s at its own 24 fps, 1920x1080 (clip_view picks the frame shown at t)
  src/A0197_30fps.npy        library A0197 (9:16, 24 fps) converted to 29.97 fps, 1080x1920
  src/B0351_30fps.npy        library B0351 (3840x2160, 30 fps) -> 29.97 fps, the vertical window on the hands and pen
                             (x 900..2115 of 3840, full height: the hand holding the pen and the other hand's fingers, face out of frame;
                             a window wide enough for both hands would be a square card), from 4.0 s of the clip, 1080x1920"""
import subprocess, numpy as np, json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[1]; F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
LIB = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library'
def dump(out, src, vf, wh, ss=None, t=None):
    cmd = [F, '-nostdin', '-v', 'error']
    if ss is not None: cmd += ['-ss', str(ss)]
    cmd += ['-i', src]
    if t is not None: cmd += ['-t', str(t)]
    raw = subprocess.check_output(cmd + ['-an', '-vf', vf + ',format=rgb24', '-f', 'rawvideo', '-'])
    a = np.frombuffer(raw, np.uint8).reshape(-1, wh[1], wh[0], 3)
    mm = np.lib.format.open_memmap(out, 'w+', np.uint8, a.shape); mm[:] = a; mm.flush(); print(out, a.shape)
DEC = 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc'
if not {'--only-b0351','--card'} & set(__import__('sys').argv): dump(W/'src/clip_30-52_24fps.npy', str(W/'src/hormozi_140-220.mkv'), DEC, (1920, 1080), ss=30.0, t=22.0)
if not {'--only-b0351','--card'} & set(__import__('sys').argv): dump(W/'src/A0197_30fps.npy', LIB + '/04 AI-Generated Clips/concepts-and-gags/A0197_man-on-analog-scale-needle-swings-metronome_9x16_6s.mp4',
     'fps=30000/1001,' + DEC, (1080, 1920))
if '--card' not in __import__('sys').argv: dump(W/'src/B0351_30fps.npy', LIB + '/03 B-Roll - Real Footage/stock/other/B0351_hands-hold-insulin-pen-blue-backdrop_16x9_12s.mp4',
     'fps=30000/1001,crop=1215:2160:900:0,' + DEC + ',scale=1080:1920:flags=area', (1080, 1920), ss=4.0, t=7.5)
# R2: the interview frame behind Dan's head after the clip (Dan 2026-10-22): Hormozi's one continuous shot, clip file 58.62-73.70 s
# (camera cuts at 58.586 and 73.711; no webcam banner), at its own 24 fps, scaled to the card (1000 x 562, full 16:9 height).
if '--card' in __import__('sys').argv:
    dump(W/'src/card_58-74_24fps.npy', str(W/'src/hormozi_140-220.mkv'), DEC + ',scale=1000:562:flags=area', (1000, 562), ss=58.62, t=15.08)
