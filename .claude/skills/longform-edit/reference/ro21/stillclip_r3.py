"""A still -> a slow 1.00 -> 1.06 push-in clip for the studio set's TV (sub-pixel warp, no zoompan jitter), lifted a little
because the TV multiplies by 0.86. Generalised from g10clip_r2.py (round 2, approved by Dan for G10).
  python3 stillclip_r3.py STILL OUT.mp4 [--fx 0.5 --fy 0.30 --secs 14 --lift 0.85]"""
import argparse, subprocess, numpy as np, cv2
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
ap = argparse.ArgumentParser(); ap.add_argument('still'); ap.add_argument('out'); ap.add_argument('--fx', type=float, default=0.5)
ap.add_argument('--fy', type=float, default=0.30); ap.add_argument('--secs', type=float, default=14); ap.add_argument('--lift', type=float, default=0.85)
ap.add_argument('--pad', action='store_true', help='portrait on a plain studio backdrop: whole body, backdrop extended to 16:9')
A = ap.parse_args()
im = cv2.imread(A.still)[:, :, ::-1].astype(np.float32) / 255
h, w = im.shape[:2]
if A.pad and w / h < 16 / 9:                         # whole body: height fills, the plain backdrop is extended sideways
    H = 1080; W = int(round(w * H / h)); body = cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4)
    L = (1920 - W) // 2; out = np.zeros((1080, 1920, 3), np.float32)
    lc = np.median(body[:, :12], axis=1, keepdims=True); rc = np.median(body[:, -12:], axis=1, keepdims=True)
    out[:, :L] = cv2.GaussianBlur(np.repeat(lc, L, 1), (0, 0), 6); out[:, L + W:] = cv2.GaussianBlur(np.repeat(rc, 1920 - L - W, 1), (0, 0), 6)
    out[:, L:L + W] = body; im = out; fy = A.fy
elif w / h < 16 / 9:                                   # portrait: centre a 16:9 band on the focus point (the TV is 16:9)
    ch = int(w * 9 / 16); y0 = int(np.clip(A.fy * h - ch / 2, 0, h - ch)); im = im[y0:y0 + ch]; fy = (A.fy * h - y0) / ch
else:
    fy = A.fy
im = cv2.resize(im, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
im = np.clip(np.clip(im, 0, 1) ** A.lift * 1.04, 0, 1)
N = int(round(A.secs * 30000 / 1001)); fx, fyp = A.fx * 1920, fy * 1080
p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30000/1001', '-i', '-',
                      '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow',
                      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', A.out], stdin=subprocess.PIPE)
for i in range(N):
    s = 1.0 + 0.06 * i / (N - 1)
    M = np.float32([[s, 0, fx - s * fx], [0, s, fyp - s * fyp]])
    f = cv2.warpAffine(im, M, (1920, 1080), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    p.stdin.write((f * 255 + .5).astype(np.uint8).tobytes())
p.stdin.close(); assert p.wait() == 0; print('clip', A.out, N, 'frames')
