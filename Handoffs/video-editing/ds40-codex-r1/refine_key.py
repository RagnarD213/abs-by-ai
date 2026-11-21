import cv2,numpy as np
from scipy.ndimage import distance_transform_edt
from pathlib import Path
W=Path(__file__).parent

def screen(im):
 h,w=im.shape[:2]; yy,xx=np.mgrid[:h,:w].astype(np.float32);xx/=w;yy/=h
 r,g,b=im.transpose(2,0,1);sel=(g-r>.10)&(g-b>.10)
 X=np.stack([np.ones_like(xx),xx,yy,xx*xx,xx*yy,yy*yy],-1)
 coef=np.linalg.lstsq(X[sel][::50],im[sel][::50],rcond=None)[0]
 return X@coef

def key(im):
 bg=screen(im);r,g,b=im.transpose(2,0,1)
 ex=np.maximum(g-np.maximum(r,b),0);be=np.maximum(bg[:,:,1]-np.maximum(bg[:,:,0],bg[:,:,2]),.08)
 a=np.clip(1-ex/be,0,1)
 core=(a>.97).astype('uint8');core=cv2.erode(core,np.ones((3,3),np.uint8))
 # A clean opaque interior supplies real foreground colors for mixed edge pixels.
 dist,inds=distance_transform_edt(1-core,return_indices=True)
 near=im[inds[0],inds[1]]
 delta=near-bg
 solved=np.sum((im-bg)*delta,axis=2)/np.maximum(np.sum(delta*delta,axis=2),.001)
 band=(dist<16)&(a<.995)
 a=np.where(band,solved,a)
 a=np.clip((a-.055)/.92,0,1); a[dist>=16]=0
 a=cv2.ximgproc.guidedFilter(im,a,2,.000015);a=np.clip(a,0,1)
 fg=im-(1-a[:,:,None])*bg
 fg=np.clip(fg,0,a[:,:,None])
 # Keep skin untouched. Remove remaining actual green dominance at the edge.
 fg[:,:,1]=np.minimum(fg[:,:,1],np.maximum(fg[:,:,0],fg[:,:,2]))
 return fg,a

if __name__=='__main__':
 im=cv2.imread(str(W/'selected.png'))[:,:,::-1].astype(np.float32)/255
 fg,a=key(im)
 for name,col in [('light',[.84,.87,.89]),('dark',[.08,.1,.13])]:
  o=fg+(1-a[:,:,None])*np.array(col)
  cv2.imwrite(str(W/f'refine-{name}.png'),(np.clip(o,0,1)[:,:,::-1]*255).astype('uint8'))
