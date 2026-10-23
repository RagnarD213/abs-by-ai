#!/usr/bin/env python3
"""Export the small keyed Dan from the approved DS-44 R2 opening as an RGBA PNG, for the split-screen cover (Dan, 2026-10-23:
"add me back into the corner like I appear in the video"). Same key cleanup, right/top edge fade and B_warmvivid grade as
r2/recipe/assemble.py, at the film's corner scale (0.2667 of the 0.75 key cache). usage: corner_dan.py FILM_FRAME OUT.png | corner_dan.py --piece A 394 OUT.png (a keyed talking frame, looking at camera)"""
import json, sys
from pathlib import Path
import numpy as np, cv2
from scipy import ndimage as ndi
from PIL import Image
W = Path('/Volumes/Expansion/_edit_work/DS-44/r2'); sys.path.insert(0, str(W/'recipe'))
from grade import grade, LOOKS
FPS = 30000/1001
edl = json.load(open(W/'edl.json')); shots = json.load(open(W/'shots.json'))
if sys.argv[1] == '--piece':
    piece, i, out = sys.argv[2], int(sys.argv[3]), sys.argv[4]; g = None
else:
    g = int(sys.argv[1]); out = sys.argv[2]; piece = 'watchF'
    seg = next(x for x in edl['clip']['segs'] if x['n0'] <= g < x['n0'] + x['frames'])
    tc = seg['clip_in'] + (g - seg['n0'])/FPS; RMC = edl['clip']['roll_minus_clip']
    i = int(round((tc + RMC - 2192.30)*FPS))
d = np.load(W/'key'/f'c2_{piece}'/f'f{i:04d}.npy').astype(np.float32); Fp, a = d[..., :3], d[..., 3]
lab, n = ndi.label(a > 0.03)
if n:
    sizes = ndi.sum(np.ones_like(a), lab, index=np.arange(1, n + 1)); keep = np.zeros(n + 1, bool); keep[1:] = sizes >= 900
    m = ndi.binary_dilation(keep[lab], iterations=4); a = np.where(m, a, 0); Fp = np.where(m[..., None], Fp, 0)
far = ndi.distance_transform_edt(a < 0.25) > 4.5
a2 = np.where(far, np.clip((a - 0.15)/0.85, 0, 1), a); Fp = Fp*np.where(a > 1e-4, a2/np.maximum(a, 1e-4), 0)[..., None]; a = a2
h, w = a.shape
rx = np.clip((w - 1 - np.arange(w, dtype=np.float32))/54, 0, 1); ry = np.clip(np.arange(h, dtype=np.float32)/180, 0, 1)
ramp = rx[None, :]*ry[:, None]; Fp, a = Fp*ramp[..., None], a*ramp
s = next(x for x in shots if x['id'] == 'S0')['corner']['scale']
tw, th = int(round(w*s)), int(round(h*s))
Fr = cv2.resize(Fp, (tw, th), interpolation=cv2.INTER_AREA); ar = np.clip(cv2.resize(a, (tw, th), interpolation=cv2.INTER_AREA), 0, 1)
G = np.where(ar[..., None] > 0.01, np.clip(Fr, 0, None)/np.maximum(ar[..., None], 1e-3), 0)
G = grade(np.clip(G, 0, 1), **LOOKS['B_warmvivid'])
rgba = np.dstack([np.clip(G, 0, 1), ar])
Image.fromarray((rgba*255 + 0.5).astype(np.uint8)).save(out)
print(out, tw, th, 'piece', piece, 'film frame', g, 'key frame', i)
