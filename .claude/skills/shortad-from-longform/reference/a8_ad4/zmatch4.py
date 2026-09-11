#!/usr/bin/env python3
"""HIS time maps for every media beat of Ad 4, by NCC of the region he shows against the source's own frames.

His frames come from mf/frames640.rgb (640x360, every 2nd frame of each media range, extracted BY INDEX -- skill A7.12).
  robot  85-437   the portrait AI clip inside his olive card        vs ai-robot-supplement-audit-10s.mp4 (24 fps)
  stack  437-639  full frame above his lower third                  vs dan-real-supplement-stack_pan (29.97)
  app    5145-5238 the phone screen inside his card                 vs 09_CLIP (60 fps -> sampled at 20)
  audit  5534-5704 the phone screen inside his card                 vs app-supplement-audit-scroll.mp4 (30)
  results 6041-6206 / safety 6282-6391: the phone beside Dan        vs the two ad-assets recordings (30)
Writes media_map.json {name: [[n, t_src, r, box]]} and mf/verify_<name>.jpg (his crop | the matched source frame)."""
import json, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw
import beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS = 30000/1001
idx = list(map(int, open('mf/index.txt').read().split())); pos = {n: i for i, n in enumerate(idx)}
HIS = np.memmap('mf/frames640.rgb', np.uint8, 'r').reshape(-1, 360, 640, 3)
assert len(HIS) == len(idx), (len(HIS), len(idx))

def src_frames(src, w, h, fps=None, color=False):
    vf = ([f'fps={fps}'] if fps else []) + [f'scale={w}:{h}:flags=area', 'format=rgb24' if color else 'format=gray']
    b = subprocess.run([FF, '-v', 'error', '-i', src, '-vf', ','.join(vf), '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape((-1, h, w, 3) if color else (-1, h, w))
def src_fps(src):
    r = subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=r_frame_rate',
                        '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split('/')
    return float(r[0])/float(r[1])
def z(a): a = a.astype(np.float32); a = a - a.mean(); return a/max(float(np.sqrt((a*a).sum())), 1e-6)

def white_box(im, xr=(0, 640), yr=(0, 360), thr=205):
    """bbox of the bright, neutral phone SCREEN (percentiles, so a stray highlight cannot stretch it)"""
    a = im[yr[0]:yr[1], xr[0]:xr[1]].astype(np.int16)
    m = (a.min(-1) > thr) & ((a.max(-1) - a.min(-1)) < 30)
    ys, xs = np.nonzero(m)
    if len(xs) < 300: return None
    return (xr[0]+int(np.percentile(xs, 1)), yr[0]+int(np.percentile(ys, 1)), xr[0]+int(np.percentile(xs, 99))+1, yr[0]+int(np.percentile(ys, 99))+1)

def hole_box(im):
    """the non-olive, non-field media hole inside his olive card"""
    a = im.astype(np.float32)
    ol = np.abs(a - np.array([93, 101, 60], np.float32)).sum(2) > 55
    fl = np.abs(a - np.array([12, 13, 9], np.float32)).sum(2) > 45
    m = ol & fl; m[:, :30] = False; m[:, 610:] = False; m[:15] = False; m[345:] = False
    ys, xs = np.nonzero(m)
    if len(xs) < 800: return None
    return (int(np.percentile(xs, 2)), int(np.percentile(ys, 2)), int(np.percentile(xs, 98))+1, int(np.percentile(ys, 98))+1)

OUT = {}
def match(name, src, n0, n1, boxfn, sw, sh, fps_samp=None, rows=None):
    sf = fps_samp or src_fps(src)
    S = src_frames(src, sw, sh, fps_samp); SZ = np.stack([z(s if rows is None else s[:int(sh*rows)]) for s in S])
    SC = src_frames(src, sw*3, sh*3, fps_samp, color=True)
    res = []
    for n in range(n0, n1):
        if n not in pos or n in B.FLASH: continue
        im = np.asarray(HIS[pos[n]]); bx = boxfn(im)
        if bx is None: res.append([n, None, 0.0, None]); continue
        x0, y0, x1, y1 = bx
        g = cv2.cvtColor(np.ascontiguousarray(im[y0:y1, x0:x1]), cv2.COLOR_RGB2GRAY)
        t = cv2.resize(g, (sw, sh), interpolation=cv2.INTER_AREA)
        if rows is not None: t = t[:int(sh*rows)]
        v = SZ.reshape(len(SZ), -1) @ z(t).reshape(-1)
        j = int(np.argmax(v)); res.append([n, round(j/sf, 3), round(float(v[j]), 3), [int(c) for c in bx]])
    OUT[name] = dict(src=src, n0=n0, n1=n1, map=res)
    ok = [r for r in res if r[1] is not None]
    print(f'{name}: {len(ok)}/{len(res)} matched, r median {np.median([r[2] for r in ok]):.2f} min {min(r[2] for r in ok):.2f}')
    print('   ', ' '.join(f'{n}->{t}({r:.2f})' for n, t, r, _ in ok[::3]))
    # verification sheet: his crop | matched source frame, 12 samples
    pick = ok[::max(1, len(ok)//12)][:12]; W = 150
    sheet = Image.new('RGB', (len(pick)*2*W + len(pick)*10, 300), (0, 0, 0)); d = ImageDraw.Draw(sheet)
    for k, (n, t, r, bx) in enumerate(pick):
        im = np.asarray(HIS[pos[n]]); x0, y0, x1, y1 = bx
        a = Image.fromarray(np.ascontiguousarray(im[y0:y1, x0:x1])); a.thumbnail((W, 280))
        bimg = Image.fromarray(SC[int(round(t*sf))]); bimg.thumbnail((W, 280))
        x = k*(2*W+10); sheet.paste(a, (x, 18)); sheet.paste(bimg, (x+W, 18)); d.text((x+2, 2), f'{n} {t:.2f} {r:.2f}', fill=(255, 255, 0))
    sheet.save(f'mf/verify_{name}.jpg', quality=85)

match('robot', B.ROBOT, 86, 437, hole_box, 27, 48)
match('stack', B.STACK, 438, 639, lambda im: (0, 0, 640, 255), 96, 38, rows=None)
match('app', B.APPGEN, 5146, 5238, lambda im: white_box(im, (180, 460), (20, 345), 190), 30, 65, fps_samp=20)
match('audit', B.AUDIT, 5535, 5704, lambda im: white_box(im, (150, 470), (10, 350), 200), 36, 64)
match('results', B.RESULTS, 6041, 6206, lambda im: white_box(im, (420, 640), (0, 330), 200), 30, 53)
match('safety', B.SAFETY, 6282, 6391, lambda im: white_box(im, (420, 640), (0, 330), 200), 30, 53)
json.dump(OUT, open('media_map.json', 'w'))
