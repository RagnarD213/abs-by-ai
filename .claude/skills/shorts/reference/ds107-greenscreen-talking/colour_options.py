"""DS-107 R1 colour options on Dan (PRE-RENDER-APPROVAL step 2): the same two moments (wide at roll 116.6, close at roll 118.6), each
through the real compositor with only Dan's grade swapped (A r5warm = house, B bright, C clean). Writes review/media/look-<k>-<w|t>.jpg
and a side-by-side sheet with an approved reference frame (DS-41 Kevin James, same green screen set) for comparison."""
import sys, os, json, numpy as np, cv2
from pathlib import Path
W = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.argv = [sys.argv[0]]
import assemble as AS, grade as G
from PIL import Image
out = W/'review'/'media'; out.mkdir(parents=True, exist_ok=True)
moments = {'w': (116.6, 1060), 't': (118.6, 860)}
for key, (t_roll, cw) in moments.items():
    Fp, a = AS.key_frame(t_roll)
    m = a > 0.5; m[:40] = False; ys, xs = np.where(m); top = ys.min(); cx = float(np.median(xs[ys < top + 150]))
    ch = round(cw/AS.CW*1610); y0 = max(0, top - 0.035*ch); x0 = float(np.clip(cx - cw/2, 0, 1620 - cw)); sc = AS.CW/cw
    for lk, fn in G.LOOKS_DAN.items():
        AS.GRADE = fn
        f = AS.place(AS.field(2.0), Fp, a, sc, -x0*sc, AS.DROP - y0*sc)
        f8 = AS.with_band(AS.u8(f), 2.0)
        Image.fromarray(f8).resize((540, 960), Image.LANCZOS).save(out/f'look-{lk}-{key}.jpg', quality=90)
print('LOOKS', sorted(os.listdir(out)))
