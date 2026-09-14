import sys; sys.path.insert(0,sys.argv[1]); exec(open(sys.argv[1]+'/matte.py').read().split("# per-pixel per-channel ridge")[0])
Pf=np.stack([P[n] for n in FIT]); Of=np.stack([O[n] for n in FIT])
# band (window edge): ridge s,k as before
lam=len(FIT)*20.0; pm=Pf.mean(0); om=Of.mean(0)
cov=((Pf-pm)*(Of-om)).sum(0); var=((Pf-pm)**2).sum(0)
s=np.clip((cov+lam)/(var+lam),0,1.0); k=om-s*pm
# label: O = (1-a)P + aL, L = text colour from the brightest core pixels
core=overlay&(res>40)
L=np.percentile(Of.max(0)[core],90,axis=0); print('label colour',L.round(1))
num=((Of-Pf)*(L-Pf)).sum((0,3)); den=((L-Pf)**2).sum((0,3))+1e-3
a=np.clip(num/den,0,1)
label=overlay&~band
def compose(n,Pn):
    c=Pn.copy()
    c=np.where(band[...,None], s*Pn+k, c)
    c=np.where(label[...,None], (1-a[...,None])*Pn+a[...,None]*L, c)
    c=np.where(outside[...,None], O[n], c)
    return c
np.savez(S+'/matte2.npz',outside=outside,band=band,label=label,s=s,k=k,a=a,L=L)
e=[];el=[]
for n in TEST:
    d=np.abs(compose(n,P[n])-O[n]).mean(-1); e.append(d.mean()); el.append(d[label].mean())
print('held-out all %.2f label %.2f'%(np.mean(e),np.mean(el)))
n=2251; c=compose(n,P[n])
z=lambda im: cv2.resize(im[680:760,90:510],None,fx=2,fy=2,interpolation=cv2.INTER_NEAREST)
viz=np.concatenate([z(O[n]),z(c),np.clip(z(np.abs(c-O[n]))*6,0,255)],0).astype(np.uint8)
cv2.imwrite(S+'/matte2_check.png',cv2.cvtColor(viz,cv2.COLOR_RGB2BGR))
