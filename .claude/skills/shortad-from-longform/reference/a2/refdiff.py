# Diff Muhammad's V1 (480p) against V2 HD: per-frame picture MAD + per-second audio corr/level.
import subprocess, numpy as np, json, sys
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
V1="/Volumes/Extreme/_edit_work/ad2-vert/reference.mp4"
V2="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/Daniel HQ Ad 2 V2 HD.mp4"
OUT="/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/4afe28ae-761a-4b5f-b5b6-9c5282b4cec6/scratchpad"
W,H=96,54
def frames(p):
    cmd=[FF,"-v","error","-i",p,"-vf",f"scale={W}:{H}:flags=area,format=gray","-r","30000/1001","-f","rawvideo","-pix_fmt","gray","-"]
    b=subprocess.run(cmd,capture_output=True).stdout
    n=len(b)//(W*H); return np.frombuffer(b[:n*W*H],np.uint8).reshape(n,H,W).astype(np.float32)
a=frames(V1); b=frames(V2); n=min(len(a),len(b)); print("frames",len(a),len(b))
a=a[:n]; b=b[:n]
mad=np.abs(a-b).mean(axis=(1,2))
np.save(f"{OUT}/refdiff_mad.npy",mad)
fps=30000/1001
# runs of changed frames
thr=6.0
ch=mad>thr
runs=[];i=0
while i<n:
    if ch[i]:
        j=i
        while j<n and ch[j]: j+=1
        runs.append((i,j)); i=j
    else: i+=1
# merge runs closer than 15 frames
m=[]
for r in runs:
    if m and r[0]-m[-1][1]<15: m[-1]=(m[-1][0],r[1])
    else: m.append(r)
print("median MAD %.2f  p90 %.2f  max %.2f"%(np.median(mad),np.percentile(mad,90),mad.max()))
for s,e in m:
    if e-s>=2: print("CHANGED %7.2f - %7.2f s  (%d fr)  meanMAD %.1f"%(s/fps,e/fps,e-s,mad[s:e].mean()))
# audio
def wav(p):
    cmd=[FF,"-v","error","-i",p,"-vn","-ac","1","-ar","16000","-f","f32le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32)
x=wav(V1); y=wav(V2); L=min(len(x),len(y)); x=x[:L]; y=y[:L]
print("audio samples",len(x),len(y))
sr=16000; secs=L//sr
bad=[]
for s in range(secs):
    xa=x[s*sr:(s+1)*sr]; ya=y[s*sr:(s+1)*sr]
    rx=np.sqrt((xa**2).mean()+1e-12); ry=np.sqrt((ya**2).mean()+1e-12)
    c=float(np.corrcoef(xa,ya)[0,1]) if rx>1e-5 and ry>1e-5 else 1.0
    g=20*np.log10(ry/rx)
    if c<0.95 or abs(g)>1.0: bad.append((s,round(c,3),round(float(g),2)))
print("audio: seconds with corr<0.95 or |gain|>1dB:",len(bad),"of",secs)
for t in bad[:80]: print("  AUDIO DIFF t=%4d corr=%.3f gain=%+.2f dB"%t)
# global lag check
seg=slice(10*sr,20*sr)
xs=x[seg]-x[seg].mean(); ys=y[seg]-y[seg].mean()
best=max(range(-200,201),key=lambda k: float(np.dot(xs[200:-200],ys[200+k:len(ys)-200+k])))
print("global lag (samples @16k) V2 vs V1 over 10-20s:",best)
