"""A7 redo 3 (review 3 FAIL) START fixes before the shared-background rebuild: (1) the jumper's hair from a Codex crop edit
matched to END's hair (crops/s_head_hair.png), merged only where it differs inside the head box; (2) his red shirt and grey
sweatpants colour-matched to END's in Lab (mean and spread per garment); (3) the mask keeps his whole left shoe and sole
(personmask lost its lower half); (4) the pale strip between the calm man's jeans and hand is left out of the mask.
Writes masks/S3fix.png, masks/S3.full.mask2.png."""
import cv2, numpy as np
D = '/Volumes/Expansion/_edit_work/RO-24/round5/ai/A7/'
S = cv2.imread(D + 'masks/S3.png'); E = cv2.imread(D + 'masks/E.png')
mS = cv2.imread(D + 'masks/S3.full.mask.png', 0); mE = cv2.imread(D + 'masks/E.mask.png', 0)
# (1) hair
x0, y0, x1, y1 = 520, 170, 720, 330
ed = cv2.resize(cv2.imread(D + 'crops/s_head_hair.png'), (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
crop = S[y0:y1, x0:x1].astype(np.float32); edf = ed.astype(np.float32)
diff = np.abs(edf - crop).max(-1) > 14
head = np.zeros(diff.shape, bool); head[210 - y0:282 - y0, 585 - x0:675 - x0] = True
w = cv2.GaussianBlur(cv2.dilate((diff & head).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32), (0, 0), 2.5)[..., None]
S[y0:y1, x0:x1] = (crop * (1 - w) + edf * w).round().clip(0, 255).astype(np.uint8)
print('hair px merged', int((w[..., 0] > 0.5).sum()))
# (2) garments, Lab match START -> END inside each man's mask
def garments(I, m, box):
    hsv = cv2.cvtColor(I, cv2.COLOR_BGR2HSV); b, g, r = [I[..., k].astype(int) for k in range(3)]
    inb = np.zeros(m.shape, bool); bx0, by0, bx1, by1 = box; inb[by0:by1, bx0:bx1] = True
    body = (m > 128) & inb
    shirt = body & (r > g + 50) & (r > b + 40)
    pants = body & (hsv[..., 1] < 70) & (hsv[..., 2] > 60) & (hsv[..., 2] < 220)
    return shirt, pants
sS, pS = garments(S, mS, (380, 180, 700, 480)); sE, pE = garments(E, mE, (330, 470, 760, 880))
LS = cv2.cvtColor(S, cv2.COLOR_BGR2LAB).astype(np.float32); LE = cv2.cvtColor(E, cv2.COLOR_BGR2LAB).astype(np.float32)
for name, a, b in (('shirt', sS, sE), ('pants', pS, pE)):
    before = LS[a].mean(0)
    for c in range(3):
        mu_a, sd_a, mu_b, sd_b = LS[..., c][a].mean(), LS[..., c][a].std(), LE[..., c][b].mean(), LE[..., c][b].std()
        k = 1.0 if c else 0.6                                     # chroma fully, lightness partly (he is in sun, END in a lit lawn)
        tgt = (LS[..., c] - mu_a) * (sd_b / max(sd_a, 1e-3)) + mu_b
        LS[..., c] = np.where(a, LS[..., c] * (1 - k) + tgt * k, LS[..., c])
    print(name, 'Lab', before.round(1), '->', LS[a].mean(0).round(1), 'END', LE[b].mean(0).round(1), int(a.sum()), int(b.sum()))
S2 = cv2.cvtColor(LS.clip(0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
soft = lambda q: cv2.GaussianBlur(cv2.dilate(q.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.2)[..., None]
wg = np.maximum(soft(sS), soft(pS))
S = (S.astype(np.float32) * (1 - wg) + S2.astype(np.float32) * wg).round().clip(0, 255).astype(np.uint8)
cv2.imwrite(D + 'masks/S3fix.png', S)
# (3) whole shoes in the mask; (4) the pale strip out
m2 = mS.copy()
hsv = cv2.cvtColor(S, cv2.COLOR_BGR2HSV)
sb = (slice(440, 476), slice(530, 630)); shoe = (hsv[sb][..., 2] > 150) & (hsv[sb][..., 1] < 60)  # white/grey shoe pixels
shoe = cv2.dilate(shoe.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
m2[sb] = np.maximum(m2[sb], shoe.astype(np.uint8) * 255)
st = (slice(296, 360), slice(1279, 1300)); b_, g_, r_ = [S[st][..., k].astype(int) for k in range(3)]
keep = ((b_ > r_ + 15) & (b_ < 150)) | ((r_ > g_ + 15) & (r_ > b_ + 25))      # denim or skin
m2[st] = np.where(keep, m2[st], 0)
cv2.imwrite(D + 'masks/S3.full.mask2.png', m2)
print('shoe px added', int(shoe.sum()), '| strip px removed', int(((mS[st] > 110) & ~keep).sum()))
# (2b) review 3 measured the END sweatpants blue-grey (median rgb 112/123/150 on the legs) against START's neutral 112/113/119:
# a per-channel gain on START's trouser pixels (inside his mask, not red, not skin, not the white shoes), feathered 1.2 px
S = cv2.imread(D + 'masks/S3fix.png'); m2 = cv2.imread(D + 'masks/S3.full.mask2.png', 0)
b_, g_, r_ = [S[..., k].astype(int) for k in range(3)]; box = np.zeros(m2.shape, bool); box[300:462, 420:640] = True
tr = box & (m2 > 128) & ~(r_ > g_ + 40) & ~((r_ > g_ + 15) & (r_ > b_ + 25)) & (S.max(-1) < 230) & (S.max(-1) > 50)
gain = np.array([150 / 119, 123 / 113, 1.0])                     # BGR
wt = cv2.GaussianBlur(tr.astype(np.float32), (0, 0), 1.2)[..., None]
S = (S.astype(np.float32) * (1 - wt) + (S.astype(np.float32) * gain).clip(0, 255) * wt).round().astype(np.uint8)
cv2.imwrite(D + 'masks/S3fix.png', S); print('trouser px tinted', int(tr.sum()), 'median now', np.median(S[tr], 0)[::-1])
