import sys, numpy as np
from PIL import Image
def stats(path, face=None, label=""):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float64)
    H,W,_ = im.shape
    R,G,B = im[...,0],im[...,1],im[...,2]
    Y = 0.2126*R+0.7152*G+0.0722*B
    mx = im.max(axis=2); mn = im.min(axis=2)
    sat = np.where(mx>0,(mx-mn)/np.maximum(mx,1),0)
    clip_hi = (mx>=252).mean()*100
    crush   = (mx<=3).mean()*100
    p1,p50,p99 = np.percentile(Y,[1,50,99])
    out = f"{label:26s} {W}x{H}  Y p1 {p1:5.1f} med {p50:5.1f} p99 {p99:5.1f}  sat {sat.mean()*100:4.1f}%  clipped-hi {clip_hi:4.2f}%  crushed {crush:4.2f}%"
    if face:
        x,y,w,h = face
        f = im[y:y+h, x:x+w]
        fr,fg,fb = f[...,0].mean(), f[...,1].mean(), f[...,2].mean()
        fy = 0.2126*fr+0.7152*fg+0.0722*fb
        fmx=f.max(axis=2); fmn=f.min(axis=2)
        fsat=np.where(fmx>0,(fmx-fmn)/np.maximum(fmx,1),0).mean()*100
        out += f"\n{'   face patch':26s} Y {fy:5.1f}  R {fr:5.1f} G {fg:5.1f} B {fb:5.1f}  R-B {fr-fb:+5.1f}  sat {fsat:4.1f}%"
    print(out)
if __name__=="__main__":
    import json
    for spec in sys.argv[1:]:
        parts=spec.split("|")
        path=parts[0]; label=parts[1] if len(parts)>1 else path
        face=tuple(int(v) for v in parts[2].split(",")) if len(parts)>2 else None
        stats(path,face,label)
