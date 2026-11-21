"""Key-check renders of a RO-24 plate, full 16:9 frame at 1920x1080 over the DS-40 check backdrops (pale, navy, pink), warm grade and
the approved light wrap.   python3 render16.py PLATE.mkv K0 K1 OUT_PREFIX [pale,navy,pink]"""
import sys, numpy as np, cv2, subprocess
sys.path.insert(0, '/Volumes/Expansion/_edit_work/RO-24/round2/recipe'); import comp16 as C
PLAIN = {'pale': [0.86, 0.89, 0.93], 'pink': [0.95, 0.25, 0.62], 'navy': [0.08, 0.12, 0.30]}
key, k0, k1, pre = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
looks = (sys.argv[5] if len(sys.argv) > 5 else 'pale,navy,pink').split(',')
p = subprocess.Popen([C.FF, '-v', 'error', '-i', key, '-an', '-vf', f'select=between(n\\,{k0}\\,{k1 - 1})', '-vsync', '0', '-f', 'rawvideo',
                      '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
W = {l: C.writer(f'{pre} {l}.mp4', crf=14) for l in looks}
bgs = {l: np.full((C.IH, C.IW, 3), PLAIN[l], np.float32) for l in looks}
n = 0
while n < k1 - k0:
    r = C.read_frame(p)
    if r is None: break
    F, A = r
    for l in looks:
        o = cv2.resize(C.compose(F, A, None, 'warm', bgs[l]), (1920, 1080), interpolation=cv2.INTER_AREA)
        W[l].stdin.write((np.clip(o, 0, 1) * 255 + .5).astype(np.uint8).tobytes())
    n += 1
for w in W.values(): w.stdin.close(); w.wait()
p.stdout.close(); p.wait(); print('RENDER DONE', pre, n)
