import numpy as np, subprocess
from scipy.ndimage import gaussian_filter
from io_ import rgb, RAW, SRC
import build
from build import grade, rgb_to_yuv420, encode, W, H, RAW_OFF
buf=np.load('seg_4500.npy'); f0=4500
light=gaussian_filter(rgb(SRC,4640,1)[0],(40,40,0))           # his flash frame, light only
his=rgb(SRC,4634,6)                                            # 4634..4639 for target brightness
lum=lambda x:(x@np.array([0.2126,0.7152,0.0722])).mean()
tgt=[lum(his[i]) for i in range(6)]
out=[]
for n in range(4635,4640):
    cam=grade(rgb(RAW,n+RAW_OFF,1)[0])
    # his ramp measured as the fraction of the way from his pre-flash frame to full flash
    frac=(tgt[n-4634]-tgt[0])/(lum(light)-tgt[0])
    best=None
    base=lum(cam); goal=base+frac*(lum(light)-base)
    for t in np.linspace(0,1,201):
        g=1-(1-cam)*(1-light*t)
        e=abs(lum(g)-goal)
        if best is None or e<best[0]: best=(e,t,g)
    print(n,'his frac %.3f t %.3f'%(frac,best[1]))
    out.append(best[2].astype(np.float32))
yuv=rgb_to_yuv420(np.stack(out))
for i,n in enumerate(range(4635,4640)): buf[n-f0]=yuv[i]
np.save('seg_4500.npy',buf); encode(buf,'seg_4500.h264')
