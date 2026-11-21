"""usage: strip04.py <tag> <first> <last> <step> [x0,y0,x1,y1] [cols] -> round3/check/<tag>/strip_<first>_<last>.jpg (approved-frame coordinates)"""
import sys, cv2, numpy as np
W = "/Volumes/Extreme/_edit_work/ra04"; tag, a, b, s = sys.argv[1], *map(int, sys.argv[2:5])
box = tuple(map(int, sys.argv[5].split(","))) if len(sys.argv) > 5 and sys.argv[5] != "-" else (0, 0, 941, 1672); cols = int(sys.argv[6]) if len(sys.argv) > 6 else 6
cap = cv2.VideoCapture(f"{W}/round3/motion/{tag}.mp4"); F = []
while True:
    ok, f = cap.read()
    if not ok: break
    F.append(cv2.resize(f, (941, 1672), interpolation=cv2.INTER_AREA))
x0, y0, x1, y1 = box; T = []
for i in range(a, min(b, len(F)-1)+1, s):
    t = F[i][y0:y1, x0:x1].copy(); cv2.rectangle(t, (0, 0), (150, 34), (0, 0, 0), -1); cv2.putText(t, f"{i} {i/24:.2f}", (4, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2); T.append(t)
while len(T) % cols: T.append(np.zeros_like(T[0]))
img = np.vstack([np.hstack(T[r*cols:(r+1)*cols]) for r in range(len(T)//cols)])
sc = min(1.0, 2400/img.shape[1]); img = cv2.resize(img, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
o = f"{W}/round3/check/{tag}/strip_{a}_{b}.jpg"; cv2.imwrite(o, img, [cv2.IMWRITE_JPEG_QUALITY, 90]); print(o, img.shape)
