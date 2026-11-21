import sys, numpy as np
from PIL import Image
# Composite the ORIGINAL hair back inside a feathered ellipse.
# Unlike facecomp, the gain is LUMINANCE-ONLY (one scalar for all 3 channels): a per-channel
# gain would re-import the very colour cast this pass exists to remove.
orig_p, ret_p, out_p = sys.argv[1:4]
fx, fy, frx, fry = map(float, sys.argv[4:8])
ret = Image.open(ret_p).convert('RGB'); W,H = ret.size
orig = Image.open(orig_p).convert('RGB').resize((W,H), Image.LANCZOS)
cx, cy, rx, ry = fx*W, fy*H, frx*W, fry*H
yy, xx = np.mgrid[0:H, 0:W]
d = np.sqrt(((xx-cx)/rx)**2 + ((yy-cy)/ry)**2)
t = np.clip((1.30-d)/(1.30-0.85), 0, 1); mask = t*t*(3-2*t)
o = np.asarray(orig).astype(np.float64); f = np.asarray(ret).astype(np.float64)
core = d < 0.85
g = float(np.clip(f[core].mean()/max(o[core].mean(),1e-6), 0.85, 1.18))
o = o*g
out = o*mask[...,None] + f*(1-mask[...,None])
def rb(v): return v[0]-(v[1]+v[2])/2
print(f"lum gain {g:.3f}  core R-bias orig {rb(o[core].mean(axis=0)):+.1f} ret {rb(f[core].mean(axis=0)):+.1f}"
      f"  touched={float((mask>0.02).mean()*100):.2f}%")
Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(out_p, quality=97)
