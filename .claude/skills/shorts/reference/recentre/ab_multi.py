"""Shipped vs proposed crop at several points ACROSS a shot -- a single midpoint frame
is not enough to judge framing on a shot where the subject moves."""
import cv2, numpy as np, json, os, subprocess, sys
SP="/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/39032698-3f11-4a8d-9382-8b0b6599b994/scratchpad"
ROOT="/Users/danielrose/Documents/Claude/Projects/Abs By AI/YouTube Long Form Video Content"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC={'v2':'V2 - How To Get Real Six Pack Abs With AI(2) - READY FOR UPLOAD.mp4',
     'v3':'V3 - My Top 10 Tips For Getting Six Pack Abs(3).mp4 - READY FOR UPLOAD.mp4',
     'v6':'V6 - 3 Minute Total Body Home Workout(2).mp4 - READY FOR UPLOAD.mp4'}
def grab(build,t):
    o=f"{SP}/ab/{build}_{t:.2f}.png"; os.makedirs(f"{SP}/ab",exist_ok=True)
    if not os.path.exists(o):
        subprocess.run([FF,'-y','-v','error','-ss',f'{t:.3f}','-i',os.path.join(ROOT,SRC[build]),'-frames:v','1',o],check=True)
    return cv2.imread(o)
def crop(im,x,cw=608):
    W=im.shape[1]; x0=int(round(min(max(x*W-cw/2,0),W-cw)))
    return cv2.resize(im[:,x0:x0+cw],(200,356),interpolation=cv2.INTER_AREA)
build=sys.argv[1]; out=sys.argv[2]; shots=sys.argv[3:]
meta={s['shot']:s for s in json.load(open(f"{SP}/fr/{build}.json"))['shots']}
fix=json.load(open(f"{SP}/fix_{build}.json"))
rows=[]
for n in shots:
    m=meta[n]; f=fix[n]; K=5
    strip=[]
    for i in range(K):
        t=m['start']+m['dur']*(i+0.5)/K
        im=grab(build,t)
        pair=np.hstack([crop(im,f['x_old']),np.zeros((356,4,3),np.uint8),crop(im,f['x_new'])])
        strip.append(pair); strip.append(np.zeros((356,14,3),np.uint8))
    body=np.hstack(strip)
    lab=np.zeros((24,body.shape[1],3),np.uint8)
    cv2.putText(lab,f"{n}   SHIPPED {f['x_old']:.3f} | PROPOSED {f['x_new']:.3f}  ({f['off_px']:+.0f}px)",
                (4,17),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
    rows.append(np.vstack([lab,body]))
w=max(r.shape[1] for r in rows)
rows=[np.hstack([r,np.zeros((r.shape[0],w-r.shape[1],3),np.uint8)]) for r in rows]
cv2.imwrite(out,np.vstack(rows)); print(out)
