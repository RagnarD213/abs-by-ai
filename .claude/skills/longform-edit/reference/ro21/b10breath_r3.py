"""RO-21 B10 fallback motion (round 3): START's own pixels, warped by the measured START->END chest movement (DIS optical
flow, kept only below the collarbones where END differs) through one slow breath in and part way out, plus a slow 1.00 ->
1.04 push-in toward his face. Nothing is redrawn, so nothing can morph (Veo takes on 2026-10-29 opened his mouth and rolled
his head). AI-GENERATED chip burned in (inserts are opaque). -> round3/broll/B10_breath.mp4 (B10's frame count + 2 padded)
  python3 b10breath_r3.py"""
import json, subprocess, numpy as np, cv2, sys
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg'); import gsbg as G
from PIL import Image
B = '/Volumes/Expansion/_edit_work/RO-21'; FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
S = cv2.imread(f'{B}/round2/ai/B10_start.png'); E = cv2.imread(f'{B}/round2/ai/B10_end.png')
g = lambda x: cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_ULTRAFAST); dis.setFinestScale(0)
flow = dis.calc(g(E), g(S), None)                 # for each END pixel, where it came from in START (backward map)
h, w = S.shape[:2]; y = np.arange(h, dtype=np.float32)[:, None]
mask = np.clip((y - 470) / 70, 0, 1); flow *= mask[..., None]                     # head/neck/room stay put
flow = cv2.GaussianBlur(flow, (0, 0), 9)                                            # one smooth body movement, no texture
P = {p['id']: p for p in json.load(open(f'{B}/round2/plan_r2.json'))}; a, b = P['B10']['a'], P['B10']['b']
FPS = 30000 / 1001; N = int(round((b - a) * FPS)) + 2
chip = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); G.SB.disclosure(chip, 'AI-GENERATED', xy=(56, 48))
ca = np.asarray(chip, np.float32) / 255; crgb, calpha = ca[..., :3][..., ::-1], ca[..., 3:4]
gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
fx, fy = 385 / w, 300 / h                                                            # push toward his face
p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1920x1080', '-r', '30000/1001', '-i', '-',
                      '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow',
                      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart',
                      f'{B}/round3/broll/B10_breath.mp4'], stdin=subprocess.PIPE)
for i in range(N):
    t = i / (N - 1)
    ph = 0.5 - 0.5 * np.cos(2 * np.pi * min(1.0, t * 0.8))                           # in (0 -> 1) by 62 %, then part way out
    fr = cv2.remap(S, (gx + flow[..., 0] * ph).astype(np.float32), (gy + flow[..., 1] * ph).astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    s = 1920 / w * (1.0 + 0.04 * t); Wd, Hd = w * s, h * s
    ox = np.clip(fx * 1920 - fx * Wd, 1920 - Wd, 0); oy = np.clip(fy * 1080 - fy * Hd, 1080 - Hd, 0)
    M = np.float32([[s, 0, ox], [0, s, oy]])
    o = cv2.warpAffine(fr, M, (1920, 1080), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).astype(np.float32) / 255
    o = o * (1 - calpha) + crgb * calpha
    p.stdin.write((np.clip(o, 0, 1) * 255 + .5).astype(np.uint8).tobytes())
p.stdin.close(); assert p.wait() == 0
print('B10_breath', N, 'frames; max chest shift px', round(float(np.abs(flow).max()), 1))
