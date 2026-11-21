"""SL-17: the RO-26 master's look, measured. raw C1768 + the recipe's grade B (eq ...) reads 4-5 levels brighter/greener than the
delivered master on aligned frames (a later step of the film's pipeline shifted it). Fit one tone curve per channel AFTER grade B
(binned medians of aligned, blurred pixel pairs from 8 frames across all framings), test on 4 held-out frames, write curves.json
and the ffmpeg `curves` filter string."""
import json, subprocess, numpy as np, sys
from PIL import Image, ImageFilter
sys.path.insert(0, "."); import lib
M = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Codex Content Videos/Top 1 Percent - RO-26/Top 1 Percent | codex | 16x9 | RO-26.mp4"
FPS = 30000 / 1001; cuts = json.load(open("ro26_cut_map.json"))["cuts"]
def grab(args):
    b = subprocess.run([lib.FF, "-nostdin", "-v", "error"] + args + ["-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.asarray(Image.frombytes("RGB", (1920, 1080), b).filter(ImageFilter.GaussianBlur(3))).astype(float)
def pair(ft, extra=""):
    c = next(c for c in cuts if c["out_in"] <= ft < c["out_out"]); n = int(round(ft * FPS)); t = n / FPS
    m = grab(["-ss", f"{t:.4f}", "-i", M, "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24"])
    x, y, w, h = c["crop"][0], c["crop"][1], c["crop"][2], c["crop"][3]
    r = grab(["-ss", f"{c['src_in'] + t - c['out_in']:.4f}", "-i", f"{lib.RAWD}/C1768.MP4", "-vf", f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,{lib.GRADE}{extra},scale=in_color_matrix=bt709:in_range=tv,format=rgb24"])
    return r, m
if __name__ == "__main__":
    fit_t = [20.0, 45.0, 60.0, 100.0, 128.0, 175.0, 200.0, 240.0]; test_t = [35.0, 150.0, 230.0, 255.5]
    P = [pair(t) for t in fit_t]; T = [pair(t) for t in test_t]
    pts = []
    for c in range(3):
        x = np.concatenate([r[..., c].ravel() for r, m in P]); y = np.concatenate([m[..., c].ravel() for r, m in P])
        xs, ys = [0.0], [0.0]
        for lo in range(0, 256, 8):
            s = (x >= lo) & (x < lo + 8)
            if s.sum() > 400: xs.append(float(np.median(x[s]))); ys.append(float(np.median(y[s])))
        slope = (ys[-1] - ys[-3]) / max(1e-6, xs[-1] - xs[-3]); end = min(255.0, ys[-1] + slope * (255.0 - xs[-1]))
        xs.append(255.0); ys.append(end)
        ys = list(np.maximum.accumulate(ys)); pts.append((xs, ys))
    def apply(r): return np.stack([np.interp(r[..., c], *pts[c]) for c in range(3)], -1)
    for t, (r, m) in zip(test_t, T): print(f"test film {t}: before {np.abs(r - m).mean():.2f}  after {np.abs(apply(r) - m).mean():.2f}")
    def keep(xs, ys):
        k = [(a, b) for a, b in zip(xs, ys)][::2]
        if k[-1][0] < 255: k.append((xs[-1], ys[-1]))
        out = []
        for a, b in k:
            if not out or a - out[-1][0] > 2: out.append((a, b))
        return out
    flt = "curves=" + ":".join(f"{ch}='" + " ".join(f"{a / 255:.4f}/{b / 255:.4f}" for a, b in keep(*pts[k])) + "'" for k, ch in enumerate(("r", "g", "b")))
    json.dump(dict(points=pts, filter=flt), open("curves.json", "w"), indent=0); print(flt)
