import numpy as np, os
from PIL import Image
SPD=os.environ['SPD']
FR={37.0:(1.00,0,0),57.0:(1.00,0,0),125.0:(1.00,0,0),33.0:(1.12,0,-50),
    53.0:(1.20,0,-60),77.0:(1.20,0,-60),205.0:(1.20,0,-60),145.0:(1.22,-20,-60)}
RAW=[];HIS=[]
for t,(sc,dx,dy) in FR.items():
    R=Image.open(f'{SPD}/geo/raw_{t}.png').convert('RGB')
    w=int(round(1920/sc)); h=int(round(1080/sc))
    x0=max(0,min((1920-w)//2+dx,1920-w)); y0=max(0,min((1080-h)//2+dy,1080-h))
    RAW.append(np.asarray(R.crop((x0,y0,x0+w,y0+h)).resize((480,270)),np.float32))
    HIS.append(np.asarray(Image.open(f'{SPD}/geo/his_{t}.png').convert('RGB').resize((480,270)),np.float32))
RAW=np.stack(RAW); HIS=np.stack(HIS)

# --- pass 1: tone curve fitted on the CENTRE box only (vignette ~= 1 there)
cy,cx=slice(80,190),slice(170,310)
curves={}
for ch in range(3):
    a=RAW[:,cy,cx,ch].ravel(); b=HIS[:,cy,cx,ch].ravel()
    pts=[(float(np.percentile(a,p)),float(np.percentile(b,p))) for p in
         [0,2,5,10,20,30,40,50,60,70,80,90,95,98,100]]
    curves['RGB'[ch]]=pts

def apply_curve(x, pts):
    xs=np.array([p[0] for p in pts]); ys=np.array([p[1] for p in pts])
    o=np.argsort(xs); xs,ys=xs[o],ys[o]
    keep=np.concatenate([[True], np.diff(xs)>0.5]); xs,ys=xs[keep],ys[keep]
    return np.interp(x,xs,ys)

TONED=np.stack([apply_curve(RAW[...,ch], curves['RGB'[ch]]) for ch in range(3)],-1)

# --- pass 2: radial gain his/toned
H,Wd=270,480
yy,xx=np.mgrid[0:H,0:Wd]
r=np.hypot((xx-Wd/2)/(Wd/2),(yy-H/2)/(H/2))
lt=TONED.mean(-1); lh=HIS.mean(-1)
m=(lt>25)&(lt<245)
bins=np.linspace(0,1.45,16); prof=[]
for i in range(len(bins)-1):
    sel=m&(r[None]>=bins[i])&(r[None]<bins[i+1])
    prof.append(float(np.median(lh[sel]/np.maximum(lt[sel],1))) if sel.sum()>500 else np.nan)
prof=np.array(prof); prof=prof/np.nanmax(prof[:3])
print('vignette gain vs radius:')
for i,p in enumerate(prof):
    if not np.isnan(p): print(f'   r {bins[i]:.2f}-{bins[i+1]:.2f}  gain {p:.3f}')
print('\ntone curve (centre-fitted):')
for i,pc in enumerate([0,2,5,10,20,30,40,50,60,70,80,90,95,98,100]):
    print(f'  p{pc:>3d}  ' + '  '.join(f'{curves[n][i][0]:6.1f}->{curves[n][i][1]:6.1f}' for n in 'RGB'))
def cs(n):
    pts=curves[n]; out=[]
    for x,y in pts:
        x=max(0,min(255,x)); y=max(0,min(255,y))
        if out and x<=out[-1][0]+0.6: continue
        out.append((x,y))
    return ' '.join(f'{x/255:.4f}/{y/255:.4f}' for x,y in out)
print("\nGRADE=\"curves=r='%s':g='%s':b='%s'\"" % (cs('R'),cs('G'),cs('B')))
np.save('vignette_profile.npy', np.stack([ (bins[:-1]+bins[1:])/2, prof]))
