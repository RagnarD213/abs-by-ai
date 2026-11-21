#!/usr/bin/env python3
"""assets/app_demo.mp4: the app recording (1320x2868 @60) played on HIS time map inside the app card (6716-6905),
capped at 24.5 s of the recording (the in-app before/after and the email form start at 26 s / 29 s -- banned);
assets/app_result.png: his result screen rebuilt -- the goal image ALONE on white under 'YOUR GOAL IMAGE'."""
import json, subprocess, numpy as np, os
from PIL import Image, ImageDraw, ImageOps
import sys; sys.path.insert(0, '.'); import g5 as G
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
LIB = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/00 ASSETS USED IN THE REFERENCE AD"
APP = f"{LIB}/09_CLIP_app-generate-future-self.mp4"; SAFE = 24.5
N0, N1 = 6716, 6905
# his anchors (frame -> recording second), from zmatch5.py; the loader (8.85 -> 17.7) runs ~2.4x, then holds
AN = [(6716, 0.30), (6729, 0.45), (6733, 1.7), (6749, 2.9), (6765, 3.75), (6777, 5.55), (6801, 5.7), (6805, 8.55),
      (6833, 8.55), (6837, 8.85), (6865, 13.8), (6901, 17.7), (6905, 17.9)]
ns = np.array([a[0] for a in AN], float); ts = np.array([a[1] for a in AN], float)
want = [float(np.clip(np.interp(n, ns, ts), 0, SAFE)) for n in range(N0, N1)]
pw = 500; ph = round(pw*2868/1320) & ~1
if not os.path.exists('assets/app_demo.mp4'):
    idx = sorted(set(int(round(t*60)) for t in want))
    p = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-i', APP, '-vf', f'scale={pw}:{ph}:flags=area', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    keep, k = {}, 0
    while True:
        b = p.stdout.read(pw*ph*3)
        if not b: break
        if k in idx: keep[k] = b
        k += 1
        if k > idx[-1]: break
    p.kill()
    e = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{pw}x{ph}', '-r', '30000/1001', '-i', '-',
                          '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                          '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', 'assets/app_demo.mp4'], stdin=subprocess.PIPE)
    for t in want:
        j = int(round(t*60)); j = min(keep, key=lambda q: abs(q-j)); e.stdin.write(keep[j])
    e.stdin.close(); e.wait(); print('app_demo.mp4', len(want), 'frames', want[0], '->', want[-1])
# the result screen: white, the goal image (AI-labelled inside it), 'YOUR GOAL IMAGE' under it -- his 231.0 frame
goal = ImageOps.exif_transpose(Image.open("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/01 Before and After Images/dan by pool - AI GOAL IMAGE.png")).convert('RGB')
W, H = pw, ph; scr = Image.new('RGBA', (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(scr)
gw = W - 60; gh = round(gw*goal.height/goal.width); g = goal.resize((gw, gh), Image.LANCZOS)
scr.paste(g, (30, 120)); G.ai_chip(scr, 30+gw-10, 120+gh-10, size=26)
d.text((W//2, 120+gh+34), "YOUR GOAL IMAGE", font=G.font(26, "SemiBold"), fill=(60, 60, 70, 255), anchor="mt")
d.text((W//2, 120+gh+80), "Results are not guaranteed.", font=G.font(18, "Medium"), fill=(140, 140, 150, 255), anchor="mt")
scr.convert('RGB').save('assets/app_result.png'); print('app_result.png', scr.size)
