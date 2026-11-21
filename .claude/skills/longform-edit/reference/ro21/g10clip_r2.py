"""RO-21 round 2: the G10 background (Dan 2026-10-29: "in the background, put a sleep-deprived fat guy"). The Codex still
round2/ai/G10_man.png becomes a slow 1.00 -> 1.06 push-in clip (sub-pixel warp, no zoompan jitter) that the studio set's
TV plays during BG22 (the set draws its own AI-GENERATED chip). Lifted a little: the TV multiplies by 0.86.
  python3 g10clip_r2.py   -> round2/bgclips/G10_man.mp4 (11 s, 1920x1080, 29.97)"""
import subprocess, numpy as np, cv2
W = '/Volumes/Expansion/_edit_work/RO-21/round2'; FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
im = cv2.imread(f'{W}/ai/G10_man.png')[:, :, ::-1].astype(np.float32) / 255
im = cv2.resize(im, (1920, int(round(1920 * im.shape[0] / im.shape[1]))), interpolation=cv2.INTER_LANCZOS4)
lut = np.clip(im, 0, 1) ** 0.85 * 1.04                              # gentle lift for the dim TV
im = np.clip(lut, 0, 1)
N = int(round(11 * 30000 / 1001)); fx, fy = 0.70 * 1920, 0.42 * im.shape[0]
p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30000/1001', '-i', '-',
                      '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow',
                      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', f'{W}/bgclips/G10_man.mp4'], stdin=subprocess.PIPE)
for i in range(N):
    s = 1.0 + 0.06 * (i / (N - 1)) ** 1.0
    s *= 1080 / im.shape[0] if im.shape[0] < 1080 else 1.0
    M = np.float32([[s, 0, fx - s * fx], [0, s, 540 - s * fy]])
    M[0, 2] = min(0, max(1920 - s * 1920, M[0, 2])); M[1, 2] = min(0, max(1080 - s * im.shape[0], M[1, 2]))
    f = cv2.warpAffine(im, M, (1920, 1080), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    p.stdin.write((np.clip(f, 0, 1) * 255 + .5).astype(np.uint8).tobytes())
p.stdin.close(); assert p.wait() == 0; print('G10 clip', N, 'frames')
