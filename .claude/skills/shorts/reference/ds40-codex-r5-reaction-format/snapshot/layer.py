import numpy as np,cv2
from scipy import ndimage as ndi
from recipe.grade import grade

def clean(d):
 Fp=d[...,:3].astype(np.float32);a=d[...,3].astype(np.float32)
 lab,n=ndi.label(a>.03)
 if n:
  sizes=np.bincount(lab.ravel());keep=sizes>=400;keep[0]=False;m=ndi.binary_dilation(keep[lab],iterations=3)
  a=np.where(m,a,0);Fp=np.where(m[...,None],Fp,0)
 far=ndi.distance_transform_edt(a<.25)>3
 an=np.where(far,np.clip((a-.15)/.85,0,1),a)
 Fp*=np.where(a>1e-4,an/np.maximum(a,1e-4),0)[...,None];a=an
 F=np.where(a[...,None]>.01,Fp/np.maximum(a[...,None],1e-3),0)
 return grade(F,'warm')*a[...,None],a

def place(bg,Fp,a,s=1.,x=0,y=0,fade=0,wrap=.12):
 h,w=a.shape;ww,hh=round(w*s),round(h*s)
 if (ww,hh)!=(w,h):Fp=cv2.resize(Fp,(ww,hh),interpolation=cv2.INTER_AREA);a=cv2.resize(a,(ww,hh),interpolation=cv2.INTER_AREA)
 if fade:
  fw=round(fade);v=np.ones(ww,np.float32);v[-fw:]=np.linspace(1,0,fw);Fp*=v[None,:,None];a*=v[None,:]
 y0=max(0,y);y1=min(bg.shape[0],y+hh);x0=max(0,x);x1=min(bg.shape[1],x+ww)
 if y0>=y1 or x0>=x1:return bg
 aa=a[y0-y:y1-y,x0-x:x1-x,None];fg=Fp[y0-y:y1-y,x0-x:x1-x];back=bg[y0:y1,x0:x1]
 comp=fg+(1-aa)*back
 if wrap:
  inv=1-aa;cov=cv2.GaussianBlur(inv[...,0],(0,0),10)[...,None];bb=cv2.GaussianBlur(back*inv,(0,0),10);wm=wrap*cov*aa
  comp=comp*(1-wm)+bb/np.maximum(cov,1e-3)*wm
 out=bg.copy();out[y0:y1,x0:x1]=comp
 return np.clip(out,0,1)

def hair(a):
 sub=a[240:680,230:850];rows=np.where((sub>.08).sum(1)>=4)[0]
 assert len(rows),'hair not measured'
 y=240+int(rows[0]);yy,xx=np.where(a[y:y+190,230:850]>.6)
 return y,float(np.median(xx)+230)
