import numpy as np, sys, json, cv2
sys.path.insert(0,'/Volumes/Expansion/_edit_work/ds40/r6/key')
import comp_opening as C
from PIL import Image
PINK=np.array([0.95,0.25,0.62],np.float32)
def tinted(src,k):
    G,a=C.dan_layer(f'{src}/f{k:04d}.npy')
    o=(np.clip(G*a[...,None]+PINK*(1-a[...,None]),0,1)*255)
    R,Gc,B=o[...,0],o[...,1],o[...,2]; lum=0.2126*R+0.7152*Gc+0.0722*B
    inner=cv2.erode((a>0.24).astype(np.uint8),np.ones((5,5),np.uint8)).astype(bool)
    t=inner&(lum<110)&(R-Gc>25)&(B-Gc>15); t[:1000]=False
    return int(t.sum()), o
if __name__=="__main__":
    a,b=sys.argv[1],sys.argv[2]; ks=[int(x) for x in sys.argv[3].split(',')]
    for k in ks:
        print(k, tinted(a,k)[0], '->', tinted(b,k)[0])
