import sys, numpy as np
from PIL import Image, ImageFilter
# Hit an intensity BETWEEN two renders. Average only the LOW band (where groove/shadow depth
# lives); keep the HIGH band (skin texture) from one parent, or a straight 50/50 pixel blend
# loses 22-27% of local gradient energy and reads plasticky.
# usage: freqblend.py A B OUT W_TOWARD_B HI_FROM(a|b) [RADIUS]
a_p,b_p,out_p = sys.argv[1:4]
w = float(sys.argv[4]); hi = sys.argv[5]; R = float(sys.argv[6]) if len(sys.argv)>6 else 30.0
A = Image.open(a_p).convert('RGB'); B = Image.open(b_p).convert('RGB').resize(A.size, Image.LANCZOS)
a = np.asarray(A).astype(np.float64); b = np.asarray(B).astype(np.float64)
loA = np.asarray(A.filter(ImageFilter.GaussianBlur(R))).astype(np.float64)
loB = np.asarray(B.filter(ImageFilter.GaussianBlur(R))).astype(np.float64)
base, lobase = (a, loA) if hi == 'a' else (b, loB)
out = np.clip((1-w)*loA + w*loB + (base - lobase), 0, 255)
def sharp(x):
    g = np.asarray(Image.fromarray(np.clip(x,0,255).astype(np.uint8)).convert('L')).astype(np.float64)
    return np.abs(np.diff(g,axis=0)).mean() + np.abs(np.diff(g,axis=1)).mean()
sa,sb,so = sharp(a),sharp(b),sharp(out)
print(f"w={w} hi={hi} R={R}  sharpness A {sa:.2f} B {sb:.2f} OUT {so:.2f} "
      f"(ratio vs hi-parent {so/(sa if hi=='a' else sb):.3f})")
Image.fromarray(out.astype(np.uint8)).save(out_p, quality=97)
