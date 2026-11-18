"""SL-36 R2 colour options: the same talking frames of each Short in L1 (parent look), L2 (warmer, richer), L3 (brighter, crisper),
title band and captions as they render. Writes review/media/look_<S>_<n>_<L>.jpg and prints median luma / saturation of Dan's picture."""
import sys, json, numpy as np, cv2
sys.path.insert(0, "recipe")
import batch as Bt; Bt.cv2 = cv2
from PIL import Image
PICK = {"A": [1.0 + 3.2, 40.0], "B": [6.0, 38.0], "C": [12.0, 28.0]}      # output seconds: one wide (W2) and one close (T2) talking frame per Short
out = {}
for S, ts in PICK.items():
    s = Bt.Short(S)
    for n, t in enumerate(ts):
        i = int(round(t * Bt.FPS))
        for L in ("L1", "L2", "L3"):
            Bt.LOOK = L
            f, sh = s.picture(i); assert sh["kind"] == "talk", (S, t, sh["kind"])
            f = s.finish(f, sh, i)
            Image.fromarray(f).save(f"review/media/look_{S}_{n}_{L}.jpg", quality=90)
            pic = f[310:1400].astype(np.float32) / 255; hsv = cv2.cvtColor((pic * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
            y = 0.2126 * pic[..., 0] + 0.7152 * pic[..., 1] + 0.0722 * pic[..., 2]
            out[f"{S}{n}{L}"] = dict(luma=round(float(np.median(y)) * 255, 1), sat=round(float(np.median(hsv[..., 1])) / 255, 3), black=round(float((y < 16 / 255).mean()), 3))
    s.close()
json.dump(out, open("review/media/looks.json", "w"), indent=1); print(json.dumps(out))
