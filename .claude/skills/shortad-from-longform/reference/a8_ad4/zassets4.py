#!/usr/bin/env python3
"""Ad 4's media assets, each played on HIS time map (media_map.json from zmatch4/4b/4c) so frame n of the asset is what
his frame n showed, one output frame per beat frame (asserted):

  assets/robot.mp4    85-437   the AI robot clip, his two shots (0.2-4.1 s, 6.1-10.0 s of the source), no held tail
  assets/stack.mp4    437-639  Dan's real supplement-stack pan, his 0.82x slow-down from its first frame
  assets/appgen.mp4   5145-5238 the future-self generation recording (09_CLIP), his 8.2-14.1 s
  assets/audit.mp4    5534-5704 the supplement-audit start screen, scrolled onto "Start my audit" and HELD there (Dan r2)
  assets/results.mp4  6041-6206 the audit results recording, banner -> keep/drop list at his pace
  assets/safety.mp4   6282-6391 the Safety Officer card
  assets/download.png           the app's "Download Your Future Self" page, cropped ABOVE the email box (Dan r2/r3)

The maps are made monotonic (running maximum) and interpolated; a sample below its r floor is not trusted."""
import json, os, subprocess, numpy as np
from PIL import Image
import beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
M = json.load(open('media_map.json')); os.makedirs('assets', exist_ok=True)

def decode(src, w, h, ss, dur, fps):
    b = subprocess.run([FF, '-v', 'error', '-ss', f'{ss:.3f}', '-t', f'{dur:.3f}', '-i', src, '-vf',
                        f'fps={fps},scale={w}:{h}:flags=lanczos,format=rgb24', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, h, w, 3)

def tmap(points, n0, n1, lo=None, hi=None):
    """monotonic piecewise-linear t(n) through (n, t) points, extended at the ends with the neighbouring slope"""
    p = sorted(points); ns = np.array([a for a, _ in p], float); ts = np.maximum.accumulate(np.array([b for _, b in p], float))
    out = np.interp(np.arange(n0, n1), ns, ts)
    if len(p) >= 2:
        s0 = (ts[min(3, len(ts)-1)] - ts[0])/max(ns[min(3, len(ns)-1)] - ns[0], 1)
        s1 = (ts[-1] - ts[max(-4, -len(ts))])/max(ns[-1] - ns[max(-4, -len(ns))], 1)
        k = np.arange(n0, n1); out = np.where(k < ns[0], ts[0] - (ns[0]-k)*s0, out); out = np.where(k > ns[-1], ts[-1] + (k-ns[-1])*s1, out)
    if lo is not None: out = np.maximum(out, lo)
    if hi is not None: out = np.minimum(out, hi)
    return out

def write(name, frames, n):
    assert len(frames) == n, (name, len(frames), n)
    h, w = frames[0].shape[:2]
    e = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', '30000/1001',
                          '-i', '-', '-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709',
                          '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', f'assets/{name}.mp4'], stdin=subprocess.PIPE)
    for f in frames: e.stdin.write(np.ascontiguousarray(f).tobytes())
    e.stdin.close(); e.wait(); print(f'assets/{name}.mp4  {w}x{h}  {n} frames')

def build(name, src, n0, n1, pts, w, h, sfps, lo=0.0, hi=None):
    t = tmap(pts, n0, n1, lo, hi); ss = max(0.0, float(t.min()) - 0.2)
    F = decode(src, w, h, ss, float(t.max()) - ss + 0.3, sfps)
    k = np.clip(np.round((t - ss)*sfps).astype(int), 0, len(F)-1)
    write(name, [F[i] for i in k], n1 - n0)
    return t

def pts_of(name, rmin):
    return [(r[0], r[1]) for r in M[name]['map'] if r[1] is not None and r[2] >= rmin]

# robot: his two shots (the source's own cut is at 5.042 s); a shot never crosses it, and no frame is held.
# STRICTLY LINEAR per shot: the NCC map of this low-motion clip jitters (1.75 s matched at 113-137, 1.62-2.08 around it), and
# the running maximum turned that jitter into plateaus -- 13 frozen runs of 8-20 frames in the first render (watch scan).
# Shot 1 follows his matched ends (97 -> 0.21 s, 257 -> 4.04 s: 0.72x); shot 2 fills its beat from his in-point (6.10 s)
# to the clip's last frame (0.68x) instead of his 1.7 s held last frame (skill A7.10).
t1 = np.clip(0.21 + (np.arange(85, 262) - 97)*(4.04 - 0.21)/(257 - 97), 0.0, 4.95)
t2 = np.linspace(6.10, 10.0, 437 - 262)
F = decode(B.ROBOT, 578, 1028, 0.0, 10.1, 24)
write('robot', [F[min(int(round(x*24)), len(F)-1)] for x in np.r_[t1, t2]], 437-85)
# stack: his 0.8226x slow-down from the first frame (zmatch4: 449->0.300 ... 635->5.405, r 0.43-0.55, monotonic)
build('stack', B.STACK, 437, 639, [(438, 0.0), (635, 5.405)], 1000, 562, FPS, 0.0, 5.50)
# app generation: his 8.2 -> 14.1 s (zmatch4 r >= 0.6; the fade-in frames before 5159 extend the first slope)
build('appgen', B.APPGEN, 5145, 5238, pts_of('app', 0.6), 500, 1086, 60)
# audit: 5.1 -> 5.8 s, then HELD on "Start my audit" to the end of the beat (Dan, round 2)
build('audit', B.AUDIT, 5534, 5704, pts_of('audit', 0.8), 540, 960, 30, 0.0, 5.8)
# results / safety: the full-res template maps (zmatch4c); the low-r tail of results extends the scroll slope
build('results', B.RESULTS, 6041, 6206, pts_of('results', 0.55), 440, 782, 30, 5.6, 19.4)
build('safety', B.SAFETY, 6282, 6391, pts_of('safety', 0.4), 440, 782, 30, 3.0, 10.9)
# the download page: the recording's 30.0 s frame, cut above "Enter Your Email" (Dan r2: "Show only the headline and the
# after picture ... the email box and the button are below the bottom of the phone frame and never in shot")
g = decode(B.APPGEN, 1320, 2868, 30.0, 0.1, 30)[0]
Image.fromarray(g).save('assets/download_full.png')
print('download_full.png saved -- crop decided against his frame f05395')
