import cv2,numpy as np,json,hashlib
from pathlib import Path
W=Path(__file__).parent;A=W/'audit';A.mkdir(exist_ok=True)
cap=cv2.VideoCapture(str(W/'review/media/sample.mp4'));frames=[];i=0
while True:
 ok,im=cap.read()
 if not ok:break
 if i in np.linspace(0,299,24).round().astype(int):
  sm=cv2.resize(im,(180,320));cv2.putText(sm,f'{i/29.97003:.2f}s',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.5,(20,70,160),1);frames.append(sm)
 i+=1
cap.release();assert i==300
cv2.imwrite(str(A/'scan-24.jpg'),np.concatenate([np.concatenate(frames[k:k+8],1) for k in range(0,24,8)]))
for start in [57,147,237]:
 cap=cv2.VideoCapture(str(W/'review/media/hair.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,start);rows=[]
 for i in range(start,start+6):
  ok,im=cap.read();assert ok
  row=np.concatenate([im[80:270,270:620],im[80:270,1020:1370]],1);cv2.putText(row,f'{i} / {i/29.97003:.3f}s',(5,18),cv2.FONT_HERSHEY_SIMPLEX,.45,(20,70,160),1);rows.append(row)
 cap.release();cv2.imwrite(str(A/f'native-motion-{start}.jpg'),np.concatenate(rows))
print('INSPECTION READY')
