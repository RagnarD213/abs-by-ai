"""Motion-compensated edge flicker: the boiling the eye sees, with Dan's real movement taken out.

    python3 mcflicker.py PALE.mp4 OUT.json

Same alpha proxies as the R1 reviewer (output: distance from the pale backdrop; source: green excess), same edge band.
Difference: the previous frame is first warped onto the current one with optical flow measured on the SOURCE picture
(DIS, forward/backward checked; pixels whose flow does not round-trip within 0.5 px are left out). What is left is
noise and flicker, not motion. Ratio below 1.0 = the key's edges are steadier than the camera's own picture.
"""
import numpy as np, subprocess, json, sys, os, cv2
from scipy import ndimage as ndi
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4"
W, H = 1080, 1920; OY = 176
VF = "scale=in_color_matrix=bt709:in_range=tv"
HAIR = (slice(470, 680), slice(300, 700))
def reader(args):
    p = subprocess.Popen([FF, "-v", "error"] + args + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
def main(pale, out):
    po = reader(["-i", pale, "-vf", VF])
    ps = reader(["-ss", os.environ.get("T0", "1400.25"), "-i", SRC, "-t", os.environ.get("DUR", "9.35"), "-vf", VF + ":w=1080:h=1920:flags=area"])
    BG = np.array([216, 225, 235], np.int16); st = np.ones((3, 3), bool)
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    yy, xx = np.mgrid[:H, :W].astype(np.float32)
    hairm = np.zeros((H, W), bool); hairm[HAIR] = True
    prev = None; rows = []
    for i, (o8, s0) in enumerate(zip(po, ps)):
        o = o8.astype(np.int16)
        s = np.zeros((H, W, 3), np.int16); s[..., 1] = 200; s[OY:] = s0[:H - OY]
        gs = s[..., 1] - np.maximum(s[..., 0], s[..., 2])
        d = np.abs(o - BG).max(-1)
        band = ndi.binary_dilation(d > 40, st, iterations=3) & ~ndi.binary_erosion(d > 40, st, iterations=3)
        ao = np.clip((d - 8) / 60.0, 0, 1).astype(np.float32); as_ = np.clip((45 - gs) / 45.0, 0, 1).astype(np.float32)
        g = cv2.cvtColor(s.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        if prev is not None:
            pao, pas, pg = prev
            f = dis.calc(g, pg, None); b = dis.calc(pg, g, None)
            mx, my = xx + f[..., 0], yy + f[..., 1]
            wb = cv2.remap(b, mx, my, cv2.INTER_LINEAR)
            ok = np.linalg.norm(f + wb, axis=2) < 0.5
            m = band & ok; mh = m & hairm
            wo = cv2.remap(pao, mx, my, cv2.INTER_LINEAR); ws = cv2.remap(pas, mx, my, cv2.INTER_LINEAR)
            do = np.abs(ao - wo); ds = np.abs(as_ - ws)
            rows.append(dict(i=i, n=int(m.sum()), out=float(do[m].mean()), src=float(ds[m].mean()),
                             hn=int(mh.sum()), hout=float(do[mh].mean()) if mh.any() else 0, hsrc=float(ds[mh].mean()) if mh.any() else 0))
        prev = (ao, as_, g)
    o_ = np.array([r['out'] for r in rows]); s_ = np.array([r['src'] for r in rows])
    ho = np.array([r['hout'] for r in rows]); hs = np.array([r['hsrc'] for r in rows])
    summ = dict(mc_ratio=round(float(o_.mean() / s_.mean()), 3), mc_ratio_worst=round(float((o_ / np.maximum(s_, 1e-6)).max()), 3),
                mc_hair_ratio=round(float(ho.mean() / hs.mean()), 3), mc_hair_ratio_worst=round(float((ho / np.maximum(hs, 1e-6)).max()), 3),
                mc_out=round(float(o_.mean()), 4), mc_src=round(float(s_.mean()), 4), mc_hair_out=round(float(ho.mean()), 4), mc_hair_src=round(float(hs.mean()), 4))
    json.dump(dict(summary=summ, frames=rows), open(out, "w"), indent=0); print(json.dumps(summ))
if __name__ == "__main__":
    main(*sys.argv[1:3])
