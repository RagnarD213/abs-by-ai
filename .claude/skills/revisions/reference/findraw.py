import subprocess,sys,numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def pcm(p,ss=None,t=None,sr=8000):
    c=[FF,"-v","error"]
    if ss is not None: c+=["-ss",str(ss)]
    if t is not None: c+=["-t",str(t)]
    c+=["-i",p,"-ac","1","-ar",str(sr),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,dtype=np.float32).astype(np.float64)
cut,raw,t0,dur=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
a=pcm(cut,t0,dur); b=pcm(raw)
a=(a-a.mean()); b=(b-b.mean())
n=len(a)
c=np.correlate(b,a,mode="valid")
cs=np.cumsum(np.insert(b,0,0)); cs2=np.cumsum(np.insert(b*b,0,0))
s=cs[n:]-cs[:-n]; s2=cs2[n:]-cs2[:-n]
var=np.maximum(s2-s*s/n,1e-9)
r=c/np.sqrt(var*(a*a).sum())
i=int(np.argmax(r))
print(f"cut {t0:.2f}s -> raw {i/8000:.2f}s   r={r[i]:.3f}")
