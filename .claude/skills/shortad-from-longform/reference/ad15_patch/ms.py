import numpy as np, pickle
from scipy.ndimage import gaussian_filter
from io_ import rgb, RAW, SRC
from PIL import Image as I
h,w=1080,1920
yy,xx=np.mgrid[0:h,0:w]; RR=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(w/2))**2)
SIGS=(6,20,60,180)
def feats(R,rr):
    r,g,b=R[...,0],R[...,1],R[...,2]; l=0.2126*r+0.7152*g+0.0722*b
    F=[np.ones_like(r),r,g,b,r*r,g*g,b*b,r*g,g*b,r*b,l**3]
    for s in SIGS:
        d=l-gaussian_filter(l,s,mode='nearest'); F+= [d, d*l, d*d]
        lb=gaussian_filter(l,s,mode='nearest'); F+=[lb, lb*lb]
    q=rr*rr; F+=[q,q*q,q*l,q*q*l,q*r,q*g,q*b]
    return np.stack(F,-1)
if __name__=="__main__":
    train=[4753,4759,4765,4777,4783,4789]; test=[4771,4792]
    rng=np.random.default_rng(1); idx=rng.choice(h*w,80000,replace=False)
    X=[];Y=[]
    for f in train:
        R=rgb(RAW,f+2872,1)[0]; H=rgb(SRC,f,1)[0]
        X.append(feats(R,RR).reshape(h*w,-1)[idx]); Y.append(gaussian_filter(H,(1,1,0)).reshape(-1,3)[idx])
    X=np.concatenate(X); Y=np.concatenate(Y)
    C=np.linalg.lstsq(X,Y,rcond=None)[0]; pickle.dump(C,open('ms.pkl','wb'))
    def grade(R,rr): return np.clip((feats(R,rr).reshape(-1,X.shape[1])@C).reshape(h,w,3),0,1)
    for f in train[:2]+test:
        R=rgb(RAW,f+2872,1)[0]; H=rgb(SRC,f,1)[0]; G=grade(R,RR)
        print(f,'test' if f in test else 'train','MAE %.2f lowfreq %.2f'%(np.abs(G-H).mean()*255,np.abs(gaussian_filter(G,(3,3,0))-gaussian_filter(H,(3,3,0))).mean()*255))
    for f in (4690,):
        R=rgb(RAW,f+2872,1)[0]; H=rgb(SRC,f,1)[0]; G=grade(R,RR)
        sc=1.2; cw,ch=w/sc,h/sc; x0=(w-cw)/2; y0=(h-ch)/2-90
        Gc=np.stack([np.asarray(I.fromarray(G[...,c]).transform((w,h),I.EXTENT,(x0,y0,x0+cw,y0+ch),I.BICUBIC)) for c in range(3)],-1)
        m=np.ones((h,w),bool); m[850:,:]=False
        print(f,'PUNCH MAE %.2f'%(np.abs(Gc-H)[m].mean()*255))
        I.fromarray((np.clip(np.concatenate([H,Gc],1),0,1)*255).astype(np.uint8)).resize((1920,540)).save('frames/punchtest.jpg')
