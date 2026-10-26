from pathlib import Path
import sys,json,wave,hashlib,shutil
import numpy as np
R=Path('/Volumes/Extreme/_edit_work/SL-11/round1');D=R/'audio/yeti-test';ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');sys.path.insert(0,str(ROOT/'.claude/skills/_shared/renderq'));import renderq
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
SR=48000
def rd(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float64).reshape(-1,w.getnchannels())/32768

def wr(p,x):
 if x.ndim==1:x=np.repeat(x[:,None],2,axis=1)
 with wave.open(str(p),'wb') as w:w.setparams((x.shape[1],2,SR,0,'NONE','not compressed'));w.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
def speech(x):
 fr=C.frames(x,2048,1024);v=np.sqrt((fr*fr).mean(1)+1e-12);return float(20*np.log10(np.sqrt((v[v>np.percentile(v,60)]**2).mean())))
MASTER=ROOT/'claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4'
with renderq.slot('Vacuum level-matched Yeti comparisons',pool='quick',group='SL-11'):
 cfg=json.loads((D/'comparisons.json').read_text());old=D/'internal-rejected-global-cap';old.mkdir(exist_ok=True);shutil.copy2(D/'comparisons.json',old/'comparisons.json')
 following=C.pcm(str(MASTER),ss=487.305,dur=11,ac=2);target=cfg['reference_speech_rms'];cap=cfg['reference_peak'];rows=[]
 for row in cfg['takes']:
  i=row['take'];raw=rd(D/f'take{i}-fit-input.wav').mean(1);row['versions']=[]
  for tag,eq in [('raw','anull'),('matched',row['eq'])]:
   z0=C.pcm(str(D/f'take{i}-fit-input.wav'),af=eq);gain=target-speech(z0)
   for _ in range(3):
    af=f'{eq},volume={gain:.5f}dB,alimiter=limit={cap:.6f}:attack=5:release=60:level=false:latency=true'
    z=C.pcm(str(D/f'take{i}-fit-input.wav'),af=af);delta=target-speech(z)
    if abs(delta)<.25:break
    gain+=delta
   assert abs(speech(z)-target)<.6,(i,tag,speech(z),target)
   corr,lag,zero=C.xcorr(z,z0)
   assert abs(lag)<=2,(i,tag,lag)
   z[:384]*=np.linspace(0,1,384);z[-384:]*=np.linspace(1,0,384)
   solo=D/f'take{i}-{tag}.wav';join=D/f'join-take{i}-{tag}.wav'
   for p in [solo,join]:
    if p.exists():shutil.copy2(p,old/p.name)
   wr(solo,z);tail=2880;p=np.repeat(z[:,None],2,axis=1);n=len(p);out=np.concatenate([p[:-tail],p[-tail:]*np.linspace(1,0,tail)[:,None]+following[:tail]*np.linspace(0,1,tail)[:,None],following[tail:]],axis=0);wr(join,out)
   row['versions'].append(dict(tag=tag,solo=str(solo),join=str(join),join_at_seconds=n/SR,overlap_start=(n-tail)/SR,gain_db=gain,limiter=af,delay_samples=lag,peak_db=float(20*np.log10(abs(z).max()+1e-12)),speech_rms=speech(z),difference_from_reference_db=speech(z)-target,sha256=hashlib.sha256(join.read_bytes()).hexdigest()))
   print('TAKE',i,tag,'RMS',speech(z),'target',target,'gain',gain,'delay',lag,flush=True)
  rows.append(row)
 cfg['takes']=rows;cfg['scope']='Correctly level-matched audio test with shared finish limiter; not final gate or user approval';(D/'comparisons.json').write_text(json.dumps(cfg,indent=2));print('CORRECTED COMPARISONS READY',flush=True)
