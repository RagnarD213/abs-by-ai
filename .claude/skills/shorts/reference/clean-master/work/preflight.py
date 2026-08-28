#!/usr/bin/env python3
"""PREFLIGHT: do the source's two timelines agree?

Run this before anything else. A master assembled by concatenating AAC segments can hold
more samples than its container declares, and the excess is spread through the file - so the
decoded-sample timeline (where Whisper word timestamps and the silence map live) drifts away
from the container timeline (where `-ss`, and therefore every cut and the whole picture,
live). On this source that drift reached 669 ms and shipped captions up to 650 ms late.

Cheap detector: decoded sample count vs declared duration.
"""
import os, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
SRC = subprocess.check_output(['node', '-e', "console.log(require('./config.js').SRC)"]).decode().strip()
WAV = 'work/audio48k.wav'
dur = float(subprocess.check_output([FP, '-v', 'error', '-show_entries', 'format=duration',
                                     '-of', 'csv=p=0', SRC]).decode())
n = (os.path.getsize(WAV) - 44) // 2
wav = n / 48000.0
delta = wav - dur
print(f"container duration {dur:.3f}s   analysis wav {wav:.3f}s   delta {delta*1000:+.0f} ms")
if abs(delta) > 0.050:
    print("\n  ✗ TIMELINE MISMATCH. The analysis wav is not on the container timeline, so every")
    print("    word timestamp and every measured silence is offset from where `-ss` will cut.")
    print("    Re-extract with:")
    print('      ffmpeg -i SRC -vn -af "aresample=async=1:first_pts=0" -ac 1 -ar 48000 \\')
    print('        -c:a pcm_s16le work/audio48k.wav')
    sys.exit(1)
print("  ✓ timelines agree - word timestamps and `-ss` cuts refer to the same audio")
