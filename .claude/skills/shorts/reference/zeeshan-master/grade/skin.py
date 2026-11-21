import sys, subprocess, numpy as np, os
from PIL import Image
PM='/Volumes/Extreme/_edit_work/sl04/build/recentre/personmask'
def stats(paths):
    subprocess.run([PM,'/tmp/sl04skin']+paths,capture_output=True)
    out=[]
    for p in paths:
        a=np.asarray(Image.open(p).convert('RGB')).astype(np.float32)/255
        m=np.asarray(Image.open('/tmp/sl04skin/'+os.path.basename(p)[:-4]+'.mask.png').resize((a.shape[1],a.shape[0])))>127
        r,g,b=a[...,0],a[...,1],a[...,2]
        Y=0.2126*r+0.7152*g+0.0722*b
        sk=m&(r>g)&(g>=b*0.9)&((r-b)>0.05)&(Y>0.06)
        mx=a.max(-1);mn=a.min(-1);S=(mx-mn)/np.maximum(mx,1e-6)
        out.append((os.path.basename(p),float(np.median(Y[sk])),float(np.median(S[sk])),float(np.percentile(Y[sk],95)),float((mx[sk]>0.95).mean()),int(sk.sum())))
    return out
if __name__=='__main__':
    for n,l,s,p,c,k in stats(sys.argv[1:]): print(f"{n:14s} skin luma {l:.3f} sat {s:.3f} p95 {p:.3f} blown {c*100:4.1f}% px={k}")
