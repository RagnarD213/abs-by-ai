"""RO-19 round 2: crop both halves of a before / after pair to the SAME body scale (Dan, 2026-10-11: "Apple-to-apple comparison:
same pose in both"). Each photo: person mask -> head top; a landmark row (navel, or the waistband on a side pose) is read off a ruled close-up by eye
(the automatic skin-to-shorts search was fooled by his forearms on the side pose). D = head top to landmark. Crop = 4:5, from KT x D
above the hair to KB x D below the landmark, centred on the body at chest height, so D is the same fraction of both cards of a pair. Writes photos/<out>.jpg.
usage: photocrop.py   (edits nothing else; the list is below)"""
import json, numpy as np, colorsys
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro19/photos"
JOBS = {  # out name: (source, landmark row read off a ruled close-up, KT above the hair, KB below the landmark)
 # the landmark is the navel on the front poses and the top of the waistband on the side pose (shorts sit at different heights, the navel does not)
 "pale2_down": ("pale_r2_219", 2065, 0.008, 0.46), "tan2_down": ("tan_247", 2595, 0.008, 0.46),     # pale 219 has 17 px above his hair: both cards use that margin
 "pale2_side": ("pale_r2_214", 3090, 0.06, 0.42), "tan2_side": ("tan_107", 2730, 0.06, 0.42),
 "pale2_hips": ("pale_r2_199", 3360, 0.06, 0.45), "tan2_hips": ("tan_273", 2650, 0.06, 0.45),
 "pale2_single": ("pale_r2_190", 3790, 0.06, 0.45), "tan2_17": ("tan_17", 2950, 0.06, 0.45),
}
def skin(rgb):
    r, g, b = rgb[..., 0]/255., rgb[..., 1]/255., rgb[..., 2]/255.; mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b); d = mx-mn+1e-6
    h = np.where(mx == r, ((g-b)/d) % 6, np.where(mx == g, (b-r)/d+2, (r-g)/d+4))*60; s = d/(mx+1e-6)
    return ((h < 45) | (h > 345)) & (s > 0.15) & (s < 0.85) & (mx > 0.25)
def measure(name, wb=None):
    im = Image.open(f"{W}/src/{name}.jpg").convert("RGB"); a = np.asarray(im); m = np.asarray(Image.open(f"{W}/mask_r2/{name}.mask.png").convert("L").resize(im.size)) > 127
    rows = np.nonzero(m.sum(1) > im.width*0.01)[0]; top = int(rows[0]); H = rows[-1]-top
    if wb is None:
        y = top + int(0.18*H); step = max(1, im.height//1000); run = 0
        while y < rows[-1]:
            xs = np.nonzero(m[y])[0]; cx = int(np.median(xs)); half = max(8, int(0.10*(xs[-1]-xs[0])))
            sk = skin(a[y, cx-half:cx+half].astype(np.float32)).mean()
            run = run+1 if sk < 0.35 else 0
            if run*step >= 0.03*im.height: wb = y - run*step; break
            y += step
    assert wb, name
    D = wb - top; yc = top + int(0.45*D); xs = np.nonzero(m[yc])[0]; cx = float(np.median(xs))
    return im, top, wb, D, cx
if __name__ == "__main__":
    out = {}
    for o, (src, wb, KT, KB) in JOBS.items():
        im, top, wb, D, cx = measure(src, wb); h = (1+KT+KB)*D; w = 0.8*h; y0 = top-KT*D; x0 = cx - w/2
        x0 = min(max(0, x0), im.width-w); y0 = max(0, y0); assert y0+h <= im.height+1 and w <= im.width, (o, y0+h, im.height, w, im.width)
        c = im.crop((int(x0), int(y0), int(x0+w), int(y0+h))).resize((1200, 1500), Image.LANCZOS); c.save(f"{W}/{o}.jpg", quality=93)
        out[o] = dict(src=src, head_top=top, landmark=int(wb), D=int(D), cx=int(cx), crop=[int(x0), int(y0), int(w), int(h)]); print(o, out[o], flush=True)
    json.dump(out, open(f"{W}/crops_r2.json", "w"), indent=1)
