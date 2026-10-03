"""RO-02 grade: bake the approved poolside colour (Codex organic colour v1: per-channel LUT -> fitted matrix -> tone
curve, all pointwise) into 3D .cube files so ffmpeg lut3d applies it. One cube per (calibration roll, tone strength)."""
import json, sys, numpy as np
T = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/codex-video-trial/templates/youtube-organic-color-v1"
W = "/Volumes/Extreme/_edit_work/ro02"
L = {k: np.array(v, np.float32) for k, v in json.load(open(f"{T}/grade-proposed.json")).items()}
CM = {k: np.array(v, np.float32) for k, v in json.load(open(f"{T}/grade-matrices.json")).items()}
def tone(x, strength):
    y = x @ np.array([.2126, .7152, .0722], np.float32)
    ys = y - .075*strength*np.sin(np.pi*y)*np.cos(np.pi*y)
    z = x*(ys/np.maximum(y, 1e-5))[..., None]
    hi = x.max(-1); lo = x.min(-1); sat = (hi-lo)/np.maximum(hi, 1e-5)
    skin = np.clip((x[..., 0]-x[..., 2]-.045)/.12, 0, 1)*np.clip((x[..., 1]-x[..., 2]-.025)/.09, 0, 1)*np.clip((sat-.12)/.12, 0, 1)
    lum = z @ np.array([.2126, .7152, .0722], np.float32); boost = 1+.045*strength+.015*strength*skin
    z = lum[..., None]+(z-lum[..., None])*boost[..., None]
    z[..., 0] += .006*strength*skin; z[..., 1] -= .005*strength*skin; z[..., 2] -= .002*strength*skin
    w = np.clip((.99-y)/.12, 0, 1)
    return np.clip(x+(z-x)*w[..., None], 0, 1)
def grade(x, roll, strength):
    """x float RGB 0..1 (BT.709-decoded 8-bit domain)."""
    l = L[roll]; idx = np.clip(x*255, 0, 255); i0 = np.floor(idx).astype(int); i1 = np.minimum(i0+1, 255); f = idx-i0
    g = np.stack([l[i0[..., c], c]*(1-f[..., c])+l[i1[..., c], c]*f[..., c] for c in range(3)], -1)/255
    m = CM[roll]; g = np.clip(g @ m[:3]+m[3], 0, 1)
    g = np.round(g*255)/255 if False else g
    return tone(g.astype(np.float32), strength) if strength > 0 else g
def cube(roll, strength, path, n=65, pre_gamma=1.0):
    r = np.linspace(0, 1, n, dtype=np.float32)
    B, G, R = np.meshgrid(r, r, r, indexing="ij")          # .cube: R fastest
    x = np.stack([R, G, B], -1).reshape(-1, 3)
    if pre_gamma != 1.0: x = np.power(x, pre_gamma).astype(np.float32)      # per-shot exposure trim, before the approved grade
    out = grade(x, roll, strength)
    with open(path, "w") as f:
        f.write(f"LUT_3D_SIZE {n}\n")
        for p in out: f.write("%.6f %.6f %.6f\n" % tuple(p))
if __name__ == "__main__":
    for name, roll, s in [("A-c1630-s100", "C1630", 1.0), ("B-c1631-s080", "C1631", 0.8), ("C-c1630-s065", "C1630", 0.65)]:
        cube(roll, s, f"{W}/look/{name}.cube"); print("wrote", name)
