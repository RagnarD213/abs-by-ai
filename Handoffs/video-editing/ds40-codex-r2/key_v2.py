import numpy as np,cv2
from scipy.ndimage import distance_transform_edt

def screen(im):
 # Fit only sampled screen pixels. Less numerical noise and consistent spatial basis.
 h,w=im.shape[:2]; y,x=np.mgrid[:h:8,:w:8].astype(np.float32);x/=w;y/=h;s=im[::8,::8];r,g,b=s.transpose(2,0,1)
 sel=(g-r>.12)&(g-b>.12)
 X=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],-1)
 coef=np.linalg.lstsq(X[sel],s[sel],rcond=None)[0]
 yy,xx=np.mgrid[:h,:w].astype(np.float32);xx/=w;yy/=h
 return sum(coef[i]*q[:,:,None] for i,q in enumerate([np.ones_like(xx),xx,yy,xx*xx,xx*yy,yy*yy]))

def key(im):
 bg=screen(im);r,g,b=im.transpose(2,0,1);ex=np.maximum(g-np.maximum(r,b),0);be=np.maximum(bg[:,:,1]-np.maximum(bg[:,:,0],bg[:,:,2]),.08)
 a0=np.clip(1-ex/be,0,1); core=(a0>.97).astype('uint8');core=cv2.erode(core,np.ones((3,3),np.uint8))
 dist,inds=distance_transform_edt(1-core,return_indices=True);near=im[inds[0],inds[1]];delta=near-bg
 solved=np.sum((im-bg)*delta,axis=2)/np.maximum(np.sum(delta*delta,axis=2),.001)
 a=np.where((dist<16)&(a0<.995),solved,a0)
 a=np.clip((a-.055)/.92,0,1);a[dist>=16]=0;a=cv2.ximgproc.guidedFilter(im,a,2,.000015);a=np.clip(a,0,1)
 # Locate hair from real opaque foreground, then isolate refinement from skin/body.
 mid=core[:1600,350:1850];ys=np.where(mid.sum(1)>24)[0];top=int(ys[0]) if len(ys) else 650
 y=np.arange(im.shape[0])[:,None];hair=np.clip((top+470-y)/180,0,1).astype(np.float32);hair=np.broadcast_to(hair,a.shape)
 # Project screen/black-hair mixture using a local opaque hair estimate.
 # Preserve subpixel hair opacity instead of a global hard threshold.
 hair_a=np.clip((solved-.018)/.975,0,1);hair_a[dist>=20]=0
 hair_a=cv2.ximgproc.guidedFilter(im,hair_a,3,.00004);hair_a=np.clip(hair_a,0,1)
 base=a.copy();a=a*(1-hair)+hair_a*hair
 return a.astype(np.float32),bg.astype(np.float32),hair,top,near.astype(np.float32),base

def foreground(im,a,bg):
 f=np.clip(im-(1-a[:,:,None])*bg,0,a[:,:,None])
 f[:,:,1]=np.minimum(f[:,:,1],np.maximum(f[:,:,0],f[:,:,2]))
 return f
