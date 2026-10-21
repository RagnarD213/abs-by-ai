"""Hand-fix test on the reviewers' flagged frames, with real motion: decodes f-1, f, f+1 at native, body key on f, DIS speed to the
neighbours as in key16.render, then approved vs refined (with hands) composited on the light field around the lower body.
Prints, per frame, how many solid pixels the hand step lowered and how many of those are DARK (luma < .2) or DEEP (> 15 px from
the screen) - both should be ~0 - and saves raw | approved | refined | lowered-pixels tiles.
usage: handtest2.py <outdir> <frame> [<frame> ...]   (source frame numbers of C1726)"""
import sys, subprocess, json, numpy as np, cv2
from scipy.ndimage import distance_transform_edt
sys.path.insert(0, '/Volumes/Expansion/_edit_work/RO-24/round1/recipe'); import key16 as K, comp16 as C
out = sys.argv[1]; frames = [int(x) for x in sys.argv[2:]]; FF = K.FF + '.real'
box = (932, 0, 2972, 2160); x0, y0, x1, y1 = box; bg = K.screen_field('plate', 0, 0, box)
bh, bw = y1 - y0, x1 - x0; sh, sw = bh // 2, bw // 2
flow = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
lum = lambda x: .2126 * x[..., 0] + .7152 * x[..., 1] + .0722 * x[..., 2]
rep = {}
for f in frames:
    raw = subprocess.check_output([FF, '-v', 'error', '-ss', f'{(f - 1 - .3) / K.FPS:.5f}', '-i', K.SRC, '-frames:v', '3', '-an', '-vf', K.DEC, '-f', 'rawvideo', '-'])
    ims = [np.ascontiguousarray(np.frombuffer(raw, '<u2', count=K.H * K.WD * 3, offset=i * K.H * K.WD * 6).reshape(K.H, K.WD, 3)[y0:y1, x0:x1]).astype(np.float32) / 65535 for i in range(3)]
    grays = [cv2.cvtColor((cv2.resize(np.clip(m, 0, 1), (sw, sh), interpolation=cv2.INTER_AREA) * 255).astype('uint8'), cv2.COLOR_RGB2GRAY) for m in ims]
    im = ims[1]
    sp = np.maximum(np.linalg.norm(flow.calc(grays[1], grays[0], None), axis=2), np.linalg.norm(flow.calc(grays[1], grays[2], None), axis=2))
    mv = cv2.dilate(cv2.GaussianBlur(sp, (0, 0), 3), np.ones((15, 15), np.uint8))
    motion = cv2.resize(np.clip((mv * 2 - K.MOTION_LO) / (K.MOTION_HI - K.MOTION_LO), 0, 1), (bw, bh)); speed = cv2.resize(mv * 2, (bw, bh))
    a, hair, top, near = K.body_key(im, bg); f_ = K.foreground(im, a, bg)
    nf = np.where(hair[:, :, None] > 0, np.array([.105, .105, .095], np.float32), near)
    a2, f2 = K.refine(im, a, f_, nf)
    a3, f3 = K.refine(im, a, f_, nf, bg, hair, motion, speed)
    low = (a2 - a3) > .1
    solid = a2 > .95
    d_bg = distance_transform_edt(~(a <= .05))
    dark = low & solid & (lum(im) < .2); deep = low & solid & (d_bg > 15)
    rep[f] = dict(lowered=int(low.sum()), lowered_solid=int((low & solid).sum()), dark_solid=int(dark.sum()), deep_solid=int(deep.sum()),
                  max_speed=round(float(speed.max()), 1))
    print(f, rep[f], flush=True)
    ys, xs = np.where(a2 > .5); yb = max(0, int(ys.max() - 1250))
    sl = np.s_[yb:, max(0, xs.min() - 40):min(bw, xs.max() + 40)]
    def comp(fp, aa):
        F = fp[sl] / np.maximum(aa[sl][..., None], 1e-4); A = aa[sl][..., None]
        return np.clip(C.grade(np.clip(F, 0, 1), 'warm') * A + (1 - A) * np.array([.84, .87, .89], np.float32), 0, 1)
    lw = np.zeros(a2[sl].shape + (3,), np.float32); lw[..., 0] = np.clip((a2 - a3)[sl] / .4, 0, 1); lw[..., 1] = a3[sl] * .5
    img = np.concatenate([np.concatenate([np.clip(im[sl], 0, 1), comp(f_, a)], 1), np.concatenate([comp(f3, a3), lw], 1)], 0)
    s = 2000 / img.shape[1]
    cv2.imwrite(f'{out}/t{f}.jpg', (cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)[:, :, ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 90])
json.dump(rep, open(f'{out}/report.json', 'w'), indent=1)
