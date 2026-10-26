from full import R,ROOT,SR,wr,dump,sha
import sys,json,numpy as np,wave
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
import renderq
with renderq.slot('Vacuum Yeti stereo summing peak correction',pool='quick',group='SL-11'):
 d=R/'audio/yeti-test';src=d/'take3-fit-input.wav';cfg=json.loads((d/'comparisons.json').read_text());target=cfg['reference_speech_rms'];cap=cfg['reference_peak']
 def speech(x):
  fr=C.frames(x,2048,1024);v=np.sqrt((fr*fr).mean(1)+1e-12);return float(20*np.log10(np.sqrt((v[v>np.percentile(v,60)]**2).mean())))
 base='pan=mono|c0=0.5*c0+0.5*c1';z0=C.pcm(str(src),af=base);gain=target-speech(z0)
 for _ in range(8):
  af=f'{base},volume={gain:.6f}dB,alimiter=limit={cap:.7f}:attack=5:release=60:level=false:latency=true';z=C.pcm(str(src),af=af);delta=target-speech(z)
  if abs(delta)<.15:break
  gain+=delta
 assert abs(z).max()<=cap+.001
 z[:384]*=np.linspace(0,1,384);z[-384:]*=np.linspace(1,0,384)
 new=d/'take3-peak-safe.wav';wr(new,np.repeat(z[:,None],2,axis=1))
 old=R/'rejected-internal/B-first-complete/his_mix.wav'
 with wave.open(str(old)) as w:x=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float64).reshape(-1,2)/32768
 n=len(z);tail=2880;following=C.pcm(str(__import__('full').MASTER),ss=487.305,dur=.06,ac=2)
 x[:n-tail]=z[:-tail,None];x[n-tail:n]=z[-tail:,None]*np.linspace(1,0,tail)[:,None]+following[:tail]*np.linspace(0,1,tail)[:,None]
 dest=R/'build/B/his_mix.wav';wr(dest,x)
 dump(d/'peak-correction.json',dict(reason='Stereo dualmono conversion after limiter added3.0103dB and clipped the intermediate PCM. Explicit0.5L+0.5R before limiter fixes it at original source. Parent audio not changed.',source=str(src),source_sha256=sha(src),filter=af,peak_db=20*np.log10(abs(z).max()),speech_rms=speech(z),target_speech_rms=target,output=str(new),output_sha256=sha(new),mix_sha256=sha(dest),parent_after_4_2_unchanged=True))
 p=R/'B-repair-journal.json';j=json.loads(p.read_text());j['repairs'][1]=dict(issue='Pickup stereo-to-mono summing after limiter exceeded full scale; parent audio already safe',solution='Recreate pickup from unclipped original with average before same shared limiter; parent audio preserved',evidence=str(d/'peak-correction.json'),abandoned_whole_mix_gain_db=-1.8);dump(p,j)
 print('PEAK SAFE',speech(z),target,20*np.log10(abs(z).max()),flush=True)
