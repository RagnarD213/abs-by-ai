import sys; sys.path.insert(0,sys.argv[1]); from model import *
from scipy import ndimage
ALL=list(range(2202,2339)); FIT=ALL[::2]; TEST=ALL[1::2]
Y,X=BB
P={n:predict(n,V,j0,None)[Y,X] for n in ALL}
O={n:H[n-N0][Y,X] for n in ALL}
Ost=np.stack([O[n] for n in ALL]); Pst=np.stack([P[n] for n in ALL])
tstd=Ost.std(0).mean(-1); mean=Ost.mean(0)
green=(mean[...,1]>mean[...,0]+2)&(mean[...,2]<mean[...,1]-15)
outside=green&(tstd<3)
lab,_=ndimage.label(outside); border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
outside=np.isin(lab,list(border)); outside=ndimage.binary_closing(outside,iterations=2)
inside=~ndimage.binary_dilation(outside,iterations=8)
res=np.abs(Ost-Pst).mean((0,3))
overlay=ndimage.binary_dilation(res>7,iterations=3)&inside
band=~outside&~inside
reg=overlay|band
print('outside',outside.sum(),'band',band.sum(),'overlay',overlay.sum())
# per-pixel per-channel ridge regression O = s*P + k on FIT frames, only on reg pixels
Pf=np.stack([P[n] for n in FIT]); Of=np.stack([O[n] for n in FIT])
lam=len(FIT)*20.0
pm=Pf.mean(0); om=Of.mean(0)
cov=((Pf-pm)*(Of-om)).sum(0); var=((Pf-pm)**2).sum(0)
s=np.clip((cov+lam*1.0)/(var+lam),0,1.15)          # prior s=1 when variance is small (inside-window pixel)
s_out=np.clip(cov/(var+1e-3),0,1.15)
k=om-s*pm
np.savez(S+'/matte.npz',outside=outside,inside=inside,reg=reg,s=s,k=k)
def compose(n,Pn):
    c=np.where(reg[...,None], s*Pn+k, Pn)
    c=np.where(outside[...,None], O[n], c)    # static card: his own pixels
    return c
e_in=[];e_reg=[];e_all=[]
for n in TEST:
    c=compose(n,P[n]); d=np.abs(c-O[n]).mean(-1)
    e_all.append(d.mean()); e_reg.append(d[reg].mean()); e_in.append(d[inside&~reg].mean())
print('held-out mean abs err: all %.2f  plain-window %.2f  overlay/edge %.2f'%(np.mean(e_all),np.mean(e_in),np.mean(e_reg)))
n=2251; c=compose(n,P[n])
viz=np.concatenate([O[n],c,np.clip(np.abs(c-O[n])*6,0,255)],1).astype(np.uint8)
cv2.imwrite(S+'/matte_check.png',cv2.cvtColor(viz,cv2.COLOR_RGB2BGR))
