#!/usr/bin/env python3
"""DS-105 R3 audio auditions only. Uses the maintained shared voice chain."""
from pathlib import Path
import os,sys,json,subprocess,hashlib,shutil
import numpy as np
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
W=Path(__file__).resolve().parents[1]; P=W.parent/'round2'
os.environ['GATE_GROUP']='DS-105';os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH']
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
def run(args,log):
 with (W/'evidence'/log).open('w') as f:
  p=subprocess.run([str(a) for a in args],stdout=f,stderr=subprocess.STDOUT)
 if p.returncode: raise RuntimeError(f'{log}: exit {p.returncode}; inspect evidence')
def sha(p): return C.sha256(str(p))
state=json.loads((W/'round-controller.json').read_text())
assert state['phase']=='complete' and state['productionOwner']=='01a182b7-eccb-7c82-aa31-9c48d25c0e76'
assert not (W/'records/delivered.json').exists(),'Already delivered; do not rebuild'
D=json.loads((W/'decisions.json').read_text());master=Path(D['priorMaster']);assert sha(master)==D['priorSha256']
(W/'execution-state.json').write_text(json.dumps(dict(disposition='in_progress',checkpoint='audio_build',revision=D['revisionId'],revision_application_count=1),indent=2))
selftest=W/'evidence/audio-selftest.log'
if not (W/'records/selftest-complete.json').exists():
 with selftest.open('w') as f:
  p=subprocess.run(['zsh',str(R/'.claude/skills/_shared/audio/selftest.sh')],stdout=f,stderr=subprocess.STDOUT)
 (W/'records/selftest-complete.json').write_text(json.dumps(dict(exit=p.returncode,log=str(selftest))))
 # Missing historical archive fixtures must remain visible. This source's exact-file
 # damage checks and listener review still run; no shared code or bounds are changed.
raw=P/'audio/cut-raw.wav';eq=json.loads((W.parent/'round1/audio/options.json').read_text())['A']['eq']
options={
 'A':dict(name='Current audio',source=str(master),process='Exact R2 AAC decoded; comparison applies constant volume only.'),
 'B':dict(name='Gentle cleanup',nr=4,clarity_dip=-0.7,clarity_lift=0.4),
 'C':dict(name='Stronger cleanup',nr=8,clarity_dip=-1.2,clarity_lift=0.7),
}
cur=C.pcm(str(master),ac=2)
run([C.FF,'-nostdin','-v','error','-y','-i',master,'-vn','-c:a','pcm_s24le','-ar','48000','-ac','2',W/'audio/A-full.wav'],'A-decode.log')
for key in ['B','C']:
 o=options[key]
 # The existing --eq filter-graph hook is recorded verbatim by the shared chain.
 # This is a restrained audition; no shared chain, gate or threshold is altered.
 af=f"afftdn=nr={o['nr']}:nf=-42:tn=1:gs=8,"+eq+f",equalizer=f=650:t=q:w=0.9:g={o['clarity_dip']},equalizer=f=2500:t=q:w=0.8:g={o['clarity_lift']}"
 o['filters']=af;o['source']=str(raw)
 run([sys.executable,R/'.claude/skills/_shared/audio/voice_chain.py','--in',raw,'--out',W/f'audio/{key}-chain.wav','--eq',af,'--target','-14.1','--tp','-2.5','--frame-lock',master,'--work',W/f'audio/work-{key}'],f'{key}-chain.log')
 # FFT denoisers can delay samples; measure against exact delivered speech and compensate.
 y=C.pcm(str(W/f'audio/{key}-chain.wav'),ac=1);x=C.pcm(str(master),ac=1)
 corr,delay,pol=C.xcorr(y[48000:21*48000],x[48000:21*48000],max_ms=100)
 o['measured_lag_samples_before']=int(delay);o['correlation_before']=float(corr)
 af2=(f'atrim=start_sample={delay},asetpts=N/SR/TB' if delay>0 else f'adelay={-delay}S:all=1' if delay<0 else 'anull')+',apad=whole_dur=63.964,atrim=0:63.964'
 run([C.FF,'-nostdin','-v','error','-y','-i',W/f'audio/{key}-chain.wav','-af',af2,'-c:a','pcm_s24le','-ar','48000','-ac','2',W/f'audio/{key}-full.wav'],f'{key}-align.log')
 C.stash_untreated(str(W/f'audio/{key}-full.wav'),C.pcm(str(raw),ss=1,dur=61.964,ac=1),'Exact same source lav/cut map before any processing. Alignment compensation is documented in options.json.')

# 13.72–25.80 is complete speech about breathing through the nose, no source audio join.
start=13.72;end=25.80;target=-16.0
for key,o in options.items():
 src=W/f'audio/{key}-full.wav';tmp=W/f'audio/{key}-excerpt.wav';out=W/f'review/media/{key}.wav'
 run([C.FF,'-nostdin','-v','error','-y','-i',src,'-af',f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS','-c:a','pcm_s24le',tmp],f'{key}-trim.log')
 I,TP,LRA=C.ebur(str(tmp));gain=target-I
 run([C.FF,'-nostdin','-v','error','-y','-i',tmp,'-af',f'volume={gain:.6f}dB','-c:a','pcm_s24le','-ar','48000','-ac','2',out],f'{key}-level.log')
 I2,TP2,LRA2=C.ebur(str(out));assert abs(I2-target)<=.15 and TP2<=-1.0,(key,I2,TP2)
 a=C.pcm(str(out),ac=1);levels=[]
 for n in range(0,len(a),48000):levels.append(float(20*np.log10(np.sqrt(np.mean(a[n:n+48000]**2))+1e-12)))
 # Refuse an audition that starts on room tone or includes a long empty stretch.
 q=np.sqrt(np.mean(a[:len(a)//4800*4800].reshape(-1,4800)**2,axis=1))
 active=20*np.log10(q+1e-12)>-35
 assert active[:5].any(),'No speech energy within first half second'
 longest=cur_run=0
 for yes in active:
  cur_run=0 if yes else cur_run+1;longest=max(longest,cur_run)
 assert longest<=15,'Possible pause exceeds 1.5 s'
 full=C.pcm(str(src),ac=1);base=C.pcm(str(master),ac=1)
 corr,delay,pol=C.xcorr(full[48000:21*48000],base[48000:21*48000],max_ms=100)
 assert abs(delay)<=2,(key,delay)
 o.update(file=str(out),sha256=sha(out),source_window=[start,end],seconds=len(a)/48000,lufs=I2,true_peak_db=TP2,lra=LRA2,comparison_gain_db=gain,per_second_rms_db=levels,longest_quiet_candidate_seconds=longest/10,post_align_delay_samples=int(delay),aligned_correlation=float(corr),speech_first_0_5s=True)
 ss,du=C.analysis_window(str(out));raw_excerpt=C.pcm(str(raw),ss=start+ss,dur=du,ac=1)
 C.stash_untreated(str(out),raw_excerpt,'Unprocessed same-lav exact excerpt with identical speech timing; prior source map verified in R2.')
 # Gate failures must be retained; they are evidence, never silently promoted to PASS.
 with (W/f'evidence/{key}-excerpt-gate.log').open('w') as f:
  p=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/audio_gate.py'),str(out)],stdout=f,stderr=subprocess.STDOUT)
 o['gate_exit']=p.returncode
(W/'records/options.json').write_text(json.dumps(options,indent=2))
assert sha(master)==D['priorSha256']
print(json.dumps({k:{x:v[x] for x in ['name','seconds','lufs','true_peak_db','post_align_delay_samples','gate_exit']} for k,v in options.items()},indent=2))
