from pathlib import Path
import sys,json,os,wave,hashlib
import numpy as np
R=Path('/Volumes/Extreme/_edit_work/SL-11/round1');D=R/'audio/yeti-test';ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'));import renderq
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C,voice_chain as VC
SR=48000
MASTER=ROOT/'claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4'
def rd(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float64).reshape(-1,w.getnchannels())/32768

def wr(p,x):
 if x.ndim==1:x=np.repeat(x[:,None],2,axis=1)
 with wave.open(str(p),'wb') as w:w.setparams((x.shape[1],2,SR,0,'NONE','not compressed'));w.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
def speech(x):
 fr=C.frames(x,2048,1024);v=np.sqrt((fr*fr).mean(1)+1e-12);return float(20*np.log10(np.sqrt((v[v>np.percentile(v,60)]**2).mean())))
with renderq.slot('Vacuum Yeti take comparisons using shared fitted EQ',pool='quick',group='SL-11'):
 x=rd(D/'pickup-original.wav').mean(1);following=C.pcm(str(MASTER),ss=487.305,dur=11,ac=2);ref=following[int(.1*SR):int(8.5*SR)].mean(1);bands=C.analyse(ref)[0];rb=dict(bands=bands.tolist());target=speech(ref);cap=float(abs(following).max());rows=[]
 for i,(a,b) in enumerate([(1.46,5.84),(6.48,10.72),(11.50,15.70)],1):
  raw=x[round(a*SR):round(b*SR)];wr(D/f'take{i}-fit-input.wav',raw)
  fd=D/f'fit{i}';fd.mkdir(exist_ok=True);af,gains,_=VC.fit_eq(str(D/f'take{i}-fit-input.wav'),rb,str(fd),iters=12)
  matched=C.pcm(str(D/f'take{i}-fit-input.wav'),af=af);err=C.analyse(matched)[0]-bands
  detail=dict(take=i,source_range=[a,b],eq=af,gains=gains,raw_edt=C.edt(np.tile(raw,3)),reference_edt=C.edt(np.tile(ref,2)),tone_error_mean=float(abs(err).mean()),tone_error_max=float(abs(err).max()),versions=[])
  for tag,z in [('raw',raw),('matched',matched)]:
   gain=target-speech(z);z=z*10**(gain/20)
   # Match speech level; protect peaks without compression or gating.
   if abs(z).max()>cap: z*=cap/abs(z).max()
   z[:384]*=np.linspace(0,1,384);z[-384:]*=np.linspace(1,0,384)
   solo=D/f'take{i}-{tag}.wav';wr(solo,z)
   # Last60ms of tail overlaps the film pre-roll; full first word is preserved at +100ms.
   tail=2880;p=np.repeat(z[:,None],2,axis=1);n=len(p);out=np.concatenate([p[:-tail],p[-tail:]*np.linspace(1,0,tail)[:,None]+following[:tail]*np.linspace(0,1,tail)[:,None],following[tail:]],axis=0);join=D/f'join-take{i}-{tag}.wav';wr(join,out)
   detail['versions'].append(dict(tag=tag,solo=str(solo),join=str(join),join_at_seconds=n/SR,overlap_start=(n-tail)/SR,gain_db=gain,peak_db=float(20*np.log10(abs(z).max()+1e-12)),speech_rms=speech(z),sha256=hashlib.sha256(join.read_bytes()).hexdigest()))
  rows.append(detail);print('TAKE',i,'tone error',detail['tone_error_mean'],detail['tone_error_max'],'room',detail['raw_edt'],detail['reference_edt'],flush=True)
 (D/'comparisons.json').write_text(json.dumps(dict(scope='Audio test, not final gate or user approval',reference_speech_rms=target,reference_peak=cap,following_parent_start=487.305,reference_bands=bands.tolist(),takes=rows),indent=2));print('COMPARISONS READY',flush=True)
