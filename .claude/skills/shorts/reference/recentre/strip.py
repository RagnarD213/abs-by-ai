#!/usr/bin/env python3
"""strip.py OUT.png VIDEO t1 t2 ... -> one row of frames (with a centre line + torso marker from the gate json if available)"""
import sys, subprocess, cv2, numpy as np, os, json
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
out, vid = sys.argv[1], sys.argv[2]; ts=[float(t) for t in sys.argv[3:]]
tiles=[]
for t in ts:
    p=f"/tmp/_strip_{os.getpid()}.png"
    subprocess.run([FF,'-nostdin','-v','error','-y','-ss',str(t),'-i',vid,'-frames:v','1','-vf','scale=270:-2',p],check=True)
    im=cv2.imread(p); h,w=im.shape[:2]
    cv2.line(im,(w//2,0),(w//2,h),(0,0,255),1)
    cv2.putText(im,f"{t:.0f}s",(6,22),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)
    tiles.append(im)
cv2.imwrite(out,np.hstack(tiles)); print(out)
