"""Exact first frame (master frame index) of each of Zeeshan's cuts: decode +-1 s with showinfo pts, find the diff peak."""
import json, subprocess, re, numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
C=json.load(open("src_cuts.json")); out={}
for S,v in C.items():
    res=[]
    for c in v["cuts"]:
        p=subprocess.run([FF,"-v","info","-copyts","-ss",f"{c-0.25:.3f}","-i","master.mp4","-frames:v","16","-vf","scale=160:90,showinfo","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True)
        pts=[float(m) for m in re.findall(r"pts_time:([0-9.]+)",p.stderr.decode())]
        fr=np.frombuffer(p.stdout,np.uint8).reshape(-1,90,160).astype(np.float32); d=np.abs(np.diff(fr,axis=0)).mean((1,2))
        k=int(np.argmax(d))+1; n=int(round(pts[k]*FPS))
        res.append(dict(t=round(n/FPS,4),n=n,score=round(float(d[k-1]),1),next=round(float(np.sort(d)[-2]),1)))
    out[S]=res; print(S,[(r["n"],r["t"],r["score"]) for r in res])
json.dump(out,open("zcuts_exact.json","w"),indent=1)
