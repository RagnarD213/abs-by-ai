"""RO-21 PH1: the approved RO-06 app tour screen (library B0544, Dan 2026-10-10 "save that for future reuse") in the approved
WV-01 iPhone shell (ro06/phone_demo.py shell geometry), as a transparent overlay on the left third beside Dan (he stands right,
the planner's side-card placement). Rises in 0.4 s, drifts gently the whole time, fades out 0.3 s; AI-GENERATED chip under the
phone (the tour shows AI exercise demos). -> round1/hf/phone/PH1.mov (ProRes 4444 with alpha)."""
import json, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared'); import softblue as SB
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; FPS = 30000 / 1001
SRC = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/screen-recordings/B0544_app-feature-tour-home-macro-tracker-775-cal-ai-trainer-pushu_432x920_10s.mp4'
P = {p['id']: p for p in json.load(open('/Volumes/Expansion/_edit_work/RO-21/round1/plan_r1.json'))}['PH1']
N = int(round((P['b'] - P['a']) * FPS)); OX = 150
raw = subprocess.run([FF.replace('ffmpeg', 'ffmpeg.real'), '-v', 'error', '-i', SRC, '-frames:v', str(N), '-vf', 'scale=in_color_matrix=bt709:in_range=tv,format=rgb24',
                      '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
fr = [Image.frombytes('RGB', (432, 920), raw[i * 432 * 920 * 3:(i + 1) * 432 * 920 * 3]) for i in range(len(raw) // (432 * 920 * 3))]
def base():
    im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size); ImageDraw.Draw(sh).rounded_rectangle((91 + OX, 34, 573 + OX, 1062), 68, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90 + OX, 28, 562 + OX, 1052), 66, fill=(95, 107, 119, 255), outline=(166, 179, 190, 255), width=2)
    d.rounded_rectangle((95 + OX, 33, 557 + OX, 1047), 62, fill=(5, 8, 12, 255))
    for b in ((86, 202, 90, 258), (86, 283, 90, 354), (562, 253, 566, 352)): d.rounded_rectangle((b[0] + OX, b[1], b[2] + OX, b[3]), 2, fill=(69, 81, 94, 255))
    return im
BASE = base(); MASK = Image.new('L', (448, 1000)); ImageDraw.Draw(MASK).rounded_rectangle((0, 0, 447, 999), 54, fill=255)
chip = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); SB.disclosure(chip, 'AI-GENERATED', xy=(OX + 500, 975))   # beside the phone, inside the frame
enc = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', '1920x1080', '-r', '30000/1001', '-i', '-',
                        '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '/Volumes/Expansion/_edit_work/RO-21/round1/hf/phone/PH1.mov'],
                       stdin=subprocess.PIPE)
for i in range(N):
    t = i / FPS; im = BASE.copy()
    p = ImageOps.contain(fr[min(i, len(fr) - 1)], (432, 920)); scr = Image.new('RGB', (448, 1000), p.getpixel((5, 5)))
    scr.paste(p, ((448 - p.width) // 2, 65)); im.paste(scr, (102 + OX, 40), MASK)
    im = Image.alpha_composite(im, chip)
    rise = min(1, t / 0.4); ease = 1 - (1 - rise) ** 3
    out_a = min(1, max(0, (N / FPS - t) / 0.3))
    dy = int(round((1 - ease) * 60 + 6 * np.sin(t * 0.9)))           # rise in, then a slow drift for its whole time on screen
    a = np.asarray(im).copy(); a[..., 3] = (a[..., 3].astype(np.float32) * ease * out_a).astype(np.uint8)
    a = np.roll(a, dy, axis=0)
    enc.stdin.write(a.tobytes())
enc.stdin.close(); assert enc.wait() == 0; print('PH1 done', N, 'frames')
