from pathlib import Path
import sys,json,numpy as np
from scipy.signal import correlate,correlation_lags
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
from qa_full_r2 import sha
ref=O/'options/C_Balanced.wav';movie=W/'review/media/dad-bod-r2-scripted.mp4';start=485/(30000/1001)+.02
x=C.pcm(str(ref),ac=1);y=C.pcm(str(W/'qa/scripted/Dan-exact-stereo-final-AAC.wav'),ss=16/(30000/1001)+.02,dur=30,ac=1);n=min(len(x),len(y));x=x[:n];y=y[:n];xd=x[::3];yd=y[::3];co=correlate(yd,xd,method='fft');la=correlation_lags(len(yd),len(xd));mask=abs(la)<1600;lag=int(la[mask][co[mask].argmax()])*3
if lag>0:y=y[lag:];x=x[:len(y)]
elif lag<0:x=x[-lag:];y=y[:len(x)]
n=min(len(x),len(y));x=x[:n];y=y[:n];gain=float(np.dot(x,y)/np.dot(x,x));err=y-x*gain
rows=[]
for i in range(0,n,5*48000):
 a,b=x[i:i+5*48000],y[i:i+5*48000]
 if len(a)<48000:continue
 g=float(np.dot(a,b)/np.dot(a,a));rows.append(dict(start=i/48000,seconds=len(a)/48000,correlation=float(np.corrcoef(a,b)[0,1]),fitted_gain_db=float(20*np.log10(abs(g))),residual_vs_signal_db=float(20*np.log10(np.sqrt(np.mean((b-g*a)**2))/np.sqrt(np.mean(b*b))))))
rec=dict(reference=str(ref),reference_sha256=sha(ref),actual_final=str(movie),video_sha256=sha(movie),film_matching_start=start,lag_samples=lag,lag_ms=lag/48,correlation=float(np.corrcoef(x,y)[0,1]),fitted_gain_db=float(20*np.log10(abs(gain))),residual_vs_signal_db=float(20*np.log10(np.sqrt(np.mean(err**2))/np.sqrt(np.mean(y*y)))),windows=rows,interpretation='Signal comparison only; it tests whether the actual export preserves the selected audition, not perceptual quality approval.')
(W/'qa/scripted/selected-voice-identity.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2))
