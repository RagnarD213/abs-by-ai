"""lockstill variant: background from START; END kept on the person (pose segmentation of both frames), grown GROW px
everywhere except inside TIGHT boxes (where only a skin-colour mask of END, grown 3 px, is kept), plus KEEP boxes.
lock_tight.py START END OUT --grow 14 --keep x0,y0,x1,y1 --tight x0,y0,x1,y1"""
import argparse, cv2, numpy as np, mediapipe as mp
ap=argparse.ArgumentParser(); ap.add_argument("start"); ap.add_argument("end"); ap.add_argument("out")
ap.add_argument("--grow",type=int,default=14); ap.add_argument("--keep",action="append",default=[]); ap.add_argument("--tight",action="append",default=[])
a=ap.parse_args(); S=cv2.imread(a.start); E=cv2.imread(a.end)
def person(img):
    with mp.solutions.pose.Pose(static_image_mode=True,model_complexity=2,enable_segmentation=True) as P:
        r=P.process(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    return (r.segmentation_mask>0.3).astype(np.uint8)
m=np.maximum(person(S),person(E)); k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*a.grow+1,)*2); mg=cv2.dilate(m,k)
ycc=cv2.cvtColor(E,cv2.COLOR_BGR2YCrCb); skin=((ycc[...,1]>135)&(ycc[...,1]<185)&(ycc[...,2]>80)&(ycc[...,2]<135)&(ycc[...,0]>50)&(E[...,2].astype(int)-E[...,1].astype(int)>25)&(E[...,0].astype(int)*100>45*E[...,2].astype(int))).astype(np.uint8)
skin=cv2.morphologyEx(skin,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(skin); skin=np.isin(lab,[i for i in range(1,n) if st[i,4]>=400]).astype(np.uint8)
cs,_=cv2.findContours(skin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); skin=np.zeros_like(skin); cv2.drawContours(skin,cs,-1,1,-1)
skin=cv2.dilate(skin,np.ones((7,7),np.uint8))
for b in a.tight:
    x0,y0,x1,y1=map(int,b.split(",")); mg[y0:y1,x0:x1]=skin[y0:y1,x0:x1]
for b in a.keep:
    x0,y0,x1,y1=map(int,b.split(",")); mg[y0:y1,x0:x1]=1
w=cv2.GaussianBlur(mg.astype(np.float32),(7,7),0)[...,None]
cv2.imwrite(a.out,(E.astype(np.float32)*w+S.astype(np.float32)*(1-w)).round().astype(np.uint8))
