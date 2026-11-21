from pathlib import Path
import sys,json,hashlib,shutil,wave,os
import numpy as np
R=Path('/Volumes/Extreme/_edit_work/SL-11/round1');D=R/'audio/yeti-test';D.mkdir(parents=True,exist_ok=True)
ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'));import renderq
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
source=Path('/Users/danielrose/Desktop/vaccuum pickup.aifc');copy=D/source.name
if not copy.exists():shutil.copy2(source,copy)
assert hashlib.sha256(source.read_bytes()).hexdigest()==hashlib.sha256(copy.read_bytes()).hexdigest()
MASTER=ROOT/'claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4'
def wr(p,x):
 if x.ndim==1:x=x[:,None]
 with wave.open(str(p),'wb') as w:w.setparams((x.shape[1],2,48000,0,'NONE','not compressed'));w.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
with renderq.slot('Vacuum Yeti pickup ingest and word times',pool='quick',group='SL-11'):
 import torch,whisper
 torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','2')))
 x=C.pcm(str(copy),ac=2);wr(D/'pickup-original.wav',x)
 rows=[]
 for i in range(2):
  z=x[:,i];rows.append(dict(channel=i,peak_db=float(20*np.log10(abs(z).max()+1e-12)),rms_db=float(10*np.log10((z*z).mean()+1e-12)),samples_clipped=int((abs(z)>=.999).sum())))
 corr,lag,zero_corr=C.xcorr(x[:,0],x[:,1]);print('channels',rows,'xcorr',lag,corr,flush=True)
 mono=x.mean(1);sr16=__import__('scipy.signal',fromlist=['resample_poly']).resample_poly(mono,1,3).astype(np.float32)
 result=whisper.load_model('small.en').transcribe(sr16,fp16=False,condition_on_previous_text=False,word_timestamps=True,initial_prompt="Here's a mistake I see with a lot of beginners when they first start doing stomach vacuums.")
 out=dict(source=str(source),copied_source=str(copy),source_sha256=hashlib.sha256(copy.read_bytes()).hexdigest(),seconds=len(x)/48000,channels=rows,channel_lag_samples=int(lag),channel_correlation=float(corr),words=[dict(w=w['word'].strip(),a=w['start'],b=w['end']) for s in result['segments'] for w in s.get('words',[])],segments=[dict(a=s['start'],b=s['end'],text=s['text']) for s in result['segments']])
 (D/'ingest.json').write_text(json.dumps(out,indent=2));print(out['segments'],flush=True)
 ref=C.pcm(str(MASTER),ss=487.405,dur=35.319,ac=2);wr(D/'parent-following.wav',ref)
 control=C.pcm(str(MASTER),ss=482.405,dur=15,ac=2);wr(D/'parent-only-control.wav',control)
 print('INGEST COMPLETE',flush=True)
