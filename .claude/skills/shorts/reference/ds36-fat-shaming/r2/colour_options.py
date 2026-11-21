"""DS-36 R2 colour options on matching frames of the off-the-cuff R1 film (same composite path as assemble.py, only Dan's grade
changes; Bill's clip, B-roll and graphics are untouched).   python3 colour_options.py
  A  Current: the approved Codex R5 warm look (rgb 1.01/1/1.015, sat 1.04, power .97, exposure 1.035, contrast 1.045)
  B  Warmer: more golden skin, a touch more colour
  C  Brighter: lifted and cleaner, softer contrast
  D  Punchier: deeper contrast, richer colour
Writes /Volumes/Expansion/_edit_work/DS-36/r2/colour/<look>_<frame>.jpg"""
import sys, numpy as np, cv2
from pathlib import Path
sys.argv = [sys.argv[0], 'offcuff']
sys.path.insert(0, str(Path(__file__).resolve().parent)); import assemble as AS
OUT = Path('/Volumes/Expansion/_edit_work/DS-36/r2/colour'); OUT.mkdir(parents=True, exist_ok=True)
LOOKS = {'A': dict(rgb=[1.01, 1.0, 1.015], sat=1.04, pw=.97, exp=1.035, con=1.045),
         'B': dict(rgb=[1.045, 1.0, 0.965], sat=1.10, pw=.97, exp=1.04, con=1.06),
         'C': dict(rgb=[1.01, 1.0, 1.0], sat=1.02, pw=.92, exp=1.07, con=1.02),
         'D': dict(rgb=[1.025, 1.0, 0.99], sat=1.10, pw=1.0, exp=1.03, con=1.13)}
def make(L):
    def g(x):
        x = x*np.array(L['rgb'], np.float32); y = np.sum(x*np.array([.2126, .7152, .0722], np.float32), -1, keepdims=True)
        x = y + L['sat']*(x - y); x = np.maximum(x, 0)**L['pw']*L['exp']; x = (x - .18)*L['con'] + .18
        return np.clip(x, 0, 1)
    return g
FRAMES = {'watching': 8.0, 'reply': 17.2, 'wide': 27.0, 'tight': 34.0}
for k, L in LOOKS.items():
    AS.grade_r5_warm = make(L)
    for name, t in FRAMES.items():
        g = AS.fr(t); f8 = AS.u8(AS.render(g))
        cv2.imwrite(str(OUT/f'{k}_{name}.jpg'), cv2.cvtColor(AS.gfx(f8, g), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    print('look', k, flush=True)
