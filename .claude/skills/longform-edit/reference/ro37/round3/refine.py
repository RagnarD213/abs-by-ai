"""RO-37 round 3 key: the BiRefNet matte (3-frame median) becomes a trimap, ViTMatte small (local, on the Mac's GPU) solves the
edge band on the colour-F frame at 1152x2048. Stored per roll frame at round3/matte2/<roll>/<frame>.png, resumes by skipping
existing files. The trimap's unknown band runs further into the hair than out into the hedge (the base model and a wider band
took dark hedge for hair at 0:11).
  python3 refine.py 9.5:12,18.5:21        film seconds, or "all"
"""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2, torch, r2
from PIL import Image
from transformers import VitMatteImageProcessor, VitMatteForImageMatting
M3 = os.environ.get("M3DIR", r2.M3); dev = "mps"; MODEL = f"hustvl/vitmatte-{os.environ.get('VM', 'small')}-composition-1k"; CW, CH = 1120, 2016


def trimap(a, r_fg=12, r_bg=4, head_fg=16, head_bg=8):
    """BiRefNet's edge sits a few px outside his real skin edge, so the unknown band runs well inside it and only a little
    outside it: a band too narrow inside keeps the bright wall as a white line; one too wide outside takes the hedge for hair."""
    h, w = a.shape; fg = (a > 0.92).astype(np.uint8); bg = (a < 0.08).astype(np.uint8)
    ys = np.where(a.max(1) > 0.5)[0]; top = ys[0] if len(ys) else 0; headend = top + int(h * 0.13)
    e = lambda m, r: cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
    F = e(fg, r_fg); B = e(bg, r_bg)
    F[:headend] = e(fg, head_fg)[:headend]; B[:headend] = e(bg, head_bg)[:headend]
    t = np.full((h, w), 128, np.uint8); t[F > 0] = 255; t[B > 0] = 0
    return t


def trimap_pair(a, b):
    t = trimap(np.minimum(a, b)); u = trimap(np.maximum(a, b))     # fg must be sure in both, bg must be sure in both
    o = np.full(a.shape, 128, np.uint8); o[t == 255] = 255; o[u == 0] = 0
    return o


def runs(ks):
    out, cur = [], []
    for k in ks:
        if cur and k != cur[-1] + 1: out.append(cur); cur = []
        cur.append(k)
    if cur: out.append(cur)
    return out


def main():
    spec = sys.argv[1]
    rng = [(0, r2.END_F / r2.FPS)] if spec == "all" else [tuple(float(x) for x in r.split(":")) for r in spec.split(",")]
    shots = r2.shots2(); need = {}
    for a, b in rng:
        for roll, ks in r2.needed_frames(r2.fr(a), r2.fr(b), shots).items(): need.setdefault(roll, set()).update(ks)
    n = sum(1 for r, ks in need.items() for k in ks if not os.path.exists(f"{M3}/{r}/{k:06d}.png")); print(n, "frames to refine", flush=True)
    proc = VitMatteImageProcessor.from_pretrained(MODEL); net = VitMatteForImageMatting.from_pretrained(MODEL).to(dev).eval()
    t0 = time.time(); done = 0
    for roll in need:
        os.makedirs(f"{M3}/{roll}", exist_ok=True)
        for run in runs(sorted(need[roll])):
            if all(os.path.exists(f"{M3}/{roll}/{k:06d}.png") for k in run): continue
            p = subprocess.Popen([r2.FF, "-nostdin", "-v", "error", "-ss", f"{(run[0] - 0.5) / r2.FPS:.6f}", "-i", r2.F.ROLLS[roll], "-frames:v", str(len(run)), "-fps_mode", "passthrough", "-vf",
                                  f"{r2.F.DEC},{r2.F.GRADES['F'][1]},scale={r2.MW}:{r2.MH}:flags=lanczos:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24",
                                  "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
            for k in run:
                raw = p.stdout.read(r2.MW * r2.MH * 3); out = f"{M3}/{roll}/{k:06d}.png"
                if os.path.exists(out) or not os.path.exists(r2.mpath(roll, k)): continue
                rgb = np.frombuffer(raw, np.uint8).reshape(r2.MH, r2.MW, 3)
                a = r2.alpha_birefnet(roll, k, run[0], run[-1])
                if os.path.exists(r2.mpath(roll, k + 1)):
                    # some BiRefNet runs were decoded one frame late (ffmpeg doubles the first frame after certain seeks unless
                    # -fps_mode passthrough), so label k may be frame k-1: the trimap spans labels k and k+1, the solve uses the true frame
                    b = np.asarray(Image.open(r2.mpath(roll, k + 1)), np.float32) * (1 / 255)
                    tri = trimap_pair(a, b)
                else: tri = trimap(a)
                ys, xs = np.where(tri > 0)
                if not len(ys): Image.fromarray(np.zeros_like(tri)).save(out); continue
                # one fixed crop size: the GPU rebuilds its whole graph on any new shape (10+ s a frame)
                x0 = int(np.clip((xs.min() + xs.max()) // 2 - CW // 2, 0, r2.MW - CW)); x1 = x0 + CW; y0, y1 = r2.MH - CH, r2.MH
                c, tc = rgb[y0:y1, x0:x1], tri[y0:y1, x0:x1]
                inp = proc(images=Image.fromarray(c), trimaps=Image.fromarray(tc), return_tensors="pt").to(dev)
                with torch.no_grad(): al = net(**inp).alphas[0, 0].cpu().numpy()[:c.shape[0], :c.shape[1]]
                A = a.copy(); A[y0:y1, x0:x1] = al; A[tri == 255] = 1; A[tri == 0] = 0
                Image.fromarray((A * 255 + 0.5).astype(np.uint8)).save(out + ".tmp.png"); os.replace(out + ".tmp.png", out)
                done += 1
                if done % 100 == 0: print(f"  {done}/{n}, {done / (time.time() - t0):.2f}/s", flush=True)
            p.stdout.close(); p.wait()
    print("refine done", done, round(time.time() - t0), "s", flush=True)
main()
