import subprocess,sys,numpy as np,json
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
src=sys.argv[1]; f0,f1=5957,6006
p=subprocess.run([FF,"-v","error","-i",src,"-vf",f"select='between(n\\,{f0}\\,{f1})'","-vsync","0","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
a=np.frombuffer(p,np.uint8).reshape(-1,1080,1920).astype(float)
ref=a[5975-f0]
def g(x): return np.abs(np.diff(x,axis=0))
R=g(ref[560:900,1110:1164])  # right side: pool/background column, few confetti? use edge
res={}
for i,L in enumerate(a):
    best=None
    for dy in range(-4,16):
        T=g(L[560+dy:900+dy,1110:1164])
        A=R-R.mean(); B=T-T.mean(); c=(A*B).sum()/np.sqrt((A*A).sum()*(B*B).sum())
        if best is None or c>best[0]: best=(c,dy)
    res[f0+i]=best[1]; print(f0+i,best[1],round(best[0],3))
json.dump(res,open('dy.json','w'))
