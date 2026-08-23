import numpy as np, subprocess, sys
f=sys.argv[1]
for off in [15,45,75,105,135,165,225]:
    cmd=["ffmpeg","-v","error","-ss",str(off),"-t","10","-i",f,"-af","pan=mono|c0=0.5*c0+0.5*c1","-ar","48000","-f","f32le","-"]
    raw=subprocess.run(cmd,capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
    if len(x)<48000: print(off,"short"); continue
    x=x-x.mean()
    # autocorrelation via FFT, look for echo peak in 3-15 ms
    N=1<<int(np.ceil(np.log2(len(x)*2)))
    X=np.fft.rfft(x,N); ac=np.fft.irfft(X*np.conj(X))
    ac0=ac[0]
    lo,hi=int(0.003*48000),int(0.015*48000)
    seg=ac[lo:hi]/ac0
    k=np.argmax(np.abs(seg))
    # also cross-channel check
    cmdL=["ffmpeg","-v","error","-ss",str(off),"-t","10","-i",f,"-af","pan=mono|c0=c0","-ar","48000","-f","f32le","-"]
    cmdR=["ffmpeg","-v","error","-ss",str(off),"-t","10","-i",f,"-af","pan=mono|c0=c1","-ar","48000","-f","f32le","-"]
    L=np.frombuffer(subprocess.run(cmdL,capture_output=True).stdout,dtype=np.float32).astype(np.float64)
    R=np.frombuffer(subprocess.run(cmdR,capture_output=True).stdout,dtype=np.float32).astype(np.float64)
    n=min(len(L),len(R)); L,R=L[:n]-L[:n].mean(),R[:n]-R[:n].mean()
    denom=(np.sqrt((L**2).sum()*(R**2).sum()) or 1)
    # lag search +-20ms
    Nc=1<<int(np.ceil(np.log2(n*2)))
    cc=np.fft.irfft(np.fft.rfft(L,Nc)*np.conj(np.fft.rfft(R,Nc)))
    lags=np.concatenate([cc[-int(0.02*48000):],cc[:int(0.02*48000)]])/denom
    kl=np.argmax(np.abs(lags))-int(0.02*48000)
    rms=np.sqrt((x**2).mean())
    print(f"t={off:3d}s rms={20*np.log10(rms+1e-12):6.1f}dB  echoPeak={seg[k]:+.3f}@{(lo+k)/48:.2f}ms  LRcorr={lags[np.argmax(np.abs(lags))]:+.3f}@{kl/48:.2f}ms")
