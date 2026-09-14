import sys; sys.path.insert(0,sys.argv[1]); from load import *; import cv2
S=sys.argv[1]; H=np.load(S+'/H.npy').astype(np.float32); V=np.load(S+'/V.npy'); J=np.load(S+'/J.npy'); j0=J.min(); N0=2190
SC,TX,TY=0.5177,683.07,37.89; C=np.load(S+'/C_0.9.npy')
def warp(src):
    s=cv2.GaussianBlur(src.astype(np.float32),(0,0),0.9)
    return cv2.warpAffine(s,np.float32([[SC,0,TX],[0,SC,TY]]),(1920,1080),flags=cv2.INTER_LINEAR)
def grade(x):
    x=x/255.; r,g,b=x[...,0],x[...,1],x[...,2]
    return np.stack([r,g,b,r*r,g*g,b*b,r*g,r*b,g*b,np.ones_like(r)],-1)@C
def rrect(x0,y0,x1,y1,rad,ss=4):
    W,Hh=1920,1080; m=np.zeros((Hh*1,W*1),np.float32)
    big=np.zeros(((y1-y0+4)*ss,(x1-x0+4)*ss),np.uint8)
    X0,Y0=2*ss,2*ss; X1,Y1=X0+int((x1-x0)*ss),Y0+int((y1-y0)*ss); R=int(rad*ss)
    cv2.rectangle(big,(X0+R,Y0),(X1-R,Y1),255,-1); cv2.rectangle(big,(X0,Y0+R),(X1,Y1-R),255,-1)
    for cx,cy in ((X0+R,Y0+R),(X1-R,Y0+R),(X0+R,Y1-R),(X1-R,Y1-R)): cv2.circle(big,(cx,cy),R,255,-1)
    sm=cv2.resize(big,((x1-x0+4),(y1-y0+4)),interpolation=cv2.INTER_AREA)/255.
    m[int(y0)-2:int(y0)-2+sm.shape[0], int(x0)-2:int(x0)-2+sm.shape[1]]=sm
    return m[...,None]
BB=(slice(60,1010),slice(650,1280))
def predict(n, src_frames, jj0, mask):
    return grade(warp(src_frames[J[n-N0]-jj0]))
