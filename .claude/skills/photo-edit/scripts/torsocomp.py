import sys, numpy as np
from PIL import Image, ImageFilter
# Composite the TORSO of a harder render into an accepted frame whose arms/face are correct.
# Used when a re-roll gives the abs you want but re-inflates a limb: the fault is spatially
# confined, so take only the region you asked for.
# usage: torsocomp.py BASE SRC OUT X0 Y0 X1 Y1 FEATHER
base_p, src_p, out_p = sys.argv[1:4]
x0,y0,x1,y1,fe = (int(v) for v in sys.argv[4:9])
B = Image.open(base_p).convert('RGB'); S = Image.open(src_p).convert('RGB').resize(B.size, Image.LANCZOS)
W,H = B.size
m = Image.new('L',(W,H),0); 
import PIL.ImageDraw as D
D.Draw(m).rectangle([x0,y0,x1,y1], fill=255)
m = m.filter(ImageFilter.GaussianBlur(fe))
mn = np.asarray(m).astype(np.float64)/255.0
b = np.asarray(B).astype(np.float64); s = np.asarray(S).astype(np.float64)
ring = (mn>0.10)&(mn<0.55)
if ring.sum()>500:
    for c in range(3):
        g = float(np.clip(b[...,c][ring].mean()/max(s[...,c][ring].mean(),1e-6),0.90,1.11))
        s[...,c] *= g
        print(f"  ring gain c{c} {g:.4f}")
out = s*mn[...,None] + b*(1-mn[...,None])
Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(out_p, quality=97)
print("torso composited ->", out_p, f"mask>0.02 = {float((mn>0.02).mean()*100):.2f}% of frame")
