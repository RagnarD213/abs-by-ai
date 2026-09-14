import sys; sys.path.insert(0,sys.argv[1]); from load import *; import cv2
S=sys.argv[1]
H=np.load(S+'/H.npy'); V=np.load(S+'/V.npy'); J=np.load(S+'/J.npy'); j0=J.min()
N0=2190
# refine geometry with ECC (scale+translation) on several frames
def warp(src,sc,tx,ty):
    M=np.float32([[sc,0,tx],[0,sc,ty]])
    return cv2.warpAffine(src,M,(1920,1080),flags=cv2.INTER_AREA if False else cv2.INTER_LINEAR)
# window rectangle from a clean frame: rows/cols where his frame differs from card colour
f=H[2250-N0].astype(int)
card=f[540,300]; print('card rgb',card, 'grid bg',f[20,20])
diff=np.abs(f-card).sum(2)>40
rows=np.where(diff[:,684:1242].mean(1)>0.9)[0]; cols=np.where(diff[98:974,:].mean(0)>0.9)[0]
print('rows',rows.min(),rows.max(),'cols',[c for c in cols if 600<c<1300][:1],[c for c in cols if 600<c<1300][-1:])
best=[]
for n in range(2205,2335,10):
    h=cv2.cvtColor(H[n-N0],cv2.COLOR_RGB2GRAY).astype(np.float32)
    s=cv2.cvtColor(V[J[n-N0]-j0],cv2.COLOR_RGB2GRAY).astype(np.float32)
    w=np.float32([[0.5175,0,684],[0,0.5175,38]])
    mask=np.zeros((1080,1920),np.uint8); mask[110:740,700:1230]=1   # above the label
    try:
        cc,w=cv2.findTransformECC(s,h,w,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,200,1e-6),mask,5)
        best.append(w.ravel()); 
    except cv2.error as e: print(n,'ecc fail')
b=np.array(best); print('affine median',np.median(b,0).round(4),'sd',b.std(0).round(4))
