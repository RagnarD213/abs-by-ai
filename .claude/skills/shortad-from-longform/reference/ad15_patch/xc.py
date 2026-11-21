import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
sr,ref=wavfile.read('ref.wav'); ref=ref.astype(float)
for ch in ('raw_L.wav','raw_R.wav'):
    _,raw=wavfile.read(ch); raw=raw.astype(float)
    for (a,b) in [(143,150.9),(150.9,152.9),(152.9,155.1),(155.1,160),(140,165)]:
        s=ref[int(a*sr):int(b*sr)]; s=s-s.mean()
        c=fftconvolve(raw,s[::-1],mode='valid')
        e=np.sqrt(np.maximum(fftconvolve(raw**2,np.ones(len(s)),mode='valid'),1e-9))*np.sqrt((s**2).sum())
        n=c/e; k=n.argmax()
        print(ch,a,b,'raw_t=%.4f'%(k/sr),'offset=%.4f'%(k/sr-a),'ncc=%.3f'%n[k])
