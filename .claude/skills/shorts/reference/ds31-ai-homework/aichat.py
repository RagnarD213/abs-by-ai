"""Full-screen 'AI writes the essay' chat screen for "Use AI to do it instead" (R1 audit: stock showed no AI).
Generic assistant UI in the Soft Blue palette, no brand. Prompt types in, the essay streams in. -> stock/aichat.mp4"""
from pathlib import Path
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R/'.claude/skills/_shared')); import softblue as B
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; N = 120
PROMPT = 'Write my 1,500-word essay on the causes of World War I'
ESSAY = ('The First World War did not begin with a single shot. It grew out of decades of rivalry between the great powers of Europe. '
         'Three forces made war almost certain by 1914: a tangle of military alliances, an arms race on land and sea, and nationalism '
         'that turned every border dispute into a matter of pride. When Archduke Franz Ferdinand was assassinated in Sarajevo, '
         'those forces pulled one nation after another into the conflict.')
BG = (13, 19, 27); PANEL = (24, 33, 44); USER = (40, 92, 130); WHITE = (238, 244, 250); MUT = (150, 168, 188)
def frame(n):
    t = n/FPS; im = Image.new('RGB', (1080, 1920), BG); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1080, 170), fill=PANEL); d.ellipse((60, 60, 110, 110), fill=B.CYAN); B.text(im, (130, 62), 'AI assistant', 40)
    f = B.font(44); typed = PROMPT[:int(min(1, t/0.55)*len(PROMPT))]
    lines = B.wrap(typed or ' ', f, 760); h = 40 + 62*len(lines)
    d.rounded_rectangle((220, 230, 1020, 230 + h), radius=28, fill=USER)
    for i, l in enumerate(lines): B.text(im, (250, 250 + i*62), l, 44)
    y = 230 + h + 60
    if t > 0.65:
        d.ellipse((60, y, 110, y + 50), fill=B.CYAN)
        shown = ESSAY[:int(min(1, (t - 0.65)/1.2)*len(ESSAY))]
        fe = B.font(42, bold=False)
        for i, l in enumerate(B.wrap(shown, fe, 880)):
            B.text(im, (140, y + i*60), l, 42, bold=False)
        if int(t*3) % 2 == 0: d.rectangle((140, y + 60*len(B.wrap(shown or ' ', fe, 880)) + 6, 166, y + 60*len(B.wrap(shown or ' ', fe, 880)) + 52), fill=B.CYAN)
    d.rounded_rectangle((60, 1700, 1020, 1810), radius=40, fill=PANEL); B.text(im, (100, 1733), 'Message AI...', 38, MUT, bold=False)
    return np.asarray(im)
out = W/'stock/aichat.mp4'
p = subprocess.Popen([F, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-framerate', '30000/1001', '-i', '-',
                      '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '16', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', str(out)], stdin=subprocess.PIPE)
for n in range(N): p.stdin.write(np.ascontiguousarray(frame(n)).tobytes())
p.stdin.close(); assert p.wait() == 0
Image.fromarray(frame(54)).save(W/'work/aichat_last.jpg'); print('AICHAT', out)
