# Precise boundaries in HIS V2: per-frame consecutive MAD + luma in each changed window.
import subprocess, numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
V2="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/Daniel HQ Ad 2 V2 HD.mp4"
FPS=30000/1001; W,H=192,108
def frames(a,d):
    cmd=[FF,"-v","error","-ss",f"{a:.3f}","-t",f"{d:.3f}","-i",V2,"-vf",f"fps=30000/1001,scale={W}:{H}:flags=area,format=gray","-f","rawvideo","-pix_fmt","gray","-"]
    b=subprocess.run(cmd,capture_output=True).stdout; n=len(b)//(W*H)
    return np.frombuffer(b[:n*W*H],np.uint8).reshape(n,H,W).astype(np.float32)
for a,d in [(2.5,6.0),(12.5,3.0),(67.5,7.5),(148.5,8.5),(191.5,18.0)]:
    F=frames(a,d); mad=np.abs(np.diff(F,axis=0)).mean(axis=(1,2)); lum=F.mean(axis=(1,2))
    print(f"--- window {a}-{a+d}: median mad {np.median(mad):.2f}")
    for k in range(len(mad)):
        t=a+(k+1)/FPS
        if mad[k]>8 or lum[k+1]>150: print(f"  t={t:8.3f}  frame {round(t*FPS)}  mad {mad[k]:6.1f}  luma {lum[k+1]:5.1f}")
