import sys, json, subprocess, numpy as np
sys.path.insert(0,'recipe'); sys.argv=['x']; import build
FF=build.FF
bad=[]
for sg in build.all_segments():
    p=build.render_seg(sg)
    raw=subprocess.run([FF,"-v","error","-i",p,"-frames:v","3","-vf","scale=320:180,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(3,180,320).astype(float)
    d01=abs(a[0]-a[1]).mean(); d12=abs(a[1]-a[2]).mean()
    if d01<0.05: bad.append((sg['o0'],round(sg['o0']/build.FPS,2),p,round(d01,3),round(d12,3)))
for b in bad: print(b)
json.dump(bad,open('round2/logs/dup_segments.json','w'))
