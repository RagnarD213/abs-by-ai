"""Ad 15 final: two-span patch on Muhammad's 09-21 HD export.

Span 1 (frames 5957-6006): add Muhammad's own AI-GENERATED pill (lifted from frame 4466) low right
inside the prospect's after picture on the "Download Your Future Self" screen.
Span 2 (frames 4523-4639): replace the repeated goal-image insert with camera scene recovered from
raw C1604 (picture = ad frame + 2860, i.e. his audio offset 95.394 s + his 1-frame picture lag),
wide framing (scale 1.00), graded with the model fitted on his 2:37 wide shot (ms.pkl), and his
flash ramp (4635-4639) rebuilt over it so it still lands on his white frame 4640.

Only GOPs [4500,4650) and [5940,6030) are re-encoded; every other access unit and all audio are
copied bit-for-bit from the source.
"""
import json, subprocess, sys, pickle
import numpy as np
from scipy.ndimage import gaussian_filter
from io_ import FF, RAW, SRC, rgb
from ms import feats, RR

W, H = 1920, 1080
FPS = 30000 / 1001
GOPS = [(4500, 4650), (5940, 6030)]
SPAN1 = (5957, 6006)
SPAN2 = (4523, 4639)
FLASH = (4635, 4639)
RAW_OFF = 2860
OUT = sys.argv[1] if len(sys.argv) > 1 else 'ad15_final.mp4'


def yuv_frames(f0, n):
    pre = max(0, f0 - 60)
    cmd = [FF, '-v', 'error', '-ss', f'{pre / FPS:.6f}', '-i', SRC, '-vf',
           f'trim=start_frame={f0 - pre}:end_frame={f0 - pre + n}', '-vsync', '0',
           '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.uint8)
    a = a.reshape(n, W * H * 3 // 2).copy()
    assert len(a) == n
    return a


def planes(buf):
    Y = buf[:W * H].reshape(H, W)
    U = buf[W * H:W * H * 5 // 4].reshape(H // 2, W // 2)
    V = buf[W * H * 5 // 4:].reshape(H // 2, W // 2)
    return Y, U, V


def rgb_to_yuv420(frames):
    """float RGB (full range) -> yuv420p bt709 limited, via ffmpeg accurate_rnd."""
    n = len(frames)
    data = (np.clip(frames, 0, 1) * 65535 + 0.5).astype('<u2').tobytes()
    cmd = [FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}', '-i', '-',
           '-vf', 'scale=in_color_matrix=bt709:out_color_matrix=bt709:in_range=pc:out_range=tv:'
                  'flags=accurate_rnd+full_chroma_int+bicubic,format=yuv420p',
           '-f', 'rawvideo', '-']
    out = subprocess.run(cmd, input=data, capture_output=True, check=True).stdout
    return np.frombuffer(out, np.uint8).reshape(n, W * H * 3 // 2).copy()


# ---------------- span 1: the pill ----------------
def pill_sprite():
    src = yuv_frames(4466, 1)[0]
    Y, _, _ = planes(src)
    x0, y0, x1, y1 = 946, 692, 1130, 724          # sprite box (exclusive end)
    # analytic rounded rect in pixel-centre coordinates, 4x4 supersampled
    L, R_, T, B, r = 947.55, 1126.35, 694.55, 721.45, 6.5
    ss = 4
    ys, xs = np.mgrid[y0:y1, x0:x1].astype(float)
    cov = np.zeros(ys.shape)
    for i in range(ss):
        for j in range(ss):
            py = ys - 0.5 + (i + 0.5) / ss
            px = xs - 0.5 + (j + 0.5) / ss
            cx = np.clip(px, L + r, R_ - r)
            cy = np.clip(py, T + r, B - r)
            inside = (px >= L) & (px <= R_) & (py >= T) & (py <= B) & ((px - cx) ** 2 + (py - cy) ** 2 <= r * r)
            cov += inside
    cov /= ss * ss
    col = np.where(cov >= 0.999, Y[y0:y1, x0:x1], 3).astype(float)   # edge ring = his outline tone
    return x0, y0, col, cov


def picture_fade(Yf, dy):
    """1.0 = picture fully in; <1 while it fades up from white (frames 5957-5959)."""
    patch = Yf[915 + dy:955 + dy, 860:960].astype(float).mean()
    return patch


def do_span1(buf, f0):
    x0, y0, col, cov = pill_sprite()
    dys = json.load(open('dy.json'))
    DX, DY = 30, 236
    ref_patch = None
    ref_idx = 5980 - f0
    Yr, _, _ = planes(buf[ref_idx])
    ref_patch = picture_fade(Yr, 0)
    report = []
    for n in range(SPAN1[0], SPAN1[1] + 1):
        k = n - f0
        Yf, Uf, Vf = planes(buf[k])
        d = int(dys[str(n)])
        d = d - (d % 2)                               # keep chroma-aligned (even) offsets
        p = picture_fade(Yf, int(dys[str(n)]))
        white = 235.0
        a_pic = float(np.clip((white - p) / (white - ref_patch), 0, 1))
        if n >= 5963:                                 # fade-up finished; confetti in the patch is not a fade
            a_pic = 1.0
        a = cov * a_pic
        ty, tx = y0 + DY + d, x0 + DX
        hh, ww = col.shape
        reg = Yf[ty:ty + hh, tx:tx + ww].astype(float)
        Yf[ty:ty + hh, tx:tx + ww] = np.clip(np.rint(reg * (1 - a) + col * a), 0, 255).astype(np.uint8)
        # chroma: neutral pill, alpha averaged over 2x2
        ac = a.reshape(hh // 2, 2, ww // 2, 2).mean((1, 3)) if (hh % 2 == 0 and ww % 2 == 0) else None
        if ac is None:
            raise SystemExit('sprite must have even size')
        cy, cx = ty // 2, tx // 2
        for P in (Uf, Vf):
            reg = P[cy:cy + hh // 2, cx:cx + ww // 2].astype(float)
            P[cy:cy + hh // 2, cx:cx + ww // 2] = np.clip(np.rint(reg * (1 - ac) + 128 * ac), 0, 255).astype(np.uint8)
        report.append((n, d, round(a_pic, 3), (tx, ty, tx + ww, ty + hh)))
    return report


# ---------------- span 2: camera scene ----------------
C = pickle.load(open('ms.pkl', 'rb'))


def grade(R):
    return np.clip((feats(R, RR).reshape(W * H, -1) @ C).reshape(H, W, 3), 0, 1)


def do_span2(buf, f0):
    n0, n1 = SPAN2
    his_ins = rgb(SRC, FLASH[0] - 1, 1)[0]                       # 4634: last clean insert frame
    his_fl = rgb(SRC, FLASH[0], FLASH[1] - FLASH[0] + 1)
    for c0 in range(n0, n1 + 1, 24):
        c1 = min(c0 + 24, n1 + 1)
        raws = rgb(RAW, c0 + RAW_OFF, c1 - c0)
        out = []
        for i, n in enumerate(range(c0, c1)):
            g = grade(raws[i])
            if FLASH[0] <= n <= FLASH[1]:
                h = his_fl[n - FLASH[0]]
                b = 1 - (1 - h) / np.maximum(1 - his_ins, 1e-3)
                b = gaussian_filter(np.clip(b, 0, 1), (6, 6, 0))
                g = 1 - (1 - g) * (1 - b)
            out.append(g.astype(np.float32))
        yuv = rgb_to_yuv420(np.stack(out))
        for i, n in enumerate(range(c0, c1)):
            buf[n - f0] = yuv[i]
        print('  span2 chunk', c0, c1 - 1, flush=True)


def encode(buf, path):
    n = len(buf)
    cmd = [FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', f'{W}x{H}',
           '-r', '30000/1001', '-i', '-', '-c:v', 'libx264', '-profile:v', 'main', '-level', '4.1',
           '-preset', 'slow', '-crf', '14', '-g', '30', '-keyint_min', '30', '-sc_threshold', '0',
           '-bf', '0', '-refs', '1',
           '-x264-params', 'aud=1:repeat-headers=1:scenecut=0:open-gop=0:vbv-maxrate=25000:vbv-bufsize=25000',
           '-bsf:v', 'h264_mp4toannexb', '-f', 'h264', path]
    subprocess.run(cmd, input=buf.tobytes(), check=True)


def split_aus(data):
    """split an Annex B stream into access units at each AUD (nal type 9)."""
    starts = []
    i = 0
    L = len(data)
    while True:
        j = data.find(b'\x00\x00\x01', i)
        if j < 0:
            break
        if j + 3 < L and (data[j + 3] & 0x1f) == 9:
            s = j - 1 if j > 0 and data[j - 1] == 0 else j
            starts.append(s)
        i = j + 3
    starts.append(L)
    return [data[starts[k]:starts[k + 1]] for k in range(len(starts) - 1)], data[:starts[0]]


if __name__ == '__main__':
    subprocess.run([FF, '-v', 'error', '-y', '-i', SRC, '-map', '0:v', '-c', 'copy', '-bsf:v', 'h264_mp4toannexb',
                    '-f', 'h264', 'src.h264'], check=True)
    src_aus, lead = split_aus(open('src.h264', 'rb').read())
    print('source AUs', len(src_aus), 'lead bytes', len(lead))
    assert len(src_aus) == 6205, len(src_aus)
    new = list(src_aus)
    reuse = set(int(x) for x in __import__('os').environ.get('REUSE', '').split(',') if x)
    for (g0, g1) in GOPS:
        if g0 in reuse:
            seg_aus, _ = split_aus(open(f'seg_{g0}.h264', 'rb').read())
            assert len(seg_aus) == g1 - g0
            new[g0:g1] = seg_aus
            print('reused', g0)
            continue
        buf = yuv_frames(g0, g1 - g0)
        if g0 <= SPAN1[0] < g1:
            for row in do_span1(buf, g0):
                print('span1', row)
        if g0 <= SPAN2[0] < g1:
            do_span2(buf, g0)
            print('span2 built')
        np.save(f'seg_{g0}.npy', buf)
        encode(buf, f'seg_{g0}.h264')
        seg_aus, seg_lead = split_aus(open(f'seg_{g0}.h264', 'rb').read())
        assert len(seg_aus) == g1 - g0, (len(seg_aus), g1 - g0)
        assert not seg_lead.strip(b'\x00'), 'unexpected bytes before first AUD'
        new[g0:g1] = seg_aus
    open('out.h264', 'wb').write(lead + b''.join(new))
    subprocess.run([FF, '-v', 'error', '-y', '-fflags', '+genpts', '-r', '30000/1001', '-f', 'h264', '-i', 'out.h264',
                    '-i', SRC, '-map', '0:v', '-map', '1:a', '-c', 'copy', '-video_track_timescale', '30000',
                    '-movflags', '+faststart', OUT], check=True)
    print('wrote', OUT)
