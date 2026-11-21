"""Median luma / median HSV saturation / black point (p1) / white (p99) of BT.709-decoded frames. usage: measure.py label file t [vf]"""
import sys, subprocess, numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def grab(path, t, vf=""):
    f=(vf+"," if vf else "")+"scale=960:540:in_color_matrix=bt709:in_range=tv,format=rgb24"
    b=subprocess.run([FF,"-v","error","-ss",str(t),"-i",path,"-frames:v","1","-vf",f,"-f","rawvideo","-"],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(540,960,3).astype(np.float32)/255
def stats(im):
    y=0.2126*im[...,0]+0.7152*im[...,1]+0.0722*im[...,2]; mx=im.max(2); mn=im.min(2); s=np.where(mx>0,(mx-mn)/(mx+1e-6),0)
    return dict(luma=float(np.median(y)), sat=float(np.median(s)), black=float(np.percentile(y,1)), white=float(np.percentile(y,99)), clip=float((y>0.98).mean()*100),
                rgb=[float(np.median(im[...,k])) for k in range(3)])
if __name__=="__main__":
    lab,path,ts=sys.argv[1],sys.argv[2],sys.argv[3]; vf=sys.argv[4] if len(sys.argv)>4 else ""
    L=[stats(grab(path,float(t),vf)) for t in ts.split(",")]
    m={k:np.median([x[k] for x in L]) for k in ("luma","sat","black","white","clip")}
    print(f"{lab:14s} luma {m['luma']:.3f} sat {m['sat']:.3f} black {m['black']:.3f} white {m['white']:.3f} clip% {m['clip']:.1f}")
