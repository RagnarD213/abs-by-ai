"""Round 1 key vs round 2 key (the approved DS-40 Claude R2 key on this roll), side by side, both warm on the depth background with
the same compositor, Dan at a readable size (the wide shot cropped to 1440 x 1620 around him, each half 960 x 1080).
    python3 compare_r2.py FILM_T0 FILM_T1 OUT.mp4 [--zoom]      (film seconds; --zoom: 2x on the lower body for hands)"""
import sys, json, subprocess, numpy as np, cv2
sys.path.insert(0, '/Volumes/Expansion/_edit_work/RO-24/round2/recipe'); import comp16 as C
W2 = '/Volumes/Expansion/_edit_work/RO-24/round2'; W1 = '/Volumes/Expansion/_edit_work/RO-24/round1'
FPS = 30000 / 1001
t0, t1, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]; zoom = '--zoom' in sys.argv
E = json.load(open(f'{W2}/edl_film_pic.json'))['pieces']
R1 = {k: json.load(open(f'{W1}/key/fm/{k}.mkv.json'))['f0'] for k in ('K1', 'K2', 'K3')}
R1N = {k: json.load(open(f'{W1}/key/fm/{k}.mkv.json'))['frames'] for k in R1}
g = 0; spans = []
for p in E:
    n = p['f1'] - p['f0']; a, b = max(g, int(t0 * FPS)), min(g + n, int(t1 * FPS))
    if a < b: spans.append((p, p['f0'] + a - g, b - a))
    g += n
def reader(path, k0, n):
    return subprocess.Popen([C.FF, '-v', 'error', '-i', path, '-an', '-vf', f'select=between(n\\,{k0}\\,{k0 + n - 1})', '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
wr = C.writer(out, crf=16); bg = C.background('depth')
def label(img, text, x, y):
    (tw, th), base = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, .8, 2)
    cv2.rectangle(img, (x - 10, y - th - 10), (x + tw + 10, y + base + 6), (20, 28, 40), -1)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, .8, (255, 255, 255), 2, cv2.LINE_AA)
for p, s0, n in spans:
    k1 = [k for k in R1 if R1[k] <= s0 and s0 + n <= R1[k] + R1N[k]]
    assert k1, ('round 1 has no key for', s0)
    r1 = reader(f'{W1}/key/fm/{k1[0]}_refined.mkv', s0 - R1[k1[0]], n)
    m2 = json.load(open(p['key'] + '.json')); r2 = reader(p['key'], s0 - m2['f0'], n)
    cx = int(np.median([gg[2] for gg in m2['geo'] if gg[2] > 0])); x0 = int(np.clip(cx - 720, 0, C.IW - 1440))
    for i in range(n):
        Fa, Aa = C.read_frame(r1); Fb, Ab = C.read_frame(r2)
        ca = C.compose(Fa, Aa, None, 'warm', bg)[:, x0:x0 + 1440]; cb = C.compose(Fb, Ab, None, 'warm', bg)[:, x0:x0 + 1440]
        if zoom: ca, cb = ca[810:1620, 360:1080], cb[810:1620, 360:1080]
        h = [cv2.resize(c, (960, 1080), interpolation=cv2.INTER_AREA if not zoom else cv2.INTER_CUBIC) for c in (ca, cb)]
        o = (np.clip(np.concatenate(h, 1), 0, 1) * 255 + .5).astype(np.uint8).copy()
        label(o, 'Round 1 key', 24, 44); label(o, 'Round 2: your approved Bill Maher R2 key', 984, 44)
        wr.stdin.write(o.tobytes())
    r1.kill(); r2.kill()
wr.stdin.close(); wr.wait(); print('COMPARE DONE', out)
