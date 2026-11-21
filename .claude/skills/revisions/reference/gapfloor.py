import subprocess,sys,numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def pcm(p,ss,t):
    r=subprocess.run([FF,"-v","error","-ss",str(ss),"-t",str(t),"-i",p,"-ac","1","-ar","48000","-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(r,dtype=np.float32).astype(np.float64)
def report(p,label,wins):
    print(f"--- {label}")
    for ss,t in wins:
        x=pcm(p,ss,t)
        if len(x)<48000: print("  no audio"); continue
        n=480
        m=len(x)//n
        fr=x[:m*n].reshape(m,n)
        rms=20*np.log10(np.sqrt((fr**2).mean(axis=1))+1e-9)
        p5=np.percentile(rms,5); p50=np.percentile(rms,50)
        # band energy in the quietest 10% frames
        q=fr[np.argsort(rms)[:max(1,m//10)]].ravel()
        F=np.abs(np.fft.rfft(q[:len(q)//480*480].reshape(-1,480),axis=1)).mean(axis=0)
        fq=np.fft.rfftfreq(480,1/48000)
        bands=[(80,500),(500,2000),(2000,6000)]
        be=[20*np.log10(F[(fq>=a)&(fq<b)].mean()+1e-9) for a,b in bands]
        print(f"  {ss:5.0f}s+{t:3.0f}  gapfloor p5 {p5:6.1f} dB  median {p50:6.1f}  gap bands 80-500 {be[0]:6.1f} | 500-2k {be[1]:6.1f} | 2-6k {be[2]:6.1f}")
if __name__=="__main__":
    import json
    p=sys.argv[1]; label=sys.argv[2]
    wins=[tuple(float(v) for v in w.split(":")) for w in sys.argv[3:]]
    report(p,label,wins)
