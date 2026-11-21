"""Round 3 second key pass. The faults left after ViTMatte sit mostly inside him: BiRefNet closed the gaps between arm, hand and body, so pool stone
and blue tile stayed solid there, where no edge band reaches. His skin is warm (red well above green), the stone is neutral and the tile blue, so inside
the cut-out a pixel that is clearly neither skin, shorts nor dark (hair, watch, ink) is taken back out. Face and glasses are protected (head: only the
outer 26 px), very small specks are left alone (sun on skin), and the mask is feathered so a blurred hand keeps its soft edge."""
import numpy as np, cv2


def nonskin(rgb):
    f = rgb.astype(np.float32); R, G, B = f[..., 0], f[..., 1], f[..., 2]
    lum = .3 * R + .59 * G + .11 * B
    rg = (R - G) / (lum + 20)
    grey = (lum > 75) & (G - B < 22)                         # shaded pool edge; olive shorts have blue far under green
    pale = np.clip((.095 - rg) / .03, 0, 1) * ((lum > 118) | grey)  # stone, sky, sunlit pool edge
    sat = (R - B) / (lum + 20)                               # a blurred mix of stone and skin still reads greyer than any skin
    pale = np.maximum(pale, np.clip((.32 - sat) / .08, 0, 1) * grey)
    blue = ((B > R + 14) & (B > G - 6) & (lum > 30)).astype(np.float32)  # tile and water
    return np.maximum(pale, blue), pale


def gapmask(rgb, a, head_frac=.20, min_area=14):
    """Soft 0..1 mask of background left inside the cut-out, at the size of rgb."""
    ys = np.where(a.max(1) > .5)[0]
    if not len(ys): return np.zeros(a.shape, np.float32)
    top = int(ys[0]); h = a.shape[0]; chin = top + int(h * head_frac)
    score, pale = nonskin(rgb)
    bad = (score > .5) & (a > .3)
    solid = (a > .5).astype(np.uint8); di = cv2.distanceTransform(solid, cv2.DIST_L2, 3)
    bad[top:chin] &= ((pale > .5) & (di < 26))[top:chin]; bad[:top] = False
    n, lab, st, _ = cv2.connectedComponentsWithStats(bad.astype(np.uint8), connectivity=8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= min_area
    m = keep[lab].astype(np.float32) * score
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    return np.clip(cv2.GaussianBlur(m, (0, 0), 1.0) * 1.2, 0, 1)


def skinfill(rgb, a, mot, reach=46):
    """Fast fingers: both matte models thin a blurred finger over the pale wall into a claw. Warm skin colour that is moving and sits just outside
    the cut-out goes back in, with its strength set by how warm the pixel is, which gives a natural blur edge. Tan stones never move, so they stay out."""
    f = rgb.astype(np.float32); R, G, B = f[..., 0], f[..., 1], f[..., 2]
    lum = .3 * R + .59 * G + .11 * B; rg = (R - G) / (lum + 20)
    warm = np.clip((rg - .125) / .05, 0, 1) * (R > B + 12)
    solid = (a > .5).astype(np.uint8)
    near = cv2.distanceTransform(1 - solid, cv2.DIST_L2, 3) < reach
    moving = cv2.GaussianBlur((cv2.GaussianBlur(mot, (0, 0), 2) > 16).astype(np.float32), (0, 0), 2) > .3
    add = warm * (near & moving)
    add = cv2.GaussianBlur(add, (0, 0), 1.0)
    add[:int(np.where(a.max(1) > .5)[0][0]) + int(a.shape[0] * .2)] = 0    # never around the head
    n, lab, st, _ = cv2.connectedComponentsWithStats(((np.maximum(add, a) > .4)).astype(np.uint8), connectivity=8)
    if n > 2: add = add * (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])))
    return np.maximum(a, add)


def softmotion(a, mot, sig=2.6, thr=30):
    """A fast hand is blurred in the picture, but a matte edge stays hard, which reads as chopped fingers. Where the picture moves fast the edge gets
    the same softness as the blur around it. Still parts of him never change."""
    z = cv2.GaussianBlur((cv2.GaussianBlur(mot, (0, 0), 2.5) > thr).astype(np.float32), (0, 0), 5)
    z = np.clip(z * 1.6, 0, 1)
    ys = np.where(a.max(1) > .5)[0]
    if len(ys): z[:int(ys[0]) + int(a.shape[0] * .2)] = 0
    return a * (1 - z) + cv2.GaussianBlur(a, (0, 0), sig) * z
