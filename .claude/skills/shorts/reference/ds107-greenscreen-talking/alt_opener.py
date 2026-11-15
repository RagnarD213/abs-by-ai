"""DS-107 R2: the 21 % alternate of the opener only (Dan said 25 % then 21 %): film 0:00-6.0 rendered exactly as the R2 master but with B0
at 1.21x, captions and the approved mix, for one-click comparison on the page. Not a second full film.   python3 alt_opener.py"""
import os, sys, subprocess, json
from pathlib import Path
sys.argv = [sys.argv[0]]; sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, assemble as AS
for s in AS.shots:
    if s['id'] == 'B0': s['speed'] = 1.21
N = AS.fr(6.0); out = AS.O/'review'/'opener-21pct.mp4'; tmp = AS.O/'opener-21pct-noaudio.mp4'
p = subprocess.Popen([AS.F, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-framerate', '30000/1001', '-i', '-', '-an',
                      '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'fast', '-crf', '15', str(tmp)], stdin=subprocess.PIPE)
for g in range(N): p.stdin.write(np.ascontiguousarray(AS.gfx(AS.u8(AS.render(g)), g)).tobytes())
p.stdin.close(); assert p.wait() == 0
subprocess.run([AS.F, '-nostdin', '-v', 'error', '-y', '-i', str(tmp), '-i', str(AS.O/'mix-balanced.wav'), '-map', '0:v', '-map', '1:a', '-vf', f"ass='{AS.O}/captions.ass'",
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-c:a', 'aac', '-b:a', '256k', '-t', '6.0', '-colorspace', 'bt709', '-color_primaries', 'bt709',
                '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', str(out)], check=True)
# the same 6 s of the 1.25x master for a matched comparison
subprocess.run([AS.F, '-nostdin', '-v', 'error', '-y', '-i', str(AS.O/'review'/f'{AS.NAME}.mp4'), '-t', '6.0', '-c', 'copy', str(AS.O/'review'/'opener-25pct.mp4')], check=True)
print('ALT', out)
