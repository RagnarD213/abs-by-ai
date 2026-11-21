import sys, numpy as np
from PIL import Image, ImageFilter
# Blend two renders with SEPARATE low- and high-band weights.
# wl controls groove/shadow depth (the "how shredded" dial); wh controls skin texture and
# fine detail such as surface veins. Averaging the high band costs sharpness, so report it.
# usage: freqblend2.py A B OUT WL WH [RADIUS]
a_p,b_p,out_p = sys.argv[1:4]
wl=float(sys.argv[4]); wh=float(sys.argv[5]); R=float(sys.argv[6]) if len(sys.argv)>6 else 30.0
A=Image.open(a_p).convert('RGB'); B=Image.open(b_p).convert('RGB').resize(A.size,Image.LANCZOS)
a=np.asarray(A).astype(np.float64); b=np.asarray(B).astype(np.float64)
loA=np.asarray(A.filter(ImageFilter.GaussianBlur(R))).astype(np.float64)
loB=np.asarray(B.filter(ImageFilter.GaussianBlur(R))).astype(np.float64)
out=np.clip((1-wl)*loA + wl*loB + (1-wh)*(a-loA) + wh*(b-loB), 0, 255)
def sharp(x):
    g=np.asarray(Image.fromarray(np.clip(x,0,255).astype(np.uint8)).convert('L')).astype(np.float64)
    return np.abs(np.diff(g,axis=0)).mean()+np.abs(np.diff(g,axis=1)).mean()
sa,sb,so=sharp(a),sharp(b),sharp(out)
print(f"wl={wl} wh={wh}  sharpness A {sa:.2f} B {sb:.2f} OUT {so:.2f} (vs max parent {so/max(sa,sb):.3f})")
Image.fromarray(out.astype(np.uint8)).save(out_p,quality=97)
