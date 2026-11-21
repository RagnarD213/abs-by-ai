"""House stage-2 composition from DS44 R2. No template forks. Local source caches, actual film grade, same .75-scale key math.
KEY_EDGE is named separately from the corner fade to avoid the reference module's EDGE name collision.
"""
from pathlib import Path
import numpy as np,cv2,json
from scipy import ndimage as ndi
from PIL import Image as _Im, ImageDraw as _Dr
from grade import grade,LOOKS
W=Path(__file__).resolve().parents[1]
FPS=30000/1001;CW,CH=1080,1920
MIN_FRAG,KEY_EDGE,HAZE=900,4,4.5
WRAP,WRAP_SIG=.12,10
EDGE,FEATHER=54,180
LOOK='B_warmvivid'
KEYS={};KSTART={}
def configure(keydata,look='B_warmvivid'):
 global KEYS,KSTART,LOOK
 KEYS={k:Path(v['cache']) for k,v in keydata.items()};KSTART={k:v['start'] for k,v in keydata.items()};LOOK=look

def key_frame(piece, t_roll):
    i = int(round((t_roll - KSTART[piece])*FPS)); p = KEYS[piece]/f'f{i:04d}.npy'
    d = np.load(p).astype(np.float32); Fp, a = d[..., :3], d[..., 3]
    lab, n = ndi.label(a > 0.03)
    if n:
        sizes = ndi.sum(np.ones_like(a), lab, index=np.arange(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= MIN_FRAG
        m = ndi.binary_dilation(keep[lab], iterations=KEY_EDGE)
        a = np.where(m, a, 0); Fp = np.where(m[..., None], Fp, 0)
    far = ndi.distance_transform_edt(a < 0.25) > HAZE
    a_new = np.where(far, np.clip((a - 0.15)/0.85, 0, 1), a)
    Fp = Fp*np.where(a > 1e-4, a_new/np.maximum(a, 1e-4), 0)[..., None]
    return Fp, a_new

def feather(Fp, a, fw=EDGE, amount=1.0):
    """Fade the keyed footage toward its right and top edges, for the small Dan whose frame edge sits inside the screen
    (a hand or shoulder that leaves the camera fades instead of stopping on a straight line). Premultiplied."""
    if amount <= 0: return Fp, a
    h, w = a.shape
    rx = np.clip((w - 1 - np.arange(w, dtype=np.float32))/max(fw, 1.0), 0, 1); ry = np.clip(np.arange(h, dtype=np.float32)/FEATHER, 0, 1)
    ramp = 1 - amount + amount*(rx[None, :]*ry[:, None])
    return Fp*ramp[..., None], a*ramp

def place(out, Fp, a, s, x0, y0, wrap=WRAP, wrap_sig=WRAP_SIG):
    """Composite a premultiplied keyed layer scaled by s with its top-left at (x0, y0) (output px); grade after the resize."""
    h, w = a.shape
    sw, sh = max(1, int(round(w*s))), max(1, int(round(h*s)))
    # crop to the visible part first (cheaper), with a small margin for the resize
    vx0, vy0 = max(0, int(np.floor(-x0/s)) - 2), max(0, int(np.floor(-y0/s)) - 2)
    vx1, vy1 = min(w, int(np.ceil((CW - x0)/s)) + 2), min(h, int(np.ceil((CH - y0)/s)) + 2)
    if vx1 <= vx0 or vy1 <= vy0: return out
    Fc, ac = Fp[vy0:vy1, vx0:vx1], a[vy0:vy1, vx0:vx1]
    ox, oy = x0 + vx0*s, y0 + vy0*s
    tw, th = max(1, int(round((vx1 - vx0)*s))), max(1, int(round((vy1 - vy0)*s)))
    interp = cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC
    Fr = cv2.resize(Fc, (tw, th), interpolation=interp); ar = np.clip(cv2.resize(ac, (tw, th), interpolation=interp), 0, 1)
    Fr = np.clip(Fr, 0, None)
    G = np.where(ar[..., None] > 0.01, Fr/np.maximum(ar[..., None], 1e-3), 0)
    G = grade(np.clip(G, 0, 1), **LOOKS[LOOK]) if LOOK != 'none' else G
    X0, Y0 = int(round(ox)), int(round(oy)); X1, Y1 = min(CW, X0 + tw), min(CH, Y0 + th)
    sx, sy = max(0, -X0), max(0, -Y0); X0, Y0 = max(0, X0), max(0, Y0)
    if X1 <= X0 or Y1 <= Y0: return out
    ga = G[sy:sy + Y1 - Y0, sx:sx + X1 - X0]; aa = ar[sy:sy + Y1 - Y0, sx:sx + X1 - X0]
    reg = out[Y0:Y1, X0:X1]; A = aa[..., None]; comp = ga*A + reg*(1 - A)
    if wrap:
        sg = max(2.0, wrap_sig*min(1.0, s/0.87)); inv = 1 - aa
        bb = cv2.GaussianBlur(reg*inv[..., None], (0, 0), sg); cover = cv2.GaussianBlur(inv, (0, 0), sg)[..., None]
        wm = wrap*cover*A; comp = comp*(1 - wm) + bb/np.maximum(cover, 1e-3)*wm
    out[Y0:Y1, X0:X1] = comp
    return out

def _rr(w, h, r):
    m = _Im.new('L', (max(1, w), max(1, h)), 0); _Dr.Draw(m).rounded_rectangle((0, 0, max(1, w) - 1, max(1, h) - 1), max(0, int(r)), fill=255)
    return np.asarray(m, np.float32)[..., None]/255

def draw_card(out, img, rect, r=22, shadow=1.0):
    """A 16:9 picture as a rounded card with a soft shadow and a hairline Soft Blue border (the DS-40 R3 card)."""
    x, y, w, h = [int(round(v)) for v in rect]
    if w < 4 or h < 4: return out
    if shadow > 0:
        sh = np.zeros(out.shape[:2], np.float32); sh[max(0, y + 14):y + 14 + h, max(0, x + 6):x + 6 + w] = 0.59*shadow
        out *= 1 - cv2.GaussianBlur(sh, (0, 0), 18)[..., None]
    if img.shape[:2] != (h, w): img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    m = _rr(w, h, r); X0, Y0, X1, Y1 = max(0, x), max(0, y), min(CW, x + w), min(CH, y + h)
    sx, sy = X0 - x, Y0 - y; reg = out[Y0:Y1, X0:X1]; mm = m[sy:sy + Y1 - Y0, sx:sx + X1 - X0]
    out[Y0:Y1, X0:X1] = img[sy:sy + Y1 - Y0, sx:sx + X1 - X0]*mm + reg*(1 - mm)
    b = np.zeros((h, w, 1), np.float32); bm = _rr(w, h, r) - np.pad(_rr(w - 4, h - 4, r - 2), ((2, 2), (2, 2), (0, 0)))
    bc = np.array([150, 200, 255], np.float32)/255; ba = np.clip(bm, 0, 1)*0.47
    reg = out[Y0:Y1, X0:X1]; bb = ba[sy:sy + Y1 - Y0, sx:sx + X1 - X0]
    out[Y0:Y1, X0:X1] = reg*(1 - bb) + bc*bb
    return out

def u8(x): return (np.clip(x, 0, 1)*255 + 0.5).astype(np.uint8)
