"""A Soft Blue Light 9:16 lower third as a STILL on a real frame: the HyperFrames lower-third template laid out by
vertical.py (content + glass mask passes snapped at the settled moment), composited the way composite.py does."""
import sys, pathlib, numpy as np
from PIL import Image
import lib
import vertical as V, hfbuild as Hf, composite as C
SHIFT = 72   # SL-03: the picture sits 310 px lower under the title band, so the strip's bottom moves from 68 % (y1306) to y1378;
              # measured on short 1: Dan's face bottom reaches y1097 in the full window while a bar is up (hair/measure.py)
_box = lib.B.lower_third_default_box
def _shifted(w, h, lines=1):
    x0, y, x1, bh = _box(w, h, lines); return x0, y + SHIFT, x1, bh
def still(bg, gid, topic, parts, a, b, out, at=None):
    V.B.lower_third_default_box = _shifted
    c = dict(id=gid, a=a, b=b, drift=-4, topic=topic, parts=parts)
    scenes, meta = V.lt_scenes(c)
    out = pathlib.Path(out); t = at if at is not None else max(0.5, (b - a) - 0.6)
    res = []
    for tpl, cfg, assets in scenes:
        d = Hf.make_scene(tpl, cfg, out / "proj", assets)
        for old in (d / "snapshots").glob("*.png"):
            try: old.unlink()
            except FileNotFoundError: pass
        shots = [x for x in Hf.snapshot(d, [round(t, 3)]) if not x.name.startswith("._")]
        res.append(np.asarray(Image.open(shots[-1]).convert("RGBA")))
    base = np.asarray(bg.convert("RGB")); content, mask = res
    o = C.over(C.glass(base, mask, meta["band"]), content)
    return Image.fromarray(o), meta
