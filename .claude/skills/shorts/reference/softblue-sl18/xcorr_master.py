import subprocess, wave, numpy as np
M="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Codex Content Videos/Im 41 Wasted Life - RO-25/Im 41 Wasted Life | codex | 16x9 | RO-25.mp4"
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
w=wave.open("master_audio.wav"); sr=48000
for t in [35.0,80.0,150.0,350.0,380.0,405.0,600.0,700.0]:
    w.setpos(int(t*sr)); a=np.frombuffer(w.readframes(sr*2),"<i2").reshape(-1,2).mean(1)
    b=np.frombuffer(subprocess.run([FF,"-v","error","-ss",f"{t}","-i",M,"-t","2","-vn","-ac","2","-ar","48000","-f","s16le","-"],capture_output=True).stdout,"<i2").reshape(-1,2).mean(1)
    n=min(len(a),len(b)); a,b=a[:n],b[:n]
    c=np.correlate(a[2400:-2400],b,"valid") if False else None
    best=None
    for lag in range(-1200,1201,4):
        x=a[2400+lag:n-2400+lag]; y=b[2400:n-2400]; r=np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y)+1e-9)
        if best is None or r>best[1]: best=(lag,r)
    print(t, "lag ms %.2f r %.3f"%(best[0]/48, best[1]))
