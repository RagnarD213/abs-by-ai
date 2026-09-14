import sys; sys.path.insert(0,sys.argv[1]); from load import *; import cv2
H=his(2190,2345); J=jmap(2190,2345); print('j range',J[0],J[12],J[-1])
V=story(V1,min(J),max(J)+1); j0=min(J)
np.save(sys.argv[1]+'/H.npy',H); np.save(sys.argv[1]+'/V.npy',V); np.save(sys.argv[1]+'/J.npy',np.array(J))
# shot boundary check: frame diff in his frames
d=[np.abs(H[i+1].astype(int)-H[i]).mean() for i in range(len(H)-1)]
for i in np.argsort(d)[-4:]: print('big diff between',2190+i,2190+i+1,round(d[i],1))
for n in (2215,2260,2295,2330):
    h=cv2.cvtColor(H[n-2190],cv2.COLOR_RGB2GRAY).astype(np.float32)/255
    s=cv2.cvtColor(V[J[n-2190]-j0],cv2.COLOR_RGB2GRAY).astype(np.float32)/255
    # init: window ~ x684..1242 wide 558 -> scale 558/1080=0.517 ; y top 98
    best=None
    for sc in np.arange(0.50,0.56,0.0025):
        sm=cv2.resize(s,None,fx=sc,fy=sc,interpolation=cv2.INTER_AREA)
        tpl=sm[100:-100,60:-60]
        r=cv2.matchTemplate(h[0:1080,600:1350],tpl,cv2.TM_CCOEFF_NORMED)
        _,mv,_,ml=cv2.minMaxLoc(r)
        if best is None or mv>best[0]: best=(mv,sc,ml[0]+600-60*1, ml[1]-100)
    print(n,'J',J[n-2190],'ncc %.4f scale %.4f x0 %d y0 %d'%best)
