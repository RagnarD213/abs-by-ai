import sys; sys.path.insert(0,sys.argv[1]); from load import *; import cv2
S=sys.argv[1]; H=np.load(S+'/H.npy').astype(np.float32); V=np.load(S+'/V.npy'); J=np.load(S+'/J.npy'); j0=J.min(); N0=2190
SC,TX,TY=0.5177,683.07,37.89
def warp(src,sig):
    s=cv2.GaussianBlur(src.astype(np.float32),(0,0),sig) if sig>0 else src.astype(np.float32)
    return cv2.warpAffine(s,np.float32([[SC,0,TX],[0,SC,TY]]),(1920,1080),flags=cv2.INTER_LINEAR,borderValue=(-1,-1,-1))
def feats(x):
    x=x/255.; r,g,b=x[...,0],x[...,1],x[...,2]
    return np.stack([r,g,b,r*r,g*g,b*b,r*g,r*b,g*b,np.ones_like(r)],-1)
Y0,Y1,X0,X1=100,972,688,1238
lab=(slice(735,835),slice(760,1150))
for sig in (0.0,0.6,0.9):
    Xs=[];Ys=[]
    for n in range(2202,2292,6):
        p=warp(V[J[n-N0]-j0],sig)[Y0:Y1,X0:X1]; h=H[n-N0][Y0:Y1,X0:X1]
        m=np.ones(p.shape[:2],bool); m[lab[0].start-Y0:lab[0].stop-Y0,:]=False
        Xs.append(feats(p)[m][::7]); Ys.append(h[m][::7])
    X=np.concatenate(Xs); Y=np.concatenate(Ys); C,_,_,_=np.linalg.lstsq(X,Y,rcond=None)
    # evaluate on held-out frames
    errs=[]
    for n in range(2205,2295,6):
        p=feats(warp(V[J[n-N0]-j0],sig)[Y0:Y1,X0:X1])@C; h=H[n-N0][Y0:Y1,X0:X1]
        e=np.abs(p-h); e[lab[0].start-Y0:lab[0].stop-Y0,:]=np.nan; errs.append(np.nanmean(e))
    print('sigma',sig,'mean abs err (0-255) %.2f'%np.mean(errs))
    np.save(S+f'/C_{sig}.npy',C)
