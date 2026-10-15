import cv2,numpy as np,sys
# paste_box.py ORIGINAL EDITED OUT x0,y0,x1,y1 [...]: OUT = ORIGINAL everywhere except inside the boxes (feathered 10 px)
o,e,out=sys.argv[1:4]; O=cv2.imread(o).astype(np.float32); E=cv2.imread(e).astype(np.float32)
m=np.zeros(O.shape[:2],np.float32)
for b in sys.argv[4:]:
    x0,y0,x1,y1=map(int,b.split(',')); m[y0:y1,x0:x1]=1
m=cv2.GaussianBlur(m,(21,21),0)[...,None]
cv2.imwrite(out,(E*m+O*(1-m)).round().astype(np.uint8)); print(out,round(float(m.mean()),3))
