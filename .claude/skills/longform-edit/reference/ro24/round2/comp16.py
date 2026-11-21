"""RO-24 compositor for the keyed 16:9 green screen: unpremultiplied F + alpha (key16.py FFV1) -> graded presenter over a
background, framed, 1920x1080. The grade is the locked DS-40 grade function applied ONCE to the reconstructed
foreground only; the background keeps its own colour (chroma-key README). Backgrounds are drawn here, static.

  comp16.py <key.mkv> <out.mp4> [--bg light|depth|navy] [--grade warm|natural|bright] [--crop x,y,w (2880 space)]
            [--stills 0,30,59] [--hair out_hair.mp4]
"""
import sys, os, json, subprocess, argparse
import numpy as np, cv2
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
IW, IH = 2880, 1620; FPS = 30000 / 1001

def grade(x, mode):
    """Locked DS-40 grade (round3-grade.py), verbatim maths; 'bright' is its third mode."""
    if mode == 'rich': gains = [1.015, 1, 1.01]; sat = 1.12; exposure = 1.03; con = 1.07     # RO-24 option: warm, more colour and snap
    elif mode == 'natural': gains = [.985, 1, 1.035]; sat = .94; exposure = 1.035; con = 1.035
    elif mode == 'warm': gains = [1.01, 1, 1.015]; sat = 1.04; exposure = 1.035; con = 1.045
    else: gains = [.985, 1.005, 1.035]; sat = .98; exposure = 1.075; con = 1.055
    x = x * np.array(gains, np.float32); y = np.sum(x * np.array([.2126, .7152, .0722], np.float32), -1, keepdims=True)
    x = y + sat * (x - y); x = np.maximum(x, 0) ** .97 * exposure; x = (x - .18) * con + .18
    return np.clip(x, 0, 1)

_BG = {}
def background(name, w=IW, h=IH, cx=0.5, cy=0.40):
    key = (name, w, h, cx, cy)
    if key in _BG: return _BG[key]
    y, x = np.mgrid[:h, :w].astype(np.float32); x /= w; y /= h
    d = np.sqrt(((x - cx) / 0.62) ** 2 + ((y - cy) / 0.85) ** 2)       # elliptical falloff from behind his head
    if name == 'light':                  # DS-40 approved flat light field
        im = np.ones((h, w, 3), np.float32) * np.array([.84, .87, .89], np.float32)
    elif name == 'depth':                # light cool studio: brighter behind him, gently deeper toward the edges
        c0 = np.array([.90, .925, .945], np.float32); c1 = np.array([.70, .755, .815], np.float32)
        t = np.clip(d, 0, 1.25) / 1.25; t = t * t * (3 - 2 * t)
        im = c0 * (1 - t[..., None]) + c1 * t[..., None]
    elif name == 'navy':                 # Soft Blue Light navy with the brand's blue light rising behind him
        base = np.array([5, 13, 28], np.float32) / 255; glow = np.array([46, 92, 150], np.float32) / 255
        g = np.exp(-(d / 0.55) ** 2)
        im = base * (1 - g[..., None]) + glow * g[..., None]
    else:
        raise SystemExit('unknown background ' + name)
    rng = np.random.default_rng(7)
    im = np.clip(im + (rng.random((h, w, 1), np.float32) - .5) / 255 * 1.5, 0, 1)   # dither against banding
    _BG[key] = im.astype(np.float32)
    return _BG[key]

def reader(path, w=IW, h=IH):
    return subprocess.Popen([FF, '-v', 'error', '-i', path, '-an', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-'], stdout=subprocess.PIPE)

def read_frame(p, w=IW, h=IH):
    raw = p.stdout.read(w * h * 8)
    if len(raw) < w * h * 8: return None
    a = np.frombuffer(raw, '<u2').reshape(h, w, 4).astype(np.float32) / 65535
    return a[..., :3], a[..., 3]

WRAP, WRAP_SIG = 0.12, 11      # approved DS-40 Claude R2 stage 2 light wrap (house key standard 2026-10-21); 0 = round 1 behaviour
def compose(F, A, bgname, mode, bgimg=None):
    bg = bgimg if bgimg is not None else background(bgname)
    aa = A[..., None]
    out = grade(F, mode) * aa + (1 - aa) * bg
    if WRAP:
        inv = (1 - A).astype(np.float32)
        bb = cv2.GaussianBlur(np.ascontiguousarray(bg * inv[..., None], dtype=np.float32), (0, 0), WRAP_SIG)
        cover = cv2.GaussianBlur(inv, (0, 0), WRAP_SIG)[..., None]
        wm = WRAP * cover * aa
        out = out * (1 - wm) + bb / np.maximum(cover, 1e-3) * wm
    return np.clip(out, 0, 1)

def writer(path, w=1920, h=1080, crf=14):
    return subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', '30000/1001', '-i', '-',
                             '-an', '-vf', 'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p', '-c:v', 'libx264',
                             '-crf', str(crf), '-preset', 'medium', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                             '-movflags', '+faststart', path], stdin=subprocess.PIPE)

def frame_out(C, crop=None, size=(1920, 1080)):
    if crop:
        x, y, w = crop; h = int(round(w * 9 / 16)); C = C[y:y + h, x:x + w]
    return cv2.resize(C, size, interpolation=cv2.INTER_AREA)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('key'); ap.add_argument('out')
    ap.add_argument('--bg', default='depth'); ap.add_argument('--grade', default='warm'); ap.add_argument('--crop')
    ap.add_argument('--stills', default=''); ap.add_argument('--hair'); ap.add_argument('--hairbox')
    A = ap.parse_args()
    crop = tuple(int(v) for v in A.crop.split(',')) if A.crop else None
    stills = {int(s) for s in A.stills.split(',') if s}
    rd = reader(A.key); wr = writer(A.out)
    hw = None
    if A.hair:
        hb = tuple(int(v) for v in A.hairbox.split(','))       # x,y in 2880 space; 960x540 window at 1:1
        hw = writer(A.hair, 960 * 2, 540, crf=12)
    i = 0
    while True:
        fr = read_frame(rd)
        if fr is None: break
        F, Al = fr
        C = compose(F, Al, A.bg, A.grade)
        o = frame_out(C, crop)
        wr.stdin.write((o * 255 + .5).astype(np.uint8).tobytes())
        if hw is not None:
            x, y = hb
            l = compose(F[y:y + 540, x:x + 960], Al[y:y + 540, x:x + 960], None, A.grade, background('light')[y:y + 540, x:x + 960])
            dk = compose(F[y:y + 540, x:x + 960], Al[y:y + 540, x:x + 960], None, A.grade, np.full((540, 960, 3), [.08, .10, .13], np.float32))
            hw.stdin.write((np.concatenate([l, dk], 1) * 255 + .5).astype(np.uint8).tobytes())
        if i in stills:
            cv2.imwrite(A.out[:-4] + f'-{i:04d}.jpg', (o[:, :, ::-1] * 255 + .5).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
        i += 1
    wr.stdin.close(); wr.wait()
    if hw is not None: hw.stdin.close(); hw.wait()
    print('COMP DONE', A.out, i)
