import json,subprocess,hashlib
from pathlib import Path
import numpy as np
from scipy import signal
R=Path(__file__).resolve().parents[1];ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
FF=str(ROOT/'Media/video_edit/bin/ffmpeg');MASTER=str(ROOT/'claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4')
old=json.loads((R/'audio-preservation.json').read_text()) if (R/'audio-preservation.json').exists() else {}
def read(path,start,dur):
    c=[FF,'-nostdin','-v','error','-ss',str(start),'-i',str(path),'-t',str(dur),'-vn','-ar','48000','-ac','2','-f','f32le','-']
    return np.frombuffer(subprocess.check_output(c),'<f4').reshape(-1,2)
for it in json.loads((R/'items-context.json').read_text()):
    if not it.get('context'):continue
    p=R/'review'/it['context'];sha=hashlib.sha256(p.read_bytes()).hexdigest()
    if old.get(it['id'],{}).get('sha256')==sha:continue
    d=it['context_frames']/(30000/1001);x=read(p,0,d);ref=read(MASTER,it['context_parent_start'],d);n=min(len(x),len(ref));x=x[:n];ref=ref[:n]
    a=x.mean(1);b=ref.mean(1);cc=signal.correlate(a,b,method='fft');lags=signal.correlation_lags(n,n);sel=np.abs(lags)<=960;lag=int(lags[sel][np.argmax(cc[sel])])
    if lag>0:a=a[lag:];b=b[:-lag]
    elif lag<0:a=a[:lag];b=b[-lag:]
    gain=float(np.dot(a,b)/max(np.dot(b,b),1e-12));corr=float(np.corrcoef(a,b)[0,1])
    old[it['id']]=dict(sha256=sha,lag_samples=lag,lag_ms=lag/48,correlation=corr,gain_db=float(20*np.log10(max(abs(gain),1e-12))),scope='Comparison to original mix; not an audio-gate stamp or listening audit')
    (R/'audio-preservation.json').write_text(json.dumps(old,indent=2));print(it['id'],old[it['id']],flush=True)
