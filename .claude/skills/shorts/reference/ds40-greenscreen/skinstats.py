import numpy as np, sys, colorsys
from PIL import Image
def stats(rgb, mask=None):
    r,g,b = rgb[...,0],rgb[...,1],rgb[...,2]
    Y = 0.2126*r+0.7152*g+0.0722*b
    Cb = (b-Y)/1.8556; Cr=(r-Y)/1.5748
    sk = (Cr>0.03)&(Cr<0.16)&(Cb>-0.12)&(Cb<0.0)&(Y>0.15)&(Y<0.9)&(r>g)&(g>b)
    if mask is not None: sk &= mask
    mx=rgb.max(-1); mn=rgb.min(-1); S=(mx-mn)/np.maximum(mx,1e-3)
    hue = np.degrees(np.arctan2(Cr, Cb)) 
    return dict(n=int(sk.sum()), Y=np.median(Y[sk]).round(3), Y90=np.percentile(Y[sk],90).round(3), S=np.median(S[sk]).round(3), hue=np.median(hue[sk]).round(1), Cr=np.median(Cr[sk]).round(3), Cb=np.median(Cb[sk]).round(3))
if __name__=="__main__":
    for f in sys.argv[1:]:
        im=np.asarray(Image.open(f).convert('RGB')).astype(np.float32)/255
        print(f.split('/')[-1], stats(im))
