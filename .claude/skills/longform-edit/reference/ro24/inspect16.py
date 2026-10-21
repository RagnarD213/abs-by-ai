"""Stills from a key16 test: full frame on each background, 1:1 hair close-ups (2880 space = 0.75 native) on light and dark
fields beside the raw source, alpha view. usage: inspect16.py <key.mkv> <frame> <outprefix> [hx hy]"""
import sys, json, subprocess, numpy as np, cv2
sys.path.insert(0, '/Volumes/Expansion/_edit_work/RO-24/round1/recipe'); import comp16 as C
C.FF = C.FF + '.real'          # inspection reads a few frames: not a build, so not queued
key, k, pre = sys.argv[1], int(sys.argv[2]), sys.argv[3]
m = json.load(open(key + '.json')) if False else None
p = subprocess.Popen([C.FF, '-v', 'error', '-i', key, '-frames:v', str(k + 1), '-an', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
for i in range(k): p.stdout.read(C.IW * C.IH * 8)
F, A = C.read_frame(p); p.kill()
for bg in ['light', 'depth', 'navy']:
    img = C.compose(F, A, bg, 'warm'); cv2.imwrite(f'{pre}-full-{bg}.jpg', (cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)[:, :, ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
rows = np.where((A > .35).sum(1) >= 3)[0]; top = rows[0]; band = A[top:top + 260] > .5; cols = np.where(band.any(0))[0]; cx = (cols[0] + cols[-1]) // 2
hx = int(sys.argv[4]) if len(sys.argv) > 4 else int(cx - 400); hy = int(sys.argv[5]) if len(sys.argv) > 5 else int(max(0, top - 80))
sl = np.s_[hy:hy + 450, hx:hx + 800]
l = C.compose(F[sl], A[sl], None, 'warm', np.full((450, 800, 3), [.84, .87, .89], np.float32))
d = C.compose(F[sl], A[sl], None, 'warm', np.full((450, 800, 3), [.08, .10, .13], np.float32))
src = json.load(open(key + '.json')) if False else None
# raw source at the same moment and scale
start = float(sys.argv[6]) if len(sys.argv) > 6 else None
row = [l, d, np.repeat(A[sl][..., None], 3, 2)]
if start is not None:
    FF = C.FF; f0 = int(round(start * C.FPS)) + k
    raw = subprocess.check_output([FF, '-v', 'error', '-ss', f'{(f0 - .3) / C.FPS:.5f}', '-i', '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1726.MP4',
                                   '-frames:v', '1', '-vf', 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,scale=2880:1620:flags=area,format=rgb24', '-f', 'rawvideo', '-'])
    R = np.frombuffer(raw, np.uint8).reshape(1620, 2880, 3).astype(np.float32) / 255
    row = [R[sl]] + row
grid = np.concatenate([np.concatenate(row[:2], 1), np.concatenate(row[2:4], 1)], 0) if len(row) == 4 else np.concatenate(row, 1)
cv2.imwrite(f'{pre}-hair.png', (np.clip(grid, 0, 1)[:, :, ::-1] * 255).astype(np.uint8))
print('top', top, 'cx', cx, 'box', hx, hy)
