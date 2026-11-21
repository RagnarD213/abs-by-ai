import subprocess, numpy as np, json, cv2
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
p=subprocess.run([FF,"-nostdin","-v","error","-ss","9","-t","22.5","-i","c1684_proxy.mp4","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
a=np.frombuffer(p,np.uint8).reshape(-1,540,960); f0=int(round(9*FPS))
ref=a[int(round(12.0*FPS))-f0]; tpl=ref[200:285,400:500].copy()      # shorts + upper thighs on the pillar at the top of a rep
ys=[]
for f in a:
    r=cv2.matchTemplate(f[150:400,380:520],tpl,cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(r)
    ys.append((loc[1]+150-200, mx))
y=np.array([v[0] for v in ys],float); c=np.array([v[1] for v in ys])
json.dump(dict(f0=f0,y=y.tolist(),c=c.tolist()),open("hs_curve3.json","w"))
print("min corr",c[int(1.5*FPS):int(21*FPS)].min())
for t in np.arange(10.0,30.6,0.1):
    i=int(round(t*FPS))-f0
    print(f"{t:.1f}:{y[i]:+.0f}",end="  " if round(t*10)%10!=9 else "\n")
