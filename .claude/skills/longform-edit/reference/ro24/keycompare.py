"""Moving key comparisons for the round-1 page, from one key range rendered both ways (key16 --variant both):
  side  : approved key | refined edges, both on the recommended background, Dan at a readable size
  hair  : 1:1 (0.75 native) head and shoulder close-ups, approved | refined, on Bill Maher's light field and a dark field
  raw   : the raw green screen | the refined key on the background, same crop
usage: keycompare.py <K.mkv> <k0> <k1> <outdir> [--bg depth] [--grade warm]"""
import sys, os, json, subprocess, argparse
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comp16 as C
SRC = '/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1726.MP4'
ap = argparse.ArgumentParser(); ap.add_argument('key'); ap.add_argument('k0', type=int); ap.add_argument('k1', type=int); ap.add_argument('out')
ap.add_argument('--bg', default='depth'); ap.add_argument('--grade', default='warm'); ap.add_argument('--tag', default='')
A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
meta = json.load(open(A.key + '.json')); f0 = meta['f0']
geo = {g[0]: g for g in meta['geo']}
cx = int(np.median([geo[k][2] for k in range(A.k0, A.k1) if k in geo and geo[k][2] > 0]))
top = min(geo[k][1] for k in range(A.k0, A.k1) if k in geo and geo[k][1] >= 0)
ref = A.key.replace('.mkv', '_refined.mkv')
def rd(path):
    return subprocess.Popen([C.FF, '-v', 'error', '-i', path, '-an', '-vf', f'select=between(n\\,{A.k0}\\,{A.k1 - 1})', '-vsync', '0',
                             '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
pa, pr = rd(A.key), rd(ref)
raw = subprocess.Popen([C.FF, '-v', 'error', '-ss', f'{(f0 + A.k0 - .3) / C.FPS:.5f}', '-i', SRC, '-frames:v', str(A.k1 - A.k0), '-an', '-vf',
                        'scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,scale=2880:1620:flags=area,format=rgb24',
                        '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
tag = A.tag
W = {n: C.writer(f'{A.out}/key-{n}{tag}.mp4', crf=16) for n in ('side', 'hair', 'raw')}
bg = C.background(A.bg); light = np.full((540, 960, 3), [.84, .87, .89], np.float32); dark = np.full((540, 960, 3), [.08, .10, .13], np.float32)
x0 = int(np.clip(cx - 720, 0, C.IW - 1440)); hx = int(np.clip(cx - 480, 0, C.IW - 960)); hy = int(max(0, top - 70))
def label(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, .9, (0, 0, 0), 4, cv2.LINE_AA); cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, .9, (255, 255, 255), 1, cv2.LINE_AA)
for i in range(A.k1 - A.k0):
    Fa, Aa = C.read_frame(pa); Fr, Ar = C.read_frame(pr)
    R = np.frombuffer(raw.stdout.read(C.IW * C.IH * 3), np.uint8).reshape(C.IH, C.IW, 3).astype(np.float32) / 255
    ca = C.compose(Fa, Aa, None, A.grade, bg); cr = C.compose(Fr, Ar, None, A.grade, bg)
    s = np.concatenate([cv2.resize(ca[:, x0:x0 + 1440], (960, 1080), interpolation=cv2.INTER_AREA), cv2.resize(cr[:, x0:x0 + 1440], (960, 1080), interpolation=cv2.INTER_AREA)], 1)
    rw = np.concatenate([cv2.resize(R[:, x0:x0 + 1440], (960, 1080), interpolation=cv2.INTER_AREA), cv2.resize(cr[:, x0:x0 + 1440], (960, 1080), interpolation=cv2.INTER_AREA)], 1)
    sl = np.s_[hy:hy + 540, hx:hx + 960]
    h = np.concatenate([np.concatenate([C.compose(Fa[sl], Aa[sl], None, A.grade, light), C.compose(Fr[sl], Ar[sl], None, A.grade, light)], 1),
                        np.concatenate([C.compose(Fa[sl], Aa[sl], None, A.grade, dark), C.compose(Fr[sl], Ar[sl], None, A.grade, dark)], 1)], 0)
    outs = {}
    for n, img in (('side', s), ('hair', h), ('raw', rw)):
        o = (np.clip(img, 0, 1) * 255 + .5).astype(np.uint8).copy()
        if n == 'side': label(o, 'Approved Bill Maher key', 24, 44); label(o, 'Refined edges', 984, 44)
        if n == 'raw': label(o, 'Raw green screen', 24, 44); label(o, 'Keyed (refined edges)', 984, 44)
        if n == 'hair': label(o, 'Approved key', 24, 40); label(o, 'Refined edges', 984, 40)
        W[n].stdin.write(o.tobytes()); outs[n] = o
    if i == (A.k1 - A.k0) // 2:
        for n, o in outs.items(): cv2.imwrite(f'{A.out}/key-{n}{tag}.jpg', o[:, :, ::-1], [cv2.IMWRITE_JPEG_QUALITY, 94])
for w in W.values(): w.stdin.close(); w.wait()
for q in (pa, pr, raw): q.stdout.close(); q.wait()
print('KEYCOMPARE DONE', A.out)
