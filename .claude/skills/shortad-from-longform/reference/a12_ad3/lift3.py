#!/usr/bin/env python3
"""Lift his 16:9 stock clips from HIS 1080p render at his exact frames, BY INDEX (one decode, streamed -- skill A7.12:
a -ss seek lands on the wrong frame on his masters). Frame n of each lift = his frame n. Each range is checked by eye
for his burned text before use (A7.8); the SixPackAbs lift stops at 874, where his own flash starts (a lift must not
carry his flash under ours).
⚠ DECODE HIS FILE AS BT.709 (2026-09-13). It carries no colour tags; the default decode of an untagged file is BT.601, so
these lifts were 601-decoded and then written as BT.709 -- every one of them shifted colour against his own ad in VLC,
the same fault Dan rejected on the talking head."""
import subprocess, numpy as np, os
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
LIFTS = dict(spa=(639, 874), row=(1544, 1665), kitchen=(1819, 1944), pushups=(3701, 3797), landmine=(7329, 7399),
             phoneguy=(7399, 7454))
os.makedirs('lifts', exist_ok=True)
lo, hi = min(a for a, b in LIFTS.values()), max(b for a, b in LIFTS.values())
p = subprocess.Popen([FF, '-v', 'error', '-i', 'ref/ad3_v6hd.mp4', '-vf', f"select='between(n\\,{lo}\\,{hi-1})',scale=in_color_matrix=bt709:in_range=tv",
                      '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
enc = {}
def encoder(k):
    return subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080',
                             '-r', '30000/1001', '-i', '-', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
                             '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-colorspace', 'bt709', '-color_primaries',
                             'bt709', '-color_trc', 'bt709', '-color_range', 'tv', f'lifts/{k}.mp4'], stdin=subprocess.PIPE)
cnt = {k: 0 for k in LIFTS}
for n in range(lo, hi):
    buf = p.stdout.read(1920*1080*3)
    if len(buf) < 1920*1080*3: raise SystemExit(f'short read at {n}')
    for k, (a, b) in LIFTS.items():
        if a <= n < b:
            if k not in enc: enc[k] = encoder(k)
            enc[k].stdin.write(buf); cnt[k] += 1
            if n == b - 1: enc[k].stdin.close(); enc[k].wait()
p.wait()
for k, (a, b) in LIFTS.items():
    assert cnt[k] == b - a, (k, cnt[k], b - a)
    print(f'{k:9s} {a}-{b}  {b-a} frames')
