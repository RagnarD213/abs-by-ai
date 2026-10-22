"""One native frame: approved body key vs refined (with hands), composited at native scale on light and dark fields around the hands."""
import sys, subprocess, numpy as np, cv2
sys.path.insert(0, '/Volumes/Expansion/_edit_work/RO-24/round1/recipe'); import key16 as K, comp16 as C
f = int(sys.argv[1]); out = sys.argv[2]; FF = K.FF + '.real'
raw = subprocess.check_output([FF, '-v', 'error', '-ss', f'{(f - .3) / K.FPS:.5f}', '-i', K.SRC, '-frames:v', '1', '-an', '-vf', K.DEC, '-f', 'rawvideo', '-'])
full = np.frombuffer(raw, '<u2').reshape(K.H, K.WD, 3).astype(np.float32) / 65535
box = (932, 0, 2972, 2160); x0, y0, x1, y1 = box
im = np.ascontiguousarray(full[y0:y1, x0:x1]); bg = K.screen_field('plate', 0, 0, box)
a, hair, top, near = K.body_key(im, bg); f_ = K.foreground(im, a, bg)
nf = np.where(hair[:, :, None] > 0, np.array([.105, .105, .095], np.float32), near)
a2, f2 = K.refine(im, a, f_, nf); a3, f3 = K.refine(im, a, f_, nf, bg, hair)
print('pixels changed by hands():', int((np.abs(a3 - a2) > .02).sum()), ' mean drop', float((a2 - a3)[np.abs(a3 - a2) > .02].mean()) if (np.abs(a3 - a2) > .02).any() else 0)
ys, xs = np.where(a2 > .5); yb = int(K.H * .55)
sl = np.s_[yb:, max(0, xs.min() - 60):min(x1 - x0, xs.max() + 60)]
def comp(fp, aa, col):
    F = fp[sl] / np.maximum(aa[sl][..., None], 1e-4); A = aa[sl][..., None]
    return np.clip(C.grade(np.clip(F, 0, 1), 'warm') * A + (1 - A) * np.array(col, np.float32), 0, 1)
rows = [np.concatenate([comp(f2, a2, c), comp(f3, a3, c)], 1) for c in ((.84, .87, .89), (.08, .10, .13))]
img = np.concatenate(rows, 0); s = 2400 / img.shape[1]
cv2.imwrite(out, (cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)[:, :, ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
np.save(out + '.a2.npy', a2[sl]); np.save(out + '.a3.npy', a3[sl])
