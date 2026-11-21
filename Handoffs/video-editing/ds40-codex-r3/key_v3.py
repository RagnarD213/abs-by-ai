"""Shot-stable green/hair colour and five-frame motion-aware fine-hair alpha.
Only used in a measured hair region; reviewed R2 body pixels stay in place.
"""
import cv2,numpy as np
from scipy.ndimage import distance_transform_edt

def key(im,bg):
 # Green excess is linear in a foreground/background mixture. Unlike nearest
 # opaque-pixel projection, this estimate has no switching nearest index.
 chroma=lambda x:x[:,:,1]-.5*(x[:,:,0]+x[:,:,2])
 bc=chroma(bg);ic=chroma(im)
 a0=np.clip(1-ic/np.maximum(bc,.08),0,1)
 core=(a0>.98).astype(np.float32)
 # Smooth normalized local estimates, blended continuously with a fixed neutral
 # dark-hair fallback where no opaque strand is nearby.
 den=cv2.GaussianBlur(core,(0,0),22)
 col=cv2.GaussianBlur(im*core[:,:,None],(0,0),22)
 near=(col+np.array([.105,.105,.095],np.float32)*.025)/(den[:,:,None]+.025)
 fc=chroma(near)
 a=np.clip((bc-ic)/np.maximum(bc-fc,.08),0,1)
 a=np.clip((a-.012)/.988,0,1)
 a=cv2.ximgproc.guidedFilter(im,a,2,.000025);a=np.clip(a,0,1)
 # Keep screen noise away from the actual head with a broad, soft support band.
 d=distance_transform_edt(a0<.7)
 a*=np.clip((75-d)/25,0,1)
 gray=cv2.cvtColor((im*255).astype('uint8'),cv2.COLOR_RGB2GRAY)
 return {'im':im,'a':a.astype(np.float32),'gray':gray,'near':near}

def align(other,cur,maker):
 h,w=cur['a'].shape;y,x=np.mgrid[:h,:w].astype(np.float32)
 flow=maker.calc(cur['gray'],other['gray'],None)
 back=maker.calc(other['gray'],cur['gray'],None)
 mx=x+flow[:,:,0];my=y+flow[:,:,1]
 wa=cv2.remap(other['a'],mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 wg=cv2.remap(other['gray'],mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 wb=cv2.remap(back,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
 fb=np.linalg.norm(flow+wb,axis=2)
 cf=np.exp(-((wg.astype(np.float32)-cur['gray'])/12)**2)*np.exp(-(fb/1.5)**2)
 cf*=np.exp(-((wa-cur['a'])/.25)**2)
 return wa,cf

def stabilize(items,idx,maker):
 cur=items[idx];acc=cur['a'].copy();weights=np.ones_like(acc)
 for j in range(max(0,idx-2),min(len(items),idx+3)):
  if j==idx:continue
  a,c=align(items[j],cur,maker);c*=.85 if abs(j-idx)==1 else .45
  acc+=a*c;weights+=c
 a=acc/weights
 # Only semitransparent pixels need temporal filtering, solid detail untouched.
 blend=np.clip((1-cur['a'])/.15,0,1)
 return cur['a']*(1-blend)+a*blend

def composite(cur,a,bg,field,grade):
 aa=a[:,:,None];fg=np.clip(cur['im']-(1-aa)*bg,0,aa)
 # A continuous local colour estimate replaces unstable reconstructed edge colour.
 n=cur['near'].copy();n[:,:,1]=np.minimum(n[:,:,1],.5*(n[:,:,0]+n[:,:,2]))
 t=(1-a)*.92
 fg=fg*(1-t[:,:,None])+n*aa*t[:,:,None]
 fg[:,:,1]=np.minimum(fg[:,:,1],np.maximum(fg[:,:,0],fg[:,:,2]))
 return np.clip(grade(fg/np.maximum(aa,.001),'warm')*aa+(1-aa)*np.array(field,np.float32),0,1)
