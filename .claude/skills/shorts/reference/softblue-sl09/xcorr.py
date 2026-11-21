import subprocess, wave, numpy as np, sys
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
w=wave.open(sys.argv[1]); SR=48000; n=w.getnframes(); x=np.frombuffer(w.readframes(n),"<i2").reshape(-1,2).mean(1).astype(np.float32)
for t in [60,200,330,500,700,960,1010,1100,1170]:
    b=subprocess.run([FF,"-v","error","-ss",str(t),"-i","master.mp4","-t","3","-vn","-ac","1","-ar","48000","-f","s16le","-"],capture_output=True).stdout
    y=np.frombuffer(b,"<i2").astype(np.float32)
    seg=x[int(t*SR)-4800:int(t*SR)+len(y)+4800]
    c=np.correlate(seg,y,'valid'); k=int(np.argmax(c))-4800
    print(t, f"lag {k/SR*1000:+.1f} ms  corr {c.max()/np.sqrt((y**2).sum()*(seg[k+4800:k+4800+len(y)]**2).sum()):.3f}")
