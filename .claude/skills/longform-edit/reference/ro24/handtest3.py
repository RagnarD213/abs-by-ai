"""Which hands() condition blocks the pixels an earlier version opened correctly (finger gaps, fast-hand rims)?
Target = pixels where key/fm/prev_refined3 (the ungated version that opened gaps, but also opened shorts) has alpha at least 0.15
below the approved key, restricted to bright pixels (luma >= .25, so the shorts/watch/shaded regions it wrongly opened drop out).
For each target pixel, report the share failing each condition of the current hands().
usage: handtest3.py <frame> [...]   (C1726 source frames)"""
import sys, subprocess, numpy as np, cv2
sys.path.insert(0, '/Volumes/Expansion/_edit_work/RO-24/round1/recipe'); import key16 as K, comp16 as C
FF = K.FF + '.real'; box = (932, 0, 2972, 2160); x0, y0, x1, y1 = box; bg = K.screen_field('plate', 0, 0, box)
bh, bw = y1 - y0, x1 - x0; sh, sw = bh // 2, bw // 2; flow = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
KF = {'K1': 16064, 'K2': 17068, 'K3': 17907}; W = '/Volumes/Expansion/_edit_work/RO-24/round1/key/fm'
lum = lambda x: .2126 * x[..., 0] + .7152 * x[..., 1] + .0722 * x[..., 2]
def plate_alpha(path, k):
    p = subprocess.Popen([FF, '-v', 'error', '-i', path, '-an', '-vf', f'select=eq(n\\,{k})', '-vsync', '0', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)
    F, A = C.read_frame(p); p.kill(); return A
for f in [int(x) for x in sys.argv[1:]]:
    kn = max((k for k in KF if KF[k] <= f), key=lambda k: KF[k]); k = f - KF[kn]
    raw = subprocess.check_output([FF, '-v', 'error', '-ss', f'{(f - 1 - .3) / K.FPS:.5f}', '-i', K.SRC, '-frames:v', '3', '-an', '-vf', K.DEC, '-f', 'rawvideo', '-'])
    ims = [np.ascontiguousarray(np.frombuffer(raw, '<u2', count=K.H * K.WD * 3, offset=i * K.H * K.WD * 6).reshape(K.H, K.WD, 3)[y0:y1, x0:x1]).astype(np.float32) / 65535 for i in range(3)]
    gr = [cv2.cvtColor((cv2.resize(np.clip(m, 0, 1), (sw, sh), interpolation=cv2.INTER_AREA) * 255).astype('uint8'), cv2.COLOR_RGB2GRAY) for m in ims]
    sp = np.maximum(np.linalg.norm(flow.calc(gr[1], gr[0], None), axis=2), np.linalg.norm(flow.calc(gr[1], gr[2], None), axis=2))
    mv = cv2.dilate(cv2.GaussianBlur(sp, (0, 0), 3), np.ones((15, 15), np.uint8))
    motion = cv2.resize(np.clip((mv * 2 - K.MOTION_LO) / (K.MOTION_HI - K.MOTION_LO), 0, 1), (bw, bh)); speed = cv2.resize(mv * 2, (bw, bh))
    im = ims[1]; a, hair, top, near = K.body_key(im, bg); f_ = K.foreground(im, a, bg)
    nf = np.where(hair[:, :, None] > 0, np.array([.105, .105, .095], np.float32), near)
    K.HDBG = {}; a3, f3 = K.refine(im, a, f_, nf, bg, hair, motion, speed); D = K.HDBG; K.HDBG = None
    ap = plate_alpha(f'{W}/{kn}.mkv', k); p3 = plate_alpha(f'{W}/prev_refined3/{kn}_refined.mkv', k)
    sc = 2880 / 3840; X0, X1 = int(x0 * sc), int(x1 * sc)
    up = lambda z: cv2.resize(z[:, X0:X1], (bw, bh), interpolation=cv2.INTER_LINEAR)
    tgt = ((up(ap) - up(p3)) > .15) & (lum(im) >= .25)
    n = int(tgt.sum()); print(f'frame {f} ({kn} {k}): target px {n}, max speed {speed.max():.0f}, target speed p50 {np.median(speed[tgt]) if n else 0:.0f}')
    if not n: continue
    conds = {'motion<0.5': D['motion'][tgt] < .5, 'reach (d_bg>reach+4)': D['d_bg'][tgt] > D['reach'][tgt] + 4, 'floor': D['lumI'][tgt] < D['lo'][tgt] - .03,
             'res>=.03': D['res'][tgt] >= .03, 't<=.06': D['t'][tgt] <= .06, 'd_sk>=60': D['d_sk'][tgt] >= 60, 'd_sk>d_dk': D['d_sk'][tgt] > D['d_dk'][tgt],
             'den<=.005': D['den'][tgt] <= .005}
    for c, m in conds.items(): print(f'   {c:24s} {100 * m.mean():5.1f} %')
    print(f'   wz>0.5 on target {100 * (D["wz"][tgt] > .5).mean():5.1f} %   t p50 {np.median(D["t"][tgt]):.2f}  d_bg p50 {np.median(D["d_bg"][tgt]):.0f}  reach p50 {np.median(D["reach"][tgt]):.0f}')
