"""Round 3 proof: new master vs round-2 master, every frame, with the two join offsets applied.
new n < 8979 -> old n ; 8979 <= n < 20952 -> old n+30 ; 20952..20968 are the 17 new frames at the 11:40 join ; n >= 20969 -> old n+13."""
import subprocess, json, numpy as np, wave
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
W="/Volumes/Extreme/_edit_work/ro16"; NEW=W+"/round3/RO16_MASTER.mp4"; OLD=W+"/round2/RO16_MASTER.mp4"
w,h=960,540; N=w*h
def rd(p): return subprocess.Popen([FF,"-v","error","-i",p,"-vf",f"scale={w}:{h}:flags=area:in_color_matrix=bt709:in_range=tv,format=gray","-f","rawvideo","-"],stdout=subprocess.PIPE,bufsize=N*8)
a=rd(NEW); b=rd(OLD); oi=0; rows=[]; n=0
def nextold():
    global oi
    buf=b.stdout.read(N); oi+=1
    return np.frombuffer(buf,np.uint8).astype(np.int16) if len(buf)==N else None
while True:
    buf=a.stdout.read(N)
    if len(buf)<N: break
    x=np.frombuffer(buf,np.uint8).astype(np.int16)
    if 20952<=n<20969: rows.append((n,None,None,None)); n+=1; continue
    want=n if n<8979 else (n+30 if n<20952 else n+13)
    while oi<want: nextold()
    y=nextold(); d=np.abs(x-y)
    blk=d.reshape(9,60,16,60).mean(axis=(1,3)).max()
    rows.append((n,want,float(d.mean()),float(blk))); n+=1
left=0
while nextold() is not None: left+=1
m=np.array([r[2] for r in rows if r[2] is not None]); k=np.array([r[3] for r in rows if r[3] is not None])
first=[r for r in rows if r[2] is not None and r[0]<8979]; mid=[r for r in rows if r[2] is not None and 8979<=r[0]<20952]; last=[r for r in rows if r[2] is not None and r[0]>=20969]
def st(R): 
    mm=np.array([r[2] for r in R]); kk=np.array([r[3] for r in R]); return dict(frames=len(R),mean=round(float(mm.mean()),4),max_mean=round(float(mm.max()),4),max_block=round(float(kk.max()),3))
worst=sorted([r for r in rows if r[3] is not None],key=lambda r:-r[3])[:15]
out=dict(new_frames=n,old_frames_left_over=left,compared=len(m),before_join1=st(first),between=st(mid),after_join2=st(last),
         worst_blocks=[dict(new=r[0],old=r[1],mean=round(r[2],3),block=round(r[3],3)) for r in worst],
         over_block_6=[dict(new=r[0],old=r[1],mean=round(r[2],3),block=round(r[3],3)) for r in rows if r[3] is not None and r[3]>6][:200])
json.dump(out,open(W+"/round3/pixel_diff.json","w"),indent=1); print(json.dumps({k2:v for k2,v in out.items() if k2!='over_block_6'},indent=1)); print("frames over block 6:",len(out["over_block_6"]))
# ---- untreated audio (the lav on the timeline, before the voice chain): sample-exact outside the join windows
def wav(p):
    v=wave.open(p); return np.frombuffer(v.readframes(v.getnframes()),np.int16).astype(np.int32)
A=wav(NEW+".untreated.wav"); B=wav(OLD+".untreated.wav"); SR=48000; FPS=30000/1001
def s(f): return int(round(f/FPS*SR))
segs=[("0 to join 1",0,s(8979)-s(8),0),("join 1 to join 2",s(8979)+s(8),s(20952)-s(8),s(9009)-s(8979)),("after join 2",s(20969)+s(8),len(A),s(20982)-s(20969))]
for name,a0,a1,off in segs:
    xa=A[a0:a1]; xb=B[a0+off:a1+off]; L=min(len(xa),len(xb)); d=np.abs(xa[:L]-xb[:L])
    print(f"untreated audio {name}: {L} samples, max abs diff {int(d.max())} (of 32767), differing samples {int((d>1).sum())}")
