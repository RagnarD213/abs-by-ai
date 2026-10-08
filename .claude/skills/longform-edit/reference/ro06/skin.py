"""Skin-anchored exposure: median luma / saturation / hue of skin-coloured pixels (hue 8-38 deg, sat .25-.75, val>.12)."""
import sys, colorsys, numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro06/recipe")
from measure import grab
def skin(im):
    r,g,b=im[...,0],im[...,1],im[...,2]; mx=im.max(2); mn=im.min(2); d=mx-mn+1e-6
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60; s=d/(mx+1e-6)
    m=(h>8)&(h<38)&(s>0.25)&(s<0.78)&(mx>0.12)
    y=0.2126*r+0.7152*g+0.0722*b
    return dict(n=float(m.mean()*100), y=float(np.median(y[m])), y90=float(np.percentile(y[m],90)), s=float(np.median(s[m])), h=float(np.median(h[m])), p995=float(np.percentile(y,99.5)), med=float(np.median(y))) if m.sum()>500 else None
if __name__=="__main__":
    lab,path,ts=sys.argv[1],sys.argv[2],sys.argv[3]; vf=sys.argv[4] if len(sys.argv)>4 else ""
    L=[x for x in (skin(grab(path,float(t),vf)) for t in ts.split(",")) if x]
    m={k:np.median([x[k] for x in L]) for k in L[0]}
    print(f"{lab:13s} skin% {m['n']:4.1f} skinY {m['y']:.3f} skinY90 {m['y90']:.3f} skinS {m['s']:.3f} hue {m['h']:.1f} | frame med {m['med']:.3f} p99.5 {m['p995']:.3f}")
