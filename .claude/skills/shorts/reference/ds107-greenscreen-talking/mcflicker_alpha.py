"""DS-107: the house-key flicker measure (ds44_mcflicker.py method: DIS optical flow from the source, forward/backward consistency,
edge band, motion-compensated frame-to-frame alpha change, output vs source) read on the key's ACTUAL finished alpha (assemble.key_frame:
stage 1.5 cache + stage 2 despeckle/haze) instead of an alpha re-estimated from a composite. Why: on C1908 Dan wears an off-white tank
(15-30 levels from the pale check backdrop) and has dark hair (low contrast on navy), so the composite-based estimate measures the
wardrobe, not the key. Geometry: cache 0.75 of the source, both taken to 0.5 (1080 x 1920 output of the source).
    python3 mcflicker_alpha.py T0 N OUT.json"""
import numpy as np, subprocess, json, sys, cv2, os
from scipy import ndimage as ndi
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); T0, N, OUT = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; sys.argv = [sys.argv[0]]
import assemble as AS
SRC = "/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1908.MP4"; W, H = 1080, 1920
HAIR = (slice(463 - 20, 463 + 100), slice(430, 700))     # cache hair top 694 x 0.667; the hair band above the glasses
p = subprocess.Popen([AS.F, "-v", "error", "-ss", f"{T0:.3f}", "-i", SRC, "-frames:v", str(N), "-fps_mode", "passthrough",
                      "-vf", "scale=in_color_matrix=bt709:in_range=tv:w=1080:h=1920:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM); yy, xx = np.mgrid[:H, :W].astype(np.float32)
hairm = np.zeros((H, W), bool); hairm[HAIR] = True; prev = None; rows = []
for i in range(N):
    b = p.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    s = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.int16)
    gs = s[..., 1] - np.maximum(s[..., 0], s[..., 2]); as_ = np.clip((45 - gs)/45.0, 0, 1).astype(np.float32)
    _, a = AS.key_frame(T0 + i/AS.FPS); ao = cv2.resize(a.astype(np.float32), (W, H), interpolation=cv2.INTER_AREA)   # 1620x2880 -> 1080x1920
    band = ndi.binary_dilation((ao > 0.05) & (ao < 0.95), iterations=3) | (ndi.binary_dilation(ao > 0.5, iterations=3) & ~ndi.binary_erosion(ao > 0.5, iterations=3))
    g = cv2.cvtColor(s.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    if prev is not None:
        pao, pas, pg = prev
        f = dis.calc(g, pg, None); bb = dis.calc(pg, g, None); mx, my = xx + f[..., 0], yy + f[..., 1]
        ok = np.linalg.norm(f + cv2.remap(bb, mx, my, cv2.INTER_LINEAR), axis=2) < 0.5
        m = band & ok; mh = m & hairm
        do = np.abs(ao - cv2.remap(pao, mx, my, cv2.INTER_LINEAR)); ds = np.abs(as_ - cv2.remap(pas, mx, my, cv2.INTER_LINEAR))
        rows.append(dict(i=i, n=int(m.sum()), out=float(do[m].mean()), src=float(ds[m].mean()), hn=int(mh.sum()),
                         hout=float(do[mh].mean()) if mh.any() else 0.0, hsrc=float(ds[mh].mean()) if mh.any() else 0.0))
    prev = (ao, as_, g)
p.stdout.close(); p.wait()
o_ = np.array([r['out'] for r in rows]); s_ = np.array([r['src'] for r in rows]); ho = np.array([r['hout'] for r in rows]); hs = np.array([r['hsrc'] for r in rows])
summ = dict(frames=len(rows), mc_ratio=round(float(o_.mean()/s_.mean()), 3), mc_ratio_p90=round(float(np.percentile(o_/np.maximum(s_, 1e-6), 90)), 3),
            mc_hair_ratio=round(float(ho.mean()/max(hs.mean(), 1e-6)), 3), mc_out=round(float(o_.mean()), 4), mc_src=round(float(s_.mean()), 4),
            mc_hair_out=round(float(ho.mean()), 4), mc_hair_src=round(float(hs.mean()), 4))
json.dump(dict(summary=summ, frames=rows), open(OUT, 'w'), indent=0); print(json.dumps(summ))
