"""Finish a stage 1.5 cache into the plate the RO-24 assembler reads: the approved stage 2 despeckle and haze clip (stage2_comp.py
comp_frame, unchanged rules), unpremultiply, FFV1 gbrap16le 2880x1620 colour + alpha, and <out>.json with f0 and per-frame head
geometry (same fields as round 1's key16: [k, hair_top, cx, x0, x1] in 2880 px).
    python3 write16.py CACHE F0 OUT.mkv [X0]   (X0 = the 4K box left edge when the cache holds only the box)"""
import numpy as np, sys, glob, json, subprocess, time
from scipy import ndimage as ndi
from common16 import FF, OW, OH, SRC
MIN_FRAG = 400
import os
ISL_T = float(os.environ.get('ISL_T', '0.12')); ISL_MAX = int(os.environ.get('ISL_MAX', '600'))   # px at 2880 scale
CACHE, F0, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
OX = int(sys.argv[4]) * 3 // 4 if len(sys.argv) > 4 else 0
edge_hits = []
files = sorted(glob.glob(f"{CACHE}/f*.npy")); assert len(files) > 200, len(files)
enc = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-s', f'{OW}x{OH}', '-r', '30000/1001', '-i', '-',
                        '-an', '-c:v', 'ffv1', '-level', '3', '-slices', '16', '-threads', '4', '-pix_fmt', 'gbrap16le', OUT], stdin=subprocess.PIPE)
geo = []; t = time.time()
for k, fn in enumerate(files):
    d = np.load(fn).astype(np.float32)
    if d.shape[1] != OW:                       # box cache: paste into the full canvas (screen outside the box)
        BW = d.shape[1]; full = np.zeros((OH, OW, 4), np.float32); full[:, OX:OX + BW] = d; d = full
    else: BW = OW
    Fp, a = d[..., :3], d[..., 3]
    lab, n = ndi.label(a > 0.03)
    if n:
        sizes = ndi.sum(np.ones_like(a), lab, index=np.arange(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= MIN_FRAG
        m = ndi.binary_dilation(keep[lab], iterations=3); a = np.where(m, a, 0); Fp = np.where(m[..., None], Fp, 0)
    # round 2 (RO-24, fast hands): the approved island rule extended to the faint band. A small component of alpha > ISL_T that does not
    # reach Dan's solid body (alpha > 0.5) is a speck: the edge-colour fill paints it skin-pink, so it reads as a floating dot beside a
    # fast arm (checks/keys/specks_R04a.jpg). Every real part of Dan (blurred fingers, glasses arm, hair) is one piece with his body above
    # ISL_T; a small piece apart from that biggest piece is a speck, even with a solid core (the arm's moving shadow on the screen).
    if ISL_T:
        lab2, n2 = ndi.label(a > ISL_T)
        if n2:
            sz = ndi.sum(np.ones_like(a), lab2, index=np.arange(1, n2 + 1))
            kill = np.zeros(n2 + 1, bool); kill[1:] = sz < ISL_MAX; kill[1 + int(np.argmax(sz))] = False   # Dan is the one big piece
            km = kill[lab2]
            if km.any(): a = np.where(km, 0, a); Fp = np.where(km[..., None], 0, Fp)
    far = ndi.distance_transform_edt(a < 0.25) > 3
    a_new = np.where(far, np.clip((a - 0.15) / 0.85, 0, 1), a)
    Fp = Fp * np.where(a > 1e-4, a_new / np.maximum(a, 1e-4), 0)[..., None]; a = a_new
    if BW < OW and ((OX > 0 and a[:, OX].max() > .3) or (OX + BW < OW and a[:, OX + BW - 1].max() > .3)): edge_hits.append(k)   # Dan reaches the box edge
    F = np.where(a[..., None] > 1e-4, np.clip(Fp / np.maximum(a[..., None], 1e-4), 0, 1), 0)
    enc.stdin.write((np.concatenate([F, a[..., None]], 2) * 65535 + .5).astype('<u2').tobytes())
    rr = np.where((a > .35).sum(1) >= 3)[0]; htop = int(rr[0]) if len(rr) else -1
    band = a[max(htop, 0):max(htop, 0) + 260] > .5; cols = np.where(band.any(0))[0]
    geo.append([k, htop, int((cols[0] + cols[-1]) // 2) if len(cols) else -1, int(cols[0]) if len(cols) else -1, int(cols[-1]) if len(cols) else -1])
    if k % 60 == 0: print(OUT.split('/')[-1], k, len(files), round(time.time() - t), flush=True)
enc.stdin.close(); assert enc.wait() == 0
json.dump({'src': SRC, 'f0': F0, 'frames': len(files), 'method': 'ds40-claude-r2 (house standard 2026-10-21), RO-24 16:9 port', 'geo': geo, 'box_x0_out': OX, 'box_edge_hits': edge_hits},
          open(OUT + '.json', 'w'), indent=1)
print('WRITE DONE', OUT, len(files), round(time.time() - t), 's', 'BOX EDGE TOUCHED on frames', edge_hits[:20] if edge_hits else 'none')
