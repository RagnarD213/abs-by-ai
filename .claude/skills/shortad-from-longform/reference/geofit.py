from PIL import Image
import numpy as np, statistics
ts=[9.0,33.0,37.0,53.0,57.0,77.0,125.0,145.0,205.0,229.0]
W,H=480,270
out=[]
for t in ts:
    R=np.asarray(Image.open(f'geo/raw_{t}.png').convert('L').resize((960,540)),dtype=np.float32)
    his=np.asarray(Image.open(f'geo/his_{t}.png').convert('L').resize((W,H)),dtype=np.float32)
    b=his-his.mean(); bn=np.linalg.norm(b)
    bb=None
    for sc in np.arange(1.00,1.42,0.02):
        w=int(round(960/sc)); h=int(round(540/sc))
        for dx in range(-30,31,5):
            for dy in range(-30,31,5):
                x0=(960-w)//2+dx; y0=(540-h)//2+dy
                if x0<0 or y0<0 or x0+w>960 or y0+h>540: continue
                c=np.asarray(Image.fromarray(R[y0:y0+h, x0:x0+w]).resize((W,H)),dtype=np.float32)
                a=c-c.mean()
                r=float((a*b).sum()/(np.linalg.norm(a)*bn+1e-9))
                if bb is None or r>bb[0]: bb=(r,sc,dx*2,dy*2)
    out.append(bb); print(f'  t={t:6.1f}  corr {bb[0]:.3f}  scale {bb[1]:.2f}  dx {bb[2]:+d} dy {bb[3]:+d}', flush=True)
print('\nmedian scale %.3f  dx %+.0f  dy %+.0f' % (statistics.median(b[1] for b in out), statistics.median(b[2] for b in out), statistics.median(b[3] for b in out)))
